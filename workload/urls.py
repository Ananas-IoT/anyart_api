from django.urls import path

from anyart_api import urls as ru
from . import views

urlpatterns = [
    path('wall_photo_wrappers/', views.WallPhotoWrapperViewSet.as_view(ru.list_dict),
         name='wall_photo_wrapper-list'),
    path('wall_photo_wrappers/<int:pk>', views.WallPhotoWrapperViewSet.as_view(ru.detail_dict),
         name='wall_photo_wrapper-detail'),
    path('sketches/', views.SketchViewSet.as_view(ru.list_dict),
         name='sketch-list'),
    path('sketches/<int:pk>', views.SketchViewSet.as_view(ru.detail_dict),
         name='sketch-detail'),
    path('wall_photo/', views.WallPhotoViewSet.as_view(ru.list_dict),
         name='wall_photo-list'),
    path('wall_photo/<int:pk>', views.WallPhotoViewSet.as_view(ru.detail_dict),
         name='wall_photo-detail')
]