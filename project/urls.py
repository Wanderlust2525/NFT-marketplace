"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from marketplace import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('detail_page/<int:id>/', views.detail_page, name='detail_page'),  
    path('marketplace/', views.marketplace, name='marketplace'),

    path('profile/', views.profile, name='profile'),
    path('create-picture/', views.create, name='create_picture'),
    path('update-picture/<int:id>/', views.update, name='update_picture'),
    path('delete-picture/<int:id>/', views.delete, name='delete_picture'),
    

    path('login/', views.user_login, name='login'),

    path('register/', views.register, name='register'),
    path('logout/', views.logout_profile, name='logout'),

    path('avatar/', include('users.urls')),
    path('', views.main, name='main'),
   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
