from django.db import models

# Create your models here.

class Color(models.Model):
    """
    The color's name (as used by the CSS 'color' attribute, meaning
    lowercase values are required), and a boolean of whether it's "liked"
    or not. There are NO USERS in this demo webapp, which is why there's no
    link/ManyToManyField to the User table.

    This implies that the website is only useable for ONE USER. If multiple
    users used it at the same time, they'd be all changing the same values
    (and would see each others' changes when they reload the page).
    """
    name = models.CharField(max_length=20)
    is_favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']