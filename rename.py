#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, math
from datetime import datetime
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QString, Qt

class AppWindow(QtGui.QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.fileLst = []
        self.perc = 0
        self.ui = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),'mainwindow.ui'))
        self.ui.show()
    
    
        self.connect(self.ui.addBtn, QtCore.SIGNAL("clicked()"), self.addFiles)
        self.connect(self.ui.removeBtn, QtCore.SIGNAL("clicked()"), self.removeFiles)
        self.connect(self.ui.renameBtn, QtCore.SIGNAL("clicked()"), self.renameFiles)
        

    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(None, QString("Select file(s) to rename"), QString(os.path.expanduser("~")))
        filesToAdd = list(set(files)-set(self.fileLst))
        self.fileLst = list(set(files+self.fileLst))
        self.ui.fileList.addItems(filesToAdd)

    def removeFiles(self):
        selected = self.ui.fileList.selectedItems() 
        for sel in selected:
            indx = self.ui.fileList.indexFromItem(sel)
            self.fileLst.remove(self.ui.fileList.takeItem(indx.row()).text())#model.removeRow(indx.row())

    def renameFiles(self):
        "Add date and time (timestamp) info, to file's name"
        #files = os.listdir("./")
        numOfFiles = self.ui.fileList.count()
        for i in xrange(0, numOfFiles):
            qfl = self.ui.fileList.item(i)
            if not qfl: continue
            fl = unicode(qfl.text())
            fl0, fl1 = os.path.splitext(fl) 
            os.rename(fl, ("%s-%s%s")%(fl0, datetime.now().strftime('%d-%m-%Y_%H-%M-%S'), fl1))
            self.updateProgBar()
        self.ui.fileList.clear()
        self.fileLst = []
        self.perc = 0

        
    def updateProgBar(self):
        self.perc += float(100)/self.ui.fileList.count()
        self.ui.progressBar.setValue(self.perc)

        if(math.ceil(self.perc)==100): #Renaming finished successfully!
            msg = QString("Completed!")
            QtGui.QMessageBox.information(None, QString("Renaming Info"),QString(msg));
            self.ui.progressBar.setValue(0);

        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec_())
