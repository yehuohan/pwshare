
---
# pwshare
 - windows下wifi热点软件，基于python3.6，现主要开发程序为gui-qt(PyQt5)版本，命令行与gui-tk版本为阶段性成果

---
# FileList
 - pyws.py        : 使用netsh开启wifi热点的库
 - pwshare.py     : 命令行封装程序
 - pwshare-tk.pyw : tkinter-gui封装程序
 - pwshare-qt.pyw : qt-gui封装程序
 - lang           : qt-gui语言文件
 - ws			  : ws.dll工程，用于管理连接共享

# Make-exe
 - 按下列步骤生成exe文件
```
# 先使用pyinstaller生成exe
cd pwshare
pyinstaller --uac-admin -w pyshare-qt.pyw

# 然后将lang和ws工程生成的ws.dll复制到./dist/pwshare-qt下
```
 
---
# TODO
 - gui-qt添加手动选择所共享的连接
 - gui-qt中英文切换选项
 - gui-qt显示wifi连接用户数量


---
# Contributors 
 - yehuohan - yehuohan@gamil.com, 550034086@qq.com


---
# ChangeLog
## 20170525 - v1.3.19
 - 添加LICENSE到远程仓库

## 20170525 - v1.3.18
 - 添加c++ ws.dll库，并使用python调用ws.dll，实现自动管理共享连接
 - 更改pwshare.py，使用新版WifiShare
 - 将.gitignore文件添加到远程仓库
 
## 20170523 - v1.2.15
 - 在开启wifi后添加设置共享连接的提示

## 20170519 - v1.2.14
 - WifiShare添加显示Wifi状态等功能
 - 实现Wifi开启状态保存功能

## 20170518 - v1.2.12
 - 完善README.md

## 20170518 - v1.2.11
 - 没有json配置文件时，自动创建

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
