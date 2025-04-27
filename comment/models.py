from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Post

# Create your models here.
User = get_user_model()
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status= models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return f'Comment by {self.user.email} on {self.post.title}'