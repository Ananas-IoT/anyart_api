from django.contrib import admin
from . import models as m

models_list = [m.UserProfile, ]

admin.site.register(models_list)
