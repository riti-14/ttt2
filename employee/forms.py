from django.forms import ModelForm
from .models import empleave_model
# ,myuser_model
# from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.widgets import DateInput # need to import



class empleave_form(ModelForm):
    class Meta:
        model= empleave_model
        fields='__all__'    

        widgets = {
            'from1': DateInput(attrs={'type': 'date'}),
            'to1': DateInput(attrs={'type': 'date'}),
        }



# class myuser_form(UserCreationForm):
#     class Meta:
#         model=myuser_model
#         fields='__all__'



