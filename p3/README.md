# Aufgabe 3 (10 Punkte)

-   Wenden Sie Ihre Implementierung auf die zur Aufgabe gehörenden Testbilder an (siehe ILIAS).
-   Visualisieren Sie Ihre Ergebnisse mit der OpenCV-Funktion imshow() auf dem Bildschirm, und
    fügen Sie die Ergebnisse Ihrer Ausarbeitung hinzu.
-   Beachten Sie auch die allgemeinen Hinweise zur Abgabe (siehe Praktikumsordner im ILIAS).

## Teil 1. Lineare Filter (6 Punkte)

Implementieren Sie eine lineare Filterung für eine Filtermatrix der Größe (2N+1,2N+1). Nutzen Sie Ihre
Implementierung um damit das Testbild zu filtern.

Untergliedern Sie Ihre Lösung in die Schritte:

(a) Implementierung einer Methode für die lineare Filterung mit Filtermaske der Größe (2N+1,2N+1).

-   Die Größe der Maske ist über einen Parameter wählbar (nur ungerade Größen)

-   Keine Filterung am Rand

(b) Filtern Sie das Testbild mit einem Binomialfilter der Größe (2N+1,2N+1) für N=1,2  
Hinweise:

-   Schreiben Sie eine Methode, mit der die Filtermaske erstellt wird
-   Nutzen Sie für die Erstellung der Filtermaske die NumPy-Funktion poly1d. Ein 1D
    Binomialfilter der Ordnung p berechnet sich wie folgt:
    (np.poly1d([0.5, 0.5])\*\*p).coeffs

## Teil 2. Gewichteter Medianfilter (4 Punkte)

Schreiben Sie eine Methode, die einen gewichteten Medianfilter implementiert, wie er in der Vorlesung
vorgestellt wurde. Übergabe der Methode ist das zu filternde Bild sowie eine Gewichtsmatrix W der
Größe (2N+1,2N+1). Nutzen Sie Ihre Implementierung um damit das Testbild mit N=1 zu filtern.
