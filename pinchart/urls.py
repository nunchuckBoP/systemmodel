"""systemmodel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, reverse_lazy
from django.urls.conf import include
from pinchart import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('index/', views.PinchartListView.as_view(), name='pinchart-list'),
    path('create/', views.PinchartCreateView.as_view(), name='pinchart-create'),
    path('update/<pk>/', views.PinchartUpdateView.as_view(), name='pinchart-update'),
    path('<pk>/word/index/', views.WordListView.as_view(), name='word-list'),
    path('<pk>/word/create/', views.WordCreateView.as_view(), name='word-create'),
    path('<pk>/sequence/index/', views.SequenceListView.as_view(), name='sequence-list'),
    path('sequence/<pk>/update/', views.SequenceUpdateView.as_view(), name='sequence-update'),
    path('word/<pk>/update', views.WordUpdateView.as_view(), name='word-update'),
    path('word/<pk>/delete', views.WordDeleteView.as_view(), name='word-delete'),
    path('word/<pk>/bitdescriptions/index/', views.BitDescriptionListView.as_view(), name='bitdescription-list'),
    path('word/<pk>/bitdescriptions/create/', views.BitDescriptionCreateView.as_view(), name='bitdescription-create'),
    
]
