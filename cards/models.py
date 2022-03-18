from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Set(models.Model):
    """
    Creates a folder for the flashcards
    Like a category section Eg: German,..
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="Untitled")
    color = models.CharField(max_length=200, default="grey")
    starred = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_visited = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.color}"

    class Meta:
        verbose_name = _("Set of flashcard")
        verbose_name_plural = _("Set of flashcards")


class Card(models.Model):
    """
    Stores the question and answer
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="Untitled")
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    question = models.CharField(null=True, blank=True, max_length=2000)
    answer = models.CharField(null=True, blank=True, max_length=2000)
    image_url = models.URLField(null=True, blank=True)
    starred = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.set.name}"
