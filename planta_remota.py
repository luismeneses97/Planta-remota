import serial
import time
import pyrebase
import requests
import time, sys, os, math
import random
import math
config = {
  "apiKey": "AIzaSyCBgqH4iFLg-W9sJcaLu3uRAXCMLI1DqDs",
  "authDomain": "plataforma-practicas-remotas.firebaseapp.com",
  "databaseURL": "https://plataforma-practicas-remotas.firebaseio.com/",
  "projectId": "plataforma-practicas-remotas",
  "storageBucket": "plataforma-practicas-remotas.appspot.com",
  "messagingSenderId": "706879783652"
}
# comunicacion con base de datos
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email = 'lalfonso7777@gmail.com'
password= '123456789'
user = auth.sign_in_with_email_and_password(email, password)
user = auth.refresh(user['refreshToken'])
db = firebase.database()
# calculo de gravedad
def gravedad(altura, tiempo):
    gravedad = ((2*altura)/100)/((tiempo/1000)**2)
    return gravedad
# conexion con arduino
serialArduino = serial.Serial("COM3",115200)

while True:
    time.sleep(1)
    
    results = db.child("/PlantaCaidaLibre/Inputs/").get(user['idToken'])    
    valores = results.val()
    inputs = list(valores.items())
    print("Bandera: ")
    print(inputs[-1][1]["banderaini1"])
    bandera = inputs[-1][1]["banderaini1"]
    
    print("altura: ")
    print(inputs[-1][1]["alturaCL"])
    altura = inputs[-1][1]["alturaCL"]
    altura = int(altura) 

    if bandera == 1:
        serialArduino.write(b'a') #mangeto off
        time.sleep(2)

        salidaSerial = serialArduino.readline().decode('ascii')  # Lectura de puerto serial
   
        sensores =  salidaSerial.split(';')
        sensor1 = int(sensores[0])
        sensor2 = int(sensores[1])
        sensor3 = int(sensores[2])
        sensor4 = sensores[3]
        sensor4 = sensor4.replace('\r', '').replace('\n', '')
        sensor4 = int(sensor4)

        if altura == 15:
            tiempo = sensor1
        elif altura == 30:
            tiempo = sensor2
        elif altura == 45:
            tiempo = sensor3
        else:
            tiempo = sensor4
        
        tiempo_final= tiempo+60 #calibracion de sensores
        
        gravetation = gravedad(float(altura),float(tiempo_final))
        gravetation = round(gravetation,1)
        print(sensor1)
        print(sensor2)
        print(sensor3)
        print(sensor4)
        
        data1 = {'tiempoV1':sensor1,'tiempoV2':sensor2,'tiempoV3':sensor3,'tiempoV4':sensor4, 'gravedad':gravetation}
      
        try:
            results = db.child("/PlantaCaidaLibre/Outputs/").push(data1, user['idToken']) 
            if 'name' in results.keys():
                print("insercion OK => codigo : ", results['name'])
            else:
                print("insercion FAIL!")
        except:
            print("error de ejecicion POST", sys.exc_info())  
        
        serialArduino.write(b'b') #motor adelante y se enciende el electroiman
        time.sleep(5)
        serialArduino.write(b'c')#motor atras
        time.sleep(3)
        serialArduino.write(b'd')#motor se apaga
        time.sleep(2)
       
        data = {'banderaini1':'0','alturaCL':altura} #resetea los datos en base de datos
        db.child("/PlantaCaidaLibre/Inputs/").push(data, user['idToken']) 
        listaTiempos = None

