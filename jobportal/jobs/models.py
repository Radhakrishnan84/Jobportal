from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    class Meta: ordering = ["name"]
    def __str__(self): return self.name

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs")
    location = models.CharField(max_length=120)
    description = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    class Meta: ordering = ["-posted_at"]
    def __str__(self): return f"{self.title} @ {self.company}"

def resume_upload_path(instance, filename):
    return f"resumes/job_{instance.job_id}/{filename}"

def validate_file_size(value):
    max_mb = 2
    if value.size > max_mb * 1024 * 1024:
        from django.core.exceptions import ValidationError
        raise ValidationError(f"Max file size is {max_mb}MB")

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    resume = models.FileField(
        upload_to=resume_upload_path,
        validators=[FileExtensionValidator(["pdf","doc","docx"]), validate_file_size],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} -> {self.job}"

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "job")
    def __str__(self): return f"{self.user.username} saved {self.job.title}"