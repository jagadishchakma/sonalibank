from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserLoginForm,UserProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self,form):
        form.save()
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password1') 
        authuser = authenticate(username=username, password=password) 
        if authuser is not None:
            login(self.request, authuser)
        return super().form_valid(form) 
    

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('homepage')

    def get_success_url(self) -> str:
        return self.success_url

class UserLogOutView(LogoutView):
    next_page =reverse_lazy('register')

class UserProfileView(LoginRequiredMixin, UpdateView):

    form_class = UserProfileForm
    template_name = 'user_profile.html'
    success_url = reverse_lazy('profile')  # Replace with your profile URL name

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        # Example: Set initial values for fields
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        initial['account_type'] = self.request.user.account.account_type
        initial['birth_date'] = self.request.user.account.birth_date
        initial['gender'] = self.request.user.account.gender
        initial['street_address'] = self.request.user.address.street_address
        initial['postal_code'] = self.request.user.address.postal_code
        initial['city'] = self.request.user.address.city
        initial['country'] = self.request.user.address.country
        return initial
    
