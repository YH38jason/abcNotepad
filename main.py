# coding=utf-8
import os
from turtle import settiltangle
import wx
from tkinter import VERTICAL, messagebox
from tkinter import Tk
import sys
import json
import sqlite3
window = Tk()
window.withdraw()
app = wx.App()
# 构建图片
save_p = wx.Image("images\\save.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
open_p = wx.Image("images\\open.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
setting_p = wx.Image("images\\setting.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
his_p = wx.Image("images\\history.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
icon = wx.Icon('images\icon.png', wx.BITMAP_TYPE_PNG)
icon2 = wx.Icon('images\setting.png', wx.BITMAP_TYPE_PNG)

class MainFrame(wx.Frame):
    def __init__(self):
        self.file_i = ''
        self.file_path = ''
        self.is_open = False
        super().__init__(None, title=strings['title'], size=(1000, 800))
        self.SetIcon(icon)
        self.Centre()
        # 创建面板
        panel = wx.Panel(self)
        # 创建文本框
        self.tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE) 
        self.text_c = wx.TextCtrl(panel)
        # 创建按钮
        save_b = wx.BitmapButton(panel, bitmap=save_p)
        open_b = wx.BitmapButton(panel, bitmap=open_p)
        setting_b = wx.BitmapButton(panel, bitmap=setting_p)
        his_b = wx.BitmapButton(panel, bitmap=his_p)
        # 添加容器
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 将控件添加至容器
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND, border=0)
        hbox.Add(save_b, proportion=0, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        hbox.Add(open_b, proportion=0, flag=wx.ALL, border=5)
        hbox.Add(setting_b, proportion=0, flag=wx.ALL, border=5)
        vbox.Add(self.tc, proportion=5, flag=wx.EXPAND | wx.ALL, border=20)
        hbox.Add(self.text_c, proportion=1, flag=wx.ALL, border=5)
        hbox.Add(his_b, proportion=0, flag=wx.ALL, border=5)
        # 设置面板布局
        panel.SetSizer(vbox)
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.save_file, save_b)
        self.Bind(wx.EVT_BUTTON, self.open_file, open_b)
        self.Bind(wx.EVT_BUTTON, self.open_setting, setting_b)
        self.Bind(wx.EVT_CLOSE, Close)
        # 显示窗口
        self.Show()

    # 保存文件

    def save_file(self, event):
        if not self.is_open:
            messagebox.showinfo(title=strings["prompt"], message=strings['not-open'])
            return
        self.file_i = self.tc.GetValue()

    # 打开文件

    def open_file(self, event):
        self.file_path = self.text_c.GetValue()
        if self.file_path == '':
            messagebox.showinfo(title=strings["prompt"], message=strings['no-input'])
            return
        try:
            with open(self.file_path, 'r') as f:
                self.file_i = f.read()
                self.tc.SetValue(self.file_i)
            self.is_open = True
        except FileNotFoundError:
            messagebox.showerror(title=strings['error'], message=strings["not-found1"]+""+self.file_path+strings['not-found2'])
        except PermissionError:
            messagebox.showerror(title=strings['error'], message=strings['p1']+self.file_path+strings['p2'])
    
    # 打开设置
    def open_setting(self, event):
        setting_frame=SettingFrame()
# 设置        
class SettingFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['setting'], size=(300,400))
        panel=wx.Panel(self)
        self.Centre()
        self.SetIcon(icon2)
        self.cbox=wx.ComboBox(panel, value='中文', choices=lang_list)
        stext=wx.StaticText(panel, label=strings['lang-set'])
        vbox=wx.BoxSizer(wx.VERTICAL)
        cbutton=wx.Button(panel, label=strings['determine'])
        vbox.Add(stext, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALL, border=5)
        vbox.Add(self.cbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(cbutton, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.determine, cbutton)
        panel.SetSizer(vbox)
        self.Show()
    def determine(self, event):
        try:
            ls = open('languages\strings.json', 'r', encoding='utf-8')
            global strings
            global lang
            strings=json.load(ls)[lconfig[self.cbox.GetValue()]]
        except json.decoder.JSONDecodeError as e:
            print(f'json Error:{e}')
        finally:
            ls.close()
            restart()
            self.Destroy()
class HistoryFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['setting'], size=(300,400))
        panel=wx.Panel(self)
def Close(event):
    con.close()
    try:
        if not main_frame.is_open:
            main_frame.Destroy()
            sys.exit()
        if main_frame.tc.GetValue() != main_frame.file_i:
            choose = messagebox.askyesno(title=strings["prompt"], message=strings["not-save"])
            if choose:
                main_frame.Destroy()
                sys.exit()
            else:
                return
        with open(main_frame.file_path, 'w') as f:
            text = main_frame.tc.GetValue()
            f.write(text)
        main_frame.Destroy()
        sys.exit()
    except FileNotFoundError:
        main_frame.Destroy()
        sys.exit()

def restart():
    global main_frame
    main_frame.Destroy()
    main_frame = MainFrame()

# 添加历史
def AddHistoryFile(file_name, path):
    cursor.execute("INSERT INTO history VALUES(?, ?)", (file_name, path))
    con.commit()

def delete_all():
    cursor.execute("truncate history")
    con.commit()

if __name__ == '__main__':
    # 连接数据库
    con = sqlite3.connect('data.db')
    cursor = con.cursor()
    # 初始化字符串文件
    with open('languages\lang_config.json', 'r', encoding='utf-8') as lc:
        lconfig = json.load(lc)
        ls = open('languages\strings.json', 'r', encoding='utf-8')
        lang = lconfig['default_lang']
        strings=json.load(ls)[lang]
        ls.close()
    lang_list=lconfig['languages']
    main_frame = MainFrame()
    app.MainLoop()
