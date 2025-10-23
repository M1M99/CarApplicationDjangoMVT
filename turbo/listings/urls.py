from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views_auth import signup

urlpatterns=[
    path('',views.listing_list,name='listing_list'),
    path('listing/<slug:slug>',views.listing_detail,name='listing_detail'),

    path('my/',views.my_listings,name='my_listings'),
    path('create/',views.listing_create,name='listing_create'),
    path('edit/<slug:slug>',views.listing_update,name='listing_update'),
    path('delete/<slug:slug>',views.listing_delete,name='listing_delete'),

    #auth Django build in and + custom
    path('login/',auth_views.LoginView.as_view(template_name='auth/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='listing_list'),name='logout'),
    path('signup/',signup,name='signup'),
]