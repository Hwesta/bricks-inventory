# From Django (alphabetical)
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

# From Inventory
from inventory.forms import InventoryForm, LocationForm, KeywordForm
from inventory.models import Part, Category, Color, PartInstance, Set
from inventory.models import Inventory, Location, LocationAmount, Keyword, KeywordValue

def index(request):
    return render(request, 'index.html')

def add_inventory(request):
    """ Adds a piece of inventory. """
    LocationFormSet = modelformset_factory(LocationAmount,
        fields = ('location', 'amount'),
        extra=3)
    KeywordFormSet = modelformset_factory(KeywordValue,
        fields = ('keyword', 'value'),
        extra = Keyword.objects.count())

    if request.method == 'POST':
        inventory_form = InventoryForm(request.POST, prefix="inv")
        location_formset = LocationFormSet(request.POST, prefix = "loc")
        kw_formset = KeywordFormSet(request.POST, prefix="kw")
        if inventory_form.is_valid() and location_formset.is_valid() \
                and kw_formset.is_valid():
            # Is there an easier way to do this with an Inventory ModelForm?
            part_str = inventory_form.cleaned_data['part']
            color = inventory_form.cleaned_data['color']
            part = Part.objects.get(part_id__iexact=part_str)
            try:
                partinstance = PartInstance.objects.get(part=part, color=color)
            except PartInstance.DoesNotExist:
                print "PartInstance not exist, creating"
                partinstance = PartInstance(color=color, part=part, user_override=True)
                partinstance.save()
            print "partinstance", partinstance
            inventory = Inventory(partinstance = partinstance)
            print "inventory", inventory
            inventory.save()

            def add_inventory_to_formset(i):
                i.inventory = inventory
                i.save()

            instances = location_formset.save(commit = False)
            map(add_inventory_to_formset, instances)

            instances = kw_formset.save(commit = False)
            map(add_inventory_to_formset, instances)

            return HttpResponseRedirect(reverse(index))
    else:
        inventory_form = InventoryForm(prefix="inv")
        location_formset = LocationFormSet(prefix = "loc",
            queryset = LocationAmount.objects.none())
        kw_formset = KeywordFormSet(prefix="kw",
            queryset=Keyword.objects.none())
    return render(request, 'add_inventory.html',
        {'inventory_form': inventory_form,
         'location_formset': location_formset,
         'kw_formset': kw_formset,
        })


def add_location(request):
    """ Adds a location. """
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            new_loc = location_form.save()
            messages.success(request, "%s added." % new_loc.name)
            if 'add_another' in request.POST:
                return HttpResponseRedirect(reverse(add_location))
            else:
                return HttpResponseRedirect(reverse(index))
    else:
        location_form = LocationForm()
    return render(request, 'add_location.html',
        {'location_form': location_form,
        })

def add_keyword(request):
    """ Adds a new keyword. """
    if request.method == 'POST':
        keyword_form = KeywordForm(request.POST)
        if keyword_form.is_valid():
            new_kw = keyword_form.save()
            messages.success(request, "Keyword %s added." % new_kw.name)
            if 'add_another' in request.POST:
                return HttpResponseRedirect(reverse(add_keyword))
            else:
                return HttpResponseRedirect(reverse(index))
    else:
        keyword_form = KeywordForm()
    return render(request, 'add_keyword.html',
        {'keyword_form': keyword_form,
        })

def view_inventory(request):
    items = Inventory.objects.filter(deleted=False)
    return render(request, 'view_inventory.html',
        {'items': items})

def view_inventory_item(request, inventory_id):
    inventory = Inventory.objects.get(pk=inventory_id)

    return render(request, 'view_inventory_item.html',
        {'inventory': inventory,})
