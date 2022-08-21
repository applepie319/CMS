import cv2
import requests
import os

def webcam():
    url = "https://notify-api.line.me/api/notify"
    access_token = '***'　#トークンを取得
    headers = {'Authorization': 'Bearer ' + access_token}

    message = 'Write your message'
    payload ={'message' : message}
    r = requests.post(url, headers = headers, params = payload,)

    #img = 'test.jpg'
    #files = {'imageFiles': open(img, 'rb')}
    #r = requests.post(url, headers = headers, params = payload, files = files,)


    cap = cv2.VideoCapture()
    i = 0
    while 1:#True:
        flag = 0
        ret, frame = cap.read()
        path = 'img' + str(i) + '.jpg'
        # cv2.imshow('camera', frame)
        cv2.imwrite(path, frame)
        result, flag2 = detect(flag, path, 'haarcascade_frontalcatface.xml')
        cv2.imwrite(path, result)
        if flag2 == 1:
            files = {'imageFile': open(path, 'rb')}
            r = requests.post(url, headers = headers, params = payload, files = files,)
        os.remove(path)
        key = cv2.waitKey(10000)
        i = i + 1
        if key == 27:
            break

def detect(flag, imagefilename, cascadefilename):
    srcimg = cv2.imread(imagefilename)
    if srcimg is None:
        print('cannot load image')
        sys.exit(-1)
    dstimg = srcimg.copy()
    cascade = cv2.CascadeClassifier(cascadefilename)
    if cascade.empty():
        print('cannnot load cascade file')
        sys.exit(-1)
    objects = cascade.detectMultiScale(srcimg, 1.1, 3)
    for (x, y, w, h) in objects:
        print(x, y, w, h)
        flag = 1
        cv2.rectangle(dstimg, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return dstimg, flag

def main():
    webcam()

if __name__ == '__main__':
    main()
