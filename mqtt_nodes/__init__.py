# Author: Aurel Wildfellner

bl_info = {
    "name": "MQTT Nodes",
    "author": "Aurel Wildfellner",
    "blender": (3, 4, 0),
    "location": "Node > Toolbox",
    "description": "Drive geometry nodes with MQTT data",
    "warning": "",
    "wiki_url": "",
    "support": 'TESTING',
    "category": "Node"}


import bpy

from bpy.app.handlers import persistent

from bpy.props import (
        StringProperty,
        BoolProperty,
        IntProperty,
        FloatProperty,
        EnumProperty,
        PointerProperty,
        CollectionProperty
        )
from bpy.types import (
        PropertyGroup
        )

from . import ui, operators

from . import mqtt_connection

class MQTTSettingsProp(PropertyGroup):
    broker_host : StringProperty(
            name="Broker Host",
            description="IP or hostname of the broker",
            default=""
            )
    topic_prefix : StringProperty(
            name="Topic Prefix",
            description="Prefix for the topic before all the input topics",
            default="/bl_prop_input/"
            )

class MQTTInputProp(PropertyGroup):
    topic : StringProperty(
            name="Topic",
            description="The topic postfix to get input data from",
            default=""
            )
    property_name : StringProperty(
            name="Custom Property Name",
            description="The name of the custom to write to in the scene",
            default="var0"
            )
    min_value : FloatProperty(
            name="Min Value",
            description="If a float value, limit to this minimum",
            default=0.0
            )
    max_value : FloatProperty(
            name="Max Value",
            description="If a float value, limit to this maximum",
            default=1.0
            )

@persistent
def post_file_load_handler(none_par):
    print("post_file_load_handler !!!!!!!!!")
    scn = bpy.context.scene
    host = scn.mqtt_settings.broker_host
    topic = scn.mqtt_settings.topic_prefix
    # sanity check hostname
    if len(host) > 3:
        mqtt_connection.mqtt_connection.run(host, topic)

classes = [
    MQTTSettingsProp,
    MQTTInputProp,
    ui.MQTTNodePanel,
    ui.MQTTPanel,
    operators.MQTTAddInputProperty,
    operators.MQTTRemoveInputProperty,
    operators.MQTTReconnectClient,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mqtt_settings = PointerProperty(type=MQTTSettingsProp)
    bpy.types.Scene.mqtt_inputs = CollectionProperty(type=MQTTInputProp)
    bpy.app.handlers.load_post.append(post_file_load_handler)


def unregister():
    mqtt_connection.mqtt_connection.stop()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mqtt_inputs
    del bpy.types.Scene.mqtt_settings

