#!/usr/bin/env python
# encoding: utf-8

"""
Transform a YAML file into a LaTeX Beamer presentation.

Copyright (C) 2009 Arthur Koziel <arthur@arthurkoziel.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '1.2'
__author__ = 'Arthur Koziel <arthur@arthurkoziel.com>'
__url__ = 'http://code.google.com/p/yml2tex/'

import os
import optparse
import sys

import yaml
from loader import PairLoader

parser = optparse.OptionParser(
    usage="usage: %prog source_file [options]",
    version=__version__,
)

def section(title):
    """
    Given the section title, return its corresponding LaTeX command.
    """
    return '\n\n\section{%s}' % _escape_output(title)

def subsection(title):
    """
    Given the subsection title, return its corresponding LaTeX command.
    """
    return '\n\subsection{%s}' % _escape_output(title)

def frame(title, items):
    """
    Given the frame title and corresponding items, delegate to the appropriate 
    function and returns its LaTeX commands.
    """
    if title.startswith('include'):
        out = code(title)
    elif title.startswith('image'):
        out = image(title, items)
    else:
        out = "\n\\frame {"
        out += "\n\t\\frametitle{%s}" % _escape_output(title)
        out += itemize(items)
        out += "\n}"
    return out

def _escape_output(text):
    """Escape special characters in Latex"""
    dic = {'&': '\&', 
           '$': '\$', 
           '%': '\%', 
           '#': '\#', 
           '_': '\_', 
           '{': '\{', 
           '}': '\}'}
    
    for i, j in dic.iteritems():  
        text = text.replace(i, j)
    return text

def itemize(items):
    """
    Given the items for a frame, returns the LaTeX syntax for an itemized list.
    If an item itself is a list, a nested itemized list will be created.
    
    The script itself doesn't limit the depth of nested lists. LaTeX Beamer 
    limits lists to be nested up to a depth of 3.
    """
    out = "\n\t\\begin{itemize}[<+-| alert@+>]"
    for item in items:
        if isinstance(item, list):
            for i in item:
                out += "\n\t\\item %s" % _escape_output(item[0][0])
                out += itemize(item[0][1])
        else:
            out += "\n\t\\item %s" % _escape_output(item)
    out += "\n\t\end{itemize}"
    return out

def code(title):
    """
    Return syntax highlighted LaTeX.
    """
    filename = title.split(' ')[1]
    
    # open the code file relative from the yml file path
    f = open(os.path.join(os.path.dirname(os.path.abspath(source_file)), filename))
    
    out = "\n\\begin{frame}[fragile,t]"
    out += "\n\t\\frametitle{Code: \"%s\"}" % filename
    
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
        from pygments.formatters import LatexFormatter
        
        try:
            lexer = get_lexer_for_filename(filename)
        except:
            lexer = get_lexer_by_name('text')
        out += "\n%s\n" % highlight(f.read(), lexer, LatexFormatter(linenos=True))
    except ImportError:
        out += "\n\t\\begin{lstlisting}\n"
        out += f.read()
        out += "\n\t\end{lstlisting}"
        
    f.close()
    out += "\n\end{frame}"
    return out

def image(title, options):
    """
    Given a frame title, which starts with "image" and is followed by the image 
    path, return the LaTeX command to include the image.
    """
    if not options:
        options = ""
    options = ",".join(["%s=%s" % (k, v) for k, v in dict(options).items()])
    
    out = "\n\\frame[shrink] {"
    out += "\n\t\\pgfimage[%s]{%s}" % (options, title.split(' ')[1])
    out += "\n}"
    return out

def header(metas):
    """
    Return the LaTeX Beamer document header declarations.
    """

    out = "\documentclass[slidestop,red]{beamer}"
    out += "\n\usepackage[utf8]{inputenc}"
    if metas.get('tex_babel'):
        out += "\n\usepackage[%s]{babel}" % metas['tex_babel']
    if metas.get('tex_fontenc'):
        out += "\n\usepackage[%s]{fontenc}" % metas['tex_fontenc']
    out += "\n\usepackage{fancyvrb,color}\n\n"
    
    # generate style definitions for pygments syntax highlighting
    try:
        from pygments.formatters import LatexFormatter
        out += LatexFormatter(style=metas.get('highlight_style', 'default')).get_style_defs()
    except ImportError:
        out += "\usepackage{listings}\n"
        out += "\lstset{numbers=left}"

    out += "\n\n\usetheme{Antibes}"
    out += "\n\setbeamertemplate{footline}[frame number]"
    out += "\n\usecolortheme{lily}"
    out += "\n\\beamertemplateshadingbackground{blue!5}{yellow!10}"
    
    if metas.has_key('short_title'):
        short_title = "[%s]" % metas.get('short_title')
    else:
        short_title = ""
    out += "\n\n\\title%s{%s}" % (short_title, metas.get('title', 'Example Presentation'))
    out += "\n\\author{%s}" % metas.get('author', 'Arthur Koziel')
    out += "\n\\institute{%s}" % metas.get('institute', '')
    out += "\n\date{%s}" % metas.get('date', '\\today')
    out += "\n\n\\begin{document}"
    out += "\n\n\\frame{\\titlepage}"
    
    if metas.get('outline', True):
        out += "\n\n\section*{%s}" % metas.get('outline_name', 'Outline')
        out += "\n\\frame {"
        out += "\n\t\\frametitle{%s}" % metas.get('outline_name', 'Outline')
        out += "\n\t\\tableofcontents"
        out += "\n}"

        out += "\n\n\AtBeginSection[] {"
        out += "\n\t\\frame{"
        out += "\n\t\t\\frametitle{%s}" % metas.get('outline_name', 'Outline')
        out += "\n\t\t\\tableofcontents[currentsection]"
        out += "\n\t}"
        out += "\n}"
    return out

def footer():
    """
    Return the LaTeX Beamer document footer.
    """
    out = "\n\end{document}"
    return out
    
def main():
    """
    Return the final LaTeX presentation after invoking all necessary functions.
    """
    options, args = parser.parse_args(sys.argv[1:])
    if not args:
        parser.print_help()
        sys.exit(1)
    try:
        global source_file
        source_file = args[0]
        doc = yaml.load(open(source_file), Loader=PairLoader)
    except IOError:
        parser.error("file does not exist")
        sys.exit(1)

    # yaml file is empty
    if not doc:
        sys.exit(1)
    
    metas = {}
    if doc[0][0] == 'metas':
        metas = dict(doc[0][1])
        del doc[0]

    out = header(metas)
    for sections, doc in doc:
        out += section(sections)
        for subsections, doc in doc:
            out += subsection(subsections)
            for frames, items in doc:
                out += frame(frames, items)
    out += footer()
    return out.encode('utf-8')

if __name__ == '__main__':
    print main()
