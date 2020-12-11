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
from bpy.types import (
    Panel,
    Curve,
    SurfaceCurve
)

from . import utils



class CUSTOM_UL_addon_list(bpy.types.UIList):
    EMPTY = 1 << 0

    use_filter_empty: bpy.props.BoolProperty(
        name="Filter Unused",
        default=True,
        options=set(),
        description="Whether to filter cameras with zero users",
    )
    use_filter_empty_reverse: bpy.props.BoolProperty(
        name="Reverse Empty",
        default=False,
        options=set(),
        description="Reverse empty filtering",
    )
    use_filter_name_reverse: bpy.props.BoolProperty(
        name="Reverse Name",
        default=False,
        options=set(),
        description="Reverse name filtering",
    )

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        active = True if index == getattr(active_data, active_propname) else False
        root = layout.row(align=True)
        root.label(text='', icon='FILE_SCRIPT')

        root.prop(item, "name", text='')
        root.prop(item, 'filter_mode', icon_only=True, expand=True)

    def draw_filter(self, context, layout):
        # Nothing much to say here, it's usual UI code...
        row = layout.row()
        row.alignment = 'RIGHT'
        # row.label(text="Filters, eventually")

    def filter_items(self, context, data, propname):

        items = getattr(data, propname)
        flt_flags = []
        flt_neworder = []

        helper_funcs = bpy.types.UI_UL_list


        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, items, "name",
                                                          reverse=self.use_filter_name_reverse)
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(items)

        # Filter by emptiness.
        # if self.use_filter_empty:
        #     for i, cam in enumerate(items):
        #         if cam.users < 1:
        #             flt_flags[i] |= ~self.EMPTY

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(items)

        return flt_flags, flt_neworder



class CUSTOM_UL_workspace_list(bpy.types.UIList):
    EMPTY = 1 << 0

    use_filter_empty: bpy.props.BoolProperty(
        name="Filter Unused",
        default=True,
        options=set(),
        description="Whether to filter cameras with zero users",
    )
    use_filter_empty_reverse: bpy.props.BoolProperty(
        name="Reverse Empty",
        default=False,
        options=set(),
        description="Reverse empty filtering",
    )
    use_filter_name_reverse: bpy.props.BoolProperty(
        name="Reverse Name",
        default=False,
        options=set(),
        description="Reverse name filtering",
    )

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        active = True if index == getattr(active_data, active_propname) else False

        indexed = True if item.name in getattr(active_data, "workspaces") else False

        root = layout.column(align=True)

        header = root.row(align=True)
        header.use_property_split = False
        header.label(text=item.name, icon='WORKSPACE')
        if not indexed:
            op = header.operator(
                "bam.create_filter",
                text="Create Filter",
            )
            op.workspace = item.name

    def draw_filter(self, context, layout):
        # Nothing much to say here, it's usual UI code...
        row = layout.row()
        row.alignment = 'RIGHT'
        # row.label(text="Filters, eventually")

    def filter_items(self, context, data, propname):

        workspaces = getattr(data, propname)
        flt_flags = []
        flt_neworder = []

        helper_funcs = bpy.types.UI_UL_list


        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, workspaces, "name",
                                                          reverse=self.use_filter_name_reverse)
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(workspaces)

        # Filter by emptiness.
        # if self.use_filter_empty:
        #     for i, cam in enumerate(workspaces):
        #         if cam.users < 1:
        #             flt_flags[i] |= ~self.EMPTY

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(workspaces)

        return flt_flags, flt_neworder


class BAM_PT_workspace_manager(Panel):
    bl_idname = "BAM_PT_workspace_manager"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "BAM"
    bl_label = "BAM Workspace Manager"
    bl_options = {'DRAW_BOX', 'HEADER_LAYOUT_EXPAND',  }
    bl_owner_use_filter = False

    def draw(self, context):
        wm = context.window_manager

        layout = self.layout
        root = layout.column(align=True)

        addons = bpy.context.preferences.addons
        prefs = addons["BlenderAddonManager"].preferences

        # root.label(text=str(prefs.wslist_index))

        # prefs = utils.get_prefs(context)

        root.template_list("CUSTOM_UL_workspace_list",      # the class that defines the filter functions and drawing
                           "",                              # No Clue 
                           context.blend_data,              # Where to get the data
                           "workspaces",                    # The data to get
                           prefs,                           # Where the index is
                           "wslist_index",                  # Index name
                           rows=1,
                           maxrows=4
                           )

        active_workspace = bpy.context.blend_data.workspaces[prefs.wslist_index]

        workspace_data = None
        for space in prefs.workspaces:
            if space.name == active_workspace.name:
                workspace_data = space
                break

        row = root.row(align=True)
        row.scale_y = 2
        row.label(text=active_workspace.name)

        # root.prop(
        #     active_workspace,
        #     "use_filter_by_owner"
        # )
        root.prop(
            active_workspace,
            "object_mode"
        )


        if workspace_data:
            root.prop(
                workspace_data,
                "fallback_mode"
            )

            row = root.row(align=True)
            row.template_list("CUSTOM_UL_addon_list",
                            "",
                            workspace_data,
                            "addons",
                            workspace_data,
                            "addon_index",
                            rows=1,
                            maxrows=4
                            )

            col = row.column(align=True)
            op = col.operator(
                "bam.modify_filter",
                text="",
                icon='ADD',
            )
            op.operation = 'ADD'
            op.workspace = workspace_data.name
            op.addon = 'Configure Me'

            active_addon = None
            if len(workspace_data.addons) > 0:
                active_addon = workspace_data.addons[workspace_data.addon_index]

                op = col.operator(
                    "bam.modify_filter",
                    text="",
                    icon='REMOVE',
                )
                op.operation = 'REMOVE'
                op.workspace = workspace_data.name
                op.addon = active_addon.name



        # body = root.split(factor=0.1, align=True)

        # body_left = body.row()

        # body_right = body.row()


        # body_right.label(text=str(active))
        # body_right.prop(
        #     item,
        #     "use_filter_by_owner",
        #     # text="",
        # )
        # body_right.prop(
        #     item,
        #     "object_mode",
        #     text="",
        # )
