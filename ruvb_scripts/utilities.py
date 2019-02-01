# python

"""Useful functions to simplify modo python scripts"""

import lx


def remember_fbx_settings():
    """Store the users FBX export settings"""

    fbx_values = []
    fbx_values.append(lx.eval('preset.fbx ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.import.compatibility ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.format ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.exportType ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.exportToASCII ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.animationOnly ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.geometry ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.materials ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.cameras ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.lights ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.animation ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.surfaceRefining ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.polygonParts ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.selectionSets ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.smoothingGroups ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.morphMaps ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.tangentsBitangents ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.units ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.scale ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.exportRgbaAsDiffCol ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.pbrMaterials ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.sampleAnimation ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.sampleAnimFpsMultiplier ?'))
    fbx_values.append(lx.eval('user.value sceneio.fbx.save.exportActionType ?'))
    return fbx_values


def restore_fbx_settings(fbx_values):
    """Restore FBX settings saved with remember_fbx_settings()"""

    lx.eval('preset.fbx %s' % fbx_values[0])
    lx.eval('user.value sceneio.fbx.import.compatibility %s' % fbx_values[1])
    lx.eval('user.value sceneio.fbx.save.format %s' % fbx_values[2])
    lx.eval('user.value sceneio.fbx.save.exportType %s' % fbx_values[3])
    lx.eval('user.value sceneio.fbx.save.exportToASCII %s' % fbx_values[4])
    lx.eval('user.value sceneio.fbx.save.animationOnly %s' % fbx_values[5])
    lx.eval('user.value sceneio.fbx.save.geometry %s' % fbx_values[6])
    lx.eval('user.value sceneio.fbx.save.materials %s' % fbx_values[7])
    lx.eval('user.value sceneio.fbx.save.cameras %s' % fbx_values[8])
    lx.eval('user.value sceneio.fbx.save.lights %s' % fbx_values[9])
    lx.eval('user.value sceneio.fbx.save.animation %s' % fbx_values[10])
    lx.eval('user.value sceneio.fbx.save.surfaceRefining %s' % fbx_values[11])
    lx.eval('user.value sceneio.fbx.save.polygonParts %s' % fbx_values[12])
    lx.eval('user.value sceneio.fbx.save.selectionSets %s' % fbx_values[13])
    lx.eval('user.value sceneio.fbx.save.smoothingGroups %s' % fbx_values[14])
    lx.eval('user.value sceneio.fbx.save.morphMaps %s' % fbx_values[15])
    lx.eval('user.value sceneio.fbx.save.tangentsBitangents %s' % fbx_values[16])
    lx.eval('user.value sceneio.fbx.save.units %s' % fbx_values[17])
    lx.eval('user.value sceneio.fbx.save.scale %s' % fbx_values[18])
    lx.eval('user.value sceneio.fbx.save.exportRgbaAsDiffCol %s' % fbx_values[19])
    lx.eval('user.value sceneio.fbx.save.pbrMaterials %s' % fbx_values[20])
    lx.eval('user.value sceneio.fbx.save.sampleAnimation %s' % fbx_values[21])
    lx.eval('user.value sceneio.fbx.save.sampleAnimFpsMultiplier %s' % fbx_values[22])
    lx.eval('user.value sceneio.fbx.save.exportActionType %s' % fbx_values[23])

def store_scene_masks():
    """Store the material masks currently in the scene"""

    scene_masks = lx.eval('query sceneservice mask.N ?')
    shader_list = []
    for mask in range(0, scene_masks):
        lx.eval('select.item %s' % mask)
        mask_id = lx.eval('query sceneservice mask.id ? %s' % mask)
        shader_list.append(mask_id)
    return shader_list


def store_scene_meshes():
    """Store the mesh items currently in the scene"""

    scene_meshes = lx.eval('query sceneservice mesh.N ?')
    mesh_list = []
    for mesh in range(0, scene_meshes):
        lx.eval('select.item %s' % mesh)
        mesh_id = lx.eval('query sceneservice mesh.id ? %s' % mesh)
        mesh_list.append(mesh_id)
    return mesh_list


def store_scene_groups():
    """Store the group locators currently in the scene"""

    scene_groups = lx.eval('query sceneservice groupLocator.N ?')
    group_list = []
    for group in range(0, scene_groups):
        lx.eval('select.item %s' % group)
        group_id = lx.eval('query sceneservice groupLocator.id ? %s' % group)
        group_list.append(group_id)
    return group_list


def store_selected_uvmap():
    """Store the currently selected UV Map"""

    selected_vmaps = lx.evalN('query layerservice vmaps ? selected')
    uvmap_names = []

    for vmap in selected_vmaps:
        vmap_type = lx.eval('query layerservice vmap.type ? %s' % vmap)
        if vmap_type == 'texture':
            for uvmap in selected_vmaps:
                vmap_name = lx.evalN('query layerservice vmap.name ? %s' % uvmap)
                uvmap_names.append(vmap_name)
        else:
            pass
    return uvmap_names
