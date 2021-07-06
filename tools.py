#----------------------------------------------------------
# File tools.py
#----------------------------------------------------------
#
# Tools - Copyright (C) 2018 Ajit Christopher D'Monte
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------

import bpy
import math

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

# Properties of the main part of the panel
# ----------------------------------------------------------

class fBlahToolsUISettings(PropertyGroup):
    """Armature Selection Box"""
    src_armature : PointerProperty(
        type=bpy.types.Armature, 
        name="Source Armature", 
        description="Select a source Armature", 
        options={'ANIMATABLE'}, 
        update=None
        )

# Helper function to check if a valid selection is made
# ----------------------------------------------------------

def is_armature_selected():
    """Checks if selected source armature is valid"""
    fbt = bpy.context.scene.fBlahToolsSettings
    if(fbt.src_armature):
        return True
    else:
        return False

# Helper function to get parent of armature
# ----------------------------------------------------------
def get_parent_armature(armature):
        for ob in bpy.data.objects:
            if (ob.data) == armature:
                return ob
        return None

# Get axis angle rotations of bones in clipboard Button (Operator)
# ----------------------------------------------------------

class GetBoneAxisAngleRotationsOperator(bpy.types.Operator):
    """Copies bone axis angle rotations to clipboard"""
    bl_idname = "fblah.getbonesaxisanglerot"
    bl_label = "Copy bone rotations"
    bl_description = 'Copies bone axis angle rotations to clipboard'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL','UNDO'}

    
    @classmethod
    def poll(cls, context):
        return is_armature_selected()

    def execute(self, context):
        result = False
        fbt = context.scene.fBlahToolsSettings
        arm = get_parent_armature(fbt.src_armature)
        if(arm):
            output = ""
            for bone in arm.pose.bones:                
                output += str(math.degrees(bone.rotation_axis_angle[0])) + "," + str(bone.rotation_axis_angle[1]) + "," + str(bone.rotation_axis_angle[2]) + "," + str(bone.rotation_axis_angle[3]) + "\n"
            bpy.context.window_manager.clipboard = output
            self.report({'INFO'}, "Copied to clipboard")
        else:
            self.report({'ERROR'},"Invalid Armature")            
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout

# Get axis angle rotations of bones in clipboard Button (Operator)
# ----------------------------------------------------------

class GetInvertedBoneAxisAngleRotationsOperator(bpy.types.Operator):
    """Copies inverted bone axis angle rotations to clipboard"""
    bl_idname = "fblah.getinvertedbonesaxisanglerot"
    bl_label = "Copy Inverted bone rotations"
    bl_description = 'Copies inverted bone axis angle rotations to clipboard'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL','UNDO'}
    
    @classmethod
    def poll(cls, context):
        return is_armature_selected()

    def execute(self, context):
        result = False
        fbt = context.scene.fBlahToolsSettings
        arm = get_parent_armature(fbt.src_armature)
        if(arm):
            output = ""
            for bone in arm.pose.bones:
                angle = math.degrees(bone.rotation_axis_angle[0])
                if(angle == 0.0):
                    output += str(angle)
                elif(angle < 0.0):
                    output += str(angle*-1.0)
                else:
                    output += "-" + str(angle)
                output +="," + str(bone.rotation_axis_angle[1]) + "," + str(bone.rotation_axis_angle[2]) + "," + str(bone.rotation_axis_angle[3]) + "\n"
            bpy.context.window_manager.clipboard = output
            self.report({'INFO'}, "Copied to clipboard")
        else:
            self.report({'ERROR'},"Invalid Armature")            
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout

# Set axis angle rotations of bones from clipboard Button (Operator)
# ----------------------------------------------------------

class SetBoneAxisAngleRotationsOperator(bpy.types.Operator):
    """Sets bone axis angle rotations from clipboard"""
    bl_idname = "fblah.setbonesaxisanglerot"
    bl_label = "Set bone rotations"
    bl_description = 'Sets bone axis angle rotations from clipboard'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL','UNDO'}
    
    @classmethod
    def poll(cls, context):
        return is_armature_selected()

    def execute(self, context):
        result = False
        fbt = context.scene.fBlahToolsSettings
        arm = get_parent_armature(fbt.src_armature)
        bpy.context.window_manager.clipboard
        if(arm):
            if((len(bpy.context.window_manager.clipboard.split("\n")) - 1) == len(arm.pose.bones)):
                i = 0
                rotations = bpy.context.window_manager.clipboard.split("\n")
                for bone in arm.pose.bones:
                    rot = rotations[i].split(",") 
                    i = i + 1
                    if(len(rot) == 4):
                        bone.rotation_axis_angle[0] = math.radians(float(rot[0]))
                        bone.rotation_axis_angle[1] = float(rot[1])
                        bone.rotation_axis_angle[2] = float(rot[2])
                        bone.rotation_axis_angle[3] = float(rot[3])
                    else:                        
                        self.report({'ERROR'},"Invalid rotations in clipboard")
                        break                
                self.report({'INFO'}, "Copied From clipboard")
            else:
                self.report({'ERROR'},"Invalid number of bones in clipboard")
        else:
            self.report({'ERROR'},"Invalid Armature")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout

# Main addon panel (Panel)
# ----------------------------------------------------------
class VIEW3D_PT_tools_fBlah(bpy.types.Panel):
    """fBlah's Tools Panel layout"""
    bl_label = "fBlah's Tools"
    bl_idname = "fblah.tools_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_category = "Tools"    

    @classmethod
    def poll(self,context):        
        return context.object is not None

    def draw(self, context):
        layout = self.layout 
        
        fbt = context.scene.fBlahToolsSettings

        icon_expand = "DISCLOSURE_TRI_RIGHT"
        icon_collapse = "DISCLOSURE_TRI_DOWN"
    
        if(not is_armature_selected()):
            layout.label(text="Select required armature", icon = 'INFO')

        layout.prop(fbt, "src_armature", text="Source Armature")

        layout.operator('fblah.getbonesaxisanglerot', icon='COPYDOWN')
        layout.operator('fblah.getinvertedbonesaxisanglerot', icon='COPYDOWN')
        layout.operator('fblah.setbonesaxisanglerot', icon='IMPORT')        
        
        layout.separator()