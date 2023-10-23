# -*- coding: utf-8 -*-
# revisão 01/09/2023

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
          - set default int. time of 10 ms
          - added graph config in graph_start_up
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("Ocean Optics")
        self.setupUi(self)

        self.spectrometer_start_up()
        self.graph_start_up()

        self.intTime_lineEdit.setText("10")

        self.measure_pushButton.clicked.connect(self.measure)
        self.freeRun_pushButton.clicked.connect(self.freerun)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)

    def graph_start_up(self):
        self.clear()
        
        x = []
        y = []
        
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "Intensity", units="a.u.")
        self.graphicsView.setLabel("bottom", "Wavelength", units="nm")

    def spectrometer_start_up(self):        
        self.spec = Spectrometer.from_first_available()  #from_first_available()
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
           rounded_x = np.round(raw_x, decimals = 2)
           raw_y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
           rounded_y = np.round(raw_y, decimals = 2)
           x = np.delete(rounded_x, [i for i in range(4)])  
           y = np.delete(rounded_y, [i for i in range(4)])
           self.graphicsView.plot(x, y, pen =(0, 114, 189), symbolPen ='w', symbol='o',
                                  symbolSize=2, clear=True) 
           pg.QtWidgets.QApplication.processEvents()

    def spectrum(self):
        inttime = int(self.intTime_lineEdit.text()) * 1000        
        self.spec.integration_time_micros(inttime)        
        raw_x = self.spec.wavelengths()
        rounded_x = np.round(raw_x, decimals = 2)
        raw_y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
        rounded_y = np.round(raw_y, decimals = 2)
        x = np.delete(rounded_x, [i for i in range(4)])  
        y = np.delete(rounded_y, [i for i in range(4)])
        self.graphicsView.plot(x, y, pen =(0, 114, 189), symbolPen ='w', symbol='o',
                               symbolSize=2, clear=False)
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


        
