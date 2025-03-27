from django import forms
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'FirstName'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'lastname'}))
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'avatar']


class ChangePasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user: UserProfile = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    old_password = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'login-form', 'placeholder':'Old password'}))
    new_password = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'login-form', 'placeholder':'New password'}),
                                   validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-form', 'placeholder':'Comfirm password'}))

    def clean(self):
        if self.is_valid():
            old_password, new_password, confirm_password = self.cleaned_data.values()

            errors = {}

            if not self.user.check_password(old_password):
                errors['old_password'] = ['The old password is incorrect.']

            if new_password != confirm_password:
                errors['confirm_password'] = ['The passwords are not matches.']

            if old_password == new_password:
                errors['new_password'] = ['The new password should not be old password.']

            if len(errors) > 0:
                raise forms.ValidationError(errors)

        return self.cleaned_data