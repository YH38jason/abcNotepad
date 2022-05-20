# coding=utf-8
import wx
from tkinter import messagebox
from tkinter import Tk
import sys
import json
window = Tk()
window.withdraw()


class MainFrame(wx.Frame):
    def __init__(self):
        self.file_i = ''
        self.file_path = ''
        self.is_open = False
        super().__init__(None, title=strings['title'], size=(1000, 800))
        # 创建菜单
        bar = wx.MenuBar
        # 创建面板
        panel = wx.Panel(self)
        # 创建文本框
        self.tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE) 
        self.text_c = wx.TextCtrl(panel)
        # 创建按钮
        save_b = wx.Button(panel, label=strings["save"])
        open_b = wx.Button(panel, label=strings["open"])

        # 添加容器
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 将控件添加至容器
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND, border=0)
        hbox.Add(save_b, proportion=0, flag=wx.ALIGN_LEFT | wx.ALL, border=10)
        hbox.Add(open_b, proportion=0, flag=wx.ALL, border=10)
        vbox.Add(self.tc, proportion=5, flag=wx.EXPAND | wx.ALL, border=20)
        hbox.Add(self.text_c, proportion=1, flag=wx.ALL, border=10)
        # 设置面板布局
        panel.SetSizer(vbox)

        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.save_file, save_b)
        self.Bind(wx.EVT_BUTTON, self.open_file, open_b)
        # 显示窗口
        self.Show()

    # 保存文件

    def save_file(self, event):
        if not self.is_open:
            messagebox.showinfo(title='提示', message='你没有打开文件')
            return
        self.file_i = self.tc.GetValue()

    # 打开文件

    def open_file(self, event):
        self.file_path = self.text_c.GetValue()
        if self.file_path == '':
            print('未输入路径！')
            messagebox.showinfo(title='提示', message='你没有输入文件路径！')
            return
        try:
            with open(self.file_path, 'r') as f:
                self.file_i = f.read()
                self.tc.SetValue(self.file_i)
            self.is_open = True
        except FileNotFoundError:
            messagebox.showerror(title='错误', message=f'未找到文件\'{self.file_path}\'')
            print('未找到文件{}'.format(self.file_path))
        except PermissionError:
            messagebox.showerror(title='错误', message=f'无法打开文件\'{self.file_path}\'，这也许不是一个文件！')
            print(f'无法打开文件\'{self.file_path}\'，这也许不是一个文件！')


def Close(event):
    try:
        if not main_frame.is_open:
            main_frame.Destroy()
            sys.exit()
        if main_frame.tc.GetValue() != main_frame.file_i:
            choose = messagebox.askyesno(title='提示', message='您还没有保存！确定退出吗？')
            if choose:
                main_frame.Destroy()
                sys.exit()
            else:
                return
        with open(main_frame.file_path, 'w') as f:
            text = main_frame.tc.GetValue()
            f.write(text)
        main_frame.Destroy()
        print('程序已关闭')
        sys.exit()
    except FileNotFoundError:
        main_frame.Destroy()
        print('程序已关闭')
        sys.exit()

if __name__ == '__main__':
    with open('languages\lang_config.json', 'r', encoding='utf-8') as lc:
        lconfig = json.load(lc)
        ls = open('languages\strings.json', 'r', encoding='utf-8')
        strings=json.load(ls)["cn"]
    app = wx.App()
    main_frame = MainFrame()
    main_frame.Bind(wx.EVT_CLOSE, Close)
    app.MainLoop()
