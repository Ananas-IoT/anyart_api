from django.urls import path

from anyart_api import urls as ru
from . import views

urlpatterns = [
    path('wall_photo_wrappers/', views.WallPhotoWrapperViewSet.as_view(ru.list_dict),
         name='wall_photo_wrapper_list'),
    path('wall_photo_wrappers/<int:pk>', views.WallPhotoWrapperViewSet.as_view(ru.detail_dict),
         name='wall_photo_wrapper_detail')
]