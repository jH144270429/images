# coding:utf-8
from PIL import Image, ImageDraw
from pyocr import tesseract
import pytesseract
import re

def binaryzation(threshold=240):  # 降噪，图片二值化# 设置阈值为145 低于145全部转化为白色
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
#去除干扰线
def pIx(data):
    # 图片的长宽
    w,h = data.size
    # print("width=",w)
    # print("height=",h)

    # data.getpixel((x,y))获取目标像素点颜色。
    # data.putpixel((x,y),255)更改像素点颜色，255代表颜色。


    try:
        for x in range(0,w):
            #print(x)
            if x > 1 and x != w-1:
                # 获取目标像素点左右位置
                left = x - 1
                right = x + 1

            for y in range(0,h):
                #print(y)
                # 获取目标像素点上下位置
                up = y - 1
                down = y + 1

                if x <= 4 or x >= 109:
                    data.putpixel((x, y), 255)
                elif (x > 18 and x < 34) or (x > 48 and x < 64) or (x > 78 and x < 94):
                    data.putpixel((x, y), 255)
                elif y <= 5 or y >= 27:
                    data.putpixel((x, y), 255)

                elif data.getpixel((x, y)) == 0:
                    if y > 1 and y != h:

                        # 以目标像素点为中心点，获取周围像素点颜色
                        # 0为黑色，255为白色
                        up_color = data.getpixel((x, up))
                        down_color = data.getpixel((x, down))
                        left_color = data.getpixel((left, y))
                        left_up_color = data.getpixel((left, up))
                        left_down_color = data.getpixel((left, down))
                        right_color = data.getpixel((right, y))
                        right_up_color = data.getpixel((right, up))
                        right_down_color = data.getpixel((right, down))
                        # print(x, y)
                        # print(up_color,down_color,left_color,left_up_color,left_down_color,right_color,right_up_color,right_down_color)

                        # 去除竖线干扰线
                        if down_color == 0 or up_color == 0:
                            if left_color == (1 or 255)and right_color == (1 or 255) :
                                data.putpixel((x, y), 255)
                            if  right_color == (1 or 255) and right_down_color == (1 or 255) and right_up_color == (1 or 255):
                                if left_color== (1 or 255) or left_up_color == (1 or 255) or left_down_color == (1 or 255):
                                    data.putpixel((x, y), 255)
                            if left_color == (1 or 255) and up_color == (1 or 255) and right_color == (1 or 255):
                                data.putpixel((x, y), 255)
                        # 去除横线干扰线
                        elif right_color == 0 or left_color == 0:
                            if down_color == (1 or 255) and right_down_color == (1 or 255) and \
                                            up_color == (1 or 255) and right_up_color == (1 or 255):
                                data.putpixel((x, y), 255)
                            if up_color == (1 or 255) and left_color == (1 or 255) and down_color ==(1 or 255):
                                data.putpixel((x, y), 255)
                            if up_color == (1 or 255) and right_color == (1 or 255) and down_color ==(1 or 255):
                                data.putpixel((x, y), 255)
                    # 去除斜线干扰线
                    if left_color == (1 or 255) and right_color == (1 or 255) \
                            and up_color == (1 or 255) and down_color == (1 or 255):
                        data.putpixel((x, y), 255)
                else:
                    pass
    except:
        return False
        print(程序终止)
    return data
#替换代码
def replace_text(text):
    sum = 0
    text = text.strip()#去除text首尾空格
    # text = text.upper()#将text中小写字母转化为大写字母
    rep = {'O': '0',
           'I': '7',
           'L': '1',
           'Z': '7',
           'A': '4',
           '&': '8',
           'Q': '0',
           'T': '7',
           'Y': '7',
           '}': '7',
           'J': '7',
           'F': '7',
           'E': '6',
           ']': '0',
           '?': '7',
           'B': '8',
           '@': '6',
           'G': '0',
           'H': '3',
           '$': '1',
           'C': '0',
           '(': '0',
           '[': '5',
           'X': '7',
           't': '1',
           '.': '7',
           '#': '7',
           '¥': '7',
           '§': '5',
           'f': '7',
           'P': '7',
           '￡': '1',
           '+': '1',
            'S': '3',
           's': '3',
           '%': '4',
           'g': '3',
           }

    #判断是否有数字，有数字直接返回第一个数字，不需要字符替换
    #print (text)
    if len(text) >= 1:
        pattern = re.compile(u'\d{1}')
        result = pattern.findall(text)
        if len(result) >= 1:
            # 字符替换,替换之后抽取数字返回
            for r in rep:
                text = text.replace(r, rep[r])
            #pattern = re.compile(u'\d{1}')
            result = pattern.findall(text)#在去已经替换好的text中查找数字（数字至少出现一次）
            if len(result) >= 1:
                sum = result

    return sum
# 测试代码
def main():
    # 打开图片
    n = 1
    while(n <= 1000):
        image = Image.open('D:/img/验证码/' + (str(n)  + '.jpg'))

        # 将图片转换成灰度图片
        image = image.convert("L")
        image = image.point(binaryzation(), '1')  # 二值化


        # image.show()  # 展示图片

        images = pIx(image)
        # images.show()
        #dir_ = 'D:/img/处理/'+str(n)+'.jpg'
        #images.save(dir_)
        code = pytesseract.image_to_string(images)
        result = replace_text(code)
        print(n, "识别前的数字：",code)
        print(n, "识别后的数字：",result)
        sum = 0
        try:
            for i in range(0,3):
                sum = int(result[0])*1000 + int(result[1])*100 + int(result[2])*10 + int(result[3])
        except IndexError:
            print("验证码识别错误！")
            sum = 1111
        result.clear()
        print(sum)
        n+=1
    print("处理成功！")


if __name__ == '__main__':
    main()