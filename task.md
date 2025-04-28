## Beleg-Teilaufgabe zur Monte-Carlo-Simulation

### Aufgabenstellung
Entwickeln Sie eigenständig ein Modell zur Monte-Carlo-Simulation eines kleinen Geschäftes oder einer Fabrik in Anlehnung an das Beispiel zum Eisgeschäft aus der Vorlesung.

Als generelle Bedingungen zur Auswahl des Untersuchungsobjektes seien definiert:
- Das Objekt muss eine zeitliche Änderung des Basisparameter (Kundenzahl, Umsatz etc.) über das Jahr haben und zum Beispiel von der mittleren Temperatur oder vom Monat oder der Jahreszeit abhängig sein. Die Änderungen selbst MÜSSEN JEDOCH UNAABHÄNIG voneinander sein!
- Auch der eigentliche Prozess pro Kunde oder Bestellung muss zumindest teilweise zufällig sein (egal ob bei Bademoden oder Glühwein meist als Funktion der Temperatur)
- Definieren Sie relevante Fragestellungen und Bewertungsparameter und leiten sie davon eine Zielfunktion ab (vgl. Vorlesungen dazu!)


### Mögliche Beispiele für die Objektauswahl könnten sein:
- ein kleines Geschäft für Eis, Imbiss oder Getränke mit zufällig kommenden Kunden und zufälligem Umsatz, Zielfunktion: maximaler Profit
- die Anrufe bei einer Hotline mit zufälligen Anrufhäufigkeiten und zufälligen Anrufdauern, Zielfunktion: zu ermittelndes Optimum aus Mitarbeiteranzahl im Callcenter (=Kosten) und Kundenzufriedenheit = f( -Wartezeit ) als Schleife über 1…N-MA
- das Verhalten der Konkurrenz bei Investition (vgl. Szenarien aus VL) ein Standard-Internetserver unter schwerer Nachfrage (bei traditionellen Apache-Servern max. 250 Requests gleichzeitig), Zielfunktion: Optimum aus Kosten für Serverfarm und Kundenzufriedenheit (kein oder kaum „Too much requests …“ { mit >> 5 Server}

Sie müssen nur genau eine Aufgabe bzw. Beispiel umsetzen!!!


### Dokumentation
Dokumentieren Sie sowohl die gewählte Aufgabenstellung und auch die Ergebnisse auf mindestens einer A4-Seite so, als wäre es ein Abschlussbericht für den Leiter der Firma oder den Verantwortlichen des Prozesse oder Gerätes. Bitte vermerken Sie Ihren Namen als Ersteller des Berichtes.
Sie müssen dabei keine langen Sätze schreiben, sondern es reichen auch Stichpunkte oder Tabellen zu den Ergebnissen. Ich selbst bevorzuge prägnante grafische Darstellungen, wo man auf einem Blick die Probleme oder Sinnhaftigkeit des Invest-Vorhabens oder Bitte kopieren Sie den Programmcode der Monte-Carlo-Simulation in den Anhang des Berichtes oder senden Sie das Projekt als ZIP (wegen Spamfilter bitte möglichst KEINE EXE-Dateien oder dann ZIP-Extension umbenennen und in Email vermerken …) mit.