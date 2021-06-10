from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Artist(models.Model):
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=True,
        help_text="Album name - can alternatively use 'id' field set to id of existing album when creating new lyrics")

    first_year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(
            datetime.date.today().year)],
        null=True,
        help_text="First year active - debut year of the artist")

    objects = models.Manager()


class Album(models.Model):
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=False,
        help_text="Album name - can alternatively use 'id' field set to id of existing album when creating new lyrics",
    )

    year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(
            datetime.date.today().year)],
        null=True,
        help_text="Release Year - year the album was released")

    artist = models.ForeignKey(
        Artist,
        related_name="albums",
        null=True,
        on_delete=models.CASCADE,
        help_text="Artist - creator of the album"
    )

    collabs = models.ManyToManyField(
        Artist,
        related_name="collab_albums",
        blank=True,
        help_text="Collabs - artists who collaborated on the creation of the album"
    )

    objects = models.Manager()

    class Meta:
        unique_together = [['name', 'artist']]


class Song(models.Model):
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=True,
        help_text="Song name - can alternatively use 'id' field set to id of existing song when creating new lyrics")

    album = models.ForeignKey(
        Album,
        related_name='songs',
        null=True,
        on_delete=models.CASCADE,
        help_text="Album")

    objects = models.Manager()


class Lyric(models.Model):
    text = models.TextField(
        blank=False,
        db_index=True,
        help_text="Lyrics from a song/album")

    song = models.ForeignKey(
        Song,
        related_name='lyrics',
        null=True,
        on_delete=models.CASCADE,
        help_text="Song")

    objects = models.Manager()


class Vote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='votes')
    lyric = models.ForeignKey(
        Lyric, on_delete=models.CASCADE, related_name='votes')
    state = models.IntegerField(
        validators=[MinValueValidator(-1), MaxValueValidator(1)], default=0, help_text="Vote state - it's whether the Lyric has been upvoted(1)/downvoted(-1) by the user")

    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'lyric')
