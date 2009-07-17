from django.contrib.syndication.feeds import FeedDoesNotExist, Feed

from models import Post, Category

class LatestEntriesByCategory(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug=bits[0])

    def title(self, category):
        return category.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, category):
        return "Les derniers items de la category %s" % category

    def items(self, category):
        return Post.availables.filter(categories=category)[:20]

class LatestEntries(Feed):
    title = "Derniers items"
    link = "/"
    description = "Derniers items du site plop plop plop"

    def items(self):
        return Post.availables.all()[:20]
    
    def item_pubdate(self, item):
        return item.published_on
    
    def item_author_name(self, item):
        return item.author.get_full_name()
    
    def item_categories(self, item):
        return item.categories.all()
    
