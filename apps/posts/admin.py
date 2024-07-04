from django.contrib import admin

from apps.posts.models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('caption', 'user', 'tag_names', 'created_at')
    filter_horizontal = ('tags',)
    readonly_fields = ('tag_names',)

    @staticmethod
    def tag_names(obj):
        return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    readonly_fields = ('post_count',)

    @staticmethod
    def post_count(obj):
        return obj.posts.count()
    
    
@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    ist_display = ('post', 'user', 'created_at')
        

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'video')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')

