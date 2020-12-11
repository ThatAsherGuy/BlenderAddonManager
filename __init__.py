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
import os

from .operators import BAM_OT_BuildDictionary
from .operators import BAM_OT_PrintModuleName
from .operators import BAM_OT_CreateWorkspaceFilter
from .operators import BAM_OT_ModifyFilter
from .operators import BAM_OT_ApplyWorkspaceFilters
from .operators import BAM_OT_printstuff

from .ui import BAM_PT_workspace_manager
from .ui import CUSTOM_UL_workspace_list
from .ui import CUSTOM_UL_addon_list

classes = (
    # Operators
    BAM_OT_BuildDictionary,
    BAM_OT_PrintModuleName,
    BAM_OT_CreateWorkspaceFilter,
    BAM_OT_ModifyFilter,
    BAM_OT_ApplyWorkspaceFilters,
    BAM_OT_printstuff,
    # UI
    CUSTOM_UL_workspace_list,
    CUSTOM_UL_addon_list,
    BAM_PT_workspace_manager,
)

bl_info = {
    "name" : "BlenderAddonManager",
    "author" : "That Asher Guy",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class BAMAddonData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Addon Name", default="Undefined")

    filter_items = [
        ("NOT", "Unfiltered", "Not filtered", 'REMOVE', 1),
        ("INCLUDE", "Whitelisted", "Included in Workspace", 'CHECKMARK', 2),
        ("EXCLUDE", "Blacklisted", "Excluded from Workspace", 'X', 3),
    ]
    filter_mode: bpy.props.EnumProperty(
        items = filter_items,
        name="Filter Mode",
        default='NOT',
        )


class BAMWorkspaceData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Workspace Name", default="Undefined")
    addons: bpy.props.CollectionProperty(
        type=BAMAddonData,
        name="Tracked Addons"
    )
    addon_index: bpy.props.IntProperty(
        name="Add-on Index",
        default=0,
    )


class BAMPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    workspaces: bpy.props.CollectionProperty(
        type=BAMWorkspaceData,
        name="Tracked Workspaces"
    )
    wslist_index: bpy.props.IntProperty(
        name="Workspace Index",
        default=0,
    )

properties = (
    BAMAddonData,
    BAMWorkspaceData,
    BAMPreferences,
)


def evil():
    victim = bpy.types.SpaceProperties


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for prop in properties:
        bpy.utils.register_class(prop)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for prop in properties:
        bpy.utils.unregister_class(prop)
