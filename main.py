import json
import sys
import time
import os
import threading
import re
import serial
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QColor, QPainter, QPixmap, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QGraphicsDropShadowEffect

# Importer la fonction météo depuis le fichier meteo.py
from meteo import get_weather_data

from dotenv import load_dotenv

load_dotenv()

my_city = os.getenv("ma_ville")


class CircleProgressWidget(QWidget):
    def __init__(self, parent=None, max_value=100, current_value=50, color="#7fccff", arc_width=6):
        super().__init__(parent)
        self.setFixedSize(130, 130)  # Réduction de la taille du cercle
        self.max_value = max_value
        self.current_value = current_value
        self.color = color
        self.arc_width = arc_width

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Cercle de fond
        painter.setBrush(QBrush(QColor("#3b4b5c")))  # Couleur de fond du cercle
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(8, 8, 120, 120)

        # Arc de progression
        pen = QPen(QColor(self.color))
        pen.setWidth(self.arc_width)
        painter.setPen(pen)

        start_angle = 90 * 16  # -90 degrés = 270° en coordonnée PyQt
        span_angle = int((self.current_value / self.max_value) * 360 * 16)

        painter.drawArc(8 + self.arc_width // 2, 8 + self.arc_width // 2,
                        120 - self.arc_width, 120 - self.arc_width, start_angle, span_angle)

        # Texte au centre
        painter.setPen(QColor("#d1d1d1"))
        font = painter.font()
        font.setPointSize(20)  # Réduction de la taille de la police
        font.setBold(True)
        painter.setFont(font)

        text = f"{self.current_value}%" if self.color == "#7fccff" else f"{self.current_value}°C"
        text_rect = self.rect()
        painter.drawText(text_rect, Qt.AlignCenter, text)


class WeatherWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(340, 400)  # Taille du widget
        self.city = "l'herbergement"  # Ville par défaut
        self.weather_data = None

        self.weather_images = {
            'ciel dégagé': 'img/meteo/ciel.jpg',
            'nuageux': 'img/meteo/nuageux.jpg',
            'quelques nuages': 'img/meteo/nuageux.jpg',
            'nuages dispersés': 'img/meteo/nuageux.jpg',
            'nuages fragmentés': 'img/meteo/nuageux.jpg',
            'peu nuageux': 'img/meteo/ciel.jpg',
            'averses de pluie': 'img/meteo/pluie.jpg',
            'pluie': 'img/meteo/pluie.jpg',
            'légère pluie': 'img/meteo/pluie.jpg',
            'forte pluie': 'img/meteo/pluie.jpg',
            'orage': 'img/meteo/orage.jpg',
            'neige': 'img/meteo/neige.jpg',
            'brouillard': 'img/meteo/bruine.jpg',
            'brume': 'img/meteo/bruine.jpg',
            'couvert': 'img/meteo/nuageux.jpg',
        }

        # Création du layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 150)

        # Icône de la météo
        self.weather_icon = QLabel(self)
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_icon.setFixedSize(150, 150)
        main_layout.addWidget(self.weather_icon)

        # Label de la ville
        self.city_label = QLabel(f"Ville : {self.city}")
        self.city_label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.city_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.city_label)

        # Label de la température
        self.temp_label = QLabel("Température : --°C")
        self.temp_label.setStyleSheet("color: #ffcc00; font-size: 24px; font-weight: bold;")
        self.temp_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.temp_label)

        # Label des conditions
        self.condition_label = QLabel("Condition: --")
        self.condition_label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.condition_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.condition_label)

        # Application du layout
        self.setLayout(main_layout)

        # Timer pour les mises à jour périodiques
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_weather_timer)
        self.update_timer.start(1800000)  # Toutes les heures (en millisecondes)

    def set_weather_icon(self, icon_path):
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Erreur : Impossible de charger l'image {icon_path}")
            pixmap = QPixmap("img/error_icon.png")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.weather_icon.setPixmap(pixmap)

    def update_weather(self, city):
        self.city = city
        self.city_label.setText(f"Ville : {self.city}")

        try:
            weather_data = json.loads(get_weather_data(self.city))
            if 'error' not in weather_data:
                self.weather_data = weather_data
                self.temp_label.setText(f"Température : {weather_data['currentTemp']}°C")
                self.condition_label.setText(f"Temps : {weather_data['currentCondition']}")

                condition = weather_data['currentCondition'].lower()

                matched_condition = None
                for key in self.weather_images.keys():
                    if key in condition:
                        matched_condition = key
                        break

                if matched_condition:
                    self.set_weather_icon(self.weather_images[matched_condition])
                else:
                    self.set_weather_icon("img/meteo/nuageux.jpg")
            else:
                self.temp_label.setText("Erreur de récupération des données")
                self.condition_label.setText("Veuillez réessayer plus tard")
                self.set_weather_icon("img/error_icon.png")
        except Exception as e:
            print(f"Erreur lors de la mise à jour météo : {e}")
            self.temp_label.setText("Erreur réseau")
            self.condition_label.setText("Impossible de récupérer les données")
            self.set_weather_icon("img/error_icon.png")

    def update_weather_timer(self):
        # Cette méthode est appelée par le QTimer toutes les heures
        self.update_weather(self.city)


class SerialThread(QThread):
    # Signaux pour envoyer les données au thread principal
    temperature_signal = pyqtSignal(float)
    humidity_signal = pyqtSignal(float)
    stop_signal = pyqtSignal()  # Nouveau signal pour arrêter le thread

    def __init__(self, port="/dev/ttyUSB0", baud_rate=115200, parent=None):
        super().__init__(parent)
        self.port = port
        self.baud_rate = baud_rate
        self.running = True
        self.ser = None  # Variable pour stocker l'instance de la connexion série

    def run(self):
        """Ouvrir le port série une seule fois, puis lire les données en continu."""
        while self.running:
            try:
                # Ouverture du port série (tenter de se reconnecter si la connexion échoue)
                if self.ser is None or not self.ser.is_open:
                    self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
                    print(f"Connexion série réussie sur {self.port} à {self.baud_rate} bauds.")
                
                # Lecture des données en continu
                line = self.ser.readline()  # Lecture d'une ligne de données
                if line:
                    # Tentative de décodage de la ligne
                    try:
                        line = line.decode('utf-8', errors='replace').strip()
                        data = json.loads(line)  # Convertir la chaîne JSON en dictionnaire
                        temperature = data.get("temperature")
                        humidity = data.get("humidity")
                        
                        # Vérification des valeurs reçues
                        if temperature is not None and humidity is not None:
                            # Émettre les signaux PyQt
                            self.temperature_signal.emit(temperature)
                            self.humidity_signal.emit(humidity)
                        else:
                            print(f"Données incomplètes : {line}")
                    except (UnicodeDecodeError, json.JSONDecodeError) as e:
                        print(f"Erreur de parsing JSON ou de décodage : {e} | Ligne ignorée.")
            
            except serial.SerialException as e:
                print(f"Erreur de communication série : {e}")
                time.sleep(5)  # Attendre avant de tenter de se reconnecter

    def stop(self):
        """Arrêter proprement le thread et fermer le port série."""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()  # Fermer proprement le port série
        self.quit()


class ModernApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Température & Humidité et Météo")
        self.setFixedSize(600, 320)
        self.setStyleSheet("background-color: #2d2d3a;")

        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(50)

        row_layout = QVBoxLayout()
        row_layout.setSpacing(0)

        temp_label = QLabel("Température / Humidité")
        temp_label.setStyleSheet("color: #d1d1d1; font-size: 18px; font-weight: bold;")
        row_layout.addWidget(temp_label)

        self.temp_widget = CircleProgressWidget(self, max_value=100, current_value=0, color="#ff7f7f", arc_width=6)
        row_layout.addWidget(self.temp_widget)

        self.humidity_widget = CircleProgressWidget(self, max_value=100, current_value=0, color="#7fccff", arc_width=6)
        row_layout.addWidget(self.humidity_widget)

        left_layout.addLayout(row_layout)
        self.weather_widget = WeatherWidget(self)

        layout.addLayout(left_layout)
        layout.addWidget(self.weather_widget)

        self.setLayout(layout)

        self.serial_thread = SerialThread(port="/dev/ttyUSB0")  # Modifier en fonction de votre port série
        self.serial_thread.temperature_signal.connect(self.update_temperature)
        self.serial_thread.humidity_signal.connect(self.update_humidity)
        self.serial_thread.stop_signal.connect(self.stop_serial_thread)  # Connexion du signal d'arrêt
        self.serial_thread.start()

        # Initialiser la météo avec une ville par défaut
        self.weather_widget.update_weather(my_city)  # Ou toute autre ville de ton choix

    def update_temperature(self, temperature):
        """Met à jour la température dans le widget."""
        print(f"Mise à jour de la température : {temperature}")
        self.temp_widget.current_value = temperature
        self.temp_widget.update()

    def update_humidity(self, humidity):
        """Met à jour l'humidité dans le widget."""
        print(f"Mise à jour de l'humidité : {humidity}")
        self.humidity_widget.current_value = humidity
        self.humidity_widget.update()

    def stop_serial_thread(self):
        """Arrêter le thread série proprement."""
        self.serial_thread.stop()

    def closeEvent(self, event):
        """Émettre un signal d'arrêt du thread série avant de fermer l'application."""
        self.serial_thread.stop_signal.emit()
        self.serial_thread.wait()  # Attendre que le thread termine son exécution avant de fermer l'application
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ModernApp()
    main_window.showFullScreen()
    sys.exit(app.exec_())
