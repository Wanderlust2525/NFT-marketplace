import os
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from marketplace.models import Picture
from users.forms import ChangePasswordForm, UserProfileForm

from users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count


from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



@login_required()

def avatar (request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Удаляем старый аватар
            if user_profile.avatar and hasattr(user_profile.avatar, 'path'):
                try:
                    if os.path.isfile(user_profile.avatar.path):
                        os.remove(user_profile.avatar.path)
                except Exception as e:
                     print(f"Error removing old avatar: {e}")
            form.save()
            messages.success(request, 'Your avatar has been updated successfully!')
            return redirect('/profile/')  

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'auth/avatar.html', {'form': form})


    
def rankings(request):
    users = UserProfile.objects.all()
    users = users.annotate(total_products=Count('picture'))
    return render(request, 'auth/creators.html', {'users': users})

@login_required()

def add_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', 0)  
        
        try:
            amount = float(amount)

            if amount > 0:
                profile = request.user.profile
                profile.add_balance(amount)
                return redirect('profile')  
            else:
                messages.error(request, 'Amount must be greater than zero')
        except ValueError:
            messages.error(request, 'Invalid amount')
    return render(request, 'auth/profile.html')


@login_required
def buy_picture(request, id=id):
    picture = get_object_or_404(Picture, id=id)
    profile = request.user.profile  
    
    success = profile.buy_picture(picture)
    
    if success:
        messages.success(request, 'The purchase was successful!')
        return redirect('/profile/')  
    else:
        messages.error(request, 'Insufficient funds to purchase.')
        return redirect('/profile/')


@login_required()
def change_password(request):
    form = ChangePasswordForm()

    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user = request.user
            user.set_password(new_password)
            user.save()

            login(request, user)

            messages.success(request, 'The password was modified successfully.')
            return redirect('/profile/')

    return render(request, 'auth/change_password.html', {'form': form})
# Create your views here.
