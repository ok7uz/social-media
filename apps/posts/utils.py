from apps.posts.models import Tag


def add_tags_to_post(post, tags):
    post.tags.clear()
    for tag in tags:
        tag_instance, _ = Tag.objects.get_or_create(name=tag)
        post.tags.add(tag_instance)
