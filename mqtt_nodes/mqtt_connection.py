import bpy

import threading

import paho.mqtt.client as mqtt

from . import driver_utils


class MQTTConnection:

    def __init__(self):
        self._thread = None
        self._keep_running = False

    def on_connect(client, userdata, flags, rc):
        client.subscribe(self._topic_prefix + "#")
        print("[MQTT] connected....")

    def on_message(client, userdata, msg):
        var_name = str(msg.topic).split('/')[-1]
        scn = bpy.context.scene
        try:
            value = float(msg.payload)
        except:
            return
        do_update_drivers = False
        for prop in scn.mqtt_inputs:
            if prop.property_name == var_name:
                print("[MQTT] update var:", var_name, " = ", value)
                scn[var_name] = value
                do_update_drivers = True
        if do_update_drivers:
            driver_utils.update_all_drivers()
            scn.update_tag()
                
    def _run(self):
        client = mqtt.Client()
        client.on_connect = MQTTConnection.on_connect
        client.on_message = MQTTConnection.on_message
        client.connect(self._broker_host, 1883, 60)
        client.loop_forever()

    def run(self, broker_host, topic_prefix):
        if self._thread:
            return
        ## set con parameters
        self._broker_host = broker_host
        # fix topic prefix
        if topic_prefix[-1] != "/":
            topic_prefix += "/"
        self._topic_prefix = topic_prefix
        ## start client thread
        self._thread = threading.Thread(target=self._run)
        self._keep_running = True
        self._thread.start()

    def stop(self):
        if self._thread:
            self._keep_running = False
            self._thread.join()
            self._thread = None


mqtt_connection = MQTTConnection()
