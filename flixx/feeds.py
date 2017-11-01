from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import *

class UT(Feed):
    title = 'hamara bajaj'
    link = 'reviews/'
    description = 'a kiss is a kiss is a kiss'

    def items(self):
        return review.objects.all()

    def item_title(selfself, item):
        return item.l

    def item_description(self, item):
        return "Description is also " + item.l

    def item_link(self, item):
        return reverse('reviews')