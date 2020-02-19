""" Django Models Utilities. """

# Django
from django.db import models


class TimeStamps(models.Model):
    """ Facebook abstract class

    This models acts as a abstract class for timestamps fields.
    This class provides the following fields:
        - created (DateTime): Store the datetime the object was created.
        - updated (DateTIme): Store the datetime the object was updated
    """

    created = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text = 'Date time on wich the object was created'
    )
    updated = models.DateTimeField(
        'updated at',
        auto_now=True,
        help_text = 'Date time on wich the object was updated'
    )

    class Meta: 
        """ Meta options. """
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-updated']




