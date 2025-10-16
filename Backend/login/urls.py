from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.register,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('projectdashboard/',views.projectdashboard,name='pdashboard'),
    path('submitcompany/',views.submitcompany,name='submitcompany'),
    path('company/<int:id>/',views.companydetail,name='detail'),
    path('invest/',views.invest,name='invest'),
    path('payment/',views.history,name='history'),
    path('investment/',views.investments,name='investment'),
    path('network/',views.network,name='network'),
]
