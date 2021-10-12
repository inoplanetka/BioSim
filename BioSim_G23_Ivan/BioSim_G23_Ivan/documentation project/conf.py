
import os
import sys

sys.path.append(os.path.abspath('/Users/IvanCherednikov/Desktop/INF200\ Project/BioSim_G23_Peter_Ivan/BioSim_G23_Peter_Ivan/documentation\ project'))


project = u'Modelling the Ecosystem of Rossumøya'
copyright = u'2020, Ivan Cherednikov'
author = u'Ivan Cherednikov'


# -- basic configurations ---------------------------------------------------------------------------------------

source_suffix = ['.rst']

master_doc = 'index'

exclude_patterns = ['_build']


templates_path = ['_templates']


extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.imgmath']

todo_include_todos = True

pygments_style = 'native'

autoclass_content = "both"
autodoc_member_order = 'bysource'  #
autodoc_default_flags = ['members']


imgmath_latex_preamble = r'''
\usepackage{xcolor}
\definecolor{offwhite}{rgb}{238,238,238}
\everymath{\color{offwhite}}
\everydisplay{\color{offwhite}}
'''

html_theme = 'graphite'

html_theme_path = ['.']


html_static_path = ['_static']


html_logo = '_static/rossum.png'


html_sidebars = {
    '**': [
        'globaltoc.html',
        'searchbox.html'
    ]
}
