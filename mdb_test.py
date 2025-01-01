import zipfile
from os import path
from lefdef import C_LefReader
import lxml.etree as ET
import xml.etree.ElementPath as EP
import codecs
import shutil
import os

def make_lftfile(base_name, base_dir):
    zip_filename = base_name + ".lxf"
    archive_dir = os.path.dirname(base_name)

    if archive_dir and not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    with zipfile.ZipFile(zip_filename, "w",
                         compression=zipfile.ZIP_DEFLATED) as zf:
        arcname = os.path.normpath(base_dir)
        base_dir = os.path.normpath(base_dir)
        if arcname != os.curdir:
            zf.write(base_dir, arcname)
        for dirpath, dirnames, filenames in os.walk(base_dir):
            arcdirpath = dirpath
            arcdirpath = os.path.normpath(arcdirpath)
            for name in sorted(dirnames):
                path = os.path.join(dirpath, name)
                arcname = os.path.join(arcdirpath, name)
                zf.write(path, arcname)
            for name in filenames:
                path = os.path.join(dirpath, name)
                path = os.path.normpath(path)
                if os.path.isfile(path):
                    arcname = os.path.join(arcdirpath, name)
                    zf.write(path, arcname)

    return zip_filename


# xpath = r'C:\Users\2008d\Downloads\Telegram Desktop\20250209_Lenexttt.lxf'
xpath = 'test.lxf'

def save_all(myzip: zipfile.ZipFile):
    for file in myzip.filelist:
        print('Saving...', file.filename)
        with myzip.open(file.filename, 'r') as f:
            fn = path.join('lenex', 'data', file.filename)
            with open(fn, 'wb+') as fw:
                fw.write(f.read())


def get_count_athletes(root: ET.Element):
    clubs = root.find('MEETS').find('MEET').find('CLUBS').findall('CLUB')
    count = 0
    for club in clubs:
        print(club.attrib)
        if club.find('ATHLETES'):
            count += len(club.find('ATHLETES').findall('ATHLETE'))
    return count

def create_club(name: str):
    club = ET.Element('CLUB')
    club.set('name', name)
    contact = ET.Element('CONTACT')
    contact.set('name', name)
    club.append(contact)
    return club

def create_athlete(root: ET.Element, club: ET.Element, lastname: str, firstname: str, birthdate: str, gender: str) -> bool:
    athletes = club.find('ATHLETES')
    if athletes is None:
        athletes = ET.Element('ATHLETES')
        club.append(athletes)
    
    aid = get_count_athletes(root)+1
    print(aid)
    
    athlete = ET.Element('ATHLETE')
    athlete.set('lastname', lastname)
    athlete.set('firstname', firstname)
    athlete.set('birthdate', birthdate)
    athlete.set('gender', gender)
    athlete.set('athleteid', str(aid))
    athletes.append(athlete)
    
    return athlete

def create_entry(athlete: ET.Element, event_id: int, entrytime: str):
    entries = club.find('ENTRIES')
    if entries is None:
        entries = ET.Element('ENTRIES')
        athlete.append(entries)
    
    entry = ET.Element('ENTRY')
    entry.set('eventid', str(event_id))
    entry.set('entrytime', entrytime)
    entries.append(entry)
    
    return entry

with zipfile.ZipFile(xpath) as myzip:
    save_all(myzip)
    for file in myzip.filelist:
        fn = path.join('lenex', 'data', file.filename)
        fndt = path.join('lenex', 'dt', file.filename)
        
        tree = ET.parse(fn)
        root = tree.getroot()
        
        e_clubs = root.find('MEETS').find('MEET').find('CLUBS')
        if e_clubs is None:
            e_clubs = ET.Element('CLUBS')
            root.find('MEETS').find('MEET').append(e_clubs)
        club = create_club('СШОР 64')
        e_clubs.append(club)
        
        athlete = create_athlete(
            root,
            club,
            'Саша',
            'Коднратиев',
            '2008-12-24',
            'M'
        )
        
        create_entry(
            athlete,
            1804,
            '00:09:00.00'
        )
        
        xml_string = ET.tostring(root, encoding='unicode', method='xml')
        with open(fndt, 'w+') as f:
            f.write(xml_string)


make_lftfile('test', 'lenex/dt')