# -*- coding: utf-8 -*-
# revisão 26/08/2026

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
from PyQt5 import uic
from seabreeze.spectrometers import Spectrometer
import numpy as np
import time
import keyboard

class OceanOptics(qtw.QWidget):
    '''
       Update:
          - dark counts correction
          - intensity artifact correction
          - set default int. time of 10 ms
          - added graph config in graph_start_up
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi('ocean_optics_interface.ui', self)

        #self.spec = Spectrometer.from_first_available()
        #self.device = str(self.spec)
        #self.n = 25 if "USB2000PLUS" in self.device else 4

        self.graph_start_up()
        self.intTime_lineEdit.setText("10")
                
        self.measure_pushButton.clicked.connect(self.measure)
        self.freeRun_pushButton.clicked.connect(self.freerun)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.close)

    def graph_start_up(self):
        self.clear()
        
        x = []
        y = []
        
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "Intensity", units="a.u.")
        self.graphicsView.setLabel("bottom", "Wavelength", units="nm")
        
    def clear(self):
        self.graphicsView.clear()

    def freerun(self):
        time.sleep(0.2)
        inttime = int(self.intTime_lineEdit.text()) * 1000
        self.spec.integration_time_micros(inttime)        
        while True:
           if keyboard.is_pressed('Escape'):
               break
           
           x = self.spec.wavelengths()
           y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
            
           self.graphicsView.plot(x[self.n:], y[self.n:], clear=True)
           pg.QtWidgets.QApplication.processEvents()

    def spectrum(self):
        inttime = int(self.intTime_lineEdit.text()) * 1000        
        self.spec.integration_time_micros(inttime)     

        x = self.spec.wavelengths()
        y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False) 

        self.graphicsView.plot(x[self.n:], y[self.n:], clear=False)
        return x[self.n:], y[self.n:]
        
    def measure(self):
        self.spect = self.spectrum()

    def save(self):
        data = np.array(self.spect).T
        file = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file, data)

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = OceanOptics()
    tela.show()
    app.exec_()