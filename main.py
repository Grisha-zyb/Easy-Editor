import os
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QWidget, QApplication, QFileDialog
)

STYLES = '''
QWidget{
    background-color:rgb(169, 181, 223);
}
QPushButton{
    background-color:rgba(45, 51, 107, 150);
    color:rgb(169, 181, 223);
    border-radius:10px;
    height:30px;
    font-size:15px;
}
QLabel{
    color:rgba(45, 51, 107, 150);
    font-size:20px;
}
QListWidget{
    color:rgb(45, 51, 107);
    background-color:rgba(45, 51, 107, 75);
    border-radius:10px;
    font-size:20px;
}
QPushButton#folder{
    background-color:rgba(45, 51, 107, 200);
    color:rgb(238, 102, 166);
}
'''

app = QApplication([])
app.setStyleSheet(STYLES)
win = QWidget()
win.setWindowTitle("Easy editor")
win.resize(700, 500)

btn_folder = QPushButton('Папка')
btn_folder.setObjectName('folder')
btn_left = QPushButton('Ліво')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Дзеркало')
btn_sharp = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')
btn_back = QPushButton('Назад')
btn_blur = QPushButton('Розмити')

lbl_image = QLabel("Тут буде картинка")

list_images = QListWidget()

vlay = QVBoxLayout()
vlay.addWidget(btn_folder)
vlay.addWidget(list_images)

hlayout = QHBoxLayout()
hlayout.addWidget(btn_left)
hlayout.addWidget(btn_right)
hlayout.addWidget(btn_mirror)
hlayout.addWidget(btn_back)
hlayout.addWidget(btn_sharp)
hlayout.addWidget(btn_bw)
hlayout.addWidget(btn_blur)

v1layout = QVBoxLayout()
v1layout.addWidget(lbl_image, )
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

    def flip_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def flip_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def back(self):
        showChosenImage()

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
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
btn_mirror.clicked.connect(workimage.mirror)
btn_left.clicked.connect(workimage.flip_left)
btn_right.clicked.connect(workimage.flip_right)
btn_sharp.clicked.connect(workimage.sharpen)
btn_back.clicked.connect(workimage.back)
btn_blur.clicked.connect(workimage.blur)

app.exec_()


