# **Système de Surveillance Météo et Température avec ESP32 et Raspberry Pi 5**


### Interface :

![Interface](.img/interface_temp.jpg)

Ce projet est un système de surveillance de la météo et de la température qui utilise un **ESP32** connecté à un **Raspberry Pi 5** pour collecter et afficher des données en temps réel telles que la température, l'humidité et les conditions météorologiques. Le système utilise un capteur de température et d'humidité **DHT22** connecté à l'ESP32, qui est relié au Raspberry Pi via USB. Le Raspberry Pi exécute également une interface graphique basée sur **PyQt5** pour visualiser les données et les conditions météorologiques actuelles récupérées depuis l'**API OpenWeatherMap**.

## **Matériel utilisé**

- **Raspberry Pi 5 (8GB de RAM)** : Exécute l'application Python et gère la communication avec l'ESP32.
- **ESP32** : Utilisé pour lire les données du capteur **DHT22** et les envoyer via la communication série au Raspberry Pi.
- **Capteur DHT22** : Un capteur numérique de température et d'humidité, connecté à l'ESP32.
- **Écran** : Connecté au Raspberry Pi pour afficher en temps réel les données sur la météo et le capteur.

### **Connexions**
- L'**ESP32** est connecté au Raspberry Pi via USB et sert à récupérer les données du capteur DHT22.
- Un **écran** est connecté au Raspberry Pi pour visualiser les données météorologiques via une interface graphique.

## **Logiciels nécessaires**

- **Python 3.8+**
- **PyQt5** : Pour l'interface graphique (GUI).
- **requests** : Pour récupérer les données météorologiques de l'API OpenWeatherMap.
- **ftfy** : Pour corriger et nettoyer tout problème lié au texte.
- **serial** : Pour la communication série entre le Raspberry Pi et l'ESP32.
- **dotenv** : Pour charger les variables d'environnement (par exemple, la clé API OpenWeatherMap).
- **Bibliothèques DHT** : Pour la gestion du capteur DHT22 avec l'ESP32.

## **Installation**

### 1. Cloner le repository

```bash
git clone https://github.com/Developpeur-Mehdi/raspberry_temperature_humidte.git
cd nom-du-repository
```

### 2. Installer les dépendances Python
Assurez-vous d'avoir Python 3 installé, puis installez les dépendances nécessaires en utilisant **pip** :
- **pip install -r requirements.txt**

### 3. Configurer l'API OpenWeatherMap
- Créez un compte sur **OpenWeatherMap** et obtenez une **clé API**.
- Créez un fichier **.env** à la racine du projet et ajoutez votre clé API comme ceci :
  - **api_key=VOTRE_CLE_API**
  - **ma_ville="NomDeVotreVille"**
  
### 4. Charger le code dans l'ESP32
Connectez votre **ESP32** à votre ordinateur via **USB**.
Utilisez l'IDE Arduino ou PlatformIO pour téléverser le code de l'ESP32 (celui contenant la gestion du capteur DHT22 et la communication série).

### 5. Lancer l'application
Une fois toutes les configurations terminées, vous pouvez démarrer l'application PyQt5 en exécutant :

- **python main.py**
Cela lancera l'interface graphique et commencera à récupérer et afficher les données en temps réel.
---
### Fonctionnement du Système
Le **capteur DHT22** connecté à l'**ESP32** lit en temps réel les données de **température et d'humidité**.
L'**ESP32** envoie ces données au **Raspberry Pi** via une connexion **série USB**.
Le Raspberry Pi utilise une **interface PyQt5** pour afficher la **température, l'humidité** et les **conditions météorologiques** actuelles, récupérées via l'**API OpenWeatherMap**.
**Les données météorologiques (température actuelle, conditions) sont actualisées toutes les heures par défaut, ou lorsque l'application est lancée**.

---

**├── main.py                    # Application principale PyQt5 pour afficher les données
├── meteo.py                   # Module pour récupérer les données météo depuis OpenWeatherMap
├── requirements.txt           # Liste des dépendances Python nécessaires
├── .env                       # Fichier de configuration pour les variables d'environnement
├── img/                       # Dossier contenant les images utilisées pour l'interface
│   ├── meteo/                 # Images pour différents types de météo (pluie, soleil, etc.)
│   └── error_icon.png         # Icône d'erreur (si les données météo ne peuvent pas être récupérées)
└── README.md                  # Ce fichier**

### Problèmes connus
Problèmes de connexion série : Si l'application ne peut pas lire les données de l'ESP32, assurez-vous que le port série est correctement configuré et que l'ESP32 est bien connecté.
Erreur d'API : Si les données météorologiques ne se chargent pas, vérifiez que votre clé API est valide et que votre connexion Internet fonctionne correctement.
--- 
### Licence
Ce projet est sous licence MIT. Vous pouvez librement l'utiliser et le modifier, mais veuillez conserver la mention de la licence dans toute redistribution.


