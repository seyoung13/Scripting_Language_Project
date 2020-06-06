from tkinter import*
import transferAPI
DEPARTURE, DESTINATION = range(2)


class GUI:

    def __init__(self):
        self.window = Tk()
        self.window.title("대중교통 경로 정보")

        Label(self.window, text='출발지').grid(row=0, column=0)
        Label(self.window, text='목적지').grid(row=1, column=0)

        self.departure = StringVar()
        self.destination = StringVar()
        self.start_x, self.start_y, self.end_x, self.end_y = [], [], [], []

        self.departure_entry = Entry(self.window, textvariable=self.departure)
        self.departure_entry.grid(row=0, column=1)
        self.destination_entry = Entry(self.window, textvariable=self.destination)
        self.destination_entry.grid(row=1, column=1)
        self.departure_button = Button(self.window, text='검색',
                                       command=lambda: self.search(DEPARTURE, self.departure_entry.get()))
        self.departure_button.grid(row=0, column=2)
        self.destination_button = Button(self.window, text='검색',
                                         command=lambda: self.search(DESTINATION, self.destination_entry.get()))
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

    def search(self, classification_code, target_location):
        self.searching_window = Tk()
        self.result_scroll = Scrollbar(self.searching_window)
        self.result_scroll.grid(row=0, column=1, sticky='w'+'n'+'s')
        self.result_list = Listbox(self.searching_window, yscrollcommand=self.result_scroll.set)

        if target_location:
            if classification_code == DEPARTURE:
                self.start_x.clear(), self.start_y.clear()
                location_name, self.start_x, self.start_y = transferAPI.search_location(target_location)
            else:
                self.end_x.clear(), self.end_y.clear()
                location_name, self.end_x, self.end_y = transferAPI.search_location(target_location)
            for i in range(len(location_name)):
                self.result_list.insert(i, str(location_name[i]))

        self.result_list.grid(row=0, column=0)
        self.result_scroll['command'] = self.result_list.yview
        Button(self.searching_window, text='확인', command=lambda:
            self.set_location(classification_code, self.result_list, self.searching_window)).grid(row=1, column=0)

    def set_location(self, classification_code, location_list, window, ):
        if location_list.curselection():
            i = location_list.curselection()
            location_info = location_list.get(i)
            if classification_code == DEPARTURE:
                print(self.start_x[i[0]], self.start_y[i[0]])
                self.departure.set(location_info)
                # location_list[location_list.curselection()]
            else:
                print(self.end_x[i[0]], self.end_y[i[0]])
                self.destination.set(location_info)
        window.destroy()

    def set_path_bus_n_subway(self, departure, destination):
        pass


GUI()
