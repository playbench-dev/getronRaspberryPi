#!/usr/bin/python3
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# import webbrowser
# url = "http://www.naver.com"
# webbrowser.open(url)
# True
import json
import os
import socket
import threading
import schedule
import time
import netifaces as ni
from multiprocessing import Process
import requests
import sys
import ctypes
from PyQt5.QtWidgets import *
import webbrowser
#from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import QRect
from PyQt5 import uic
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException
import psutil
import subprocess
import platform
import datetime
import logging

test = False
versionStr = "VER. 1.0.0"
serverUrl = "https://getronpush.com"
serverUrl1 = "http://192.168.0.102:8080"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches",['enable-automation'])
#chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

processNameList = []
processViewNoList = []
xprocessViewNoList = []
#reboot_thread = threading.Thread(target=schedule_reboot)
#reboot_thread.start()

def schedule_reboot():
    now = datetime.datetime.now()
    half_day_seconds = 60
    qSetting = QSettings("TestPro", "infoFile")
    siteNo = qSetting.value("siteNo")
    f = open("/home/pi/Desktop/Getron/getronBootTime", 'r')
    line = f.readline()
    f.close()
    if not siteNo == None :
        if int(siteNo)%60 < 10 :
            schedule.every().day.at(line+":00".replace("00","0"+str(int(siteNo)%60))).do(schedule_job)
        else:
            schedule.every().day.at(line+":00".replace("00",str(int(siteNo)%60))).do(schedule_job)
        while True:
            schedule.run_pending()
            time.sleep(half_day_seconds)
    else:
        schedule.every().day.at(line+":00").do(schedule_job)
        while True:
            schedule.run_pending()
            time.sleep(half_day_seconds)
    
def schedule_job():
    now = datetime.datetime.now()
    f = open("/home/pi/Desktop/Getron/getronMainLog","a")
    f.write("\n"+str(now))
    f.close()
    print("os reboot")
    os.system("reboot")

global thOsStart
global driver
        
class myLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

class myEdit(QLineEdit):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()
            
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    
class SubWindow(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Logout')
        self.setGeometry(810, 440, 300, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        subLayout = QHBoxLayout()
        txtContents = QLabel("Are you sure you want to exit?")
        txtContents.setFont(font)
        btnOK = QPushButton("Done")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
    
        layout.addWidget(txtContents)
        subLayout.addWidget(btnCancel)
        subLayout.addWidget(btnOK)
        
        layout.addStretch(1)
        layout.addLayout(subLayout)
        
        self.setLayout(layout)
        
    def onOKButtonClicked(self):
        self.accept()
        global thOsStart
        thOsStart.terminate()
        os._exit(0)
        
    def onCancelButtonClicked(self):
        self.reject()
        
    def showModal(self):
        return super().exec_()
        
class PopupWindow(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(810, 440, 300, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        subLayout = QHBoxLayout()
        txtContents = QLabel("Checked your Id or Password")
        txtContents.setFont(font)
        btnOK = QPushButton("Done")
        btnOK.clicked.connect(self.onOKButtonClicked)
    
        layout.addWidget(txtContents)
        subLayout.addWidget(btnOK)
        
        layout.addStretch(1)
        layout.addLayout(subLayout)
        
        self.setLayout(layout)
        
    def onOKButtonClicked(self):
        self.reject()
        
    def showModal(self):
        return super().exec_()
        
class PopupTimeSettingWindow(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        f = open("/home/pi/Desktop/Getron/getronBootTime", 'r')
        line = f.readline()
        f.close()
        self.setWindowTitle('Reboot Time Setting')
        self.setGeometry(810, 440, 350, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        subLayout = QHBoxLayout()
        self.txtContents = myEdit(line)
        self.txtContents.setMaxLength(2)
        self.txtContents.setFont(font)
        self.txtContents.clicked.connect(lambda: self.keyboard_on())
        btnOK = QPushButton("Save")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
    
        layout.addWidget(self.txtContents)
        subLayout.addWidget(btnCancel)
        subLayout.addWidget(btnOK)
        
        layout.addStretch(1)
        layout.addLayout(subLayout)
        
        self.setLayout(layout)
        
    def keyboard_on(self):
        keyboard_quit("matchbox-keyboard")
        subprocess.Popen(["matchbox-keyboard"])
        
    def onOKButtonClicked(self):
        keyboard_quit("matchbox-keyboard")
        f = open("/home/pi/Desktop/Getron/getronBootTime","w")
        print("length : " + str(len(self.txtContents.text())))
        if len(self.txtContents.text()) == 1:
            self.accept()
            f.write("0"+self.txtContents.text())
            f.close()
        elif len(self.txtContents.text()) == 2:
            if int(self.txtContents.text()) > 23:
                self.accept()
                f.write("04")
                f.close()
            else:
                self.accept()
                f.write(self.txtContents.text())
                f.close()
        else:
            self.accept()
            f.write("04")
            f.close()
            
    def onCancelButtonClicked(self):
        keyboard_quit("matchbox-keyboard")
        self.reject()
        
    def showModal(self):
        return super().exec_()
        
class MyApp(QMainWindow):
    clicked = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        global thOsStart
        print("myapp : " + str(widget.currentIndex()))
        qSetting = QSettings("TestPro", "infoFile")
        self.userNo = qSetting.value("userNo")
        self.siteNo = qSetting.value("siteNo")
        self.siteName = qSetting.value("siteName")
        
        self.setWindowTitle('key')
        self.move(0, 0)
        self.resize(1920, 1115)

        label1 = QLabel("light", self)
        label1.move(0, 0)
        label1.resize(1920, 1115)
        label1.setPixmap(QPixmap("/home/pi/Desktop/Getron/login_background.png").scaled(1920, 1115))

        label2 = QLabel("light", self)
        label2.move(300, 480)
        label2.resize(150, 120)
        label2.setPixmap(QPixmap("/home/pi/Desktop/Getron/login_logo.png").scaled(150, 120))

        self.editId = myEdit(self)
        self.editId.setPlaceholderText("Your E-mail")
        self.editId.move(200, 630)
        self.editId.resize(350, 50)
        self.editId.clicked.connect(lambda: self.keyboard_on())
        self.editId.setObjectName("userEmail")

        self.editPw = myEdit(self)
        self.editPw.setPlaceholderText("Password")
        self.editPw.move(200, 700)
        self.editPw.resize(350, 50)
        self.editPw.clicked.connect(lambda: self.keyboard_on())
        self.editPw.setObjectName("userPassword")
        self.editPw.setEchoMode(QLineEdit.Password)

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        buttonLogin = myLabel("Login", self)
        buttonLogin.move(200, 770)
        buttonLogin.resize(350, 50)
        buttonLogin.setStyleSheet("background-color: #3774D2;\ncolor: white;\nborder-radius: 8px;")
        buttonLogin.setAlignment(Qt.AlignCenter)
        buttonLogin.setFont(font)
        buttonLogin.clicked.connect(lambda: self._Login())

        buttonLogin1 = myLabel("Exit", self)
        buttonLogin1.move(1720, 1030)
        buttonLogin1.resize(175, 50)
        buttonLogin1.setStyleSheet("background-color: black;\ncolor: white;\nborder-radius: 8px;")
        buttonLogin1.setAlignment(Qt.AlignCenter)
        buttonLogin1.setFont(font)
        buttonLogin1.clicked.connect(lambda: self.app_exit())
        
        print("login")
        self.show()
        
#        thOsStart = Process(target=os_start,args=(),name="osCheck")
#        thOsStart.start()
#        thOsStart.join()
        
    def app_exit(self):
        keyboard_quit("matchbox-keyboard")
        win = SubWindow()
        r = win.showModal()
#        self.th2.terminate()
#        os._exit(0)
        
    def keyboard_on(self):
        keyboard_quit("matchbox-keyboard")
        subprocess.Popen(["matchbox-keyboard"])

    def afterClass(self):
        viewSettingView = ViewSetting()
        widget.addWidget(viewSettingView)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def _Login(self):
        keyboard_quit("matchbox-keyboard")
        if get_ip_address() == "127.0.0.1":
            test = False
            self._blabel = BubbleLabel()
            self._blabel.setText("network not connect")
            self._blabel.show()
        else:
            test = True
            try:
                r = requests.post(serverUrl+'/GetronRaspberry/loginProcess.do',
                              data={'email': self.editId.text(), 'password': self.editPw.text()}, timeout=2)
                
                if r:
                    json_data = json.loads(r.text)
                    if json_data["result"] == True:
                        self.editId.setText("")
                        self.editPw.setText("")
                        qSetting = QSettings("TestPro", "infoFile")
                        userNo = json_data["USER_NO"]
                        siteNo = json_data["SITE_NO"]
                        siteName = json_data["NAME"]

                        qSetting.setValue("userNo", userNo)
                        qSetting.setValue("siteNo", siteNo)
                        qSetting.setValue("siteName", siteName)

                        self.afterClass()
                    else:
                        print("login failed")
                        win = PopupWindow()
                        r = win.showModal()
            except Exception as e:
                print("except login failed")
                pass

class ViewSetting(QMainWindow):
    def __init__(self):
        super().__init__()
        print("viewSetting : " + str(widget.currentIndex()))
        self.selectPosition = -1
        qSetting = QSettings("TestPro", "infoFile")
        self.userNo = qSetting.value("userNo")
        self.siteNo = qSetting.value("siteNo")
        self.siteName = qSetting.value("siteName")
        self.viewType = qSetting.value("viewType")
        print("viewType : " + str(self.viewType))
        
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        background = myLabel("",self)
        background.move(0,0)
        background.resize(1920,1115)
        background.clicked.connect(lambda: self.bgTouch())
        background.setStyleSheet("background-color: #f0f0f6")
        
        siteNameTitle = QLabel("site Name", self)
        siteNameTitle.move(20,35)
        siteNameTitle.resize(350,65)
        siteNameTitle.setFont(font)
        
        fontName = QFont()
        fontName.setPointSize(14)
        siteName = QLabel(self.siteName, self)
        siteName.move(20,95)
        siteName.setFont(fontName)
        siteName.adjustSize()
        siteName.setStyleSheet("color: black;"
                             "background-color: white;"
                             "border-style: solid;"
                             "border-width: 2px;"
                             "border-color: #5E5F61;"
                             "border-radius: 8px;"
                             "padding: 12px;"
                             "min-height: 30px;"
                             "min-width: 380px")
                             
        typeTitle = QLabel("Select a view type", self)
        typeTitle.move(1350,55)
        typeTitle.setFont(font)
        typeTitle.resize(200,30)
        typeBox = QComboBox(self)
        typeBox.move(1350,95)
        typeBox.resize(200,50)
        typeBox.addItem('Process Type')
        typeBox.addItem('Tile Type')
        typeBox.addItem('Map Type')
        if self.viewType == None or self.viewType == "1" :
            typeBox.setCurrentIndex(0)
        elif self.viewType == "2" :
            typeBox.setCurrentIndex(1)
        else :
            typeBox.setCurrentIndex(2)
            
        typeBox.activated[str].connect(self.onActivated)
        
        viewTitle = QLabel("Select View", self)
        viewTitle.move(1600,55)
        viewTitle.setFont(font)
        viewTitle.resize(150,30)
        
        font = QFont()
        font.setPointSize(10)
        listTitle = QLabel("ProcessList", self)
        listTitle.move(1600,95)
        listTitle.setFont(font)
        listTitle.setStyleSheet("color: white;"
                                "background-color: #2D4667;")
        listTitle.resize(250,30)
        listTitle.setAlignment(Qt.AlignCenter)
        
        self.listWidget_Test = QListWidget(self)
        self.listWidget_Test.move(1600,125)
        self.listWidget_Test.resize(250,400)
        self.listWidget_Test.setUniformItemSizes(True)
        self.listWidget_Test.setResizeMode(QListView.Fixed)
        
        self.listWidget_Test.itemClicked.connect(self.chkItemClicked)
#        self.listWidget_Test.itemDoubleClicked.connect(self.chkItemDoubleClicked)
#        self.listWidget_Test.currentItemChanged.connect(self.chkCurrentItemChanged)

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        
        version = QLabel(versionStr,self)
        version.move(20, 1035)
        version.resize(130,45)
        version.setFont(font)
        version.setAlignment(Qt.AlignLeft|Qt.AlignCenter)
        ipAddress = QLabel("IP address : " + get_ip_address(),self)
        ipAddress.move(150, 1035)
        ipAddress.resize(350,45)
        ipAddress.setFont(font)
        ipAddress.setAlignment(Qt.AlignLeft|Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(14)
        
        timeSettingBtn = myLabel("Time Setting",self)
        timeSettingBtn.move(970, 1035)
        timeSettingBtn.resize(200,45)
        timeSettingBtn.setFont(font)
        timeSettingBtn.setAlignment(Qt.AlignCenter)
        timeSettingBtn.setStyleSheet("background-color: #3774D2;\ncolor: white;\nborder-radius: 8px;")
        timeSettingBtn.clicked.connect(lambda: self.timeSetting())
        
        logoutBtn = myLabel("Log out",self)
        logoutBtn.move(1200, 1035)
        logoutBtn.resize(200,45)
        logoutBtn.setFont(font)
        logoutBtn.setAlignment(Qt.AlignCenter)
        logoutBtn.setStyleSheet("background-color: #3774D2;\ncolor: white;\nborder-radius: 8px;")
        logoutBtn.clicked.connect(lambda: self._Logout())
        
        rebootBtn = myLabel("Reboot",self)
        rebootBtn.move(1430, 1035)
        rebootBtn.resize(200,45)
        rebootBtn.setFont(font)
        rebootBtn.setAlignment(Qt.AlignCenter)
        rebootBtn.setStyleSheet("background-color: #3774D2;\ncolor: white;\nborder-radius: 8px;")
        rebootBtn.clicked.connect(lambda: self._Reboot())
                
        doneBtn = myLabel("Confirm",self)
        doneBtn.move(1660, 1035)
        doneBtn.resize(200,45)
        doneBtn.setFont(font)
        doneBtn.setAlignment(Qt.AlignCenter)
        doneBtn.setStyleSheet("background-color: #3774D2;\ncolor: white;\nborder-radius: 8px;")
        doneBtn.clicked.connect(lambda: self.afterClass())
        
        if self.viewType == None or self.viewType == "1" :
            self.viewType = 1
            qSetting.setValue("viewType", "1")
        
        self._ViewList(str(self.viewType))
                
    def bgTouch(self) :
        keyboard_quit("matchbox-keyboard")
        
    def onActivated(self, text):
        print("select type : " + text)
        qSetting = QSettings("TestPro", "infoFile")
        if text == "Process Type":
            qSetting.setValue("viewType", "1")
            self._ViewList("1")
        elif text == "Tile Type":
            qSetting.setValue("viewType", "2")
            self._ViewList("2")
        else :
            qSetting.setValue("viewType", "3")
            self._ViewList("3")
        
    def chkItemClicked(self, index):
        print("currentRow : ",self.listWidget_Test.currentRow())
        self.selectPosition = self.listWidget_Test.currentRow()
        
    def timeSetting(self):
#        opener = "open" if sys.platform == "darwin" else "xdg-open"
#        subprocess.call([opener, '/home/pi/Desktop/Getron/getronBootTime'])
#        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/pi/Desktop/Getron/getronBootTime')
        win = PopupTimeSettingWindow()
        r = win.showModal()
            
    def _Logout(self):
        qSetting = QSettings("TestPro", "infoFile")
        qSetting.clear()
#        widget.setCurrentIndex(widget.currentIndex()-1)
        widget.removeWidget(widget.currentWidget())
    
    def _Reboot(self):
        os.system("reboot")
    
    def afterClass(self):
        if self.selectPosition == -1:
            print("process click")
        else:
            if get_ip_address() == "127.0.0.1":
                self._blabel = BubbleLabel()
                self._blabel.setText("network not connect")
                self._blabel.show()
            else:
                qSetting = QSettings("TestPro", "infoFile")
                qSetting.setValue("viewNo", str(processViewNoList[self.selectPosition]))
                webviewMain = WebviewMain()
                widget.addWidget(webviewMain)
                widget.setCurrentIndex(widget.currentIndex()+1)
    
    def _ViewList(self,text):
        if get_ip_address() == "127.0.0.1":
            print("network not connect")
            self._blabel = BubbleLabel()
            self._blabel.setText("network not connect")
            self._blabel.show()
        else:
            processNameList.clear()
            processViewNoList.clear()
            self.listWidget_Test.clear()
            try:
                r = requests.post(serverUrl+'/GetronRaspberry/viewList.do',
                              data={'viewType' : text,'siteNo' : str(self.siteNo)}, timeout=2)
                if r:
                    json_data = json.loads(r.text)
                    for obj in json_data :
                        processNameList.append(obj["TITLE"])
                        processViewNoList.append(str(obj["VIEW_NO"]))
                        self.listWidget_Test.addItem(obj["TITLE"])

            except Exception as e:
                print("except view list call failed")

class WebviewMain(QMainWindow):
    global driver
    def __init__(self):
        super().__init__()
        self.hover = False
        self.internetCheck = True
        print("webview : " + str(widget.currentIndex()))
        qSetting = QSettings("TestPro", "infoFile")
        self.userNo = qSetting.value("userNo")
        self.siteNo = qSetting.value("siteNo")
        self.siteName = qSetting.value("siteName")
        self.viewNo = qSetting.value("viewNo")
        
        self.viewType = qSetting.value("viewType")
        
        if self.viewType == None or self.viewType == "1" :
            self.url = "processRedirect.do"
            qSetting.setValue("viewType", "1")
        elif self.viewType == "2" :
            self.url = "tileRedirect.do"
        else :
            self.url = "mapRedirect.do"

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        
        labelBg = QLabel("",self)
        labelBg.setStyleSheet("background-color: white")
        labelBg.resize(1920,1115)
        labelBg.move(0,0)

        label = QLabel("The program is running.",self)
        label.setFont(font)
        label.resize(1920,50)
        label.move(0,235)
        label.setAlignment(Qt.AlignCenter)
        
        labelImg = QLabel("light", self)
        labelImg.move(0, 300)
        labelImg.resize(1920, 335)
        labelImg.setAlignment(Qt.AlignCenter)
        labelImg.setPixmap(QPixmap("/home/pi/Desktop/Getron/run-img.png").scaled(150, 150))
        
        font = QFont()
        font.setPointSize(12)
        
        self.logoutBtn = myLabel("View Settings",self)
        self.logoutBtn.move(885, 735)
        self.logoutBtn.resize(150,40)
        self.logoutBtn.setFont(font)
        self.logoutBtn.setAlignment(Qt.AlignCenter)
        self.logoutBtn.setStyleSheet("background-color: #3774D2;\ncolor: white;\nborder-radius: 8px;")
        self.logoutBtn.clicked.connect(lambda: self.beforeClass())
        self.logoutBtn.installEventFilter(self)
        
        self.win = SubWindow()
        self._ViewList11()

    def _ViewList11(self):
        if get_ip_address() == "127.0.0.1":
            print("network not connect")
            self._blabel = BubbleLabel()
            self._blabel.setText("network not connect")
            self._blabel.show()
            self.beforeClass()
        else:
            try:
                xprocessViewNoList.clear()
                r = requests.post(serverUrl+'/GetronRaspberry/viewList.do',
                              data={'viewType' : str(self.viewType),'siteNo' : str(self.siteNo)}, timeout=2)
        
                if r:
                    json_data = json.loads(r.text)
                    for obj in json_data :
                        xprocessViewNoList.append(str(obj["VIEW_NO"]))
                    
                    qSetting = QSettings("TestPro", "infoFile")
                    viewNo = qSetting.value("viewNo")
                    if not viewNo == None :
                        if str(viewNo) in xprocessViewNoList:
                            self.th1 = Process(target=self.chromium_check,args=(self.url,))
                            self.th1.start()
                        else :
                            print("None")
                            self.beforeClass()
                    else:
                        self.beforeClass()
            except Exception as e:
                print("except view list call failed")
                self.beforeClass()
                
    def beforeClass(self):
        try:
            self.th1.terminate()
            qSetting = QSettings("TestPro", "infoFile")
            qSetting.remove("viewNo")
            widget.removeWidget(widget.currentWidget())
        except:
            qSetting = QSettings("TestPro", "infoFile")
            qSetting.remove("viewNo")
            widget.removeWidget(widget.currentWidget())

    def internet_check(self,url):
        global driver
        print('internet check')
        if get_ip_address() == "127.0.0.1" :
                print('not connect internet')
                if self.internetCheck == True:
                    self.internetCheck = False
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get("file:///home/pi/Desktop/Getron/notConnected.html")
                
        else :
            print('connect internet')
            if self.internetCheck == False:
                self.internetCheck = True
                try:
                    driver.switch_to_window(driver.window_handles[0])
                    driver.get(serverUrl+"/GetronRaspberry/"+self.url+"?siteNo="+str(self.siteNo)+"&viewNo="+str(self.viewNo))
                except:
                    pass
        time.sleep(5)
        self.internet_check(url)
        
    def chromium_check(self,url):
        global driver
        print("chrome check")
        time.sleep(2)
        try:
            try:
                driver.window_handles
                print("chrome try")
                if get_ip_address() == "127.0.0.1" :
                    print('not connect internet')
                    if self.internetCheck == True:
                        self.internetCheck = False
                        driver.get("file:///home/pi/Desktop/Getron/notConnected.html")
                    
                else :
                    print('connect internet')
                    if self.internetCheck == False:
                        self.internetCheck = True
                        try:
                            driver.get(serverUrl+"/GetronRaspberry/"+self.url+"?siteNo="+str(self.siteNo)+"&viewNo="+str(self.viewNo))
                        except:
                            pass
            except NameError as e :
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(serverUrl+"/GetronRaspberry/"+self.url+"?siteNo="+str(self.siteNo)+"&viewNo="+str(self.viewNo))
                driver.implicitly_wait(80)
        except :
            print("chrome except")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(serverUrl+"/GetronRaspberry/"+self.url+"?siteNo="+str(self.siteNo)+"&viewNo="+str(self.viewNo))
            driver.implicitly_wait(80)
        time.sleep(58)
        self.chromium_check(url)
        
def keyboard_quit(kill):
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
            processID = proc.pid

            if processName == kill:
                parent_pid = processID
                parent = psutil.Process(parent_pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def internet_check_t(viewType, viewNo):
    if get_ip_address() == "127.0.0.1" :
        print('not connect internet')
        time.sleep(60)
        internet_check_t(viewType, viewNo)
    else :
        viewSettingView = ViewSetting()
        widget.addWidget(viewSettingView)
        if not viewNo == None :
            webviewMain = WebviewMain()
            widget.addWidget(webviewMain)
            widget.setCurrentIndex(2)
        else:
            widget.setCurrentIndex(1)

class BubbleLabel(QWidget):

    BackgroundColor = QColor(0, 0, 0)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text", "")
        super(BubbleLabel, self).__init__(*args, **kwargs)
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # Set minimum width and height
        self.setMinimumWidth(200)
        self.setMinimumHeight(58)
#        self.setAttribute(Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout(self)
        # Top left and bottom right margins (16 below because triangles are included)
        layout.setContentsMargins(0, 0, 0, 8)
        self.label = QLabel(self)
        self.label.setStyleSheet("color: #ffffff")
        self.label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.label)
        self.setText(text)
        # Get screen height and width
        self._desktop = QApplication.instance().desktop()

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.close()

    def show(self):
        super(BubbleLabel, self).show()
        # Window start position
        startPos = QPoint(
            860,
            900)
        endPos = QPoint(
            860,
            900)
        self.move(startPos)
        # Initialization animation
        print("start : " + str(startPos) + " end : " + str(endPos))
        self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        # Transparency animation
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        # Set the animation curve
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(2000)
        # Moving up animation
        moveAnimation = QPropertyAnimation(self, b"pos")
        moveAnimation.setStartValue(startPos)
        moveAnimation.setEndValue(endPos)
        moveAnimation.setEasingCurve(QEasingCurve.InQuad)
        moveAnimation.setDuration(2000)
        # Parallel animation group (the purpose is to make the two animations above simultaneously)
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(moveAnimation)
        # Close window at the end of the animation
        self.animationGroup.finished.connect(self.close)
        self.animationGroup.start()

    def paintEvent(self, event):
        super(BubbleLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Antialiasing

        rectPath = QPainterPath()                     # Rounded Rectangle
        triPath = QPainterPath()                      # Bottom triangle

        height = self.height() - 8                    # Offset up 8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 5, 5)
        x = self.width() / 5 * 4
        triPath.moveTo(x, height)                     # Move to the bottom horizontal line 4/5
        # Draw triangle
        triPath.lineTo(x + 6, height + 8)
        triPath.lineTo(x + 12, height)

#        rectPath.addPath(triPath)                     # Add a triangle to the previous rectangle

        # Border brush
        painter.setPen(QPen(self.BorderColor, 1, Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        # Background brush
        painter.setBrush(self.BackgroundColor)
        # Draw shape
        painter.drawPath(rectPath)
        # Draw a line on the bottom of the triangle to ensure the same color as the background
        painter.setPen(QPen(self.BackgroundColor, 1,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(x, height, x + 12, height)

    def windowOpacity(self):
        return super(BubbleLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(BubbleLabel, self).setWindowOpacity(opacity)

    # Since the opacity property is not in QWidget, you need to redefine one
    opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)
    
def os_start():
    now = datetime.datetime.now()
    print("date : " + str(now))
    print("Time = %s:%s" % (now.hour, now.minute))
    qSetting = QSettings("TestPro", "infoFile")
    day = qSetting.value("day")
    siteNo = qSetting.value("siteNo")
    if day == None:
        qSetting.setValue("day",str(now.day))
        day = str(now.day)
    
    if not siteNo == None:
#        if now.minute == 5 or now.minute == 15 or now.minute == 25 or now.minute == 35 or now.minute == 45 or now.minute == 55:
        if now.hour == 12 and now.minute == (int(siteNo)%60):
            time.sleep(60)
            qSetting.setValue("day",str(now.day))
            f = open("/home/pi/Desktop/Getron/getronMainLog","a")
            f.write("\n"+str(now))
            f.close()
            print("os reboot")
            os.system("reboot")
        else :
            time.sleep(60)
            os_start()
    else:
        time.sleep(60)
        os_start()
    
if __name__ == '__main__':
    qSetting = QSettings("TestPro", "infoFile")
    userNo = qSetting.value("userNo")
    siteNo = qSetting.value("siteNo")
    siteName = qSetting.value("siteName")
    viewType = qSetting.value("viewType")
    viewNo = qSetting.value("viewNo")
    
    global thOsStart
    global driver
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    ex = MyApp()
    widget.addWidget(ex)
    
    widget.setFixedHeight(1115)
    widget.setFixedWidth(1920)
    widget.setGeometry(QRect(0, -30, 1920, 1115))
#    widget.setGeometry(QRect(0, 0, 1920, 1080))
#    widget.showFullScreen()
    
    jobs = []
    thOsStart = Process(target=schedule_reboot)
    jobs.append(thOsStart)
    thOsStart.start()
    
    if not userNo == None :
        
        if not get_ip_address() == "127.0.0.1" :
            viewSettingView = ViewSetting()
            widget.addWidget(viewSettingView)
            if not viewNo == None :
                webviewMain = WebviewMain()
                widget.addWidget(webviewMain)
                widget.setCurrentIndex(2)
            else:
                widget.setCurrentIndex(1)
            widget.show()
        else :
            widget.show()
            internet_check_t(viewType,viewNo)
    else:
        widget.show()
        
    sys.exit(app.exec_())




