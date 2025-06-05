#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' CycloneDX converter class

    Converts the AISVS JSON into CycloneDX Standards format
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

import json
from dicttoxml2 import dicttoxml
import datetime
import uuid
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class CycloneDX:
    bom = {}
    bom['bomFormat'] = "CycloneDX"
    bom['specVersion'] = "1.6"
    bom['serialNumber'] = "urn:uuid:" + str(uuid.uuid4())
    bom['version'] = 1
    bom['metadata'] = {}
    bom['metadata']['timestamp'] = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    bom['metadata']['licenses'] = []
    bom['metadata']['licenses'].append({})
    bom['metadata']['licenses'][0]['license'] = {}
    bom['metadata']['licenses'][0]['license']['id'] = "CC-BY-SA-4.0"
    bom['metadata']['licenses'][0]['license']['url'] = "https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt"
    bom['metadata']['supplier'] = {}
    bom['metadata']['supplier']['name'] = "OWASP Foundation"
    bom['metadata']['supplier']['url'] = [ "https://owasp.org" ]
    bom['declarations'] = {}
    bom['declarations']['standards'] = []
    bom['declarations']['standards'].append({})

    def __init__(self, aisvs_json_in):
        self.aisvs = aisvs_json_in
        aisvs = json.loads(aisvs_json_in)
        bom_ref = aisvs["ShortName"] + "-" + aisvs["Version"]
        self.bom['declarations']['standards'][0]['bom-ref'] = bom_ref
        self.bom['declarations']['standards'][0]['name'] = \
            aisvs["Name"].replace('Project', '') + "(" + aisvs["ShortName"] + ")"
        self.bom['declarations']['standards'][0]['version'] = aisvs["Version"]
        self.bom['declarations']['standards'][0]['description'] = aisvs["Description"]
        self.bom['declarations']['standards'][0]['owner'] = aisvs["Name"]

        requirements = []
        l1_requirements = []
        l2_requirements = []
        l3_requirements = []
        for aisvs_chapter in aisvs['Requirements']:
            chapter_req = self.convert_requirement(aisvs_chapter, None)
            requirements.append(chapter_req)
            if 'Items' in aisvs_chapter:
                for aisvs_section in aisvs_chapter['Items']:
                    section_req = self.convert_requirement(aisvs_section, chapter_req['bom-ref'])
                    requirements.append(section_req)
                    for aisvs_requirement in aisvs_section['Items']:
                        requirement = self.convert_requirement(aisvs_requirement, section_req['bom-ref'])
                        requirements.append(requirement)
                        if 'L1' in aisvs_requirement and 'Required' in aisvs_requirement['L1'] and aisvs_requirement['L1']['Required'] is True:
                            l1_requirements.append(requirement['bom-ref'])
                        if 'L2' in aisvs_requirement and 'Required' in aisvs_requirement['L2'] and aisvs_requirement['L2']['Required'] is True:
                            l2_requirements.append(requirement['bom-ref'])
                        if 'L3' in aisvs_requirement and 'Required' in aisvs_requirement['L3'] and aisvs_requirement['L3']['Required'] is True:
                            l3_requirements.append(requirement['bom-ref'])

        self.bom['declarations']['standards'][0]['requirements'] = requirements

        self.bom['declarations']['standards'][0]['levels'] = []
        self.bom['declarations']['standards'][0]['levels'].append({})
        self.bom['declarations']['standards'][0]['levels'][0] = {}
        self.bom['declarations']['standards'][0]['levels'][0]['bom-ref'] = "level-1"
        self.bom['declarations']['standards'][0]['levels'][0]['identifier'] = "Level 1"
        self.bom['declarations']['standards'][0]['levels'][0]['description'] = "This level contains the minimum requirements to consider when securing an application and represents a critical starting point."
        self.bom['declarations']['standards'][0]['levels'][0]['requirements'] = l1_requirements
        self.bom['declarations']['standards'][0]['levels'].append({})
        self.bom['declarations']['standards'][0]['levels'][1] = {}
        self.bom['declarations']['standards'][0]['levels'][1]['bom-ref'] = "level-2"
        self.bom['declarations']['standards'][0]['levels'][1]['identifier'] = "Level 2"
        self.bom['declarations']['standards'][0]['levels'][1]['description'] = "AISVS Level 2 requirements generally relate to either less common attacks or more complicated protections against common attacks. They may still be a first layer of defense, or they may require certain preconditions for the attack to be successful."
        self.bom['declarations']['standards'][0]['levels'][1]['requirements'] = l2_requirements
        self.bom['declarations']['standards'][0]['levels'].append({})
        self.bom['declarations']['standards'][0]['levels'][2] = {}
        self.bom['declarations']['standards'][0]['levels'][2]['bom-ref'] = "level-3"
        self.bom['declarations']['standards'][0]['levels'][2]['identifier'] = "Level 3"
        self.bom['declarations']['standards'][0]['levels'][2]['description'] = "AISVS Level 3 should be the goal for applications looking to demonstrate the highest levels of security and requirements in this section are generally either defense-in-depth mechanisms or other useful but hard-to-implement controls."
        self.bom['declarations']['standards'][0]['levels'][2]['requirements'] = l3_requirements

        self.bom['declarations']['standards'][0]['externalReferences'] = []
        self.bom['declarations']['standards'][0]['externalReferences'].append({})
        self.bom['declarations']['standards'][0]['externalReferences'][0]['type'] = 'website'
        self.bom['declarations']['standards'][0]['externalReferences'][0]['url'] = 'https://owasp.org/aisvs'
        self.bom['declarations']['standards'][0]['externalReferences'].append({})
        self.bom['declarations']['standards'][0]['externalReferences'][1]['type'] = 'vcs'
        self.bom['declarations']['standards'][0]['externalReferences'][1]['url'] = 'https://github.com/OWASP/AISVS'
        self.bom['declarations']['standards'][0]['externalReferences'].append({})
        self.bom['declarations']['standards'][0]['externalReferences'][2]['type'] = 'issue-tracker'
        self.bom['declarations']['standards'][0]['externalReferences'][2]['url'] = 'https://github.com/OWASP/AISVS/issues'
        self.bom['declarations']['standards'][0]['externalReferences'].append({})
        self.bom['declarations']['standards'][0]['externalReferences'][3]['type'] = 'social'
        self.bom['declarations']['standards'][0]['externalReferences'][3]['url'] = 'https://twitter.com/OWASP_AISVS'

    def convert_requirement(self, aisvs_requirement, parent):
        requirement = {}
        requirement['bom-ref'] = aisvs_requirement['Shortcode']
        requirement['identifier'] = aisvs_requirement['Shortcode']
        if 'ShortName' in aisvs_requirement and aisvs_requirement['ShortName'] != '':
            requirement['title'] = aisvs_requirement['ShortName']
        if 'Name' in aisvs_requirement and aisvs_requirement['Name'] != '':
            requirement['title'] = aisvs_requirement['Name']
        if 'Description' in aisvs_requirement and aisvs_requirement['Description'] != '':
            requirement['text'] = aisvs_requirement['Description']
        if parent:
            requirement['parent'] = parent
        return requirement

    def to_json(self):
        ''' Returns a JSON-formatted string '''
        return json.dumps(self.bom, indent = 2, sort_keys = False, ensure_ascii=False).strip()
