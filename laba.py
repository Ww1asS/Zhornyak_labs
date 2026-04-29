from tkinter import *

import math

def solve_cubic(a,b,c,d):

    if a==0:
        return "Это не кубическое уравнение.",None,None,None
    p=(3*a*c-b**2)/(3*a**2)
    q=(2*b**3-9*a*b*c+27*a**2*d)/(27*a**3)
    delta=(q/2)**2+(p/3)**3
    
    if delta>0:
        u=-q/2+math.sqrt(delta)
        v=-q/2-math.sqrt(delta)
        u=u**(1/3) if u>=0 else -((-u)**(1/3))
        v=v**(1/3) if v>=0 else -((-v)**(1/3))
        x1=u+v-b/(3*a)
        return "Уравнение имеет один действительный корень.",x1,None,None

    elif delta==0:
        if p==0 and q==0:
            x1=-b/(3*a)
            return "Уравнение имеет тройной корень.",x1,x1,x1
        else:
            u=(-q/2)**(1/3) if -q/2>=0 else -((-q/2)**(1/3))
            x1=2*u-b/(3*a)
            x2=-u-b/(3*a)
            return "Уравнение имеет два действительных корня.",x1,x2,None

    else:
        phi=math.acos(-q/(2*math.sqrt(-(p/3)**3)))
        r=2*math.sqrt(-p/3)
        x1=r*math.cos(phi/3)-b/(3*a)
        x2=r*math.cos((phi+2*math.pi)/3)-b/(3*a)
        x3=r*math.cos((phi+4*math.pi)/3)-b/(3*a)
        return "Уравнение имеет три действительных корня.",x1,x2,x3
    
def proverka(value):

    try:
        return float(value)
    except ValueError:
        return None

def Button1click():
    Entry5.delete(0,END)
    Entry6.delete(0,END)
    Entry7.delete(0,END)
    Entry8.delete(0,END)
    a=proverka(Entry1.get())
    b=proverka(Entry2.get())
    c=proverka(Entry3.get())
    d=proverka(Entry4.get())

    if any(x is None for x in [a,b,c,d]):
        Entry5.insert(0,"Ошибка: введите числовые значения")
        return
    try:
        message,x1,x2,x3=solve_cubic(a,b,c,d)
        Entry5.insert(0,message)
        if x1 is not None:
            Entry5.insert(0,str(round(x1,4)))
        if x2 is not None:
            Entry6.insert(0,str(round(x2,4)))
        if x3 is not None:
            Entry7.insert(0,str(round(x3,4)))
    except (OverflowError,ValueError):
        Entry5.insert(0,"Ошибка: вычисление невозможно")

window=Tk()
window.title("Кубическое уравнение")
window.geometry('200x160')
label1=Label(window,text="A:")
label1.grid(column=0,row=0)
Entry1=Entry(window,width=20)
Entry1.grid(column=1,row=0)
label2=Label(window,text="B:")
label2.grid(column=0,row=1)
Entry2=Entry(window,width=20)
Entry2.grid(column=1,row=1)
label3=Label(window,text="C:")
label3.grid(column=0,row=2)
Entry3=Entry(window,width=20)
Entry3.grid(column=1,row=2)
label4=Label(window,text="D:")
label4.grid(column=0,row=3)
Entry4=Entry(window,width=20)
Entry4.grid(column=1,row=3)
button1=Button(window,text="решить уравнение",command=Button1click)
button1.grid(column=0,row=4,columnspan=2)
label5=Label(window,text="решение:")
label5.grid(column=0,row=5)
Entry5=Entry(window,width=20)
Entry5.grid(column=1,row=5)
label6=Label(window,text="X1:")
label6.grid(column=0,row=6)
Entry6=Entry(window,width=20)
Entry6.grid(column=1,row=6)
label7=Label(window,text="X2:")
label7.grid(column=0,row=7)
Entry7=Entry(window,width=20)
Entry7.grid(column=1,row=7)
label8=Label(window,text="X3:")
label8.grid(column=0,row=8)
Entry8=Entry(window,width=20)
Entry8.grid(column=1,row=8)
window.mainloop()