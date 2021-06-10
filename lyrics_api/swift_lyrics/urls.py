from django.conf.urls import url
from django.urls import path, include

from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from swift_lyrics import views


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('users', views.UserViewSet.as_view({'get':'list', 'post':'create'}), name='users'),
    path('users/<int:pk>', views.UserViewSet.as_view({'get':'retrieve','patch':'partial_update'}), name='users'),
    path('users/authenticate', obtain_auth_token, name='authenticate'),
    path('lyric', views.APIIndex.as_view(), name='api_index'),
    path('lyric/<int:pk>', views.APIDetail.as_view(), name='api_detail'),
    path('lyric/<int:pk>/upvote', views.LyricViewSet.as_view({'post':'upvote'}), name='lyric_upvote'),
    path('lyric/<int:pk>/downvote', views.LyricViewSet.as_view({'post':'downvote'}), name='lyric_downvote'),
    path('lyric/random', views.LyricViewSet.as_view({'get':'random_lyric'}), name='random_lyric'),
    path('artists', views.ArtistViewSet.as_view({'get':'list', 'post':'create'}), name='album_index'),
    path('artists/<int:pk>', views.ArtistViewSet.as_view({'get':'retrieve', 'patch':'partial_update', 'put': 'update', 'delete':'destroy'}), name='album_index'),
    path('album', views.AlbumIndex.as_view(), name='album_index'),
    url(r'^album/(?P<pk>\d+)/?$', views.AlbumDetail.as_view(), name='album_detail'),
    url(r'^song/$', views.SongIndex.as_view(), name='song_index'),
    url(r'^song/(?P<pk>\d+)/?$', views.SongDetail.as_view(), name='song_detail'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
