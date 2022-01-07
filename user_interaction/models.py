from django.db import models


class UserInteraction(models.Model):
    user_id = models.PositiveIntegerField()
    content_id = models.PositiveIntegerField()
    is_like = models.BooleanField(null=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user_id', 'content_id']
