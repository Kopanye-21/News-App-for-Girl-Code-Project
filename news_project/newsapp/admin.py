from django.contrib import admin

# Register your models here.
from .models import SavedArticle, Advertisement

admin.site.register(SavedArticle)
admin.site.register(Advertisement)