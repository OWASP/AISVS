#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' AISVS document parser and converter class.

    Based upon code written for MAISVS By Bernhard Mueller
    Significant improvement by Jonny Schnittger @JonnySchnittger
    Additional modifications by Josh Grossman @tghosth
    Copyright (c) 2023 OWASP Foundation

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    '''

import os
import re
import json
from xml.sax.saxutils import escape
import csv
from dicttoxml2 import dicttoxml
import xml.etree.ElementTree as ET

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class AISVS:
    aisvs = {}
    aisvs['Name'] = "Artificial Intelligence Security Verification Standard Project"
    aisvs['ShortName'] = "AISVS"
    aisvs['Version'] = ""
    aisvs['Description'] = "The OWASP Artificial Intelligence Security Verification Standard (AISVS) Project " \
        "provides a basis for testing artificial intelligence technical security controls and also " \
        "provides developers with a list of requirements for secure development."

    aisvs_flat = {}
    aisvs_flat2 = {}
    aisvs_flat['requirements'] = []
    aisvs_flat2['requirements'] = []
    aisvs_raw = {}
    language = ''

    def __init__(self, language_in):    
        
        self.language = language_in
        prefix_char1, prefix_char2, prefix_char1_b = self.get_prefix()

        version_regex = re.compile('Version (([\d.]+){3})')
        
        for line in open(os.path.join(self.language, "0x01-Frontispiece.md"), encoding="utf8"):
            m = re.search(version_regex, line)
            if m:
                self.aisvs['Version'] = m.group(1)
                break

        about_regex = re.compile('## About the Standard\n\n(.*)')

        with open(os.path.join(self.language, "0x01-Frontispiece.md"), encoding="utf8") as content:
            m = re.search(about_regex, content.read())
            if m:
                self.aisvs['Description'] = m.group(1)

        self.aisvs['Requirements'] = chapters = []
        self.aisvs_raw['Chapters'] = chapters_raw = []

    
        for file in sorted(os.listdir(self.language)):

            if re.match("0x\d{2}-V", file):
                
                chapter = {}
                chapter_raw = {}
                chapter['Shortcode'] = ""
                chapter['Ordinal'] = ""
                chapter['ShortName'] = ""
                chapter['Name'] = ""
                chapter_raw['Filename'] = file
                chapter_raw['Name'] = ""
                chapter['Items'] = []

                section = {}
                section_raw = {}
                section['Shortcode'] = ""
                section['Ordinal'] = ""
                section['Name'] = ""
                section_raw['Name'] = ""
                section['Items'] = []

                # The filename_regex is used to match filenames that follow the pattern:
                # "0xNN-VNNN-Name", where NN is a two-digit number, VNNN is a chapter number, 
                # and Name is a string that does not contain a dot or hyphen.
                filename_regex = re.compile('0x\d{2}-(V([0-9]{1,3}))-(\w[^-.]*)')
                
                m = re.search(filename_regex, file)
                if m:
                    chapter = {}
                    chapter['Shortcode'] = m.group(1).replace('V', prefix_char1)
                    chapter['Ordinal'] = int(m.group(2))
                    chapter['ShortName'] = m.group(3)
                    chapter['Name'] = ""
                    chapter_raw['Name'] = ""
                    chapter['Items'] = []
                    chapter_raw['Lines'] = []
                    chapter_raw['Sections'] = []

                    '''
                    section = {}
                    section['Shortcode'] = m.group(1).replace('V', prefix_char1)
                    section['Ordinal'] = int(m.group(2))
                    section['Name'] = m.group(3)
                    print(m)
                    section['Items'] = []
                    '''
                    chapters.append(chapter)
                    chapters_raw.append(chapter_raw)

                # This regex matches lines that start with a hash (#) followed by a space,
                # prefix_char1 (usually 'V'), one or two digits, prefix_char1_b (which is usually empty)
                # another space, and then some sort of text
                chapter_heading_regex = re.compile("^#\s(" + prefix_char1 + "([0-9]{1,2})" + prefix_char1_b + ")\s([\w\s][^\n]*)")

                # section_regex matches section headings in the format "## VNN.NNN Name".
                section_regex = re.compile("## (" + prefix_char2 + "[0-9]{1,2}.([0-9]{1,3})) ([\w\s][^\n]*)")

                # This regex matches requirement lines with the format:
                # **number** | text | text | text | text | numbers, separated by commas | text, separated by slashes
                # req_regex = re.compile("\*\*([\d\.]+)\*\*\s\|\s{0,1}(.*?)\s{0,1}\|(.*?)\|"
                #                        "(.*?)\|(.*?)\|([0-9,\s]*)\|{0,1}([A-Z0-9/\s,.]*)\|{0,1}")

                req_regex = re.compile("\*\*([\d\.]+)\*\*\s\|\s{0,1}(.*?)\s{0,1}\|"
                                "([1-3 ]*?)\|([0-9,\s]*)\|{0,1}([A-Z0-9\s,.]*)\|{0,1}")

                before_reqs = True
                matched_already = False
                
                for line in open(os.path.join(self.language, file), encoding="utf8"):
                    matched_already = False
                    
                    m = re.search(chapter_heading_regex, line)
                    if m:
                        chapter['Name'] = m.group(3)
                        chapter_raw['Name'] = line
                        chapter_raw['Chapter'] = chapter
                        
                        matched_already = True
                    
                    m = re.search(section_regex, line)
                    if m:
                        section = {}
                        section_raw = {}
                        section['Shortcode'] = m.group(1)
                        section['Ordinal'] = int(m.group(2))

                        if self.language == 'ar':
                            section['Ordinal'] = int(m.group(1).split('.')[0].replace(prefix_char2, ''))

                        section['Name'] = m.group(3)
                        section_raw['Section'] = section
                        section_raw['Name']  = line
                        section['Items'] = []
                        section_raw['LinesBeforeReqs'] = []
                        section_raw['LinesAfterReqs'] = []
                        section_raw['Reqs'] = []
                        chapter['Items'].append(section)
                        chapter_raw['Sections'].append(section_raw)
                        before_reqs = True
                        has_cwe = True

                        matched_already = True

                    m = re.search(req_regex, line)
                    if m:
                        before_reqs = False
                        req_flat = {}
                        req_flat2 = {}
                        req_flat2['Section'] = req_flat['chapter_id'] = chapter['Shortcode']
                        req_flat2['Name'] = req_flat['chapter_name'] = chapter['Name']
                        req_flat['section_id'] = section['Shortcode']
                        req_flat['section_name'] = section['Name']
                        
                        req = {}
                        req_flat2['Item'] = req_flat['req_id'] = req['Shortcode'] = prefix_char2 + m.group(1)
                        req['Ordinal'] = int(m.group(1).rsplit('.',1)[1])
                        if self.language == 'ar':
                            req['Ordinal'] = int(m.group(1).split('.')[0])

                        req_flat2['Description'] = req_flat['req_description'] = req['Description'] = m.group(2)

                        level1 = {}
                        level2 = {}
                        level3 = {}

                        int_level = int(m.group(3)) if m.group(3) != ' ' else 99
                        
                        str_l1 = '✓' if int_level <= 1 else '' # m.group(3)
                        str_l2 = '✓' if int_level <= 2 else ''  # m.group(4)
                        str_l3 = '✓' if int_level <= 3 else ''  # m.group(5)


                        req_flat['level1'] = str_l1.strip(' ')
                        req_flat['level2'] = str_l2.strip(' ')
                        req_flat['level3'] = str_l3.strip(' ')
                        
                        level1['Required'] = str_l1.strip() != ''
                        req_flat2['L1'] = ('X' if level1['Required'] else '')
                        level2['Required'] = str_l2.strip() != ''
                        req_flat2['L2'] = ('X' if level2['Required'] else '')
                        level3['Required'] = str_l3.strip() != ''
                        req_flat2['L3'] = ('X' if level3['Required'] else '')

                        level1['Requirement'] = ("Optional" if str_l1.strip('✓ ') == "o" else str_l1.strip(' '))
                        level2['Requirement'] = ("Optional" if str_l2.strip('✓ ') == "o" else str_l2.strip(' '))
                        level3['Requirement'] = ("Optional" if str_l3.strip('✓ ') == "o" else str_l3.strip(' '))

                        req['L1'] = level1
                        req['L2'] = level2
                        req['L3'] = level3

                        req['CWE'] = [int(i.strip()) for i in filter(None, m.group(4).strip().split(','))]
                        req_flat2['CWE'] = req_flat['cwe'] = m.group(4).strip()
                        req['NIST'] = [str(i.strip()) for i in filter(None,m.group(5).strip().split('/'))]
                        req_flat2['NIST'] = req_flat['nist'] = m.group(5).strip()
                        
                        section['Items'].append(req)
                        self.aisvs_flat['requirements'].append(req_flat)
                        self.aisvs_flat2['requirements'].append(req_flat2)
                        req2 = req.copy()
                        req2['raw_text'] = line
                        req2['has_cwe'] = has_cwe
                        req2['DescriptionClean'] = req2['Description']
                        section_raw['Reqs'].append(req2)
                        matched_already = True

                    elif not matched_already:
                        if section['Ordinal']:
                            if before_reqs:
                                section_raw['LinesBeforeReqs'].append(line)
                                if '| # |' in line and '| CWE |' not in line:
                                    has_cwe = False
                            else:
                                section_raw['LinesAfterReqs'].append(line)
                        else:
                            chapter_raw['Lines'].append(line)






    def print_raw_requirement(self, req):
        ret_str = ''
        description = f'{req["DescriptionClean"]}'

           



        ret_str =  (f'| **{req["Shortcode"][1:]}** '
            f'| {description.strip()} '
            f'| {self.pad_if_set(req["L1"]["Requirement"])}'
            f'| {self.pad_if_set(req["L2"]["Requirement"])}'
            f'| {self.pad_if_set(req["L3"]["Requirement"])}|'
        )

        if req['has_cwe']:
            ret_str += f' {self.pad_if_set(" ".join(map(str, req["CWE"])))}|'
            
        return f'{ret_str}\n'
    
    def pad_if_set(self, string):
        if len(string) > 0:
            return string + ' '
        return string
    
    def get_prefix(self):
        prefix_char1 = prefix_char2 = 'V'
        prefix_char1_b = ''
        if self.language == 'ar':
            prefix_char1 = 'ت'
            prefix_char1_b = ':'
            prefix_char2 = 'ق'

        

        return prefix_char1, prefix_char2, prefix_char1_b

    def to_raw(self, output_folder):
        ''' Returns the raw data '''
        str_return = ''

        str_chapter = ''
        for chapter in self.aisvs_raw['Chapters']:
            #str_chapter = chapter['Name']
            str_chapter = f"# V{chapter['Chapter']['Ordinal']} {chapter['Chapter']['Name']}\n"
            for line in chapter['Lines']:
                str_chapter += line
            for section in chapter['Sections']:
                #str_chapter += section['Name']

                # This is a silly hack for the first section that was moved for V1
                if 'V1' in section['Name']:
                    str_chapter += section['Name']
                else:
                    str_chapter += f"## V{chapter['Chapter']['Ordinal']}.{section['Section']['Ordinal']} {section['Section']['Name']}\n"
                for line in section['LinesBeforeReqs']:
                    str_chapter += line
                for req in section['Reqs']:
                    #if len(req['raw_text']) != len(self.print_raw_requirement(req)):
                    #str_chapter += req['raw_text']
                    str_chapter += self.print_raw_requirement(req)
                for line in section['LinesAfterReqs']:
                    str_chapter += line
            
            if output_folder != '':
                with open(os.path.join(output_folder, chapter['Filename']), 'w', encoding='utf-8') as f:
                    f.write(str_chapter)
            else:
                str_return += str_chapter

        return str_return


    def to_json(self):
        ''' Returns a JSON-formatted string '''
        return json.dumps(self.aisvs, indent = 2, sort_keys = False, ensure_ascii=False).strip()
    
    def to_json_xl(self):
        ''' Returns a JSON-formatted string '''
        return json.dumps(self.aisvs_raw['Chapters'], indent = 2, sort_keys = False, ensure_ascii=False).strip()

    def to_json_flat(self):
        ''' Returns a JSON-formatted string which is flattened and simpler '''
        return json.dumps(self.aisvs_flat, indent = 2, sort_keys = False, ensure_ascii=False).strip()

    def to_xmlOLD(self):
        ''' Returns XML '''
        xml = ''

        for r in self.requirements:

            xml += "<requirement id = \"" + escape(r['id']) + "\">" + escape(r['text']) + "</requirement>\n"

        return xml
    def to_xml(self):
        ''' Returns XML '''
        return dicttoxml(self.aisvs, attr_type=False).decode('utf-8')

    def to_csv(self):
        ''' Returns CSV '''
        si = StringIO()

        writer = csv.DictWriter(si, ['chapter_id', 'chapter_name', 'section_id', 'section_name', 'req_id', 'req_description', 'level1', 'level2', 'level3', 'cwe', 'nist'])
        writer.writeheader()
        writer.writerows(self.aisvs_flat['requirements'])

        return si.getvalue()

    def dict_increment(self, dict_obj, dict_key):
        if dict_key not in dict_obj:
            dict_obj[dict_key] = 0
        
        dict_obj[dict_key] += 1

        return dict_obj
    
    def summary_total(self, summary):
        total = 0
        for chapter in summary:
            total += summary[chapter]
        
        return total

    def summary_string(self, format, summary):
        return f'Language: {self.language}. Format: {format}. Total: {self.summary_total(summary)}. Details: {summary}\n'


    def verify_csv(self, csv):
        
        prefix_char1, _, _ = self.get_prefix()

        summary = {}
        for line in csv.splitlines():
            if 'chapter_id,chapter_name' not in line:
                summary = self.dict_increment(summary, line.split(',')[0].replace(prefix_char1,''))

        return self.summary_string('csv', summary)

    def verify_json_flat(self, json_flat):
        prefix_char1, _, _ = self.get_prefix()
        data = json.loads(json_flat)
        summary = {}
        for req in data['requirements']:
            summary = self.dict_increment(summary, req['chapter_id'].replace(prefix_char1,''))

        return self.summary_string('json_flat', summary)

    def verify_json(self, json_reg):
        prefix_char1, _, _ = self.get_prefix()
        data = json.loads(json_reg)
        summary = {}
        for req in data['Requirements']:
            for ite1 in req['Items']:
                for _ in ite1['Items']:
                    summary = self.dict_increment(summary, req['Shortcode'].replace(prefix_char1,''))

        return self.summary_string('json', summary)


    def verify_xml(self, xml_string):
        prefix_char1, _, _ = self.get_prefix()
        data = ET.fromstring(xml_string)
        summary = {}
        scode = ''
        for req in data.iter():
            if req.tag == 'Requirements':
                for el_item in req:
                    for el_item_sub in el_item:
                        if el_item_sub.tag == 'Shortcode':
                            scode = el_item_sub.text
                        if el_item_sub.tag == 'Items':
                            for el_Items in el_item_sub:
                                for el_item2_sub in el_Items:
                                    if el_item2_sub.tag == 'Items':
                                        for _ in el_item2_sub:
                                            summary = self.dict_increment(summary, scode.replace(prefix_char1,''))
                    
        return self.summary_string('xml', summary)
