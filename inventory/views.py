# From Django (alphabetical)
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# From Inventory
from inventory.forms import InventoryForm
from inventory.models import Part, Category, Color, PartInstance, Set
from inventory.models import Inventory, Location, Keyword, KeywordValue

def index(request):
    return render(request, 'index.html')

def add_inventory(request):
    """ Adds a piece of inventory. """
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            part = form.cleaned_data['part']
            color = form.cleaned_data['color']
            count = form.cleaned_data['count']

            print "part", part, "color type", type(color)
            part_obj = Part.objects.get(part_id__iexact=part)
            print "part_obj", part_obj, type(part_obj)
            partinstance = PartInstance.objects.get(part=part_obj, color=color)
            # HELP color+part do not uniquely define a partinstance
            # codename actually uniquely defines a partinstance, and color+part are actually useless
            # How to determine which version of the partinstance (same color+part) to attaching Inventory to?
            # Should we keep the codenames??

            # partinstance = PartInstance.objects.filter(part=part_obj)#, color=color)
            print "partinstance", partinstance
            #i = Inventory(partinstance=partinstance, count=count)
            #i.save()
            return HttpResponseRedirect(reverse(index))
    else:
        form = InventoryForm()
    return render(request, 'add_inventory.html', {'form': form, })

