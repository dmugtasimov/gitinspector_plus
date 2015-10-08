# coding: utf-8
#
# Copyright © 2012-2015 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from __future__ import unicode_literals
import localization
import version
import base64
import basedir
import os
import terminal
import textwrap
import time
import zipfile

__available_formats__ = ["html", "htmlembedded", "text", "xml"]

DEFAULT_FORMAT = __available_formats__[2]

__selected_format__ = DEFAULT_FORMAT

class InvalidFormatError(Exception):
    def __init__(self, msg):
        super(InvalidFormatError, self).__init__(msg)
        self.msg = msg

def select(format):
    global __selected_format__
    __selected_format__ = format

    return format in __available_formats__

def get_selected():
    return __selected_format__

def is_interactive_format():
    return __selected_format__ == "text"

def __output_html_template__(name):
    template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)
    file_r = open(template_path, "rb")
    return file_r.read().decode("utf-8", "replace")

def __get_zip_file_content__(name, file_name="/html/flot.zip"):
    zip_file = zipfile.ZipFile(basedir.get_basedir() + file_name, "r")
    content = zip_file.read(name)
    zip_file.close()
    return content.decode("utf-8", "replace")

def output_header():
    if __selected_format__ == "html" or __selected_format__ == "htmlembedded":
        base = basedir.get_basedir()
        html_header = __output_html_template__(base + "/html/html.header")
        tablesorter_js = __get_zip_file_content__("jquery.tablesorter.min.js",
                                                  "/html/jquery.tablesorter.min.js.zip").encode("latin-1", "replace")
        tablesorter_js = tablesorter_js.decode("utf-8", "ignore")
        flot_js = __get_zip_file_content__("jquery.flot.js")
        pie_js = __get_zip_file_content__("jquery.flot.pie.js")
        resize_js = __get_zip_file_content__("jquery.flot.resize.js")

        logo_file = open(base + "/html/gitinspector_piclet.png", "rb")
        logo = logo_file.read()
        logo_file.close()
        logo = base64.b64encode(logo)

        if __selected_format__ == "htmlembedded":
            jquery_js = ">" + __get_zip_file_content__("jquery.js")
        else:
            jquery_js = " src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js\">"

        print(html_header.format(title = _("Repository statistics for {0}").format(os.path.basename(basedir.get_basedir_git())),
                                 jquery = jquery_js,
                                 jquery_tablesorter = tablesorter_js,
                                 jquery_flot = flot_js,
                                 jquery_flot_pie = pie_js,
                                 jquery_flot_resize = resize_js,
                                 logo = logo.decode("utf-8", "replace"),
                                 logo_text = _("The output has been generated by {0} {1}. The statistical analysis tool"
                                               " for git repositories.").format(
                                   "<a href=\"https://github.com/ejwa/gitinspector\">gitinspector</a>",
                                               version.__version__),
                                 repo_text = _("Statistical information for the repository '{0}' was gathered on {1}.").format(
                                               os.path.basename(basedir. get_basedir_git()), localization.get_date()),
                                 show_minor_authors = _("Show minor authors"),
                                 hide_minor_authors = _("Hide minor authors"),
                                 show_minor_rows = _("Show rows with minor work"),
                                 hide_minor_rows = _("Hide rows with minor work")))
    elif __selected_format__ == "xml":
        print("<gitinspector>")
        print("\t<version>" + version.__version__ + "</version>")
        print("\t<repository>" + os.path.basename(basedir. get_basedir_git()) + "</repository>")
        print("\t<report-date>" + time.strftime("%Y/%m/%d") + "</report-date>")
    else:
        print(textwrap.fill(_("Statistical information for the repository '{0}' was gathered on {1}.").format(
              os.path.basename(basedir.get_basedir_git()), localization.get_date()), width=terminal.get_size()[0]))

def output_footer():
    if __selected_format__ == "html" or __selected_format__ == "htmlembedded":
        base = basedir.get_basedir()
        html_footer = __output_html_template__(base + "/html/html.footer")
        print(html_footer)
    elif __selected_format__ == "xml":
        print("</gitinspector>")
