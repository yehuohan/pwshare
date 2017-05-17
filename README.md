
---
# pwshare
## Introduction
 - windows下wifi热点软件，基于python3.6，现主要开发程序为gui-qt(PyQt5)版本，命令行与gui-tk版本为阶段性成果

## Information
 - brief  : windows下使用python建立wifi热点
 - e-mail : 550034086@qq.com, yehuohan@gmail.com
 - author : yehuohan

---
# FileList
 - WifiShare.py    : 使用netsh开启wifi热点的库
 - pwshare.py      : 命令行封装程序
 - pwshare-gui.pyw : tkinter-gui封装程序
 - pwshare-qt.pyw  : qt-gui封装程序
 - lang            : qt-gui语言文件
 
---
# TODO
 - 每次开启需要重新设置Internet连接共享（选去掉，再选上）
 - 管理员打开问题
 - gui-qt动态显示信息 

---
# Log
## 20170517 - v1.2.10
 - 移除cmd文件
 - lbl_status同样显示返回的错误值
 
## 20170517 - v1.2.8
 - 增加json配置
 - 修复gui-tk打开与重启逻辑错误

## 20170517 - v1.2.6
 - 修复WifiShare.create_wifi bug(不能马上以提供的参数创建wifi热点)
 - 去掉WifiShare.print_wifi和WifiShare.restart_wifi函数
 - WifiShare的start_wifi, close_wifi, create_wifi使用subprocess.getstatusoutput执行命令，并返回结果
 - 完善qt-gui界面与显示信息，修复关闭wifi的逻辑Bug

## 20170517 - v1.2.2
 - 添加qt-gui，基于pyqt5(由qt5.7.0编译而来)
 - 添加语言文件(zh_CN)
 
## 20170516 - v1.1.0
 - 添加tkinter-gui

## 20170515 - v1.0.0
 - command-line版wifi共享，使用python编写，附加cmd版作为参考
