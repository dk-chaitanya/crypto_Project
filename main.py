import sys,requests,os
from PyQt5.QtWidgets import QApplication, QComboBox,QWidget,QPushButton,QLabel,QLineEdit,QFormLayout,QScrollArea,QVBoxLayout
from PyQt5.QtCore import pyqtSlot,QThread,Qt
import time

from functools import lru_cache

os.environ["QT_SCALE_FACTOR"] = "1.30"

#if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
#if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


#Book search request background QT thread.
class BookGetThread(QThread):
    def __init__(self,search_term=None,parent=None):
        super(BookGetThread, self).__init__(parent)
        self.search_term=search_term
        self.parent=parent

        #Please note that this API credential key will be disabled after one week.
        self.googleapikey="AIzaSyBmQNKwLhn79Clin5QX2dpOge6A5WAsMmA"

    def setSearchTerm(self,search_term):
        self.search_term=search_term

    #thread.start()
    def run(self):
        curr_time=time.time()
        self.book_list=self.get_book(self.search_term)
        if self.book_list[0]=="Error connecting to Internet. Please try again later.":
            self.get_book.cache_clear()
        self.time_elapsed=time.time()-curr_time
            
    #cached book request handler.
    @lru_cache(maxsize=100)
    def get_book(self,search_term):
        parms = {"q":search_term, 'key':self.googleapikey}

        #try to get request
        try:
            request_ouput = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        except:
            return ["Error connecting to Internet. Please try again later."]
        requests_dict = request_ouput.json()
        book_list=[]
        if requests_dict["totalItems"]>0:
            for item in requests_dict["items"]:
                book_item="\n"            
                try:
                    book_item+="Title:   "+item["volumeInfo"]["title"]+"\n"
                except:
                    pass
                try:
                    book_item+="Authors:   "+",".join(item["volumeInfo"]["authors"])+"\n"
                except:
                    pass            
                try:
                    book_item+="AverageRating:   "+item["volumeInfo"]["averageRating"]+"\n"
                except:
                    pass
                try:
                    book_item+="PageCount:   "+str(item["volumeInfo"]["pageCount"])+"\n"
                except:
                    pass
                try:
                    if len(item["volumeInfo"]["industryIdentifiers"])==2:                
                        book_item+="ISBN(13):   "+str(item["volumeInfo"]["industryIdentifiers"][1]["identifier"])+"\n"
                    else:
                        book_item+="ISBN(13):   "+str(item["volumeInfo"]["industryIdentifiers"][0]["identifier"])+"\n"
                except:
                    pass                        
                try:
                    book_item+="Description:\n"+str(item["volumeInfo"]["description"])+"\n"
                except:
                    pass            
                try:
                    book_item+="Publisher:   "+item["volumeInfo"]["publisher"]+"\n"
                except:
                    pass            
                try:
                    book_item+="Categories:   "+",".join(item["volumeInfo"]["categories"])+"\n"
                except:
                    pass
                book_list.append(book_item)            
        else:
            book_list.append("No Matching Items Found")
        return book_list

#App UI
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Google Books Search APP '
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.book_list=[]

        self.button1=QPushButton("Search Book Database",self)
        self.button1.clicked.connect(self.getBookInfo)

        self.text_box1=QLineEdit(self)

        self.combobox1 = QComboBox(self)
        self.combobox1.addItem("Recents")
        self.combobox1.activated[str].connect(self.set_text_box)

        self.lbl1=QLabel("Type Book Title, ISBN number, Author Name, etc for searching.",self)

        self.scrollLayout = QFormLayout()
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_box1)
        self.layout.addWidget(self.combobox1)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.lbl1)
        self.layout.addWidget(self.scrollArea)

        self.get_custom_thread = BookGetThread(parent=self)        
        self.init_bookUI()

    #Book List UI Filler
    def init_bookUI(self):
        for i in reversed(range(self.scrollLayout.count())): 
            self.scrollLayout.itemAt(i).widget().setParent(None)        

        for i in self.book_list:
            lbl_box_temp=QLabel(i,self)
            lbl_box_temp.setWordWrap(True)
            lbl_box_temp.setStyleSheet("font:16px")
            self.scrollLayout.addWidget(lbl_box_temp)

        self.setLayout(self.layout)        
        self.show()

    #Setting textbox to recent combobox selection   
    @pyqtSlot(str)
    def set_text_box(self,recent):
        self.text_box1.setText(recent)

    #Book Search thread start function
    @pyqtSlot()
    def getBookInfo(self):
        search_term=self.text_box1.text()
        if search_term=="":
            pass
        else:
            if search_term not in [self.combobox1.itemText(i) for i in range(self.combobox1.count())]:
                self.combobox1.addItem(search_term)        
            self.combobox1.setCurrentIndex(0)
            self.lbl1.setText("Fetching.....")
            self.get_custom_thread.setSearchTerm(search_term)
            self.get_custom_thread.start()
            self.get_custom_thread.finished.connect(self.postGetWork)

    #Post Thread Work UI manipulation
    @pyqtSlot()
    def postGetWork(self):
        self.lbl1.setText(f"Time Elapsed:{round(self.get_custom_thread.time_elapsed, 5)} sec \n Total Results: {len(self.get_custom_thread.book_list)}\n")
        self.book_list=self.get_custom_thread.book_list
        self.init_bookUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
