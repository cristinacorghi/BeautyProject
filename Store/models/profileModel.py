from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="static/img/avatars/", null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Profile'  # serve per togliere la "s" finale nel model

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')
