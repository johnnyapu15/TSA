import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

FOLDER_NAME = 'results'
OCX_NODE = "{961DB208-0F2F-41F0-95C8-723633857844}"


class SDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S_Parser")
        self.setGeometry(500, 500, 400, 200)

        self.gocx = QAxWidget(OCX_NODE)
        self.gocx.ReceiveData.connect(self.received)

        self.lb1 = QLabel("주문번호")
        self.lb2 = QLabel("그래프타입")
        self.lb3 = QLabel("기간")
        self.lb4 = QLabel("시작일")
        self.lb5 = QLabel("끝일")
        self.lb6 = QLabel("TR 수")
        self.lb7 = QLabel("출력할 인덱스")
        self.lb8 = QLabel("일자,시간,시가,고가,저가,종가\n주가수정계수,거래량수정계수,\n락구분,단위거래량,단위거래대금")

        self.te1 = QTextEdit('265520')
        self.te2 = QTextEdit('D')
        self.te3 = QTextEdit('1')
        self.te4 = QTextEdit('20170101')
        self.te5 = QTextEdit('20170511')
        self.te6 = QTextEdit('9999')
        self.te7 = QTextEdit('0,1,2,3,4,5')
        self.te1.setFixedHeight(35)
        self.te2.setFixedHeight(35)
        self.te3.setFixedHeight(35)
        self.te4.setFixedHeight(35)
        self.te5.setFixedHeight(35)
        self.te6.setFixedHeight(35)
        self.te7.setFixedHeight(35)

        self.bt1 = QPushButton("조회 요청 및 저장")
        self.bt1.clicked.connect(self.requestChart)
        self.l1 = QGridLayout(self)

        self.l1.addWidget(self.lb1, 0,0)

        self.l1.addWidget(self.te1, 0,1)        
        self.l1.addWidget(self.lb2)
        self.l1.addWidget(self.te2)   
        self.l1.addWidget(self.lb3)
        self.l1.addWidget(self.te3)   
        self.l1.addWidget(self.lb4)
        self.l1.addWidget(self.te4)   
        self.l1.addWidget(self.lb5)
        self.l1.addWidget(self.te5)   
        self.l1.addWidget(self.lb6)
        self.l1.addWidget(self.te6)  
        self.l1.addWidget(self.lb7)
        self.l1.addWidget(self.te7)
        self.l1.addWidget(self.lb8)    
        self.l1.addWidget(self.bt1, 8,1)
        

        self.param = list()
        
    def saveChart(self):
        fileName = ""
        fileName = "_".join(self.param)
        fileName += ".txt"
        fp = open(FOLDER_NAME + '/' + fileName, 'w')
        
        count = self.gocx.GetMultiRowCount()
        column = self.te7.toPlainText().split(',')
        
        print('It will print out data of ' + str(count) + ' X ' + str(len(column)))
        for c in range(0, count):
            for i in column:
                fp.write(self.gocx.GetMultiData(count - c - 1, int(i)) + " ")
            fp.write("\n")
        print('Saved as ' + fileName + '.')
    def requestChart(self):
        self.param.clear()
        self.param.append(self.te1.toPlainText())
        self.param.append(self.te2.toPlainText())
        self.param.append(self.te3.toPlainText())
        self.param.append(self.te4.toPlainText())
        self.param.append(self.te5.toPlainText())
        self.param.append(self.te6.toPlainText())

        self.gocx.SetQueryName('TR_SCHART')
        i = 0
        for p in self.param:
            if(self.gocx.SetSingleData(i, p) != True):
                print("셋팅에 실패.")
                break
            i += 1
        if self.gocx.RequestData() == 0:
            print("요청에 실패")
        if self.gocx.GetErrorMessage() != "":
            print(self.gocx.GetErrorMessage())
    
    def received(self, no):
        print(str(no) + " TR Received.")
        self.saveChart()



app = QApplication(sys.argv)
myWin = SDialog()
myWin.show()
app.exec_()