#!/usr/bin/env python3

# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import os
import re
import sys

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))

from __pkginfo__ import __version__

# User-configurable lines
# End of user-configurable lines

github_username = "domdfcoding"
github_repository = "repo_helper"
github_url = f"https://github.com/{github_username}/{github_repository}"


rst_prolog = f""".. |pkgname| replace:: repo_helper
.. |pkgname2| replace:: ``repo_helper``
.. |browse_github| replace:: `Browse the GitHub Repository <{github_url}>`__
"""

author = "Dominic Davis-Foster"
project = "repo_helper"
slug = re.sub(r'\W+', '-', project.lower())
release = version = __version__
copyright = "2020 Dominic Davis-Foster"  # pylint: disable=redefined-builtin
language = 'en'
package_root = "repo_helper"

extensions = [
	'sphinx_toolbox',
	'sphinx_toolbox.more_autodoc',
	'sphinx_toolbox.more_autosummary',
	'sphinx_toolbox.tweaks.param_dash',
	'sphinx.ext.intersphinx',
	'sphinx.ext.mathjax',
	'sphinxcontrib.httpdomain',
	'sphinxcontrib.extras_require',
	'sphinx.ext.todo',
	'sphinxemoji.sphinxemoji',
	'notfound.extension',
	'sphinx_copybutton',
	'sphinxcontrib.default_values',
	'sphinxcontrib.toctree_plus',
	'seed_intersphinx_mapping',
	'autoconfig',
	]

sphinxemoji_style = 'twemoji'
todo_include_todos = bool(os.environ.get("SHOW_TODOS", 0))
gitstamp_fmt = "%d %b %Y"

templates_path = ['_templates']
html_static_path = ['_static']
source_suffix = '.rst'
exclude_patterns = []

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']
pygments_style = 'default'

intersphinx_mapping = {
		'python': ('https://docs.python.org/3/', None),
		'sphinx': ('https://www.sphinx-doc.org/en/stable/', None),
		'rtd': ('https://docs.readthedocs.io/en/latest/', None),
		"h5py": ('https://docs.h5py.org/en/latest/', None),
		"sarge": ('https://sarge.readthedocs.io/en/latest/', None),
		'jinja2': ('https://jinja.palletsprojects.com/en/2.11.x/', None),
		}

html_theme = 'repo_helper_sphinx_theme'
html_theme_options = {
		'page_width': '1200px',
		'logo_name': 'true',
		'github_user': 'domdfcoding',
		'github_repo': 'repo_helper',
		'description': 'Update multiple configuration files, build scripts etc. from a single location',
		'github_banner': 'true',
		'github_type': 'star',
		'badge_branch': 'master',
		'fixed_sidebar': 'true',
		}
html_theme_path = ["../.."]
html_show_sourcelink = True  # True will show link to source

html_context = {
		}

htmlhelp_basename = slug

latex_documents = [('index', f'{slug}.tex', project, author, 'manual')]
man_pages = [('index', slug, project, [author], 1)]
texinfo_documents = [('index', slug, project, author, slug, project, 'Miscellaneous')]

toctree_plus_types = {
		"class",
		"function",
		"method",
		"data",
		"enum",
		"flag",
		"confval",
		"directive",
		"role",
		"confval",
		"protocol",
		"typeddict",
		"namedtuple",
		}

add_module_names = False


autodoc_default_options = {
		'members': None,  # Include all members (methods).
		'special-members': None,
		"autosummary": None,
		"show-inheritance": None,
		'exclude-members': ','.join([   # Exclude "standard" methods.
				"__dict__",
				"__class__",
				"__dir__",
				"__weakref__",
				"__module__",
				"__annotations__",
				"__orig_bases__",
				"__parameters__",
				"__subclasshook__",
				"__init_subclass__",
				"__attrs_attrs__",
				"__init__",
				"__new__",
				"__getnewargs__",
				"__abstractmethods__",
				"__hash__",
				]),
		}
