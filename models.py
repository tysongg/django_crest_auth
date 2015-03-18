from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone

class CRESTUserManager(BaseUserManager):

    def create_user(self, id, character_name, refresh_token=""):
        """
        Created and save User
        """
        user = self.model(id=id, character_name=character_name, refresh_token=refresh_token)
        user.save(using=self._db)
        return user

class CRESTUser(models.Model):
    """
    A minimal User model used to login users after successful SSO authentication

    ID and Character Name fields are required
    """
    id = models.IntegerField(primary_key=True)
    character_name = models.CharField(max_length=250, unique=True)
    refresh_token = models.CharField(max_length=250, default="")
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = CRESTUserManager()

    USERNAME_FIELD = 'character_name'
    REQUIRED_FIELDS = [id, character_name]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        """
        Return the character name
        """
        return self.character_name

    def get_short_name(self):
        """
        Return the character name
        """
        return self.character_name

    def __unicode__(self):
        return self.character_name