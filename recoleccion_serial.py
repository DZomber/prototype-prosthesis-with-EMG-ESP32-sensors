import serial
import csv
import time

# CONFIGURA ESTO SEGÚN TU CASO
puerto = 'COM14'  # Cambia esto según el puerto real de tu ESP32
baudrate = 115200
archivo_csv = "hand.csv"

# Movimientos a capturar (puedes incluir "reposo" si lo usas)
movimientos = ["dedo1", "dedo2", "dedo3", "dedo4", "dedo5", "mano"]

# Solicitar número de muestras
try:
    num_muestras = int(input("¿Cuántas muestras quieres por movimiento?: "))
    assert num_muestras > 0
except:
    print("❌ Ingresa un número válido.")
    exit()

# Diccionario de datos
datos = {mov: [] for mov in movimientos}

# Intentar conexión serial
try:
    ser = serial.Serial(puerto, baudrate, timeout=1)
    time.sleep(2)
    print("✅ Conexión con ESP32 establecida.")
except:
    print(f"❌ No se pudo abrir el puerto {puerto}.")
    exit()

# Captura de datos por clase
for mov in movimientos:
    input(f"\n🔄 Prepara el movimiento '{mov}' y presiona Enter para comenzar...")
    print(f"🎯 Capturando {num_muestras} muestras para '{mov}'...")

    contador = 0
    while contador < num_muestras:
        if ser.in_waiting > 0:
            linea = ser.readline().decode().strip()
            try:
                valor = float(linea)  # ACEPTA VALORES CON DECIMALES
                datos[mov].append(valor)
                print(f"{mov}: {valor}")
                contador += 1
            except ValueError:
                pass  # Ignora líneas inválidas

ser.close()
print("\n✅ Captura completa. Guardando archivo...")

# Guardar CSV
with open(archivo_csv, mode='w', newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(movimientos)
    for i in range(num_muestras):
        fila = [datos[mov][i] for mov in movimientos]
        writer.writerow(fila)

print(f"\n📁 Archivo guardado como: {archivo_csv}")
