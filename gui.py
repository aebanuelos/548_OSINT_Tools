### This script is responsible for displaying the GUI for the 538 OSINT Tool

import sys
import searchtweets
from pytz import unicode

import twittersample
import beautifulSoupCollect
import googlescrape_func

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# Window utilized for the Social Media OSINT Tool
class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Media OSINT Tool")
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.label = QLabel("Social Media Tool:", self)
        self.label.move(20, 30)

        # Text field
        self.twitterHandle = QLabel(self)
        self.twitterHandle.setText("Enter user's Twitter handle: ")
        self.responseBox = QLineEdit(self)

        self.twitterHandle.move(225, 145)
        self.twitterHandle.resize(300, 40)
        self.responseBox.move(225, 175)
        self.responseBox.resize(200, 32)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 32)
        pybutton.move(225, 215)

        toMain = QPushButton('Back', self)
        toMain.clicked.connect(self.returnToMain)
        toMain.resize(100, 30)
        toMain.move(550, 10)

        self.show()


    def clickMethod(self):
        tweets = twittersample.get_users_tweets(self.responseBox.text())
        rowcount = len(tweets['Username'])
        try:
            self.table = TableView(tweets, rowcount, 2)
            self.table.show()
            self.hide()
        except Exception as e:
            print(e)


    def returnToMain(self):
        self.w = Window()
        self.w.show()
        self.hide()

########################################################################################################################
# TEMP
class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
########################################################################################################################


# Window utilized for the Google Maps OSINT Tool
class Window3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Maps OSINT Tool")
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.label = QLabel("Google Maps OSINT Tool:", self)
        self.label.move(20, 30)
        self.label.resize(250, 40)

        # Text field

        self.locationLabel1 = QLabel(self)
        self.locationLabel1.setText("Please enter coordinates: ")
        self.responseBox1 = QLineEdit(self)

        self.locationLabel1.move(225, 145)
        self.locationLabel1.resize(300, 40)
        self.responseBox1.move(225, 175)
        self.responseBox1.resize(200, 32)



        self.locationLabel2 = QLabel(self)
        self.locationLabel2.setText("Please enter search radius in meters: ")
        self.responseBox2 = QLineEdit(self)

        self.locationLabel2.move(225, 95)
        self.locationLabel2.resize(300, 40)
        self.responseBox2.move(225, 125)
        self.responseBox2.resize(200, 32)



        self.locationLabel3 = QLabel(self)
        self.locationLabel3.setText("Please enter search term: ")
        self.responseBox3 = QLineEdit(self)

        self.locationLabel3.move(225, 45)
        self.locationLabel3.resize(300, 40)
        self.responseBox3.move(225, 75)
        self.responseBox3.resize(200, 32)




        pybutton = QPushButton('Gather Data', self) 
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 32)
        pybutton.move(225, 250)

        toMain = QPushButton('Back', self)
        toMain.clicked.connect(self.returnToMain)
        toMain.resize(100, 30)
        toMain.move(550, 10)

        self.show()

    def clickMethod(self):
        places = googlescrape_func.googleplace(self.responseBox1.text(), self.responseBox3.text(), self.responseBox2.text()) #location, search_string, distance
        #print('Your name: ' + self.responseBox1.text())
        #print('Your name: ' + self.responseBox2.text())
        #print('Your name: ' + self.responseBox3.text())
        self.done = DoneWindowe()
        self.done.show()
        self.hide()
    
    def returnToMain(self):
        self.w = Window()
        self.w.show()
        self.hide()

class DoneWindowe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Finished Gathering Data"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.label = QLabel("A list of relevant locations has been generated and will be available in the same directory as this script", self)
        self.label.move(20, 30)
        self.label.resize(650, 40)



















########################################################################################################################
# Window utilized for the Web Scraping Tool
class Window4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Scraping OSINT Tool")
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.label = QLabel("Web Scraping Tool - Utilizing Beautiful Soup 4:", self)
        self.label.move(20, 30)
        self.label.resize(450, 40)

        # Text field
        self.webURLLabel = QLabel(self)
        self.webURLLabel.setText("Please enter web URL: ")
        self.responseBox = QLineEdit(self)
        self.folderLabel = QLabel(self)
        self.folderLabel.setText("Please enter folder name to save content: ")
        self.responseFolder = QLineEdit(self)

        self.webURLLabel.move(225, 145)
        self.webURLLabel.resize(300, 40)
        self.responseBox.move(225, 175)
        self.responseBox.resize(200, 32)

        self.folderLabel.move(225, 195)
        self.folderLabel.resize(300, 40)
        self.responseFolder.move(225, 225)
        self.responseFolder.resize(200, 32)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 32)
        pybutton.move(225, 260)

        toMain = QPushButton('Back', self)
        toMain.clicked.connect(self.returnToMain)
        toMain.resize(100, 30)
        toMain.move(550, 10)

        self.show()

    def clickMethod(self):
        try:
            beautifulSoupCollect.savePage(self.responseBox.text(), self.responseFolder.text())
        except Exception as e:
            print(e)
        self.done = DoneWindow()
        self.done.show()
        self.hide()

    def returnToMain(self):
        self.w = Window()
        self.w.show()
        self.hide()


class DoneWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Finished Web Scraping"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.label = QLabel("Your webscraping has finished and the content may be seen on your desktop screen!", self)
        self.label.move(20, 30)
        self.label.resize(650, 40)


########################################################################################################################


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "ITMS 548 OSINT Tool"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        ###############################################################################################################
        # Button 1

        self.pushButton = QPushButton("Social Media OSINT Tool", self)
        # self.pushButton.setStyleSheet("QPushButton"
        #                                  "{"
        #                                  "background-color : yellow;"
        #                                  "}"
        #                                  "QPushButton::pressed"
        #                                  "{"
        #                                  "background-color : red;"
        #                                  "}"
        #                                  )
        self.pushButton.resize(240, 25)
        self.pushButton.move(225, 200)
        self.pushButton.setFont(QFont('Courier New', 13))
        self.pushButton.setToolTip("<h3>Start First OSINT Tool</h3>")

        ###############################################################################################################
        # Button 2

        self.pushButton2 = QPushButton("Google Maps OSINT Tool", self)
        # self.pushButton.setStyleSheet("QPushButton"
        #                                  "{"
        #                                  "background-color : yellow;"
        #                                  "}"
        #                                  "QPushButton::pressed"
        #                                  "{"
        #                                  "background-color : red;"
        #                                  "}"
        #                                  )
        self.pushButton2.resize(235, 25)
        self.pushButton2.move(225, 225)
        self.pushButton2.setFont(QFont('Courier New', 13))
        self.pushButton2.setToolTip("<h3>Start Second OSINT Tool</h3>")

        ###############################################################################################################
        # Button 3

        self.pushButton3 = QPushButton("Web Scraper Tool", self)
        # self.pushButton.setStyleSheet("QPushButton"
        #                                  "{"
        #                                  "background-color : yellow;"
        #                                  "}"
        #                                  "QPushButton::pressed"
        #                                  "{"
        #                                  "background-color : red;"
        #                                  "}"
        #                                  )
        self.pushButton3.resize(235, 25)
        self.pushButton3.move(225, 250)
        self.pushButton3.setFont(QFont('Courier New', 13))
        self.pushButton3.setToolTip("<h3>Start Third OSINT Tool</h3>")

        ################################################################################################################

        self.pushButton.clicked.connect(self.window2)
        self.pushButton2.clicked.connect(self.window3)
        self.pushButton3.clicked.connect(self.window4)
        self.main_window()

    def main_window(self):
        self.label = QLabel("Tools:", self)
        self.label.move(225, 175)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def window2(self):
        self.w = Window2()
        self.w.show()
        self.hide()

    def window3(self):
        self.w = Window3()
        self.w.show()
        self.hide()

    def window4(self):
        self.w = Window4()
        self.w.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
