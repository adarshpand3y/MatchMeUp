from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=False, null=True, blank=True)
    full_name = models.CharField(max_length=50, default="")
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

class MatchRequest(models.Model):
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_sent_by")
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_sent_to")

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_user_1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_user_2")
