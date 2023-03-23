from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class TalmudText(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    hebrew_content = models.TextField()

class WikipediaArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    talmud_text = models.ForeignKey(TalmudText, on_delete=models.CASCADE, null=True)
    wikipedia_article = models.ForeignKey(WikipediaArticle, on_delete=models.CASCADE, null=True)

class Highlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    talmud_text = models.ForeignKey(TalmudText, on_delete=models.CASCADE, null=True)
    wikipedia_article = models.ForeignKey(WikipediaArticle, on_delete=models.CASCADE, null=True)
    highlighted_text = models.TextField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    talmud_text = models.ForeignKey(TalmudText, on_delete=models.CASCADE, null=True)
    wikipedia_article = models.ForeignKey(WikipediaArticle, on_delete=models.CASCADE, null=True)
    content = models.TextField()
