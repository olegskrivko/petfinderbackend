# articles/models.py
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    summary = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    public = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Paragraph(models.Model):
    article = models.ForeignKey(Article, related_name="paragraphs", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    text = models.TextField()
    order = models.IntegerField(default=0)
    image_prompt = models.TextField()

    def __str__(self):
        return f'{self.article.title} - {self.title}'

    class Meta:
        ordering = ['order']

