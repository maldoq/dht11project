# **dht11project**
 
Bienvenue sur notre projet **dht11project**.Ce projet vise à faire intérargir une application et un dispositif de capteur de température pour afficher les informations de température et d'humidité en tant réel. Il nous permettra d'avoir la température et l'humidité ambiants moyens d'une pièce et une courbe montrant donc l'évolution de ceux-ci.

---

## 📖 **Table des Matières**

- [Prérequis](#prérequis)
- [Elaboration du projet](#élaboration-du-projet)
- [Exécution des Tests](#exécution-des-tests)

---

## *prérequis*
Pour ce projet, nous aurons besoin d'une dépendance hardware et software.
Au niveau du hardware, nous aurons besoin de:
- dht11 sensor (capteur de température et d'humidité)
- esp8266 (carte arduino captant le wifi)
- 3 fils de connection femelle-femelle
- 1 planche à pain
**Nb**: La majorité de ces éléments peuvent être trouvé dans un kit arduino sauf la esp8266.

Au niveau du software, nous aurons besoin de:
- [visual studio code](https://code.visualstudio.com/Download)
- [git](https://git-scm.com/downloads)
- [Arduino IDE](https://www.arduino.cc/en/software)
- [python](https://www.python.org/downloads/)

---

## *élaboration du projet*
Nous allons d'abord mettre en place l'application qui sera réalisé avec django qui est un [**framework**](https://fr.wikipedia.org/wiki/Framework) backend python et du *HTML, CSS et JS* pour le côté Frontend. Et ensuite, nous mettrons en place le dispositif du dht11. Après cela, nous programmerons le dispositif à l'aide de *Arduino IDE* pour pouvoir récupérer les informations. Et pour finir, nous connecterons ce dispositif à l'application faite avec django.
1. **Clone du projet et installation des dépendances**

Avant de cloner le projet, Créez un dossier *projet* dans le repertoire document.
Ensuite, ouvrir vscode et ouvrir le dossier nouvellement crée.
![image](https://github.com/user-attachments/assets/383bcdfa-2e10-4d55-8125-3ade5f9455c5)
Après cela, ouvrir le terminal et entrer cette commande:
    ```bash
    
        git clone https://github.com/maldoq/dht11project.git
        cd dht11project
        py -m pip install virtualenv
        py -m venv env
        env/scripts/activate
        pip install -r requirements.txt
2. **Montage du circuit de la dht11**

Nous utiliserons principalement deux outils, la dht11 et l'esp8266
Au niveau de la dht11:
![image](https://github.com/user-attachments/assets/d3ac57b9-d996-4fb0-be66-d27fb799f1c3)
Elle est généralement constitué de trois ou quatres bornes. Cependant, nous nous intéresserons au cas ou elle n'a que trois bornes. La première borne de la dht11 transmet le signal pour la température et l'humidité, la deuxième borne est la Vcc (compris entre 3,3v et 6v) et la dernière borne pour la terre (tension de sortie).
**Nb**: La borne du signal et la Vcc peuvent permuter les places selon la version du dht11 donc bien vérifier les bornes.
Pour plus d'information, cliquer sur ce lien : [dht11 info](https://projecthub.arduino.cc/arcaegecengiz/using-dht11-12f621)

Au niveau de la esp8266:
![image](https://github.com/user-attachments/assets/ca1fc755-5327-4fc5-b921-55a4b25dbda8)
Elle  fonctionne de la même façon qu'une *carte arduino uno* à la seule différence qu'elle a la possibilité de ce connecter au wifi et qu'elle se limite à 3,3v de tension délivrée. Elle a des bornes ground pour la masse et Vcc (3,3v) pour la tension qu'elle fournie. Deplus, elle a aussi une multitude de port numérique et analogique (D0 à D8). Cependant, les ports D0 et D1 ne peuvent pas être utilisé.
Pour plus d'information, cliquer sur ce lien : [esp8266 info](https://projecthub.arduino.cc/PatelDarshil/getting-started-with-nodemcu-esp8266-on-arduino-ide-b193c3)
Voici un exemple de comment connecter la dht11 et l'esp8266:
![image](https://github.com/user-attachments/assets/bbd67265-f20c-4522-bdd9-17776465a378)
**Nb**: Sur ce schema, la borne data et la borne Vcc ont été permuté.
3. **Programmation de la carte esp8266**

Ayant installé le logiciel Arduino IDE sur notre ordinateur, nous allons l'ouvrir et créer un nouveau projet. Ce projet ce nommera (dht11projectsensor).
Nous auront besoin d'installer des librairies qui nous permettrons d'utiliser la dht11 et la esp8266:
![image](https://github.com/user-attachments/assets/824d7aad-6685-45b4-86c8-58b36aceea66)
Dans le manage librairies, chercher Dht11 sensor by adafruit et installer le (pour la bibliothèque dht11).
Et pour la esp8266, rendez-vous sur ce lien pour suivre les étapes d'installation: [esp8266 info](https://projecthub.arduino.cc/PatelDarshil/getting-started-with-nodemcu-esp8266-on-arduino-ide-b193c3).
Ceci étant fait, nous allons copier le code ci-dessous et le remplacer dans le code du fichier actuel:
    ```bash
    
        #include <ESP8266WiFi.h>
        #include <DHT.h>
        #include <ESP8266HTTPClient.h>
        
        const char* ssid = "your_wifi_name";
        const char* password = "your_wifi_code";
        
        #define DHTPIN D3
        #define DHTTYPE DHT11
        DHT dht(DHTPIN, DHTTYPE);
        
        WiFiClient wifiClient;  // Declare WiFiClient object
        const char* serverURL = "http://192.168.x.x:8000/save-data/";  // Replace with your actual server URL
        
        void setup() {
          Serial.begin(115200);
          dht.begin();
          
          WiFi.begin(ssid, password);
          while (WiFi.status() != WL_CONNECTED) {
            delay(1000);
            Serial.println("Connecting to WiFi...");
          }
          Serial.println("Connected to WiFi.");
        }
        
        void loop() {
          if (WiFi.status() == WL_CONNECTED) {
            float temperature = dht.readTemperature();
            float humidity = dht.readHumidity();
        
            if (isnan(temperature) || isnan(humidity)) {
              Serial.println("Failed to read from DHT sensor!");
              return;
            }
        
            String jsonData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";
        
            HTTPClient http;
            http.begin(wifiClient, serverURL);  // Use the updated version with WiFiClient
        
            http.addHeader("Content-Type", "application/json");
            int httpResponseCode = http.POST(jsonData);
        
            if (httpResponseCode > 0) {
              String response = http.getString();
              Serial.println("Server Response: " + response);
            } else {
              Serial.println("Error sending data to server");
            }
        
            http.end();
          }
        
          delay(15000);  // Collect data every 15 seconds
        }

**Nb:** remplacer la valeur de la constante ssid par le nom du wifi et et celui du password par celui du wifi. La esp8266 doit être connecté au même réseau que l'ordinateur.
Après cela, exécuter ou uploader le code sur la carte esp8266

4. **Liaison du hardware et du software**

Retournons dans le terminal de vscode, là où le projet à été laissé c'est-à-dire après avoir cloné le projet et installer les dépendances. Nous allons maintenant éffectuer les migrations et lancer le serveur. Pour ce faire, taper ces commandes dans le terminal:

        py manage.py makemigrations
        py manage.py migrate
        py manage.py runserver 192.168.x.x:8000
nb: ne pas oublié de remplacer le x.x par celui l'ip address de votre pc.
