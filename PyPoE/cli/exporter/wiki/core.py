"""
Core Wiki Exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/core.py                                  |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Core Wiki Exporter

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.handler import BaseHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.parsers import WIKI_HANDLERS
from PyPoE.cli.exporter.wiki.admin import ADMIN_HANDLERS

# =============================================================================
# Globals
# =============================================================================

__all__ = ['WikiHandler']

# =============================================================================
# Classes
# =============================================================================


class WikiHandler(BaseHandler):
    def __init__(self, sub_parser):
        # Config Options
        config.add_option('temp_dir', 'is_directory(exists=True, make_absolute=True)')
        config.add_option('out_dir', 'is_directory(exists=True, make_absolute=True)')
        config.register_setup('temp_dir', self._setup)
        config.add_setup_variable('temp_dir', 'hash', 'string(default="")')
        config.add_setup_listener('version', self._ver_dist_changed)
        config.add_setup_listener('ggpk_path', self._ver_dist_changed)

        # Parser
        self.parser = sub_parser.add_parser('wiki', help='Wiki Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        wiki_sub = self.parser.add_subparsers()

        for handler in WIKI_HANDLERS:
            handler(wiki_sub)

        for handler in ADMIN_HANDLERS:
            handler(wiki_sub)

    def _ver_dist_changed(self, key, value, old_value):
        if value == old_value:
            return
        config.set_setup_variable('temp_dir', 'performed', False)
        console('Setup needs to be performed due to changes to "%s"' % key,
                msg=Msg.warning)

    def _setup(self, args):
        """
        :param args: argparse args passed on
        :return:
        """
        console('Done.')

