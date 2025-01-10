from lenexdb.baseapi import BaseApi
import lxml.etree as ET

print(BaseApi)
xpath = 'result/test.lxf'
bapi = BaseApi(xpath)
bapi.save('result/test2.lef')
print(bapi.athletes)

xml_string = ET.tostring(
    bapi.root,
    encoding='Windows-1251',
    method="xml",
    xml_declaration=True
)
with open('result/result2.lef', 'wb+') as f:
    f.write(xml_string)