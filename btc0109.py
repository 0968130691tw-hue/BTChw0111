import cv2
import numpy as np

def btc_simple(img):
    h, w = img.shape
    res = np.zeros_like(img)
    
    for i in range(0, h, 4):
        for j in range(0, w, 4):
            # 1. 取得 4x4 區塊
            block = img[i:i+4, j:j+4].astype(float)
            
            # 2. 計算統計值與位元平面
            m = 16
            mean = np.mean(block)
            std = np.std(block)
            mask = block >= mean
            q = np.sum(mask) # 亮點數量
            
            # 3. 計算重建值 (核心公式)
            if std == 0 or q == 0 or q == m:
                a = b = mean
            else:
                a = mean - std * np.sqrt(q / (m - q))
                b = mean + std * np.sqrt((m - q) / q)
            
            # 4. 填回數值 (壓縮結果)
            res[i:i+4, j:j+4] = np.where(mask, b, a)
            
    return res.astype(np.uint8)
\
# 讀取並執行
img = cv2.imread('1-0000.jpg', 0)
out = btc_simple(img)
cv2.imshow('BTC Result', out)
cv2.waitKey(0)