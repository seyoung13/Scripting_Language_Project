from tkinter import*
import transferAPI


class GUI:

    def __init__(self):
        self.window = Tk()
        self.window.title("대중교통 경로 정보")

        Label(self.window, text='출발지').grid(row=0, column=0)
        Label(self.window, text='목적지').grid(row=1, column=0)
        self.departure = Entry(self.window)
        self.departure.grid(row=0, column=1)
        self.destination = Entry(self.window)
        self.destination.grid(row=1, column=1)

        self.departure_button = Button(self.window, text='검색',
                                       command=lambda: self.search_departure(self.departure.get()))
        self.departure_button.grid(row=0, column=2)
        self.destination_button = Button(self.window, text='검색',
                                         command=lambda: self.search_destination(self.destination.get()))
        self.destination_button.grid(row=1, column=2)

        Label(self.window, text='예상 경로').grid(row=2, column=0)
        self.path_scroll = Scrollbar(self.window)
        self.path_scroll.grid(row=2, column=2, sticky='w'+'n'+'s')
        self.path_list = Listbox(self.window, yscrollcommand=self.path_scroll.set)
        self.path_list.grid(row=2, column=1)

        Label(self.window, text='이메일 주소').grid(row=3, column=0)
        Entry(self.window).grid(row=3, column=1)
        Button(self.window, text='경로 보내기').grid(row=3, column=2, stick='w')

        self.window.mainloop()

    def search_departure(self, target_location):
        self.searching_window = Tk()
        self.result_scroll = Scrollbar(self.searching_window)
        self.result_scroll.grid(row=0, column=1, sticky='w'+'n'+'s')
        self.result_list = Listbox(self.searching_window, yscrollcommand=self.result_scroll.set)

        self.location_name, self.lx, self.ly = transferAPI.search_location(target_location)

        for i in range(len(self.location_name)):
            self.result_list.insert(i, str(self.location_name[i]))
        self.result_list.grid(row=0, column=0)
        self.result_scroll['command'] = self.result_list.yview
        Button(self.searching_window, text='확인', command=self.searching_window.destroy).grid(row=1, column=0)

        self.departure.configure(text='ok')

    def search_destination(self, target_location):
        self.searching_window = Tk()
        self.result_scroll = Scrollbar(self.searching_window)
        self.result_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        self.result_list = Listbox(self.searching_window, yscrollcommand=self.result_scroll.set)

        self.location_name, self.lx, self.ly = transferAPI.search_location(target_location)

        for i in range(len(self.location_name)):
            self.result_list.insert(i, str(self.location_name[i]))
        self.result_list.grid(row=0, column=0)
        self.result_scroll['command'] = self.result_list.yview
        Button(self.searching_window, text='확인', command=self.searching_window.destroy).grid(row=1, column=0)

        self.destination.configure(text=str(self.result_list.curselection()))


GUI()
