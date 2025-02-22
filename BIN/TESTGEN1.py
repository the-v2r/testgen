import sys, os, shutil, random, subprocess, tkinter
import tkinter as tk
from termcolor import colored
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter.filedialog import askopenfile

# KHOI TAO
root = Tk()
root.title("Chương trình tạo test cases Python (By Nguyen Van Hai) - V1.0")
root.geometry("200x540")
# ===========

foldF = 0
fileF = 0

#UI
label_name = Label(root, text="Tên file")
label_name.pack()
entry_name = Entry(root)
entry_name.pack()

label_num = Label(root, text="Số tests cần tạo")
label_num.pack()
entry_num = Entry(root)
entry_num.pack()

label_file = Label(root, text="Upload file code chuẩn")
label_file.pack()
entry_file = tk.Button(root, text="Upload", command=lambda:upload_file())
entry_file.pack()
entry_file_check = Entry(root)
entry_file_check.insert(0, "[filepath]")
entry_file_check.pack()

label_fold = Label(root, text="Chọn thư mục chứa tests")
label_fold.pack()
entry_fold = tk.Button(root, text="Browse", command=lambda:upload_fold())
entry_fold.pack()
entry_fold_check = Entry(root)
entry_fold_check.insert(0, "[folderpath]")
entry_fold_check.pack()

label_inp = Label(root, text="Số lượng kí tự trong INPUT")
label_inp.pack()
entry_inp = Entry(root)
entry_inp.pack()
inp_num_entry = tk.Button(root, text="Tùy chỉnh", command=lambda:option())
inp_num_entry.pack()
inp_num_check = tk.Entry(root)
inp_num_check.pack()
inp_demo = tk.scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=15)
inp_demo.pack()

submit_entry = tk.Button(root, text="TẠO TESTS", command=lambda:submit_form())
submit_entry.pack()

credit = Label(root, text="Chương trình được tạo bởi")
credit.pack()
despcredit = Label(root, text="NGUYỄN VĂN HẢI")
despcredit.pack()

#upload file + folder
def upload_fold():
    fold = filedialog.askdirectory(title="CHỌN THƯ MỤC CHỨA TESTS").replace("/", "\\\\")
    entry_fold_check.delete(0,END)
    entry_fold_check.insert(0, str(fold)+"\\\\")
    return str(fold)

def upload_file():
    file = filedialog.askopenfilename(title="CHỌN FILE CODE CHUẨN").replace("/", "\\\\")
    entry_file_check.delete(0,END)
    entry_file_check.insert(0, str(file))
    return str(file)

# ==================================

def option():
    root2 = Toplevel(root)

    def ButtonBlock(self):
        self.label = []
        self.field1 = []
        self.field2 = []

        for i in range(1, int(entry_inp.get())+1):
            self.label.append(tk.Label(root2, text=str(i)))
            self.field1.append(tk.Entry(root2))
            self.field2.append(tk.Entry(root2))
            self.label[-1].pack()
            self.field1[-1].pack()
            self.field2[-1].pack()

        saveBtn = tk.Button(root2, text="SAVE", command=lambda:close_option())
        saveBtn.pack()

        def close_option():
            inp_num_check.delete(0, END)
            for i in range(0, int(entry_inp.get())):
                inp_num_check.insert(END, self.field1[i].get()+"~"+self.field2[i].get() + " ")
            root2.destroy()

            fin = []
            res = []
            dat = inp_num_check.get().split(" ")
            for k in range(0, int(entry_num.get())):                
                for i in range(0, len(dat)-1):
                    pie = dat[i].split("~")
                    res.append(str(random.randint(int(pie[0]), int(pie[1]))))
                print(" ".join(res))
                fin.append(" ".join(res))
                res.clear()

            inp_demo.insert(tk.INSERT, "\n".join(fin))
            inp_demo.configure(state = 'disabled')
            

    root2.title("Tùy chọn file INP")
    root2.geometry("200x"+str(int(entry_inp.get())*60+40))
    ButtonBlock(root2)

# inp()

def excute():
    name = entry_name.get()
    num_tests = int(entry_num.get())
    
    path_pri = entry_fold_check.get() + "\\"
    
    subprocess.run("Pyinstaller -y " + entry_file_check.get() + " --distpath " + path_pri + "BIN\\dist" + " --workpath " + path_pri + "BIN\\build" + " --specpath " + path_pri + "BIN")
    
    if os.path.isdir(path_pri + name):
        shutil.rmtree(path_pri + name)
    
    os.makedirs(path_pri + name)
    
    sub_path = path_pri + name
    
    old_stdout = sys.stdout
    print("TESTS:")

    fileF = inp_demo.get("1.0", tkinter.END).split("\n")
    fileF.pop(int(entry_num.get()))
    
    for i in fileF:
        a = fileF.index(i) + 1
        if a <= 9:
            num = "00" + str(a)
        elif a >= 10 and a <= 99:
            num = "0" + str(a)
        else:
            num = str(a)
    
        os.makedirs(sub_path + "\\" + "TEST"+num)
        test_path = sub_path + "\\" + "TEST"+num
        sys.stdout = open(test_path + "\\" + name + ".inp", "w")
        print(i)
        sys.stdout = old_stdout
        print(num, end=" ")
    
        # CODE GIAI BAI TOAN
        sys.stdin = open(test_path + "\\" + name + ".inp", "r")
        sys.stdout = open(test_path + "\\" + name + ".out", "w")
        subprocess.call(path_pri + "BIN\\dist\\" + name + "\\" + name, stdin = sys.stdin, stdout = sys.stdout )
        # =============================================
        
    sys.stdout.close()

    box()

def box():
    root3 = Toplevel(root)
    root3.title("Thành công!")
    a = tk.Label(root3, text="Bạn đã tạo thành công " + str(entry_num.get()) + " tests.")
    a.pack()
    b = tk.Button(root3, text="Thoát", command=lambda:root.destroy())
    b.pack()

#collect data
def submit_form():
    nameData = entry_name.get()
    numData = entry_num.get()
    submit_data = [str(nameData), str(numData)]
    print(submit_data)
    excute()
    return submit_data

root.mainloop() 