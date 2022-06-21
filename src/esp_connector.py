import paho.mqtt.client as mqtt


class ESP_Connector():
    def __init__(self) -> None:
        self.mqttc = mqtt.Client()

    def reinit(self) -> None:
        self.mqttc.reinitialise()

