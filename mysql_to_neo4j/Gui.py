import tkinter as tk
import neo4jClass
import sqlClass
import N2S
import sys
import threading
import multiprocessing
class ConsoleRedirect:
    def __init__(self, console):
        self.console = console
    def write(self, s):
        self.console.insert(tk.END, s)
        self.console.see(tk.END)


np=0
mp=0
n2s=0
window = tk.Tk()
window.geometry("800x800")
window.resizable(width=False, height=False)

lable1 = tk.Label(window, text='neo4j地址:')
lable1.place(relx=0.1, rely=0.1)
entry1 = tk.Entry(window)
entry1.insert(0, 'http://localhost:7474')
entry1.place(relx=0.1, rely=0.2)
text1=''

lable2 = tk.Label(window, text='neo4j密码:')
lable2.place(relx=0.1, rely=0.3)
entry2 = tk.Entry(window)
entry2.place(relx=0.1, rely=0.4)
text2=''

lable3 = tk.Label(window, text='neo4j库名:')
lable3.place(relx=0.1, rely=0.5)
entry3 = tk.Entry(window)
entry3.insert(0, 'neo4j')
entry3.place(relx=0.1, rely=0.6)
text3=''

lable4 = tk.Label(window, text='mysql主机地址:')
lable4.place(relx=0.5, rely=0.1)
entry4 = tk.Entry(window)
entry4.place(relx=0.5, rely=0.2)
entry4.insert(0, 'localhost')
text4=''

lable5 = tk.Label(window, text='mysql用户名:')
lable5.place(relx=0.5, rely=0.3)
entry5 = tk.Entry(window)
entry5.place(relx=0.5, rely=0.4)
entry5.insert(0, 'root')
text5=''

lable6 = tk.Label(window, text='mysql密码:')
lable6.place(relx=0.5, rely=0.5)
entry6 = tk.Entry(window)
entry6.place(relx=0.5, rely=0.6)
text6=''

lable7 = tk.Label(window, text='mysql数据库名:')
lable7.place(relx=0.5, rely=0.7)
entry7 = tk.Entry(window)
entry7.place(relx=0.5, rely=0.8)
text7=''

p = 0
t=0
def medium():
    n2s.transit()

def new_thread_for_transit():
    global p
    global n2s
    global t
    p = threading.Thread(target=medium)
    t=threading.Thread(target=thread_end_call)

    p.start()
    t.start()

def thread_end_call():
    global p
    p.join()
    print('import successful')
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


button2 = tk.Button(window, text='确认导入', command=new_thread_for_transit)
console = tk.Text(window, height=5, width=50)
sys.stdout = ConsoleRedirect(console)


#console.place(relx=0.0,rely=0.8)

def get_str_from_entry():
    global n2s
    global mp
    global np
    global button2
    global button1
    text1=entry1.get()
    text2=entry2.get()

    text3=entry3.get()
    text4=entry4.get()
    text5=entry5.get()
    text6=entry6.get()

    text7=entry7.get()


    try:
        np=neo4jClass.Neo4jOperation(key=text2,url=text1,name=text3)
        mp=sqlClass.SqlOperation(host=text4,user=text5,password=text6,database=text7)
        n2s=N2S.N2S(np=np,mp=mp,sql_database=text7)


        button2.pack()
        console.pack()
        button1.destroy()


    except:
        print("error of input")

button1 = tk.Button(window, text='确认',command=get_str_from_entry)
button1.place(relx=0.3, rely=0.9)



window.mainloop()
