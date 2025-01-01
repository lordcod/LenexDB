import zipfile
from os import path
from lxml import etree
import lxml.etree as ET

encodings = {
    'uc': 'unicode',
    'u8': 'utf-8' 
}


# xpath = r"C:\Users\2008d\Downloads\Telegram Desktop\20250209_Lenex.lxf"
xpath = 'test.lxf'


def var1():
    with zipfile.ZipFile(xpath) as myzip:
        for file in myzip.filelist:
            print('Saving...', file.filename)
            with myzip.open(file) as f:
                fn = path.join('test', file.filename)
                with open(fn, 'wb+') as fw:
                    fw.write(f.read())

def var2():
    with zipfile.ZipFile(xpath) as myzip:
        for file in myzip.filelist:
            print('Saving...', file.filename)
            with myzip.open(file) as f:
                tree = ET.parse(f)
                root = tree.getroot()
            
            fn = path.join('test', file.filename)
            xml_string = ET.tostring(root, encoding=encodings.get(input('> ')), method='xml')
            mode = 'w+' if isinstance(xml_string, str) else 'wb+'
            print(mode)
            with open(fn, mode) as f:
                f.write(xml_string)

var2()