from django import forms
from .models import PostAd
import requests
import json

TITLES=[]
LOCATIONS = [('UK','UK')]

"""
r = requests.get("http://partners.api.skyscanner.net/apiservices/reference/v1.0/countries/en-US?apiKey=ha393385273835879384162930498674", json={"key": "ha393385273835879384162930498674"})
data=r.json()

for x in range(len(data['Countries'])):
    TITLES.append(data['Countries'][x]['Code'])

for i in (TITLES):
    r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/"+i+"/"+i+"/anytime/anytime?&apiKey=ha393385273835879384162930498674", json={"key": "ha393385273835879384162930498674"})
    data=r.json()
    for x in range(len(data['Places'])):
        LOCATIONS.append([data['Places'][x]['SkyscannerCode'],data['Places'][x]['Name']])
"""



class PostAdForm(forms.ModelForm):
    error_css_class = 'error'

    location = forms.ChoiceField(choices=LOCATIONS)

    class Meta:
        model = PostAd
        fields = {"name","location","outbound","inbound"}
        widgets = {
            'name': forms.TextInput(),
            'outbound': forms.TextInput(),
            'inbound': forms.TextInput(),
        }
