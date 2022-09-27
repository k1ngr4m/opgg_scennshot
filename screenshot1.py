import datetime
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.by import By


def screenshot_to_pdf_and_png(link, name):
    path = '../screenshot/temp'
    # 1> 获取chrome参数对象
    chrome_options = Options()
    # 2> 添加无头参数r,一定要使用无头模式，不然截不了全页面，只能截到你电脑的高度
    chrome_options.add_argument('--headless')
    # 3> 为了解决一些莫名其妙的问题关闭 GPU 计算
    chrome_options.add_argument('--disable-gpu')
    # 4> 为了解决一些莫名其妙的问题浏览器不动
    chrome_options.add_argument('--no-sandbox')
    # 5> 添加驱动地址。 由于在函数内，设置参数chrome_options需要再导入
    driver = webdriver.Chrome(options=chrome_options)

    driver.set_page_load_timeout(20)
    print(f"try：{name}")
    # 6> 模仿手动滑动滚动条，解决懒加载问题
    try:
        driver.implicitly_wait(20)
        # print(datetime.datetime.now())
        # driver.get(link)
        try:
            driver.get(link)
            # print(datetime.datetime.now())
        except:
            # print("加载超时")
            driver.execute_script("window.stop()")

        # print(datetime.datetime.now())
        # 模拟人滚动滚动条,处理图片懒加载问题
        js_height = "return document.body.clientHeight"
        try:
            driver.get(link)
            # print(datetime.datetime.now())
        except:
            # print("加载超时")
            driver.execute_script("window.stop()")
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 200)
                # print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break

        time.sleep(1)

        # 7>  # 直接截图截不全，调取最大网页截图
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
            "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
            "document.documentElement.offsetWidth);")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);")
        # print(width, height)
        # 将浏览器的宽高设置成刚刚获取的宽高
        driver.set_window_size(width + 100, height + 100)
        # driver.set_window_size(1150, 1700)
        time.sleep(1)
        # date = datetime.datetime.now().strftime('%Y-%m-%d %H')

        print("开始截图！")
        png_head_path = path + '/{}.png'.format(f'{name}_head_opgg_screenshot')
        png_body_path = path + '/{}.png'.format(f'{name}_body_opgg_screenshot')

        png_head = driver.find_element(By.XPATH, '//*[@id="content-container"]/main/div[1]')
        png_body = driver.find_element(By.XPATH, '//*[@id="content-container"]/main/div[2]')
        # 截图并关掉浏览器
        png_head.screenshot(png_head_path)
        png_body.screenshot(png_body_path)

        image_Splicing(png_head_path, png_body_path, path, name)

        driver.close()

    except Exception as e:
        print(e)


def image_Splicing(img_1, img_2, path, name, flag='y'):
    print(f"开始拼图{name}")
    img1 = Image.open(img_1)
    img2 = Image.open(img_2)
    size1, size2 = img1.size, img2.size
    if flag == 'x':
        joint = Image.new("RGB", (size1[0] + size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
    else:
        joint = Image.new("RGB", (size1[0], size2[1] + size1[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
    joint.paste(img1, loc1)
    joint.paste(img2, loc2)
    newpath = '../screenshot'
    png_path = newpath + '/{}.png'.format(f'{name}_opgg_screenshot')

    joint.save(png_path)
    print(f"{name}拼图成功！")


if __name__ == '__main__':
    tf = open("../Demo/lol.json", "r")
    hero_dict = json.load(tf)
    name_en = list(hero_dict.values())
    name_en = list(set(name_en))
    # print(name_en)
    for i in range(len(name_en)):
        url = f"https://www.op.gg/modes/aram/{name_en[i]}/build"
        screenshot_to_pdf_and_png(url, name_en[i])
        print(f"{name_en[i]}图片保存成功{i}")
        time.sleep(1)

