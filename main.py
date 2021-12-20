from PyQt5 import QtCore ,QtWidgets, uic
import sys
from functools import partial
import subprocess
import threading


file_loc='/etc/default/grub'
import os
HOME =os.getenv('HOME')
subprocess.Popen([f'mkdir -p {HOME}/.grub_editor/snapshots'],shell=True)
from datetime import datetime as dt
from time import sleep
#! has to be changed on release
write_file='/opt/grub_fake.txt'
write_file=file_loc

commands=[]
to_write_data=None

def getValue(name):
    with open(file_loc) as file:
        print(file_loc,'file_loc')
        data =file.read()
        start_index =data.find(name)
        end_index =data[start_index+len(name):].find('\n')+start_index+len(name)
        print('end_index',end_index)
        print(data[start_index+len(name):end_index])
        if start_index <0:
            return "None"
        else:
            if end_index <0:
                return data[start_index+len(name):]
            else:
                return data[start_index+len(name):end_index]


def setValue(name,val):
    global to_write_data
    if to_write_data is None:
        with open(file_loc) as file:
            to_write_data =file.read()
    
    start_index =to_write_data.find(name)
    end_index =to_write_data[start_index+len(name):].find('\n')+start_index+len(name)
    print(start_index,'start_index',to_write_data[start_index:start_index+len(name)])
    print('end_index',end_index)
    
    to_write_data = to_write_data.replace(name+to_write_data[start_index+len(name):end_index],name+str(val))
    
    subprocess.Popen([f'mkdir -p {HOME}/.cache/grub_editor/'],shell=True)
    subprocess.Popen([f'touch {HOME}/.cache/grub_editor/grub.txt'],shell=True)
    with open(f'{HOME}/.cache/grub_editor/temp.txt','w') as file:
        file.write(to_write_data)



def clearLayout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())
                
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        
        uic.loadUi('main.ui',self)
        self.show()
        self.setUiElements()
        
        #dictionary to store qlineEdits for rename .stored widget is qlineEditWidget. key is index of the row
        self.rename_line_edits={}
        
        #dictionary for storing labels (rename) . key is index of the row
        self.btn_set.clicked.connect(self.btn_set_callback)
        self.rename_labels={}
        
        
    def setUiElements(self):
        """reloads the ui elements that should be reloaded"""
        self.ledit_grub_timeout.setText(getValue('GRUB_TIMEOUT='))
        
        if getValue('GRUB_TIMEOUT_STYLE=')=='hidden':
            self.comboBoxTimeoutStyle.setCurrentIndex(0)
        elif getValue('GRUB_TIMEOUT_STYLE=')=='menu':
            self.comboBoxTimeoutStyle.setCurrentIndex(1)
            
            
        self.createSnapshotList()
        
    #! combine all the commands to be executed into a string and then do it
    def saveConfs(self):
        
        setValue('GRUB_TIMEOUT=',self.ledit_grub_timeout.text())
        setValue('GRUB_TIMEOUT_STYLE=',['hidden', 'menu'][self.comboBoxTimeoutStyle.currentIndex()])
        subprocess.Popen([f'pkexec sh -c \' cp -f  "{HOME}/.cache/grub_editor/temp.txt"  '+write_file +' && sudo update-grub \' '],shell=True)

    def createSnapshot(self):
        with open(file_loc) as file:
            data= file.read()
        date_time =str(dt.now()).replace(' ','_')[:-7]
        print(date_time)
        subprocess.Popen([f'touch {HOME}/.grub_editor/snapshots/{date_time}'],shell=True)
        with open(f'{HOME}/.grub_editor/snapshots/{date_time}','w') as file:
            file.write(data)
        self.createSnapshotList()
    


    def btn_set_callback(self):
        print('set button callback here')
        grub_timeout_value=self.ledit_grub_timeout.text()
        # sleep(5)
        if grub_timeout_value=='0':
            print(grub_timeout_value=='0','grub_timeout_value==0 before what')
            self.ledit_grub_timeout.setText('Use 0.0 instead of 0 ')
            print(grub_timeout_value=='0','grub_timeout_value==0 after  what')
            self.ledit_grub_timeout.selectAll()
            self.ledit_grub_timeout.setFocus()
        else:
            try:
                float(grub_timeout_value)
                self.saveConfs()
            except Exception as e:
                print(e)
                self.ledit_grub_timeout.setText('not a number error')
                self.ledit_grub_timeout.selectAll()
                self.ledit_grub_timeout.setFocus()
        

    def btn_rename_callback(self,number):
        pass
    
    def btn_show_orginal_callback(self):
        global file_loc
        file_loc='/etc/default/grub'
        self.setUiElements()
        self.verticalLayout.itemAt(3).widget().deleteLater()
        
    def btn_view_callback(self,arg):
        global file_loc
        print(arg)
        file_loc= f'{HOME}/.grub_editor/snapshots/'+arg
        self.setUiElements()

        if self.verticalLayout.itemAt(3) is None:
            #create frame
            self.frame = QtWidgets.QFrame(self.edit_configurations)
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            
            
            
            self.lbl_snapshot_view= QtWidgets.QLabel(self.frame)
            self.lbl_snapshot_view.setObjectName('lbl_snapshot_view')
            self.lbl_snapshot_view.setText('You are currently looking at snapshot from '+arg)
            # self.lbl_snapshot_view.setStyleSheet('QLabel{border:1px solid #ff0000;\
            #                                      border-radius: 10px 10px 10px 10px;}')
            self.lbl_snapshot_view.setWordWrap(True)
            self.lbl_snapshot_view.setMinimumSize(100,30)
            self.HLayout_=QtWidgets.QHBoxLayout()
            
            
            # the '.' in the string is there to avoid QLabel getting affected
            self.frame.setStyleSheet('.QFrame{border:1px solid #ff0000;\
                                                 border-radius: 10px 10px 10px 10px;}')
            

            
            
            
            self.HLayout_.setObjectName('HLayout_')
            # self.HLayout_.addWidget(self.lbl_snapshot_view)
            
            #button to reverto to original
            self.btn_show_orginal =QtWidgets.QPushButton(self.frame)
            self.btn_show_orginal.setObjectName('btn_show_original')
            self.btn_show_orginal.setText('Show original configuration')
            self.btn_show_orginal.clicked.connect(self.btn_show_orginal_callback)
            # self.HLayout_.addWidget(self.btn_show_orginal)
            
            
            
            self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
            self.gridLayout_3.setObjectName("gridLayout_3")
            self.gridLayout_3.addWidget(self.lbl_snapshot_view, 0, 0, 1, 1)
            self.gridLayout_3.addWidget(self.btn_show_orginal, 0, 1, 1, 1)
            self.verticalLayout.addWidget(self.frame)
            
            
            
            # add 20 px margin to top of the HLayout_
            # self.HLayout_.setContentsMargins(0,0,20, 0)
            
            # self.verticalLayout.addLayout(self.HLayout_)
            self.lbl_snapshot_view.setText('You are currently looking at snapshot from '+arg)
            
            
            
            
            
        else:
            self.verticalLayout.itemAt(3)
            self.lbl_snapshot_view.setText('You are currently looking at snapshot from '+arg)
                
    def set_btn_callback(self,line):
        print(f'pkexec sh -c  \' cp -f  "{HOME}/.grub_editor/snapshots/{line}" {write_file} && sudo update-grub  \' ')
        subprocess.run([f'pkexec sh -c  \' cp -f  "{HOME}/.grub_editor/snapshots/{line}" {write_file}&& sudo update-grub  \' '],shell=True)
        self.setUiElements()
            
    def deleteCallbackCreator(self,arg):
        def func():
            string =f'rm {HOME}/.grub_editor/snapshots/{arg}'
            print(string)
            subprocess.Popen([f'rm \'{HOME}/.grub_editor/snapshots/{arg}\''],shell=True)
            global file_loc
            print(file_loc,'file_loc after delete')
            print(f'{HOME}/.grub_editor/snapshots/{arg}','condition check string')
            if file_loc == f'{HOME}/.grub_editor/snapshots/{arg}':
                file_loc='/etc/default/grub'
                print(file_loc,'file_loc after delete and before set ui elems')
                print(self.verticalLayout.itemAt(3),'before if')
                print(self.verticalLayout.itemAt(3),'before if')
                print(self.verticalLayout.itemAt(3),'before if')
                if self.verticalLayout.itemAt(3):
                    print(self.verticalLayout.itemAt(3))
                    self.verticalLayout.itemAt(3).widget().deleteLater()
                    print(file_loc,'file_loc after delete and before set ui elems')
            self.setUiElements()
        return func
    def btn_rename_callback(self,number):
        btn = self.sender()
        if btn.text() == 'rename':
            self.ledit_ = QtWidgets.QLineEdit(self.conf_snapshots)
            self.ledit_.setObjectName(f"ledit_{number}")
            self.rename_line_edits[number]=self.ledit_
            self.targetLabel=self.HLayouts_list[number].itemAt(0).widget()
            
            self.rename_labels[number] = self.targetLabel
            print(number)
            print(self.targetLabel)
            btn.parent().layout().replaceWidget(self.targetLabel,self.ledit_)
            self.targetLabel.deleteLater()
            self.ledit_.setText(self.lines[number])
            self.ledit_.selectAll()
            
            self.ledit_.setFocus()
            btn.setText('set name')
            
        elif btn.text() == 'set name':
            self.targetLabel=self.rename_labels[number]
            self.ledit_ = self.rename_line_edits[number]
            text = self.ledit_.text()
            line=self.lines[number]
            subprocess.Popen([f'mv \'{HOME}/.grub_editor/snapshots/{line}\' \'{HOME}/.grub_editor/snapshots/{text}\' '],shell=True)
            self.lbl_1 =QtWidgets.QLabel(self.conf_snapshots)
            self.lbl_1.setObjectName(f"label{number}")
            self.lbl_1.setText(self.lines[number])
            
            print(self.ledit_)
            # print(self.targetLabel.parent())
            btn.parent().layout().replaceWidget(self.ledit_,self.lbl_1)
            self.ledit_.deleteLater()
            btn.setText('rename')
            self.setUiElements()
            
        
        
               
    def createSnapshotList(self):
        contents = subprocess.check_output([f'ls {HOME}/.grub_editor/snapshots/'],shell=True).decode()
        print(contents)
        self.lines =contents.splitlines()

        self.HLayouts_list=[]
        number =0
        clearLayout(self.VLayout_snapshot)
        self.btn_create_snapshot = QtWidgets.QPushButton(self.conf_snapshots)
        self.btn_create_snapshot.setObjectName("btn_create_snapshot")
        self.btn_create_snapshot.setText("create a snapshot now")
        self.btn_create_snapshot.clicked.connect(self.createSnapshot)
        self.VLayout_snapshot.addWidget(self.btn_create_snapshot)
        for line in self.lines:
            #first number is 0
            
            self.HLayouts_list.append(QtWidgets.QHBoxLayout())
            self.HLayouts_list[-1].setObjectName(f'HLayout_snapshot{number}')
            
            #!needs change variables cannot be used
            self.lineEdit = QtWidgets.QLabel(self.conf_snapshots)
            self.lineEdit.setObjectName(f"lbl_snapshot{number}")
            self.lineEdit.setText(line)
            self.HLayouts_list[-1].addWidget(self.lineEdit)
            self.pushButton_3 = QtWidgets.QPushButton(self.conf_snapshots)
            self.pushButton_3.setObjectName(f"btn_rename{number}")
            self.pushButton_3.setText('rename')
            self.pushButton_3.clicked.connect(partial(self.btn_rename_callback,number))
            self.HLayouts_list[-1].addWidget(self.pushButton_3)
            self.pushButton = QtWidgets.QPushButton(self.conf_snapshots)
            self.pushButton.setObjectName(f"btn_view{number}")
            self.pushButton.setText('view')
            self.pushButton.clicked.connect(partial(self.btn_view_callback,line))
            self.HLayouts_list[-1].addWidget(self.pushButton)
            self.pushButton_3 = QtWidgets.QPushButton(self.conf_snapshots)
            self.pushButton_3.setObjectName(f"btn_delete{number}")
            self.pushButton_3.setText('delete')
            self.pushButton_3.clicked.connect(self.deleteCallbackCreator(line))
            self.HLayouts_list[-1].addWidget(self.pushButton_3)
            self.pushButton_2 = QtWidgets.QPushButton(self.conf_snapshots)
            self.pushButton_2.setObjectName(f"btn_set{number}")
            self.pushButton_2.setText('set')
            self.pushButton_2.clicked.connect(partial(self.set_btn_callback,line))
            self.HLayouts_list[-1].addWidget(self.pushButton_2)
            
            # print(self.VLayout_snapshot)
            self.VLayout_snapshot.addLayout(self.HLayouts_list[-1])
            
            #first number is 0
            
            number +=1

app =QtWidgets.QApplication(sys.argv)
window=Ui()
app.exec_()