import django_filters
import random
from rest_framework import mixins, generics, filters, status, viewsets

from rest_framework.response import Response
from rest_framework.decorators import action
from django.urls import reverse

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.
from swift_lyrics.models import Lyric, Album, Song, Vote, Artist
from swift_lyrics.serializers.serializer import LyricSerializer, \
    BaseSongSerializer, BaseAlbumSerializer, AlbumDetailSerializer, \
    SongDetailSerializer, SongSerializer, LyricDetailSerializer, \
    CreateUserSerializer, BaseArtistSerializer, ArtistDetailSerializer


class HealthCheckView(View):
    """
    Checks to see if the site is healthy.
    """

    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")


class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = BaseArtistSerializer
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['name', 'first_year']
    filter_fields = {
        'first_year': ['gte', 'lte', 'gt', 'lt']
    }

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        return BaseArtistSerializer

    def get_queryset(self):
        return Artist.objects.all()


class AlbumIndex(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    serializer_class = BaseAlbumSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AlbumDetail(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    serializer_class = AlbumDetailSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SongIndex(mixins.ListModelMixin,
                generics.GenericAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SongDetail(mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    serializer_class = SongDetailSerializer

    def get_queryset(self):
        return Song.objects.all()


class APIIndex(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    serializer_class = LyricDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'song__name', 'song__album__name']
    ordering_fields = ['text', 'song__name', 'song__album__name']

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class APIDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LyricViewSet(viewsets.ModelViewSet):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        return Lyric.objects.all()

    @action(detail=True)
    def random_lyric(self, request, *args, **kwargs):
        rndm_lyric = random.choice(self.get_queryset())
        lyric_data = LyricDetailSerializer(rndm_lyric).data
        return Response(data=lyric_data, status=200)

    @action(detail=True, methods=['post'])
    def upvote(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)
        try:
            lyric = Lyric.objects.get(pk=kwargs['pk'])
        except Lyric.DoesNotExist:
            return HttpResponse('Lyric not found', status=404)

        [vote, created] = Vote.objects.get_or_create(lyric_id=lyric.id, user_id=request.user.id, defaults={
            'lyric_id': lyric.id, 'user_id': request.user.id, 'state': 1
        })
        if not created:
            if vote.state == 1:
                vote.state = 0
                vote.save()
            else:
                vote.state = 1
                vote.save()

        return self.retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def downvote(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)
        try:
            lyric = Lyric.objects.get(pk=kwargs['pk'])
        except Lyric.DoesNotExist:
            return HttpResponse('Lyric not found', status=404)

        [vote, created] = Vote.objects.get_or_create(lyric_id=lyric.id, user_id=request.user.id, defaults={
            'lyric_id': lyric.id, 'user_id': request.user.id, 'state': -1
        })

        if not created:
            if vote.state == -1:
                vote.state = 0
                vote.save()
            else:
                vote.state = -1
                vote.save()

        return self.retrieve(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer

    def get_queryset(self):
        return User.objects.all()
