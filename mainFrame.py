from tkinter import CENTER, END, Label,Button, Entry, Frame, Radiobutton, Scrollbar
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import *
from tkinter.constants import DISABLED, NORMAL
from tkinter import  messagebox
from libExcel import Excel
from libCaminoCritico import CaminoCritico


class MainFrame(Frame):
    archivoExcel = ""
    dataFrame = ""
    auxInput = []
    rutaCritica = ''
    def __init__(self, master=None):
        super().__init__(master, width=800, height= 660)
        self.master = master        
        self.pack()
        claseExcel = Excel 
        claseCPM = CaminoCritico
        self.create_widgets(claseExcel,claseCPM)  

    def recolectarInput(self,input1,input2,input3,input4,tabla):
        ident = input1.get()
        desc = input2.get()
        duracion = input3.get()
        predec = input4.get()
        if predec == '':
            predec = float("NaN")
            self.auxInput.append(ident+'-'+desc+'-'+duracion+'-'+'.')
        else:
            self.auxInput.append(ident+'-'+desc+'-'+duracion+'-'+predec)
        tabla.insert("",END,text=ident, values=(predec,desc,duracion))

    
    def cargarArchivo(self, excel,tabla1):
        self.dataFrame, self.archivoExcel = excel.abrir_archivo()
        if(self.archivoExcel == ""):
            messagebox.showinfo(title="Advertencia", message = "No seleccionaste ningun archivo") 
        else:
            for x in range(0,self.dataFrame['identificacion'].size):
                tabla1.insert("",END,text=self.dataFrame['identificacion'][x]
                    ,values=(self.dataFrame['predecessors'][x],self.dataFrame['descripcion'][x]
                        ,self.dataFrame['duracion'][x]))


    def llenarTablas(self,llenadoTabla,tabla1,tabla2):
        informacion = ''
        if (self.archivoExcel == "" and len(self.auxInput)==0):
            messagebox.showinfo(title="Advertencia", message = "No hay datos ingresados")
        elif self.archivoExcel == "":
            informacion = llenadoTabla.procesarInput(CaminoCritico,self.auxInput) 
        elif len(self.auxInput)==0:
            informacion = llenadoTabla.procesarArchivo(CaminoCritico,self.dataFrame)

        if informacion != '':
            self.rutaCritica = informacion
            Fp = informacion.forwardPass
            bP = informacion.backwardPass
            indices = Fp.index
            for x in range(0,Fp['earlyFinish'].size):
                tabla1.insert("",END,text=indices[x],values=(Fp['earlyFinish'][x],Fp['earlyStart'][x]))
            indices = bP.index
            for x in range(0,bP['lateStart'].size):
                tabla2.insert("",END,text=indices[x],values=(bP['lateStart'][x],bP['lateFinish'][x],bP['slack'][x]))


        
        
    def create_widgets(self,excel,llenadoTabla):
 
        # labels
        Label(self,text="CARGA DE DATOS").place(x=20,y=10)
        Label(self,text="_____________________________________________________________________________________________________").place(x=20,y=30)
        Label(self,text="Identificador").place(x=20,y=50)
        Label(self,text="Descripción").place(x=140,y=50)
        Label(self,text="Duración").place(x=430,y=50)
        Label(self,text="Predecesor").place(x=20,y=92)
        Label(self,text="_____________________________________________________________________________________________________").place(x=20,y=130)
        Label(self,text="TABLA DE INICIO").place(x=230,y=155)
        Label(self,text="FORWARD PASS").place(x=230,y=320)
        Label(self,text="BACKWARD PASS").place(x=230,y=485)
        Label(self,text="ESTADÍSTICAS").place(x=650,y=155)
        Label(self,text="¿Posee ruta crítica?").place(x=590,y=195)
        Label(self,text="Ruta crítica:").place(x=590,y=255)
        Label(self,text="¿Posee holgura?").place(x=590,y=315)
        Label(self,text="Contador eventos con holgura").place(x=590,y=375)
        Label(self,text="Eventos y su holgura:").place(x=590,y=435)


        # textbox
        #input1
        txt_id = Entry(self, bg="white")
        txt_id.place(x=20, y=70, width=100, height=20)

        #input2
        txt_des = Entry(self, bg="white")
        txt_des.place(x=140, y=70, width=270, height=20)

        #input3
        txt_du = Entry(self, bg="white")
        txt_du.place(x=430, y=70, width=100, height=20)

        #respuesta1
        txt_existeRC = Entry(self, bg="white")
        txt_existeRC.place(x=590, y=225, width=190, height=20)
        
        #respuesta2
        txt_RC = Entry(self, bg="white")
        txt_RC.place(x=590, y=285, width=190, height=20)
        
        #respuesta3
        txt_holgura = Entry(self, bg="white")
        txt_holgura.place(x=590, y=345, width=190, height=20)
       
        #respuesta4
        txt_contador = Entry(self, bg="white")
        txt_contador.place(x=590, y=405, width=190, height=20)

        #respuesta5
        txt_listaHolgura = Entry(self, bg="white")
        txt_listaHolgura.place(x=590, y=465, width=190, height=100)

        #input4
        txt_pre = Entry(self, bg="white")
        txt_pre.place(x=260, y=110, width=150, height=20)
        
        # radiobuttons        
        
        rbt_unico = Radiobutton(self, text= "Único")
        rbt_unico.place(x=20,y=110)
        rbt_varios = Radiobutton(self, text= "Varios")
        rbt_varios.place(x=75,y=110)
        
        rbt_manual = Radiobutton(self, text= "Manual",)
        rbt_manual.place(x=140,y=10)
        rbt_archivo = Radiobutton(self, text= "Archivo")
        rbt_archivo.place(x=260,y=10)

        #opcion = IntVar()
        #rbt_manual = Radiobutton(self, text= "Manual", variable=opcion, value=1)
        #rbt_manual.place(x=140,y=10)
        #rbt_archivo = Radiobutton(self, text= "Archivo", variable=opcion, value=2)
        #rbt_archivo.place(x=260,y=10)

        # combo_box

        self.opciones=["Hola", "Holax2", "Holax3"]
        Combobox(self, values=self.opciones, state="readonly").place(x=140,y=110, width=100)
        

        # tabla datos iniciales

        tv = ttk.Treeview(self, columns=("col1","col2", "col3"))
        tv.column("#0",width=30)
        tv.column("col1",width=30, anchor=CENTER)
        tv.column("col2",width=150, anchor=CENTER)
        tv.column("col3",width=50, anchor=CENTER)

        tv.heading("#0", text="Identificador", anchor=CENTER)
        tv.heading("col1", text="Predecesor", anchor=CENTER)
        tv.heading("col2", text="Descripción", anchor=CENTER)
        tv.heading("col3", text="Duración", anchor=CENTER)

        #tv.insert("",END,text="Azucar", values=("28","lala", "12"))
        #tv.insert("",END,text="Refresco", values=("16","lala", "2"))
        #tv.insert("",END,text="AQceite", values=("34","lala", "3"))
        tv.place(x=20, y=180, width=510, height=130)

        # frame para scrollbar de tabla inicial

        p_aux =Frame(self)
        p_aux.place(x=530,y=180, width=20, height=130)

        # scrollbar de tabla inicial

        scroll_syn = Scrollbar(p_aux)
        scroll_syn.pack(side='right', fill='y')
        scroll_syn.config(command = tv.yview )

        # tabla forward

        tv1 = ttk.Treeview(self, columns=("col1","col2"))
        tv1.column("#0",width=30)
        tv1.column("col1",width=30, anchor=CENTER)
        tv1.column("col2",width=150, anchor=CENTER)

        tv1.heading("#0", text="Identificador", anchor=CENTER)
        tv1.heading("col1", text="EarlyFinish", anchor=CENTER)
        tv1.heading("col2", text="EarlyStart", anchor=CENTER)

        #tv1.insert("",END,text="A", values=("28","2"))
        #tv1.insert("",END,text="B", values=("16","3"))
        #tv1.insert("",END,text="C", values=("34","1"))
        tv1.place(x=20, y= 345, width=510, height=130)
        
        # tabla backward

        tv2 = ttk.Treeview(self, columns=("col1","col2", "col3"))
        tv2.column("#0",width=30)
        tv2.column("col1",width=30, anchor=CENTER)
        tv2.column("col2",width=150, anchor=CENTER)
        tv2.column("col3",width=50, anchor=CENTER)

        tv2.heading("#0", text="Identificador", anchor=CENTER)
        tv2.heading("col1", text="LateStart", anchor=CENTER)
        tv2.heading("col2", text="LateFinish", anchor=CENTER)
        tv2.heading("col3", text="Slack", anchor=CENTER)

        #tv2.insert("",END,text="A", values=("28","2", "0"))
        #tv2.insert("",END,text="B", values=("16","3", "0"))
        #tv2.insert("",END,text="C", values=("34","1", "0"))
        tv2.place(x=20, y=510, width=510, height=130)

        # frame para scrollbar syn de tablas for y back

        p_aux2 =Frame(self)
        p_aux2.place(x=530,y=345, width=20, height=295)

        # funcion syncro-scroll

        def  multiple_yview(*args):
            tv1.yview(*args)
            tv2.yview(*args)

        # scrollbar syn de tablas for y back 

        scroll_syn = Scrollbar(p_aux2)
        scroll_syn.pack(side='right', fill='y')
        scroll_syn.config(command = multiple_yview )

        # buttons

        self.btnA=Button(self,text="Agregar"
            ,command=lambda: self.recolectarInput(txt_id,txt_des,txt_du,txt_pre,tv))
        self.btnA.place(x=430,y=110, width=100)

        self.btnRC=Button(self,text="Pert CMP / Ruta Crítica"
            ,command=lambda: self.llenarTablas(llenadoTabla,tv1,tv2))
        self.btnRC.place(x=590,y=110, width=190)

        self.btnExcel=Button(self,text="Archivo Excel",command=lambda: self.cargarArchivo(excel,tv))
        self.btnExcel.place(x=430,y=10, width=100) 

        # cambio de estado para radiobuttons
        #if opcion == 1:
        #    self.btnExcel.place_forget()      
            
        #else:
            #self.btnExcel.configure(state= NORMAL) 
        #    self.btnExcel.place(x=430,y=10, width=100)            
        
        # para hacer lineas
        # p_aux3 =Frame(self, bg="black")
        # p_aux3.place(x=570,y=10, width=1, height=640)  
        #tv.place(x=10, y=170, width=540, height=80)

     
