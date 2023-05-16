import email
from email.mime import image
from django.db import models

# Create your models here.
class User_Info(models.Model):
    user_id = models.CharField(primary_key=True,max_length=10,)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image=models.ImageField(upload_to="mainproj/images")
    
    def __str__(self):
        return self.user_id