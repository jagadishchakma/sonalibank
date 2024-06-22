from .views import UserRegistrationView,UserLoginView,UserLogOutView,UserProfileView, UserPassChangeView
from django.urls import path
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('pass_change/', UserPassChangeView.as_view(), name='pass_change'),
]
