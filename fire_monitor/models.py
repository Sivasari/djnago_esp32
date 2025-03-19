from django.db import models
from django.utils.timezone import now

class FireSensor(models.Model):
    status = models.BooleanField(default=False)  # True if fire detected
    updated_at = models.DateTimeField(default=now)  # Stores fire event time

    def save(self, *args, **kwargs):
        """Update timestamp only when status changes."""
        if self.pk:  # Check if the object exists in the database
            existing = FireSensor.objects.get(pk=self.pk)
            if existing.status != self.status:  # Update only if status changes
                self.updated_at = now()
        else:
            self.updated_at = now()  # Set initial creation time

        super().save(*args, **kwargs)  # Call Django's default save method

    def __str__(self):
        return f"🔥 Fire Detected at {self.updated_at}" if self.status else f"✅ No Fire (Last Checked: {self.updated_at})"
