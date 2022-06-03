# Aufgabe 7 (10 Punkte)

- Wenden Sie Ihre Implementierung auf die zur Aufgabe gehörenden Testbilder an (siehe ILIAS).
- Visualisieren Sie Ihre Ergebnisse mit der OpenCV-Funktion imshow() auf dem Bildschirm, und
fügen Sie die Ergebnisse Ihrer Ausarbeitung hinzu.
- Beachten Sie auch die allgemeinen Hinweise zur Abgabe (siehe Praktikumsordner im ILIAS).

## Teil 1. Template Matching (5 Punkte)
Implementieren Sie ein Template Matching mit unterschiedlichen Ähnlichkeitsmaßen und visualisieren
Sie die Positionen der gefundenen Matches im Bild. Referenzbild und Templatebild finden Sie in ILIAS.  
### (a) Ähnlichkeitsmaße
Implementieren Sie folgende Ähnlichkeitsmaße, die beim Template Matching verwendet werden sollen:  
- Sum of squared differences (SSD)
- Korrelationskoeffizient (COR)

### (b) Suchstrategie im Bild
Implementieren Sie für das Template Matching einen Brute force Ansatz, der an jeder Stelle des Bildes nach Übereinstimmungen mit dem Template sucht. Berechnen Sie die Ergebnisse für beide Ähnlichkeitsmaße. Eine Randbehandlung muss nicht vorgenommen werden. Unterteilen Sie Ihre Lösung in folgende Schritte:
1. Ähnlichkeiten pro Pixel berechnen und in einem Bild speichern
2. Suche nach Bereichen mit größter Ähnlichkeit in diesem Bild
3. Visualisierung der Ergebnisse für die implementierten Ähnlichkeitsmaße
## Teil 2. Harris Corner Detektor (5 Punkte)
Implementieren Sie einen Harris Corner Detektor, wie er in der Vorlesung vorgestellt wurde. Unterteilen Sie Ihre Lösung in folgende Schritte:  
1. Berechnung des Stukturtensors und Glättung der einzelnen Einträge mit einem Gaußfilter
2. Berechnung der Corner Reponse Funktion (typische Werte für 𝛼: 𝛼 ∈ [0.04,0.06])
Verwenden Sie für die Berechnung nicht det() oder trace() aus der numpy-Bibliothek.
3. Punkte ausdünnen
    1. Thresholding (typische Werte: 20 000)
    2. Non-maxima Unterdrückung auf einer sortierten Liste der Kandidaten (typische Werte für Umgebungsradius: 10)