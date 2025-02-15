from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)  # Many-to-many relationship

    def __str__(self):
        return self.title
    
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    




class Comment(models.Model):  
    # Each comment is linked to a specific blog post using a ForeignKey
    post = models.ForeignKey(
        'Blog',  # Replace 'app1' with your actual app name
        on_delete=models.CASCADE,  
        related_name='comments'  # Allows us to access comments via post.comments.all()
    )

    # The user who made the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The actual text of the comment
    content = models.TextField()

    # Timestamp when the comment was created (auto-filled)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f'Comment by {self.user.username} on {self.post.title}'
