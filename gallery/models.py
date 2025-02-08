from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images")
    title = models.CharField(max_length=255, default='New Image')
    tags = models.CharField(max_length=255, help_text="Comma-separated tags", default="")

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()