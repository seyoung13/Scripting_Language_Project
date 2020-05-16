from tkinter import*


class GUI:

    def __init__(self):
        self.window = Tk()
        self.window.title("목적지까지의 경로 구하기")

        Label(self.window, text='출발지').grid(row=0, column=0)
        Label(self.window, text='목적지').grid(row=1, column=0)
        self.departure = Entry(self.window)
        self.departure.grid(row=0, column=1)
        self.destination = Entry(self.window)
        self.destination.grid(row=1, column=1)

        self.departure_button = Button(self.window, text='검색', command=self.search)
        self.departure_button.grid(row=0, column=2)
        self.destination_button = Button(self.window, text='검색', command=self.search)
        self.destination_button.grid(row=1, column=2)

        Label(self.window, text='예상 경로').grid(row=2, column=0)
        self.path = Scrollbar(self.window, width=200, borderwidth=100)
        self.path.grid(row=2, column=1)

        self.window.mainloop()

    def search(self):
        self.serach_window = Tk()
        Scrollbar(self.serach_window, width=200, borderwidth=100).pack()
        Button(self.serach_window, text='확인', command=self.get_location).pack()

    def get_location(self):
        self.serach_window.destroy()


GUI()
