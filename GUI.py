import sys,os
import sqlite3
from PyQt5.QtWidgets import QApplication,QMessageBox,QHBoxLayout,QMainWindow,QDialog,QComboBox,QWidget,QGroupBox,QPushButton,QLabel,QButtonGroup,QLineEdit,QRadioButton,QFormLayout,QScrollArea,QVBoxLayout
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QPixmap
import datetime

import custom_blockchain

os.environ["QT_SCALE_FACTOR"] = "1.30"
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

db = sqlite3.connect('VoterInfo.db')


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
        voterId=self.text_box1.text()
        token=self.text_box2.text()
        db = sqlite3.connect('VoterInfo.db')    
        cursor = db.cursor()

        cursor.execute(f"SELECT Voted FROM tokentable where voter='{voterId}' and token='{token}'")           
        all_rows1 = cursor.fetchall()
        print(all_rows1)      
        if len(all_rows1)>0: 
            if all_rows1[0][0]=='1':
                QMessageBox.about(self, "Alert","Already Voted")              
            else:
                self.hide()
                cursor.execute(f"SELECT name FROM candidate")            
                all_rows = cursor.fetchall()            
                print(all_rows)
                db.close()
                voting_win=VotingWindow(voterId,all_rows,self)         
        else:
            QMessageBox.about(self, "Alert","Invalid Credentials")                   
        db.close()
        
class VotingWindow(QDialog):
    def __init__(self,voterId,candidate_list,parent=None):
        super().__init__(parent)
        self.title = 'Cast Voting'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.voterId=voterId
        self.lbl1=QLabel("Cast yout Vote",self)
        self.lbl1.setStyleSheet("font: 16px")
        
        self.candidate_list=candidate_list
        
        self.button1=QPushButton("Cast yout Vote",self)
        self.button1.clicked.connect(self.castVote)
        
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
            
            lbl_box=QLabel(self.candidate_list[i][0],self)
            lbl_box.setStyleSheet("font:16px")
            
            layout.addWidget(rb)
            layout.addWidget(lbl_box)
            layout.addStretch(1)            
            
            self.scrollLayout.addLayout(layout)
            
        self.setLayout(self.layout1)
        self.show()
        
    @pyqtSlot()
    def castVote(self):
        if self.button_group.checkedId()>=0:
            print("voted ",self.candidate_list[self.button_group.checkedId()][0])
            
            blockchain = custom_blockchain.Blockchain()
            blockchain.load_stored_blockchain()
            
            verify_data=blockchain.is_chain_valid()
            if verify_data:
                
                blockchain.add_and_mine_block(self.voterId,self.candidate_list[self.button_group.checkedId()][0])
                blockchain.update_stored_blockchain()
                
                db = sqlite3.connect('VoterInfo.db')    
                cursor = db.cursor()
                cursor.execute(f"Update tokentable set voted='1' where voter='{self.voterId}'")            
                db.commit()
                
                self.hide()
                voting_win=ThankYouWindow(self.candidate_list[self.button_group.checkedId()][0],self)
            else:
                QMessageBox.about(self, "Alert","Blockchain Voting data corrupted. Voting is suspended currently. Please wait until further Notice.")                
                self.close()
        else:                            
            QMessageBox.about(self, "Alert","Please select one candidate.")                 
            
class ThankYouWindow(QDialog):

    def __init__(self,candidate,parent=None):
        super().__init__(parent)
        self.title = 'ThankYou'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.lbl1=QLabel(f"Thank You For Voting. \nYou Voted for {candidate}.\n\nPlease Press Exit.",self)
        self.lbl1.setStyleSheet("font: 20px")
        self.lbl1.move(200,200)
        self.lbl1.resize(500,140)
        
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