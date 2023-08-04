import bpy

from bpy.types import Operator

class MQTTAddInputProperty(Operator):
    """Adds an input property to the scene"""
    bl_idname = "mqtt.add_input_property"
    bl_label = "MQTT Add Input Property"

    def execute(self, context):
        scn = context.scene
        scn.mqtt_inputs.add()
        return {'FINISHED'}


class MQTTRemoveInputProperty(Operator):
    """Remove an input property to the scene"""
    bl_idname = "mqtt.remove_input_property"
    bl_label = "MQTT Remove Input Property"

    property_index : bpy.props.IntProperty()

    def execute(self, context):
        scn = context.scene
        scn.mqtt_inputs.remove(int(self.property_index))
        return {'FINISHED'}

