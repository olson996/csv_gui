#!/usr/bin/env python 
import csv
import tkinter
from tkinter import filedialog
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.backends.backend_pdf import PdfPages




def subroutine3(csvfile,  i):
    y = []
    for i in csvfile:
        x = list(i)
        if len(x) == 0:
            return y
        else:
            if x[0][0] != 'C':
                for i in range(len(x)):
                    x[i] = float(x[i])
            #print(x)
            y.append(x)

def subroutine(csvfile, i):
    y = []
    for i in csvfile:
        x = list(i)
        
        if len(x) == 0:
            return y + subroutine3(csvfile, i)
        else:
            y = [x] + y        
            #y.append((float(x[0]), float(x[1])))




class Example(tkinter.Frame):

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()

    def initUI(self):

        self.parent.title("File dialog")
        self.pack(fill=tkinter.BOTH, expand=1)

        menubar = tkinter.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tkinter.Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)        

        self.txt = tkinter.Text(self)
        self.txt.pack(fill=tkinter.BOTH, expand=1)


    def onOpen(self):

        ftypes = [('csv files', '*.csv'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        
        if fl != '':
            self.subroutine2(fl)
            

    def subroutine2(self, fileName):
        self.txt.delete(1.0, tkinter.END)
        file_i = open(fileName)
        file_i_read = csv.reader(file_i)
        h = []
        for i in file_i_read:
            x = list(i)
            if len(x)!=0:
                if x[0][-6:] == 'Factor':
                    y = subroutine(file_i_read, i)
                    y = [x[0], x[1]] + y
                    h.append(y)
        y_vals = []
        for i in range(len(h[0][4:])):
            y_vals.append(h[0][4:][i][0])
        values = []
        for j in range(len(h)):
            temp = []
            for i in range(len(h[j][4:])):
                temp.append(h[j][4:][i][1])
            values.append(temp)

        self.txt.insert(tkinter.END, 'loaded: ' + str(fileName))
        df = pd.DataFrame({'Slackoff Openhole 0.1': values[0],
            'Slackoff Openhole 0.2': values[1],
            'Slackoff Openhole 0.3': values[2],
            'Slackoff Openhole 0.4': values[3],
            'Slackoff Openhole 0.5': values[4],
            'Rotaryoff Bottom Openhole 0.0': values[5],
            'Pickup Openhole 0.1': values[6],
            'Pickup Openhole 0.2': values[7],
            'Pickup Openhole 0.3': values[8],
            'Pickup Openhole 0.4': values[9],
            'Pickup Openhole 0.5': values[10]
            }, index=y_vals)

        fig, ax = plt.subplots(1, 1, figsize=(8,5))
    
        
        ax.plot(df, y_vals)
        plt.grid(b=True)
        plt.gca().invert_yaxis()
        plt.legend(list(df.columns.values), loc=2, prop={'size': 6})
        ax.set_title('Broomstick Plot')
        newFile = str(fileName).split('/')[-1].split('.')[0]
        print(newFile)
        plt.savefig(newFile + '.pdf', dpi=None, facecolor='w', edgecolor='w',
        orientation='landscape', papertype=None, format='pdf',
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    

        plt.show()
        
        file_i.close()


def main():
    root = tkinter.Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()  
