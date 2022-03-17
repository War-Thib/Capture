from django import forms 
from .models import Labellized_Images, MLalgorithm

class ImageForm(forms.ModelForm):
    class Meta:
        model = Labellized_Images
        fields = ("label", "image", "ml_name")


class MLForm(forms.ModelForm):
    class Meta:
        model = MLalgorithm
        fields = ("user", "name")        