import tkinter as tk
from tkinter import filedialog as fd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.messagebox as tkm
import xml.etree.ElementTree as ET


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.geometry("800x600")
        self.mainMenu = tk.Menu(self)
        self.fileMenu = tk.Menu(self.mainMenu)
        self.btnOm = tk.Button(self, text="угл. скорости (БССИ)", font="helvetica 10", foreground="#004D40", background="#B2DFDB", command=self.graf_h)
        self.btnOm.place(x=10, y=2, height=30)

        self.btnBOKZ = tk.Button(self, text="БОКЗ в Wxyz", font="helvetica 10", foreground="#004D40",
                               background="#B2DFDB")
        self.btnBOKZ.place(x=155, y=2, height=30)

        self.btnAngle = tk.Button(self, text="углы", font="helvetica 10", foreground="#004D40",
                               background="#B2DFDB")
        self.btnAngle.place(x=255, y=2, height=30)

        self.btnBSHV = tk.Button(self, text="БШВ", font="helvetica 11", foreground="#004D40", background="#B2DFDB")
        self.btnBSHV.place(x=300, y=2, height=30)

        self.Rx_arr = []
        self.Ry_arr = []
        self.Rz_arr = []

        self.init_menu()

    def init_menu(self):
        self.config(menu=self.mainMenu)
        self.fileMenu.add_command(label="Открыть файл", command=self.parse_xmlfile)
        self.mainMenu.add_cascade(label="Файл", menu=self.fileMenu)

    def parse_xmlfile(self):
        file_name = fd.askopenfilename(filetypes=(("RSP files", "*.rsp"), ("All files", "*.*")))
        if file_name[-4:] == ".rsp":
            tree = ET.parse(file_name)
            main_root = tree.getroot()
            idggp_data = main_root.find('idggp_data')
            raw_data = idggp_data.find('raw_data')
            ksv = raw_data.find('KSV')

            Rx = ksv.find('Rx_array').get('val')
            self.Rx_arr = Rx.split(",")
            self.Rx_arr = list(map(float, self.Rx_arr))

            Ry = ksv.find('Ry_array').get('val')
            self.Ry_arr = Ry.split(",")
            self.Ry_arr = list(map(float, self.Ry_arr))

            Rz = ksv.find('Rz_array').get('val')
            self.Rz_arr = Rz.split(",")
            self.Rz_arr = list(map(float, self.Rz_arr))

            print(self.Rx_arr, self.Ry_arr, self.Rz_arr)
            tkm.showinfo(title="Успешно", message="Файл успешно открыт!")
        else:
            tkm.showerror(title="Ошибка", message="Файл не удалось открыть!")

    def graf_h(self):
        height = []
        for el, i in enumerate(range(0, len(self.Rz_arr))):
            height.append(pow(self.Rx_arr[el]**2 + self.Ry_arr[el]**2 + self.Rz_arr[el]**2, 1/2) - 6371)
        print(height)
        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.plot(height)
        canvas = FigureCanvasTkAgg(fig)
        canvas.draw()
        canvas.get_tk_widget().place(x=50, y=60)


if __name__ == "__main__":
    window = Window()

    window.mainloop()
