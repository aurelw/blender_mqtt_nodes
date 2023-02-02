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

