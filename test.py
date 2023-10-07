import re
import sqlite3

connection = sqlite3.connect('auth_users.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    surname TEXT,
                    nickname TEXT,
                    password TEXT,
                    mail TEXT)''')
connection.commit()

class User:
    id_inc = 1

    def __init__(self):
        self.id = User.id_inc
        User.id_inc += 1
        self.name = None
        self.surname = None
        self.nickname = None
        self.password = None
        self.mail = None

    def check_name(self):
        if isinstance(self.name, str) and isinstance(self.surname, str) and self.name == self.name.capitalize() and self.surname == self.surname.capitalize():
            print(f'{self.name} прошел проверку имени и фамилии ✅')
        else:
            print(f'{self.name} не прошел проверку имени и фамилии (Регистр) ❌')


    
    def check_pass(self):
        if len(self.password) < 8:
            print(f'{self.name} не прошел проверку пароля (слишком короткий) ❌')
        elif re.search(r'\d', self.password) is None or re.search(r'[A-Z]', self.password) is None:
            print(f'{self.name} не прошел проверку пароля (без цифр и заглавных букв) ❌')
        else:
            print(f'{self.name} прошел проверку пароля ✅')

    def check_nickname(self):
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT nickname FROM Users WHERE nickname = ?', (self.nickname,))
        already_exist_nickname = cursor.fetchone()
        connection.close()
        if already_exist_nickname:
            print('Такой никнейм уже есть в базе данных ❌')
        elif len(self.nickname) == 0:
            print(f'{self.name} не прошел проверку никнейма (Пустое поле ввода) ❌')
        else:
            print(f'{self.name} прошел проверку никнейма ✅')

    def check_mail(self):
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT mail FROM Users WHERE mail = ?', (self.mail,))
        already_exist_mail = cursor.fetchone()
        connection.close()
        if already_exist_mail:
            print("Аккаунт с такой почтой уже есть в базе данных")
        elif not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), self.mail):
            print(f'{self.name} не прошел проверку почты (некорректный ввод) ❌')
        else:
            connection = sqlite3.connect('auth_users.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Users (name, surname, nickname, password, mail) VALUES (?, ?, ?, ?, ?)',
                            (self.name, self.surname, self.nickname, self.password, self.mail))
            connection.commit()
            connection.close()
            print(f'{self.name} прошел проверку почты ✅ \nПользователь {self.name} успешно зарегистрировался ✅✅✅')

    def find_mail(self):
        self.mail = input('Введите почту: ')
        print(f"Проверка для логина пользователя для авторизации:")
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT mail FROM Users WHERE mail = ?', (self.mail,))
        already_exist_mail = cursor.fetchone()
        connection.close()
        if already_exist_mail:
            print(f'Пользователь с почтой существует в базе данных ✅')
        else: 
            print('Пользователя с такой почтой нет в базе данных, пройдите регистрацию пожалуйста')

    def find_pass(self):
        password = input('Введите пароль: ')
        print(f"Проверка для пароля пользователя для авторизации:")
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM Users WHERE mail = ?', (self.mail,))
        already_exist_password = cursor.fetchone()
        connection.close()
        if already_exist_password and password == already_exist_password[0]:
            print(f'Вы успешно авторизовались ✅')
        else:
            print('Вы ввели неверный пароль')


    def registration(self):
        self.name = input('Введите имя: ')
        self.surname = input('Введите фамилию: ')
        self.nickname = input('Введите желаемый никнейм: ')
        self.password = input('Введите безопасный пароль: ')
        self.mail = input('Введите почту: ')
        print(f"Проверка для пользователя {self.name} для регистрации:")
        
        if len(self.name) == 0 or len(self.surname) == 0:
            print('Ошибка: Имя и фамилия должны быть заполнены ❌')
        else:
            self.check_name()
            self.check_nickname()
            self.check_pass()
            self.check_mail()

                
    def authorization(self):
        self.find_mail()
        self.find_pass()


def main():
    while True:
        print("Выберите действие:")
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            user = User()
            user.registration()
        elif choice == "2":
            user = User()
            user.authorization()
        elif choice == "3":
            break
        else:
            print("Некорректный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()



