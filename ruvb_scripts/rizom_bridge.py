# python

"""Bridge between Modo and RizomUV"""

import sys
import tempfile
import os
import subprocess
import platform
import lx
import ruvb_scripts.utilities as utilities


EXPORTED_FILE = tempfile.gettempdir() + os.sep + 'rizom_temp.fbx'


def rizom_path_update():
    """Allows the user to set a new path to the RizomUV executable"""

    try:
        if lx.eval('!!query scriptsysservice userValue.isDefined ? coh.rizom_path'):
            lx.eval('dialog.setup style:fileOpen')
            lx.eval('!!dialog.title {Select the RizomUV executable}')
            lx.eval('dialog.open')
            rizom_exe = lx.eval('!!dialog.result ?')
            lx.eval('!!user.value coh.rizom_path {%s}' % rizom_exe)

        else:
            lx.eval('!!user.defNew name:coh.rizom_path type:string life:config')
            lx.eval('dialog.setup style:fileOpen')
            lx.eval('!!dialog.title {Select the RizomUV executable}')
            lx.eval('dialog.open')
            rizom_exe = lx.eval('!!dialog.result ?')
            lx.eval('!!user.value coh.rizom_path {%s}' % rizom_exe)

    except RuntimeError:
        if lx.eval('!!query scriptsysservice userValue.isDefined ? coh.rizom_path'):
            lx.eval('!!user.defDelete coh.rizom_path')
        sys.exit()


def rizom_path_check():
    """prompts the user to set the path to rizomuv if it is not saved in the config already"""

    try:
        if lx.eval('!!query scriptsysservice userValue.isDefined ? coh.rizom_path'):
            pass

        else:
            lx.eval('!!user.defNew name:coh.rizom_path type:string life:config')
            lx.eval('dialog.setup style:fileOpen')
            lx.eval('!!dialog.title {Select the RizomUV executable}')
            lx.eval('dialog.open')
            rizom_exe = lx.eval('dialog.result ?')
            lx.eval('!!user.value coh.rizom_path {%s}' % rizom_exe)

    except RuntimeError:
        if lx.eval('!!query scriptsysservice userValue.isDefined ? coh.rizom_path'):
            lx.eval('user.defDelete coh.rizom_path')
        sys.exit()


def export_settings():
    """Set the FBX export settings for exporting to rizom"""

    lx.eval('user.value sceneio.fbx.save.format FBXLATEST')
    lx.eval('user.value sceneio.fbx.save.exportType FBXExportSelection')
    lx.eval('user.value sceneio.fbx.save.geometry true')
    lx.eval('user.value sceneio.fbx.save.materials true')
    lx.eval('user.value sceneio.fbx.save.lights false')
    lx.eval('user.value sceneio.fbx.save.cameras false')
    lx.eval('user.value sceneio.fbx.save.smoothingGroups true')
    lx.eval('user.value sceneio.fbx.save.selectionSets false')


def assign_polyset_materials():
    """Assign unique materials to every polygon selection set"""

    num_polset = lx.eval('query layerservice polset.N ? selected')
    for polyset in range(num_polset):
        polset_name = lx.eval('query layerservice polset.name ? %s' % polyset)
        lx.eval('select.drop polygon')
        lx.eval('select.useSet {%s} select' % polset_name)
        lx.eval('poly.setMaterial {%s} {0.5 0.5 0.5} 0.8 0.2 true false false' % polset_name)
        lx.eval('select.drop polygon')


def delete_polyset_material_tags():
    """Delete the left over tags from the 'assign_polyset_materials' function"""

    sel_mesh = lx.evalN('query sceneservice selection ? all')
    num_polset = lx.eval('query layerservice polset.N ? selected')

    for polyset in range(num_polset):
        polset_name = lx.eval('query layerservice polset.name ? %s' % polyset)
        for _ in sel_mesh:
            lx.eval('poly.renameTag {%s} {} MATR' % polset_name)


def to_rizom():
    """Export the selected meshes to a temporary directory"""

    rizom_path_check()

    rizomuv_path = lx.eval('!!user.value coh.rizom_path ?')

    # Store the selected meshes
    sel_layers = lx.evalN('query sceneservice selection ? all')

    shader_list = utilities.store_scene_masks()

    if lx.eval('!!user.value coh.polyset_toggle ?') == 'on':
        assign_polyset_materials()

    fbx_values = utilities.remember_fbx_settings()

    # Select the stored meshes
    for mesh in sel_layers:
        lx.eval('select.subItem %s add' % mesh)

    # Add rizomtemp suffix for easy identification later
    for mesh in sel_layers:
        lx.eval('select.Item {%s}' % str(mesh))
        mesh_name = lx.eval('query sceneservice item.name ? {%s}' % mesh)
        new_name = mesh_name + '_rizomtemp'
        lx.eval('item.name {%s}' % (new_name))

    # Make sure meshes are selected for export
    for mesh in sel_layers:
        lx.eval('select.subItem %s add' % mesh)

    export_settings()

    # Export the meshes to RizomUV
    lx.eval('scene.saveAs "%s" fbx true' % EXPORTED_FILE)

    try:
        cmd = '"' + rizomuv_path + '" "' + EXPORTED_FILE + '"'
        if platform.system() == 'Windows':
            subprocess.Popen(cmd)
        else:
            subprocess.Popen(['open', '-a', rizomuv_path, '--args', EXPORTED_FILE])

    except WindowsError:
        lx.eval('dialog.setup style:Error')
        lx.eval('dialog.title {Invalid excecutable path}')
        lx.eval('dialog.msg {There is a problem with your selected path, please make sure it is correct.}')
        lx.eval('dialog.open')
        lx.eval('!!user.value coh.rizom_path ""')
        lx.eval('user.defDelete coh.rizom_path')
        sys.exit()

    utilities.restore_fbx_settings(fbx_values)

    delete_polyset_material_tags()

    # Get the material masks in the scene now that the temp materials have been applied and exported
    new_shader_list = utilities.store_scene_masks()

    lx.eval('select.drop item')

    # Find and delete the temporary materials by getting the difference between the lists of masks
    new_shader_list = [shader for shader in new_shader_list if shader not in shader_list]
    for mask in new_shader_list:
        lx.eval('select.item {%s} mode:add' % mask)

    lx.eval('delete')

    # Delete the rizomtemp suffix now that the meshes have been exported
    for mesh in sel_layers:
        lx.eval('select.subItem {%s} mode:add' % mesh)

    for mesh in sel_layers:
        lx.eval('select.Item {%s}' % mesh)
        mesh_name = lx.eval('query sceneservice item.name ? {%s}' % mesh)
        new_name = mesh_name.replace('_rizomtemp', '')
        lx.eval('item.name {%s}' % (new_name))

    # End with the meshes selected to return the scene to its original state
    for mesh in sel_layers:
        lx.eval('select.subItem {%s} mode:add' % mesh)


def from_rizom():
    """Import mesh from RizomUV and copy the UVs to original meshes"""

    sel_layers = lx.evalN('query sceneservice selection ? all')

    uvmap_name = utilities.store_selected_uvmap()

    original_meshes = utilities.store_scene_meshes()
    original_groups = utilities.store_scene_groups()

    lx.eval('loaderOptions.fbx false true false false false false false false false false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport')
    lx.eval('!scene.open "%s" import' % EXPORTED_FILE)

    new_meshes = []
    new_meshes = utilities.store_scene_meshes()
    new_groups = utilities.store_scene_groups()

    # Find new meshes and groups
    new_meshes = [mesh for mesh in new_meshes if mesh not in original_meshes]
    new_groups = [group for group in new_groups if group not in original_groups]

    lx.eval('select.drop item')

    # Copy UVs from the imported meshes to the original meshes, uses the rizomtemp suffix to identify the correct mesh pairs

    for mesh in new_meshes:
        lx.eval('select.Item {%s} mode:add' % mesh)

    imported_sel = lx.evalN('query sceneservice selection ? all')
    mesh_names = []

    for mesh in imported_sel:
        mesh_names.append(lx.eval('query sceneservice item.name ? {%s}' % mesh))

    for mesh in mesh_names:
        for uvmap in uvmap_name:
            lx.eval('select.Item {%s}' % mesh + '_rizomtemp')
            lx.eval('select.vertexMap {%s} txuv replace' % uvmap)
            sel = lx.evalN('query sceneservice selection ? all')
            lx.eval('uv.copy')
            temp_id = lx.eval('query sceneservice item.name ? {%s}' % sel)
            lx.eval('select.drop item')

            for _ in new_meshes:
                lx.eval('select.Item {%s}' % temp_id.replace('_rizomtemp', ''))
                lx.eval('select.vertexMap {%s} txuv replace' % uvmap)
                lx.eval('uv.paste selection')
                lx.eval('select.drop item')

    # Clean up the scene
    for mesh in new_meshes:
        lx.eval('select.item {%s} mode:add' % mesh)
        lx.eval('delete')

    for group in new_groups:
        lx.eval('select.item {%s} mode:add' % group)
        lx.eval('delete')

    for mesh in sel_layers:
        lx.eval('select.item {%s} mode:add' % mesh)
        lx.eval('select.vertexMap {%s} txuv replace' % uvmap_name[0])
