unsigned long finished = 0;
unsigned long elapsed = 0;
unsigned long start = 0;

int PWM = 10; 
int IN1 = 9;
int IN2 = 8;
int Mag = 11; 

int sensor1 = 2;
int sensor2 = 3;
int sensor3 = 4;
int sensor4 = 5;
int sensor5 = 6;
int cont = 0;
int cont2 = 0;
int cont3 = 0;
int cont4 = 0;
int cont5 = 0;
int lista[4];
int miArray[10];
int posicion = 0;

 void setup(){ 
  Serial.begin(115200); 
  pinMode(2, INPUT); 
  pinMode(3, INPUT); 
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  cont = 0;

  pinMode (PWM, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (Mag, OUTPUT);
  digitalWrite (Mag,LOW);
  } 
int Result(){ 
  float  s; 
  elapsed = finished - start;   
  return elapsed;
} 

int tomaTiempos(int contB ){
  if(contB < 1){
    finished = millis();
    //Serial.println(Result());
    cont = 0;
    contB = contB + 1;
  } 
  return contB;
}

void Adelante(){
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (PWM, 150); 
}

void Atras(){
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (PWM, 200);
}

void Detener(){
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, HIGH);
 analogWrite (PWM, 100); 
}

void MagnetoOff(){
 digitalWrite (Mag, HIGH);
}

void MagnetoOn(){
 digitalWrite (Mag, LOW);
}

void temporizador(){
    if (digitalRead(sensor1) == LOW ) { 
      start = millis(); 
      if(cont < 1){
        cont = cont + 1;
        cont2 = 0;
        cont3 = 0;
        cont4 = 0;
        cont5 = 0;
      }
    }
    if (digitalRead(sensor2) == LOW ) { 
       cont2 = tomaTiempos(cont2);
       lista[0]= Result();
    }
    if (digitalRead(sensor3) == LOW) { 
       cont3 = tomaTiempos(cont3);
       lista[1]= Result();
    }
    if (digitalRead(sensor4) == LOW) { 
       cont4 = tomaTiempos(cont4);
       lista[2]= Result();
    }
    if (digitalRead(sensor5) == LOW ) { 
       cont5 = tomaTiempos(cont5);
       lista[3]= Result();
       if(cont5 < 2){
          for(int i=0;i<4;i++){
              Serial.print(lista[i]);
              lista[i]=0;
              if(i<3){
              Serial.print(";");
              }
          }
          Serial.println("");     
          cont5++;
       }
    }
}

void loop() { 
  char  bandera = (char)Serial.read();
  temporizador();
  if (bandera ==  'a'){ //el magneto se apaga 
   MagnetoOff();
   Detener();  
  }

  if (bandera == 'b'){ //motor baja y magneto enciende
     Adelante();
     MagnetoOn();
  }
   
  if (bandera == 'c'){ //motor sube
     Atras();   
  }
  
  if (bandera == 'd'){ //motor se detiene
     Detener();
     Serial.print("");
     Serial.write(0x0d);  
  }  
}
