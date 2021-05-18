import cv2
import sys
import math
import face_recognition
import pygame

face_locations = []
cap = cv2.VideoCapture(0)#("C:/Users/pattp/Videos/head-pose-face-detection-female-and-male.mp4",0)#imread('./3000.jpg')

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)

rel_path_img = "./image/"

pygame.init()
MOMIUscreen = pygame.display.set_mode((1024,600))
running = True
pygame.display.set_caption("MOMIU Face")
icon = pygame.image.load(rel_path_img+'MOMIU_DeeJai.png')
pygame.display.set_icon(icon)

eye_img = pygame.image.load(rel_path_img+'MOMIU_eye.png')

def lefteye(lefteye_xy):
    MOMIUscreen.blit(eye_img,(lefteye_xy))

def righteye(righteye_xy):
    MOMIUscreen.blit(eye_img,(righteye_xy))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
    MOMIUscreen.fill((10,10,10))

    ret,img = cap.read()
    img = cv2.resize(img, (320,240))
    img = cv2.flip(img,1)

    # img = cv2.resize(img, (420, 420))     

    # rgb_img = img[:, :, ::-1]

    face_locations = face_recognition.face_locations(img)

    areas = []
    ds = []
    maxaidx = 0
    for top, left, bottom, right in face_locations:
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 4)
        y1 = top
        x2 = left
        y2 = bottom
        x1 = right

        a = (x2 - x1) * (y2 - y1)
        areas.append(a)

        d = (-0.0013 * a) + 61.25
        ds.append(d)

    kx = 0.3
    ky = 0.3
    #skipx = 100
    #skipy = 100
    lefteye_pos = (96,40)
    righteye_pos = (608,40)
    if areas != []:
        print(areas)
        amax = max(areas)
        maxaidx = areas.index(amax)
        face = face_locations[maxaidx]
        xface = math.ceil(face[3]+(face[1]-face[3])/2)
        yface = math.ceil(face[0]+(face[2]-face[0])/2)
        pos = (xface-160, -yface+120)
        mopos = (math.ceil(kx*pos[0]+160), math.ceil(-ky*pos[1]+120))
        lefteye_pos = (round(mopos[0]*0.6),round(mopos[1]*0.33))
        righteye_pos = (lefteye_pos[0]+512,lefteye_pos[1])
        cv2.circle(img, mopos, radius=5, color=(0, 0, 255), thickness=2)
        print (pos, maxaidx)
    cv2.imshow('Your Face', img)

    lefteye(lefteye_pos)
    righteye(righteye_pos)

    if cv2.waitKey(25) == 13:
        break
    pygame.display.update()


cap.release()
cv2.destroyAllWindows()
