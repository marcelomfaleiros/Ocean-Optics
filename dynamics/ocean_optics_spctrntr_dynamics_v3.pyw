# -*- coding: utf-8 -*-
# revisão 27/09/2023

import sys
from ocean_optics_intrfc_dynamics import Ui_Form
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
from seabreeze.spectrometers import Spectrometer
import numpy as np
from time import sleep
import keyboard

class Worker(QThread):
    signal = pyqtSignal(object)
    finished = pyqtSignal()
    
    def run(self, mode = str):
        self.spec.integration_time_micros(self.int_time) 
        t_array = [round(i * self.tstep, 2) for i in range(self.n_spectra + 1)]
        t_array = np.array(t_array)
        self.t_string = np.array2string(t_array, precision=2, separator=' ', suppress_small=True)
        
        for i in t_array:
            if keyboard.is_pressed('Escape'):
                break             
            x = self.spec.wavelengths()
            rounded_x = np.round(x, decimals = 2)
            y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
            self.data = (rounded_x, y)
            self.data = np.asarray(self.data, dtype=None, order=None)
            self.signal.emit(self.data)
            if i == 0:
                self.spec_array = (rounded_x, y)
            else:
                self.spec_array = np.vstack((self.spec_array, y))

            sleep(self.tstep)

        self.finished.emit()

class Measurement(qtw.QWidget, Ui_Form):
    '''
       Updates:
          - dark counts correction
          - intensity artifact correction
          - set default int. time of 10 ms
          - added graph config in graph_start_up
          - improving user experience with QThreads
    '''
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Ocean Optics")
        self.setupUi(self)

        self.thread = Worker()
        self.thread.spec = Spectrometer.from_first_available()

        self.graphStartUp()        

        self.intTime_lineEdit.setText("10")
        self.num_spectra_lineEdit.setText("5")
        self.time_step_lineEdit.setText("1")
        
        self.measure_pushButton.clicked.connect(self.measure)
        self.freeRun_pushButton.clicked.connect(self.freeRun)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)

    def graphStartUp(self):
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "Intensity", units="a.u.")
        self.graphicsView.setLabel("bottom", "Wavelength", units="nm")
        
    def clear(self):
        self.graphicsView.clear()
        
    def exit(self):
        self.close()

    def freeRun(self):
        self.thread.int_time = int(self.intTime_lineEdit.text()) * 1000
        self.thread.spec.integration_time_micros(self.thread.int_time) 
        while True:
            if keyboard.is_pressed('Escape'):
                break
            x = self.thread.spec.wavelengths()
            y = self.thread.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
            x = np.delete(x, [i for i in range(4)])  
            y = np.delete(y, [i for i in range(4)])
            self.graphicsView.plot(x, y, clear=True)
            pg.QtWidgets.QApplication.processEvents()

    def measure(self):      
        self.thread.int_time = int(self.intTime_lineEdit.text()) * 1000
        self.thread.n_spectra = int(self.num_spectra_lineEdit.text())
        self.thread.tstep = float(self.time_step_lineEdit.text())
        self.thread.signal.connect(self.plot)
        self.thread.start()

        self.measure_pushButton.setEnabled(False)
        self.freeRun_pushButton.setEnabled(False)
        self.save_pushButton.setEnabled(False)
        self.clear_pushButton.setEnabled(False)
        self.thread.finished.connect(lambda: self.measure_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.freeRun_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.save_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.clear_pushButton.setEnabled(True))
        

    def plot(self, data):
        self.graphicsView.plot(data[0], data[1], clear=False)
        pg.QtWidgets.QApplication.processEvents()

    def save(self):
        self.spec_array = self.thread.spec_array.transpose()
        file_spec = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file_spec, self.spec_array, header=self.thread.t_string[1:-1], comments='#sec ')   #, fmt='%1.2f'

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = Measurement()
    tela.show()
    app.exec_()


        
