import datetime as dt
import xlsxwriter
from xlsxwriter.utility import xl_range
import xml.etree.ElementTree as ElementTree


class PWSafeEntry:
    def __init__(self, entry):
        self.entry = entry
        self._group = ''
        self._groups = []
        self.title = ''
        self.username = ''
        self.password = ''
        self.note = ''
        self.email = ''
        self.url = ''
        for field in self.entry:
            key = str(field.tag)
            if key == 'group':
                self._group = field.text
                self._groups = self._group.split('.')
            elif key == 'title':
                self.title = field.text
            elif key == 'username':
                self.username = field.text
            elif key == 'password':
                self.password = field.text
            elif key == 'notes':
                self.note = field.text.replace('»',' >> ')
            elif key == 'email':
                self.email = field.text
            elif key == 'url':
                self.url = field.text
    @property
    def group(self):
        return self._group

    @property
    def groups(self):
        return self._groups

    @property
    def root_group(self):
        try:
            return self._groups[0]
        except:
            return ''

    @property
    def sub_group(self):
        try:
            return '.'.join(self._groups[1:])
        except:
            return 'Anonymous Sub Group'

    def __repr__(self):
        result = ''
        if self.group:
            result += f'## {self.group}\n'
        result += f'*{self.title}* Details\n'
        return result

    @property
    def header(self):
        result  = 'Title       | User       | Password       | Comment                          \n'
        result += '------------|------------|----------------|----------------------------------\n'
        return result

    @property
    def field_comment(self):
        comment = ''
        if self.email:
            comment += f'**Email:** {self.email} '
        if self.url:
            comment += f'**url:** {self.url} '
        if self.note:
            comment += f'**Note:** {self.note} '
        return comment

    @property
    def line(self):
        return f'{self.title}|{self.username}|{self.password}|{self.field_comment}\n'

    @property
    def header_list(self):
        return(['Title', 'User', 'Password', 'Comment'])

    @property
    def data_list(self):
        return([f'{self.title}', f'{self.username}',
                f'{self.password}', f'{self.field_comment}'])

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
                        result += f'\n\n## {e.group}\n'
                    else:
                        result += f'\n\n## Passwords with no group\n'
                    result += e.header
                    group = e.group
                result += e.line
            elif str(entry.tag) == 'Preferences':
                pass
            else:
                result += f'\n### Unknown tag &rarr; {entry.tag}\n'
        result += '\n### *File data*\n'
        result += 'Field | Value\n'
        result += '------|------\n'
        # TODO Problem with Pandoc conversion of Windows path names
        # result += 'Database | {}\n'.format(root.attrib['Database'])
        result += 'WhenLastSaved |  {}\n'.format(root.attrib['WhenLastSaved'])
        result += 'WhoSaved |  {}\n'.format(root.attrib['WhoSaved'])
        result += 'FromDatabaseFormat |  {}\n'.format(root.attrib['FromDatabaseFormat'])
        result += f'Filename | {self.file_name}\n'
        result += f'Printed  |  {dt.datetime.now()}\n'
        return result

    def set_formats(self):
        """AT teh beginging of creating a spreadsheet set up all the formats to be used."""
        self.format_title = self.workbook.add_format({
            'bold': True,
            'font_size': 18,
            'text_wrap': True,
            'valign': 'top',
            'align': 'center',
            'fg_color': '#D7E4BC',
            'border': 0})
        self.format_header = self.workbook.add_format({
            'bold': True,
            'font_size': 14,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#C0C0D0',
            'border': 0})
        self.format_group_header = self.workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#C0C080',
            'border': 1})
        self.format_table_header_cell = self.workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'border': 1})
        self.format_table_cell = self.workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'border': 1})


    def write_main_header(self, message):
        """This is used only for the major heading of whole document"""
        self.worksheet.merge_range(xl_range(self.line, 0, self.line, 9),
                                   message, self.format_title)
        self.line += 1

    def write_group(self, message):
        """This is used only for the chnages of a group, the group_root"""
        self.worksheet.merge_range(xl_range(self.line + 1, 0, self.line + 1, 9),
                                   message, self.format_header)
        self.line += 2

    def write_group_header(self, entry):
        """This is used for sub groups headings which are then overwritten"""
        self.worksheet.merge_range(xl_range(self.line, min(5, self.group_level - 1),
                                            self.line, 6),
                                   entry.sub_group, self.format_group_header)
        self.line += 1

    def write_table_header(self, entry):
        for i, field in enumerate(entry.header_list):
            if i == 0:
                self.worksheet.merge_range(xl_range(self.line, min(5,self.group_level),
                                                    self.line, 6),
                                           field, self.format_table_header_cell)
            else:
                self.worksheet.write(self.line, i+6, field, self.format_table_header_cell)
        self.line += 1

    def write_table_data(self, entry):
        for i, field in enumerate(entry.data_list):
            if i == 0:
                self.worksheet.merge_range(xl_range(self.line, min(5,self.group_level),
                                                    self.line, 6),
                                           field, self.format_table_cell)
            else:
                self.worksheet.write(self.line, i+6, field, self.format_table_cell)
        self.line += 1

    def load_to_excel(self):
        """The format of the Excel sheet is that first 6 columns are used for indenting. to indicate
        group hierachy, no more than 6 levels of hierachary are support  grpahically."""
        self.set_formats()
        self.worksheet.set_landscape()
        self.worksheet.set_paper(9)  # A4
        # Set width of columns
        self.worksheet.set_column(0, 5, 1)
        self.worksheet.set_column(6, 6, 17)
        self.worksheet.set_column(7, 8, 23)
        self.worksheet.set_column(9, 9, 54)  # Width of columns B:D set to 30.
        root = self.tree.getroot()
        self.line=0
        # Add a bold format to use to highlight cells.
        self.write_main_header('Password File')
        group = None
        groups = None
        self.group_level = 0
        for entry in root:
            if str(entry.tag) == 'entry':
                e = PWSafeEntry(entry)
                if e.root_group != group:
                    if e.root_group:
                        self.write_group(f'{e.root_group}')
                    else:
                        self.write_group('Passwords with no group')
                    self.write_table_header(e)
                    group = e.root_group
                if e.groups != groups:
                    self.group_level = max(0, len(e.groups) - 1)
                    if e.sub_group:
                        self.write_group_header(e)
                    groups = e.groups
                self.write_table_data(e)
            elif str(entry.tag) == 'Preferences':
                pass
            else:
                # result += f'\n### Unknown tag &rarr; {entry.tag}\n'
                pass
        # result += '\n### *File data*\n'
        # result += 'Field | Value\n'
        # result += '------|------\n'
        # TODO Problem with Pandoc conversion of Windows path names
        # result += 'Database | {}\n'.format(root.attrib['Database'])
        # result += 'WhenLastSaved |  {}\n'.format(root.attrib['WhenLastSaved'])
        # result += 'WhoSaved |  {}\n'.format(root.attrib['WhoSaved'])
        # result += 'FromDatabaseFormat |  {}\n'.format(root.attrib['FromDatabaseFormat'])
        # result += f'Filename | {self.file_name}\n'
        #esult += f'Printed  |  {dt.datetime.now()}\n'

    def to_excel(self, filename):

        self.workbook = xlsxwriter.Workbook(filename)
        try:
            self.worksheet = self.workbook.add_worksheet()
            self.load_to_excel()
        finally:
            self.workbook.close()