import sys,os

from PyQt5.QtWidgets import QApplication,QMessageBox,QHBoxLayout,QMainWindow,QDialog,QComboBox,QWidget,QGroupBox,QPushButton,QLabel,QButtonGroup,QLineEdit,QRadioButton,QFormLayout,QScrollArea,QVBoxLayout
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QPixmap
os.environ["QT_SCALE_FACTOR"] = "1.30"
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Login'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.lbl1=QLabel("Enter your Voter ID",self)
        self.lbl1.setStyleSheet("font: 16px")
        self.lbl1.move(100,100)
        self.lbl1.resize(200,70)
        
        self.lbl2=QLabel("Enter Your Voting Token",self)
        self.lbl2.setStyleSheet("font: 16px")
        self.lbl2.move(100,250)
        self.lbl2.resize(200,70)
        
        self.text_box1=QLineEdit(self)
        self.text_box1.move(400,100)
        self.text_box1.resize(400,70)
                
        self.text_box2=QLineEdit(self)
        self.text_box2.setEchoMode(QLineEdit.Password)
        self.text_box2.move(400,250)
        self.text_box2.resize(400,70)
        
        self.button1=QPushButton("Login",self)
        self.button1.clicked.connect(self.loginUser)
        self.button1.move(320,400)
        self.button1.resize(250,70)
        
        self.show()
        
    @pyqtSlot()
    def loginUser(self):
        uname=self.text_box1.text()
        passwrd=self.text_box2.text()
        if uname=="123" and passwrd=="123":
            self.hide()
            voting_win=VotingWindow(self)
        else:
            QMessageBox.about(self, "Alert","Please Enter Valid Credentials")             
class VotingWindow(QDialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'Cast Voting'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.lbl1=QLabel("Cast yout Vote",self)
        self.lbl1.setStyleSheet("font: 16px")
        
        self.candidate_list=['John','Alice','Michael','Mrinal','Trump','Modi']
        
        self.button1=QPushButton("Cast yout Vote",self)
        self.button1.clicked.connect(self.castVote)
        print("y")
        
        self.scrollLayout = QVBoxLayout()
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
    
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.lbl1)
        self.layout1.addSpacing(10) 
        self.layout1.addWidget(self.scrollArea)        
        self.layout1.addWidget(self.button1)
        self.layout1.addSpacing(20)

        self.init_candidates()
    def setCandidateList(self,candidate_list):
        self.candidate_list=candidate_list
        
    def init_candidates(self):
        self.button_group = QButtonGroup()
        for i in range(len(self.candidate_list)):
            
            layout = QHBoxLayout()
            
            rb=QRadioButton("")
            self.button_group.addButton(rb,i)
            
            lbl_box=QLabel(self.candidate_list[i],self)
            lbl_box.setStyleSheet("font:16px")
            
            layout.addWidget(rb)
            layout.addWidget(lbl_box)
            layout.addStretch(1)            
            
            self.scrollLayout.addLayout(layout)
            
        self.setLayout(self.layout1)
        self.show()
        
    @pyqtSlot()
    def castVote(self):
        print(self.button_group.checkedId())
        self.hide()
        voting_win=ThankYouWindow(self)

class ThankYouWindow(QDialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'ThankYou'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.lbl1=QLabel("Thank You For Voting",self)
        self.lbl1.setStyleSheet("font: 16px")
        self.lbl1.move(200,200)
        self.lbl1.resize(200,70)
        
        self.button1=QPushButton("Exit",self)
        self.button1.clicked.connect(self.exit_now)
        self.button1.move(320,400)
        self.button1.resize(250,70)
        self.show()

    @pyqtSlot()
    def exit_now(self):
        self.hide()
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWindow()
    sys.exit(app.exec_())