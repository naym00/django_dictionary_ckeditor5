from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class CreatePassageForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'passage-title',
            'placeholder': 'Enter the title...'
        })
    )
    content = forms.CharField(
        required=False,
        widget=CKEditor5Widget(
            attrs={'class': 'django_ckeditor_5'},
            config_name='extends'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ''
            
            
class CreatePassageNote(forms.Form):
    note = forms.CharField(
        required=False,
        widget=CKEditor5Widget(
            attrs={'class': 'django_ckeditor_5'},
            config_name='extends'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ''