from django import forms
from django.forms import ModelForm
from inventory.models import Part, Category, Color, PartInstance, Set
from inventory.models import Inventory, Location, LocationAmount, Keyword, KeywordValue


# Form should enter:
# Color
# PartNumber (goes to Part)
# (add PartInstance automatically if not in there)
# Count
# Location
#   create new as needed (this is in, this is in...)
# Keywords
class InventoryForm(forms.Form):
    part = forms.CharField()
    color = forms.ModelChoiceField(queryset=Color.objects.all())

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

class KeywordForm(forms.ModelForm):
    class Meta:
        model = KeywordValue
        fields = ('keyword', 'value')
