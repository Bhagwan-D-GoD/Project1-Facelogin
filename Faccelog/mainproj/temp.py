import face_recognition,os
import cv2 



def facedect(loc):
        
        cam = cv2.VideoCapture(0)   
        s, img = cam.read()
        if s:   
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'mainproj')

                loc=(str(MEDIA_ROOT)+str(loc))
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

                #
                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]
                cv2.imshow('Webcam', img)
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                

                print(check)
                if check[0]:
                        return True

                else :
                        return False   
                    
                    

facedect('/media/mainproj/images/DSC09776.JPG')