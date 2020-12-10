# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Hell is other peoples' code

import bpy
import addon_utils
import os
import rna_info
import inspect
import sys


### Basic Getters ###

def get_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_name():
    return os.path.basename(get_path())


def get_prefs(context):
    """A generic utility function that fetches the add-on's perferences"""
    addons = context.preferences.addons
    return bpy.context.preferences.addons[get_name()].preferences

### Add-on List Utilities ###

def build_addon_list(context):
    import sys
    addon_map = {mod.__name__: mod for mod in addon_utils.modules()}

    for addon in context.preferences.addons:
        mod = sys.modules.get(addon.module)
        classes = getattr(mod, "classes", "")
        # print(str(classes))

        # print(dir(addon))
        # print(str(addon.module))

        for modclass in classes:
            print(str(modclass))
            print(str(modclass.__class__))
            print(dir(modclass))
            print("\n\n")

        # for op in mod.operators:
        #     print(str(op))

    # for addon in context.preferences.addons:



        


### Keymap Utilities ###

def build_keymap_tree(context):
    """
    Creates an addon:keymap dictionary 
    so UI functions don't have to rebuild one 
    on each redraw.
    """
    addonmap = {}
    # structs, funcs, ops, props = rna_info.BuildRNAInfo()

    # for thing in props:
    #     print(str(thing))

    all_configs = []
    all_configs.append(context.window_manager.keyconfigs.addon)

    for config in all_configs:
        for keymap in config.keymaps:
            print(str(keymap.name))
            print(str(keymap.bl_owner_id))
            print("\n")
            owner_id = keymap.bl_owner_id



            # if owner_id == "mesh_f2":
            #     print("*****NERP")
            #     print(str(keymap))
            #     print("\n")

            #     for key in keymap.keymap_items:
            #         print(str(key.idname))
                
            #     print("\n")

            if not owner_id == "":
                if owner_id in addonmap:
                    addonmap[owner_id].append(keymap)
                    # print(str(addonmap[owner_id]))
                else:
                    addonmap[owner_id] = [keymap]
            else:
                print("NO OWNER")

    print("DONE\n")
    for key in addonmap:
        print(str(key))
        sublist = addonmap[key]
        for item in sublist:
            for key in item.keymap_items:
                print(str(key.idname))
        print("\n\n")



### Operator Stubs ###

class BAM_OT_EnhancedPie(bpy.types.Operator):
    """
    Operator base class for pie menus 
    that samples the cursor location on invoke.
    """

    def invoke(self, context, event):
        self.loc = (event.mouse_region_x, event.mouse_region_y)
        return self.execute(context)


### Property Groups ###
