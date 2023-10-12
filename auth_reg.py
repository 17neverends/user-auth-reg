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
        self.name = input('Введите имя: ')
        self.surname = input('Введите фамилию: ')
        self.nickname = input('Введите желаемый никнейм: ')
        self.password = input('Введите безопасный пароль: ')
        self.mail = input('Введите почту: ')

    def check_name(self):
        if isinstance(self.name, str) and isinstance(self.surname, str) and self.name == self.name.capitalize() and self.surname == self.surname.capitalize():
            print(f'{self.name} прошел проверку имени и фамилии ✅')
            return True
        else:
            print(f'{self.name} не прошел проверку имени и фамилии (Регистр) ❌')
            return False

    def check_pass(self):
        if len(self.password) < 8:
            print(f'{self.name} не прошел проверку пароля (слишком короткий) ❌')
            return False
        elif re.search(r'\d', self.password) is None or re.search(r'[A-Z]', self.password) is None:
            print(f'{self.name} не прошел проверку пароля (без цифр и заглавных букв) ❌')
            return False
        else:
            print(f'{self.name} прошел проверку пароля ✅')
            return True

    def check_nickname(self):
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT nickname FROM Users WHERE nickname = ?', (self.nickname,))
        already_exist_nickname = cursor.fetchone()
        connection.close()
        if already_exist_nickname:
            print('Такой никнейм уже есть в базе данных ❌')
            return False
        elif len(self.nickname) == 0:
            print(f'{self.name} не прошел проверку никнейма (Пустое поле ввода) ❌')
            return False
        else:
            print(f'{self.name} прошел проверку никнейма ✅')
            return True

    def check_mail(self):
        connection = sqlite3.connect('auth_users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT mail FROM Users WHERE mail = ?', (self.mail,))
        already_exist_mail = cursor.fetchone()
        connection.close()
        if already_exist_mail:
            print("Аккаунт с такой почтой уже есть в базе данных ❌")
            return False
        elif not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'),
                              self.mail):
            print(f'{self.name} не прошел проверку почты (некорректный ввод) ❌')
            return False
        else:
            print(f'{self.name} прошел проверку почты ✅')
            return True

    def registration(self):
        print(f"Проверка для пользователя {self.name} для регистрации:")
        if len(self.name) == 0 or len(self.surname) == 0:
            print('Ошибка: Имя и фамилия должны быть заполнены ❌')
        else:
            name_check = self.check_name()
            nickname_check = self.check_nickname()
            pass_check = self.check_pass()
            mail_check = self.check_mail()
            if name_check and nickname_check and pass_check and mail_check:
                connection = sqlite3.connect('auth_users.db')
                cursor = connection.cursor()
                cursor.execute('INSERT INTO Users (name, surname, nickname, password, mail) VALUES (?, ?, ?, ?, ?)',
                               (self.name, self.surname, self.nickname, self.password, self.mail))
                connection.commit()
                connection.close()
                print(f'Пользователь {self.name} успешно зарегистрирован!')
            else:
                print(f'Пользователь {self.name} не прошел одну или несколько проверок, поэтому не был зарегистрирован ❌')

def find_mail():
    mail = input('Введите почту: ')
    print(f"Проверка для логина пользователя для авторизации:")
    connection = sqlite3.connect('auth_users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT mail FROM Users WHERE mail = ?', (mail,))
    already_exist_mail = cursor.fetchone()
    connection.close()
    if already_exist_mail:
        print(f'Пользователь с почтой существует в базе данных ✅')
        return True, mail
    else:
        print('Пользователя с такой почтой нет в базе данных, пройдите регистрацию, пожалуйста')
        return False, mail

def find_pass(mail):
    password = input('Введите пароль: ')
    print(f"Проверка для пароля пользователя для авторизации:")
    connection = sqlite3.connect('auth_users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM Users WHERE mail = ?', (mail,))
    already_exist_password = cursor.fetchone()
    connection.close()
    if already_exist_password and password == already_exist_password[0]:
        print(f'Вы ввели верный пароль ✅')
        return True
    else:
        print('Вы ввели неверный пароль ❌')
        return False

def authorization():
    mail_exists, mail = find_mail()
    if mail_exists:
        pass_exists = find_pass(mail)
        if mail_exists and pass_exists:
            print('Пользователь успешно авторизовался ✅')
        else:
            print('Вы ввели неверные данные ❌')

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
            authorization()
        elif choice == "3":
            break
        else:
            print("Некорректный ввод, попробуйте снова. ❌")


if __name__ == "__main__":
    main()
