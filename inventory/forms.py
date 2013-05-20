from django import forms
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet
from inventory.models import Part, Category, Color, PartInstance, Set
from inventory.models import Inventory, Location, LocationAmount, Keyword, KeywordValue
from django.db.models import Count


# Form should enter:
# Color
# PartNumber (goes to Part)
# (add PartInstance automatically if not in there)
# Count
# Location
#   create new as needed (this is in, this is in...)
# Keywords

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return Color.objects.get(color_id=obj['color_id'])

class InventoryForm(forms.Form):
    part = forms.CharField()
    
    sorted_color = Color.objects.extra(select={'color_count':'SELECT COUNT(color_id) FROM inventory_partinstance WHERE inventory_partinstance.color_id=inventory_color.color_id'}).order_by('-color_count')
    color = forms.ModelChoiceField(queryset=sorted_color)
 
    def clean_part(self):
        data = self.cleaned_data['part']
        try:
            Part.objects.get(part_id__iexact=data)
        except:
            raise forms.ValidationError("Specified part does not exist")
        return data

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'parent')

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('name',)

class RequiredFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False
