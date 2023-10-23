# -*- coding: utf-8 -*-
# revisão 05/04/2023

import sys
from ocean_optics_interface import Ui_Form
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
from seabreeze.spectrometers import Spectrometer
import numpy as np
import time
import keyboard

class OceanOptics(qtw.QWidget, Ui_Form):
    '''
       Update:
          - dark counts correctio
          - intensity artifact correction
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("Ocean Optics")
        self.setupUi(self)

        self.start_up()
        
        self.measure_pushButton.clicked.connect(self.measure)
        self.freeRun_pushButton.clicked.connect(self.freerun)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)

    def start_up(self):        
        self.spec = Spectrometer.from_first_available()
        self.device = str(self.spec)
        
    def clear(self):
        self.graphicsView.clear()
        
    def exit(self):
        self.close()

    def freerun(self):
        time.sleep(0.2)
        inttime = int(self.intTime_lineEdit.text()) * 1000
        self.spec.integration_time_micros(inttime)        
        while True:
           if keyboard.is_pressed('Escape'):
               break
           raw_x = self.spec.wavelengths()
           raw_y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
           if "USB2000PLUS" in self.device:
               x = np.delete(raw_x, [i for i in range(25)])
               y = np.delete(raw_y, [i for i in range(25)])
           else:
               x = np.delete(raw_x, [i for i in range(4)])
               y = np.delete(raw_y, [i for i in range(4)])
           self.graphicsView.plot(x, y, clear=True)
           pg.QtWidgets.QApplication.processEvents()

    def spectrum(self):
        inttime = int(self.intTime_lineEdit.text()) * 1000        
        self.spec.integration_time_micros(inttime)        
        raw_x = self.spec.wavelengths()
        raw_y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
        if "USB2000PLUS" in self.device:
            x = np.delete(raw_x, [i for i in range(25)])
            y = np.delete(raw_y, [i for i in range(25)])
        else:
            x = np.delete(raw_x, [i for i in range(4)])
            y = np.delete(raw_y, [i for i in range(4)])      
        self.graphicsView.plot(x, y, clear=False)
        return x, y
        
    def measure(self):
        self.spect = self.spectrum()

    def save(self):
        raw_spec = np.vstack(self.spect)
        data = raw_spec.transpose()
        file = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file, data)

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = OceanOptics()
    tela.show()
    app.exec_()


        
