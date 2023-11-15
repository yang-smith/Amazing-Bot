import tkinter as tk
from tkinter import filedialog


def choose_bookmarks_file():
    """ 弹出文件选择对话框让用户选择文件 """
    root = tk.Tk()
    root.withdraw()  # 隐藏 Tkinter 主窗口
    file_path = filedialog.askopenfilename(
        filetypes=[("HTML files", "*.html")],
        title="选择书签文件"
    )
    root.destroy()
    return file_path