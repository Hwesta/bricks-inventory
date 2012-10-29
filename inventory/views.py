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
        inventory_form = InventoryForm(request.POST, prefix="inv")
        #kw_form = KeywordForm(request.POST, prefix="kw")
        if inventory_form.is_valid():
            part_str = inventory_form.cleaned_data['part']
            color = inventory_form.cleaned_data['color']
            count = inventory_form.cleaned_data['count']

            part = Part.objects.get(part_id__iexact=part_str)
            try:
                partinstance = PartInstance.objects.get(part=part, color=color)
            except PartInstance.DoesNotExist:
                print "PartInstance not exist, creating"
                partinstance = PartInstance(color=color, part=part, user_override=True)
                partinstance.save()
            print "partinstance", partinstance
            i = Inventory(partinstance=partinstance, count=count)
            print "inventory", i
            i.save()
            return HttpResponseRedirect(reverse(index))
    else:
        inventory_form = InventoryForm(prefix="inv")
        #KeywordFormSet = modelformset_factory(KeywordValue, form=KeywordForm, extra=0)
        #kw_formset = KeywordFormSet(queryset=Keyword.objects.all(), prefix="kw")
    return render(request, 'add_inventory.html',
        {'inventory_form': inventory_form,
        # 'kw_formset': kw_formset,
        })

