from django.db import models
from django.utils.text import slugify

# Create your models here.
class SavedArticle(models.Model): 
    title = models.CharField(max_length=300) 
    url = models.URLField() 
    source = models.CharField(max_length=200, blank=True) 
    created = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('technology', 'Technology'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment')
    ])
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title