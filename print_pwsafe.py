import datetime as dt
import xml.etree.ElementTree as ElementTree


class PWSafeEntry:
    def __init__(self, entry):
        self.entry = entry
        self.group = ''
        self.title = ''
        self.username = ''
        self.group = ''
        self.note = ''
        self.email = ''
        self.url = ''
        for field in self.entry:
            key = str(field.tag)
            if key == 'group':
                self.group = field.text
            elif key == 'title':
                self.title = field.text
            elif key == 'username':
                self.username = field.text
            elif key == 'notes':
                self.note = field.text
            elif key == 'email':
                self.email = field.text
            elif key == 'url':
                self.url = field.text

    def __repr__(self):
        result = ''
        if self.group:
            result += f'## {self.group}\n'
        result += f'*{self.title}* Details\n'
        return result

    @property
    def header(self):
        result  = 'Title | User | Password | Comment | Email | URL\n'
        result += '------|------|----------|---------|-------|----\n'
        return result

    @property
    def line(self):
        result = f'{self.title}|{self.username}|{self.group}|{self.note}|{self.email}|{self.url}\n'
        return result


class PrintPySafe:
    def __init__(self, file_name):
        self.tree = ElementTree.parse(file_name)
        self.file_name = file_name
        # root = tree.getroot()

    def __repr__(self):
        root = self.tree.getroot()
        result = f'# Password File\n'
        group = None
        for entry in root:
            if str(entry.tag) == 'entry':
                e = PWSafeEntry(entry)
                if e.group != group:
                    if e.group:
                        result += f'## {e.group}\n'
                    else:
                        result += f'## Passwords with no group\n'
                    result += e.header
                    group = e.group
                result += e.line
            elif str(entry.tag) == 'Preferences':
                pass
            else:
                result += f'\n### Unknown tag &rarr; {entry.tag}\n'
        result += '### *File data*\n'
        result += 'Field | Value\n'
        result += '------|------\n'
        result += 'Database | {}\n'.format(root.attrib['Database'])
        result += 'WhenLastSaved |  {}\n'.format(root.attrib['WhenLastSaved'])
        result += 'WhoSaved |  {}\n'.format(root.attrib['WhoSaved'])
        result += 'FromDatabaseFormat |  {}\n'.format(root.attrib['FromDatabaseFormat'])
        result += f'Filename | {self.file_name}\n'
        result += f'Printed  |  {dt.datetime.now()}\n'
        return result
