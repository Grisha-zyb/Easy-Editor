import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QWidget, QApplication, QFileDialog
)

app = QApplication([])
win = QWidget()
win.setWindowTitle("Easy editor")
win.resize(700, 500)

btn_folder = QPushButton('Папка')
btn_left = QPushButton('Ліво')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Дзеркало')
btn_sharp = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')

lbl_image = QLabel("Тут буде картинка")

list_images = QListWidget()

vlay = QVBoxLayout()
vlay.addWidget(btn_folder)
vlay.addWidget(list_images)

hlayout = QHBoxLayout()
hlayout.addWidget(btn_left)
hlayout.addWidget(btn_right)
hlayout.addWidget(btn_mirror)
hlayout.addWidget(btn_sharp)
hlayout.addWidget(btn_bw)

v1layout = QVBoxLayout()
v1layout.addWidget(lbl_image)
v1layout.addLayout(hlayout)

mainLay = QHBoxLayout()
mainLay.addLayout(vlay,20)
mainLay.addLayout(v1layout,80)

win.setLayout(mainLay)

win.show()

#Фільтрує елементи папки за закінченням
def filter(files, extensions):
    filtered = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                filtered.append(filename)
    return filtered

workdir = ''

#Відкриває вікно для вибору папки
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


#Виводить у список всі відфільтровані елементи
def showFilenamesList():
    extensions = ['.jpg','.png','.gif','.bmp','.jpeg']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)

    list_images.clear()
    list_images.addItems(filenames)

btn_folder.clicked.connect(showFilenamesList)

app.exec_()


