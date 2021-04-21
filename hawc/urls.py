
from django.conf.urls import url
from django.urls import path


from hawc import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^paper/$', views.PaperListView.as_view(), name='paper'),
    url(r'^author/$', views.AuthorListView.as_view(), name='author'),

    path('signed/<int:paper>/', views.signed, name='signed'),

    path('accounts/login/', views.LoginPageView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]