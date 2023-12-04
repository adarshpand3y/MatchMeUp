from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=False, null=True, blank=True)
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
    pic1 = models.ImageField()
    pic2 = models.ImageField()
    pic3 = models.ImageField()

    def __str__(self) -> str:
        return f"Details for: {self.user}"