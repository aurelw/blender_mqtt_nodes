import bpy

import threading

import paho.mqtt.client as mqtt

from . import driver_utils, protocol


class MQTTConnection:

    def __init__(self):
        self._thread = None
        self._keep_running = False
        self._do_pub_manifest = False

    def _on_connect(client, userdata, flags, rc):
        topic_prefix = userdata
        client.subscribe(topic_prefix + "#")
        print("[MQTT] connected.")

    def _on_message(client, userdata, msg):
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


    def _pub_manifest(self, client):
        manifest = protocol.get_manifest()
        client.publish(self._topic_prefix + "manifest", manifest,
                       qos=0, retain=True)
                
    def _run(self):
        print("[MQTT] Connecting to host:", self._broker_host)
        client = mqtt.Client()
        client.user_data_set(self._topic_prefix)
        client.on_connect = MQTTConnection._on_connect
        client.on_message = MQTTConnection._on_message
        client.connect(self._broker_host, 1883, 60)
        self._pub_manifest(client)
        while self._keep_running:
            client.loop(timeout=0.2)
            #FIXME may need locking for race condition
            if self._do_pub_manifest:
                self._pub_manifest(client)
                self._do_pub_manifest = False

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

    def pub_manifest(self):
        self._do_pub_manifest = True

    def stop(self):
        if self._thread:
            self._keep_running = False
            self._thread.join()
            self._thread = None


mqtt_connection = MQTTConnection()
