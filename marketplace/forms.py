from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from marketplace.models import Picture

class PictureForm(forms.ModelForm):
    class Meta:
        model=Picture
        exclude =('rating','user')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'login-form', 'placeholder': 'Название'}),
            'image': forms.FileInput(attrs={'class': 'login-form', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'login-form', 'placeholder': 'Описание', 'rows': 7}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'class': 'login-form', 'placeholder': 'Цена', 'min': '0', 'step': '0.01'}),
            'highest_bid': forms.NumberInput(attrs={'class': 'login-form', 'placeholder': 'Макс. ставка', 'min': '0', 'step': '0.01'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }
        

class LoginForm(forms.Form):
    username = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'login-form', 'placeholder': 'Username'}))
    
    password = forms.CharField( widget=forms.PasswordInput(attrs={
        'class': 'login-form', 'placeholder': 'Password'
    }))


class RegisterForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True


    username = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'login-form', 'placeholder': 'Username'}))
    
    email = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'login-form', 'placeholder': 'Email Address'}))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-form', 'placeholder': 'Password'}),
                                validators=[validate_password])

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-form', 'placeholder': 'Confirm Password'}))
    

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'login-form'}),
            'email': forms.EmailInput(attrs={'class': 'login-form'}),
        }

        def clean(self):
            if self.is_valid():

                password1 = self.cleaned_data.get('password1')
                password2 = self.cleaned_data.get('password2')

                if password1 != password2:
                    raise forms.ValidationError({'password2': ['The passwords do not match']})

            return self.cleaned_data


    

