import socket

students = {"Бирюков": "Илья", "Грибачев": "Максим", "Деркач": "Анастасия"
        , "Королев": "Артем", "Косов": "Роман", "Липатов": "Егор"
        , "Макин": "Денис", "Полубояров": "Максим", "Поляков": "Сергей"
        , "Попов": "Геннадий", "Родькин": "Андрей", "Фролов": "Леонид"
        , "Храбров": "Андрей", "Шабалина": "Полина"}

with socket.create_server(('',8080)) as serversocket:
    print("Сервер запущен...")
    while True:
        conn, addr = serversocket.accept()
        data = conn.recv(1024)
        surname = data.decode().strip()

        if surname in students:
            greeting = f"Привет, {students[surname]}! \n"
            conn.send(greeting.encode())
        else:
            error_message = f"Извините, студента с фамилией '{surname}' нет в списке. \n"
            conn.send(error_message.encode())
        conn.close()
