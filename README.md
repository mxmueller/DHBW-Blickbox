## Board
https://taiga-dhhdhai-u11685.vm.elestio.app/project/gruppe-1-iot/backlog

## Git Workflow
1. **Sprint-basierte Entwicklung:**
   - Für jeden Sprint wird eine eigene Sprint-Branch erstellt.
   - Am Ende jedes Sprints wird der Sprint-Branch in den Master-Branch gemerged.

2. **Story-Branches:**
   - Jede Story erhält einen eigenen Branch, abgeleitet vom Sprint-Branch.
   - Die Benennung erfolgt nach dem Schema: `#id-name`.

3. **Commits:**
   - Sprache: Deutsch
   - Innerhalb der Story-Branches werden für jeden Task oder mehrere Tasks separate Commits durchgeführt.
   - Die Commit-Nachricht enthält die IDs der zugehörigen Tasks und den Namen der Änderung im Format: `#id_#id2_#id3-name`.

5. **Abschluss einer Story:**
   - Nach Abschluss einer Story wird der entsprechende Branch sowohl lokal als auch remote vom Entwickler gelöscht.

6. **Merge und Approvals:**
   - Vor dem Merge einer Story in den Sprint-Branch muss mindestens ein Approver die Änderungen genehmigen.


## Definition of done (Dod)

Im Team wurden die folgenden Kriterien definiert, damit eine Aufgabe oder ein Produkt als abgeschlossen gilt:
1. **Code-Review:** Der Code wurde von mindestens einem Teammitglied überprüft.

2. **Unit-Tests:** Es wurden ausreichende Unit-Tests geschrieben, und alle Tests sind erfolgreich durchgelaufen.

3. **Integrationstests:** Der Code wurde erfolgreich in den Hauptentwicklungszweig integriert, und alle Integrationstests sind bestanden.

4. **Dokumentation:** Alle relevanten Code-Änderungen wurden in der Projektdokumentation aktualisiert. Ergo sollten spezielle Diagramme erstellt worden sein, müssen diese auch von dem jeweiligen Entwickelnden im Arc42 erläutert und implementiert werden.

5. **Benutzerdokumentation:** Falls erforderlich, wurde die Benutzerdokumentation aktualisiert.

6. **Code-Stil:** Der Code entspricht den vereinbarten Code-Standards und Best Practices.

7. **Performance-Überprüfung:** Die Performance des Codes wurde überprüft und erfüllt die definierten Anforderungen.

8. **Sicherheitsprüfung:** Falls relevant, wurden Sicherheitsprüfungen durchgeführt und alle Sicherheitsanforderungen sind erfüllt.

9. **Akzeptanzkriterien:** Alle in den Akzeptanzkriterien definierten Anforderungen sind erfüllt.

10. **Review mit dem Product Owner:** Der Product Owner hat das Ergebnis überprüft und akzeptiert.

Die DoD wird regelmäßig überprüft und bei Bedarf aktualisiert, um sicherzustellen, dass sie den aktuellen Anforderungen entspricht.


## Rollen
**Dokumentation** 
- Release Notes (Aron, Max)
- Diagramme allg.  / UML (May)
- arc42 (LaTeX) pflegen (Vivi, Aron)

**PO/Scrum** (Max)
- Moderation Freitagsmeeting 
- Showcase der Demo
- Backlog pflegen
- Sprinttermine legen

**Techlead Hardware** (May, Vivi)

**Techlead Client**
- Frontend (Max)
- Backend (Aron)

**Techlead Infrastruktur**
- Server (Webserver für Client) (Max)
- WLAN 
- Sensordaten (May)


## Releases
Die Releases erfolgen innerhalb der Sprintwechsel. Als Dokumentation dienen die Releasnotes innerhalb der Git-Releases.


## Releases
Die Releases erfolgen innerhalb der Sprintwechsel. Als Dokumentation dienen die Releasnotes innerhalb der Git-Releases.


