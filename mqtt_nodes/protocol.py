import bpy

import json


def get_manifest():
    scn = bpy.context.scene
    inp_property_descs = []
    for prop in scn.mqtt_inputs:
        name = prop.property_name
        inp_property_descs.append({"name" : name})
    manifest = {"input_properties" : inp_property_descs}
    return json.dumps(manifest)

