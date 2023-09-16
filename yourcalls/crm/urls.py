from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),    
    path('crm', views.crm, name='crm'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('delete_records', views.delete_records, name='delete_records'),
    path('token', views.GetToken.as_view(), name='token'),
    path('caller', views.caller, name='caller'),    
    path('call', views.Call.as_view(), name='call')
]
