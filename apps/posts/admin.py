from django.contrib import admin

from apps.posts.models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'tag_names', 'created_at')
    filter_horizontal = ('tags',)
    readonly_fields = ('tag_names',)

    @staticmethod
    def tag_names(obj):
        return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
