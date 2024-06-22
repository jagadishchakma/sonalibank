from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserLoginForm,UserProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
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
    
class UserPassChangeView(PasswordChangeView):
    template_name = 'pass_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def send_password_change_email(self, msg, type):
        mail_subject=msg
        message = render_to_string('pass_change_email.html', {'user':self.request.user, 'type': type})
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject,'',to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        self.send_password_change_email('Password Change Confirmation','Password change')
        logout(self.request)
        return super().form_valid(form)
