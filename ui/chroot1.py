# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chroot.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(598, 360)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.VLyout_chroot = QtWidgets.QVBoxLayout()
        self.VLyout_chroot.setContentsMargins(-1, 0, -1, -1)
        self.VLyout_chroot.setSpacing(40)
        self.VLyout_chroot.setObjectName("VLyout_chroot")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_11.addWidget(self.label_3)
        self.VLyout_chroot.addLayout(self.horizontalLayout_11)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.gridLayout_9.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.VLyout_chroot.addWidget(self.groupBox_3)
        self.gridLayout.addLayout(self.VLyout_chroot, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Chroot is accessing another operating system from this operating system. Grub-editor uses manjaro-chroot to chroot"))
        self.groupBox_3.setTitle(_translate("Form", "Select an operating system to chroot into"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())