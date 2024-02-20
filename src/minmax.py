import cv2
import numpy as np

# Lade das Bild
image = cv2.imread('src/bild.jpg')

# Konvertiere das Bild in den HSV-Farbraum
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)



# Extrahiere den Farbton (Hue) aus dem Bild
hue_channel = hsv_image[:, :, 0]

print(hue_channel)

# Finde den minimalen und maximalen Farbton im Bild
min_hue = np.min(hue_channel)
max_hue = np.max(hue_channel)

print(f'Minimaler Farbton: {min_hue}')
print(f'Maximaler Farbton: {max_hue}')

# Zeige das ursprüngliche Bild und das Ergebnis an

import cv2
import numpy as np

# Lade das Bild
image = cv2.imread('src/bild.jpg')

# Konvertiere das Bild in den HSV-Farbraum
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definiere den Farbbereich für Hellblau
lower_color = np.array([90, 50, 50])
upper_color = np.array([120, 255, 255])

# Erstelle eine Maske basierend auf dem Farbbereich
mask = cv2.inRange(hsv_image, lower_color, upper_color)

# Wende die Maske auf das Originalbild an, um nur die erkannten Farben zu behalten
result = cv2.bitwise_and(image, image)

# Berechne den Durchschnitt der Farbe in der erkannten Region
average_color = cv2.mean(result)
print(average_color)

# Konvertiere den Durchschnitt in den BGR-Farbraum
average_color_bgr = np.uint8([[average_color]])

print(average_color_bgr)


print(f'Durchschnittliche Farbe: BGR({average_color_bgr[0][0][0]}, {average_color_bgr[0][0][1]}, {average_color_bgr[0][0][2]})')
# Zeige das ursprüngliche Bild, das Ergebnis und die durchschnittliche Farbe an



# Zeige die durchschnittliche Farbe als Text aus
