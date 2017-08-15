
---
# ChangeLog

## 20170714 - v1.3.31
 - 完善docs

## 20170604 - v1.3.30
 - 添加docs

## 20170602 - v1.3.29
 - 更新README.md，添加图片
 
## 20170530 - v1.3.28
 - 优化显示密码界面

## 20170529 - v1.3.27
 - 美化ssid和key的文本框显示

## 20170527 - v1.3.26
 - 实现gui-qt托盘图标
 
## 20170527 - v1.3.25
 - 实现手动选择所共享的连接
 - 分离qt-gui界面类，实现动态切换语言
 - 优化Json配置类的结构
 - WifiShare类每次获取用户数量，都对hostednetwork status进行一次更新
 - 更改.py文件名称
 
## 20170526 - v1.3.20
 - 添加gui-qt图标
 
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
