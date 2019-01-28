from django.urls import path
from . import views

urlpatterns = [
    path('wall_photo_wrappers/', views.WallPhotoWrapperViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='user-upload-view')
]