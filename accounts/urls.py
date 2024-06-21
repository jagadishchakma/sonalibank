from .views import UserRegistrationView,UserLoginView,UserLogOutView,UserProfileView
from django.urls import path
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
