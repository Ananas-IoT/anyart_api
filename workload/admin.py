from django.contrib import admin
from . import models as m

models_list = [m.Workload, m.WallPhotoWrapper, m.WallPhoto, m.Location, m.Sketch, m.SketchImage]

admin.site.register(models_list)