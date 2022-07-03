# coding=utf-8

"""
发布地址:https://1drv.ms/u/s!AmfWVyfgkF2_hx73sbeabmAOm5_2?e=M3DJKn
"""
import wx
import sys
import json
import sqlite3
import os
import webbrowser
import requests

version = '2.0 beta'
app = wx.App()

# 构建图片
save_p = wx.Image("images\\save.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
open_p = wx.Image("images\\open.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
setting_p = wx.Image("images\\setting.png",
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap()
his_p = wx.Image("images\\history.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
new_p = wx.Image("images\\new.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
about_p = wx.Image("images/icon-200x200.png",
                   wx.BITMAP_TYPE_PNG).ConvertToBitmap()
find_p = wx.Image("images\\find.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
tran_p = wx.Image("images/translate.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
replace_p = wx.Image('images\\replace.png',
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap()
run_p = wx.Image("images/run.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
icon = wx.Icon('images\\icon.png', wx.BITMAP_TYPE_PNG)
icon2 = wx.Icon('images\setting.png', wx.BITMAP_TYPE_PNG)
icon3 = wx.Icon("images\\history.png", wx.BITMAP_TYPE_PNG)
icon4 = wx.Icon('images\\about.png', wx.BITMAP_TYPE_PNG)


class MainFrame(wx.Frame):
    def __init__(self):
        self.file_i = ''
        self.file_path = ''
        self.is_open = False
        self.file_name = ''
        self.isFind = False
        self.index_list = []
        self.find_index = 0
        super().__init__(None, title=strings['title'].format(version), size=(800, 600))
        self.SetIcon(icon)
        self.Centre()
        self.key_find = wx.NewIdRef()
        self.key_save = wx.NewIdRef()
        self.key_open = wx.NewIdRef()
        self.key_exit = wx.NewIdRef()
        self.RegisterHotKey(self.key_find, wx.MOD_ALT,
                            wx.WXK_DOWN)
        self.RegisterHotKey(self.key_save, wx.MOD_ALT, wx.WXK_UP)
        self.RegisterHotKey(self.key_open, wx.MOD_ALT, wx.WXK_LEFT)
        self.RegisterHotKey(self.key_exit, wx.MOD_ALT, wx.WXK_ESCAPE)
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
        self.find_tc = wx.TextCtrl(panel, size=(200, 28))
        tran_b = wx.BitmapButton(panel, bitmap=tran_p)
        hk = wx.Button(panel, label=strings['hk'])
        runb = wx.BitmapButton(panel, bitmap=run_p)
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
        hbox2.Add(self.find_tc)
        vbox.Add(hbox2, flag=wx.ALL | wx.EXPAND, border=5)
        hbox2.Add(tran_b)
        hbox2.Add(hk)
        hbox2.Add(runb)
        # 设置面板布局
        panel.SetSizer(vbox)
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.save_file, save_b)
        self.Bind(wx.EVT_BUTTON, self.open_file, open_b)
        self.Bind(wx.EVT_BUTTON, self.open_setting, setting_b)
        self.Bind(wx.EVT_CLOSE, Close)
        self.Bind(wx.EVT_BUTTON, self.open_history, his_b)
        self.Bind(wx.EVT_BUTTON, self.new_file, new_b)
        self.Bind(wx.EVT_HOTKEY, self.OnFindHotkey, id=self.key_find)
        self.Bind(wx.EVT_BUTTON, self.OnTran, tran_b)
        self.Bind(wx.EVT_HOTKEY, self.save_file, id=self.key_save)
        self.Bind(wx.EVT_HOTKEY, self.open_file, id=self.key_open)
        self.Bind(wx.EVT_HOTKEY, Close, id=self.key_exit)
        self.Bind(wx.EVT_BUTTON, self.open_hotkeyzy, hk)
        self.Bind(wx.EVT_BUTTON, self.run, runb)
        # self.Bind(wx.EVT_BUTTON, self.FindShow, find_b)
        # self.Bind(wx.EVT_FIND, self.OnFind)
        # 显示窗口
        self.is_setting_open = False
        self.is_history_open = False
        self.is_hotkeyzy_open = False
        self.is_newfile_open = False
        self.is_runfile_open = False
        self.Show()

    # 保存文件
    def save_file(self, event):
        if not self.is_open:
            wx.MessageBox(strings['not-open'],
                          strings["prompt"], wx.ICON_INFORMATION)
            return
        self.file_i = self.tc.GetValue()

    def open_hotkeyzy(self, event):
        if not self.is_hotkeyzy_open:
            self.hk_frame = HotKeyFrame()
            self.is_hotkeyzy_open = True

    # 打开文件

    def open_file(self, event):
        self.file_path = self.path_tc.GetPath()
        if self.file_path == '':
            wx.MessageBox(strings['no-input'],
                          strings["prompt"], wx.ICON_INFORMATION)
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.file_i = f.read()
                _, self.file_name = os.path.split(self.file_path)
                self.SetTitle('{}-{}'.format(strings['title'].format(version), self.file_name))
                self.tc.SetValue(self.file_i)
            self.is_open = True
        except FileNotFoundError:
            wx.MessageBox(strings["not-found1"]+""+self.file_path +
                          strings['not-found2'], strings['error'], wx.ICON_ERROR)
        except PermissionError:
            wx.Messagebox(strings['p1']+self.file_path +
                          strings['p2'], strings['error'], wx.ICON_ERROR)
    # 从路径打开文件

    def open_from_path(self, p):
        self.file_path = p
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.file_i = f.read()
                _, self.file_name = os.path.split(self.file_path)
                self.SetTitle('{}-{}'.format(strings['title'].format(version), self.file_name))
                self.tc.SetValue(self.file_i)
            self.is_open = True
        except FileNotFoundError:
            wx.MessageBox(strings['error'],
                          strings["can-not-open-hf"], wx.ICON_ERROR)
            self.path_tc.SetValue('')

    # 打开设置
    def open_setting(self, event):
        if not self.is_setting_open:
            self.setting_frame = SettingFrame()
            self.is_setting_open = True
    # 打开历史

    def open_history(self, event):
        if not self.is_history_open:
            self.history_frame = HistoryFrame()
            self.is_setting_open = True

    def new_file(self, event):
        if not self.is_newfile_open:
            self.nf = NewFileFrame()
            self.is_newfile_open = True
    
    def run(self, event):
        self.run_file_frame = RunFileFrame()
        self.is_runfile_open = True

    # def FindShow(self, event):
    #     self.find_frame = FindFrame()
    #     self.find_frame.Show()

    # 按下查找热键
    def OnFindHotkey(self, event):
        if self.isFind:
            self.FindLoop(self.index_list)
            return
        nftxt: str = main_frame.tc.GetValue()
        # sele: int = nftxt.find(self.find_tc.GetValue())
        index = nftxt.find(self.find_tc.GetValue())
        self.index_list.append(index)
        while index != -1:
            index = nftxt.find(self.find_tc.GetValue(), index+1)
            if index == -1:
                break
            self.index_list.append(index)
        self.find_index = 0
        self.isFind = True
        self.FindLoop(self.index_list)
            
        # if sele == -1:
        #     wx.MessageBox(strings["not-found-txt"].format(self.find_tc.GetValue()),
        #                   strings['prompt'], wx.ICON_INFORMATION)
        # main_frame.tc.SetSelection(sele, sele+len(self.find_tc.GetValue()))

    def FindLoop(self, l:list):
        if self.find_index == len(l):
            self.isFind = False
            return
        long = len(self.find_tc.GetValue())
        self.tc.SetSelection(l[self.find_index], l[self.find_index]+long)
        self.find_index += 1
    # 翻译

    def OnTran(self, event):
        try:
            trantxt = self.tc.GetValue()
            if trantxt == '':
                return
            results = translate(trantxt)
            with open('translate/'+strings['tranre']+'.txt', 'w', encoding='utf-8') as f:
                f.write(results)
        except requests.exceptions.JSONDecodeError:
            return
        except requests.exceptions.ConnectionError:
            wx.MessageBox(strings['cb'], strings['error'], wx.ICON_ERROR)
            return

# 设置


class SettingFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['setting'], size=(300, 400))
        panel = wx.Panel(self)
        self.Centre()
        self.SetIcon(icon2)
        self.cbox = wx.ComboBox(panel, value='中文', choices=lang_list)
        stext = wx.StaticText(panel, label=strings['lang-set'])
        vbox = wx.BoxSizer(wx.VERTICAL)
        delb = wx.Button(panel, label=strings['del-his'])
        cbutton = wx.Button(panel, label=strings['determine'])
        abutton = wx.Button(panel, label=strings['about'])
        vbox.Add(stext, flag=wx.ALL | wx.ALIGN_LEFT | wx.ALL, border=5)
        vbox.Add(self.cbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(delb, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        vbox.Add(abutton, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        vbox.Add(cbutton, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.determine, cbutton)
        self.Bind(wx.EVT_BUTTON, self.delete_history, delb)
        self.Bind(wx.EVT_BUTTON, self.open_about, abutton)
        self.Bind(wx.EVT_CLOSE, self.close)
        panel.SetSizer(vbox)
        self.Show()

    def determine(self, event):
        try:
            ls = open('languages\strings.json', 'r', encoding='utf-8')
            global strings
            global lang
            strings = json.load(ls)[lconfig[self.cbox.GetValue()]]

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
    def close(self, event):
        main_frame.is_setting_open = False
        self.Destroy()


class HistoryFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['history'], size=(300, 400))
        panel = wx.Panel(self)
        self.SetIcon(icon3)
        self.Center()
        hlist = get_all_history()
        self.plist = []
        self.nlist = []
        for h in hlist:
            i1, i2 = h
            self.nlist.append(i1)
            self.plist.append(i2)
        self.list_box = wx.ListBox(
            panel, choices=self.nlist, style=wx.LB_SINGLE)
        apply_b = wx.Button(panel, label=strings['apply'])
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.list_box, proportion=7,
                 flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(apply_b, proportion=1, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.use_history_file, apply_b)
        self.Bind(wx.EVT_CLOSE, self.close)
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
    
    def close(self, event):
        main_frame.is_history_open = False
        self.Destroy()


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
        hbox.Add(stext2, flag=wx.ALL, border=2)
        hbox.Add(self.ntc, flag=wx.ALL | wx.EXPAND, border=2)
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(b, flag=wx.ALL | wx.ALIGN_LEFT, border=5)
        self.Bind(wx.EVT_BUTTON, self.create, b)
        self.Bind(wx.EVT_CLOSE, self.close)
        panel.SetSizer(vbox)
        self.Center()
        self.Show()

    def create(self, event):
        try:
            new_file_path = self.fpk.GetValue()+self.ntc.GetValue()
            if new_file_path == '':
                wx.MessageBox(strings['no-input'],
                              strings['prompt'], wx.ICON_INFORMATION)
                self.Destroy()
                return
            f = open(new_file_path, 'w')
            f.close()
            self.Destroy()
            main_frame.open_from_path(new_file_path)
        except FileNotFoundError:
            wx.MessageBox(strings['not-found1'],
                          strings['prompt'], wx.ICON_INFORMATION)
    def close(self, event):
        main_frame.is_newfile_open = False
        self.Destroy()


class AboutFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=strings['about'], size=(400, 500))
        panel = wx.Panel(self)
        self.SetIcon(icon4)
        stbmp = wx.StaticBitmap(panel, bitmap=about_p)
        t1 = wx.StaticText(panel, label=strings['a1'].format(version))
        t2 = wx.StaticText(panel, label=strings['icc'])
        github_button = wx.Button(panel, label='Github')
        bilibili_button = wx.Button(panel, label='Bilibili')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=1, flag=wx.EXPAND)
        vbox.Add(t2, proportion=6, flag=wx.ALL, border=20)
        hbox2.Add(github_button, flag=wx.ALL, border=10)
        hbox2.Add(bilibili_button, flag=wx.ALL, border=10)
        hbox.Add(stbmp, proportion=1, flag=wx.ALL, border=10)
        hbox.Add(t1, proportion=4, flag=wx.TOP | wx.BOTTOM, border=30)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.github, github_button)
        self.Bind(wx.EVT_BUTTON, self.bilibili, bilibili_button)
        self.Show()

    def github(self, event):
        webbrowser.open('https://github.com/YH38jason/abcNotepad')

    def bilibili(self, event):
        webbrowser.open('https://space.bilibili.com/1306084387')


# class FindFrame(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title=strings['find'], size=(379, 170))
#         self.panel = FindPanel(self)
#         self.Bind(wx.EVT_BUTTON, self.OnFind, self.panel.fb)

#     def OnFind(self, event):
#         nftxt: str = main_frame.tc.GetValue()
#         sele: int = nftxt.find(self.panel.m_textCtrl2.GetValue())
#         main_frame.tc.SetSelection(0, 3)


def Close(event):
    main_frame.UnregisterHotKey(main_frame.key_find)
    try:
        if not main_frame.is_open:
            EXIT()
        if main_frame.tc.GetValue() != main_frame.file_i:
            choose = wx.MessageBox(
                strings["not-save"], strings["prompt"], wx.OK | wx.CANCEL | wx.ICON_WARNING)
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

# By wxFromBuilder


class FindPanel (wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(379, 200), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos,
                          size=size, style=style, name=name)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.m_textCtrl2 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl2, 0, wx.ALL | wx.EXPAND, 10)
        self.fb = wx.Button(
            self, wx.ID_ANY, strings['find'], wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.fb, 0, wx.ALL, 10)
        self.cb1 = wx.CheckBox(
            self, wx.ID_ANY, strings['case'], wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.cb1, 0, wx.ALL, 10)
        self.SetSizer(bSizer1)
        self.Layout()


def translate(txt: str):
    url = 'http://fanyi.youdao.com/translate'
    data = {
        "i": txt,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }
    res = requests.post(url, data=data)
    return res.json()["translateResult"][0][0]['tgt']

class HotKeyFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['hk'])
        self.label = """1、退出:ALT+ESC  
2、保存:ALT+方向键上  
3、打开:ALT+方向键左
"""
        panel = wx.Panel(self)
        hotkey_st = wx.StaticText(panel, label=self.label)
        box = wx.BoxSizer()
        box.Add(hotkey_st, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        panel.SetSizer(box)
        self.Center()
        self.Show()

    def close(self, event):
        main_frame.is_hotkeyzy_open = False
        self.Destroy()
        
class RunFileFrame(wx.Frame):
    def __init__(self):
        super().__init__(main_frame, title=strings['run'])
        panel = wx.Panel(self)
        Terminal = wx.TextCtrl(panel, style=wx.TE_MULTILINE, value='Terminal output......')
        Terminal.Enable(False)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(Terminal, flag=wx.ALL | wx.EXPAND, border=5, proportion=1)
        if not main_frame.is_open:
            wx.MessageBox(strings['not-open'], strings['prompt'], wx.ICON_INFORMATION)
        panel.SetSizer(vbox)
        self.Center()
        self.Show()

        output = os.popen('python '+main_frame.file_path).read()
        Terminal.SetValue(output)
        Terminal.Enable()

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
    # 读取字符串json文件
    with open('languages\lang_config.json', 'r', encoding='utf-8') as lc:
        lconfig = json.load(lc)
        ls = open('languages\strings.json', 'r', encoding='utf-8')
        lang = lconfig['default_lang']
        strings = json.load(ls)[lang]
        ls.close()
    lang_list = lconfig['languages']
    main_frame = MainFrame()
    app.MainLoop()
