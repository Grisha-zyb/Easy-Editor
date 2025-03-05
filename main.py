import os
from PyQt5.QtGui import QPixmap
from PIL import Image
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

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lbl_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lbl_image.width(), lbl_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lbl_image.setPixmap(pixmapimage)
        lbl_image.show()

    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)



def showChosenImage():
    if list_images.currentRow() >= 0:
        filename = list_images.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()
list_images.itemClicked.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)

app.exec_()


