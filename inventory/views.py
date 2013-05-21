# From Django (alphabetical)
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import simplejson

# From Inventory
from inventory.forms import InventoryForm, LocationForm, KeywordForm, RequiredFormSet
from inventory.models import Part, Category, Color, PartInstance, Set
from inventory.models import Inventory, Location, LocationAmount, Keyword, KeywordValue

def index(request):
    return render(request, 'index.html')

def add_inventory(request):
    """ Adds a piece of inventory. """
    LocationFormSet = modelformset_factory(LocationAmount,
        fields = ('location', 'amount'),
        extra=3,
        formset=RequiredFormSet)
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
            inventory = Inventory(partinstance = partinstance)
            inventory.save()

            def add_inventory_to_formset(i):
                i.inventory = inventory
                i.save()

            instances = location_formset.save(commit = False)
            map(add_inventory_to_formset, instances)

            previous_keywords = []
            def process_kw_formset(i):
                # Add the inventory to each item and save it
                i.inventory = inventory
                i.save()
                # Save the keyword and value for populating next time
                d = {'keyword': i.keyword.pk, 'value': i.value}
                previous_keywords.append(d)

            instances = kw_formset.save(commit = False)
            map(process_kw_formset, instances)
            request.session['previous_keywords'] = previous_keywords

            if 'add_another' in request.POST:
                return redirect(add_inventory)
            else:
                return redirect(index)
    else:
        inventory_form = InventoryForm(prefix="inv")
        location_formset = LocationFormSet(prefix = "loc",
            queryset = LocationAmount.objects.none())

        if 'previous_keywords' in request.session:
            # Use keywords from previous form, if they exist
            previous_keywords = request.session['previous_keywords']
            del request.session['previous_keywords']
            kw_formset = KeywordFormSet(prefix="kw",
                queryset=Keyword.objects.none(),
                initial=previous_keywords)
        else:
            kw_formset = KeywordFormSet(prefix="kw",
                queryset=Keyword.objects.none())

    return render(request, 'add_inventory.html',
        {'inventory_form': inventory_form,
         'location_formset': location_formset,
         'kw_formset': kw_formset,
        })

def check_location(request):
    results = []
    if request.method == 'GET':
        if request.GET.has_key('part_id'):
            part_id = request.GET['part_id']
            color = request.GET['color']
            # check for stuff
            similar_items = LocationAmount.objects.filter(inventory__partinstance__part__part_id__iexact=part_id)
            if color: # Color might not be specified
                similar_items = similar_items.filter(inventory__partinstance__color__pk=color)
            # Include all display information in JSON
            for i in similar_items.iterator():
                return_dict = {}
                return_dict['amount'] = i.amount
                return_dict['inventory'] = {
                    'part_name': i.inventory.partinstance.part.name,
                    'part_id': i.inventory.partinstance.part.part_id,
                    'color': i.inventory.partinstance.color.name,
                    }
                return_dict['location'] = {
                    'name': i.location.name,
                    'pk': i.location.pk
                    }

                results.append(return_dict)
    results = simplejson.dumps(results)
    return HttpResponse(results, mimetype='application/json')

def add_location(request):
    """ Adds a location. """
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            new_loc = location_form.save()
            messages.success(request, "%s added." % new_loc.name)
            if 'add_another' in request.POST:
                return redirect(add_location)
            else:
                return redirect(index)
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
                return redirect(add_keyword)
            else:
                return redirect(index)
    else:
        keyword_form = KeywordForm()
    return render(request, 'add_keyword.html',
        {'keyword_form': keyword_form,
        })

def view_inventory(request):
    # Group by part instance, annotate with count of items
    items = Inventory.objects.filter(deleted=False).values('partinstance').annotate(amount=Sum('locationamount__amount'))

    # Convert foreign key back to the object
    def foreign_key_to_object(d):
        d['partinstance'] = PartInstance.objects.get(pk=d['partinstance'])
        return d
    items = map(foreign_key_to_object, items)

    return render(request, 'view_inventory.html',
        {'items': items})

def view_inventory_item(request, part_id):
    try:
        part = Part.objects.get(part_id=part_id)
        items = Inventory.objects.filter(partinstance__part=part).filter(deleted=False)
        items = items.annotate(total_amount=Sum('locationamount__amount'))
    except Part.DoesNotExist:
        print "exception"
        part = None
        items = None

    return render(request, 'view_inventory_item.html',
        {'part': part,
         'items': items,})
