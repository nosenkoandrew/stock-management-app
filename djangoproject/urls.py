"""djangoproject URL Configuration

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
from django.urls import include, path
from stock_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('items_list/', views.items_list, name='items_list'),
    path('add_item/', views.add_item, name='add_item'),
    path('update_item/<str:pk>/', views.update_item, name='update_item'),
    path('delete_item/<str:pk>/', views.delete_item, name='delete_item'),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('accounts/', include('registration.backends.default.urls')),
]
