from django import forms
from .models import Booking


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])

class BookingForm(forms.ModelForm): 

  

    # create meta class 

    class Meta: 

        # specify model to be used 

        model = Booking

  

        # specify fields to be used 

        fields = [ 

            "check_in", 

            "check_out"] 