from django import forms
# from passage import models as MODELS_PASS
from django_ckeditor_5.widgets import CKEditor5Widget

# class CreatePassageForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['content'].required = False
        
#         # Remove labels for all fields
#         for field_name in self.fields:
#             self.fields[field_name].label = ''
#             self.fields['title'].widget.attrs.update({
#                 'class': 'passage-title',
#                 'placeholder': 'Enter the title...'
#             })

#     class Meta:
#         model=MODELS_PASS.Passage
#         fields=['title', 'content']
        
#         # widgets = {
#         #       'content': CKEditor5Widget(
#         #           attrs={"class": "django_ckeditor_5"}, config_name="extends"
#         #       )
#         #   }
#         content = CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends')

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