import os
from django.shortcuts import render, redirect

from users.forms import UserProfileForm

from users.models import UserProfile
from django.contrib.auth.decorators import login_required


@login_required
def avatar (request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Удаляем старый аватар, если он существует
            if user_profile.avatar and hasattr(user_profile.avatar, 'path'):
                if os.path.isfile(user_profile.avatar.path):
                    os.remove(user_profile.avatar.path)

            form.save()
            return redirect('/profile/')  

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'auth/avatar.html', {'form': form})


# Create your views here.
