import serial
import time

# Verbindung herstellen (angepasst je nach Ihrem Setup)
ser = serial.Serial('COM5', 115200) # Anpassen Sie den Port und die Baudrate entsprechend

try:
    while True:
        # Daten vom Benutzer eingeben
        data_to_send = input("Enter data to send: ")
        
        # Daten an Arduino senden
        ser.write(data_to_send.encode())
        
        # Kurze Verzögerung, um Zeit für die Verarbeitung auf Arduino-Seite zu geben
        time.sleep(0.3)
        
        # Antwort vom Arduino lesen
        response = ser.readline().decode().strip()
        print("Response from Arduino:", response)
        ser.flush()

except KeyboardInterrupt:
    ser.close()
    print("Program terminated.")