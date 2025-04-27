from django.contrib import admin
from .models import Comment
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user","post","created_date","status",)

    list_filter = ('status', 'created_date')
    search_fields = ('content',)