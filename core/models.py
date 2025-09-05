from django.db import models

class AllowedUser(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="user")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} ({self.role})"