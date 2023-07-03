from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions
from .models import Room, Message
from .forms import RoomForm
from .serializers import RoomSerializer, MessageSerializer, BaseRoomSerializer
import logging

logger = logging.getLogger('main')
# Create your views here.


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    template_name = "rooms/create.html"
    form_class = RoomForm
    success_url = reverse_lazy('rooms:list')
    success_message = "New room '%(name)s'. Be the first one to start speaking"


class RoomsListView(ListView):
    model = Room
    template_name = "rooms/list.html"
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = super(RoomsListView, self).get_queryset()
        queryset = queryset.filter(
            name__icontains=self.request.GET.get('q', '')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = "rooms/detail.html"
    context_object_name = 'room'
    queryset = Room.objects.all()


# API VIEWSETS
class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        """This helps to keep consistency between views
        (that allow users to see rooms but not in detail)
        with the apis
        """
        if self.request.user.is_authenticated:
            return RoomSerializer
        return BaseRoomSerializer


class MessageViewSet(ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)
