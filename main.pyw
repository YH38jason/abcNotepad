# coding=utf-8
from email import message
import wx
import sys
import json
import sqlite3
import os
app = wx.App()
# 构建图片
save_p = wx.Image("images\\save.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
open_p = wx.Image("images\\open.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
setting_p = wx.Image("images\\setting.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
his_p = wx.Image("images\\history.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
new_p = wx.Image("images\\new.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
icon = wx.Icon('images\icon.png', wx.BITMAP_TYPE_PNG)
icon2 = wx.Icon('images\setting.png', wx.BITMAP_TYPE_PNG)
icon3 = wx.Icon("images\\history.png", wx.BITMAP_TYPE_PNG)

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
        self.path_tc = wx.FilePickerCtrl(panel, message=strings['select-file'])
        # 创建按钮
        save_b = wx.BitmapButton(panel, bitmap=save_p)
        open_b = wx.BitmapButton(panel, bitmap=open_p)
        setting_b = wx.BitmapButton(panel, bitmap=setting_p)
        his_b = wx.BitmapButton(panel, bitmap=his_p)
        new_b = wx.BitmapButton(panel, bitmap=new_p)
        # 添加容器
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 将控件添加至容器
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND, border=0)
        hbox.Add(save_b, proportion=0, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        hbox.Add(open_b, proportion=0, flag=wx.ALL, border=5)
        hbox.Add(new_b, proportion=0, flag=wx.ALL, border=5)
        hbox.Add(his_b, proportion=0, flag=wx.ALL, border=5)
        vbox.Add(self.tc, proportion=5, flag=wx.EXPAND | wx.ALL, border=20)
        hbox.Add(self.path_tc, proportion=1, flag=wx.ALL, border=5)
        hbox.Add(setting_b, proportion=0, flag=wx.ALL, border=5)
        # 设置面板布局
        panel.SetSizer(vbox)
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.save_file, save_b)
        self.Bind(wx.EVT_BUTTON, self.open_file, open_b)
        self.Bind(wx.EVT_BUTTON, self.open_setting, setting_b)
        self.Bind(wx.EVT_CLOSE, Close)
        self.Bind(wx.EVT_BUTTON, self.open_history,his_b)
        self.Bind(wx.EVT_BUTTON, self.new_file, new_b)
        # 显示窗口
        self.Show()

    # 保存文件

    def save_file(self, event):
        if not self.is_open:
            wx.MessageBox(strings['not-open'],strings["prompt"],wx.ICON_INFORMATION)
            return
        self.file_i = self.tc.GetValue()

    # 打开文件

    def open_file(self, event):
        self.file_path = self.path_tc.GetPath()
        if self.file_path == '':
            wx.MessageBox(strings['no-input'],strings["prompt"], wx.ICON_INFORMATION)
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.file_i = f.read()
                self.tc.SetValue(self.file_i)
            self.is_open = True
        except FileNotFoundError:
            wx.MessageBox(strings["not-found1"]+""+self.file_path+strings['not-found2'],strings['error'],wx.ICON_ERROR)
        except PermissionError:
            wx.Messagebox(strings['p1']+self.file_path+strings['p2'], strings['error'], wx.ICON_ERROR)
    # 从路径打开文件
    def open_from_path(self, p):
        self.file_path = p
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.file_i = f.read()
                self.tc.SetValue(self.file_i)
            self.is_open = True
        except FileNotFoundError:
            wx.MessageBox(strings['error'], strings["can-not-open-hf"] ,wx.ICON_ERROR)
            self.path_tc.SetValue('')
        
    # 打开设置
    def open_setting(self, event):
        setting_frame=SettingFrame()
    # 打开历史
    def open_history(self, event):
        history_frame=HistoryFrame()
    def new_file(self, event):
        nf = NewFileFrame()
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
        delb = wx.Button(panel, label=strings['del-his'])
        cbutton=wx.Button(panel, label=strings['determine'])
        vbox.Add(stext, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALL, border=5)
        vbox.Add(self.cbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(delb, flag=wx.ALL|wx.ALIGN_RIGHT, border=5)
        vbox.Add(cbutton, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.determine, cbutton)
        self.Bind(wx.EVT_BUTTON, self.delete_history, delb)
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
    def delete_history(self, event):
        delete_all()
class HistoryFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['history'], size=(300,400))
        panel=wx.Panel(self)
        self.SetIcon(icon3)
        self.Center()
        hlist = get_all_history()
        self.plist = []
        self.nlist = []
        for h in hlist:
            i1, i2 = h
            self.nlist.append(i1)
            self.plist.append(i2)
        self.list_box = wx.ListBox(panel, choices=self.nlist, style=wx.LB_SINGLE)
        apply_b = wx.Button(panel, label=strings['apply'])
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.list_box,proportion=7,flag=wx.EXPAND|wx.ALL, border=5)
        vbox.Add(apply_b, proportion=1, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.use_history_file, apply_b)
        self.Show()
    def use_history_file(self, event):
        if self.list_box.GetSelection() == -1:
           self.Destroy()
           return
        self.Destroy()
        restart()
        p = self.plist[self.list_box.GetSelection()]
        main_frame.path_tc.SetPath(p)
        main_frame.open_from_path(p)

class NewFileFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['new'], size=(300, 180))
        panel = wx.Panel(self)
        self.SetIcon(icon)
        stext = wx.StaticText(panel, label=strings['select-path']+' :')
        stext2 = wx.StaticText(panel, label=strings['name'])
        self.ntc = wx.TextCtrl(panel)
        self.fpk = wx.TextCtrl(panel)
        b = wx.Button(panel, label=strings['determine'])
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(stext, flag=wx.ALL, border=5)
        vbox.Add(self.fpk, flag=wx.ALL | wx.EXPAND, border=5)
        hbox = wx.BoxSizer()
        hbox.Add(stext2, flag=wx.ALL, border = 2)
        hbox.Add(self.ntc, flag=wx.ALL|wx.EXPAND, border=2)
        vbox.Add(hbox, flag=wx.EXPAND|wx.ALL, border=5)
        vbox.Add(b, flag=wx.ALL|wx.ALIGN_LEFT, border=5)
        self.Bind(wx.EVT_BUTTON, self.create, b)
        panel.SetSizer(vbox)
        self.Center()
        self.Show()
    
    def create(self, event):
        new_file_path = self.fpk.GetValue()+self.ntc.GetValue()
        f = open(new_file_path, 'w')
        f.close()
        self.Destroy()
        main_frame.open_from_path(new_file_path)
def Close(event):
    try:
        if not main_frame.is_open:
            main_frame.Destroy()
            sys.exit()
        if main_frame.tc.GetValue() != main_frame.file_i:
            choose = wx.MessageBox(strings["not-save"], strings["prompt"], wx.OK | wx.CANCEL | wx.ICON_WARNING)
            if choose == 4:
                main_frame.Destroy()
                sys.exit()
            else:
                return
        _, fn = os.path.split(main_frame.file_path)
        AddHistoryFile(path=main_frame.file_path, file_name=fn)
        con.close()
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
    main_frame.tc.SetValue(main_frame.file_i)
    main_frame.path_tc.SetPath(main_frame.file_path)

# 添加历史
def AddHistoryFile(file_name, path):
    cursor.execute("INSERT INTO history VALUES(?, ?)", (file_name, path))
    con.commit()
# 删除历史
def delete_all():
    cursor.execute("DELETE FROM history")
    con.commit()
# 获取历史
def get_all_history():
    command = 'SELECT file_name, path FROM history'
    cursor.execute(command)
    return cursor.fetchall()

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