import json
import threading

import cv2
import os
import asyncio

import httpx
import requests
import websockets
from aiohttp import ClientSession


async def faceDetection():
    dataPath = 'C:/Users/Camilo/PycharmProjects/PeopleIdentification/inputdata'  # Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath)
    print('imagePaths=', imagePaths)

    # face_recognizer = cv2.face.EigenFaceRecognizer_create()
    # face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Leyendo el modelo
    # face_recognizer.read('modeloEigenFace.xml')
    # face_recognizer.read('modeloFisherFace.xml')
    face_recognizer.read('C:/Users/Camilo/PycharmProjects/PeopleIdentification/modeloLBPHFace.xml')

    # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    count_to_send = 0
    while True:
        ret, frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            # LBPHFace
            if result[1] < 70:
                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print(format(imagePaths[result[0]]))
                fileDataJson = dataPath + '/' + format(imagePaths[result[0]]) + '/' + 'code.json'
                f = open(fileDataJson,)

                headers={ 'Accept' : 'application/json','Content-type':'application/text'}
                response=requests.post('http://localhost:8083/rest/user/confirm-user', params=f.read(),headers=headers)
                print(response.text)
                exit(200)
                # with open('detected_person.txt', "w") as file:
                #     file.write(format(imagePaths[result[0]]) + "\n")
                #     break
                count_to_send = count_to_send + 1
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # (flag, imgencode) = cv2.imencode(".jpg", frame)
        cv2.imshow('frame', frame)
        # if not flag:
        #     continue
        # print('Detectando')

        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


loop = asyncio.get_event_loop()
loop.run_until_complete(faceDetection())
