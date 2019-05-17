from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views
from anyart_api.urls import list_dict

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserCreateView.as_view(), name='user_create'),
    path('profile/', views.profile, name='user_retrieve'),
    path('verify_email/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
         views.verify_email, name='verify_email'), 
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_reset_code/', views.verify_reset_code, name='verify_reset_code'),
    path('change_password/', views.change_password, name='chnage_password'),
    path('feedback/', views.FeedbackViewSet.as_view(list_dict), name='feedback')
]