import sys,os,time
import sqlite3
import hashlib
from PyQt5.QtWidgets import QApplication,QMessageBox,QHBoxLayout,QMainWindow,QDialog,QComboBox,QWidget,QGroupBox,QPushButton,QLabel,QButtonGroup,QLineEdit,QRadioButton,QFormLayout,QScrollArea,QVBoxLayout
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QPixmap
os.environ["QT_SCALE_FACTOR"] = "1.30"
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


db = sqlite3.connect('VoterInfo.db')
cursor = db.cursor()
cursor.execute(f"SELECT First,Last,Voter FROM UserInfo")            
all_rows = cursor.fetchall()            
print(all_rows)

class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Token_Generation'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.lbl1=QLabel("Enter your First Name",self)
        self.lbl1.setStyleSheet("font: 16px")
        self.lbl1.move(100,100)
        self.lbl1.resize(200,70)
        
        self.lbl4=QLabel("Enter your Last Name",self)
        self.lbl4.setStyleSheet("font: 16px")
        self.lbl4.move(100,200)
        self.lbl4.resize(200,70)        
        
        self.lbl2=QLabel("Enter Your Voter ID",self)
        self.lbl2.setStyleSheet("font: 16px")
        self.lbl2.move(100,300)
        self.lbl2.resize(200,70)
        
        self.text_box1=QLineEdit(self)
        self.text_box1.move(400,100)
        self.text_box1.resize(400,70)

        self.text_box3=QLineEdit(self)
        self.text_box3.move(400,200)
        self.text_box3.resize(400,70)
                
        self.text_box2=QLineEdit(self)
        self.text_box2.setEchoMode(QLineEdit.Password)
        self.text_box2.move(400,300)
        self.text_box2.resize(400,70)

        self.lbl3=QLabel("",self)
        self.lbl3.setStyleSheet("font: 16px")
        self.lbl3.move(50,500)
        self.lbl3.resize(800,70)
        
        self.button1=QPushButton("Generate Token",self)
        self.button1.clicked.connect(self.loginUser)
        self.button1.move(320,400)
        self.button1.resize(250,70)
        self.reset_login=False
        self.show()
        
    @pyqtSlot()
    def loginUser(self):
        if self.reset_login:
            self.text_box1.setText("")
            self.text_box2.setText("")
            self.lbl3.setText("")
            self.text_box3.setText("")
            self.button1.setText("Generate Token")
            self.reset_login=False
        else:            
            fname=self.text_box1.text()
            lname=self.text_box3.text()
            voterId=self.text_box2.text()
            db = sqlite3.connect('VoterInfo.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT First,Last,Voter FROM UserInfo where First='{fname}' and Last='{lname}' and voter='{voterId}'")            
            all_rows = cursor.fetchall()            
            print(all_rows)
            if len(all_rows)==1:
                cursor.execute(f"SELECT Voter FROM tokentable where voter='{voterId}'")            
                all_rows1 = cursor.fetchall()            
                print(all_rows1)
                if len(all_rows1)==0:
                    token=hashlib.sha1((voterId+str(time.time())).encode()).hexdigest()
                    token=token[:10]
                    print(token)
                    cursor.execute(f"INSERT INTO tokenTable values('{voterId}','{token}','0')")
                    db.commit()
                    self.lbl3.setText(f"Your Token is:-  \n{token}")
                    self.button1.setText("Clear All")
                    self.reset_login=True
                else:
                    QMessageBox.about(self, "Alert","Token already generated.")
                    self.button1.setText("Clear All")
                    self.reset_login=True                    
            else:
                QMessageBox.about(self, "Alert","Please Enter Valid Credentials")
            db.close()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWindow()
    sys.exit(app.exec_())