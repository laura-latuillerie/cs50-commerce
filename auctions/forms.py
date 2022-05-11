from django.forms import ModelForm
from django import forms
from .models import CATEGORY_CHOICES, Listing

class NewListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'starting_bid', 'description', 'image', 'category']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Ex : Big Rainbow Kawaii Night Lamp'}),
      'description': forms.Textarea(attrs={'rows':5, 'maxlength': 1024, 'class': 'form-control', 'placeholder' : 'Useful informations only'}),
      'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder' : 'Only digits'}),
      'image': forms.URLInput(attrs={'class': 'form-control', 'placeholder' : 'https://image-link.com'}),
      'category' : forms.Select(choices=CATEGORY_CHOICES, attrs={'class' : 'form-select'})
    }
    labels = {
      'image': 'Image (URL only)',
      'category' : 'Choose category in list'
      }