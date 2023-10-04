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
connection.close()

class User:
    id_inc = 1

    def __init__(self):
        self.id = User.id_inc
        User.id_inc += 1
        self.name = ''
        self.surname = ''
        self.nickname = ''
        self.password = ''
        self.mail = ''
        self.user_reg = 0
        self.user_auth = 0

    def reg(self):
        self.name = input('Введите имя: ')
        self.surname = input('Введите фамилию: ')
        self.nickname = input('Введите желаемый никнейм: ')
        self.password = input('Введите безопасный пароль: ')
        self.mail = input('Введите почту: ')
        print(f"Проверка для пользователя {self.name} для регистрации:")
        if type(self.name) == str and self.name == self.name.capitalize() and type(self.surname) == str and self.surname == self.surname.capitalize():
            print(f'{self.name} прошел проверку имени и фамилии ✅')
            connection = sqlite3.connect('auth_users.db')
            cursor = connection.cursor()
            cursor.execute('SELECT nickname FROM Users WHERE nickname = ?', (self.nickname,))
            already_exist_nickname = cursor.fetchone()
            cursor.execute('SELECT mail FROM Users WHERE mail = ?', (self.mail,))
            already_exist_mail = cursor.fetchone()
            connection.close()
            if already_exist_nickname:
                print(f'Пользователь с никнеймом {self.nickname} уже существует в базе данных ❌')
            elif already_exist_mail:
                print(f'Пользователь с почтой {self.mail} уже существует в базе данных ❌')
            else:
                if len(self.nickname) != 0:
                    print(f'{self.name} прошел проверку никнейма ✅')
                    if len(self.password) < 8:
                        print(f'{self.name} не прошел проверку пароля (слишком короткий) ❌')
                    elif re.search(r'\d', self.password) is None or re.search(r'[A-Z]', self.password) is None:
                        print(f'{self.name} не прошел проверку пароля (без цифр и заглавных букв) ❌')
                    else:
                        print(f'{self.name} прошел проверку пароля ✅')
                        if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), self.mail):
                            print(f'{self.name} прошел проверку почты ✅ \nПользователь {self.name} успешно зарегистрировался ✅✅✅ ')
                            self.user_reg += 1
                            connection = sqlite3.connect('auth_users.db')
                            cursor = connection.cursor()
                            cursor.execute('INSERT INTO Users (name, surname, nickname, password, mail) VALUES (?, ?, ?, ?, ?)',
                                           (self.name, self.surname, self.nickname, self.password, self.mail))
                            connection.commit()
                            connection.close()
                        else:
                            print(
                                f'{self.name} не прошел проверку почты (некорректный ввод) ❌')
                else:
                    print(
                        f'{self.name} не прошел проверку никнейма (Пустое поле ввода) ❌')
        else:
            print(
                f'{self.name} не прошел проверку имени и фамилии (Регистр) ❌')

    def auth(self):
        mail = input('Введите почту: ')
        password = input('Введите пароль: ')
        print(f"Проверка для пользователя для авторизации:")
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM Users WHERE mail = ?', (mail,))
        already_exist_password = cursor.fetchone()
        cursor.execute('SELECT mail FROM Users WHERE mail = ?', (mail,))
        already_exist_mail = cursor.fetchone()
        connection.close()
        if already_exist_mail:
            print(f'Пользователь с почтой существует в базе данных ✅')
            if already_exist_password:
                if password == already_exist_password[0]:
                    print(f'Вы успешно авторизовались ✅')
                else:
                    print('Вы ввели неверный пароль')
            else:
                print('Пользователя с такой почтой нет в базе данных, пройдите регистрацию пожалуйста')
        else:
            print('Пользователя с такой почтой нет в базе данных, пройдите регистрацию пожалуйста')

def main():
    while True:
        print("Выберите действие:")
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Выход")
        choice = input("Введите номер действия: ")
        
        if choice == "1":
            user = User()
            user.reg()
        elif choice == "2":
            user = User()
            user.auth()
        elif choice == "3":
            break
        else:
            print("Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
