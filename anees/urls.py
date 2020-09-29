from django.contrib import admin
from django.urls import path,include
from anees import views

from django.contrib.auth import views as auth_views

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'campaign', views.CampaignViewSet)
router.register(r'email', views.EmailViewSet)





urlpatterns = [
    path('',views.basic,name='basic'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('index',views.index, name='index'),
    path('about',views.about, name='about'),
    path('sendmail',views.sendmail,name='sendmail'),
    path('emailslist',views.emailslist,name='emailslist'),
    path('valid',views.valid,name='valid'),
    path('mailing',views.mailing,name='Mailing'),
    path('customer',views.customer,name='Customer'),
    #path('dashboard',views.dashboard,name='Dashboard'),
    path('dashboard/<str:pk_test>/',views.dashboard,name='Dashboard'),
    path('profile/<str:pk_test>/', views.profile, name="Profile"),
    path('updatecamp', views.updatecamp, name="UpdateCamp"),

    path('updateemail', views.updateemail, name="UpdateEmail"),


    path('addcampaign',views.campaign,name='Campaign'),
    path('addemaillist',views.email,name='Emaillist'),
    path("sign/", views.handleSign, name="handleSign"),
    path("log/", views.handleLog, name="handleLog"),
    path('sending/<str:pk_test>/', views.sending, name="Sending"),
    path('manytomany/<str:pk_test>/', views.manytomany, name="ManytoMany"),
    #path('sendmail/<str:pk_test>/', views.sendmail, name="Sendmail"),
    path('sendmail/', views.sendmail, name="Sendmail"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),

]
