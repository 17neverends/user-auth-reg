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
    count = 0
    id_inc = 1

    def __init__(self, name, surname, nickname, password, mail):
        self.id = User.id_inc
        User.id_inc += 1
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.password = password
        self.mail = mail
        self.auth = 0
        User.count += 1

    @staticmethod
    def show_count():
        print(f'Всего попыток регистрации: {User.count}')

    def check(self):
        print(f"Проверка для пользователя {self.id}:")
        if type(self.name) == str and self.name == self.name.capitalize() and type(self.surname) == str and self.surname == self.surname.capitalize():
            print(f'{self.id} прошел проверку имени и фамилии ✅')
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
                    print(f'{self.id} прошел проверку никнейма ✅')
                    if len(self.password) < 8:
                        print(f'{self.id} не прошел проверку пароля (слишком короткий) ❌')
                    elif re.search(r'\d', self.password) is None or re.search(r'[A-Z]', self.password) is None:
                        print(f'{self.id} не прошел проверку пароля (без цифр и заглавных букв) ❌')
                    else:
                        print(f'{self.id} прошел проверку пароля ✅')
                        if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), self.mail):
                            print(f'{self.id} прошел проверку почты ✅ \nПользователь {self.id} успешно зарегистрировался ✅✅✅ ')
                            self.auth += 1
                            connection = sqlite3.connect('auth_users.db')
                            cursor = connection.cursor()
                            cursor.execute('INSERT INTO Users (name, surname, nickname, password, mail) VALUES (?, ?, ?, ?, ?)',
                                           (self.name, self.surname, self.nickname, self.password, self.mail))
                            connection.commit()
                            connection.close()
                        else:
                            print(
                                f'{self.id} не прошел проверку почты (некорректный ввод) ❌')
                else:
                    print(
                        f'{self.id} не прошел проверку никнейма (Пустое поле ввода) ❌')
        else:
            print(
                f'{self.id} не прошел проверку имени и фамилии (Регистр) ❌')


User1 = User("sarah", "Matrilos", "sarah2002", "123qweQwe__./", "try@mail.ru")
User2 = User("Travis", "gregoriev", "trasss", "qweyyyQwe", "uiiyu@yandex.ru")
User3 = User("Larah", "Matrilos", "", "password123", "ertrtert123@gmail.com")
User4 = User("Eray", "Kalpos", "abccds", "password123", "ertrtert123@gmail.com")
User5 = User("Sevil", "Retyl", "qwrgdf", "Password123", "ertrtert123@gmail.com")
User6 = User("Sevil", "Retyl", "fsdfs", "Password123", "ertrtert123@gmail.com")
User7 = User("Sveta", "Malinuk", "aas", "Password123", "ertrtert123@email.com")
User8 = User("Artur", "Welkut", "fdfgdsmif", "Password123", "ertrt123@gmail.com")
User9 = User("Mike", "Feliry", "qwe", "Pass12333333", "mikeqwe@gmail.com")
User10 = User("Kate", "Lipow", "kate124", "kate124KATE", "kata2000@gmail.com")
Users = [User1, User2, User3, User4, User5, User6, User7, User8, User9, User10]



def do_check(Users):
    auths = 0
    for User in Users:
        User.check()
        auths += User.auth
    print(f'Успешных авторизаций: {auths}')


do_check(Users)

connection = sqlite3.connect('auth_users.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM Users')
authorized_users = cursor.fetchall()
connection.close()
for user in authorized_users:
    print(
        f'ID: {user[0]}, Имя: {user[1]}, Фамилия: {user[2]}, Никнейм: {user[3]}, Почта: {user[5]} , Пароль: {user[4]}')
