from django.db import models
    
class Link(models.Model):
    user = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    original_link = models.URLField(max_length=200)
    short_link = models.CharField(max_length=50)
    short_tag = models.CharField(max_length=6,default='')
    transitions = models.IntegerField(default=0)

    def __str__(self):
        return self.original_link
    
