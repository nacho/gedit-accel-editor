# -*- coding: utf-8 -*-

#  Copyright (C) 2011 - Ignacio Casal Quinteiro
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

from gi.repository import GObject, Gtk, Gedit
import re

from gettext import gettext as _

ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="EditShortcuts" action="EditShortcuts"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class AccelEditor(Gtk.Dialog, Gtk.Buildable):
    __gtype_name__ = "GeditAccelEditorDialog"

    ACTION_COLUMN = 0
    SHORTCUT_COLUMN = 1
    HEADER_COLUMN = 2

    def __init__(self):
        pass

    def do_parser_finished(self, builder):
        self.builder = builder

    def do_response(self, resp):
        self.destroy()

class AccelPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "AccelPlugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self.dlg = None

    def do_activate(self):
        manager = self.window.get_ui_manager()

        self._action_group = Gtk.ActionGroup('EditShortcutsPluginActions')
        self._action_group.add_actions([('EditShortcuts', None, 
                                         _('Edit Shortcuts'), None, 
                                         _('Edit keyboard shortcuts'),
                                         self._on_assign_accelerators)])

        manager.insert_action_group(self._action_group, -1)
        self._ui_id = manager.add_ui_from_string(ui_str)

    def do_deactivate(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()

    def update_status(self):
        pass

    def editor_destroyed(self, dlg):
        self.dlg = None

    def _on_assign_accelerators(self, action, data=None):
        if not self.dlg:
            builder = Gtk.Builder()
            #builder.add_from_file(os.path.join(self.plugin_info.get_data_dir(), 'ui', 'accelmap.ui'))
            builder.add_from_file('accelmap.ui')

            self.dlg = builder.get_object('accel_dialog')
            self.dlg.connect('destroy', self.editor_destroyed)

        self.dlg.set_transient_for(self.window)
        self.dlg.present()

# ex:ts=4:et:
