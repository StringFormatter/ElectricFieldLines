import os
import sys
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
        self.scaleList = []
        #self.varList = []
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

        #very top frame
        self.gframe = Frame(self.notebook)
        #canvas frame
        self.gtframe = Frame(self.gframe)
        #button frame
        self.gbframe = Frame(self.gframe)
        #scaler frame
        self.gsframe = Frame(self.gframe)

        #manage the packing of associated frames
        #self.gtframe.pack(side=TOP, fill="both", expand=YES)
        self.gsframe.pack(side=RIGHT, expand=NO)
        self.gtframe.pack(side=TOP, fill="both", expand=YES)
        self.gbframe.pack(side=BOTTOM, expand=NO)
        #self.gsframe.pack(side=RIGHT, expand=NO)
        
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

        

        #self.fframe = Frame(self.notebook)
        #self.label = Label(self.fframe, text="WIP please ignore, JUST LEAVE", bg = "#3e3e3e")
        
        #self.label.grid(column=0, row=0)
        
        self.notebook.add(self.gframe, text="Graph")
        #self.notebook.add(self.fframe, text="Charges")
        
        self.notebook.pack(fill="both", expand=YES)

    def add_node(self):
        #clear the screen and draw node and text
        self.clear_lines()
        self.nodeList.append(self.canvas.create_oval(0, 0, 30, 30, outline="#e00030", activeoutline="#e000e0", fill="#e00030", activefill="#e000e0", tags=str(self.nodenum)))
        self.textList.append(self.canvas.create_text(15, 15, tags=str(self.nodenum), text="q"+str(self.nodenum)))

        #add the scaling widget
        scale = Scale(self.gsframe, from_=-1, to=1, resolution=.1, orient=HORIZONTAL, command=self.color_check, label="q"+str(self.nodenum)+"             nC")
        scale.pack()
        self.scaleList.append(scale)
        #activate the click_move function when clicked
        self.canvas.tag_bind(ALL, '<B1-Motion>', func = self.click_move)
        self.nodenum += 1

    def remove_node(self):
        self.clear_lines()
        if self.nodeList == []: return 0
        self.canvas.delete(self.nodeList.pop())
        self.canvas.delete(self.textList.pop())
        self.scaleList.pop().destroy()
        self.nodenum -= 1

    def color_check(self, event):
        self.clear_lines()
        for i in range(len(self.scaleList)):
            tmp = self.scaleList[i].get()
            if tmp > 0:
                self.canvas.itemconfig(self.nodeList[i], fill="#e00030")
                self.canvas.itemconfig(self.nodeList[i], outline="#e00030")
            elif tmp < 0:
                self.canvas.itemconfig(self.nodeList[i], fill="#3000e0")
                self.canvas.itemconfig(self.nodeList[i], outline="#3000e0")
            else:
                self.canvas.itemconfig(self.nodeList[i], fill="#e0e0e0")
                self.canvas.itemconfig(self.nodeList[i], outline="#e0e0e0")



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
        #siz = len(self.textList)
        for i in range(len(self.textList)):
            if self.scaleList[i].get() == 0:
                continue
            for j in stan_coords:
                coords = self.canvas.coords(self.textList[i])
                #for j in stan_coords:
                x = coords[0]+j[0]
                y = coords[1]-j[1]
                og = (x,y)
                V = self.compute_equ(x, y)
                x_1 = x+(V[0])
                y_1 = y-(V[1])
                count = 0
                #print(str(coords) + '\n')
                #while(not math.isclose((math.sqrt( (og[0]+x_1)**2 + (og[1]+y_1)**2 )), 0, abs_tol=.05)):
                while(not (math.isclose(x_1,og[0],rel_tol=.0005) and math.isclose(y_1,og[1],rel_tol=.005))):
                    V = self.compute_equ(x_1, y_1)
                    x_2 = x_1+(V[0]/10)
                    y_2 = y_1-(V[1]/10)
                    #print(x_2,y_2)
                    count = count + 1
                    #print(tmp_slope)
                    #print(str(V) + '\n')
                    
                    self.lineList.append(self.canvas.create_line(x,y,x_1,y_1,x_2,y_2,smooth="true",fill="#0099ff"))
                    if count % 100 == 0:
                        self.canvas.update_idletasks()
                    x = x_1
                    y = y_1
                    x_1 = x_2
                    y_1 = y_2
                    if count > 50*j[1]*j[1]:
                        break
                #self.lineList.append(self.canvas.create_line(x,y,x_1,y_1,og[0],og[1],smooth="true",fill="#0099ff"))

    def compute_e_vec(self, x, y):
        E = 0
        Ex = 0
        Ey = 0

        CHARGE = 1e-7
        CONSTANT = 9e9

        for i in range(len(self.textList)):
            coords = self.canvas.coords(self.textList[i])
            ax = coords[0]
            ay = coords[1]
            #print(str(x) + " and " + str(y) + " and " + str(avgcoord_x) + " and " + str(avgcoord_y))
            #print((x),(y))
            cmod = self.scaleList[i].get()
            if cmod == 0:
                continue

            r = ((ay-y)**2 + (x-ax)**2)**(1/2)
            if(r == 0):
                return((1e9,1e9))
            Ex += (x-ax)*CHARGE*cmod*CONSTANT/(r**3)
            Ey += (ay-y)*CHARGE*cmod*CONSTANT/(r**3)


        return((Ex, Ey))
        
    def compute_equ(self, x, y):
        E = self.compute_e_vec(x, y)
        return ((E[1],-1*E[0]))


    def draw_field(self):
        #Draws field lines around each point particle
        stan_coords = [(0,15),(15,0),(10.6,-10.6),(10.6,10.6)]
        #stan_coords = [(15,0)]
        coord_list = []
        for i in self.textList:
            coord_list.append(self.canvas.coords(i))
        for i in range(len(self.textList)):
            coords = coord_list[i]
            crg = self.scaleList[i].get()
            if crg  <= 0:
                continue
            for j in stan_coords:
                for k in (1,-1):
                    x = coords[0]+j[0]*k
                    y = coords[1]-j[1]*k
                    E = self.compute_e_vec(x, y)
                    x_1 = x+(E[0])
                    y_1 = y-(E[1])
                    count = 0
                    #print(str(coords) + '\n')
                    while(not (x > self.canvas.winfo_width() or y > self.canvas.winfo_height() or x < 0 or y < 0)):
                        E = self.compute_e_vec(x_1, y_1)
                        x_2 = x_1+(E[0])*10
                        y_2 = y_1-(E[1])*10
                        if self.check_dist(coord_list, x_2, y_2):
                            break
                        #print(x_2,y_2)

                        #print(tmp_slope)
                        #print(str(E) + '\n')

                        self.lineList.append(self.canvas.create_line(x,y,x_1,y_1,x_2,y_2,smooth="true",fill="#03fc98"))

                        if count % 10 == 0:
                            self.canvas.update_idletasks()
                        x = x_1
                        y = y_1
                        x_1 = x_2
                        y_1 = y_2
                        count += 1
                        if count > 4000:
                            break
                        #tmp_slope = slope


    def check_dist(self, c_list, x, y):
        for i in c_list:
            xc = i[0]
            yc = i[1]
            if ((x-xc)**2 + (y-yc)**2)**(1/2) < 15:
                return True
        return False
                        
    def clear_lines(self):
        while self.lineList != []:
            self.canvas.delete(self.lineList.pop())


if __name__ == "__main__" :
    root = Tk()

    app = Main_App(root)

    root.mainloop()
