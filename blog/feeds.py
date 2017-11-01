from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Post

class BlogFeed(Feed):
    title = "RSS Feed"
    link = "/utkarsh/"
    description = "RSS feeds"

    def items(self):
        return Post.objects.all()

    def item_description(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_link(self, item):
        return reverse('rss')