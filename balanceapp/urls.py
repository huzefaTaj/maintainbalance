from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_transaction, name='add_transaction'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page
    path('add_bank/', views.add_bank, name='add_bank'),  # Add bank
    path('login/', views.user_login, name='login'),  # Custom login view
    path('logout/', views.user_logout, name='logout'),  # Logout page
     path('set-spending-limit/', views.set_spending_limit, name='set_spending_limit'),  # Set spending limit
]
