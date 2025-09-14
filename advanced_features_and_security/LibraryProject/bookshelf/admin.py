# bookshelf/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role", "date_of_birth", "profile_photo")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)