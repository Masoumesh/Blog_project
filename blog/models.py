from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here. 
class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    