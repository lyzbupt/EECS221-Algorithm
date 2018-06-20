
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from Tkinter import *
import tkFileDialog, os

class warehouse():
    def run(self):
        root = tk.Tk()
        root.title('EECS221 Warehouse.' )
        root.wm_geometry("1200x800")

        leftFrame = Frame(root)
        leftFrame.pack(padx=20, side = LEFT)
        rightFrame = Frame(root)
        rightFrame.pack(padx=20, side = RIGHT)
        rightFrame.config(highlightbackground='grey')
        #rightFrame.wm_geometry("200x300")

        welcome = tk.Label(leftFrame, text='Welcome to warehouse system!', width=25)
        welcome.pack(side =TOP)

        # left side option
        def print_selection():
            #val = var2.get()
            pass
            #labelR1.config(text='you have selected '+var.get())

            #type
        var1=tk.StringVar()
        labelR1=tk.Label(leftFrame,bg='grey',width=20,text='1. Choose processing type:')
        labelR1.pack()

        r1=tk.Radiobutton(leftFrame,text='(A)Type in items',variable=var1,value='A',command=print_selection)
        r1.pack()
        r2=tk.Radiobutton(leftFrame,text='(B)Batch processing of orders',variable=var1,value='B',command=print_selection)
        r2.pack()
        #r3=tk.Radiobutton(leftFrame,text='Option C',variable=var,value='C',command=print_selection)
        #r3.pack()

        tk.Label(leftFrame,bg='white',width=20,text='').pack()
            #2.algorithm
        var2=tk.StringVar()
        labelR2=tk.Label(leftFrame,bg='grey',width=20,text='2. Choose Algorithm:')
        labelR2.pack()

        r1=tk.Radiobutton(leftFrame,text='(A)Near Neighbor',variable=var2,value='A',command=print_selection)
        r1.pack()
        r2=tk.Radiobutton(leftFrame,text='(B)Branch & Bound',variable=var2,value='B',command=print_selection)
        r2.pack()


        tk.Label(leftFrame,bg='white',width=20,text='').pack()
            #3.weight
        var3=tk.StringVar()
        labelR3=tk.Label(leftFrame,bg='grey',width=20,text='3. Consider items weight? :')
        labelR3.pack()

        r1=tk.Radiobutton(leftFrame,text='(A)Yes',variable=var3,value='A',command=print_selection)
        r1.pack()
        r2=tk.Radiobutton(leftFrame,text='(B)No',variable=var3,value='B',command=print_selection)
        r2.pack()

        miniFrame = Frame(leftFrame)
            #4. begin, end
        tk.Label(miniFrame,bg='white',width=20,text='').pack()
        labelR4=tk.Label(miniFrame,bg='grey',width=20,text='4. Type in begin end point :')
        labelR4.pack(LEFT)
        beginEndPoint = Entry(miniFrame, width = 15, borderwidth = 3, relief = 'sunken')
        beginEndPoint.pack()
        beginEndPoint.get()

            #5. weight
        tk.Label(miniFrame,bg='white',width=20,text='').pack()
        labelR5=tk.Label(miniFrame,bg='grey',width=20,text='5. Type in max weight :')
        labelR5.pack(LEFT)
        maxWight = Entry(miniFrame, width = 15, borderwidth = 3, relief = 'sunken')
        maxWight.pack()
        maxWight.get()

            #6. order
        tk.Label(leftFrame,bg='white',width=20,text='').pack()
        labelR6=tk.Label(leftFrame,bg='grey',width=20,text='5. Type in order here :')
        labelR6.pack()
        order = Entry(leftFrame, width = 40, borderwidth = 3, relief = 'sunken')
        order.pack()
        order.get()

        #7. upload orders

        def openfile():
            path = os.getcwd()
            print path
            r = tkFileDialog.askopenfilename(title='Open file. ', initialdir=path,
                                             filetypes=[('Python', '*.py *.pyw'), ('All Files', '*')])
            print r
            #print(r)

        tk.Label(leftFrame,bg='white',width=20,text='').pack()
        labelR7=tk.Label(leftFrame,bg='grey',width=20,text='6. Upload orders here :')
        labelR7.pack()
        #b = Button(... command = lambda: button('hey'))
        btn1 = tk.Button(leftFrame, text='Upload orders', command=openfile)
        btn1.pack()



        def process():
            pass

        tk.Label(leftFrame,bg='white',width=20,text='').pack()
        #labelR7=tk.Label(leftFrame,bg='grey',width=20,text='6. Upload orders here :')
        #labelR7.pack()
        #b = Button(... command = lambda: button('hey'))
        btn2 = tk.Button(leftFrame, text='Pocessing!', command=process)
        btn2.pack()

        #8. Result


        tk.Label(leftFrame,bg='white',width=20,text='').pack()
            # create a Frame for the Text and Scrollbar
        txt_frm = tk.Frame(leftFrame, width=200, height=200)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
         # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)
        # create a Text widget
        txt = tk.Text(txt_frm, borderwidth=1)
        txt.config(font=("consolas", 12), undo=True, wrap='word')
        txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        txt['yscrollcommand'] = scrollb.set
        txt.insert(END, "Result txt box. \n")

        #9.  Delete Button
        btn3 = Button(leftFrame, text='Clear All', command=lambda: txt.delete(1.0,END))
        btn3.pack()
        '''
        
        go_button = tk.Button(right, text='Quit!', width=3, height=1, command=root.destroy)
        go_button.pack(side="top")
        '''
        l = []
        height = 30
        width = 30
        for i in range(height): #Rows
            for j in range(width): #Columns
                #my_test = tk.Label(leftFrame, text='Quit!', width=1)
                if((i+1)%2 ==0  and (j+1)%2 ==0 ):
                    Label(rightFrame, text="    ", bg='black').grid(row =i,column =j)
                else:
                    Label(rightFrame, text="    ", bg='white').grid(row=i, column=j)

        root.mainloop()

if __name__ == '__main__':
	try:
		ware = warehouse()
		#ware.test4()
		#ware.test2()
		ware.run()
	except KeyboardInterrupt as e:
		print('\nExit.')
	except Exception as e:
		print(e)