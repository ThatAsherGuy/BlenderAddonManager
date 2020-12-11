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
import sys
from . import utils

class BAM_OT_BuildDictionary(bpy.types.Operator):
    bl_idname = 'bam.build_dict'
    bl_label = "Build Keymap Dictionary"
    bl_description = "Generates a dictionary of addon:keymap relationships"

    def invoke(self, context, event):
        print(str(self.__module__))
        print("\n")
        utils.build_keymap_tree(context)
        # utils.build_addon_list(context)
        return {'FINISHED'}


class BAM_OT_PrintModuleName(bpy.types.Operator):
    bl_idname = 'bam.print_mods'
    bl_label = "BAM PRINT MODS"
    bl_description = "Generates a dictionary of addon:keymap relationships"

    def invoke(self, context, event):
        utils.build_addon_list(context)
        # for addon in context.preferences.addons:
            # mod = sys.modules.get(addon.module)
            # print(str(mod.__name__))
            # print(str(mod.__package__))
            # print(dir(mod))
            # print("\n")
            
        return {'FINISHED'}

class BAM_OT_CreateWorkspaceFilter(bpy.types.Operator):
    bl_idname = 'bam.create_filter'
    bl_label = "BAM Create Workspace Filter"
    bl_description = "Creates a BAM filter set"

    workspace: bpy.props.StringProperty(name="Workspace Name")
    whitelist: bpy.props.BoolProperty(name="Whitelist", default=False)

    def invoke(self, context, event):
        addons = bpy.context.preferences.addons
        prefs = addons["BlenderAddonManager"].preferences

        new_filter = prefs.workspaces.add()
        new_filter.name = self.workspace

        return {'FINISHED'}

class BAM_OT_ModifyFilter(bpy.types.Operator):
    bl_idname = 'bam.modify_filter'
    bl_label = "BAM modify Workspace Filter"
    bl_description = "Modifies a BAM filter set"

    workspace: bpy.props.StringProperty(name="Workspace Name")
    addon: bpy.props.StringProperty(name="Add-on Name")

    op_items = [
        ("ADD", "Add", ""),
        ("REMOVE", "Remove", "")
    ]

    operation: bpy.props.EnumProperty(
        items=op_items,
        name="Operation"
    )

    def invoke(self, context, event):
        addons = bpy.context.preferences.addons
        prefs = addons["BlenderAddonManager"].preferences

        workspace_data = None
        for space in prefs.workspaces:
            if space.name == self.workspace:
                workspace_data = space
                break
        
        if workspace_data:
            target_addon = None
            for addon in workspace_data.addons:
                if addon.name == self.addon:
                    target_addon = addon
                    break

            if ((self.operation == 'ADD')):
                new_addon = workspace_data.addons.add()
                new_addon.name = self.addon
                return {'FINISHED'}

            if ((self.operation == 'REMOVE') and target_addon):
                index = workspace_data.addons.find(target_addon.name)
                workspace_data.addons.remove(index)
                return {'FINISHED'}

        return {'FINISHED'}

class BAM_OT_ApplyWorkspaceFilters(bpy.types.Operator):
    bl_idname = 'bam.apply_filters'
    bl_label = "BAM Apply Filters"
    bl_description = "Applies BAM filters to Workspaces"

    workspace: bpy.props.StringProperty(name="Workspace Name")
    whitelist: bpy.props.BoolProperty(name="Whitelist", default=False)

    def invoke(self, context, event):
        addons = bpy.context.preferences.addons
        addon_map = {addon_utils.module_bl_info(mod)["name"]: mod for mod in addon_utils.modules()}
        prefs = addons["BlenderAddonManager"].preferences

        for space in prefs.workspaces:
            do_fallback = True if not space.fallback_mode == 'NONE' else False
            workspace = bpy.context.blend_data.workspaces[space.name]
            owner_ids = {owner_id.name for owner_id in workspace.owner_ids}
            ignore = []

            if not workspace:
                continue

            if len(space.addons) > 0:
                workspace.use_filter_by_owner = True
                for addon in space.addons:

                    addon_module = addon_map.get(addon.name)

                    if not addon_module:
                        print(addon.name)
                        continue

                    if addon.filter_mode == 'INCLUDE':
                        bpy.ops.wm.owner_enable(
                            'INVOKE_DEFAULT',
                            False,
                            owner_id=addon_module.__name__
                        )
                        ignore.append(addon.name)
                    elif addon.filter_mode == 'EXCLUDE':
                        if addon_module.__name__ in owner_ids:
                            bpy.ops.wm.owner_disable(
                                'INVOKE_DEFAULT',
                                False,
                                owner_id=addon_module.__name__
                            )
                        ignore.append(addon.name)

                if do_fallback:
                    for addon in addons:

                        module = sys.modules.get(addon.module)
                        if not module.__addon_enabled__:
                            continue

                        key = addon_utils.module_bl_info(module)["name"]
                        if not key in ignore:
                            if space.fallback_mode == 'INCLUDE':
                                bpy.ops.wm.owner_enable(
                                    'INVOKE_DEFAULT',
                                    False,
                                    owner_id=module.__name__
                                )
                            else:
                                if addon.module in owner_ids:
                                    bpy.ops.wm.owner_disable(
                                        'INVOKE_DEFAULT',
                                        False,
                                        owner_id=module.__name__
                                    )

        return {'FINISHED'}


class BAM_OT_printstuff(bpy.types.Operator):
    bl_idname = 'bam.print'
    bl_label = "BAM PRINT"
    bl_description = "Applies BAM filters to Workspaces"


    def invoke(self, context, event):
        property_space = None
        for space in bpy.context.area.spaces:
            if space.type == 'PROPERTIES':
                property_space = space

        print(dir(property_space.context))
        property_space.context = 'SHADERFX'

        return {'FINISHED'}