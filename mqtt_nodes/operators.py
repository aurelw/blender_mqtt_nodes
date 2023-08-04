import bpy

from bpy.types import Operator

from . import mqtt_connection

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


class MQTTReconnectClient(Operator):
    """Reconnect the MQTT Client"""
    bl_idname = "mqtt.reconnect_client"
    bl_label = "MQTT Reconnect Client"

    def execute(self, context):
        mqtt_connection.mqtt_connection.stop()
        try:
            scn = bpy.context.scene
            host = scn.mqtt_settings.broker_host
            topic = scn.mqtt_settings.topic_prefix
            mqtt_connection.mqtt_connection.run(host, topic)
        except:
            return {'CANCELED'}
        return {'FINISHED'}

