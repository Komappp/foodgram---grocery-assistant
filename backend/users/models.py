from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name', 'password']

    def __str__(self):
        return self.username


class Following(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='follows',
        verbose_name='Подписчик',
        on_delete=models.CASCADE
    )
    follow = models.ForeignKey(
        User,
        related_name='followers',
        verbose_name='Подписан на',
        on_delete=models.CASCADE
    )

    class Meta:
        UniqueConstraint(fields=['follower', 'follow'], name='unique_follows')

    def __str__(self):
        return f'Подписка {self.follower} на {self.follow}'
