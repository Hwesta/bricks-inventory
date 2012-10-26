from django import forms
from django.forms import ModelForm
from inventory.models import Part, Category, Color, PartInstance, Set
from inventory.models import Inventory, Location, Keyword, KeywordValue


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
    count = forms.IntegerField(min_value=1)

    def clean_part(self):
        data = self.cleaned_data['part']
        try:
            Part.objects.get(part_id__iexact=data)
        except:
            raise forms.ValidationError("Specified part does not exist")
        return data

