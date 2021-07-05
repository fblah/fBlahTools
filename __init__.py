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

# load and reload submodules
# ----------------------------------------------------------

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

import bpy
from bpy.props import (PointerProperty)
import traceback
from .tools import UISettings

# register
# ----------------------------------------------------------

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    #Custom scene properties
    bpy.types.Scene.fBlahToolsSettings = PointerProperty(type=UISettings)
    
    #print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

# unregister
# ----------------------------------------------------------

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    del bpy.types.Scene.fBlahToolsSettings

    #print("Unregistered {}".format(bl_info["name"]))
