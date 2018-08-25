from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import random, string, re

from .models import Link


def home(request):
    if request.user.is_authenticated:
        return redirect('shortener/')
    return render(request, 'shortener/home.html')


def index(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/links/shortener')
        else:
            render(request, 'shortener/index.html', {'error': "Wrong password or username."})
    return render(request, 'shortener/index.html')
    

def logoutUser(request):
    logout(request)
    return redirect('/links/')


def registration(request):
    if request.method == 'POST':
        name = request.POST['user']
        password = request.POST['password']
        email = request.POST['email']

        if isTaken(name):
            return render(request, 'shortener/registration.html', {'error': 'Username already taken.'})

        if name != '' and password != '' and email != '':
            user = User.objects.create_user(name, email, password)
            return redirect('/links/login')
        else:
            return render(request, 'shortener/registration.html', {'error': 'Fill in all fields.'})

    return render(request, 'shortener/registration.html')   


def isTaken(name):
    if User.objects.filter(username=name).exists():
        return True
    else:
        return False

def redirectShort(request, query):
    if Link.objects.filter(short_tag=query).exists():
        url = get_object_or_404(Link, short_tag=query)
        url.transitions += 1
        url.save()
        
        return redirect(url.original_link)
    else:
        return render(request, 'shortener/error.html', {'f':query})
            

def shortenLink(request):
    if request.user.is_authenticated:
        numberOfRows = 15
        links = Link.objects.filter(user=request.session['_auth_user_id'])
        args = {'links':links.order_by('-pub_date')[:numberOfRows]}

        if request.method == 'POST':
            link = request.POST['text']
            link = makeAbsolute(link)
            site = request.get_host()
            shortLink = shorten(site)
            l = Link.objects.create(user=request.session['_auth_user_id'],pub_date=timezone.now(), 
                                    original_link=link, short_link=site+'/links/'+shortLink, short_tag=shortLink)

            return redirect('/links/shortener')
        return render(request, 'shortener/shortener.html', args)
    else:
        return redirect('/links')


def makeAbsolute(link):
    if re.match(r'http.://', link) is not None:
        return link
    if not 'www.' in link:
        newLink = 'www.' + link
        link = newLink
    if not r'http.://' in link:
        newLink = 'https://' + link
        link = newLink
    return link


def shorten(site):
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while(True):
        shortLink = ''.join(random.choice(char) for i in range(length))
        #shortLink = site + '/links/' + chunk
        if not Link.objects.filter(short_link=shortLink).exists():
            return shortLink
    
    