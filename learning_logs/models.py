from django.db import models

class Topic(models.Model):
    """A topic that user is learning about."""
    text = models.CharField(max_length = 200)
    date_ended = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """Returning string representation of the model."""
        return self.text