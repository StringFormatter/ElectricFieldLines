import os
import sys
import  queue
import threading
import time
from tkinter import *
from tkinter import ttk
import math

class Main_App():

    def __init__(self, master):
        
        self.mWidth = 1200
        self.mHeight = 800
        self.nodeList = []
        self.textList = []
        self.lineList = []
        self.nodenum = 0

        frame = Frame(master, width=self.mWidth, height=self.mHeight)
        frame.pack(fill="both", expand=YES)

        self.create_widgets(frame)

        '''
        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=TOP)
        '''

    def create_widgets(self, frame):
        
        self.notebook = ttk.Notebook(frame)
        
        self.gframe = Frame(self.notebook)
        self.gtframe = Frame(self.gframe)
        self.gbframe = Frame(self.gframe)
        
        self.gtframe.pack(fill="both", expand=YES)
        self.gbframe.pack(expand=NO)

        self.canvas = Canvas(self.gtframe, bg = "#1e1e1e")

        self.canvas.pack(fill="both", expand=YES)
        
        self.abttn = Button(self.gbframe, text="Add Point Charge", command=self.add_node)
        self.rbttn = Button(self.gbframe, text="Remove Point Charge", command=self.remove_node)
        self.fbttn = Button(self.gbframe, text="Draw Field Lines", command=self.draw_field)
        self.tbttn = Button(self.gbframe, text="Draw Equipotential Lines", command=self.draw_equ)
        
        self.abttn.grid(column=0, row=1)
        self.rbttn.grid(column=1, row=1)
        self.fbttn.grid(column=0, row=2)
        self.tbttn.grid(column=1, row=2)

        self.fframe = Frame(self.notebook)
        self.label = Label(self.fframe, text="WIP please ignore, JUST LEAVE", bg = "#3e3e3e")
        
        self.label.grid(column=0, row=0)
        
        self.notebook.add(self.gframe, text="Graph")
        self.notebook.add(self.fframe, text="Charges")
        
        self.notebook.pack(fill="both", expand=YES)

    def add_node(self):
        self.clear_lines()
        self.nodeList.append(self.canvas.create_oval(0, 0, 30, 30, outline="#e00030", activeoutline="#e000e0", fill="#e00030", activefill="#e000e0", tags=str(self.nodenum)))
        self.textList.append(self.canvas.create_text(15, 15, tags=str(self.nodenum), text="q"+str(self.nodenum)))
        self.canvas.tag_bind(ALL, '<B1-Motion>', func = self.click_move)
        self.nodenum += 1

    def remove_node(self):
        self.clear_lines()
        if self.nodeList == []: return 0
        self.canvas.delete(self.nodeList.pop())
        self.canvas.delete(self.textList.pop())
        self.nodenum -= 1

    def click_move(self, event):
        self.clear_lines()
        mouse_x = self.canvas.winfo_pointerx()-self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery()-self.canvas.winfo_rooty()
        coords = self.canvas.coords(CURRENT)
        avgcoord_x = (coords[0]+coords[2])/2
        avgcoord_y = (coords[1]+coords[3])/2

        self.canvas.move(CURRENT, mouse_x-avgcoord_x, mouse_y-avgcoord_y)
        self.canvas.move(self.canvas.find_above(CURRENT), mouse_x-avgcoord_x, mouse_y-avgcoord_y)


        #print((mouse_x,mouse_y))
        #print(coords)

    def draw_equ(self):
        #Draws equipotential lines around each point particle
        stan_coords = [(0,30),(0,50),(0,70)]
        #stan_coords = [(0,40)]
        for i in self.textList:
            coords = self.canvas.coords(i)
            for j in stan_coords:
                x = coords[0]+j[0]
                y = coords[1]-j[1]
                og = (x,y)
                V = self.compute_equ(x, y)
                x_1 = x+(V[0]/100)
                y_1 = y-(V[1]/100)
                #print(str(coords) + '\n')
                #while(not math.isclose((math.sqrt( (og[0]+x_1)**2 + (og[1]+y_1)**2 )), 0, abs_tol=.05)):
                while(not (math.isclose(x_1,og[0],rel_tol=.000005) and math.isclose(y_1,og[1],rel_tol=.005))):
                    V = self.compute_equ(x_1, y_1)
                    x_2 = x_1+(V[0]/100)
                    y_2 = y_1-(V[1]/100)
                    #print(x_2,y_2)
                    
                    #print(tmp_slope)
                    #print(str(V) + '\n')
                
                    self.lineList.append(self.canvas.create_line(x,y,x_1,y_1,x_2,y_2,smooth="true",fill="#0099ff"))
                    self.canvas.update_idletasks()
                    x = x_1
                    y = y_1
                    x_1 = x_2
                    y_1 = y_2
                        
                self.lineList.append(self.canvas.create_line(x,y,x_1,y_1,og[0],og[1],smooth="true",fill="#0099ff"))

    def compute_e_vec(self, x, y):
        E = 0
        Ex = 0
        Ey = 0

        CHARGE = 1e-7
        CONSTANT = 9e9

        for i in self.textList:
            coords = self.canvas.coords(i)
            ax = coords[0]
            ay = coords[1]
            #print(str(x) + " and " + str(y) + " and " + str(avgcoord_x) + " and " + str(avgcoord_y))
            #print((x),(y))

            theta = math.atan2(ay-y,x-ax)

            r2 = (ay-y)**2 + (x-ax)**2
            if(r2 == 0):
                return((1e9,1e9))
            E = CHARGE*CONSTANT/r2
            Ex += math.cos(theta)*E
            Ey += math.sin(theta)*E


        return((Ex, Ey))
        
    def compute_equ(self, x, y):
        E = self.compute_e_vec(x, y)
        return ((E[1],-1*E[0]))


    def draw_field(self):
        #Draws field lines around each point particle
        stan_coords = [(0,15),(15,0),(10.6,-10.6),(10.6,10.6)]
        #stan_coords = [(15,0)]
        for i in self.textList:
            coords = self.canvas.coords(i)
            for j in stan_coords:
                for k in (1,-1):
                    x = coords[0]+j[0]*k
                    y = coords[1]-j[1]*k
                    E = self.compute_e_vec(x, y)
                    x_1 = x+(E[0])
                    y_1 = y-(E[1])
                    #print(str(coords) + '\n')
                    while(not (x > self.canvas.winfo_width() or y > self.canvas.winfo_height() or x < 0 or y < 0)):
                        E = self.compute_e_vec(x_1, y_1)
                        x_2 = x_1+(E[0])
                        y_2 = y_1-(E[1])
                        #print(x_2,y_2)

                        #print(tmp_slope)
                        #print(str(E) + '\n')

                        self.lineList.append(self.canvas.create_line(x,y,x_1,y_1,x_2,y_2,smooth="true",fill="#03fc98"))

                        #self.canvas.update_idletasks()
                        x = x_1
                        y = y_1
                        x_1 = x_2
                        y_1 = y_2
                        #tmp_slope = slope

    def clear_lines(self):
        while self.lineList != []:
            self.canvas.delete(self.lineList.pop())


if __name__ == "__main__" :
    root = Tk()

    app = Main_App(root)

    root.mainloop()
