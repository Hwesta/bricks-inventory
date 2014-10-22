from django import forms
from inventory import models


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
        return models.Color.objects.get(color_id=obj['color_id'])


class InventoryForm(forms.Form):
    part = forms.CharField()

    sorted_color = models.Color.objects.extra(select={'color_count': 'SELECT COUNT(color_id) FROM inventory_partinstance WHERE inventory_partinstance.color_id=inventory_color.color_id'}).order_by('-color_count')
    color = forms.ModelChoiceField(queryset=sorted_color)

    def clean_part(self):
        data = self.cleaned_data['part']
        try:
            models.Part.objects.get(part_id__iexact=data)
        except:
            raise forms.ValidationError("Specified part does not exist")
        return data


class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = ('name', 'parent')


class KeywordForm(forms.ModelForm):
    class Meta:
        model = models.Keyword
        fields = ('name',)


class RequiredFormSet(forms.models.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False
