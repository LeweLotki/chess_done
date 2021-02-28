import cv2 
import numpy as np 
import random

def detection(list, array):
    temp = []
    for val in list:
        if array[val[0],val[1],0] < 150 and array[val[0],val[1],1] > 150 and array[val[0],val[1],2] < 10:
            temp.extend([[val[0],val[1]]])
    list.clear()
    list.extend(temp)
    
def detection_gray(list, array):
    temp = []
    for val in list:
        if array[val[0],val[1]] < 120:
            temp.extend([[val[0],val[1]]])
    list.clear()
    list.extend(temp)
    
def average_gray(list, img):
    sum = 0
    for val in list:
        sum += img[val[0], val[1]]
    avg = sum / len(list)
    return avg
    
def resultant(list):
    result = 0 
    all_x = 0
    all_y = 0
    lenght = len(list)
    if lenght == 1:
        result = list[0]
    elif lenght > 1:
        for val in list:
            all_x += val[0]
            all_y += val[1]
        all_x = int(all_x/lenght)
        all_y = int(all_y/lenght)
        result = [all_x,all_y]
    if type(result) == int:
        print(result)
    return result
    
def radiation(num,list1):
    radiation = 0
    temp = distance(num, list1)
    for val in temp:
        if val[1] > radiation:
            radiation = val[1]
    return radiation

def distance(num, list):
    temp = []
    temp2 = []
    for val in list:
        d = int(((num[0]-val[0])**2 + (num[1]-val[1])**2)**0.5)
        temp.append(d)
    for i in range(0, len(list)):
        temp2.extend([[list[i],temp[i]]])
    return temp2

def average(list):
    sum = 0
    for val in list: 
        sum += val[1]
    sum = int(sum/len(list))
    return sum
    
# def deviation(list, num):
    # sum = 0
    # for val in list:
        # sum += (val[1] - num)**2
    # sum = sum/len(list)
    # sum = int((sum)**0.5)
    # return sum
    
def unify(dist, avg, points):
    a = 0
    b = avg
    i = 0
    density = False
    temp = []
    density = True
    while density:
        for val in dist:
            if val[1] in range(a, b):
                temp.extend([val[0]])
                if val[0] in points:
                    points.remove(val[0])
            else:
                i += 1
                if i == len(dist):
                    density = False
                    break             
        a += int(avg/10)
        b += int(avg/10)
        i = 0
    if len(temp) == 0:
        print('ERROR')
    return temp
        
def compare(old, new):
    result = []
    for val1 in old:
        i = 0
        for val2 in new:
            if val1[0][0] in range(val2[0][0] - 10, val2[0][0] + 10) and val1[0][1] in range(val2[0][1] - 10, val2[0][1] + 10):
                continue
            else:
                i += 1
                if i == len(new):
                    result.append(val1)                    
    for val1 in new:
        i = 0
        for val2 in old:
            if val1[0][0] in range(val2[0][0] - 10, val2[0][0] + 10) and val1[0][1] in range(val2[0][1] - 10, val2[0][1] + 10):
                continue
            else:
                i += 1
                if i == len(new):
                    result.append(val1)    
    return result

def unify_simple(dist, points):
    a = 0
    b = 10
    i = 0
    temp = []
    density = True
    while density:
        for val in dist:
            if val[1] in range(a, b):
                temp.extend([val[0]])
                if val[0] in points:
                    points.remove(val[0])
            else:
                i += 1
                if i == len(dist):
                    density = False
                    break             
        a += 1
        b += 1
        i = 0
    if len(temp) == 0:
        print('ERROR')
    return temp
    
def subdivided(frame):
    shape = np.shape(frame)
    a = 0
    b = 0
    list = []
    list_cord = []
    for val1 in range(int(shape[0]/8), shape[0], int(shape[0]/8)):
        b = 0
        for val2 in range(int(shape[1]/8), shape[1], int(shape[1]/8)):
            list.append(frame[a:val1, b:val2, :])
            list_cord.append((a, val1, b, val2))
            b += int(shape[1]/8)
        a += int(shape[0]/8)
    return list, list_cord
    
    
def contrast(img):
    img2 = img.copy()
    height, width = np.shape(img)
    for val in range(0, height):
        for val2 in range(0, width):
            img2[val,val2] = int(2* img2[val,val2])
            if img2[val,val2] > 255:
                img2[val,val2] = 255
    return img2
    
def extremum(list):
    max_height = 0
    min_height = 10000
    max_width = 0
    min_width = 10000
    for val in list:
        if val[0] > max_height:
            max_height = val[0]
        if val[0] < min_height:
            min_height = val[0]
        if val[1] > max_width:
            max_width = val[1]
        if val[1] < min_width:
            min_width = val[1]
    return max_height, min_height, max_width, min_width
    
def deviation(list, num):
    sum = 0
    for val in list:
        sum += (val - num)**2
    sum = sum/len(list)
    sum = (sum)**0.5
    return sum
    
def average2(list):
    sum = 0
    for val in list: 
        sum += val
    sum = sum/len(list)
    return sum
    
def cord_division(frame, list):
    squares = []
    for val in list:
        squares.append(frame[val[0]:val[1], val[2]:val[3], :])
    return squares
# def compare(old, new):
    # result = []
    # for val1 in old:
        # i = 0
        # for val2 in new:
            # if val1 in range(val2 - 10, val2 + 10):
                # continue
            # else:
                # i += 1
                # if i == len(new):
                    # result.append(val1)                    
    # for val1 in new:
        # i = 0
        # for val2 in old:
            # if val1 in range(val2 - 10, val2 + 10):
                # continue
            # else:
                # i += 1
                # if i == len(new):
                    # result.append(val1)     
    # return result
    
pola = []
for val in range(1, 9):
    pola.extend(["h"+str(val), "g"+str(val), "f"+str(val), "e"+str(val), "d"+str(val),"c"+str(val), "b"+str(val), "a"+str(val)])
