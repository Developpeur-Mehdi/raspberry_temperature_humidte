#include <DHT.h>
#include <Adafruit_Sensor.h>
#include "esp_sleep.h"

// Définition du capteur DHT
const int DHT_PIN = 4;        // GPIO4 pour le DHT22
const int DHT_TYPE = DHT22;   // Type du capteur (DHT22)
DHT dht(DHT_PIN, DHT_TYPE);   // Objet DHT

// Variables pour gérer les délais
unsigned long lastDHTTime = 0;   // Temps de la dernière lecture du DHT22
const long dhtInterval = 2000;    // Intervalle de 2 secondes pour DHT

void setup() {
  // Désactiver la veille de l'ESP32
  esp_sleep_disable_wakeup_source(ESP_SLEEP_WAKEUP_ALL);

  // Initialisation de la liaison série
  Serial.begin(115200);
  dht.begin();

  Serial.println("ESP32 prêt. Envoi des données au format JSON...");
}

void loop() {
  unsigned long currentMillis = millis(); // Obtenir l'heure actuelle

  // Lecture du capteur DHT si le délai est écoulé
  if (currentMillis - lastDHTTime >= dhtInterval) {
    lastDHTTime = currentMillis;  // Mettre à jour le dernier temps de lecture DHT

    // Lecture des données du DHT22
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("{\"error\":\"Capteur DHT22 non disponible\"}");
    } else {
      Serial.print("{\"temperature\":");
      Serial.print(temperature, 2);
      Serial.print(",\"humidity\":");
      Serial.print(humidity, 2);
      Serial.println("}");
    }
  }
}
