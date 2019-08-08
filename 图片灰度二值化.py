import pytesseract
from PIL import Image, ImageEnhance


def binaryzation(threshold=245):  # 降噪，图片二值化# 设置阈值为145 低于145全部转化为白色
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


image = Image.open('..//code1.jpg')  # 打开图片
image = image.convert('L')  # 转化为灰度图
# image.show()#展示图片
image = image.point(binaryzation(), '1')  # 二值化
image.show()#展示图片