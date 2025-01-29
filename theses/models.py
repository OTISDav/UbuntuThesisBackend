from django.db import models
from django.contrib.auth import get_user_model

class Thesis(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    summary = models.TextField()
    document = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    field_of_study = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.title



User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔹 Relation avec l'utilisateur
    thesis = models.ForeignKey('Thesis', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thesis')

class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔹 Relation avec l'utilisateur
    thesis = models.ForeignKey('Thesis', on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
