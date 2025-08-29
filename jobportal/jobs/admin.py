from django.contrib import admin
from .models import Category, Job, Application, SavedJob

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "category", "location", "posted_at")
    list_filter = ("category","location","posted_at")
    search_fields = ("title","company","description")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name","email","job","created_at")
    search_fields = ("name","email")

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("user","job","created_at")
