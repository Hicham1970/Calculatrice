from tkinter import *
import math
import tkinter.messagebox
import clipboard
from PIL import Image, ImageTk


root = Tk()
root.title('Scientific calculator')
root.configure(background='DarkGoldenrod1')
root.iconbitmap("calc.ico")
root.resizable(width=False, height=False)
root.geometry('400x568+0+0')

menu_frm = Frame(root)
menu_frm.grid()
# ----------------------------------Entry information----------------------#
display_entry = Entry(menu_frm,
                      font=('arial', 20, 'bold'),
                      bg='SpringGreen2',
                      bd=30, width=22,
                      justify='right')
display_entry.grid(row=0, column=0, columnspan=4, pady=1)


# ---------------------------------T54B-------------------------------#
class T54BCalculator:
    def __init__(self, density_entry, temperature_entry, result_label):
        self.density_entry = density_entry
        self.temperature_entry = temperature_entry
        self.result_label = result_label

    def T54B(self):
        try:
            density = float(self.density_entry.get())
            temperature = float(self.temperature_entry.get())

            dens = density * 1000
            X = int((dens * 100 + 25) / 50) * 0.5
            Y = int((temperature * 1000 + 25) / 50) * 0.05

            if 653 <= X <= 770.5:
                A1 = int(10000000000 * 346.4228 / X / X) / 10000000000
                B1 = int(10000000000 * 0.4388 / X) / 10000000000
                C1 = int(10000000 * (A1 + B1) + 0.5) / 10000000
            elif 770.5 < X <= 787.5:
                A1 = int(10000000000 * 2680.3206 / X / X) / 10000000000
                C1 = int(10000000 * (A1 - 0.00336312) + 0.5) / 10000000
            elif 787.5 < X <= 839:
                A1 = int(10000000000 * 594.5418 / X / X) / 10000000000
                C1 = int(10000000 * A1 + 0.5) / 10000000
            elif 839 < X <= 1075:
                A1 = int(10000000000 * 186.9696 / X / X) / 10000000000
                B1 = int(10000000000 * 0.4862 / X) / 10000000000
                C1 = int(10000000 * (A1 + B1) + 0.5) / 10000000
            else:
                self.result_label.config(text="False")
                return

            D = Y - 15
            E1 = -(C1 * D) - (0.8 * C1 * C1 * D * D)
            E = int(100000000 * E1) / 100000000
            F = int(math.exp(E) * 100000000 + 0.5) / 100000000
            F = int(F * 10000 + 0.5) / 10000

            self.result_label.config(text=str(F))
        except ValueError:
            self.result_label.config(text="Invalid input")


# ... (existing code)
def table54b():
    tab = Toplevel()
    tab.title('T54B')
    tab.iconbitmap("calc.ico")
    tab.resizable(0, 0)

    # Create labels
    Label(tab, text="Temperature:").grid(row=0, column=0, sticky="e")
    Label(tab, text="Density:").grid(row=1, column=0, sticky="e")
    Label(tab, text="Result:").grid(row=2, column=0, sticky="e")

    # Create entries
    temperature_entry = Entry(tab)
    temperature_entry.grid(row=0, column=1)
    density_entry = Entry(tab)
    density_entry.grid(row=1, column=1)
    result_label = Label(tab, text="")
    result_label.grid(row=2, column=1)

    # Create the button
    t54b_calculator = T54BCalculator(density_entry, temperature_entry, result_label)
    calculate_button = Button(tab, text="Calculate", command=t54b_calculator.T54B)
    calculate_button.grid(row=3, columnspan=2)

    tab.mainloop()


# ---------------------------------T54A-------------------------------#
class T54ACalculator:
    def __init__(self, density_entry, temperature_entry, result_label):
        self.density_entry = density_entry
        self.temperature_entry = temperature_entry
        self.result_label = result_label

    def T54A(self):
        try:
            density = float(self.density_entry.get())
            temperature = float(self.temperature_entry.get())

            C = density * 1000
            D = int((613.9723 / (C * C)) / 0.0000001 + 0.5) * 0.0000001
            F = temperature - 15
            G = int((D * F) / 0.00000001 + 0.5) * 0.00000001
            H = int((0.8 * G) / 0.00000001 + 0.5) * 0.00000001
            Y = math.exp(-G * (H + 1))
            result = int(Y / 0.0001 + 0.5) * 0.0001

            self.result_label.config(text=str(result))
        except ValueError:
            self.result_label.config(text="Invalid input")


def table54a():
    tab = Toplevel()
    tab.title('T54A')
    tab.iconbitmap("calc.ico")
    tab.resizable(0, 0)

    # Create labels
    Label(tab, text="Temperature:").grid(row=0, column=0, sticky="e")
    Label(tab, text="Density:").grid(row=1, column=0, sticky="e")
    Label(tab, text="Result:").grid(row=2, column=0, sticky="e")

    # Create entries
    temperature_entry = Entry(tab)
    temperature_entry.grid(row=0, column=1)
    density_entry = Entry(tab)
    density_entry.grid(row=1, column=1)
    result_label = Label(tab, text="")
    result_label.grid(row=2, column=1)

    # Create the button
    calculate_button = Button(tab, text="Calculate",
                              command=T54ACalculator(density_entry, temperature_entry, result_label).T54A)
    calculate_button.grid(row=3, columnspan=2)

    tab.mainloop()


# ----------------------------------CALCULATOR PART----------------------------------#
class Calculator:
    def __init__(self):
        self.total = 0
        self.current = ''
        self.input_value = True
        self.check_sum = False
        self.operator = ''
        self.result = False

    def numberEnter(self, num):
        self.result = False
        first_num = display_entry.get()
        second_num = str(num)
        if self.input_value:
            self.current = second_num
            self.input_value = False
        else:
            if second_num == '.':
                if second_num in first_num:
                    return
            self.current = first_num + second_num
        self.display(self.current)

    def sum_of_total(self):
        self.result = True
        self.current = float(self.current)
        if self.check_sum == True:
            self.valid_function()

    def valid_function(self):
        if self.operator == 'add':
            self.total += self.current
        if self.operator == 'sub':
            self.total -= self.current
        if self.operator == 'mult':
            self.total *= self.current
        if self.operator == 'div':
            self.total /= self.current
        if self.operator == 'mod':
            self.total %= self.current

        self.input_value = True
        self.check_sum = False
        self.display(self.total)

    def operators(self, operator):
        self.current = float(self.current)
        if self.check_sum:
            self.valid_function()
        elif not self.result:
            self.total = self.current
            self.input_value = True
        self.check_sum = True
        self.operator = operator
        self.result = False

    def display(self, value):
        display_entry.delete(0, END)
        display_entry.insert(0, value)

    def clear(self):
        self.result = False
        if len(self.current) > 0:
            if len(self.current) == 1:
                self.display(0)
                self.input_value = True
            else:
                self.current = self.current[0:len(self.current) - 1]
                self.display(self.current)
        else:
            self.display(0)
            self.input_value = True

    def clear_all(self):
        self.display(0)
        self.input_value = True

    def plus_minus(self):
        self.result = False
        self.current = -(float(display_entry.get()))
        self.display(self.current)

    def pi(self):
        self.result = False
        self.current = math.pi
        self.display(self.current)

    def twopi(self):
        self.result = False
        self.current = math.tau
        self.display(self.current)

    def deg(self):
        self.result = False
        self.current = math.degrees(float((display_entry.get())))
        self.display(self.current)

    def cos(self):
        self.result = False
        self.current = math.cos(float((display_entry.get())))
        self.display(self.current)

    def sin(self):
        self.result = False
        self.current = math.sin(float((display_entry.get())))
        self.display(self.current)

    def acoshyp(self):
        self.result = False
        self.current = math.acosh(float((display_entry.get())))
        self.display(self.current)

    def asinh(self):
        self.result = False
        self.current = math.asinh(float((display_entry.get())))
        self.display(self.current)

    def atanhyp(self):
        self.result = False
        self.current = math.atanh(float((display_entry.get())))
        self.display(self.current)

    def coshyp(self):
        self.result = False
        self.current = math.cosh(float((display_entry.get())))
        self.display(self.current)

    def sinhyp(self):
        self.result = False
        self.current = math.sinh(float(display_entry.get()))
        self.display(self.current)

    def tan(self):
        self.result = False
        self.current = math.tan(float(display_entry.get()))
        self.display(self.current)

    def tanhyp(self):
        self.result = False
        self.current = math.tanh(float(display_entry.get()))
        self.display(self.current)

    def log(self):
        self.result = False
        self.current = math.log(float(display_entry.get()))
        self.display(self.current)

    def log2(self):
        self.result = False
        a = float(display_entry.get())
        if a < 0:
            self.display("Can't log negatif numbers")
        elif a == 0:
            self.display("Can't zero")
        else:
            self.current = math.log2(float(display_entry.get()))
            self.display(self.current)

    def log10(self):
        self.result = False
        self.current = math.log10(float(display_entry.get()))
        self.display(self.current)

    def log1p(self):
        self.result = False
        self.current = math.log1p(float(display_entry.get()))
        self.display(self.current)

    def lgamma(self):
        self.result = False
        self.current = math.lgamma(float(display_entry.get()))
        self.display(self.current)

    def exp(self):
        self.result = False
        self.current = math.exp(float(display_entry.get()))
        self.display(self.current)

    def exmp1(self):
        self.result = False
        self.current = math.expm1(float(display_entry.get()))
        self.display(self.current)

    def sqrt(self):
        self.result = False
        self.current = math.sqrt(float((display_entry.get())))
        self.display(self.current)

    def e(self):
        self.result = False
        self.current = math.e
        self.display(self.current)

    def cut_text(self, event=None):
        if event:
            event.widget.event_generate("<<Cut>>")

    def copy_text(self, event=None):
        if event:
            event.widget.event_generate("<<Copy>>")

    def paste_text(self, event=None):
        if event:
            event.widget.event_generate("<<Paste>>")

    # Bind keyboard shortcuts for cut, copy, and paste
    root.bind('<Control-x>', cut_text)
    root.bind('<Control-c>', copy_text)
    root.bind('<Control-v>', paste_text)


add_value = Calculator()
# ---------------------------------Buttons--------------------------------#
number_str = "789456123"
btn = []
i = 0
for j in range(2, 5):
    for k in range(3):
        btn.append(Button(menu_frm, width=5, height=2, font=('arial', 20, 'bold'), bd=4, text=number_str[i]))
        btn[i].grid(row=j, column=k, pady=1)
        btn[i]['command'] = lambda x=number_str[i]: add_value.numberEnter(x)
        i += 1

# --------------------------------standard--------------------------#
btn_clear = Button(menu_frm, text=chr(67), width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.clear)
btn_clear.grid(row=1, column=0, pady=1)
btn_All_clear = Button(menu_frm, text=chr(67) + chr(69), width=5, height=2,
                       font=('arial', 20, 'bold'), bd=4,
                       background='DarkGoldenrod1',
                       command=add_value.clear_all)
btn_All_clear.grid(row=1, column=1, pady=1)
btn_sq = Button(menu_frm, text=chr(8730), width=5, height=2,
                font=('arial', 20, 'bold'), bd=4,
                background='DarkGoldenrod1',
                command=add_value.sqrt)
btn_sq.grid(row=1, column=2, pady=1)
btn_Add = Button(menu_frm, text="+", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=lambda: add_value.operators("add"))
btn_Add.grid(row=1, column=3, pady=1)
btn_Sub = Button(menu_frm, text="-", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=lambda: add_value.operators("sub"))
btn_Sub.grid(row=2, column=3, pady=1)
btn_Mul = Button(menu_frm, text="*", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=lambda: add_value.operators("mult"))
btn_Mul.grid(row=3, column=3, pady=1)
btn_Div = Button(menu_frm, text="/", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=lambda: add_value.operators("div"))
btn_Div.grid(row=4, column=3, pady=1)

btn_Zero = Button(menu_frm, text="0", width=5, height=2,
                  font=('arial', 20, 'bold'), bd=4,
                  background='DarkGoldenrod1',
                  command=lambda: add_value.numberEnter("0"))
btn_Zero.grid(row=5, column=0, pady=1)
btn_Point = Button(menu_frm, text=".", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=lambda: add_value.numberEnter("."))
btn_Point.grid(row=5, column=1, pady=1)
btn_PM = Button(menu_frm, text=chr(177), width=5, height=2,
                font=('arial', 20, 'bold'), bd=4,
                background='DarkGoldenrod1',
                command=add_value.plus_minus)
btn_PM.grid(row=5, column=2, pady=1)
btn_Equal = Button(menu_frm, text="=", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.sum_of_total)
btn_Equal.grid(row=5, column=3, pady=1)
# --------------------------------Scientific--------------------------#
btn_Pi = Button(menu_frm, text="兀", width=5, height=2,
                font=('arial', 20, 'bold'), bd=4,
                background='DarkGoldenrod1',
                command=add_value.pi)
btn_Pi.grid(row=1, column=4, pady=1)
btn_Cos = Button(menu_frm, text="Cos", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.cos)
btn_Cos.grid(row=1, column=5, pady=1)
btn_Sin = Button(menu_frm, text="Sin", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.sin)
btn_Sin.grid(row=1, column=6, pady=1)
btn_Tan = Button(menu_frm, text="Tan", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.tan)
btn_Tan.grid(row=1, column=7, pady=1)

btn_2Pi = Button(menu_frm, text="2兀", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.twopi)
btn_2Pi.grid(row=2, column=4, pady=1)
btn_Coshyp = Button(menu_frm, text="CosH", width=5, height=2,
                    font=('arial', 20, 'bold'), bd=4,
                    background='DarkGoldenrod1',
                    command=add_value.coshyp)
btn_Coshyp.grid(row=2, column=5, pady=1)
btn_Sinhyp = Button(menu_frm, text="SinH", width=5, height=2,
                    font=('arial', 20, 'bold'), bd=4,
                    background='DarkGoldenrod1',
                    command=add_value.sinhyp)
btn_Sinhyp.grid(row=2, column=6, pady=1)
btn_Tanhyp = Button(menu_frm, text="TanH", width=5, height=2,
                    font=('arial', 20, 'bold'), bd=4,
                    background='DarkGoldenrod1',
                    command=add_value.tanhyp)
btn_Tanhyp.grid(row=2, column=7, pady=1)

btn_Log = Button(menu_frm, text="Log", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.log)
btn_Log.grid(row=3, column=4, pady=1)
btn_Exp = Button(menu_frm, text="Exp", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.exp)
btn_Exp.grid(row=3, column=5, pady=1)
btn_Mod = Button(menu_frm, text="%", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=lambda: add_value.operators("mod"))
btn_Mod.grid(row=3, column=6, pady=1)
btn_E = Button(menu_frm, text="e", width=5, height=2,
               font=('arial', 20, 'bold'), bd=4,
               background='DarkGoldenrod1',
               command=add_value.e)
btn_E.grid(row=3, column=7, pady=1)

btn_Log2 = Button(menu_frm, text="Log2", width=5, height=2,
                  font=('arial', 20, 'bold'), bd=4,
                  background='DarkGoldenrod1',
                  command=add_value.log2)
btn_Log2.grid(row=4, column=4, pady=1)
btn_Deg = Button(menu_frm, text="Deg", width=5, height=2,
                 font=('arial', 20, 'bold'), bd=4,
                 background='DarkGoldenrod1',
                 command=add_value.deg)
btn_Deg.grid(row=4, column=5, pady=1)
btn_aCosh = Button(menu_frm, text="Acosh", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.acoshyp)
btn_aCosh.grid(row=4, column=6, pady=1)
btn_aSinh = Button(menu_frm, text="Asinh", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.asinh)
btn_aSinh.grid(row=4, column=7, pady=1)

btn_Log10 = Button(menu_frm, text="Log10", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.log10)
btn_Log10.grid(row=5, column=4, pady=1)
btn_Log1p = Button(menu_frm, text="Log1p", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.log1p)
btn_Log1p.grid(row=5, column=5, pady=1)
btn_Expm1 = Button(menu_frm, text="Expm1", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.exmp1)
btn_Expm1.grid(row=5, column=6, pady=1)
btn_Gamma = Button(menu_frm, text="Lgam", width=5, height=2,
                   font=('arial', 20, 'bold'), bd=4,
                   background='DarkGoldenrod1',
                   command=add_value.lgamma)
btn_Gamma.grid(row=5, column=7, pady=1)

text_display = Label(menu_frm, text='Scientific calculator',
                     font=('arial', 30, 'bold'))
text_display.grid(row=0, column=4, columnspan=4)


# --------------------------------- Menu Functions------------------------------#
def quitter():
    quite = tkinter.messagebox.askyesno("Scientific Calculator", 'Are you sur that you want to quite?')
    if quite > 0:
        root.destroy()
        return


def standard():
    root.resizable(width=False, height=False)
    root.geometry('408x568+0+0')


def scientific():
    root.resizable(width=False, height=False)
    root.geometry('800x568+0+0')


def help():
    root = Toplevel()
    root.title('Contact')
    root.geometry('400x300')
    root.iconbitmap("calc.ico")

    load = Image.open("G.jpg")
    photo = ImageTk.PhotoImage(load)
    label = Label(root, image=photo)
    label.image = photo
    label.place(x=0, y=0)

    text = Label(root, text='Made by Hicham Garoum\n Email: h.garoum@gmail.com\n '
                            'phone : +212663796930',
                 font=('Arial', 15, 'bold'), bd=6, fg='blue4')
    text.pack()


    root.mainloop()
# ----------------------------------Menu----------------------------------#


# Menu principal
menu_bar = Menu(menu_frm)
# 1er Menu: File
file_menu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Standard', command=standard)
file_menu.add_command(label='Scientific', command=scientific)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=quitter)

# 2e Menu: Edite
edite_menu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label='Edit', menu=edite_menu)
edite_menu.add_command(label='Cut', command=add_value.cut_text)
edite_menu.add_command(label='Copy', command=add_value.copy_text)
edite_menu.add_separator()
edite_menu.add_command(label='Paste', command=add_value.paste_text)

# 3e Menu: Contact
help_menu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label='Contact', menu=help_menu)
help_menu.add_command(label='About Us', command=help)
help_menu.add_command(label='T54A', command=table54a)
help_menu.add_separator()
help_menu.add_command(label='T54B', command=table54b)

root.config(menu=menu_bar)

root.mainloop()
