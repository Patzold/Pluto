import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog

import numpy as np

import pluto as pl

util = pl.PlutoObject(None)

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(547, 349)
        self.last_action = None
        
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.selectImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectImageButton.setGeometry(QtCore.QRect(20, 10, 120, 31))
        self.selectImageButton.setObjectName("selectImageButton")
        self.selectImageButton.clicked.connect(self.selectpath)
        
        self.grabFromClipboardButton = QtWidgets.QPushButton(self.centralwidget)
        self.grabFromClipboardButton.setGeometry(QtCore.QRect(155, 10, 125, 31))
        self.grabFromClipboardButton.setObjectName("grabClipboardButton")
        self.grabFromClipboardButton.clicked.connect(self.grab_clipboard)
        
        self.imgPathLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgPathLabel.setGeometry(QtCore.QRect(20, 50, 681, 21))
        self.imgPathLabel.setObjectName("imgPathLabel")
        
        self.analyseButton = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton.setGeometry(QtCore.QRect(20, 90, 75, 25))
        self.analyseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton.setObjectName("analyseButton")
        self.analyseButton.clicked.connect(self.do_foxnews)
        
        self.analyseButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton2.setGeometry(QtCore.QRect(100, 90, 75, 25))
        self.analyseButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton2.setObjectName("analyseButton2")
        self.analyseButton2.clicked.connect(self.do_nyt)
        
        self.analyseButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton3.setGeometry(QtCore.QRect(180, 90, 75, 25))
        self.analyseButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton3.setObjectName("analyseButton3")
        self.analyseButton3.clicked.connect(self.do_facebook)
        
        self.analyseButton4 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton4.setGeometry(QtCore.QRect(260, 90, 75, 25))
        self.analyseButton4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton4.setObjectName("analyseButton3")
        self.analyseButton4.clicked.connect(self.do_whatsapp)
        
        self.analyseButton5 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton5.setGeometry(QtCore.QRect(340, 90, 75, 25))
        self.analyseButton5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton5.setObjectName("analyseButton5")
        self.analyseButton5.clicked.connect(self.do_wpost)
        
        self.analyseButton6 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton6.setGeometry(QtCore.QRect(20, 120, 75, 25))
        self.analyseButton6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton6.setObjectName("analyseButton6")
        self.analyseButton6.clicked.connect(self.do_welt)
        
        self.analyseButton7 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton7.setGeometry(QtCore.QRect(100, 120, 100, 25))
        self.analyseButton7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton7.setObjectName("analyseButton7")
        self.analyseButton7.clicked.connect(self.do_tagesschau)
        
        self.analyseButton8 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton8.setGeometry(QtCore.QRect(205, 120, 75, 25))
        self.analyseButton8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton8.setObjectName("analyseButton8")
        self.analyseButton8.clicked.connect(self.do_discord)
        
        self.analyseButton9 = QtWidgets.QPushButton(self.centralwidget)
        self.analyseButton9.setGeometry(QtCore.QRect(285, 120, 110, 25))
        self.analyseButton9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analyseButton9.setObjectName("analyseButton9")
        self.analyseButton9.clicked.connect(self.do_fbm)
        
        self.analyseSep = QtWidgets.QFrame(self.centralwidget)
        self.analyseSep.setGeometry(QtCore.QRect(20, 70, 201, 16))
        self.analyseSep.setFrameShadow(QtWidgets.QFrame.Plain)
        self.analyseSep.setLineWidth(1)
        self.analyseSep.setFrameShape(QtWidgets.QFrame.HLine)
        self.analyseSep.setObjectName("analyseSep")
        
        self.resultSep = QtWidgets.QFrame(self.centralwidget)
        self.resultSep.setGeometry(QtCore.QRect(20, 150, 201, 16))
        self.resultSep.setFrameShadow(QtWidgets.QFrame.Plain)
        self.resultSep.setLineWidth(1)
        self.resultSep.setFrameShape(QtWidgets.QFrame.HLine)
        self.resultSep.setObjectName("resultSep")
        
        self.actionSearch = QtWidgets.QPushButton(self.centralwidget)
        self.actionSearch.setGeometry(QtCore.QRect(20, 170, 110, 25))
        self.actionSearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.actionSearch.setObjectName("actionSearch")
        self.actionSearch.clicked.connect(self.nyt_search)
        
        self.actionJSON = QtWidgets.QPushButton(self.centralwidget)
        self.actionJSON.setGeometry(QtCore.QRect(20, 170, 110, 25))
        self.actionJSON.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.actionJSON.setObjectName("actionJSON")
        self.actionJSON.clicked.connect(self.save_json)
        
        self.actionSearch = QtWidgets.QPushButton(self.centralwidget)
        self.actionSearch.setGeometry(QtCore.QRect(280, 170, 110, 25))
        self.actionSearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.actionSearch.setObjectName("actionSearch")
        self.actionSearch.clicked.connect(self.nyt_search)
        
        self.googleSearch = QtWidgets.QPushButton(self.centralwidget)
        self.googleSearch.setGeometry(QtCore.QRect(150, 170, 110, 25))
        self.googleSearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.googleSearch.setObjectName("googleSearch")
        self.googleSearch.clicked.connect(self.google_search)
        
        self.actionSep = QtWidgets.QFrame(self.centralwidget)
        self.actionSep.setGeometry(QtCore.QRect(20, 200, 201, 16))
        self.actionSep.setFrameShadow(QtWidgets.QFrame.Plain)
        self.actionSep.setLineWidth(1)
        self.actionSep.setFrameShape(QtWidgets.QFrame.HLine)
        self.actionSep.setObjectName("actionSep")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 220, 211, 161))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 547, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pluto"))
        self.selectImageButton.setText(_translate("MainWindow", "Select Image..."))
        self.grabFromClipboardButton.setText(_translate("MainWindow", "use clipboard..."))
        self.imgPathLabel.setText(_translate("MainWindow", "Selected Image: [null]"))
        self.analyseButton.setText(_translate("MainWindow", "Fox News"))
        self.analyseButton2.setText(_translate("MainWindow", "NYT"))
        self.analyseButton3.setText(_translate("MainWindow", "FB"))
        self.analyseButton4.setText(_translate("MainWindow", "WhatsApp"))
        self.analyseButton5.setText(_translate("MainWindow", "W Post"))
        self.analyseButton6.setText(_translate("MainWindow", "WELT"))
        self.analyseButton7.setText(_translate("MainWindow", "Tagesschau"))
        self.analyseButton8.setText(_translate("MainWindow", "Discord"))
        self.analyseButton9.setText(_translate("MainWindow", "FB Messenger"))
        self.actionJSON.setText(_translate("MainWindow", "Save as JSON"))
        self.actionSearch.setText(_translate("MainWindow", "---"))
        self.googleSearch.setText(_translate("MainWindow", "Open Google"))
        self.label.setText(_translate("MainWindow", "Result:"))
    
    def selectpath(self):
        userInput, okPressed = QInputDialog.getText(self, "Input Image Path", "Please enter the path to your image:")
        if okPressed:
            self.imgPathLabel.setText("Selected Image: " + userInput)
            # self.photo.setPixmap(QtGui.QPixmap(userInput))
            self.img_path = userInput
        self.update()
    
    def grab_clipboard(self):
        from PIL import ImageGrab
        img = ImageGrab.grabclipboard().convert("RGB")
        img = np.array(img)
        self.img_path = img
        self.imgPathLabel.setText("Selected Image: clipboard content")
    
    def do_foxnews(self):
        self.last_action = "fox"
        try:
            img = img = pl.read_image(self.img_path)
            pubsplit, headline, subtitle, author, dotsplit = pl.FoxNews(img).analyse()
            self.label.setText("Result: \nAuthor: " + author + "\nSubtitle: " + subtitle + "\nHeadline: " + headline + "\nPublished: " + pubsplit + "\nTopic: " + dotsplit)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def do_facebook(self):
        self.last_action = "fb"
        try:
            img = img = pl.read_image(self.img_path)
            author, date, body_text, engagement_text = pl.Facebook(img).analyse(img)
            self.label.setText("Result: \nAuthor: " + author + "\nPublished: " + date + "\nPost: " + body_text + "\nEngagement: " + str(engagement_text))
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def do_twitter(self):
        # img = img = pl.read_image(self.img_path)
        # name, handle, text = pl.Twitter(img).analyse()
        # self.label.setText("Result: \nName: " + name + "\nHandle: " + handle + "\nText: " + text)
        self.label.setText("Twitter feature is currently unavailable due to update lag.")
        self.update()
    
    def do_nyt(self):
        self.last_action = "nyt"
        _translate = QtCore.QCoreApplication.translate
        self.actionSearch.setText(_translate("MainWindow", "NYT Search"))
        try:
            img = img = pl.read_image(self.img_path)
            nyt = pl.NYT(img)
            headline, subtitle, author = nyt.analyse(img)
            self.search_term = headline
            self.label.setText("Result: \nHeadline: " + str(headline) + "\nSubtitle: " + str(subtitle) + "\nAuthor: " + str(author))
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def nyt_search(self, query=str):
        pl.NYT(None).search(self.search_term)

    def do_wpost(self):
        self.last_action = "wpost"
        try:
            img = img = pl.read_image(self.img_path)
            wpost = pl.WPost(img)
            category, headline, author, date, body = wpost.analyse(img)
            self.label.setText("Result: \nHeadline: " + headline + "\nCategory: " + category + "\nAuthor(s): " + author + "\nPublished: " + date + "\nContent: " + body)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def do_welt(self):
        self.last_action = "welt"
        try:
            img = img = pl.read_image(self.img_path)
            welt = pl.WELT(img)
            headline, author, date, category = welt.analyse(img)
            self.label.setText("Result: \nHeadline: " + headline + "\nCategory: " + category + "\nPublished: " + date + "\nAuthor(s): " + author)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def do_tagesschau(self):
        self.last_action = "tag"
        try:
            img = img = pl.read_image(self.img_path)
            tschau = pl.Tagesschau(img)
            date, headline, body, category = tschau.analyse(img)
            self.label.setText("Result: \nHeadline: " + headline + "\nCategory: " + category + "\nPublished: " + date + "\nContent: " + body)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
        
    def do_discord(self):
        self.last_action = "discord"
        try:
            img = img = pl.read_image(self.img_path)
            discord = pl.Discord(img)
            return_list = discord.analyse(img)
            out = ""
            for msg in return_list:
                out += str(msg) + "\n"
            self.label.setText(out)#"Result: \nHeadline: " + headline + "\nCategory: " + category + "\nPublished: " + date + "\nContent: " + body)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def do_whatsapp(self):
        self.last_action = "whatsapp"
        try:
            img = img = pl.read_image(self.img_path)
            whatsapp = pl.WhatsApp(img)
            return_list = whatsapp.analyse(img)
            out = ""
            for msg in return_list:
                out += str(msg) + "\n"
            self.label.setText(out)#"Result: \nHeadline: " + headline + "\nCategory: " + category + "\nPublished: " + date + "\nContent: " + body)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def do_fbm(self):
        self.last_action = "fbm"
        try:
            img = img = pl.read_image(self.img_path)
            fbm = pl.FBM(img)
            return_list = fbm.analyse(img)
            out = ""
            for msg in return_list:
                out += str(msg) + "\n"
            self.label.setText(out)#"Result: \nHeadline: " + headline + "\nCategory: " + category + "\nPublished: " + date + "\nContent: " + body)
        except Exception as e:
            error_line = "(Error on line {})".format(sys.exc_info()[-1].tb_lineno)
            self.label.setText("Something went wrong!\n" + str(e) + "\n" + error_line)
        self.update()
    
    def save_json(self):
        userInput, okPressed = QInputDialog.getText(self, "Output File Path", "Please enter the path for the output file:")
        print(userInput[-5:])
        print(userInput)
        if okPressed:
            if userInput[-5:] != ".json":
                print("output path is not a .json file!")
                return
            
            try:
                img = img = pl.read_image(self.img_path)
                if self.last_action == "fb": pl.Facebook(img).to_json(img, userInput)
                elif self.last_action == "nyt": pl.NYT(img).to_json(img, userInput)
                elif self.last_action == "discord": pl.Discord(img).to_json(img, userInput)
                elif self.last_action == "whatsapp": pl.WhatsApp(img).to_json(img, userInput)
                elif self.last_action == "fbm": pl.FBM(img).to_json(img, userInput)
                elif self.last_action == "wpost": pl.WPost(img).to_json(img, userInput)
                elif self.last_action == "welt": pl.WELT(img).to_json(img, userInput)
                elif self.last_action == "fox": pl.FoxNews(img).to_json(img, userInput)
            except Exception as e:
                self.label.setText("Something went wrong!\n" + str(e))
                self.update()
    
    def google_search(self):
        pass
        # if self.last_action == "fb": pl.Facebook(img).to_json(img, userInput)
        # elif self.last_action == "nyt": pl.NYT(img).to_json(img, userInput)
        # elif self.last_action == "discord": pl.Discord(img).to_json(img, userInput)
        # elif self.last_action == "whatsapp": pl.WhatsApp(img).to_json(img, userInput)
        # elif self.last_action == "fbm": pl.FBM(img).to_json(img, userInput)
        # elif self.last_action == "wpost": pl.WPost(img).to_json(img, userInput)
        # elif self.last_action == "welt": pl.WELT(img).to_json(img, userInput)
        # elif self.last_action == "fox": pl.FoxNews(img).to_json(img, userInput)

    def update(self):
        self.centralwidget.adjustSize()
        self.imgPathLabel.adjustSize()
        self.label.adjustSize()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())