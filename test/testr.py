from lenexdb.baseapi import BaseApi

print(BaseApi)
xpath = 'test.lxf'
bapi = BaseApi(xpath)
print(bapi.athletes)
