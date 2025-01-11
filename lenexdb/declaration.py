import re


def fix_declaration(text: str):
    def change(match: re.Match):
        return f'{match.group(1)}="{match.group(2)}"'

    return re.sub(r"([a-z]+)='([^']+)'",
                  change, text)


def get_declaration(text: str):
    return re.findall(r"<\?xml.*\?>", text)[0]


def change_declaration(text: str):
    declaration = get_declaration(text)
    declaration2 = fix_declaration(declaration)
    return text.replace(declaration, declaration2)
