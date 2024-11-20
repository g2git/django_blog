from django.db import models

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.conf import settings
from django.contrib.auth.models import User
import uuid # Required for unique comments


class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(
        max_length=200,
        unique=True,
    )

    bio = models.TextField(max_length=10000)


    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

class Blog(models.Model):
    """Model representing a blog."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    # Foreign Key used because blog can only have one author, but authors can have multiple blogs.

    description = models.TextField(
        max_length=10000, help_text="Enter blog")
    post_date = models.DateField(auto_now_add=True)


    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blog."""
        return reverse('blog-detail', args=[str(self.id)])
    
    class Meta:
        pass

class Comment(models.Model):
    content = models.TextField(
        max_length=500,
    )
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because comment can only have one author, but authors can have multiple comments.
    
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.blog.title})'

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('comment-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['-post_date']