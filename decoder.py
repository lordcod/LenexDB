import re

string = 'name="GeoLogix AG" street="Muristrasse 60" city="Bern" zip="3006" country="CH" phone="+41 31 356 80 56" fax="+41 31 356 80 81" email="info@splash-software.ch" internet="http://www.splash-software.ch"'
result = re.findall('([a-zA-Z\d]+)="([^"]+)"', string)
print(dict(result))