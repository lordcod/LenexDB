from lenexdb.baseapi import BaseApi, Athlete, Club, Event
import json
import openpyxl
import re
import codecs

xpath = 'test.lxf'
bapi = BaseApi(xpath)
print(bapi.athletes)
