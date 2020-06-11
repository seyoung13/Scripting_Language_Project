from tkinter import*
import transferAPI
import webbrowser
import folium
import folium.plugins
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

        #Label(self.window, text='이메일 주소').grid(row=3, column=0, padx=10, pady=5)
        #Entry(self.window).grid(row=3, column=1)
        #Button(self.window, text='보내기').grid(row=3, column=2, stick='w', padx=10)

        self.window.mainloop()

    def search(self, classification_code, target_location):
        search_window = Tk()
        result_scroll = Scrollbar(search_window)
        result_scroll.grid(row=0, column=1, sticky='w'+'n'+'s')
        result_list = Listbox(search_window, yscrollcommand=result_scroll.set)

        if target_location:
            if classification_code == DEPARTURE:
                self.start_x.clear(), self.start_y.clear()
                location_name, self.start_x, self.start_y = transferAPI.search_location(target_location)
            else:
                self.end_x.clear(), self.end_y.clear()
                location_name, self.end_x, self.end_y = transferAPI.search_location(target_location)
            for i in range(len(location_name)):
                result_list.insert(i, str(location_name[i]))

        result_list.grid(row=0, column=0)
        result_scroll['command'] = result_list.yview
        Button(search_window, text='확인', command=lambda:
            self.set_location(classification_code, result_list, search_window)).grid(row=1, column=0)

        Button(search_window, text='지도 보기', command=lambda:
            self.show_location(classification_code, result_list)).grid(row=1, column=1)

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
        path_window = Tk()
        path_window.title('경로')
        path_scroll = Scrollbar(path_window)
        path_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        path_list = Listbox(path_window, yscrollcommand=path_scroll.set, width=0, height=0)
        path_list.grid(row=0, column=0)

        if self.selected_index >= 0:
            departure_name, fx, fy, destination_name, tx, ty, route, minutes = transferAPI.search_path_info_bus(
                self.start_x[self.selected_index], self.start_y[self.selected_index],
                self.end_x[self.selected_index], self.end_y[self.selected_index])
            for i in range(len(departure_name)):
                path = ''
                transfer_time = len(departure_name[i])
                for j in range(len(departure_name[i])):
                    path += departure_name[i][j] + ' ' + route[i][j] + ' 탑승 ~ ' + destination_name[i][j] + ' 하차'
                    if transfer_time > 1:
                        path += ' <환승> '
                        transfer_time -= 1
                path += ' |소요 시간: ' + str(minutes[i]) + '분|'
                path_list.insert(i, path)

            Button(path_window, text='지도 보기', command=lambda:
                self.show_path(path_list, departure_name, fx, fy, destination_name, tx, ty)).grid(row=1, column=1)

    def set_path_sub(self):
        path_window = Tk()
        path_window.title('경로')
        path_scroll = Scrollbar(path_window)
        path_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        path_list = Listbox(path_window, yscrollcommand=path_scroll.set, width=0, height=0)
        path_list.grid(row=0, column=0)

        if self.selected_index >= 0:
            departure_name, fx, fy, destination_name, tx, ty, route, minutes = transferAPI.search_path_info_sub(
                self.start_x[self.selected_index], self.start_y[self.selected_index],
                self.end_x[self.selected_index], self.end_y[self.selected_index])
            for i in range(len(departure_name)):
                path = ''
                transfer_time = len(departure_name[i])
                for j in range(len(departure_name[i])):
                    path += departure_name[i][j] + ' ' + route[i][j] + ' 탑승 ~ ' + destination_name[i][j] + ' 하차'
                    if transfer_time > 1:
                        path += ' <환승> '
                        transfer_time -= 1
                path += ' |소요 시간: ' + str(minutes[i]) + '분|'
                path_list.insert(i, path)

            Button(path_window, text='지도 보기', command=lambda:
                self.show_path(path_list, departure_name, fx, fy, destination_name, tx, ty)).grid(row=1, column=1)

    def set_path_bus_n_subway(self):
        path_window = Tk()
        path_window.title('경로')
        path_scroll = Scrollbar(path_window)
        path_scroll.grid(row=0, column=1, sticky='w' + 'n' + 's')
        path_list = Listbox(path_window, yscrollcommand=path_scroll.set, width=0, height=0)
        path_list.grid(row=0, column=0)

        if self.selected_index >= 0:
            departure_name, fx, fy, destination_name, tx, ty, route, minutes = transferAPI.search_path_info_bus_N_sub(
                self.start_x[self.selected_index], self.start_y[self.selected_index],
                self.end_x[self.selected_index], self.end_y[self.selected_index])
            for i in range(len(departure_name)):
                path = ''
                transfer_time = len(departure_name[i])
                for j in range(len(departure_name[i])):
                    path += departure_name[i][j] + ' ' + route[i][j] + ' 탑승 ~ ' + destination_name[i][j] + ' 하차'
                    if transfer_time > 1:
                        path += ' <환승> '
                        transfer_time -= 1
                path += ' |소요 시간: ' + str(minutes[i]) + '분|'
                path_list.insert(i, path)

            Button(path_window, text='지도 보기', command=lambda:
                self.show_path(path_list, departure_name, fx, fy, destination_name, tx, ty)).grid(row=1, column=1)

    def show_location(self, classification_code, location_list):
        if location_list.curselection():
            self.selected_index = location_list.curselection()[0]
            location_info = location_list.get(self.selected_index)

            if classification_code == DEPARTURE:
                x, y = self.start_x[self.selected_index], self.start_y[self.selected_index]
            else:
                x, y = self.end_x[self.selected_index], self.end_y[self.selected_index]

            # 위도 경도 지정
            map_osm = folium.Map(location=[y, x], zoom_start=16)
            # 마커 지정
            folium.Marker([y, x], popup=location_info).add_to(map_osm)
            # html 파일로 저장
            map_osm.save('osm.html')
            webbrowser.open_new('osm.html')

    def show_path(self, path_list, departure_name, fx, fy, destination_name, tx, ty):
        if path_list.curselection():
            i = path_list.curselection()[0]

            map_osm = folium.Map(location=[fy[i][0], fx[i][0]], zoom_start=16)
            # 위도 경도 지정
            for j in range(len(departure_name[i])):
                # 마커 지정
                folium.Marker([fy[i][j], fx[i][j]], popup=departure_name[i][j]).add_to(map_osm)
            #folium.plugins.polyline_offset([fy[i][j], fx[i][j]], weight=1, color='blue', opacity=1)

            for j in range(len(departure_name[i])):
                # 마커 지정
                folium.Marker([ty[i][j], tx[i][j]], popup=destination_name[i][j]).add_to(map_osm)
            # html 파일로 저장
            map_osm.save('osm.html')
            webbrowser.open_new('osm.html')


GUI()
