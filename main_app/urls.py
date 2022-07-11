from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('rides/', views.rides_index, name='rides'),
    path('rides/<int:ride_id>/', views.rides_detail, name='detail'),
    path('rides/create/', views.RideCreate.as_view(), name='ride_create'),
    path('rides/<int:pk>/update/', views.RideUpdate.as_view(), name='ride_update'),
    path('rides/<int:pk>/delete/', views.RideDelete.as_view(), name='ride_delete'),
]