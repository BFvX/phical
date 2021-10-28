from time import time
from PIL import Image
from tqdm import tqdm
import pytesseract
import numpy as np

def ocr_score():
    time_list = []
    img_range = int(input("请输入图片张数："))
    frame_rate = eval(input("请输入帧速率："))
    #BUG
    print('正在OCR读取分数图片：')
    for i in tqdm(range(img_range)):
        if(i<10):
            seq = '000' + str(i)
        elif(i<100):
            seq = '00' + str(i)
        elif(i<1000):
            seq = '0' + str(i)
        else:
            seq = str(i)
        res = pytesseract.image_to_string(Image.open('./img/test'+seq+'.bmp'),lang='eng',
            config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').strip()
        try:
            #time_list.append([np.around(i/frame_rate*1000),int(res)])
            time_list.append([i/frame_rate*1000,int(res)])
        except ValueError:
            pass
        
    return time_list