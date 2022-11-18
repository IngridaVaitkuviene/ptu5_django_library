from django.contrib.auth import get_user_model
from django.db import models

# user profile tures visada tik viena user'i, todel OneToOneField

class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name="user",
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photo = models.ImageField("photo", upload_to='user_profile/photos', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} profile"
