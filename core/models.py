from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    description = models.TextField()
    file = models.FileField(upload_to='applications/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"