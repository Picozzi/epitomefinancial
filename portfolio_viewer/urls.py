from django.urls import path
from . import views
from portfolio_viewer.views import (AccountCreateView, AccountDeleteView, AccountListView, AccountDetailView, AccountUpdateView,
SecurityCreateView, SecurityDeleteView, SecurityListView, SecurityDetailView, SecurityUpdateView)
 
urlpatterns = [
    path('', views.home, name = 'home'),
    path('dashboard/', views.dashboard, name = 'dashboard'),

    path('account/', AccountListView.as_view(), name = 'account_list'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name ='account_detail'),
    path('account/create/', AccountCreateView.as_view(), name ='account_create'),
    path('account/<int:pk>/update/', AccountUpdateView.as_view(), name ='account_update'),
    path('account/<int:pk>/delete/', AccountDeleteView.as_view(), name ='account_delete'),

    path('security/', SecurityListView.as_view(), name = 'security_list'),
    path('security/<int:pk>/', SecurityDetailView.as_view(), name ='security_detail'),
    path('security/create/', SecurityCreateView.as_view(), name ='security_create'),
    path('security/<int:pk>/update/', SecurityUpdateView.as_view(), name ='security_update'),
    path('security/<int:pk>/delete/', SecurityDeleteView.as_view(), name ='security_delete')
]