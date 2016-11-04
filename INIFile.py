# The MIT License (MIT)
#
# Copyright (c) 2016 apalo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

class INIFile:
    """ Class used to create and manipulate ini-files """

    GLOBAL_SECTION = "__global__"
    setting_re = re.compile(r'^(\w+)([ \t]*=[ \t]*)([\w\.,]+|".*")$')
    section_re = re.compile(r"^\[([a-zA-Z0-9_\.]+)\]$")

    def __init__(self, file_str=None):
        """ Create new INIFile instance """
        self.sections = {}
        self.sections[INIFile.GLOBAL_SECTION] = {}
        if file_str != None:
            self.read(file_str)

    def read(self, file_str):
        """ Open existing ini-file """
        current = INIFile.GLOBAL_SECTION
        with open(file_str, "r") as f:
            for line in f:
                if line[-1] == '\n':
                    line = line[0:-1] # remove newline
                line = line.strip()   # remove space at start/end
                match = INIFile.setting_re.match(line)
                if match:
                    key = match.group(1)
                    val = match.group(3)
                    # add ini setting to current section
                    self.sections[current][key] = val
                    continue
                match = INIFile.section_re.match(line)
                if match:
                    current = match.group()
                    self.sections[current] = {} # add new ini section
                    continue

    def write(self, file_str):
        """ Write ini file to disk """
        with open(file_str, "w") as f:
            # write settings without section first
            g_settings = self.sections.pop(INIFile.GLOBAL_SECTION)
            for setting_name, setting in g_settings.items():
                f.write(setting_name + " = " + setting + '\n')
            # write all sections and ordinary settings
            for section_name, section in self.sections.items():
                f.write(section_name + '\n')
                for setting_name, setting in section.items():
                    f.write(setting_name + " = " + setting + '\n')
                f.write('\n')
            # return global settings to the sections dictionary
            self.sections[INIFile.GLOBAL_SECTION] = g_settings

    def set_value(self, section, setting_name, value):
        """ Add or change setting """
        if not INIFile.section_re.match(section):
            raise ValueError("Invalid section name")
        if not INIFile.setting_re.match(setting_name + " = " + value):
            raise ValueError("Invalid setting format")
        if section not in self.sections:
            self.sections[section] = {}
        self.sections[section][setting_name] = value

    def delete_section(self, section):
        """ Delete section if it exists """
        if INIFile.section_re.match(section):
            try:
                del self.sections[section]
            except:
                pass

    def delete_setting(self, section, setting):
        """ Delete setting if it exists """
        if INIFile.section_re.match(section):
            try:
                del self.sections[section][setting]
            except:
                pass

    def has_setting(self, section, setting):
        """ Check if setting exists in the ini-file """
        if section in self.sections:
            if setting in self.sections[section]:
                return True
        return False
                
if __name__ == "__main__":
    file1 = r"X:\path\to\test.ini"
    try:
        ini = INIFile(file1)
        print(ini.has_setting("[Section]", "SettingName"))
    except IOError:
        print("File error")
        
