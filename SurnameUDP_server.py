import socket

students = {"Бирюков": "Илья", "Грибачев": "Максим", "Деркач": "Анастасия"
        , "Королев": "Артем", "Косов": "Роман", "Липатов": "Егор"
        , "Макин": "Денис", "Полубояров": "Максим", "Поляков": "Сергей"
        , "Попов": "Геннадий", "Родькин": "Андрей", "Фролов": "Леонид"
        , "Храбров": "Андрей", "Шабалина": "Полина"}

with socket.socket(type=socket.SOCK_DGRAM) as serversocket:
    serversocket.bind(('',8080))
    print("Сервер запущен...")
    while True:
        data, addr = serversocket.recvfrom(4096)
        surname = data.decode().strip()
        if surname in students:
            answer = f"Привет, {students[surname]}! \n".encode()
        else:
            answer = (f"Извините, студента с фамилией '{surname}' "
                      f"нет в списке.\n").encode()
        serversocket.sendto(answer, addr)