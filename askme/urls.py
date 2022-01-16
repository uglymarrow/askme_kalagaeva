"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from app import views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hot/', views.hot_questions, name='hot'),
    path('question/<int:pk>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str>/', views.tagged_questions, name='tag'),
    path('', views.index, name='index'),
    path('answer/', views.answer, name='answer'),
    path('qvote/', views.qvote, name='qvote'),
    path('avote/', views.avote, name='avote'),
    path('check/', views.check, name='check')
]
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

