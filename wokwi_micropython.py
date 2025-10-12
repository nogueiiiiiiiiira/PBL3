import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
import dht

# configurações
SSID = "Wokwi-GUEST"
PASSWORD = ""
MQTT_BROKER = "broker.hivemq.com"

TOPICO_TEMPERATURA = b"/sensor/temperatura"
TOPICO_UMIDADE = b"/sensor/umidade"
TOPICO_LED = b"/atuador"
TOPICO_ATUALIZA = b"/atualizar"

# inicializando
led_vermelho = Pin(2, Pin.OUT)
sensor = dht.DHT22(Pin(4))

# callback MQTT
def mqtt_callback(topic, msg):
    if topic == TOPICO_LED:
        led_vermelho.value(1 if msg == b"1" else 0)
    elif topic == TOPICO_ATUALIZA:
        try:
            sensor.measure()
            temperatura = sensor.temperature()
            umidade = sensor.humidity()
            # Envia como JSON
            client.publish(TOPICO_TEMPERATURA, '{"sensor":"/sensor/temperatura", "valor":' + str(temperatura) + '}')
            client.publish(TOPICO_UMIDADE, '{"sensor":"/sensor/umidade", "valor":' + str(umidade) + '}')
        except Exception as e:
            print("Erro ao ler sensor:", e)

# conexão Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
while not wifi.isconnected():
    time.sleep(1)

# conexão MQTT
client = MQTTClient(b"KarenNogueira", MQTT_BROKER)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(TOPICO_LED)
client.subscribe(TOPICO_ATUALIZA)
print("MQTT conectado")

# loop principal apenas processa mensagens
while True:
    try:
        client.check_msg()  # aguarda mensagens
        time.sleep(0.1)
    except Exception as e:
        print("Erro no loop:", e)
        try:
            client.disconnect()
        except:
            pass
        time.sleep(5)
        while True:
            try:
                client.connect()
                client.subscribe(TOPICO_LED)
                client.subscribe(TOPICO_ATUALIZA)
                break
            except:
                time.sleep(5)
