import bpy

from bpy.types import Panel

class MQTTNodePanel(Panel):

    bl_label = 'MQTT'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'MQTT'
    bl_idname = 'NODE_PT_mqtt'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row()
        row.label(text="This is a test")


class MQTTPanel(Panel):
    bl_label = 'MQTT'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_idname = 'SCENE_PT_mqtt'

    def draw(self, context):
        scn = bpy.context.scene
        mqtt_settings = scn.mqtt_settings
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.prop(mqtt_settings, "broker_host")
        col.prop(mqtt_settings, "topic_prefix")

