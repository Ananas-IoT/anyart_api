from django.contrib import admin
from . import models as m

models_list = [m.Workload, m.WallPhotoWrapper, m.WallPhoto, m.Location, m.Sketch, m.SketchImage]

admin.site.site_title = 'AnyArt site admin'
admin.site.site_url = 'https://anyart.netlify.com'
admin.site.site_header = 'AnyArt administration'
admin.site.register(models_list)