from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    genders=[
        ("m", "Male"),
        ("f", "Female")
    ]
    gender = models.CharField(
        max_length=1,
        choices=genders,
        default="m",
    )
    bio = models.CharField(max_length=150)
    pic1 = models.CharField(max_length=2048)
    pic2 = models.CharField(max_length=2048)
    pic3 = models.CharField(max_length=2048)