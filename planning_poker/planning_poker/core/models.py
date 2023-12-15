import json
from django.utils import timezone
from django.db import models

from django.conf import settings

from django.utils.translation import gettext_lazy as _


# Create your models here.
class PokerSession(models.Model):
    class SESSION_MODE(models.TextChoices):
        STRICT = "strict", _("Strict")
        MEDIUM = "medium", _("Moyen")
        # MEDIAN = "median", _("Median")

    class SESSION_STATUS(models.TextChoices):
        CREATED = "created", _("Créée")
        STARTED = "started", _("Commencée")
        FINISHED = "finished", _("Terminée")
    players = models.IntegerField(default=1, verbose_name="Participants")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poker_sessions")
    feature_field_name = models.CharField(max_length=50, default="items", verbose_name="Nom du champ des features")
    product_backlog = models.TextField()
    product_backlog_file = models.FileField(upload_to="files", verbose_name="Fichier du backlog")
    mode = models.CharField(max_length=10, choices=SESSION_MODE.choices, default=SESSION_MODE.STRICT)
    status = models.CharField(max_length=10, choices=SESSION_STATUS.choices, default=SESSION_STATUS.CREATED)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    result_file = models.FileField(upload_to="files", verbose_name="Fichier du résultat", null=True, blank=True)

    @property
    def get_result_file(self):
        return self.result_file.url if self.result_file else ""

    @property
    def get_result_file_name(self):
        return self.result_file.name if self.result_file else ""

    @property
    def can_start(self):
        return self.participants.count() == self.players

    def tours_reverse(self):
        return self.tours.all().order_by("-pk")

    def gen_features(self):
        _features = json.load(self.product_backlog_file)
        Feature.objects.bulk_create(
            [
                Feature(
                    poker_session=self,
                    title=item["name"],
                    description=item["description"],
                )
                for item in _features[self.feature_field_name]
            ]
        )
        return _features[self.feature_field_name]

    @property
    def get_next_feature(self):
        return self.features.filter(voted=False).first()

    def get_previous_features(self):
        return self.features.filter(voted=True)

    def update_status(self):
        if self.features.filter(voted=False).exists() and self.get_next_feature:
            self.status = self.SESSION_STATUS.CREATED
        else:
            self.status = self.SESSION_STATUS.FINISHED
        self.save()

    def save(
        self,
        *args,
        **kwargs,
    ):

        self.product_backlog = json.load(self.product_backlog_file)
        super().save(*args, **kwargs)


class Feature(models.Model):
    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    story_points = models.IntegerField(default=0)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def tours_reverse(self):
        return self.tours.all().order_by("-pk")

    @property
    def is_consensus(self):
        return len(set(self.get_last_tour.votes.values_list("vote", flat=True)) if self.get_last_tour else []) == 1

    # check if all participants have voted
    @property
    def is_completed(self):
        return len(self.get_last_tour.votes.all() if self.get_last_tour else []) == len(
            self.poker_session.participants.all())

    @property
    def is_validated(self):
        return self.is_consensus and self.is_completed

    @property
    def is_started(self):
        return self.votes.all().exists()

    def check_votes(self, mode):
        vote_count = len(self.votes.all()) == len(self.poker_session.participants.all())
        if mode == PokerSession.SESSION_MODE.STRICT:
            return

    def get_next_feature(self):
        return self.poker_session.features.filter(voted=False).first()

    def get_previous_features(self):
        return self.poker_session.features.filter(voted=True)

    @property
    def get_last_tour(self):
        return self.tours.last()

    def set_next_tour(self):
        # breakpoint()
        tour = Tour.objects.create(poker_session=self.poker_session, feature=self,
                                   designation=self.get_last_tour.designation + 1)
        tour.save()
        return tour


class Participant(models.Model):
    class Meta:
        unique_together = ("poker_session", "user")

    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participants")

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="votes")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="votes")
    vote = models.IntegerField()
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE, related_name="votes")
    cafe = models.BooleanField(default=False)
    interro = models.BooleanField(default=False)


class Tour(models.Model):
    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="tours")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="tours")
    designation = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # breakpoint()
        _votes = Vote.objects.filter(tour=self).count()
        if _votes > 0 and _votes != self.poker_session.players:
            return
        self.designation = len(Tour.objects.filter(feature=self.feature).all()) + 1
        return super().save(*args, **kwargs)


class Messages(models.Model):
    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
