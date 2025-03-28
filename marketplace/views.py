from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from marketplace.decorators import is_owner, login_required
from marketplace.forms import  LoginForm, PictureForm, RegisterForm
from marketplace.models import Category, Picture
from users.models import UserProfile
from django.db.models import Count
from django.core.paginator import Paginator

def main(request):
    pictures =Picture.objects.all()
    categories = Category.objects.all() 
    total_pictures = UserProfile.objects.annotate(total_products=Count('picture'))
    
    return render(request, 'index.html',{ 'pictures':pictures,'categories': categories, 'total_pictures':total_pictures})


def detail_page (request,id):
    pictures =Picture.objects.all()
    picture = get_object_or_404(Picture, id=id)    
    user_pictures = Picture.objects.filter(user=picture.user).exclude(id=id).order_by('-date')
    categories = Category.objects.all()    

    page = request.GET.get('page', 1) 
    pagin = Paginator(pictures, 9)
    pictures = pagin.get_page(page) 
   
    return render(request, 'detail_page.html', { 'picture':picture,'user_pictures':user_pictures,'categories':categories, 'pictures':pictures})

def marketplace(request):
    # pictures =Picture.objects.all()
    categories = Category.objects.all() 
    # total_pictures = Picture.objects.filter(user=request.user).count()

    pictures = Picture.objects.all()
    total_pictures = pictures.count()
    

    search = request.GET.get('search')
    if search is not None:
        pictures = pictures.filter(name__icontains=search)

    

    page = request.GET.get('page', 1) or 1
    pagin = Paginator(pictures, 12)
    pictures = pagin.get_page(page)


    return render(request, 'marketplace.html',{ 'pictures':pictures,'categories': categories, 'total_pictures':total_pictures})


def user_login(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            return redirect('/profile/')
        else:
            messages.error(request, 'The user is not found or the password is incorrect.')

    return render(request, 'auth/login.html', {'form': form})



def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            password = form.cleaned_data.pop('password1')

            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            login(request, user)
            messages.success(request, f'Welcome to marketplace "{user.username}"')
            return redirect(reverse('main'))

    return render(request, 'auth/register.html', {'form': form})

def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully logged out!')

    return redirect('/')

def profile(request):    
    user_pictures = Picture.objects.filter(user=request.user.profile).order_by('-date')
    total_pictures = Picture.objects.filter(user=request.user.profile).count()

    page = request.GET.get('page', 1) or 1
    pagin = Paginator(user_pictures, 9)
    user_pictures = pagin.get_page(page)
    
    return render (request,'auth/profile.html',{'total_pictures':total_pictures,'user_pictures':user_pictures} )


# @login_required()
# @is_owner
# def upload_picture(request):
#     if request.method == 'POST':
#         form = PictureForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  
#     else:
#         form = PictureForm()
#     return render(request, 'auth/upload_picture.html', {'form': form})

@login_required()
def create(request):
    form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            picture = form.save(commit=False)
            try:
                picture.user = UserProfile.objects.get(user=request.user)  
            except UserProfile.DoesNotExist:
                messages.error(request, "Ошибка: У пользователя нет профиля.")
                return redirect('/profile/')
            
            if not picture.rating:  
                picture.rating = 3.0
            picture.save()
            messages.success(request, f'The picture "{picture.name}" was created successfully.')
            return redirect('/profile/')
        
        messages.error(request, 'Please correct the errors in the form.')

    return render(request, 'picture_create.html', {'form': form})


@login_required()

def update(request, id):
    picture = get_object_or_404(Picture, id=id)
    form = PictureForm(instance=picture)

    if request.method == 'POST':
        form = PictureForm(data=request.POST, files=request.FILES, instance=picture)

        if form.is_valid():
            form.save()
            messages.error(request, f'The picture "{picture.name}" was updated successfully.')
            return redirect('/profile/')

        messages.error(request, 'Please correct errors')

    return render(request, 'picture_update.html', {'form': form, 'picture': picture})

@login_required()
@is_owner
def delete(request, id):
    picture = get_object_or_404(Picture, id=id)
    picture.delete()
    messages.success(request, f'The picture "{picture.name}" was deleted successfully.')
    return redirect('/profile/')


