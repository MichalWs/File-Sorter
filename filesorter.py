from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QDialog
import sys
from multiprocessing.reduction import duplicate
import os
import shutil
import datetime


#vars for printing operations
files = 0
folders = 0
duplicates = 0

USER = os.environ['USERPROFILE']

#extracting metadata in separate functions so they can be referenced in OPTIONS_TO_DATA

def file_extension(entry):
    #extract file extension
    root_ext = os.path.splitext(entry)[1]
    return root_ext

def file_year(entry):
    #extract creation time
    c_time = os.path.getmtime(entry)
    #transform epoch time to date
    dt_c = datetime.datetime.fromtimestamp(c_time)
    #reformat time to YYYY format
    f_year = dt_c.strftime("%Y")
    return f_year

def file_month(entry):
    #extract creation time
    c_time = os.path.getmtime(entry)
    #transform epoch time to date
    dt_c = datetime.datetime.fromtimestamp(c_time)
    #reformat time to full month format
    f_month = dt_c.strftime("%B")
    return f_month

def file_size(entry):
    #extract file size
    f_size = os.path.getsize(entry)
    #convert size to MB
    f_size = int(f_size/(1024*1024))
    if f_size <= 100:
        f_size = "Up to 100 MB"
    else:
        f_size = "Over 100 MB"
    return f_size

#possible button options
SORT_OPTIONS = {1 : "None",
                2 : "Year",
                3 : "Month",
                4 : "File Extension",
                5 : "Size",
}

#current button values, these change
SORT_BUTTONS = {"sort_order_1" : 2,
                "sort_order_2" : 1,
                "sort_order_3" : 1,
} 

#text displayed on the button translates to function called
OPTIONS_TO_DATA = {"None" : "",
                   "Year" : file_year,
                  "Month" : file_month,
         "File Extension" : file_extension,
                   "Size" : file_size,
}


def folder_recursive_check(sourcedir, destdir, sort_order_1, sort_order_2, sort_order_3):
    with os.scandir(sourcedir) as entries:
        global files, folders, duplicates
        #for a file in folder
        for entry in entries:
            #if entry is a file
            if os.path.isfile(entry):
                #get file name
                file_name = entry.name
                #create directory path: destination folder\sort button 1\sort button 2\sort button 3              
                fin_path = os.path.join(destdir, sort_order_1(entry), sort_order_2(entry), sort_order_3(entry))
                #create directory path: destination folder\sort button 1\sort button 2\sort button 3\file name
                fin_file_path = os.path.join(fin_path, file_name)
                #if destination directory doesn't exist create directory and copy file
                if not os.path.exists(fin_path):
                    os.makedirs(fin_path)
                    shutil.copy(entry.path, fin_path)
                #if file already copied print information about duplicate
                elif os.path.exists(fin_file_path):
                    duplicates += 1
                    print(f"{entry.name} already copied, duplicate count {duplicates}")
                #if directory exists and file is not there copy file
                else:
                    shutil.copy(entry.path, fin_path)
                files +=1
                print(f"file {files} copied")
            #if entry is a folder
            else:
                folder_recursive_check(entry, destdir, sort_order_1, sort_order_2, sort_order_3)
                folders +=1
                print(f"folder {folders} copied")

#constructor class for UI
class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(371, 311)
        self.source_text_field = QtWidgets.QLineEdit(Dialog)
        self.source_text_field.setGeometry(QtCore.QRect(12, 60, 301, 21))
        self.source_text_field.setObjectName("source_text_field")
        self.destination_text_field = QtWidgets.QLineEdit(Dialog)
        self.destination_text_field.setGeometry(QtCore.QRect(10, 140, 301, 22))
        self.destination_text_field.setObjectName("destination_text_field")
        self.Confirm_button = QtWidgets.QPushButton(Dialog)
        self.Confirm_button.setGeometry(QtCore.QRect(280, 270, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Confirm_button.setFont(font)
        self.Confirm_button.setObjectName("Confirm_button")
        #connect submit button to class method which calls main function
        self.Confirm_button.clicked.connect(self.run_sort)
        self.label1 = QtWidgets.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(10, 20, 171, 31))
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(10, 100, 171, 31))
        self.label2.setObjectName("label2")
        self.destination_text_field_expand = QtWidgets.QToolButton(Dialog)
        self.destination_text_field_expand.setGeometry(QtCore.QRect(330, 140, 31, 22))
        self.destination_text_field_expand.setObjectName("destination_text_field_expand")
        self.destination_text_field_expand.clicked.connect(self.browsefiles)
        self.source_text_field_expand = QtWidgets.QToolButton(Dialog)
        self.source_text_field_expand.setGeometry(QtCore.QRect(330, 60, 31, 22))
        self.source_text_field_expand.setObjectName("source_text_field_expand")
        self.source_text_field_expand.clicked.connect(self.browsefiles)
        self.sort_order_1 = QtWidgets.QPushButton(Dialog)
        self.sort_order_1.setGeometry(QtCore.QRect(20, 220, 91, 31))
        self.sort_order_1.setObjectName("sort_order_1")
        #connect sort button to change sort method
        self.sort_order_1.clicked.connect(self.change_sort)
        self.sort_order_2 = QtWidgets.QPushButton(Dialog)
        self.sort_order_2.setGeometry(QtCore.QRect(140, 220, 91, 31))
        self.sort_order_2.setObjectName("sort_order_2")
        #connect sort button to change sort method
        self.sort_order_2.clicked.connect(self.change_sort)
        self.sort_order_3 = QtWidgets.QPushButton(Dialog)
        self.sort_order_3.setGeometry(QtCore.QRect(260, 220, 91, 31))
        self.sort_order_3.setObjectName("sort_order_3")
        #connect sort button to change sort method
        self.sort_order_3.clicked.connect(self.change_sort)
        self.label2_2 = QtWidgets.QLabel(Dialog)
        self.label2_2.setGeometry(QtCore.QRect(10, 180, 171, 31))
        self.label2_2.setObjectName("label2_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.source_text_field, self.source_text_field_expand)
        Dialog.setTabOrder(self.source_text_field_expand, self.destination_text_field)
        Dialog.setTabOrder(self.destination_text_field, self.destination_text_field_expand)
        Dialog.setTabOrder(self.destination_text_field_expand, self.sort_order_1)
        Dialog.setTabOrder(self.sort_order_1, self.sort_order_2)
        Dialog.setTabOrder(self.sort_order_2, self.sort_order_3)
        Dialog.setTabOrder(self.sort_order_3, self.Confirm_button)
    #open Windows filebrowser
    def browsefiles(self):
        filepath = QFileDialog.getExistingDirectory(self, "Open File", f"C:\\Users\\{USER}\\Desktop")
        btn = self.sender()
        if btn.objectName() == "source_text_field_expand":
            self.source_text_field.setText(filepath)
        elif btn.objectName() == "destination_text_field_expand":
            self.destination_text_field.setText(filepath)
        else:
            print("program go brrrr")
    #call main function
    def run_sort(self):
        folder_recursive_check(self.source_text_field.text(), 
        self.destination_text_field.text(),
        OPTIONS_TO_DATA[SORT_OPTIONS[SORT_BUTTONS["sort_order_1"]]], 
        OPTIONS_TO_DATA[SORT_OPTIONS[SORT_BUTTONS["sort_order_2"]]], 
        OPTIONS_TO_DATA[SORT_OPTIONS[SORT_BUTTONS["sort_order_3"]]] )
    #sorting format is changed on-click; this is for all 3 buttons
    def change_sort(self):
        btn = self.sender()
        btn_name = btn.objectName()
        btn_text = btn.text()
        print(btn_name+ " " + btn_text)
        if SORT_BUTTONS[btn_name] <= 4:
            print("up by 1")
            btn.setText(SORT_OPTIONS[SORT_BUTTONS[btn_name] + 1])
            SORT_BUTTONS[btn_name] += 1
            print(OPTIONS_TO_DATA[SORT_OPTIONS[SORT_BUTTONS[btn_name]]])
        else:
            print("back to 1")
            SORT_BUTTONS[btn_name] = 1
            btn.setText(SORT_OPTIONS[SORT_BUTTONS[btn_name]])
            print(OPTIONS_TO_DATA[SORT_OPTIONS[SORT_BUTTONS[btn_name]]])


    #idk
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "File Sorter"))
        self.Confirm_button.setText(_translate("Dialog", "Sort"))
        self.label1.setText(_translate("Dialog", "Choose folder to be sorted"))
        self.label2.setText(_translate("Dialog", "Choose destination folder"))
        self.destination_text_field_expand.setText(_translate("Dialog", "..."))
        self.source_text_field_expand.setText(_translate("Dialog", "..."))
        self.sort_order_1.setText(_translate("Dialog", "Year"))
        self.sort_order_2.setText(_translate("Dialog", "None"))
        self.sort_order_3.setText(_translate("Dialog", "None"))
        self.label2_2.setText(_translate("Dialog", "Sort order"))

#run program
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
