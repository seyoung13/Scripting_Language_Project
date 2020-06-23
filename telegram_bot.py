import telepot
import sys
import traceback
import subwayinformationAPI
import time

token = '1044038828:AAHOownkIhmHzB8IkRPllvKz77spzGJIrgs'
chat_id = '1141194039'


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        send_message(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('찾기') and len(args) > 1:
        print('검색 중입니다.', args[1])
        route, name, station_id = subwayinformationAPI.get_station_info(args[1])
        msg = get_station_info_message(route, name, station_id)
        send_message(chat_id, msg)
    elif text.startswith('시간표') and len(args) > 1:
        print('시간표 출력 중입니다.', args[1])
        up_line_departure_time, up_line_end_station_name = subwayinformationAPI.get_up_line_timetable(args[1])
        down_line_departure_time, down_line_end_station_name = subwayinformationAPI.get_down_line_timetable(args[1])
        msg1 = get_timetable_message(up_line_departure_time, up_line_end_station_name)
        msg2 = get_timetable_message(down_line_departure_time, down_line_end_station_name)
        send_message(chat_id, msg1)
        send_message(chat_id, msg2)
    else:
        send_message(chat_id, '모르는 명령어입니다.\n찾기 [역명], 시간표 [ID] 중 하나의 명령을 입력하세요.')


def send_message(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


def get_station_info_message(route, name, station_id):
    msg = ''
    if not route:
        msg = '결과가 없습니다.'
    else:
        for i in range(len(route)):
            msg += '호선:\t' + route[i] + '\t역명: ' + name[i] + '\tID: ' + station_id[i] + '\n\n'

    return msg


def get_timetable_message(departure_time, end_station_name):
    msg = ''
    if not departure_time:
        msg = '결과가 없습니다.'
    else:
        for i in range(len(departure_time)):
            msg += end_station_name[i]+'행 열차\t' + departure_time[i][0]+departure_time[i][1] + ' : ' + \
                  departure_time[i][2]+departure_time[i][3] + '\t운행 시작' + '\n\n'

    return msg


bot = telepot.Bot(token)
update = bot.getUpdates()
send_message(chat_id, '찾기 [역명], 시간표 [ID] 중 하나의 명령을 입력하세요.')
bot.message_loop(handle)

while True:
    time.sleep(1000)