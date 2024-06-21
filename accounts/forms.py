from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from .models import UserAddress,UserBankAccount


class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'account_type', 'birth_date', 'gender', 'street_address', 'city', 'postal_code', 'country', 'password1', 'password2']
    

    


    def save(self, commit=True):
        user = super().save(commit=False) #return user instance(means equal obj = Person(username,first_name,last_name, email, password1, password2) that this instance available all parent methods and attributes)) only from UserCreationForm not save
        if commit == True:
            user.save() #for this user.save()
            account_type = self.cleaned_data['account_type']
            birth_date = self.cleaned_data['birth_date']
            gender = self.cleaned_data['gender']
            street_address = self.cleaned_data['street_address']
            city = self.cleaned_data['city']
            postal_code = self.cleaned_data['postal_code']
            country = self.cleaned_data['country']

            UserAddress.objects.create( # objects will be create in database
                user = user,
                street_address = street_address,
                city = city,
                postal_code = postal_code,
                country = country
            )
            UserBankAccount.objects.create( #object will be create in database
                user = user,
                account_type = account_type,
                gender = gender,
                birth_date = birth_date,
                account_no = 1000+user.id
            )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        print(type(self.fields))
        for field in self.fields.values():
            field.widget.attrs.update({
                'class':('custom')
            })

class UserLoginForm(AuthenticationForm):
    pass


class UserProfileForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'account_type', 'birth_date', 'gender', 'street_address', 'city', 'postal_code', 'country']

    # def __init__(self,*args, **kwargs):
    #         self.user = kwargs.pop('user', None)
    #         super(UserProfileForm, self).__init__(*args, **kwargs)
    #         print(self.user.username)
    #         if self.instance:
    #             print(self.instance.first_name)
                # try:
                #     user_account = self.instance.account
                #     user_address = self.instance.address
                # except UserBankAccount.DoesNotExist:
                #     user_account = None
                #     user_address = None 
                # self.fields['first_name'].initial = self.instance.first_name
                # self.fields['last_name'].initial = self.instance.last_name
                # self.fields['email'].initial = self.instance.email
                # if user_account:
                #     self.fields['account_type'].initial = user_account.account_type
                #     self.fields['birth_date'].initial = user_account.birth_date
                #     self.fields['gender'].initial = user_account.gender
                # if user_address:
                #     self.fields['street_address'].initial = user_address.street_address
                #     self.fields['city'].initial = user_address.city
                #     self.fields['postal_code'].initial = user_address.postal_code
                #     self.fields['country'].initial = user_address.country
        
    def save(self, commit=True):
            user = super().save(commit=False)
            if commit == True:
                user.save()
                # print(UserBankAccount.objects.get_or_create(user=user)[0].account_type)
                # print(type(UserBankAccount.objects.get_or_create(user=user)))
                user_account = UserBankAccount.objects.get_or_create(user=user)[0]
                user_address = UserAddress.objects.get_or_create(user=user)[0]

                user_account.account_type = self.cleaned_data['account_type']
                user_account.birth_date = self.cleaned_data['birth_date']
                user_account.gender = self.cleaned_data['gender']
                user_account.save()
                user_address.street_address = self.cleaned_data['street_address']
                user_address.city = self.cleaned_data['city']
                user_address.postal_code = self.cleaned_data['postal_code']
                user_address.country = self.cleaned_data['country']
                user_address.save()
            return user