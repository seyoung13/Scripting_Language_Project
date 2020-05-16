from tkinter import*


class GUI:

    def __init__(self):
        window = Tk()
        window.title("목적지까지의 경로 구하기")
        window.geometry("800x600")



        self.departure_button = Button(text='출발지')
        self.departure_button.pack(side=RIGHT)
        self.destination_button = Button(text='목적지')
        self.departure_button.pack(side=RIGHT)

        self.scrollbar = Scrollbar()
        self.scrollbar.pack()

        window.mainloop()


GUI()