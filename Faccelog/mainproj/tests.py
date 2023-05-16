from django.test import TestCase

# Create your tests here.
import face_recognition,os
import cv2 

def facedect(loc):
        cam = cv2.VideoCapture(0)   
        s, img = cam.read()
        if s:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'mainproj')

                loc=(str(MEDIA_ROOT)+loc)
                face_1_image = cv2.imread(loc)
                face_1_image = cv2.cvtColor(face_1_image, cv2.COLOR_BGR2RGB)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
                print(face_1_face_encoding)

                #

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                facesCurrentFrame = face_recognition.face_locations(img)
                face2_encodings = face_recognition.face_encodings(img)[0]
                print(face2_encodings)
                check=face_recognition.compare_faces(face_1_face_encoding,face2_encodings)
                

                print(check)
        

facedect('/media/mainproj/images/DSC09774.JPG')