from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet, basename='api-rooms')
router.register(r'messages', views.MessageViewSet, basename='api-messages')

urlpatterns = [
    path('', views.RoomsListView.as_view(), name='list'),
    path('create/', views.RoomCreateView.as_view(), name='create'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='detail'),
    path('api/', include(router.urls)),
]
