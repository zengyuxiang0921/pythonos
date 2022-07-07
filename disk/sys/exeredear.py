import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy

hWnd = win32gui.FindWindow("sys", None)
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = right - left
height = bot - top
hWndDC = win32gui.GetWindowDC(hWnd)
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
saveDC = mfcDC.CreateCompatibleDC()
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
saveDC.SelectObject(saveBitMap)
saveDC.BitBlt((0, 0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
saveBitMap.SaveBitmapFile(saveDC,"img_Winapi.bmp")
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)

signedIntsArray = saveBitMap.GetBitmapBits(True)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hWnd,hWndDC)

im_PIL.save("im_PIL.png")
im_PIL.show()

im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
im_opencv.shape = (height, width, 4)
cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
cv2.imwrite("im_opencv.jpg", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100]) #保存
cv2.namedWindow('im_opencv')
cv2.imshow("im_opencv", im_opencv)
cv2.waitKey(0)
cv2.destroyAllWindows()

