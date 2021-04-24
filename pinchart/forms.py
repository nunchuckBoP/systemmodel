from django import forms
import pinchart.models as models

class WordForm(forms.ModelForm):
    """
        WordForm - when the pinchart object is
        known and is a hidden input into the 
        form
    """
    class Meta:
        model = models.Word
        fields = ['pinchart', 'name', 'type', 'address_template']
        widgets = {
            'pinchart':forms.HiddenInput(),
        }

class BitDescriptionForm(forms.ModelForm):
    """
        BitDescriptionForm - model form when the word
        is a hidden input into the form. Meaning, the
        word is known and is a parameter into the
        view
    """
    class Meta:
        model = models.BitDescription
        fields = ['word', 'bit', 'device', 'description']
        widgets = {
            'word':forms.HiddenInput(),
        }