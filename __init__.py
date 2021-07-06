# ----------------------------------------------------------
# File __init__.py
# ----------------------------------------------------------
#
# ShapeKeyTransfer - Copyright (C) 2018 Ajit Christopher D'Monte
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

# Addon info
# ----------------------------------------------------------

bl_info = {
    "name": "fBlah's Tools",
    "description": "Miscellaneous tools by fBlah for blender",
    "author": "Ajit D'Monte (fBlah), email: ajitdmonte@gmail.com",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Tools > fBlah's Tools",    
    "warning": "This has not been tested rigorously.",
    "wiki_url": "",    
    "category": 'Mesh'}

# register
# ----------------------------------------------------------

import bpy
from bpy.props import (PointerProperty)

from . tools import *

def register():
    bpy.utils.register_class(fBlahToolsUISettings)
    bpy.utils.register_class(GetBoneAxisAngleRotationsOperator)
    bpy.utils.register_class(GetInvertedBoneAxisAngleRotationsOperator)
    bpy.utils.register_class(SetBoneAxisAngleRotationsOperator)
    bpy.utils.register_class(VIEW3D_PT_tools_fBlah)  
    #Custom scene properties
    bpy.types.Scene.fBlahToolsSettings = PointerProperty(type=fBlahToolsUISettings)
    
    #print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

# unregister
# ----------------------------------------------------------

def unregister():
    bpy.utils.unregister_class(fBlahToolsUISettings)
    bpy.utils.unregister_class(GetBoneAxisAngleRotationsOperator)
    bpy.utils.unregister_class(GetInvertedBoneAxisAngleRotationsOperator)
    bpy.utils.unregister_class(SetBoneAxisAngleRotationsOperator)
    bpy.utils.unregister_class(VIEW3D_PT_tools_fBlah)  
    del bpy.types.Scene.fBlahToolsSettings

    #print("Unregistered {}".format(bl_info["name"]))