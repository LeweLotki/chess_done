from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import cv2 
import numpy as np 
import random
from mypackages import fun2 as fun
# wykrywanie szachownicy
points = []
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
aim_list = []
radius_list = []
if (cap.isOpened()== False):  
  print("Error opening video  file")
ret, frame = cap.read()  
n =  100*int((frame.shape[0]*frame.shape[1])**0.5)
chessboard_exist = False
squares_list = []
squares_cord_list = []
cord = False

while(cap.isOpened()): 
    m = 0
    ret, frame = cap.read()
    # n = 130
    # frame[ :, 130 + 10:130 + 20,: ] = (0, 0, 0)
    # frame[ 50+ 10:50 + 20, :, : ] = (0, 0, 0)
    if ret == True: 
        if cv2.waitKey(25) & 0xFF == ord('s'): 
            aim_list.clear()
            while m < n:
            
                x = random.randint(0, frame.shape[0]-1)
                y = random.randint(0, frame.shape[1]-1)
                points.extend([[x,y]])
                m += 1   
            fun.detection(points, frame) 
            
            if len(points) > 1:
               
                while len(points) > 5:
                    chessboard_exist = True
                    dist = fun.distance(points[0], points)
                    uni = fun.unify_simple(dist, points)  
                    aim = tuple(fun.resultant(uni)) 
                    aim_list.append(aim)
                    dist.clear()
                    uni.clear()               
                points.clear()
                
            else:
                chessboard_exist = False

        if chessboard_exist and len(aim_list) == 2: 
            print(aim_list)
            #frame_cropped = frame.copy()
            if aim_list[0][0] > aim_list[1][0] and aim_list[0][1] > aim_list[1][1]:
                frame_cropped = frame[aim_list[1][0]:aim_list[0][0],aim_list[1][1]:aim_list[0][1],:]
            else:
                frame_cropped = frame[aim_list[0][0]:aim_list[1][0],aim_list[0][1]:aim_list[1][1],:]           
            squares_list, squares_cord_list = fun.subdivided(frame_cropped)
            chessboard_exist = False
            cord = True
        cv2.imshow('Frame', frame) 
        
        if cord:
            old_frame_cropped = frame_cropped.copy()
            old_squares_list = squares_list.copy()
            cv2.imshow('frame_cropped', frame_cropped)

            # print(len(squares_list))
            if len(squares_list) == 64:
                # print(squares_cord_list[0])
                # cv2.imshow('b1', cv2.bilateralFilter(squares_list[1], 9, 75, 75))
                # cv2.imshow('d2', cv2.bilateralFilter(squares_list[51], 9, 75, 75))
                pass
        if cv2.waitKey(25) & 0xFF == ord('p'): 
            if aim_list[0][0] > aim_list[1][0] and aim_list[0][1] > aim_list[1][1]:
                frame_cropped = frame[aim_list[1][0]:aim_list[0][0],aim_list[1][1]:aim_list[0][1],:]
            else:
                frame_cropped = frame[aim_list[0][0]:aim_list[1][0],aim_list[0][1]:aim_list[1][1],:]  
            squares_list = fun.cord_division(frame_cropped, squares_cord_list)
            ssim_cord = False
            index_list = []
            for index in range(0, 64):
                (ssim, diff) = structural_similarity(cv2.bilateralFilter(cv2.cvtColor(squares_list[index], cv2.COLOR_BGR2GRAY), 9, 75, 75), cv2.bilateralFilter(cv2.cvtColor(old_squares_list[index], cv2.COLOR_BGR2GRAY), 9, 75, 75), full=True)
                ssim = round(100*(ssim), 3)
                if ssim < 70:   
                    # print("index", index, "SSIM", ssim) # important line
                    index_list.append(index)
                    ssim_cord = True
            if not (ssim_cord):
                print("no changes")
            if len(index_list) == 2:
                print("pawn ", fun.pola[index_list[0]], " - ", fun.pola[index_list[1]])
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break

    else:  
        break
# print(fun.pola)
cap.release() 

cv2.destroyAllWindows() 
