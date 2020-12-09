from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=120)
    main_story = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    mentioned_stock = models.CharField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    article_image = models.ImageField(default = 'default_article.jpg', upload_to='article_pictures')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bulletin_detail', kwargs={'pk': self.pk})