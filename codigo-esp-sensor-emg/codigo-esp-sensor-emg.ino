// Variables para el filtrado exponencial
float emgFiltrado = 0.0;
float N = 5.0;  // Constante de suavizado

const int pinEMG = 34; // Pin de entrada analógica (GPIO 35)

void setup() {
  analogReadResolution(12); // ADC de 12 bits (0–4095 en ESP32)
  pinMode(pinEMG, INPUT);
  Serial.begin(115200);
}

void loop() {
  int lecturaRaw = analogRead(pinEMG); // Lectura cruda del EMG

  // Aplicación del filtro exponencial (media móvil)
  emgFiltrado = emgFiltrado * (N - 1) / N + lecturaRaw / N;

  // Mostrar por serial
  Serial.println(emgFiltrado);

  // Pausa de 50 milisegundos (~20 Hz de muestreo)
  delay(50);
}
