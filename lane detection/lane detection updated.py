import numpy as np
import cv2
import matplotlib.pyplot as plt
cap=cv2.VideoCapture(r'D:\machine learning complete\data\road video\road.mp4')
while(cap.isOpened()):
    ret,frame=cap.read()
    frame1=frame.copy()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    canny=cv2.Canny(blur,50,150)
    #cv2.imshow('frame',lines)
    mask=np.zeros_like(canny)
    polygons=np.array([[(0,760),(650,500),(850,500),(1200,760)]])
    mask=cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(canny,mask)
    cv2.imshow("sd",masked_image)
    imagem=cv2.bitwise_not(masked_image)
    lines = cv2.HoughLinesP(masked_image,1,np.pi/180,100,minLineLength=100,maxLineGap=50)
    try:
        left_line=[]
        right_line=[]
        #for x1,x2,x3,x4 in lines[0:72][0]:
            #cv2.line(frame,(x1,x2),(x3,x4),(152,156,20),2)
            #cv2.imshow('frame',frame)
        for i in range(0,lines.shape[0]):
            x1,y1,x2,y2=lines[i][0]
            parameters=np.polyfit((x1,x2),(y1,y2),1)
            slope=parameters[0]
            intercept=parameters[1]
            if slope<0:
                left_line.append((slope,intercept))
            else:
                right_line.append((slope,intercept))
        left_avg=np.average(left_line,axis=0)
        right_avg=np.average(right_line,axis=0)
        left_x1=int((760-left_avg[1])/left_avg[0])
        left_x2=int((500-left_avg[1])/left_avg[0])
        right_x1=int((760-right_avg[1])/right_avg[0])
        right_x2=int((500-right_avg[1])/right_avg[0])
        cv2.line(frame,(left_x1,760),(left_x2,500),(0,255,255),10)
        cv2.line(frame,(right_x1,760),(right_x2,500),(0,255,255),10)
        #r=cv2.line(frame,(left_x1,760),(left_x2,500),(0,255,255),2)
        #l=cv2.line(frame,(right_x1,760),(right_x2,500),(0,255,255),2)
        #print("right",r)
        #print("left",l)
        pts=np.array([[left_x1,760],[right_x1,760],[right_x2,500],[left_x2,500]])
        cv2.polylines(frame,[pts],True,(0,255,255))
        poly=cv2.fillPoly(frame,[pts],(0,255,0))
        alpha=0.5
        cv2.addWeighted(poly, alpha, frame1, 1 - alpha,
		0, frame1)
        frame1=cv2.resize(frame1,(720,720))
        cv2.imshow("detected lane",frame1)
    except:
        pass
    cv2.waitKey(1);
cap.release()
cv2.destroyAllWindows()

