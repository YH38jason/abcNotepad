# coding=utf-8
import wx
import sys
import json
import sqlite3
import os
import webbrowser
app = wx.App()
# 构建图片
save_p = wx.Image("images\\save.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
open_p = wx.Image("images\\open.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
setting_p = wx.Image("images\\setting.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
his_p = wx.Image("images\\history.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
new_p = wx.Image("images\\new.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
about_p = wx.Image("images\icon-200x200.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
find_p = wx.Image("images\\find.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
replace_p = wx.Image('images\\replace.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
icon = wx.Icon('images\\icon.png', wx.BITMAP_TYPE_PNG)
icon2 = wx.Icon('images\setting.png', wx.BITMAP_TYPE_PNG)
icon3 = wx.Icon("images\\history.png", wx.BITMAP_TYPE_PNG)
icon4 = wx.Icon('images\\about.png', wx.BITMAP_TYPE_PNG)

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
        self.tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_RICH2) 
        self.path_tc = wx.FilePickerCtrl(panel, message=strings['select-file'])
        # 创建按钮
        save_b = wx.BitmapButton(panel, bitmap=save_p)
        open_b = wx.BitmapButton(panel, bitmap=open_p)
        setting_b = wx.BitmapButton(panel, bitmap=setting_p)
        his_b = wx.BitmapButton(panel, bitmap=his_p)
        new_b = wx.BitmapButton(panel, bitmap=new_p)
        find_b = wx.BitmapButton(panel, bitmap=find_p)
        # 添加容器
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer()
        # 将控件添加至容器
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND, border=0)
        hbox.Add(save_b, proportion=0, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        hbox.Add(open_b, proportion=0, flag=wx.ALL, border=5)
        hbox.Add(new_b, proportion=0, flag=wx.ALL, border=5)
        hbox.Add(his_b, proportion=0, flag=wx.ALL, border=5)
        vbox.Add(self.tc, proportion=5, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.path_tc, proportion=1, flag=wx.ALL, border=5)
        hbox.Add(setting_b, proportion=0, flag=wx.ALL, border=5)
        hbox2.Add(find_b)
        vbox.Add(hbox2, flag=wx.ALL | wx.EXPAND, border=5)
        # 设置面板布局
        panel.SetSizer(vbox)
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.save_file, save_b)
        self.Bind(wx.EVT_BUTTON, self.open_file, open_b)
        self.Bind(wx.EVT_BUTTON, self.open_setting, setting_b)
        self.Bind(wx.EVT_CLOSE, Close)
        self.Bind(wx.EVT_BUTTON, self.open_history,his_b)
        self.Bind(wx.EVT_BUTTON, self.new_file, new_b)
        self.Bind(wx.EVT_BUTTON, self.FindShow, find_b)
        self.Bind(wx.EVT_FIND, self.OnFind)
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
    # 打开查找窗口
    def FindShow(self, event):
        self.data = wx.FindReplaceData()
        self.dlg = wx.FindReplaceDialog(self.tc, self.data, 'Find')
        self.dlg.Show()
    # 查找
    def OnFind(self, event):
        pos = 0
        txt = self.tc.GetValue()
        ftxt = self.data.GetFindString()          
        pos = txt.find(ftxt, pos)
        size = len(ftxt) 
        self.tc.SetStyle(pos, pos+size, wx.TextAttr("white", "blue"))
    # 打开设置
    def open_setting(self, event):
        self.setting_frame=SettingFrame()
    # 打开历史
    def open_history(self, event):
        self.history_frame=HistoryFrame()
    def new_file(self, event):
        self.nf = NewFileFrame()
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
        abutton = wx.Button(panel, label=strings['about'])
        vbox.Add(stext, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALL, border=5)
        vbox.Add(self.cbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(delb, flag=wx.ALL|wx.ALIGN_RIGHT, border=5)
        vbox.Add(abutton, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        vbox.Add(cbutton, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.determine, cbutton)
        self.Bind(wx.EVT_BUTTON, self.delete_history, delb)
        self.Bind(wx.EVT_BUTTON, self.open_about, abutton)
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
    def open_about(self, event):
        self.about = AboutFrame()
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
        try:
            new_file_path = self.fpk.GetValue()+self.ntc.GetValue()
            if new_file_path == '':
                wx.MessageBox(strings['no-input'], strings['prompt'], wx.ICON_INFORMATION)
                self.Destroy()
                return
            f = open(new_file_path, 'w')
            f.close()
            self.Destroy()
            main_frame.open_from_path(new_file_path)
        except FileNotFoundError:
            wx.MessageBox(strings['not-found1'], strings['prompt'], wx.ICON_INFORMATION)
class AboutFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=strings['about'], size=(400, 500))
        panel = wx.Panel(self)
        self.SetIcon(icon4)
        stbmp = wx.StaticBitmap(panel, bitmap=about_p)
        t1 = wx.StaticText(panel, label=strings['a1'])
        t2 = wx.StaticText(panel, label=strings['icc'])
        github_button = wx.Button(panel, label='Github')
        bilibili_button = wx.Button(panel, label='Bilibili')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, proportion=1,flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=1,flag=wx.EXPAND)
        vbox.Add(t2, proportion=6,flag=wx.ALL, border=20)
        hbox2.Add(github_button, flag=wx.ALL, border=10)
        hbox2.Add(bilibili_button, flag=wx.ALL, border=10)
        hbox.Add(stbmp, proportion=1, flag=wx.ALL, border=10)
        hbox.Add(t1, proportion=4, flag=wx.TOP|wx.BOTTOM, border=30)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.github, github_button)
        self.Bind(wx.EVT_BUTTON, self.bilibili, bilibili_button)
        self.Show()
    def github(self, event):
        webbrowser.open('https://github.com/YH38jason/abcNotepad')
    def bilibili(self, event):
        webbrowser.open('https://space.bilibili.com/1306084387')
def Close(event):
    try:
        if not main_frame.is_open:
            EXIT()
        if main_frame.tc.GetValue() != main_frame.file_i:
            choose = wx.MessageBox(strings["not-save"], strings["prompt"], wx.OK | wx.CANCEL | wx.ICON_WARNING)
            if choose == 4:
                EXIT()
            else:
                return
        _, fn = os.path.split(main_frame.file_path)
        AddHistoryFile(path=main_frame.file_path, file_name=fn)
        con.close()
        with open(main_frame.file_path, 'w') as f:
            text = main_frame.tc.GetValue()
            f.write(text)
        EXIT()
    except FileNotFoundError:
        EXIT()

def EXIT():
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