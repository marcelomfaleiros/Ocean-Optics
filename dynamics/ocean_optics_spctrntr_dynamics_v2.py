# -*- coding: utf-8 -*-
# revisão 22/09/2023

import sys
from ocean_optics_intrfc_dynamics import Ui_Form
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
from seabreeze.spectrometers import Spectrometer
import numpy as np
import time
import keyboard

class Measurement(qtw.QWidget, Ui_Form):
    '''
       Updates:
          - dark counts correction
          - intensity artifact correction
          - set default int. time of 10 ms
          - added graph config in graph_start_up
          - optimization in t_array generation
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("Ocean Optics")
        self.setupUi(self)

        self.spectrometer_start_up()
        self.graph_start_up()

        self.intTime_lineEdit.setText("10")
        self.num_spectra_lineEdit.setText("5")
        self.time_step_lineEdit.setText("1")
        
        self.measure_pushButton.clicked.connect(self.measure)
        self.freeRun_pushButton.clicked.connect(self.freerun)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)

    def spectrometer_start_up(self):        
        self.spec = Spectrometer.from_first_available()
        self.device = str(self.spec)

    def graph_start_up(self):
        self.clear()
        
        x = []
        y = []
        
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "Intensity", units="a.u.")
        self.graphicsView.setLabel("bottom", "Wavelength", units="nm")
        
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
           x = self.spec.wavelengths()
           y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
           rounded_x = np.round(x, decimals = 2)
           rounded_y = np.round(y, decimals = 2)
           x = np.delete(rounded_x, [i for i in range(4)])  
           y = np.delete(rounded_y, [i for i in range(4)])           
           self.graphicsView.plot(x, y, clear=True)
           pg.QtWidgets.QApplication.processEvents()

    def spectrum(self):
        inttime = int(self.intTime_lineEdit.text()) * 1000        
        self.spec.integration_time_micros(inttime)        
        x = self.spec.wavelengths()
        rounded_x = np.round(x, decimals = 2)
        y = self.spec.intensities(correct_dark_counts = True, correct_nonlinearity = False)
        rounded_y = np.round(y, decimals = 2)        
        self.graphicsView.plot(x, y, pen =(0, 114, 189), symbolPen ='w', symbol='o',
                               symbolSize=2, clear=False)
        return x, y
        
    def measure(self):
        n_spectra = int(self.num_spectra_lineEdit.text())
        tstep = float(self.time_step_lineEdit.text())
        t_total = n_spectra * tstep        
        t_array = [round(i * tstep, 2) for i in range(n_spectra + 1)]
        t_array = np.array(t_array)
        self.t_string = np.array2string(t_array, precision=2, separator=' ', suppress_small=True)
        
        for i in t_array:
            if keyboard.is_pressed('Escape'):
                break             
            spec = self.spectrum()
            self.graphicsView.plot(spec[0], spec[1], clear=False)
            if i == 0:
                self.spec_array = (spec)
            else:
                self.spec_array = np.vstack((self.spec_array, spec[1]))                
                        
            pg.QtWidgets.QApplication.processEvents()

            time.sleep(tstep)
          
    def save(self):         
        self.spec_array = self.spec_array.transpose()
        file_spec = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file_spec, self.spec_array, fmt='%1.2f', header=self.t_string[1:-1], comments='#sec ')

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = Measurement()
    tela.show()
    app.exec_()


        
