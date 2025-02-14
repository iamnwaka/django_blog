from django.contrib import admin
from .models import Blog, Category, Client

# ✅ Register Category correctly
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Show category names in admin

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'password')  # Show category names in admin

# ✅ Register Blog with custom admin options
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')  # Show these columns in admin
    search_fields = ('title', 'category__name')  # Enable search (use category__name)
    list_filter = ('category', 'created_at')  # Add filters
