---
date: Januar 2023
title: "Blickbox Dokumentation"
---

# Dokumentation

## Stakeholder

Ein umfassender Überblick über die Stakeholder des Systems ist von entscheidender Bedeutung. 
Dies bezieht sich auf sämtliche Personen, Rollen oder Organisationen, die entweder die Architektur des Systems kennen sollten oder von dieser überzeugt werden müssen. Zu den Stakeholdern zählen auch jene, die aktiv mit der Architektur oder dem Code arbeiten, beispielsweise indem sie Schnittstellen nutzen. Ebenso gehören Personen dazu, die die Dokumentation der Architektur benötigen, um ihre eigene Arbeit effizient zu gestalten. Darüber hinaus sind Stakeholder involviert, die Entscheidungen über das System und dessen Entwicklung treffen.
Die nachfolgende Analyse zeigt alle Stakeholder gebündelt in ihren Gewichtungen und Beziehungen.

<div style="text-align: left;">
  <img src="../../resources/stakeholderanalyse.drawio.png" alt="Stakeholder Analyse" width="500px">
  <p>Stakeholder Analyse und Zusammenfassung in den Unterscheidungen: Einbindungsgrad, Interesse und Einflüsse. Das Entwicklungsteam geht deutlich als am stärksten partizipativ gekennzeichneten Stakeholder hevor. Am repressivsten zeigen sich die Stakeholder in Form der Fußgänger.</p>
</div>

## Anforderungskonzept
Die Anforderungen an die Umsetzung des Blickbox-Projekts werden in die Kategorien funktionale, nicht funktionale und hypothetische Anforderungen unterteilt.
Diese Differenzierung ermöglicht eine umfassende Abdeckung aller Aufgabenstellungen im
Zusammenhang mit der Umsetzung des Blickbox-Projekts.

### Funktionale Anforderungen (FA)

Funktionale Anforderungen beschreiben spezifisch die konkreten Zwecke, die das zu entwickelnde Produkt erfüllen soll.


### Nicht funktionale Anforderungen (NFA)

Im Gegensatz zu funktionalen Anforderungen sind nicht-funktionale Anforderungen eher allgemein gehalten und betreffen die gesamte Architektur und das Design des Produkts.
Sie können auf verschiedene Projekte angewendet werden.

| **Anforderung**                                    | **Beschreibung**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Datenerfassung und -übertragung (FA1)**          | Das IOT-System muss in der Lage sein, kontinuierlich Sensordaten zu erfassen. <br> Diese Daten sollen in der Sensoreinheit eingelesen, an den Raspberry Pi geschickt, dort gespeichert und verarbeitet werden. <br> Die Datenübertragungen erfolgen Event-gesteuert und drahtlos. <br> Von der Sensoreinheit erfolgt die Übertragung über Bluetooth und zum Server über einen http-Client. <br> Die Daten werden in festgelegten Intervallen im JSON-Format an den Server übertragen und in der Datenbank festgehalten |
| **Interaktivität zu Dritten (FA2)**                | Die Blickbox soll attraktiver werden und Fußgänger sollen mit ihm interagieren können. <br> Das soll in Form eines Displays oder Ton und Licht geschehen. <br> Ein Display soll in der Lage sein, Dritten aktuelle Daten aus der Datenbank wie etwa das Wetter anzuzeigen. <br> Bei Dunkelheit sollen Bewegungsmelder Lichter aktivieren.                                                                                                                                                                              |
| **Containerisierung (FA3)**                        | Die Serveranwendungen sollen in Containern gekapselt werden, um eine verbesserte Portabilität und Skalierbarkeit zu gewährleisten. <br> Es wird die Container-Technologien Docker verwendet werden, um die Anwendungen effizient zu verwalten und zu deployen.                                                                                                                                                                                                                                                         |
| **Erweiterbarkeit und Wartung (NF1)**              | Die Architektur und Dokumentation des Systems sollen leicht zugänglich sein, um Erweiterungen und Verbesserungen der Features zu erleichtern. <br> Eine klare Dokumentation sowie ein vereinfachter Hardwareaufbau sollen die Wartung und Erweiterbarkeit des Systems unterstützen.                                                                                                                                                                                                                                    |
| **Sicherheit (NF2)**                               | Die Verbindung zum Server soll verschlüsselt sein, um die Sicherheit der übertragenen Daten zu gewährleisten. <br> Es müssen geeignete Verschlüsselungsprotokolle und Sicherheitsmaßnahmen implementiert werden, um die Vertraulichkeit und Integrität der Daten zu schützen.                                                                                                                                                                                                                                          |
| **Datenwiederherstellung und -erhaltung (NF3)**    | Ein Standardprogramm auf dem Raspberry Pi soll die kontinuierliche Sicherung der Daten gewährleisten, um die ungestörte Funktionalität der Blickbox zu sichern. <br> Die Daten puffern wir auf dem Pi, damit die Datenbank nur zur Darstellung in Grafana existiert. <br> Die Daten sollen dazu auf dem Raspberry Pi in einer Datei gespeichert werden. <br> Das Risiko des Verlierens der zeitabhängigen Daten soll so minimiert werden.                                                                              |
| **Bereitstellung einer geeigneten Umgebung (NF4)** | Die Hardware muss sowohl innerhalb als auch außerhalb der Blickbox an trockenen und sicheren Orten platziert werden. <br> Es sollen wetterfeste und isolierte Boxen verwendet werden, um die Hardware vor Umwelteinflüssen zu schützen und ihre Langlebigkeit zu unterstützen.                                                                                                                                                                                                                                         |
| **Bereitstellung eines Dashboards (NF5)**          | Die Daten der Datenbank sollen mit Grafana grafisch dargestellt werden. <br> Auf dem Dashboard sollen die Grafana-Grafen visualisiert werden und den Verbindungsstatus zur Datenbank sowie zur Blickbox angegeben werden. <br> Es soll nutzerfreundlich sein, um die Datenvisualisierung für Benutzer intuitiv zugänglich zu machen.                                                                                                                                                                                   |

## Randbedingungen

### Technisch

| **Randbedingungen**  | **Beschreibung**                                                             |
|----------------------|------------------------------------------------------------------------------|
| **Datenbank**        | Zur Datenbankpersistenz wird eine NoSQL-Datenbank wie InfluxDB verwendet.    |
| **Datenübertragung** | Die Wetterstation wird über das Internet (WLAN) mit einer API kommunizieren. |
| **Aufteilung**       | Frontend und Backend werden strikt getrennt.                                 |
| **Fremdsoftware**    | Open Source Bibliotheken dürfen verwendet werden.                            |
| **Wasserfestigkeit** | Jegliche Hardware muss Wasserfest installiert werden.                        |

### Organisatorisch

| **Randbedingungen**    | **Beschreibung**                                                                                                |
|------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Team**               | Vivian Berger, Maylis Grune, Max Müller und Aron Seidl.                                                         |
| **Zeitplan**           | Der Zeitplan wird auf 2 Monate vom 01.02.2024 - 28.03.2024 und 2 Monate von 09.08.2024 - 24.09.2024 festgelegt. |
| **Projektmanagement**  | Die Entwicklung folgt dem Scrum-Framework mit zweiwöchigen Sprints.                                             |
| **Definition of Done** | Entwickler folgen der DoD auf dem Git-Repository.                                                               |

## Kontextabgrenzung
### Fachlicher Kontext

| **Knoten**    | **Beschreibung**                                                |
|---------------|-----------------------------------------------------------------|
| **Fußgänger** | Fußgänger die sich die Blickbox anschauen und die Daten sehen.  |
| **Admin**     | Administriert Dashboards und steuert Blickbox manuell.          |
| **Blickbox**  | Enthält Sensor Hardware und Anzeige der Daten.                  |
| **Server**    | Externer Server der mit der Hardware der Blickbox kommuniziert. |
 
### Technischer Kontext

| **Knoten**         | **Beschreibung**                                                   |
|--------------------|--------------------------------------------------------------------|
| **Lichtsystem**    | Beleuchtet die Blickbox.                                           |
| **Sensorik**       | Hardware, welche die Messdaten sammelt.                            |
| **RaspberryPI**    | Verarbeitet die Sensorik Daten und schickt diese an die Datenbank. |
| **Visualisierung** | Gesammelte Daten werden angezeigt.                                 |
| **Datenbank**      | Speichert die Messdaten.                                           |
| **Webserver**      | Visualisiert die Messdaten und Stellt Frontend bereit.             |

## Lösungsstrategie


| **Ziel/Requirement**                                          | **Lösungsstrategie**                                | **Details**                                                                                                                                                                                                                                                 |
|---------------------------------------------------------------|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Alle funktionalen Requirements**                            | Eventgesteuerte Architektur                         | Sensorarchitektur sendet die Messdaten an dem PI. <br>Der PI sendet die Daten an den Webserver über das Internet, da LoraWan ineffizient ist. <br> Der Webserver speichert diese ab und stellt diese im Frontend da.                                        |       
| **Erweiterbarkeit & Wartung**                                 | Modularer Projektaufbau und Tests                   | Damit Dritte (Stakeholder, neue Entwickler, etc.), sich in das Projekt leicht einarbeiten können: <br> Codekomponenten sind voneinander getrennt aufgebaut. <br> Sie befinden sich in Modulen. <br> Zudem sind Funktionen getestet.                         |   
| **Sicherheit**                                                | Https-Verbindung, Containerisierung & Reverse-Proxy | Über den Reverse-Proxy sind die Verschiedenen Server-Apps nicht direkt dem Internet Exposed. <br>Durch die Containerisierung können die Komponenten innerhalb des Containers kommunizieren. <br> Die verschiedenen Ports können also verschlossen sein.     |   
| **Wiederherstellung und -erhaltung der Daten**                |                                                     | Auf dem Pi werden in einer history file, die daten abgelegt, damit man sollte die verbindung abbrechen, die noch seperat auf dem Pi sind.                                                                                                                   |   
| **Bereitstellung einer geeigneten Umgebung für die Hardware** | Box                                                 | SARA wird in einer Box einbaut, welche Wasserdicht ist. <br>Durch eine eigene Batterie ist sie Autak und braucht keine Spannung von außen. <br> Die Sensoren werden über Kabelverschraubung in den Innenraum der Box gebraucht dadurch ist sie Wasserdicht. |   
| **Bereitstellung eines Dashboard**                            | Grafana als Open-Source Fertiglösung                | Das erlaubt eine einfache Darstellung der Messdaten mit direkter Datenbank-anbindung, sowie eine einfache Verknüpfung mit dem Frontend.                                                                                                                     |   

## Bausteinsicht

Erstmal nur bis hier

## Laufzeitsicht

## Verteilungssicht

## Querschnittliche Konzepte

## Architekturentscheidungen

### Evaluation zur Wahl des Frontend-Frameworks des Clients

Der Client zur Anzeige und Aufbereitung der Sensordaten wird unter dem
Arbeitstitel *Valentin* (Komposita aus *Value* und *Notification*)
geführt. Vor der Initialisierung von *Valentin* muss ein geeignetes
Framework gewählt werden. Die nachfolgende Nutzwertanalyse dient dafür
als Entscheidungsgrundlage.


Die Auswahl zum Framework innerhalb des *Valentin* Client Aufbaus viel
auf *React*. *React* ist eine JavaScript-Bibliothek von Facebook für die
Entwicklung von interaktiven, komponentenbasierten Benutzeroberflächen.
Sie ermöglicht eine effiziente Aktualisierung des DOM und eine
verbesserte Leistung durch die Verwendung einer virtuellen
DOM-Repräsentation.

## Qualitätsanforderungen

### Qualitätsbaum

### Qualitätsszenarien

## Risiken und Teschnische Schulden

