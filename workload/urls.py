from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.DocumentCreateView.as_view(), name='doc-test'),
    path('doc-retrieve/', views.DocumentRetrieveView.as_view(), name='doc-retrieve'),
    path('wall_photo/', views.WallPhotoView.as_view(), name='user-upload-view')
]