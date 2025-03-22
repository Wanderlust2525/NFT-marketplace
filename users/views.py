import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from marketplace.models import Picture
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


@login_required
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
                return HttpResponse('Amount must be greater than zero', status=400)
        except ValueError:
            return HttpResponse('Invalid amount', status=400)
    return render(request, 'auth/profile.html')


@login_required
def buy_picture(request, id=id):
    picture = get_object_or_404(Picture, id=id)
    profile = request.user.profile  
    
    success = profile.buy_picture(picture)
    
    if success:
        return redirect('profile')  
    else:
        return HttpResponse("Недостаточно средств для покупки.", status=400)

# Create your views here.
