from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
#from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pictures')
    date_of_birth = models.DateField(default = datetime.now)

    def __str__(self):
        return f'{self.user.username} Profile'

    # RESIZE IMAGES ON DEV
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)