import sys
import os
import sqlite3
import mutagen
import datetime
import time
import threading
import random

from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtDesigner import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.play_stop_Button = QPushButton(parent=self.centralwidget)
        self.play_stop_Button.setGeometry(QRect(340, 500, 101, 51))
        self.play_stop_Button.setObjectName("pushButton")

        self.new_music_button = QPushButton(parent=self.centralwidget)
        self.new_music_button.setGeometry(QRect(450, 500, 61, 51))
        self.new_music_button.setObjectName("pushButton_2")

        self.back_music_Button = QPushButton(parent=self.centralwidget)
        self.back_music_Button.setGeometry(QRect(270, 500, 61, 51))
        self.back_music_Button.setObjectName("pushButton_3")

        self.choose_folder = QPushButton(parent=self.centralwidget)
        self.choose_folder.setGeometry(QRect(20, 240, 191, 61))
        self.choose_folder.setObjectName("pushButton_4")

        self.new_playlist_button = QPushButton(parent=self.centralwidget)
        self.new_playlist_button.setGeometry(QRect(20, 170, 191, 61))
        self.new_playlist_button.setObjectName("pushButton_5")

        self.listView = QListWidget(parent=self.centralwidget)
        self.listView.setGeometry(QRect(240, 40, 531, 431))
        self.listView.setObjectName("listView")

        self.playlistView = QListWidget(parent=self.centralwidget)
        self.playlistView.setGeometry(QRect(10, 40, 211, 121))
        self.playlistView.setObjectName("listView")

        self.volume_Slider = QSlider(parent=self.centralwidget)
        self.volume_Slider.setGeometry(QRect(580, 520, 160, 22))
        self.volume_Slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_Slider.setObjectName("horizontalSlider")

        self.label = QLabel(parent=self.centralwidget)
        self.label.setGeometry(QRect(620, 500, 91, 20))
        self.label.setObjectName("label")

        self.label_2 = QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QRect(70, 10, 81, 21))
        self.label_2.setObjectName("label_2")

        self.current_playlist_label = QLabel(parent=self.centralwidget)
        self.current_playlist_label.setGeometry(QRect(480, 10, 81, 21))
        self.current_playlist_label.setObjectName("label_3")

        self.author_label = QLabel(parent=self.centralwidget)
        self.author_label.setGeometry(QRect(10, 290, 221, 71))
        self.author_label.setObjectName("label_4")

        self.name_label = QLabel(parent=self.centralwidget)
        self.name_label.setGeometry(QRect(10, 370, 221, 51))
        self.name_label.setObjectName("label_5")

        self.time_music = QLabel(parent=self.centralwidget)
        self.time_music.setGeometry(QRect(60, 490, 151, 51))
        self.time_music.setObjectName("label_6")

        self.radioButton = QRadioButton(parent=self.centralwidget)
        self.radioButton.setGeometry(QRect(50, 440, 131, 31))
        self.radioButton.setObjectName("radioButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Никита плейер"))
        self.play_stop_Button.setText(_translate("MainWindow", "►"))
        self.new_music_button.setText(_translate("MainWindow", ">>"))
        self.back_music_Button.setText(_translate("MainWindow", "<<"))
        self.radioButton.setText(_translate("MainWindow", "Случайный порядок"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">громкость</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Плейлисты</span></p></body></html>"))
        self.current_playlist_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">TextLabel</span></p></body></html>"))
        self.author_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">TextLabel</span></p></body></html>"))
        self.choose_folder.setText(_translate("MainWindow", "Добавить музыку"))
        self.name_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">TextLabel</span></p></body></html>"))
        self.time_music.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:24pt;\">TextLabel</span></p></body></html>"))
        self.new_playlist_button.setText(_translate("MainWindow", "Добавить плейлист"))

class MIDI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.random_choice = False
        self.volume = 0.5
        self.setupUi(self)
        self.volume_Slider.setTracking(True)
        self.play = True
        self.duration_stopped = 0

        self.con = sqlite3.connect('music.sqlite')
        self.cur = self.con.cursor()
        self.playlists = self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchall()
        self.current_playlist = self.playlists[0][0]
        self.current_music_info = [None, None, None]

        for j in self.playlists:
            j = j[0]
            self.playlistView.addItem(j)
        self.no_played = [i[0] for i in self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()]

        self.play_stop_Button.clicked.connect(lambda: self.change_play_stop())
        self.back_music_Button.clicked.connect(lambda: self.to_start())
        self.new_music_button.clicked.connect(lambda: self.change_music())
        self.volume_Slider.sliderReleased.connect(lambda: self.value_changed(self.volume_Slider.value()))
        self.choose_folder.clicked.connect(lambda: self.choose_folder_())
        self.new_playlist_button.clicked.connect(lambda: self.create_new_playlist())
        self.radioButton.toggled.connect(lambda: self.switch_choice())
        self.k = 1
        self.blit_music()
        self.listView.currentRowChanged.connect(
            lambda: self.proverca())
        self.playlistView.currentRowChanged.connect(lambda: self.if_playlist_changed(self.playlistView.currentRow()))

    def run_every_n_seconds(self, seconds, action, *args):
        threading.Timer(seconds, self.run_every_n_seconds, [seconds, action] + list(args)).start()
        action(*args)
    
    def switch_choice(self):
        self.random_choice = self.radioButton.isChecked()
        print(self.random_choice)
    def proverca(self):
        print(self.current_playlist)
        if self.listView.currentRow() != -1:
            self.load_mp3(self.cur.execute(
                f"""SELECT file FROM {self.current_playlist} WHERE id = {int(self.listView.currentRow()) + 1}""").fetchall()[0][0])
            self.current_music_info = self.current_music_info = [self.cur.execute(f"""SELECT author FROM {self.current_playlist} 
            WHERE id = {int(self.listView.currentRow()) + 1}""").fetchall()[0][0],
                                   self.cur.execute(f"""SELECT name FROM {self.current_playlist} 
                                   WHERE id = {int(self.listView.currentRow()) + 1}""").fetchall()[0][0], self.cur.execute(f"""SELECT duration FROM {self.current_playlist} 
            WHERE id = {int(self.listView.currentRow()) + 1}""").fetchall()[0][0]]
            _translate = QCoreApplication.translate
            self.author_label.setText(_translate("MainWindow", f"<html><head/><body><p><span style=\" font-size:20pt;\">{self.current_music_info[0]}</span></p></body></html>"))
            self.name_label.setText(_translate("MainWindow", f"<html><head/><body><p><span style=\" font-size:16pt;\">{self.current_music_info[1]}</span></p></body></html>"))
            self.nach = time.time()
            self.run_every_n_seconds(0.5, self.blit_time)
    def blit_music(self):
        self.listView.clear()
        for i in self.cur.execute(f"""SELECT name FROM {self.current_playlist} """).fetchall():
            i = i[0]
            self.listView.addItem(i)
    def choose_folder_(self):
        dirname = QFileDialog.getExistingDirectory(self, 'Выбрать папку', '')
        files = os.listdir(dirname)
        con = sqlite3.connect('music.sqlite')
        cur = con.cursor()
        try:
            new_id = cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()[-1][0] + 1
        except:
            new_id = 1
        for i in files:
            #print(dirname, i, new_id)
            self.find_data(dirname, i, new_id)
            new_id += 1

    def create_new_playlist(self):
        name_playlist, ok = QInputDialog().getText(self, 'Новый плейлист', 'Название:')
        if name_playlist and ok:
            self.cur.execute(f"""CREATE TABLE {name_playlist} (id INTEGER PRIMARY KEY UNIQUE NOT NULL, author TEXT, 
            name TEXT, file TEXT, duration INTEGER)""")
            self.con.commit()
            self.playlistView.addItem(name_playlist)
    def load_mp3(self, filename):
        media = QUrl.fromLocalFile(filename)
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(self.volume)
        self.player.setSource(media)
        self.play = False
        self.change_play_stop()

    def change_play_stop(self):
        if self.play:
            self.player.pause()
            self.play = False
            _translate = QCoreApplication.translate
            self.play_stop_Button.setText(_translate("MainWindow", "►"))
            #self.tread = threading.Thread(target=self.blit_time())
            self.time1 = time.time()
        else:
            self.player.play()
            self.play = True
            _translate = QCoreApplication.translate
            self.play_stop_Button.setText(_translate("MainWindow", "||"))
            try:
                self.duration_stopped += time.time() - self.time1
            except:
                pass


    def to_start(self):
        self.player.stop()
        if self.play:
            self.player.play()

    def value_changed(self, value):
        print(value)
        self.volume = value / 100
        self.audio_output.setVolume(self.volume)

    def change_music(self, filename):
        media = QUrl.fromLocalFile(filename)
        self.player.setSource(media)

    def find_data(self, dirname, filename, k):
        filename = dirname + '/' + filename
        audiofile = mutagen.File(filename)
        duration = int(datetime.timedelta(seconds=audiofile.info.length).total_seconds())
        song_title = str(audiofile.tags.getall('TIT2')[0])
        singer_title = str(audiofile.tags.getall('TPE1')[0])

        if len(self.cur.execute(f"""SELECT * FROM {self.current_playlist} WHERE author = ? and name = ?""",
                           (singer_title, song_title)).fetchall()) == 0:
            self.cur.execute(f"""INSERT INTO {self.current_playlist} (id, author, name, file, duration) VALUES (?, ?, ?, ?, ?);""",
                           (k, singer_title, song_title, filename, duration))
        self.con.commit()
        #self.con.close()
        self.listView.addItem(song_title)
        self.k += 1

    def if_playlist_changed(self, row):
        self.current_playlist = self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchall()[row][0]
        _translate = QCoreApplication.translate
        self.current_playlist_label.setText(_translate("MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt;\">{self.current_playlist}</span></p></body></html>"))
        self.blit_music()
        self.no_played = [i[0] for i in
                          self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()]

    def blit_time(self):
        #print('///////')
        cur_time = time.time() - self.nach - self.duration_stopped
        if self.play:
            if int(cur_time) <= self.current_music_info[2] :
            #cur_time = time.time() - self.nach
                print(int(cur_time))
                if int(cur_time) <= self.current_music_info[2]:
                    _translate = QCoreApplication.translate
                    self.time_music.setText(_translate("MainWindow", f"<html><head/><body><p><span style=\" font-size:24pt;\">{int(cur_time)}|{self.current_music_info[2]}</span></p></body></html>"))
            else:
                self.change_music()

    def change_music(self):
        max_id = self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()[-1][0]
        if self.random_choice:
            next_music = random.choice(self.no_played)
            self.no_played.remove(next_music)
            print(self.no_played)
            if len(self.no_played) == 0:
                self.no_played = [i[0] for i in
                                  self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()]
                self.no_played.remove(next_music)
        else:
            next_music = self.listView.currentRow() + 2
            if next_music > max_id:
                next_music = 1
        self.listView.setCurrentRow(next_music - 1)
        self.load_mp3(self.cur.execute(f"""SELECT file FROM {self.current_playlist} WHERE id = {next_music}""").fetchall()[0][0])
        self.nach = time.time()
        self.run_every_n_seconds(0.5, self.blit_time)

    def mouseDoubleClickEvent(self, event):
        print('////////')
        current_id = self.listView.currentRow() + 1
        self.cur.execute(f"""DELETE FROM {self.current_playlist} WHERE id = {current_id}""")
        result = self.cur.execute(f"""SELECT * FROM {self.current_playlist} WHERE id >= {current_id}""")
        for elem in result:
            self.cur.execute(f"""DELETE FROM {self.current_playlist} WHERE id = {elem[0]}""")
            self.cur.execute(f"""INSERT INTO {self.current_playlist} (id, author, name, file, duration) VALUES (?, ?, ?, ?, ?);""",
                        (elem[0] - 1, elem[1], elem[2], elem[3], elem[4]))
        self.con.commit()
        self.blit_music()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MIDI()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())