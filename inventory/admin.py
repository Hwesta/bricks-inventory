from django.contrib import admin
from inventory.models import Part, Category, Color, PartInstance, Set, Inventory, Location, Keyword, KeywordValue

admin.site.register(Part)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(PartInstance)
admin.site.register(Set)
admin.site.register(Inventory)
admin.site.register(Location)
admin.site.register(Keyword)
admin.site.register(KeywordValue)

