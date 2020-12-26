from django.urls import path, include
from . import views
from .views import SignUp, Register, RoomList, BookingList, request, BookingView, RoomDetailView



urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('review/', views.review, name="review"),
    path('booking/', views.booking, name="bookinglist"),
    path('request/', views.request, name="request"),
    path('gallery/', views.gallery, name="gallery"),
    path('moreinfo/', views.gallery, name="moreinfo"),
    path('register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
    path('roomlist/', RoomList.as_view(), name='room-list'),
    path('bookinglist/', BookingView.as_view(), name='booking-list'),
    path('book/', BookingView.as_view(), name='booking_view'),
    path('room/<category>', RoomDetailView.as_view(), name='roomdetailview')
]
 