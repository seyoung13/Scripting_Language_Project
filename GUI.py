from tkinter import*
import transferAPI
import webbrowser
import folium
import folium.plugins
import gmail
import spam
DEPARTURE, DESTINATION = range(2)


class GUI:

    def __init__(self):
        self.window = Tk()
        self.window.title("대중교통 경로 정보")

        Label(self.window, text='출발지').grid(row=0, column=0)
        Label(self.window, text='목적지').grid(row=1, column=0)

        # 출발지 목적지 좌표 정보
        self.departure = StringVar()
        self.destination = StringVar()
        self.start_x, self.start_y, self.end_x, self.end_y = [], [], [], []
        # 검색 리스트박스에서 선택한 장소의 인덱스 값을 가져오기 위한 변수
        self.selected_index = 0
        self.category = DEPARTURE

        # 출발지 및 목적지 검색 버튼
        self.departure_entry = Entry(self.window, textvariable=self.departure, width=30)
        self.departure_entry.grid(row=0, column=1)
        self.destination_entry = Entry(self.window, textvariable=self.destination, width=30)
        self.destination_entry.grid(row=1, column=1)
        self.departure_button = Button(self.window, text='검색', padx=12,
                                       command=lambda: self.search(DEPARTURE, self.departure_entry.get()))
        self.departure_button.grid(row=0, column=2)
        self.destination_button = Button(self.window, text='검색', padx=12,
                                         command=lambda: self.search(DESTINATION, self.destination_entry.get()))
        self.destination_button.grid(row=1, column=2)

        # 검색 결과 리스트박스와 스크롤바
        self.search_result_scroll = Scrollbar(self.window)
        self.search_result_scroll.grid(row=3, column=2, sticky='w' + 'n' + 's')
        self.search_result_list = Listbox(self.window, yscrollcommand=self.search_result_scroll.set, width=30, height=15)

        self.search_result_list.grid(row=3, column=1)
        self.search_result_scroll['command'] = self.search_result_list.yview
        Button(self.window, text='확인', command=lambda:
            self.set_location(self.category, self.search_result_list)).grid(row=4, column=1, sticky='w', ipadx=30)

        Button(self.window, text='지도 보기', command=lambda:
            self.show_location_map(self.category, self.search_result_list)).grid(row=4, column=1, sticky='e', ipadx=20)

        # 사이에 빈 공간 만들기
        Label(self.window).grid(row=2, padx=20)
        Label(self.window).grid(column=3, padx=20)
        Label(self.window).grid(row=7)

        # 환승 경로에 관한 변수
        self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = [], [], [], [], [], [], [], []
        # 경로 선택 라디오 버튼
        self.selected_radio_button = IntVar()

        Radiobutton(self.window, text='버스', value=0, variable=self.selected_radio_button).grid(row=0, column=4, sticky='w')
        Radiobutton(self.window, text='지하철', value=1, variable=self.selected_radio_button).grid(row=1, column=4, sticky='w')
        Radiobutton(self.window, text='버스+지하철', value=2, variable=self.selected_radio_button).grid(row=2, column=4, sticky='w')

        self.transfer_time = []
        self.is_sorted_by_transfer_time = False
        Button(self.window, text='경로 확인', command=self.select_path).grid(row=0, column=4, sticky='e')
        Button(self.window, text='시간 순 <-> 환승 횟수 순', command=self.sort_by_transfer_time).grid(row=2, column=4, sticky='e')

        # 경로 리스트박스와 스크롤바
        self.path_result_scroll = Scrollbar(self.window)
        self.path_result_scroll.grid(row=3, column=5, sticky='w' + 'n' + 's')
        self.path_result_list = Listbox(self.window, yscrollcommand=self.path_result_scroll.set, width=0, height=15)

        self.path_result_list.grid(row=3, column=4)
        self.path_result_scroll['command'] = self.path_result_list.yview

        Button(self.window, text='지도 보기', command=lambda: self.show_path_map(self.path_result_list,
                self.fname, self.fx, self.fy, self.tname, self.tx, self.ty)).grid(row=4, column=4, sticky='e', ipadx=20)

        # 이메일 연동
        self.email_address = Entry(self.window, width=40)
        self.email_address.grid(row=6, column=4)
        Button(self.window, text='메일'
                                 ' 보내기', command=lambda:
            gmail.send_email(self.write_email_message(), self.email_address.get())).grid(row=6, column=4, sticky='e', ipadx=10)

        '''Label(self.window, text='텔레그램 봇').grid(row=3, column=4, padx=10, pady=5)
        Button(self.window, text='지하철 시간표 출력', command=telegram_bot.start).grid(row=3, column=5, stick='w', padx=10)'''

        self.window.mainloop()

    def search(self, category, target_location):
        self.category = category

        self.search_result_list.delete(0, 'end')
        if target_location:
            if self.category == DEPARTURE:
                self.start_x.clear(), self.start_y.clear()
                location_name, self.start_x, self.start_y = transferAPI.search_location(target_location)
            else:
                self.end_x.clear(), self.end_y.clear()
                location_name, self.end_x, self.end_y = transferAPI.search_location(target_location)
            for i in range(len(location_name)):
                self.search_result_list.insert(i, str(location_name[i]))

    def set_location(self, category, location_list):
        if location_list.curselection():
            self.selected_index = location_list.curselection()[0]
            location_info = location_list.get(self.selected_index)
            if category == DEPARTURE:
                self.departure.set(location_info)
            else:
                self.destination.set(location_info)

    def select_path(self):
        if len(self.start_x) == 0 or len(self.end_x) == 0:
            return

        self.is_sorted_by_transfer_time = False
        value = self.selected_radio_button.get()
        if value == 0:
            self.set_path_bus()
        elif value == 1:
            self.set_path_sub()
        else:
            self.set_path_bus_n_sub()

    def sort_by_transfer_time(self):
        if self.is_sorted_by_transfer_time:
            self.select_path()
            return

        self.is_sorted_by_transfer_time = True
        self.path_result_list.delete(0, 'end')

        value = self.selected_radio_button.get()
        if value == 0:
            self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = \
                transferAPI.search_path_info_bus(self.start_x[self.selected_index], self.start_y[self.selected_index],
                                                 self.end_x[self.selected_index], self.end_y[self.selected_index])
        elif value == 1:
            self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = \
                transferAPI.search_path_info_sub(self.start_x[self.selected_index], self.start_y[self.selected_index],
                                                 self.end_x[self.selected_index], self.end_y[self.selected_index])
        else:
            self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = \
                transferAPI.search_path_info_bus_N_sub(self.start_x[self.selected_index], self.start_y[self.selected_index],
                                                 self.end_x[self.selected_index], self.end_y[self.selected_index])

        index_list = spam.sort_by_transfer_time(self.transfer_time)
        for i in range(len(self.fname)):
            path = ''
            transfer_time = len(self.fname[index_list[i]]) - 1
            for j in range(len(self.fname[index_list[i]])):
                path += self.fname[index_list[i]][j] + ' ' + self.route[index_list[i]][j] + ' 탑승 - ' + self.tname[index_list[i]][j] + ' 하차'
                if transfer_time > 0:
                    path += ' <환승> '
                    transfer_time -= 1
            path += ' |소요 시간: ' + str(self.minutes[index_list[i]]) + '분|'
            self.path_result_list.insert(i, path)

    def set_path_bus(self):
        self.path_result_list.delete(0, 'end')
        self.transfer_time.clear()

        if self.selected_index >= 0:
            self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = \
                transferAPI.search_path_info_bus(self.start_x[self.selected_index], self.start_y[self.selected_index],
                                                 self.end_x[self.selected_index], self.end_y[self.selected_index])
            if not self.fname:
                self.path_result_list.insert(0, "경로 없음")
            for i in range(len(self.fname)):
                path = ''
                transfer_time = len(self.fname[i]) - 1
                self.transfer_time.append(transfer_time)
                for j in range(len(self.fname[i])):
                    path += self.fname[i][j] + ' ' + self.route[i][j] + ' 탑승 - ' + self.tname[i][j] + ' 하차'
                    if transfer_time > 0:
                        path += ' <환승> '
                        transfer_time -= 1
                path += ' |소요 시간: ' + str(self.minutes[i]) + '분|'
                self.path_result_list.insert(i, path)

    def set_path_sub(self):
        self.path_result_list.delete(0, 'end')
        self.transfer_time.clear()

        if self.selected_index >= 0:
            self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = \
                transferAPI.search_path_info_sub(self.start_x[self.selected_index], self.start_y[self.selected_index],
                                                 self.end_x[self.selected_index], self.end_y[self.selected_index])
            if not self.fname:
                self.path_result_list.insert(0, "경로 없음")
            for i in range(len(self.fname)):
                path = ''
                transfer_time = len(self.fname[i]) - 1
                self.transfer_time.append(transfer_time)
                for j in range(len(self.fname[i])):
                    path += self.fname[i][j] + ' ' + self.route[i][j] + ' 탑승 - ' + self.tname[i][j] + ' 하차'
                    if transfer_time > 0:
                        path += ' <환승> '
                        transfer_time -= 1
                path += ' |소요 시간: ' + str(self.minutes[i]) + '분|'
                self.path_result_list.insert(i, path)

    def set_path_bus_n_sub(self):
        self.path_result_list.delete(0, 'end')
        self.transfer_time.clear()

        if self.selected_index >= 0:
            self.fname, self.fx, self.fy, self.tname, self.tx, self.ty, self.route, self.minutes = \
                transferAPI.search_path_info_bus_N_sub(self.start_x[self.selected_index], self.start_y[self.selected_index],
                                                       self.end_x[self.selected_index], self.end_y[self.selected_index])
            if not self.fname:
                self.path_result_list.insert(0, "경로 없음")
            for i in range(len(self.fname)):
                path = ''
                transfer_time = len(self.fname[i]) - 1
                self.transfer_time.append(transfer_time)
                for j in range(len(self.fname[i])):
                    path += self.fname[i][j] + ' ' + self.route[i][j] + ' 탑승 - ' + self.tname[i][j] + ' 하차'
                    if transfer_time > 0:
                        path += ' <환승> '
                        transfer_time -= 1
                path += ' |소요 시간: ' + str(self.minutes[i]) + '분|'
                self.path_result_list.insert(i, path)

    def show_location_map(self, classification_code, location_list):
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

    def write_email_message(self):
        msg = ''
        for i in range(self.path_result_list.size()):
            msg += self.path_result_list.get(i) + '\n'

        return msg

    def show_path_map(self, path_list, departure_name, fx, fy, destination_name, tx, ty):
        if path_list.curselection():
            i = path_list.curselection()[0]

            map_osm = folium.Map(location=[fy[i][0], fx[i][0]], zoom_start=16)
            # 위도 경도 지정
            for j in range(len(departure_name[i])):
                # 마커 지정
                folium.Marker([fy[i][j], fx[i][j]], popup=departure_name[i][j]).add_to(map_osm)

            for j in range(len(departure_name[i])):
                # 마커 지정
                folium.Marker([ty[i][j], tx[i][j]], popup=destination_name[i][j]).add_to(map_osm)
            # html 파일로 저장
            map_osm.save('osm.html')
            webbrowser.open_new('osm.html')

GUI()
