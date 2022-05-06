# Aufgabe 4 (10 Punkte)

- Wenden Sie Ihre Implementierung auf die zur Aufgabe gehörenden Testbilder an (siehe ILIAS).

- Visualisieren Sie Ihre Ergebnisse mit der OpenCV-Funktion imshow() auf dem Bildschirm, und
fügen Sie die Ergebnisse Ihrer Ausarbeitung hinzu.

- Beachten Sie auch die allgemeinen Hinweise zur Abgabe (siehe Praktikumsordner im ILIAS).  

Implementieren Sie einen Canny-Kantendetektor mit den folgenden Schritten:  

### (a) Glättung mit Gaußfilter (2 Punkte)  
Implementieren Sie die Berechnung einer Filtermatrix für einen Gaußfilter mit folgenden Parametern
- Die Standardabweichung σ ist als Fließkommazahl einstellbar ist.
- Die Größe der (2N+1,2N+1) Filtermaske ist einstellbar
Beachten Sie, das die Filtersumme auf 1 normiert wird.  

Nutzen Sie bei der Erstellung der Filtermatrix aus, dass der Gaußfilter separierbar ist. Verwenden Sie die
OpenCV-Funktion filter2D() für die Filterung mit ihrer Filtermatrix.  

### (b) Kanten finden (2 Punkt)  
Implementieren sie eine Gradientenberechnung, die als Ergebnis eines Eingangsbildes jeweils ein
Ergebnisbild für den Gradientenbetrag und für die Gradientenrichtung liefert. Verwenden Sie die
OpenCV-Funktion filter2D() für die Berechnung des Gradienten – z.B. mit Sobelfiltern.  

### (c) Kanten ausdünnen (Non-maxima-suppression) (3 Punkte)  
Implementieren Sie eine Non-maxima-suppression, welche als Eingabebilder ein Bild für den
Gradientenbetrag und ein Bild für die Gradientenrichtung bekommt, und als Ergebnis ein ausgedünntes
Gradientenbild (Betrag) liefert.  

### (d) Zusammengehörende Kanten finden (Hysterese) (3 Punkte)  
Implementieren Sie eine Hysterese, welche als Eingabe ein Gradientenbild (Betrag) und zwei
Schwellenwerte bekommt. Als Ergebnis wird ein Bild mit zusammengehörenden Kanten entsprechen
der Schwellenwerte geliefert.