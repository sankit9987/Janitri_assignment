from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Patient(models.Model):
    # minimal patient metadata
    first_name = models.CharField(
        max_length=120,
    )
    last_name = models.CharField(
        max_length=120,
        blank=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            (
                f"{self.first_name} {self.last_name}"
                if self.last_name
                else self.first_name
            ),
        )


class HeartRate(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name="heart_rates",
        on_delete=models.CASCADE,
    )
    bpm = models.PositiveIntegerField()
    recorded_at = models.DateTimeField()
    note = models.CharField(
        max_length=255,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-recorded_at"]

    def clean(self):

        if not (20 <= self.bpm <= 250):
            raise ValidationError(
                {"bpm": "bpm must be between 20 and 250"},
            )

    def __str__(self):
        return f"{self.patient} - {self.bpm} @ {self.recorded_at.isoformat()}"
