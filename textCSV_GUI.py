

#import tkinter as tk
#from tkinter import filedialog
from functools import partial
import re, sys, os
from opinion_model import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    #from tkinter import ttk
    from tkinter.ttk import Notebook
    from tkinter.ttk import Treeview
    from tkinter.ttk import Button
    import tkinter.filedialog as tkf
    import tkinter.messagebox as msg
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    from ttk import Treeview
    from ttk import Entry
    import tkFileDialog as tkf
    import tkMessageBox as msg
    

try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")

try:
    import networkx
except:
    print("Warning: networkx cannot be imported.  Unable to draw graph model!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")
        

class Editor(object):
    def __init__(self):
        
        self.open_file = None
        if os.path.exists("log.txt"):
            for line in open("log.txt", "r"):
                #if re.match('FN_FDS', line):
                #    temp =  line.split('=')
                #    FN_FDS = temp[1].strip()
                if re.match('FN', line):
                    temp =  line.split('=')
                    self.open_file = temp[1].strip()
                    
        print(self.open_file)
        self.fname_OutTXT = None
        self.fname_OutBIN = None
        self.fname_OutNPZ = None

        #self.currentSimu = None
        if self.open_file:
            self.currentdir = os.path.dirname(self.open_file)
        else:
            self.currentdir = None

        self.AUTOCOMPLETE_WORDS = ["stress", "fixed", "random", "auto", "True", "False"]
        self.FONT_SIZE = 13
        #self.AUTOCOMPLETE_WORDS = ["def", "import", "if", "else", "while", "for","try:", "except:", "print(", "True", "False"]
        self.WINDOW_TITLE = "CSV Text Editor"

        self.window = Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.geometry("800x600")

        self.menubar = Menu(self.window, bg="lightgrey", fg="black")
        self.window.config(menu=self.menubar)
    
        self.file_menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")
        self.file_menu.add_command(label="SaveAs", command=self.file_save_as)
        
        self.edit_menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.edit_menu.add_command(label="Cut", command=self.edit_cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste", command=self.edit_paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Undo", command=self.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.edit_redo, accelerator="Ctrl+Y")

        self.py_menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        #self.py_menu.add_command(label="runABS(Agent-Based Simulation)", command=self.pyrunABS, accelerator="F5")
        self.py_menu.add_command(label="runOpinionModel", command=self.pyrunOP, accelerator="F5")
        self.py_menu.add_command(label="Data2GroupC", command=self.transData, accelerator="F6")
        self.py_menu.add_command(label="DrawSocialTopology", command=self.drawGraph, accelerator="F7")

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menubar.add_cascade(label="Run", menu=self.py_menu)
        
        
        #self.line_numbers = Text(self, bg="lightgrey", fg="black", width=6, font=("Times", self.FONT_SIZE))
        #self.line_numbers.insert(1.0, "1 \n")
        #self.line_numbers.configure(state="disabled")
        #self.line_numbers.pack(side=LEFT, fill=Y)
                
        self.main_text = Text(self.window, undo=True, bg="white", fg="black", font=("Times", self.FONT_SIZE))
        self.main_text.pack(expand=1, fill=BOTH)
        #self.main_text = Text(self.window, width=45,height=6, bg="brown", fg="lightcyan", wrap=WORD,font=("Courier",10))
        #self.main_text.pack(side=LEFT,fill=BOTH,expand=YES)

        
        scrollInfo = Scrollbar(self.main_text)
        scrollInfo.pack(side=RIGHT, fill=Y)
        scrollInfo.config(command=self.main_text.yview)
        
        self.main_text.config(yscrollcommand=scrollInfo.set)
        self.main_text.insert(END, 'QuickStart: \nStep1: Please select csv file to read in agent data!\n')
        self.main_text.insert(END, 'Step2: Compute and visualize simulation!\n')
        #self.main_text.insert(END, '\nWhen simulation starts, please try to press the following keys in your keybroad, and you will see the effects on the screen. \n')
        #self.main_text.insert(END, 'Press <pageup/pagedown> to zoom in or zoom out.\n')
        #self.main_text.insert(END, 'Press arrow keys to move the entities vertically or horizonally in screen.\n')
        #self.main_text.insert(END, 'Press 1/2/3 in number panel (Right side in the keyboard) to display the door or exit data on the screen.\n')
        #self.main_text.insert(END, 'Press <space> to pause or resume the simulaton. \n')

        '''
        if self.open_file:
            self.main_text.delete(1.0, END)
            with open(self.open_file, "r") as file_contents:
                file_lines = file_contents.readlines()
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        line = re.sub(r',,', '', line)
                        line_t = re.sub(r',', ',\t', line)
                        self.main_text.insert(index, line_t)
                        #self.main_text.insert(index, line)
        self.window.title(" - ".join([self.WINDOW_TITLE, self.open_file]))
        '''
        
        #self.scrollbar = Scrollbar(self, orient="vertical") #, command=self.scroll_text_and_line_numbers)
        #self.main_text.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.main_text.yview)
        #self.scrollbar.pack(side=RIGHT, fill=Y)
    
        self.main_text.bind("<space>", self.destroy_autocomplete_menu)
        #self.main_text.bind("<KeyRelease>", self.display_autocomplete_menu)
        self.main_text.bind("<Tab>", self.insert_spaces)
    
        self.window.bind("<Control-s>", self.file_save)
        self.window.bind("<Control-o>", self.file_open)
        self.window.bind("<Control-n>", self.file_new)
        
        self.window.bind("<Control-a>", self.select_all)
        #self.window.bind("<F5>", self.pyrunABS)
        self.window.bind("<F5>", self.pyrunOP)

    '''
        self.main_text.bind("<MouseWheel>", self.scroll_text_and_line_numbers)
        self.main_text.bind("<Button-4>", self.scroll_text_and_line_numbers)
        self.main_text.bind("<Button-5>", self.scroll_text_and_line_numbers)
        self.line_numbers.bind("<MouseWheel>", self.skip_event)
        self.line_numbers.bind("<Button-4>", self.skip_event)
        self.line_numbers.bind("<Button-5>", self.skip_event)

    def skip_event(self, event=None):
        pass

    def scroll_text_and_line_numbers(self, *args):  
        try:
            # from scrollbar
            self.main_text.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
        except IndexError:
            #from MouseWheel
            event = args[0]
            if event.delta:
                move = -1*(event.delta/120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1
    
            self.main_text.yview_scroll(int(move), "units")
            self.line_numbers.yview_scroll(int(move), "units")
        '''

    def pyrunOP(self, event=None):
        #os.system("python main.py "+self.open_file)
        #simulationOP(self.open_file)
        T=None
        if os.path.exists(self.open_file):
            for line in open(self.open_file, "r"):
                if re.match('&TimeStep', line):
                    temp =  line.split('=')
                    T = int(temp[1].rstrip('\n').rstrip(',').strip()) 
        if T is None:
            T = 60
            print("NO total time is specified in the input file and default value is used: T=60. ")
            msg.showinfo('Info', 'NO total time is specified in the input file and default value is used: T=60.')
        simulationOP(self.open_file, T)
    
    def file_new(self, event=None):
        file_name = tkf.asksaveasfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")),\
        initialdir=self.currentdir)
        if file_name:
            self.open_file = file_name
            self.main_text.delete(1.0, END)
            self.title(" - ".join([self.WINDOW_TITLE, self.open_file]))


    def transData(self, event=None):
        if self.open_file is None:
            msg.showinfo('Info', 'Please open an input csv file first!')
            return
        else:
            dataIS, isStart, isEnd = getData(self.open_file, "&inti")
            dataWP, wpStart, wpEnd = getData(self.open_file, "&prob")
  
            print(dataIS)
            print(dataWP)

            NumAgents=len(dataIS)-1

            matrixIS=readFloatArray(dataIS, NumAgents, 1)
            if matrixIS.shape[0]!=NumAgents:
                print('\nError with matrixIS\n')
            if len(dataWP)>1:
                matrixWP=readFloatArray(dataWP, NumAgents, NumAgents)
                # %%%% Input parameter check
                if np.shape(matrixWP)!= (NumAgents, NumAgents):
                    print('\nError on input parameter\n')
            dataC, dataP = wp2groupC(matrixWP)
            print(dataC, dataP)

            self.main_text.insert(END, '\n&groupC\n')
            self.main_text.insert(END, str(dataC)+'\n')
            self.main_text.insert(END, '\n&p\n')
            self.main_text.insert(END, str(dataP)+'\n')
            

    def drawGraph(self, event=None):
        if self.open_file is None:
            msg.showinfo('Info', 'Please open an input csv file first!')
            return
        else:
            dataIS, isStart, isEnd = getData(self.open_file, "&inti")
            dataWP, wpStart, wpEnd = getData(self.open_file, "&prob")
            dataP, pStart, pEnd = getData(self.open_file, "&p")
            dataC, cStart, cEnd = getData(self.open_file, "&groupC")

            print(dataIS)
            print(dataWP)
            print(dataP)
            print(dataC)

            NumAgents=len(dataIS)-1

            matrixIS=readFloatArray(dataIS, NumAgents, 1)
            if matrixIS.shape[0]!=NumAgents:
                print('\nError with matrixIS\n')

            if len(dataWP)>1:
                matrixWP=readFloatArray(dataWP, NumAgents, NumAgents)
                # %%%% Input parameter check
                if np.shape(matrixWP)!= (NumAgents, NumAgents):
                    print('\nError on input parameter\n')

            if len(dataP)>1 and len(dataC)>1 and len(dataP)==len(dataC):

                matrixP=readFloatArray(dataP, NumAgents, 1)
                if matrixP.shape[0]!=NumAgents:
                    print('\nError with matrixP\n')

                CArray=readFloatArray(dataC, NumAgents, NumAgents)
                if CArray.shape!=(NumAgents, NumAgents):
                    print('\nError with CArray\n')

                print("matrixP:\n", np.shape(matrixP), "\n", matrixP, "\n")
                print("CArray:\n", np.shape(CArray), "\n", CArray, "\n")

                PFactor = np.zeros((NumAgents, NumAgents))
                print("CArray:\n", np.shape(CArray), "\n", CArray, "\n")
                for idai in range(NumAgents):
                    #if ai.inComp == 0:
                    #    continue
                    if np.sum(np.fabs(CArray[idai,:]))>0:
                        CArray[idai,:] = np.sign(CArray[idai,:])*np.fabs(CArray[idai,:])/np.sum(np.fabs(CArray[idai,:]))
                        for idaj in range(NumAgents):
                            if idaj == idai:
                                PFactor[idai,idaj] = 1-matrixP[idai,0]*np.sum(CArray[idai,:])
                            else:
                                PFactor[idai,idaj] = CArray[idai,idaj]*matrixP[idai,0]
                    else:
                        for idaj in range(NumAgents):
                            if idaj == idai:
                                PFactor[idai,idaj] = 1.0
                            else:
                                PFactor[idai,idaj] = 0.0
                print("PFactor:\n", np.shape(PFactor), "\n", PFactor, "\n")
                matrixWP = PFactor

            print("matrixWP:\n", np.shape(matrixWP), "\n", matrixWP, "\n")
            print("matrixIS:\n", np.shape(matrixIS), "\n", matrixIS, "\n")

            adj_matrix  = matrixWP
            G = networkx.from_numpy_matrix(adj_matrix)
            networkx.draw(G, with_labels =True)
            plt.show()


    def file_open(self, event=None):
        file_to_open = tkf.askopenfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")),\
        initialdir=self.currentdir)

        if file_to_open:
            self.open_file = file_to_open
            self.main_text.delete(1.0, END)
            self.currentdir = os.path.dirname(self.open_file)
            if os.path.exists("log.txt"):
                f = open("log.txt", "w+")
                f.write("---------------------------------------------------------------------\n")
                f.write("-------------------Opinion Dynamic Process-------------------\n")
                f.write("---------------------------------------------------------------------\n")
                f.write("Date&Time:"+time.strftime('%Y-%m-%d_%H_%M_%S')+"\n")
                f.write("FN="+str(self.open_file))
                f.write("\n\n")

            with open(file_to_open, "r") as file_contents:
                file_lines = file_contents.readlines()
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        line = re.sub(r',,', '', line)
                        line_t = re.sub(r',', ',\t', line)
                        self.main_text.insert(index, line_t)
                        #self.main_text.insert(index, line)
        self.window.title(" - ".join([self.WINDOW_TITLE, self.open_file]))
        #self.update_line_numbers()
        

    def file_save(self, event=None):
        if not self.open_file:
            new_file_name = tkf.asksaveasfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")),\
            initialdir=self.currentdir)
            self.open_file = new_file_name
        if self.open_file:
            #new_contents = self.main_text.get(1.0, END)
            #with open(self.open_file, "w") as open_file:
            #    open_file.write(new_contents)
            new_contents = self.main_text.get(1.0, END)
            new_contents2 = re.sub(',\t', ',', new_contents)
            try:
                with open(self.open_file, "w") as open_file:
                    open_file.write(new_contents2)
                msg.showinfo('Info', 'File saved successfully')
            except:
                msg.showinfo('Info', 'Errors in saving files')
            

    def file_save_as(self, event=None):
        #if not self.open_file:
        new_file_name = tkf.asksaveasfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")),\
        initialdir=self.currentdir)
        if new_file_name:
            self.open_file = new_file_name
        if self.open_file:
            #new_contents = self.main_text.get(1.0, END)
            #with open(self.open_file, "w") as open_file:
            #    open_file.write(new_contents)
            new_contents = self.main_text.get(1.0, END)
            new_contents2 = re.sub(',\t', ',', new_contents)
            try:
                with open(self.open_file, "w") as open_file:
                    open_file.write(new_contents2)
                msg.showinfo('Info', 'File saved successfully')
                self.window.title(" - ".join([self.WINDOW_TITLE, self.open_file]))
            except:
                msg.showinfo('Info', 'Errors in saving files')

    def select_all(self, event=None):
        self.main_text.tag_add("sel", 1.0, END)
        return None

    def edit_cut(self, event=None):
        self.main_text.event_generate("<<Cut>>")
        return None

    def edit_paste(self, event=None):
        self.main_text.event_generate("<<Paste>>")
        self.on_key_release()
        self.tag_all_lines()
        return None

    def edit_undo(self, event=None):
        self.main_text.event_generate("<<Undo>>")
        return None

    def edit_redo(self, event=None):
        self.main_text.event_generate("<<Redo>>")
        return None

    def insert_spaces(self, event=None):
        self.main_text.insert(INSERT, " ")
        return None

    def get_menu_coordinates(self):
        bbox = self.main_text.bbox(INSERT)
        menu_x = bbox[0] + self.winfo_x() + self.main_text.winfo_x()
        menu_y = bbox[1] + self.winfo_y() + self.main_text.winfo_y() + self.FONT_SIZE + 2
        
        return (menu_x, menu_y)

    def display_autocomplete_menu(self, event=None):
        current_index = self.main_text.index(INSERT)
        start = self.adjust_floating_index(current_index)

        try:
            currently_typed_word = self.main_text.get(start + " wordstart", INSERT)
        except TclError:
            currently_typed_word = ""
        
        currently_typed_word = str(currently_typed_word).strip()

        if currently_typed_word:
            self.destroy_autocomplete_menu()

            suggestions = []
            for word in self.AUTOCOMPLETE_WORDS:
                if word.startswith(currently_typed_word) and not currently_typed_word == word:
                    suggestions.append(word)

            if len(suggestions) > 0:
                x, y = self.get_menu_coordinates()
                self.complete_menu = Menu(self, tearoff=0, bg="lightgrey", fg="black")

                for word in suggestions:
                    insert_word_callback = partial(self.insert_word, word=word, part=
                        currently_typed_word, index=current_index)
                    self.complete_menu.add_command(label=word, command=
                        insert_word_callback)

                self.complete_menu.post(x, y)
                self.main_text.bind("<Down>", self.focus_menu_item)


    def destroy_autocomplete_menu(self, event=None):
        try:
            self.complete_menu.destroy()
            self.main_text.unbind("<Down>")
            self.main_text.focus_force()
        except AttributeError:
            pass

    def insert_word(self, word, part, index):
        amount_typed = len(part)
        remaining_word = word[amount_typed:]
        remaining_word_offset = " +" + str(len(remaining_word)) + "c"
        self.main_text.insert(index, remaining_word)
        self.main_text.mark_set(INSERT, index + remaining_word_offset)
        self.destroy_autocomplete_menu()
        self.main_text.focus_force()

    def adjust_floating_index(self, number):
        indices = number.split(".")
        x_index = indices[0]
        y_index = indices[1]
        y_as_number = int(y_index)
        y_previous = y_as_number - 1
        return ".".join([x_index, str(y_previous)])

    def focus_menu_item(self, event=None):
        try:
            self.complete_menu.focus_force()
            self.complete_menu.entryconfig(0, state="active")
        except TclError:
            pass
    
    '''
    def tag_all_lines(self):
        final_index = self.main_text.index(END)
        final_line_number = int(final_index.split(".")[0])

        for line_number in range(final_line_number):
            line_to_tag = ".".join([str(line_number), "0"])
            self.tag_keywords(None, line_to_tag)
        self.update_line_numbers()
    
    def update_line_numbers(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete(1.0, END)
        number_of_lines = self.main_text.index(END).split(".")[0]
        line_number_string = "\n".join(str(no+1) for no in range(int(number_of_lines)))
        self.line_numbers.insert(1.0, line_number_string)
        self.line_numbers.configure(state="disabled")
    '''
    
    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    editor = Editor()
    editor.start()
