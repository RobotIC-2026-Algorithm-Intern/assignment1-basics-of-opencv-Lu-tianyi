# 传统视觉常用起手式
import cv2
import numpy as np
import matplotlib.pyplot as plt

class ColorRange:
    def __init__(self):
        self.mask_list=[]
    def set_bound(self,h,s,v):
        return np.array([h,s,v], dtype=np.uint8)
    def mask(self,frame,h_lower,s_lower,v_lower,h_upper,s_upper,v_upper):
        self.mask_list.append(cv2.inRange(frame,self.set_bound(h_lower,s_lower,v_lower), self.set_bound(h_upper,s_upper,v_upper)))
    def combine(self,frame,h_lower,s_lower,v_lower,h_upper,s_upper,v_upper):
        self.mask(frame,h_lower,s_lower,v_lower,h_upper,s_upper,v_upper)
        self.mask_list[0]+=self.mask_list[1]
        del self.mask_list[1]
    def count(self):
        return cv2.countNonZero(self.mask_list[0])
# 从output.avi中逐帧读取并将当前帧存为frame
cam = cv2.VideoCapture(r"res/output.avi")
cnt = 0
while True:
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    if not ret:
        break
    roi= frame[135:312,205:435]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV_FULL)
    red=ColorRange()#红色
    red.mask(hsv_roi,0,0,46,30,255,255)
    red.combine(hsv_roi,240,0,46,255,255,255)
    red_pixel_count=red.count()
    blue=ColorRange()# 蓝色
    blue.mask(hsv_roi,160,43,46,180,255,255)
    blue_pixel_count=blue.count()
    purple=ColorRange()# 紫色
    purple.mask(hsv_roi,200,0,15,235,255,255)
    purple_pixel_count=purple.count()
    green_empty=ColorRange()# 绿色(空)
    green_empty.mask(hsv_roi,92,0,15,125,255,255)
    green_empty_pixel_count=green_empty.count()
     # 找到像素数量最多的颜色
    color_counts = {'红色': red_pixel_count, '蓝色': blue_pixel_count, '紫色': purple_pixel_count, '绿色(空)': green_empty_pixel_count}
    dominant_color = max(color_counts, key=color_counts.get)
    # 展示当前帧
    if dominant_color == '红色':
        cv2.imshow('red',frame)
    elif dominant_color == '蓝色':
        cv2.imshow('blue',frame)
    elif dominant_color == '紫色':
        cv2.imshow('purple',frame)
    elif dominant_color == '绿色(空)':
        cv2.imshow('empty',frame)
    cv2.waitKey(10)
    # 在while循环中进行你对frame的处理

cam.release()