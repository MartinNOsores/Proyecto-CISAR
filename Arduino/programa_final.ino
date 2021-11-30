#include <stdio.h>
//#include <Adafruit_CircuitPlayground.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <MAX30105.h>
#include <spo2_algorithm.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
MAX30105 particleSensor;

byte MLXAddr = 0x5A<<1;
float medicion;
const int Trigger = 2;   
const int Echo = 3;   
//int luzroja = 7;
//int luzverde = 8;

// ----> COMUNICACION RASPBERRY
int flag_temp = 5;

// ----> RELAYS
int relay_generadorozono = 15;
int relay_coolers = 14;
int relay_bombarociador = 17;
int relay_lucesled = 16;

int sensorInflarojo = 4;
int a = 0; 
const int maxtemp = 37.5;

#define MAX_BRIGHTNESS 255

#if defined(_AVR_ATmega328P) || defined(AVR_ATmega168_)
//Arduino Uno doesn't have enough SRAM to store 100 samples of IR led data and red led data in 32-bit format
//To solve this problem, 16-bit MSB of the sampled data will be truncated. Samples become 16-bit data.
uint16_t irBuffer[100]; //infrared LED sensor data
uint16_t redBuffer[100];  //red LED sensor data
#else

uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
#endif

int32_t bufferLength; //data length
int32_t spo2; //SPO2 value
int8_t validSPO2; //indicator to show if the SPO2 calculation is valid
int32_t heartRate; //heart rate value
int8_t validHeartRate; //indicator to show if the heart rate calculation is valid
byte pulseLED = 11; //Must be on PWM pin
byte readLED = 13; //Blinks with each data read

void setup() {
  Serial.begin(9600);
  Serial.println(" \n<-- Inicializando Monitor Serial --> \n ");
  mlx.begin();
  pinMode(Trigger, OUTPUT); 
  pinMode(Echo, INPUT);  
  pinMode(relay_generadorozono, OUTPUT);
  pinMode(relay_coolers, OUTPUT);
  pinMode(relay_bombarociador , OUTPUT);
  pinMode(relay_lucesled , OUTPUT);
  //pinMode(flagtemp, OUTPUT);
  pinMode(sensorInflarojo, INPUT);
  pinMode(pulseLED, OUTPUT);
  pinMode(readLED, OUTPUT);
  //pinMode(rociador, OUTPUT);
  //pinMode(luzroja, OUTPUT);
  //pinMode(luzverde, OUTPUT);
  delay(2000);
  
  digitalWrite(relay_generadorozono, HIGH);
   digitalWrite(relay_coolers , LOW); 
   digitalWrite(relay_bombarociador , LOW); 
   digitalWrite(relay_lucesled , LOW);
  digitalWrite(Trigger, LOW);
  delay(1000);

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println(F("MAX30105 was not found. Please check wiring/power."));
    while (1);
  }
}

void loop(){
  
  long t; //tiempo que demora en llegar el eco
  long d; //distancia en centimetros

  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);
  
  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = t/59;             //escalamos el tiempo a una distancia en cm
  
  Serial.print("Distancia: ");
  Serial.print(d);      //Enviamos serialmente el valor de la distancia
  Serial.print("cm");
  Serial.println();
  delay(100);

  if (d < 170){
    medirTemperatura();
   }
   }
 void permitirIngreso() {
    digitalWrite(relay_coolers , HIGH);
    digitalWrite(relay_lucesled , HIGH);
    
    digitalWrite(relay_generadorozono, HIGH);
    delay(3000);
    digitalWrite(relay_generadorozono, LOW);

    delay(12000);
    digitalWrite(relay_coolers , LOW);
    digitalWrite(relay_lucesled , LOW);

    // AVISARLE A LA RASPBERRY QUE SALÍO LA PERSONA   
    }
 
void medirTemperatura(){                                                                    
  Wire.begin(15);
  int i=0;
  while(i<5){
    i= i + 1;
    delay (3000); // damos un tiempo para medirse la temp. de 3 seg.
    float medicion = mlx.readObjectTempC();
    float medicion_corregida = medicion * 1.152; //calibramos la medición de temperatura mediante un factor
    
    Serial.println("Temperatura: ");
    Serial.print(mlx.readObjectTempC());
    Serial.println("Cº");
  }
    delay(1000);
  
    if ( medicion > 20 && medicion <40) {
    Serial.println("\nComenzando medicion de la saturacion\n");
    delay(1000);
    
    medirsaturacion();
      }
    else {
      exit;
    //mandarle un 1 a la raspberry

      }    
}

void medirDistanciaRociador(){
  delay(5000); //damos un tiempo de 5 seg.
  int flag = 1; 
 while (flag) {
 
  if (digitalRead(sensorInflarojo) == LOW){     
      Serial.println("\nObstaculo Detectado\n");
      digitalWrite(relay_bombarociador, HIGH);
      delay(1000);
      digitalWrite(relay_bombarociador, LOW);
      flag = 0;
      }}

      permitirIngreso();
     
  }

  void medirsaturacion(){
  Wire.begin(24) ;
  Serial.read();

  byte ledBrightness = 60; //Options: 0=Off to 255=50mA
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings
  
  delay(5000); // damos un retardo de 5 seg.
  int contador = 0;
  bufferLength = 100; //buffer length of 100 stores 4 seconds of samples running at 25sps

  //read the first 100 samples, and determine the signal range
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //do we have new data?
      particleSensor.check(); //Check the sensor for new data

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); //We're finished with this sample so move to next sample

    Serial.print(F("red="));
    Serial.print(redBuffer[i], DEC);
    Serial.print(F(", ir="));
    Serial.println(irBuffer[i], DEC);
  }

  //calculate heart rate and SpO2 after first 100 samples (first 4 seconds of samples)
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

    //dumping the first 5 sets of samples in the memory and shift the last 75 sets of samples to the top
    for (byte i = 25; i < 30; i++)
    {
      redBuffer[i - 25] = redBuffer[i];
      irBuffer[i - 25] = irBuffer[i];
    }
    
    //take 1 set of sample before calculating the heart rate.
    for (byte i = 75; i < 80; i++)
    {
      while (particleSensor.available() == false) //do we have new data?
        particleSensor.check(); //Check the sensor for new data

      digitalWrite(readLED, !digitalRead(readLED)); //Blink onboard LED with every data read

      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();
      particleSensor.nextSample(); //We're finished with this sample so move to next sample

      //send samples and calculation result to terminal program through UART
      Serial.print(F("red="));
      Serial.print(redBuffer[i], DEC);
      Serial.print(F(", ir="));
      Serial.print(irBuffer[i], DEC);
      Serial.print(F(", HR="));
      Serial.print(heartRate, DEC);
      Serial.print(F(", HRvalid="));
      Serial.print(validHeartRate, DEC);
      Serial.print(F(", SPO2="));
      Serial.print(spo2, DEC);
      Serial.print(F(", SPO2Valid="));
      Serial.println(validSPO2, DEC);

    //After gathering 25 new samples recalculate HR and SP02
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
  }
  medirDistanciaRociador();
  }
