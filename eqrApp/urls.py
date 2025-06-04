from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('',views.home),
    path('login',views.login_page,name='login-page'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('student_list',views.student_list,name='student-page'),
    path('add_student',views.manage_student,name='add-student'),
    path('edit_student/<int:pk>',views.manage_student,name='edit-student'),
    path('save_student',views.save_student,name='save-student'),
    path('view_card/<int:pk>',views.view_card,name='view-card'),
    path('view_details/<str:code>',views.view_details,name='view-details'),
    path('view_details',views.view_details,name='scanned-code'),
    path('delete_student/<int:pk>',views.delete_student,name='delete-student'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
