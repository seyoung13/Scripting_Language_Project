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
        # 리스트박스에서 선택한 장소의 인덱스 값을 가져오기 위한 변수
        self.selected_index = 0

        self.departure_entry = Entry(self.window, textvariable=self.departure)
        self.departure_entry.grid(row=0, column=1)
        self.destination_entry = Entry(self.window, textvariable=self.destination)
        self.destination_entry.grid(row=1, column=1)
        self.departure_button = Button(self.window, text='검색', padx=8,
                                       command=lambda: self.search(DEPARTURE, self.departure_entry.get()))
        self.departure_button.grid(row=0, column=2)
        self.destination_button = Button(self.window, text='검색', padx=8,
                                         command=lambda: self.search(DESTINATION, self.destination_entry.get()))
        self.destination_button.grid(row=1, column=2)

        Button(self.window, text='버스', command=self.set_path_bus).grid(row=2, column=1, sticky='w')
        Button(self.window, text='지하철', command=self.set_path_sub).grid(row=2, column=1)
        Button(self.window, text='혼합', command=self.set_path_bus_n_subway).grid(row=2, column=1, sticky='e')

        Label(self.window, text='예상 경로').grid(row=2, column=0, pady=10)

        Label(self.window, text='이메일 주소').grid(row=3, column=0, padx=10, pady=5)
        Entry(self.window).grid(row=3, column=1)
        Button(self.window, text='보내기').grid(row=3, column=2, stick='w', padx=10)

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

    def set_location(self, classification_code, location_list, window):
        if location_list.curselection():
            self.selected_index = location_list.curselection()[0]
            location_info = location_list.get(self.selected_index)
            if classification_code == DEPARTURE:
                self.departure.set(location_info)
            else:
                self.destination.set(location_info)
        window.destroy()

    def set_path_bus(self):
        self.path_window = Tk()
        self.path_window.title('경로')
        self.path_scroll = Scrollbar(self.path_window)
        self.path_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        self.path_list = Listbox(self.path_window, yscrollcommand=self.path_scroll.set, width=140, height=20)
        self.path_list.grid(row=0, column=0)

        if self.selected_index >= 0:
            departure_name, destination_name, route, minutes = transferAPI.search_path_info_bus(
                self.start_x[self.selected_index], self.start_y[self.selected_index],
                self.end_x[self.selected_index], self.end_y[self.selected_index])
            for i in range(len(departure_name)):
                path = ''
                transfer_time = len(departure_name[i])
                for j in range(len(departure_name[i])):
                    path += departure_name[i][j] + '에서 ' + route[i][j] + ' 탑승 ~ ' + destination_name[i][j] + '에서 하차'
                    if transfer_time > 1:
                        path += ' <환승> '
                        transfer_time -= 1
                self.path_list.insert(i, path)

    def set_path_sub(self):
        self.path_window = Tk()
        self.path_window.title('경로')
        self.path_scroll = Scrollbar(self.path_window)
        self.path_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        self.path_list = Listbox(self.path_window, yscrollcommand=self.path_scroll.set, width=140, height=20)
        self.path_list.grid(row=0, column=0)

        if self.selected_index >= 0:
            departure_name, destination_name, route, minutes = transferAPI.search_path_info_sub(
                self.start_x[self.selected_index], self.start_y[self.selected_index],
                self.end_x[self.selected_index], self.end_y[self.selected_index])
            for i in range(len(departure_name)):
                path = ''
                transfer_time = len(departure_name[i])
                for j in range(len(departure_name[i])):
                    path += departure_name[i][j] + '에서 ' + route[i][j] + ' 탑승 ~ ' + destination_name[i][j] + '에서 하차'
                    if transfer_time > 1:
                        path += ' <환승> '
                        transfer_time -= 1
                self.path_list.insert(i, path)

    def set_path_bus_n_subway(self):
        self.path_window = Tk()
        self.path_window.title('경로')
        self.path_scroll = Scrollbar(self.path_window)
        self.path_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        self.path_list = Listbox(self.path_window, yscrollcommand=self.path_scroll.set, width=140, height=20)
        self.path_list.grid(row=0, column=0)

        if self.selected_index >= 0:
            departure_name, destination_name, route, minutes = transferAPI.search_path_info_bus_N_sub(
                self.start_x[self.selected_index], self.start_y[self.selected_index],
                self.end_x[self.selected_index], self.end_y[self.selected_index])
            for i in range(len(departure_name)):
                path = ''
                transfer_time = len(departure_name[i])
                for j in range(len(departure_name[i])):
                    path += departure_name[i][j] + '에서 ' + route[i][j] + ' 탑승 ~ ' + destination_name[i][j] + '에서 하차'
                    if transfer_time > 1:
                        path += ' <환승> '
                        transfer_time -= 1
                self.path_list.insert(i, path)


GUI()
