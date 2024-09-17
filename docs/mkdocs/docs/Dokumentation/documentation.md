---
date: Januar 2023
title: "Blickbox Dokumentation"
---

# Dokumentation

## Stakeholder

Ein umfassender Überblick über die Stakeholder des Systems ist von
entscheidender Bedeutung. Dies bezieht sich auf sämtliche Personen,
Rollen oder Organisationen, die entweder die Architektur des Systems
kennen sollten oder von dieser überzeugt werden müssen. Zu den
Stakeholdern zählen auch jene, die aktiv mit der Architektur oder dem
Code arbeiten, beispielsweise indem sie Schnittstellen nutzen. Ebenso
gehören Personen dazu, die die Dokumentation der Architektur benötigen,
um ihre eigene Arbeit effizient zu gestalten. Darüber hinaus sind
Stakeholder involviert, die Entscheidungen über das System und dessen
Entwicklung treffen. Die nachfolgende Analyse zeigt alle Stakeholder
gebündelt in ihren Gewichtungen und Beziehungen.


## Anforderungskonzept

Die Anforderungen an die Umsetzung des Blickbox-Projekts werden in die
Kategorien funktionale, nicht funktionale und hypothetische
Anforderungen unterteilt. Diese Differenzierung ermöglicht eine
umfassende Abdeckung aller Aufgabenstellungen im Zusammenhang mit der
Umsetzung des Blickbox-Projekts.

### Funktionale Anforderungen (FA)

Funktionale Anforderungen beschreiben spezifisch die konkreten Zwecke,
die das zu entwickelnde Produkt erfüllen soll.

### Nicht funktionale Anforderungen (NFA)

Im Gegensatz zu funktionalen Anforderungen sind nicht-funktionale
Anforderungen eher allgemein gehalten und betreen die gesamte
Architektur und das Design des Produkts. Sie können auf verschiedene
Projekte angewendet werden.

### Hyptohetische Anforderungen (HFA)

Hypothetische Anforderungen werden aufgrund von unsicheren Ergebnissen
und vorherigen Abhängigkeiten definiert. Ihr Zweck besteht darin,
mögliche Entscheidungen und Eventualitäten abzudecken, die eintreten
können oder auch nicht.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
**Datenerfassung und -übertragung (FA1)**
Beschreibung: Das IOT-System muss in der Lage sein, kontinuierlich Sensordaten zu erfassen. Diese Daten sollen in der Sensoreinheit eingelesen und im Raspberry PI gespeichert und verarbeitet werden. Die Datenübertragung auf den Server erfolgt Event-gesteuert und drahtlos über einen http-Client. Die Daten werden in festgelegten Intervallen im JSON-Format übertragen und in der Datenbank festgehalten.
**Interaktivität zu Dritten (FA2)**
Beschreibung: Der Blickbox soll attraktiver werden und Fußgänger sollen mit ihm interagieren können. Das soll in Form eines Displays oder Ton und Licht geschehen. Ein Display soll in der Lage sein, Dritten aktuelle Daten aus der Datenbank wie etwa das Wetter anzuzeigen. Bei Dunkelheit sollen Bewegungsmelder Lichter aktivieren.
**Containerisierung (FA3)**
Beschreibung: Die Anwendungen sollen in Containern gekapselt werden, um eine verbesserte Portabilität und Skalierbarkeit zu gewährleisten. Es wird die Container-Technologien Docker verwendet werden, um die Anwendungen effizient zu verwalten und zu deployen.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
**Erweiterbarkeit und Wartung (NF1)**
Beschreibung: Die Architektur und Dokumentation des Systems sollen leicht zugänglich sein, um Erweiterungen und Verbesserungen der Features zu erleichtern. Eine klare Dokumentation sowie ein vereinfachter Hardwareaufbau sollen die Wartung und Erweiterbarkeit des Systems unterstützen.
**Sicherheit (NF2)**
Beschreibung: Die Verbindung zum Server soll verschlüsselt sein, um die Sicherheit der übertragenen Daten zu gewährleisten. Es müssen geeignete Verschlüsselungsprotokolle und Sicherheitsmaßnahmen implementiert werden, um die Vertraulichkeit und Integrität der Daten zu schützen.
**Datenwiederherstellung und -erhaltung (NF3)**
Beschreibung: Ein Standardprogramm auf dem Raspberry Pi soll die kontinuierliche Sicherung der Daten gewährleisten, um die ungestörte Funktionalität der Blickbox zu sichern. Die Daten puffern wir auf dem Pi, damit die Datenbank nur zur Darstellung in Grafana existiert. Die Daten sollen dazu auf dem Raspberry Pi in einer Datei gespeichert werden. Das Risiko des Verlierens der Daten soll so minimiert werden.
**Bereitstellung einer geeigneten Umgebung für die Hardware (NF4)**
Beschreibung: Die Hardware muss sowohl innerhalb als auch außerhalb der Blickbox an trockenen und sicheren Orten platziert werden. Es sollen wetterfeste und isolierte Boxen verwendet werden, um die Hardware vor Umwelteinflüssen zu schützen und ihre Langlebigkeit zu gewährleisten.
**Bereitstellung eines Dashboard (NF5)**
Beschreibung: Die Daten der Datenbank sollen mit Grafana grafisch dargestellt werden. Auf dem Dashboard sollen die Grafana-Grafen visualisiert werden und den Verbindungsstatus zur Datenbank sowie zur Blickbox angegeben werden. Es soll nutzerfreundlich sein, um die Datenvisualisierung für Benutzer intuitiv zugänglich zu machen.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Randbedingungen

### Technisch

Randbedingung      Beschreibung
  ------------------ ------------------------------------------------------------------------------
Datenbank          Zur Datenbankpersistenz wird eine NoSQL-Datenbank wie InfluxDB verwendet.
Datenübertragung   Die Wetterstation wird über das Internet (WLAN) mit einer API kommunizieren.
Aufteilung         Frontend und Backend werden strikt getrennt.

Fremdsoftware      Opensource Bibiliotheken dürfen verwendet werden.

Wasserfestigkeit   Jegliche Hardware muss Wasserfest implementiert werden.

### Organisatorisch

Randbedingung        Beschreibung
  -------------------- ------------------------------------------------------------------------
Team                 Vivian Berger, Maylis Grune, Max Müller und Aron Seidl
Zeitplan             Der Zeitplan wird auf 2 Monate vom 01.02.2024 - 28.03.2024 festgelegt.

Projektmanagement    Die Entwicklung folgt dem Scrum-Framework mit zweiwöchigen Sprints.
Definition of Done   Entwickler folgen der DoD auf dem Git-Repository.

## Kontextabgrenzung

### Fachlicher Kontext

Knoten      Beschreibung
  ----------- -----------------------------------------------------------------
Fußgänger   Fußgänger die sich die Blickbox anschauen und die Daten sehen.
Admin       Administriert Dashboards und stuert Blickbox manuell.

Blickbox    Enthält Sensor Hardware und Anzeige der Daten.

Server      Externer Server der mit der Hardware der Blickbox kommuniziert.

### Technischer Kontext

Knoten           Beschreibung
  ---------------- --------------------------------------------------------------------
Lichtsystem      Beleuchtet die Blickbox.
Sensorik         Hardware welche die Messdaten sammelt.

RaspberryPI      Verarbeitet die Sensorik Daten und schickt diese an die Datenbank.
Visualisierung   Gesammelte Daten werden angezeigt.
Datenbank        Speichert die Messdaten.
Webserver        Visualisiert die Messdaten und Stellt Frontend bereit.

## Lösungsstrategie

Ziel / Requirement                                          Lösungsstrategie                                      Details
  ----------------------------------------------------------- ----------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Alle funktionalen Requirements                              Eventgesteuerte Architektur                           Sensorarchitektur sendet die Messdaten an dem PI. Der PI sendet die Daten an den Webserver über das Internet, da LoraWan ineffizient ist. Der Webserver speichert diese ab und stellt diese im Frontend da.

Erweitbarkeit & Wartung                                     Modularer Projektaufbau und Tests                     Damit Dritte, sei es irgendwelche Stakeholder oder neue Entwickler, sich in das Projekt leicht einarbeiten können, bauen wir das Projekt so auf, dass Codecomponenten voneinander getrennt aufgebaut sind, sich also in Modulen befinden. Zudem sind Funktionen getestet.

Sicherheit                                                  Https-Verbindung, Containerisierung & Reverse-Proxy   Über den Reverse-Proxy sind die Verschiedenen Server-Apps nicht direkt dem Internet Exposed. Durch die Containersierung können die Komponenten innerhalb des Containers kommunizieren. Die verschiedenen Ports können also verschlossen sein.

Wiederherstellung und -erhaltung der Daten                                                                        Auf dem Pi werden in einer history file, die daten abgelegt, damit man sollte die verbindung abbrechen, die noch seperat auf dem Pi sind.

Bereitstellung einer geeigneten Umgebung für die Hardware   Box                                                   SARA wird in einer Box einbaut, welche Wasserdicht ist. Durch eine eigene Batterie ist sie Autak und braucht keine Spannung von außen. Die Sensoren werden über Kabelverschraubung in den Innenraum der Box gebraucht dadurch ist sie Wasserdicht.

Bereitstellung eines Dashboard                              Grafana als Open-Source Fertiglösung                  Das erlaubt eine einfache Darstellung der Messdaten mit direkter Datenbank-anbindung, sowie eine einfache Verknüpfung mit dem Frontend.

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

