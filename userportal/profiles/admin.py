from django.contrib import admin

from .models import User
from .models import Profile
from .models import Settings

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Settings)