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
from PIL import Image
from io import BytesIO

global driver  # 在使用前初次声明
global oth_user


def webpTojpg(path):
    f = Image.open(path)
    f.save(path.rsplit('.')[0]+'.jpg', 'JPEG')
    os.remove(path)
    # res = os.popen("dwebp %s -o %s"%(path, path.rsplit('.')[0]+'.png')).readlines()
    print("* jpg转换完成 *")


def scroll2bottom():
    global driver  # 再次声明，表示在这里使用的是全局变量
    # 将滚动条移动到页面的底部
    driver.switch_to.default_content()
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(5)
    driver.switch_to.frame('tphoto')


img_name = 0
total_img = 0
import imghdr
def picdownload():
    global img_name, total_img
    global driver  # 再次声明，表示在这里使用的是全局变量
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
    # total_img += len(img)
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
        print("[{}/{}] Img_URL: {}".format(img_name, total_img, img_rel))
        # print("[", img_name, "]", ' Img_URL: ', img_rel)
        # path2 = os.path.join(path_dir,'%s.jpg' % str(img_name))
        # urllib.request.urlretrieve(img_rel,path2) # 核心是urllib.urlretrieve()方法,直接将远程数据下载到本地
        # time.sleep(0.5)
        img_html = requests.get(img_rel)
        f = open(str(img_name) + '.jpg', 'wb')  # 写入多媒体文件必须要 b 这个参数！
        f.write(img_html.content)  # 多媒体文件要是用conctent！
        f.close()
        if imghdr.what(str(img_name) + '.jpg') == 'webp':
            print("* webp格式图片 *")
            os.rename(str(img_name)+'.jpg', str(img_name)+'.webp')
            webpTojpg(str(img_name)+'.webp')
        # time.sleep(0.1)
    print('当前页下载完成!')
    os.chdir(path)


def main_enter():
    global driver, oth_user  # 再次声明，表示在这里使用的是全局变量
    user = input('输入账号: \r\n  ').strip()
    word = input('输入密码: \r\n  ').strip()
    oth_user = input('输入对方账号(空表示下载自己): \r\n  ').strip()
    print('*'*60, '\r\n\t\t    即将开始!')
    print('*'*60)
    # while True:
    geturl = r'https://qzone.qq.com/'
    geturl_other = r'https://user.qzone.qq.com/' + oth_user
    profile = webdriver.FirefoxProfile(os.path.join(os.getcwd(), 'selenium_firefox'))
    driver = webdriver.Firefox(profile)   # 读入浏览器配置，以屏蔽浏览器通知
    # driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.implicitly_wait(30)  # 隐性等待
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
    # time.sleep(1)
    username.send_keys(user)  # 输入账号
    print('输入密码中...')
    password.clear()
    # time.sleep(1)
    password.send_keys(word)  # 输入密码
    print('登陆中...')
    time.sleep(1)
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
        time.sleep(5)
        print('进入', oth_user)
        driver.get(geturl_other)
        print('等待稳定...')
        time.sleep(5)
        if 'btn-fs-sure' in driver.page_source:
            friendship = driver.find_element_by_class_name('btn-fs-sure')
            friendship.click()
            time.sleep(1)
        print("稳定结束")
        # driver.refresh()


def main_album():
    global driver, img_name, total_img, oth_user  # 再次声明，表示在这里使用的是全局变量
    total_img = 0
    img_name = 0
    driver.refresh()
    time.sleep(2)
    driver.find_element_by_class_name('icon-homepage').click()
    # driver.find_element_by_class_name('logo').click()
    time.sleep(2)
    try:
        print("执行js调出'我的主页'界面")
        js = r'document.getElementById("tb_menu_panel").style.display="block"'
        driver.execute_script(js)
        # mainpage = driver.find_element_by_css_selector('.homepage-link.a-link')  # 进入主页
        # ActionChains(driver).move_to_element(mainpage).perform()
        time.sleep(2)
        menu_item = driver.find_elements_by_class_name('menu_item_4')[0]
        menu_item.click()
        # ActionChains(driver).move_by_offset(200, 200)
        # time.sleep(2)
        print("执行js退出'我的主页'界面")
        js = r'document.getElementById("tb_menu_panel").style.display="none"'
        driver.execute_script(js)
        time.sleep(2)
        # try:
        #     menu_item = driver.find_element_by_id('QM_Profile_Photo_A')
        # except:
        #     menu_item = driver.find_elements_by_class_name('menu_item_4')[1]
        # print('进入相册列表中...')
        # menu_item.click()  # 进入相册列表
        # time.sleep(6)

        print('检测广告中...')
        if '.op-icon.icon-close' in driver.page_source:
            guanggao = driver.find_element_by_css_selector('.op-icon.icon-close')
            print('检测到弹窗广告，自动关闭！')
            guanggao.click()
        else:
            print('无广告')
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
        which_album = int(input("输入数字(如:1) ").strip()) - 1

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        total_img = int(soup.find_all(class_='pic-num')[which_album].string)
        #total_img = int(driver.find_elements_by_class_name('pic-num')[which_album])  # 'pic-num'  'j-pl-albuminfo-total'

        print("本相册共有[%s]张照片" % total_img)
        while True:
            album_list = driver.find_elements_by_css_selector('.c-tx2.js-album-desc-a')[which_album]
            print('进入相册中...', album_list.get_attribute('title'))
            album_list.click()
            time.sleep(5)

            #driver.find_element_by_class_name('pic-num-wrap')

            if oth_user:
                if '转载' not in driver.page_source:
                    print('进入相册失败,将重试!')
                    # album = driver.find_elements_by_css_selector('.item-wrap.bor-tx')[0]
                    # album.click()
                    # 滚动
                    driver.switch_to.default_content()
                    length = length + 100
                    js = "var q=document.documentElement.scrollTop=" + str(500 + length)
                    driver.execute_script(js)
                    time.sleep(3)
                    driver.switch_to.frame('tphoto')
                    time.sleep(2)
                    continue
                else:
                    print('进入成功!')
                    break
            else:
                if 'pic-num-wrap' in driver.page_source:
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
                else:
                    print('进入成功!')
                    break
    except Exception as e:
        print(e)

    print('扫描图片中...')
    counter = 2
    while counter > 0:
        scroll2bottom()
        counter = counter - 1
    print('扫描完成')

    if 'pager_last_1' in driver.page_source:
        page_num = driver.find_element_by_id('pager_last_1').get_attribute('innerHTML')
    elif 'js-pagenormal' in driver.page_source:
        page_num = driver.find_elements_by_css_selector('.js-pagenormal')[-1].get_attribute('title')
    else:
        page_num = 1

    page_current = 1
    print('**第{}/{}页**'.format(page_current, page_num))
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
        try:
            picdownload()
        except Exception as e:
            print(e)




#******************************程序从此处开始******************************#


if __name__ == '__main__':
    global driver  # 再次声明，表示在这里使用的是全局变量
    print('程序运行要求：\r\n  '
          '1、下载火狐浏览器。\r\n  '
          '2、下载火狐驱动 geckodriver.exe\r\n  '
          '3、将驱动放至火狐安装目录。\r\n  '
          '4、将火狐安装目录添加至系统环境变量。\r\n  '
          '5、按提示输入信息，随后自动运行，若出错请多试几次。\r\n  '
          '6、程序有时运行缓慢，请耐心等待！\r\n  '
          '7、进入相册前，请不要在浏览器界面移动鼠标，以免干扰程序判断\r\n\r\n'
          'Github: https://github.com/1061700625/QQZone_AutoDownload_Album\r\n\r\n'
          )

    # ping = os.popen("ping baidu.com -n 1").readlines()
    # if "丢失 = 0" in ping[5]:
    #     print("网络可用")
    # else:
    #     print("网络不可用 - ", ping[5])
    #     input("任意键退出")
    #     os._exit(0)

    main_enter()
    main_album()
    while(input("是否继续？(Y/N): ").strip().lower() == 'y'):
        print('\r\n\r\n')
        main_album()
    print('感谢使用，下次见!')
    driver.close()

