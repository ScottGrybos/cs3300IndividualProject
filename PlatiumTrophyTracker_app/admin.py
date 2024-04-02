from django.contrib import admin
from .models import UserAccount
from .models import User
from .models import TrophyTracker

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(User)
admin.site.register(TrophyTracker)