import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import json

# Konfigurasi pin GPIO untuk sensor LDR
ldr_pin = 4  # Sesuaikan dengan pin GPIO yang digunakan
led_pin = 17

# Konfigurasi broker MQTT
mqtt_broker = "IP Address"  # Ganti dengan alamat broker MQTT yang Anda gunakan
mqtt_port = 1883 #Port MQQT
mqtt_topic = "sensor/light_intensity" #Topic MQQT

# Fungsi untuk mengirim data ke MQTT dalam format JSON
def send_mqtt_data(client, light_intensity):
    payload = {"light_intensity": light_intensity}
    json_payload = json.dumps(payload) # Convert to JSON format
    client.publish(mqtt_topic, json_payload)

# Fungsi callback ketika terhubung ke broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Terhubung ke broker MQTT dengan kode:", rc)

# Inisialisasi client MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Konfigurasi mode GPIO dan resistansi pull-down untuk sensor LDR
GPIO.setmode(GPIO.BCM)
GPIO.setup(ldr_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)
# Koneksi ke broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Loop utama
try:
    while True:
        # Baca data dari sensor LDR
        light_intensity = GPIO.input(ldr_pin)

        # Jika data valid, kirim ke MQTT dalam format JSON
        print(f"Intensitas Cahaya: {light_intensity}")
        send_mqtt_data(client, light_intensity)

        # Lampu
        if light_intensity == 1:
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            GPIO.output(led_pin, GPIO.LOW)

        # Tunggu selama 10 detik sebelum membaca sensor lagi
        time.sleep(2)

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")
finally:
    # Tutup koneksi ke broker MQTT
    client.disconnect()
    # Matikan mode GPIO
    GPIO.cleanup()
