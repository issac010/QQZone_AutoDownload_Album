# coding:utf-8
from bs4 import BeautifulSoup
import requests
import os
import re
import time
import threading
from selenium import webdriver
import urllib.request
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def scroll2bottom():
    # 将滚动条移动到页面的底部
    driver.switch_to.default_content()
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(5)
    driver.switch_to.frame('tphoto')

img_name = 0
def picdownload():
    global img_name
    Soup = BeautifulSoup(driver.page_source, 'lxml')
    img = Soup.find_all('img', class_='j-pl-photoitem-img')
    # print('img:  ', img, '\r\n', '*' * 60)
    path = os.getcwd()  # 获取路径
    album_title = driver.find_element_by_css_selector(
        '.j-pl-quickedit-normal-content.j-pl-albuminfo-title').get_attribute('title')
    path_dir = os.path.join(path, album_title)  # 拼接路径
    print(path_dir)
    try:
        print('创建文件夹 --> {}'.format(album_title))
        os.mkdir(path_dir)  # 创建目录
    except:
        print('此文件夹已存在!')
        pass
    os.chdir(path_dir)  # 切换路径

    print('*' * 60, '\r\n开始下载图片')
    for img_url in img:  # 下载图片
        try:
            img_ori = img_url['src']
        except:
            img_ori = img_url['data-src']
            pass
        # head = r'http://m.qpic.cn/psb?'
        # end = r'viewer_4'
        # img_rel = head + img_ori[22:-47] + r'b' + img_ori[-46:-9] + end
        img_rel = img_ori.replace(r'/m/', r'/b/').replace(r'psbe?', r'psb?')  # 很重要
        img_name = img_name + 1
        print(img_name, ' img url: ', img_rel)
        # path2 = os.path.join(path_dir,'%s.jpg' % str(img_name))
        # urllib.request.urlretrieve(img_rel,path2) # 核心是urllib.urlretrieve()方法,直接将远程数据下载到本地
        # time.sleep(0.5)
        img_html = requests.get(img_rel)
        f = open(str(img_name) + '.jpg', 'ab')  # 写入多媒体文件必须要 b 这个参数！
        f.write(img_html.content)  # 多媒体文件要是用conctent！
        f.close()
        # time.sleep(0.2)
    print('当前页下载完成!')
    os.chdir(path)

###################################程序从此处开始#############################################
print('程序运行要求：\r\n  '
      '1、下载火狐浏览器。\r\n  '
      '2、下载火狐驱动 geckodriver.exe\r\n  '
      '3、将驱动放至火狐安装目录。\r\n  '
      '4、将火狐安装目录添加至系统环境变量。\r\n  '
      '5、按提示输入信息，随后自动运行，若出错请多试几次。\r\n  '
      '6、程序有时运行缓慢，请耐心等待！\r\n  '
      '7、进入相册前，请不要在浏览器界面移动鼠标，以免干扰程序判断\r\n\r\n'
      )

user = input('输入账号: \r\n  ')
word = input('输入密码: \r\n  ')
oth_user = input('输入对方账号(空表示下载自己): \r\n  ')
print('*'*60,'\r\n\t\t    即将开始!')
print('*'*60)
# while True:
geturl = r'https://qzone.qq.com/'
geturl_other = r'https://user.qzone.qq.com/' + oth_user
driver = webdriver.Firefox()
# driver = webdriver.PhantomJS()
driver.maximize_window()
driver.implicitly_wait(10)  # 隐性等待
driver.get(geturl)

print('切换到登录表单')
driver.switch_to.frame('login_frame')  # 登录表单在页面的框架中，所以要切换到该框架
switcher_plogin = driver.find_element_by_id('switcher_plogin')
switcher_plogin.click()
time.sleep(1)

username = driver.find_element_by_id('u')  # 查找账号
password = driver.find_element_by_id('p')  # 查找密码
login_button = driver.find_element_by_id('login_button')  # 查找登陆按键

print('输入账号中...')
username.clear()
time.sleep(2)
username.send_keys(user)  # 输入账号
print('输入密码中...')
password.clear()
time.sleep(5)
password.send_keys(word)  # 输入密码
print('登陆中...')
time.sleep(5)
login_button.click()
print('**此处若有滑块验证，请在10s内手动完成！！！**')
time.sleep(10)
while True:
    try:
        driver.find_element_by_id('switcher_plogin')
        print('登陆失败,将重试!')
        login_button.click()
        print('**此处若有滑块验证，请在10s内手动完成！！！**')
        time.sleep(10)
        # driver.delete_all_cookies()
        # driver.close()
        continue
    except:
        print('登陆成功!')
        break

driver.switch_to.default_content()  # 返回

if oth_user:
    print('进入', oth_user)
    driver.get(geturl_other)
    print('等待稳定...')
    try:
        background = driver.find_element_by_css_selector('.mode_lace.mode_bg_opacity100')
        background.click()
        time.sleep(4)
    except:
        pass
    try:
        button = driver.find_element_by_class_name('btn-fs-sure')
        button.click()
    except:
        pass
    # driver.refresh()

try:
    mainpage = driver.find_element_by_css_selector('.homepage-link.a-link')  # 进入主页
    ActionChains(driver).move_to_element(mainpage).perform()
    time.sleep(2)
    menu_item = driver.find_elements_by_class_name('menu_item_4')[0]
    menu_item.click()
    ActionChains(driver).move_by_offset(200, 200)
    time.sleep(2)
    # try:
    #     menu_item = driver.find_element_by_id('QM_Profile_Photo_A')
    # except:
    #     menu_item = driver.find_elements_by_class_name('menu_item_4')[1]
    # print('进入相册列表中...')
    # menu_item.click()  # 进入相册列表
    # time.sleep(6)
    try:
        guanggao = driver.find_element_by_css_selector('.op-icon.icon-close')
        print('检测到弹窗广告，自动关闭！')
        guanggao.click()
    except:
        pass
    driver.switch_to.frame('tphoto')
    print('switch to tphoto frame')
    print('**此页面如果有未处理广告，且干扰程序运行，请手动关闭！！！**')
    # 滚动
    driver.switch_to.default_content()
    js = "var q=document.documentElement.scrollTop=400"
    driver.execute_script(js)
    time.sleep(3)
    driver.switch_to.frame('tphoto')
    time.sleep(2)
    length = 0

    album_list = driver.find_elements_by_css_selector('.c-tx2.js-album-desc-a')
    album_list_cnt = 0
    print("你共有以下相册，请输入需要下载相册的序号 \r\n  ")
    for i in album_list:
        album_list_cnt = album_list_cnt + 1
        print("[", album_list_cnt, "] ", i.text)
    which_album = int(input("输入数字(如:1)")) - 1
    while True:
        album_list = driver.find_elements_by_css_selector('.c-tx2.js-album-desc-a')[which_album]
        print('进入相册中...', album_list.get_attribute('title'))
        album_list.click()
        time.sleep(5)
        try:
            driver.find_element_by_class_name('pic-num-wrap')
            print('进入相册失败,将重试!')
            # album = driver.find_elements_by_css_selector('.item-wrap.bor-tx')[0]
            # album.click()
            # 滚动
            driver.switch_to.default_content()
            length = length + 100
            js = "var q=document.documentElement.scrollTop="+str(500+length)
            driver.execute_script(js)
            time.sleep(3)
            driver.switch_to.frame('tphoto')
            time.sleep(2)
            continue
        except:
            print('进入成功!')
            break
except Exception as e:
    print(e)

print('扫描图片中...')
counter = 2
while counter > 0:
    scroll2bottom()
    counter = counter - 1
try:
    try:
        page_num = driver.find_element_by_id('pager_last_1').get_attribute('innerHTML')
        # print('page_num: ',page_num)
    except:
        page_num = driver.find_elements_by_css_selector('.js-pagenormal')[-1].get_attribute('title')
        pass
except:
    page_num = 1
    pass
page_current = 1
print('**第{}/{}页**'.format(page_current,page_num))
picdownload()
while page_current < int(page_num):
    next_page =driver.find_element_by_id('pager_next_1')
    next_page.click()
    page_current = page_current + 1
    print('**第{}/{}页**'.format(page_current,page_num))
    time.sleep(2)
    print('扫描图片中...')
    counter = 2
    while counter > 0:
        scroll2bottom()
        counter = counter - 1
    picdownload()

print('感谢使用，下次见!')
driver.close()



