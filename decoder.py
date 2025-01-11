import re

string = ''
result = re.findall('([a-zA-Z\d]+)="([^"]+)"', string)
print(dict(result))