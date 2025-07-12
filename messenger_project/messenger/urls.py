from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name ='home'),
    path('inbox/', views.inbox, name='inbox'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
]
