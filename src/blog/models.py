from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from taggit.managers import TaggableManager

class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title      = models.CharField(max_length=100)
    slug       = models.SlugField(max_length=100, unique_for_date='publish')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    image      = models.ImageField(upload_to='media', height_field=None, null=True, blank=True)
    body       = models.TextField(blank=True, null=True)
    publish    = models.DateTimeField(default=timezone.now)
    created    = models.DateTimeField(auto_now_add=True)
    update     = models.DateTimeField(auto_now=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    objects    = models.Manager() # the default Manager.
    published  = PublishManager() # custom manager.
    tags       = TaggableManager()

    class meta:
        ordering = ('publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


class Comment(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name    = models.CharField(max_length=100)  
    email   = models.EmailField()
    body    = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)

    class meta:
        ordering = ('created')

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"