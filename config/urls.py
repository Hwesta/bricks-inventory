from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('lego.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'inventory.views.index'),
    url(r'^add/inventory/', 'inventory.views.add_inventory'),
    url(r'^add/location/', 'inventory.views.add_location'),
    url(r'^add/keyword/', 'inventory.views.add_keyword'),

    url(r'^inventory/$', 'inventory.views.view_inventory'),
    url(r'^inventory/(\d+)$', 'inventory.views.view_inventory_item'),

    url(r'^check_location/$', 'inventory.views.check_location'),
)
