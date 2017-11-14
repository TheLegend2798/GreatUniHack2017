from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone
TITLES=[]
LOCATIONS = []

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

class PostAd(models.Model):
    name        = models.CharField(max_length=10)
    location    = models.CharField(max_length=3, choices=LOCATIONS)
    outbound     = models.CharField(max_length=15)
    inbound      = models.CharField(max_length=15)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        self.a=[float(self.name),str(self.location),str(self.outbound),str(self.inbound)]
        return self.a
