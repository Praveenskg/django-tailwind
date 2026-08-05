import datetime

from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("travel_date", "num_travelers", "notes")
        widgets = {
            "travel_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "num_travelers": forms.NumberInput(attrs={"min": 1, "max": 50}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Any special requirements…"}),
        }

    def clean_travel_date(self):
        travel_date = self.cleaned_data["travel_date"]
        if travel_date < datetime.date.today():
            raise forms.ValidationError("Please choose a future travel date.")
        return travel_date

    def clean_num_travelers(self):
        n = self.cleaned_data["num_travelers"]
        if n < 1:
            raise forms.ValidationError("At least 1 traveler required.")
        return n
