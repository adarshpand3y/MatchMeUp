from django.contrib import admin
from .models import Profile, Match, MatchRequest

# Register your models here.
admin.site.register(Profile)
admin.site.register(Match)
admin.site.register(MatchRequest)