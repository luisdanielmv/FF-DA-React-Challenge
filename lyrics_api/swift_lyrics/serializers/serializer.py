import datetime
from django.db.models.fields import TextField
from drf_yasg import openapi
from rest_framework import serializers
from django.contrib.auth.models import User
from swift_lyrics.models import Lyric, Song, Album, Artist


# Base Serializers
class LyricSerializer(serializers.ModelSerializer):
    # No corresponding model property.
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        up = 0
        down = 0
        for vote in obj.votes.all():
            if vote.state > 0:
                up += 1
            elif vote.state < 0:
                down = + 1
        return {'upvotes': up, 'downvotes': down, 'difference': up - down}

    class Meta:
        model = Lyric
        fields = ['id', 'text', 'votes']


class BaseSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name']


class BaseAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name']


class BaseArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'first_year']


# Create Serializers
class CreateUserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return super().validate(data)

    def create(self, validated_data):
        new_user = User(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class CreateLyricSerializer(LyricSerializer):
    song = BaseSongSerializer(read_only=True)
    album = BaseAlbumSerializer(source='song.album', read_only=True)

    def validate(self, data):
        song_id = self.initial_data.get('song', dict()).get('id', None)
        if song_id:
            # If song_id, then the album and song already exist, just fetch them from datastore
            song = Song.objects.get(id=song_id)
            data['song'] = song
        else:
            # If album_id, then album already exists - just fetch, then handle create/fetch song
            album_id = self.initial_data.get('album', dict()).get('id', None)

            song = self.initial_data.get('song', dict())
            song_name = song.get('name', None)

            album = None
            if album_id:
                album = Album.objects.get(id=album_id)
            else:
                raise serializers.ValidationError("Field album_id is required")
            
            if album == None: 
                raise serializers.ValidationError("Album not found")

            if song_name:
                song = Song.objects.filter(name=song_name).first()
                if song is None:
                    song = Song(name=song_name, album=album)
                    song.save()
                data['song'] = song

        return super().validate(data)

    def create(self, validated_data):
        lyric = Lyric(**validated_data)
        lyric.save()
        return lyric

    class Meta(LyricSerializer.Meta):
        fields = LyricSerializer.Meta.fields + ['song', 'album']

class CreateAlbumSerializer(serializers.ModelSerializer):
    def validate(self, data):
        year = self.initial_data.get('year')
        if year == None:
            raise serializers.ValidationError("Field 'year' is required")
        artist = self.initial_data.get('artist')
        if artist == None:
            raise serializers.ValidationError("Field 'artist' is required")
        return super().validate(data)

    def create(self, validated_data):
        # breakpoint()
        album = Album(**validated_data)
        album.save()
        return album

    class Meta:
        model = Album
        fields = ['id', 'name', 'year', 'artist', 'collabs']


# Detail Serializers

class LyricDetailSerializer(LyricSerializer):
    song = BaseSongSerializer(read_only=True)
    album = BaseAlbumSerializer(source='song.album', read_only=True)

    class Meta(LyricSerializer.Meta):
        fields = LyricSerializer.Meta.fields + ['song', 'album']

class SongSerializer(BaseSongSerializer):
    album = BaseAlbumSerializer()

    class Meta(BaseSongSerializer.Meta):
        fields = BaseSongSerializer.Meta.fields + ['album']


class SongDetailSerializer(SongSerializer):
    lyrics = LyricSerializer(many=True, read_only=True)

    class Meta(SongSerializer.Meta):
        fields = SongSerializer.Meta.fields + ['lyrics']


class AlbumDetailSerializer(BaseAlbumSerializer):
    songs = BaseSongSerializer(many=True, read_only=True)

    class Meta(BaseAlbumSerializer.Meta):
        fields = BaseAlbumSerializer.Meta.fields + \
            ['songs', 'year', 'artist', 'collabs']


class ArtistDetailSerializer(serializers.ModelSerializer):
    albums = BaseAlbumSerializer(many=True)

    class Meta:
        model = Artist
        fields = ['id', 'name', 'first_year', 'albums']
