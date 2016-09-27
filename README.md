# krebsregister_parser
## Was, wie, wo?
Der Datenexport des Krebsregister NRW ist etwas eigen. Dieses kleine Python-Programm kann aktuell den HTML-output von "Fallzahlen, aufgeschlÃ¼sselt nach Altersgruppen und Jahren" mit Aggregation: 1 und Geschlechter: beide in JSON und tab-delimited .txt exportieren.

Tests und Anpassungen für andere Anfragen folgen eventuell später.

## Abhängigkeiten
- beautifulsoup4

## Benutzung
```
pip3 install -r requirements.txt
```
```
python3 main.py inputfile.html
```
oder
```
python3 main.py < inputfile.html
```
## Lizenz
MIT License (fulltext see LICENSE.md)
