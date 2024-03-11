from django.contrib import admin
from .models import UserModel, blogdata, Category, Comment

# admin.site.register(UserModel)

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'password', 'is_varified', 'category']


@admin.register(blogdata)
class blogdataAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'category']

admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment',  ]

