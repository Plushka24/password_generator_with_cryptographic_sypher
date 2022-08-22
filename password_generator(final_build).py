import random
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread
import sys
import sqlite3
import pyAesCrypt
import os
from threading import Thread
import glob
import time 



class App(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.alphabet = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h', 9:'i', 10:'j', 11:'k',
                         12:'l', 13:'m', 14:'n', 15:'o', 16:'p', 17:'q', 18:'r', 19:'s', 20:'t', 21:'u',
                         22:'v', 23:'w', 24:'x', 25:'y', 26:'z'}
        self.spec_change = {1: '.', 2: ',', 3: '?', 4: '!', 5: '@', 6: '#', 7: '$', 8: '%', 9: '^',
                            10: '&', 11: '*', 12: '(', 13: ')', 14: '-', 15: '+', 16: '=', 17: '>', 18: '<',  }

        self.colors = {1:'red', 2:'white', 3:'blue', 4:'green', 5:'purple', 6:'black', 7:'violet', 8:'gold', 9:'silver',
                       10:'gray', 11:'crimson', 12:'ruby', 13:'coral', 14:'flame', 15:'amber', 16:'emerald', 17:'mint',
                       18:'lime', 19:'azure', 20:'snowy', 21:'platinum', 22:'rust', 23:'khaki', 24:'maroon'}
        
        self.animal = {1:'cat', 2:'dog', 3:'lion', 4:'spider', 5:'tiger', 5:'puppy', 6:'hamster', 7:'parrot', 8:'rat',
                       9:'mouse', 10:'kitten', 11:'bull', 12:'cow', 13:'sheep', 14:'chicken', 15:'roaster', 16:'horse',
                       17:'goat',18:'kong', 19:'fox',20:'bear', 21:'wolf', 22:'rabbit',23:'deer',24:'boar', 25:'seal',
                       26:'camel', 27:'panda'}

        self.thread = Thread(target = self.denc)
        try:
            os.mkdir('C:/db')
        except:
            self.db_path = 'C:/db'
        self.db_path = 'C:/db/database.db'
        self.login = ''
        self.password_for_db = '' 
        self.buffer_size = 512*1024
        
        self.len_pass = 10 #длина пароля
        self.flag_for_add_bind = True
        self.flag_for_get_bind = True
        self.start()
        self.set()
    def start(self):
        self.ui = uic.loadUi('generator_password.ui')
        self.ui.show()

    def set(self):
        self.ui.spinBox.setValue(self.len_pass)
        self.ui.pushButton.clicked.connect(lambda: self.sum_func())
        self.ui.pushButton_2.clicked.connect(lambda: self.add())
        self.ui.pushButton_3.clicked.connect(lambda: self.get())
    def sum_func(self):
        try:
            self.generate_full_pass()
        except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
        if self.ui.checkBox.isChecked():
            self.generate_login()

    def start_change(self):# генерация стартового значения(буква/цифра)
        self.num_or_alph = random.randint(1,2)# с чего начинается пароль(буква/цифра)
        if self.num_or_alph == 1:
            self.password = str(random.randint(1, 9))
        else:
            low_up = random.randint(1,2)
            if low_up == 1:
                self.password = self.alphabet[random.randint(1, 26)].upper()
            elif low_up == 2:
                self.password = self.alphabet[random.randint(1, 26)].lower()
    def generate_full_pass(self):#генерация полного пароля
        self.count_spec = 0
        self.spec = 2
        if self.ui.radioButton.isChecked():
            self.spec = 3
        self.start_change()
        for i in range(self.ui.spinBox.value()-1):
            if self.count_spec > 1:
                self.spec = 2
            self.num_or_letter = random.randint(1, self.spec)
            if self.num_or_letter == 1:
                self.password += str(random.randint(1, 9))
            elif self.num_or_letter == 3:
                self.password += self.spec_change[random.randint(1, 18)]
                self.count_spec += 1
            else:
                low_up1 = random.randint(1,2)
                if low_up1 == 1:
                    self.password += self.alphabet[random.randint(1, 26)].upper()
                elif low_up1 == 2:
                    self.password += self.alphabet[random.randint(1, 26)].lower()
            
            self.ui.lineEdit.setText(self.password)
    def generate_login(self):#генерация логина
        self.random_color = self.colors[random.randint(1, 24)]
        self.random_animal = self.animal[random.randint(1, 27)]
        self.login = self.random_color + self.random_animal + str(random.randint(1, 5000))
        self.ui.lineEdit_2.setText(self.login)
    def database(self):#создание базы данных
        self.conn = sqlite3.connect(self.db_path
                                    )
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Data
                            (Resource_name TEXT, Login TEXT, Password TEXT)""")
        self.conn.commit()
        self.conn.close()
        self.dir = os.path.abspath(self.db_path)# получение пути к базе данных
        self.dir = self.dir.replace('\\', '/')
        self.dir = self.dir[:-12]

    def bind_for_add(self):
        self.ui_add.pushButton_4.clicked.connect(lambda: self.password_for_database_check())
        self.ui_add.pushButton_5.clicked.connect(lambda: self.add_data())
        self.ui_add.pushButton_6.clicked.connect(lambda: self.go_home_1())
        self.flag_for_add_bind == False
    def bind_for_get(self):
        self.ui_get.pushButton_7.clicked.connect(lambda: self.get_data())
        self.ui_get.pushButton_8.clicked.connect(lambda: self.go_home_2())
        self.ui_get.pushButton_6.clicked.connect(lambda: self.password_for_database_check_1())
        self.flag_for_get_bind == False
    def add(self):
        self.ui.hide()
        self.ui_add = uic.loadUi('add.ui')
        self.ui_add.show()
        if self.flag_for_add_bind == True:
            self.bind_for_add()
    def get(self):
        self.ui.hide()
        self.ui_get = uic.loadUi('get.ui')
        self.ui_get.show()
        if self.flag_for_get_bind == True:
            self.bind_for_get()
        
    def password_for_database_check(self):
        self.password_for_db_1 = self.ui_add.lineEdit_2.text()
        if self.password_for_db == '' and self.password_for_db_1 != '':
            if os.path.exists(os.path.abspath(self.db_path+'crp')) == True:
                self.thread.start()
            self.ui_add.lineEdit.setText(self.db_path)
            self.password_for_db = self.password_for_db_1
            self.ui_add.lineEdit_3.setEnabled(True)
            self.ui_add.lineEdit_4.setEnabled(True)
            self.ui_add.lineEdit_5.setEnabled(True)
            self.ui_add.pushButton_5.setEnabled(True)
            self.ui_add.label_9.setText('Confirm password')
            self.ui_add.lineEdit_2.setText('')
            self.database()
        elif not self.password_for_db_1:
            self.ui_add.label_9.setText('Invalid password')
        else:
            self.password_for_db_1 = self.ui_add.lineEdit_2.text()
            if self.password_for_db_1 == self.password_for_db:
                if os.path.exists(os.path.abspath(self.db_path+'crp')) == True:
                    self.thread.start()
                self.ui_add.lineEdit.setText(self.db_path)
                self.ui_add.lineEdit_3.setEnabled(True)
                self.ui_add.lineEdit_4.setEnabled(True)
                self.ui_add.lineEdit_5.setEnabled(True)
                self.ui_add.pushButton_5.setEnabled(True)
                self.ui_add.label_9.setText('Confirm password')
                self.ui_add.lineEdit_2.setText('')
                self.database()
            else:
                self.ui_add.label_9.setText('Invalid password')
    def password_for_database_check_1(self):
        self.password_for_db_1 = self.ui_get.lineEdit_7.text()
        if self.password_for_db == '' and self.password_for_db_1 != '':
            if os.path.exists(os.path.abspath(self.db_path+'crp')) == True:
                self.thread.start()
            self.ui_get.lineEdit_6.setText(self.db_path)
            self.password_for_db = self.password_for_db_1
            self.ui_get.lineEdit_8.setEnabled(True)
            self.ui_get.lineEdit_9.setEnabled(True)
            self.ui_get.lineEdit_10.setEnabled(True)
            self.ui_get.pushButton_7.setEnabled(True)
            self.ui_get.label_16.setText('Confirm password')
            self.ui_get.lineEdit_7.setText('')
            self.database()
        elif not self.password_for_db_1:
            self.ui_get.label_16.setText('Invalid password')
        else:
            self.password_for_db_1 = self.ui_get.lineEdit_7.text()
            if self.password_for_db_1 == self.password_for_db:
                if os.path.exists(os.path.abspath(self.db_path+'crp')) == True:
                    self.thread.start()
                self.ui_get.lineEdit_6.setText(self.db_path)
                self.ui_get.lineEdit_8.setEnabled(True)
                self.ui_get.lineEdit_9.setEnabled(True)
                self.ui_get.lineEdit_10.setEnabled(True)
                self.ui_get.pushButton_7.setEnabled(True)
                self.ui_get.label_16.setText('Confirm password')
                self.ui_get.lineEdit_7.setText('')
                self.database()
            else:
                self.ui_add.label_16.setText('Invalid password')

    def add_data(self):
        self.conn = sqlite3.connect(self.db_path)
        self.resource_name = self.ui_add.lineEdit_3.text()
        self.login_add = self.ui_add.lineEdit_4.text()
        self.password_add = self.ui_add.lineEdit_5.text()
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"INSERT or IGNORE INTO Data VALUES(?, ?, ?)", (self.resource_name,
                                                                           self.login_add,
                                                                           self.password_add))
        self.conn.commit()
        self.conn.close()
        self.resource_name = self.ui_add.lineEdit_3.setText('')
        self.ui_add.lineEdit_4.setText('')
        self.password_add = self.ui_add.lineEdit_5.setText('')
    def get_data(self):
        self.ui_get.label_19.setText('')
        self.conn = sqlite3.connect(self.db_path)
        self.resource_namee = self.ui_get.lineEdit_8.text()
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT Login, Password FROM Data WHERE Resource_name = ?', (self.resource_namee,))
        self.arr = self.cursor.fetchall()
        self.arr = str(self.arr)
        self.arr = self.arr.replace("[('", "").replace(")]", "").replace("',", "").replace("'", "")
        self.find = self.arr.find(' ')
        self.logg = self.arr[0:self.find]
        self.passs = self.arr[self.find+1:]
        if self.logg == '[' and self.passs == '[]':
            self.ui_get.label_19.setText('Not found')
        else:
            self.ui_get.lineEdit_9.setText(self.logg)
            self.ui_get.lineEdit_10.setText(self.passs)
            self.conn.commit()
            self.conn.close()

    def go_home_1(self):
        self.ui_add.hide()
        self.ui.show()
    def go_home_2(self):
        self.ui_get.hide()
        self.ui.show()
        
    def enc(self):
        for name in os.listdir(self.dir):
                    self.path = os.path.join(self.dir, name)
        pyAesCrypt.encryptFile(
        str(self.path),
        str(self.path)+"crp",
        self.password_for_db,
        self.buffer_size
        )
        os.remove(self.db_path)
        
    def denc(self):
        self.dir = os.path.abspath(self.db_path)# получение пути к базе данных
        self.dir = self.dir.replace('\\', '/')
        self.dir = self.dir[:-12]
        for name in os.listdir(self.dir):
                    self.path = os.path.join(self.dir, name)
        pyAesCrypt.decryptFile(
        str(self.path),
        str(os.path.splitext(self.path)[0])+".db",
        self.password_for_db,
        self.buffer_size
        )
        os.remove(self.db_path+'crp')
                
        
            
    
if __name__ == '__main__':
    APP = QApplication(sys.argv)
    example = App()
    APP.exec_()
    password_for_db = example.password_for_db
    db_path = 'C:/db/database.db'
    def enc(password_for_db):
        db_path1 = 'C:/db/database.db'
        buffer_size = 512*1024
        dirr = os.path.abspath(db_path1)# получение пути к базе данных
        dirr = dirr.replace('\\', '/')
        dirr = dirr[:-12]
        for name in os.listdir(dirr):
                    path = os.path.join(dirr, name)
        pyAesCrypt.encryptFile(
        str(path),
        str(path)+"crp",
        password_for_db,
        buffer_size
        )
        os.remove(db_path1)
    if os.path.exists(os.path.abspath(db_path+'crp')) != True:
        enc(password_for_db)
    
                

                 
   
        
