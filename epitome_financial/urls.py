from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from bulletin.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),
    
    path('bulletin/', ArticleListView.as_view(template_name='bulletin/bulletin.html'), name = 'bulletin'),
    path('bulletin/<int:pk>/', ArticleDetailView.as_view(), name ='bulletin_detail'),
    path('bulletin/create/', ArticleCreateView.as_view(), name ='bulletin_create'),
    path('bulletin/<int:pk>/update/', ArticleUpdateView.as_view(), name ='bulletin_update'),
    path('bulletin/<int:pk>/delete/', ArticleDeleteView.as_view(), name ='bulletin_delete'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name = 'password_reset_complete'),

    path('profile/', user_views.profile, name = 'profile'),
    path('', include('portfolio_viewer.urls')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)