#!/usr/bin/python3

from seleniumrequests import Firefox
import requests as req
import os
import re
from bs4 import BeautifulSoup as soup
import pywebcopy as copy
import pyautogui
import time
import glob

fire = Firefox()
_session = req.session()
pyautogui.FAILSAFE = False
sleep = time.sleep

# Create the session
def login():
    login = 'https://www.tudodecaotransforma.com.br/wp-login.php'
    mainpage = 'https://www.tudodecaotransforma.com.br'
    testpage = 'https://www.tudodecaotransforma.com.br/videos/para-assistir-antes-de-treinar/socializacao/'
    values = { 
        "log": "xxx",
        "pwd": "xxx",
        "wp-submit": "Acessar",
        "redirect_to": "https://www.tudodecaotransforma.com.br/wp-admin/",
        "testcookie": "1" }

    isok = _session.post(login, values)
    fire.get(login)

    for cookie in _session.cookies:
        fire.add_cookie({
            'name': cookie.name, 
            'value': cookie.value,
            'path': '/',
            'domain': cookie.domain,
        })

    return isok.ok

def repeat(n, func, *args):
    for _ in range(n):
        func(*args)

def savepage(name, n):
    name = name+'.html'
    def sendkeys():
        repeat( 2, pyautogui.press, 'esc' )
        sleep(0.2)
        repeat( 2, pyautogui.hotkey, 'ctrl', 's' )
        sleep(0.2)
        repeat( 2, pyautogui.hotkey, 'ctrl', 'a' )
        sleep(0.2)
        pyautogui.write(name)
        sleep(0.2)
        repeat( 2, pyautogui.press, 'enter' )
        sleep(1.1)

    while not os.path.exists('/root/Downloads/'+name):
        sendkeys()

    print('Downloading page {0}...'.format(n))

def replaceverify():
    def go_on():
        for f in os.listdir('/root/Downloads/'):
            if re.findall(r'pagina [0-9]+|\([0-9]\)pagina [0-9]+', f):
                return True
    if not go_on():
        return ''
    fn = 0
    list = glob.glob('/root/Downloads/*.html')
    tab = []
    for f in list:
        f = f.strip('/root/Downloads/')
        n = re.findall('^.(.).', f)[0]
        try:
            n = int(n)
        except:
            continue
        else:
            tab.append(n)
    if len(tab) > 0:
        fn = max( tab ) + 1
    return '({0})'.format(fn)


def run():
    print('Running...')
    mapa = 'https://www.tudodecaotransforma.com.br/mapa-do-portal/'
    regx = r'(?i)(https:\/\/www.tudodecaotransforma.com.br\/videos\/.+?)"'
    mapPage = _session.get(mapa)
    links = re.findall(regx, mapPage.text)
    num = replaceverify()
    for n in range( len(links) ):
        fire.get(links[n])
        name = num + 'pagina '+str(n)
        savepage( name, n )

def execution():
    if login():
        print('Successful logged in!')
        run()
    else:
        print('Couldn\'t login')

execution()
