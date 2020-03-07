from django import forms 
from django.utils.translation import gettext_lazy as _
from .models import Guest
from .constants import NGUESTS_CHOICES, limit_date
import datetime

class NewBookingForm(forms.Form):
    entry_date     = forms.DateField(label="Fecha de entrada", initial=datetime.date.today, required=True, 
                                    error_messages={'invalid': 'Formato de fecha no válido'}, 
                                    input_formats=['%Y-%m-%d'], 
                                    widget= forms.TextInput(attrs={'class':'datepicker'}))

    departure_date = forms.DateField(label="Fecha de salida", initial=datetime.date.today, required=True,
                                    error_messages={'invalid': 'Formato de fecha no válido'},
                                    input_formats=['%Y-%m-%d'],
                                    widget= forms.TextInput(attrs={'class':'datepicker'}))

    number_guests  = forms.ChoiceField(choices = NGUESTS_CHOICES, label="Número de invitados", widget=forms.Select(), required=True)

    def clean(self):
        cleaned_data   = super().clean()
        entry_date     = cleaned_data.get("entry_date")
        departure_date = cleaned_data.get("departure_date")

        if entry_date and departure_date:
            if entry_date > departure_date:
                raise forms.ValidationError(
                    "La fecha de entrada no puede ser posterior a la fecha de salida"
                )
            elif entry_date < datetime.date.today():
                raise forms.ValidationError(
                    "La fecha de entrada no puede ser anterior a la fecha actual"
                )
            elif departure_date > limit_date:
                raise forms.ValidationError(
                    "La fecha de salida no puede ser posterior a la fecha '2020-12-31'"
                )

class ContactForm(forms.ModelForm):
    class Meta:
        model  = Guest
        fields = ('name', 'phone', 'email')
        labels = {'name': _('Nombre'), 'phone': _('Teléfono')}
  