from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trips_index, name='trips_index'),
    path('trips/<int:trip_id>/', views.trips_detail, name='detail'),
    path('trips/<int:pk>/update/', views.TripUpdate.as_view(), name='trips_update'),
    path('trips/<int:pk>/delete/', views.TripDelete.as_view(), name='trips_delete'),
    path('trips/create/', views.TripCreate.as_view(), name='trips_create'),
    path('friends/create/', views.FriendCreate.as_view(), name='friends_create'),
    path('friends/', views.friends_index, name='friends_index'),
    path('friends/<int:friend_id>/', views.friends_detail, name='friends_detail'),
    path('friends/<int:pk>/update/', views.FriendUpdate.as_view(), name='friends_update'),
    path('friends/<int:pk>/delete/', views.FriendDelete.as_view(), name='friends_delete'),
    path('trips/<int:trip_id>/assoc_friend/<int:friend_id>/', views.assoc_friend, name='assoc_friend'),
    path('trips/<int:trip_id>/remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('flight_search/', views.flight_search, name='flight_search'),
    path('trips/<int:trip_id>/add_photo/', views.add_photo, name='add_photo'),
    path('trips/<int:trip_id>/add_itinerary/', views.add_itinerary, name='add_itinerary'),
    path('trips/<int:pk>/remove_itinerary', views.remove_itinerary, name='remove_itinerary'),
    path('accounts/signup/', views.signup, name='signup'),
]