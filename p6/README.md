# Aufgabe 6 (10 Punkte)

- Wenden Sie Ihre Implementierung auf die zur Aufgabe gehörenden Testbilder an (siehe ILIAS).  
- Visualisieren Sie Ihre Ergebnisse mit der OpenCV-Funktion imshow() auf dem Bildschirm, und
fügen Sie die Ergebnisse Ihrer Ausarbeitung hinzu.  
- Beachten Sie auch die allgemeinen Hinweise zur Abgabe (siehe Praktikumsordner im ILIAS).  
## Teil 1. Morphologische Operatoren (5 Punkte)
Entfernen Sie die Störungen in dem gegebenen Testbild durch eine Closing-Operation mit einem
geeigneten Strukturelement. Implementieren Sie dazu jeweils eine Dilatation sowie eine Erosion auf
Binärbildern.  
Das Strukturelement soll als Parameter übergeben werden. Es sollen lediglich
symmetrische Strukturelemente mit ungerader Größe betrachtet werden.  

## Teil 2. Segmentierung mit OpenCV (5 Punkte)
Nutzen Sie die Implementierung der Wasserscheidentransformation aus der OpenCV-Bibliothek um die
im Testbild unten dargestellten Objekte automatisch (ohne Benutzerinteraktion) zu segmentieren.  
Nutzen Sie weitere Methoden der OpenCV-Bibliothek für eine geeignete Vorverarbeitung. Jedes Objekt
soll im Ergebnis eine eigene ID erhalten.  