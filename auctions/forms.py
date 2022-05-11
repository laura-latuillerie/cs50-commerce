from django.forms import ModelForm
from django import forms
from .models import CATEGORY_CHOICES, Listing

class NewListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'starting_bid', 'description', 'image', 'category']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'rows':2, 'maxlength': 1000, 'class': 'form-control'}),
      'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
      'image': forms.URLInput(attrs={'class': 'form-control'}),
      'category' : forms.Select(choices=CATEGORY_CHOICES, attrs={'class' : 'form-select'}),
      }