#import tkinter as tk   # 这种导入方式类似于from ... imort *   
from tkinter import *
## 这个*表示所有都选择，所以这句话的意思是导入所有tkinter 里面的函数
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from unicodedata import name


class Application(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.dir = ''
        self.create_widgets()
        self.create_login_widgets()
        self.create_textboard_widgets()

    def create_textboard_widgets(self):
        self.textboard = Text(self, bg= "gray", font= "楷体",foreground= "white",height=20,width=20)
        self.textboard.pack()

        self.textboard.insert(1.0, "真好用")  # 1.0 表示1行0列 ，行是从1开始列是从0开始 INSERT 表示光标处，END表示尾部
        self.textboard.insert(1.2, "插入一个文本")



    def create_login_widgets(self):
        self.label01 = Label(self, text= '用户名')
        self.label01.pack()
        text01 = StringVar()
        text01.set("liufei")
        self.entry01 = Entry(self, textvariable= text01 )
        self.entry01.pack()
        text01.get()

        self.label02 = Label(self, text= "密码")
        self.label02.pack()
        text02 = StringVar()
        self.entry02 = Entry(self, textvariable= text02, show="*")
        self.entry02.pack()
        text02.get()

        self.btnstart = Button(self, text= "开始", command= self.login)
        self.btnstart.pack()

    def login(self):
        username  = self.entry01.get()
        psw = self.entry02.get()


        print("用户名："+username)
        print("密码："+psw)
        print("数据库比对中...")

        if username == "liufei" and psw == "12345":
            messagebox.showinfo("登陆提示","登陆成功！")
        else:
            messagebox.showerror("登陆提示", "登陆失败! 请检查用户名和密码！")

        

    def create_widgets(self):

        self.btn01 = Button(self, text = '选择文件夹', command = self.get_dir)
        ##### 这里的command = self.get_dir 不能打括号，否则会直接用，而不是传给command
        self.btn01.pack()



    def get_dir(self):
        self.dir = askdirectory(initialdir='D:\\', title='选择文件夹')
        print(self.dir)

if __name__ == '__main__':

    root = Tk()         #  创建一个Tk窗口设为根窗口root  k是小写符号

    root.title('程序名称')
    root.geometry("300x300+300+300")  # 定义窗口大小和窗口距离屏幕最左上角的位置 ，这里不是*号是字母x
    tool = Application(root)   

    root.mainloop()


