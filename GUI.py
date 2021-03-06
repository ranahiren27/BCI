# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 09:47:47 2016
@name: GUI.py
@description: Graphic user interface of BCI system
@author: superVPi
"""

# Import module
import initialization as init
import datasets_2 as dat2
import ANN as ann

# Import libraries
import sys # To ensure application will nice, clean, close when exiting
#import os
import threading
import time
import serial
import numpy as np
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt

''' GUI variables '''

class Window(QtGui.QMainWindow):
    # Create variables to emit signal and display on progress bar
    value_progbar_1 = QtCore.pyqtSignal(int)
    value_progbar_2 = QtCore.pyqtSignal(int)
    value_progbar_3 = QtCore.pyqtSignal(int)
    value_progbar_4 = QtCore.pyqtSignal(int)
    value_progbar_5 = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super(Window, self).__init__()
        ''' Initialize basic feature '''
        self.setGeometry(100, 100, 1150, 500) # Initialize dimension for GUI
        self.setWindowTitle("Brain - Computer Interface v.1.0") # Set title for GUI
        self.setWindowIcon(QtGui.QIcon('taegaryen.ico')) # Set icon
        
        ''' Make tab '''
        self.tabs = QtGui.QTabWidget(self)        
        self.tabs.resize(1150, 480)
        
        # flag for connection
        self.flag_connection = 0
        
        # sensitive variables
        self.slider_up = 0
        self.slider_right = 0
        self.slider_down = 0
        self.slider_left = 0
        
        # serial variables
        self.serial_port = ''
        self.serial_baudrate = ''
        self.ser = serial.Serial()
        
        self.home()
    
    def home(self):        
        ''' Configure tab '''
        tab_train = QtGui.QWidget(self)
        tab_user = QtGui.QWidget(self)
        
        ''' ------------------------------------------------------------------
                                    Design tab Train
        ------------------------------------------------------------------ '''
        # Frame option
        frame_t1 = QtGui.QFrame(tab_train)
        frame_t1.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_t1.move(5, 65)
        frame_t1.resize(600, 300)  
        # Label option
        label_t = QtGui.QLabel('Record Signals', tab_train)
        label_t.setGeometry(190, 0, 300, 60)
        label_t.setFont(QtGui.QFont('Times', 30))
        
        # Label for record signals
        label_t1 = QtGui.QLabel('Neutral', tab_train)
        label_t1.setGeometry(20, 90, 80, 50)
        label_t1.setFont(QtGui.QFont('Times', 15))
        
        label_t2 = QtGui.QLabel('Up', tab_train)
        label_t2.setGeometry(20, 140, 80, 50)
        label_t2.setFont(QtGui.QFont('Times', 15))
        
        label_t3 = QtGui.QLabel('Right', tab_train)
        label_t3.setGeometry(20, 190, 80, 50)
        label_t3.setFont(QtGui.QFont('Times', 15))
        
        label_t4 = QtGui.QLabel('Down', tab_train)
        label_t4.setGeometry(20, 240, 80, 50)
        label_t4.setFont(QtGui.QFont('Times', 15))
        
        label_t5 = QtGui.QLabel('Left', tab_train)
        label_t5.setGeometry(20, 290, 80, 50)
        label_t5.setFont(QtGui.QFont('Times', 15))
        
        # Progress bar
        self.progress_t1 = QtGui.QProgressBar(tab_train)
        self.progress_t1.setGeometry(120, 100, 400, 30)
        self.value_progbar_1.connect(self.progress_t1.setValue) # Emit progress and display on progress bar
        
        self.progress_t2 = QtGui.QProgressBar(tab_train)
        self.progress_t2.setGeometry(120, 150, 400, 30)
        self.value_progbar_2.connect(self.progress_t2.setValue)
        
        self.progress_t3 = QtGui.QProgressBar(tab_train)
        self.progress_t3.setGeometry(120, 200, 400, 30)
        self.value_progbar_3.connect(self.progress_t3.setValue)
        
        self.progress_t4 = QtGui.QProgressBar(tab_train)
        self.progress_t4.setGeometry(120, 250, 400, 30)
        self.value_progbar_4.connect(self.progress_t4.setValue)
        
        self.progress_t5 = QtGui.QProgressBar(tab_train)
        self.progress_t5.setGeometry(120, 300, 400, 30)
        self.value_progbar_5.connect(self.progress_t5.setValue)
        
        # Record button
        btn_t1 = QtGui.QPushButton('Record', tab_train)
        btn_t1.setGeometry(530, 100, 60, 30)
                
        btn_t2 = QtGui.QPushButton('Record', tab_train)
        btn_t2.setGeometry(530, 150, 60, 30)
                
        btn_t3 = QtGui.QPushButton('Record', tab_train)
        btn_t3.setGeometry(530, 200, 60, 30)
                
        btn_t4 = QtGui.QPushButton('Record', tab_train)
        btn_t4.setGeometry(530, 250, 60, 30)
                
        btn_t5 = QtGui.QPushButton('Record', tab_train)
        btn_t5.setGeometry(530, 300, 60, 30)
                
        btn_t1.clicked.connect(self.record_t1)
        btn_t2.clicked.connect(self.record_t2)
        btn_t3.clicked.connect(self.record_t3)
        btn_t4.clicked.connect(self.record_t4)
        btn_t5.clicked.connect(self.record_t5)
        
        # Train button
        btn_t = QtGui.QPushButton('Train', tab_train)
        btn_t.setGeometry(400, 390, 100, 50)
        btn_t.clicked.connect(self.training_ANN)
        
        # Reset button
        btn_trs = QtGui.QPushButton('Reset', tab_train)
        btn_trs.setGeometry(100, 390, 100, 50)
        btn_trs.clicked.connect(self.reset_button)
        
        ''' Arrow image patterns '''
        # Frame arrow
        frame_t2 = QtGui.QFrame(tab_train)
        frame_t2.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_t2.move(650, 15)
        frame_t2.resize(470, 410)
        
        ''' Up arrow '''                
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_train)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(835, 0, 130, 200)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/up_0_5Hz.gif", QtCore.QByteArray(), tab_train) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Right arrow '''
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_train)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(960, 155, 200, 130)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/right_0_5Hz.gif", QtCore.QByteArray(), tab_train) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Down arrow '''
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_train)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(835, 240, 130, 200)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/down_0_5Hz.gif", QtCore.QByteArray(), tab_train) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Left arrow '''
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_train)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(660, 155, 200, 130)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/left_0_5Hz.gif", QtCore.QByteArray(), tab_train) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
                
        ''' ------------------------------------------------------------------
                                    Design tab User 
        ------------------------------------------------------------------ '''
        ''' Arrow image patterns '''
        
        # Frame arrow
        frame_u1 = QtGui.QFrame(tab_user)
        frame_u1.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_u1.move(50, 15)
        frame_u1.resize(470, 410)         
        
        ''' Up arrow '''                
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_user)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(235, 0, 130, 200)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/up_0_5Hz.gif", QtCore.QByteArray(), tab_user) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Right arrow '''
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_user)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(360, 155, 200, 130)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/right_0_5Hz.gif", QtCore.QByteArray(), tab_user) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Down arrow '''
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_user)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(235, 240, 130, 200)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/down_0_5Hz.gif", QtCore.QByteArray(), tab_user) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Left arrow '''
        # set up the movie screen on a label
        self.movie_screen = QtGui.QLabel(tab_user)
        # expand and center the label 
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)    
        #self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(60, 155, 200, 130)
                
         # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QtGui.QMovie("stimulus/left_0_5Hz.gif", QtCore.QByteArray(), tab_user) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.scaledSize()
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
        ''' Slider to change sensitiveness '''
        # Frame for sensitive slider
        frame_u2 = QtGui.QFrame(tab_user)
        frame_u2.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_u2.move(600, 210)
        frame_u2.resize(500, 215)        
        
        # Up
        self.slider_u1 = QtGui.QSlider(QtCore.Qt.Horizontal, tab_user)
        self.slider_u1.setGeometry(680, 230, 400, 30)
        self.slider_u1.setRange(0, 10)
        self.slider_u1.setSliderPosition(5)
        
        # Right
        self.slider_u2 = QtGui.QSlider(QtCore.Qt.Horizontal, tab_user)
        self.slider_u2.setGeometry(680, 280, 400, 30)
        self.slider_u2.setRange(0, 10)
        self.slider_u2.setSliderPosition(5)
        
        # Down
        self.slider_u3 = QtGui.QSlider(QtCore.Qt.Horizontal, tab_user)
        self.slider_u3.setGeometry(680, 330, 400, 30)
        self.slider_u3.setRange(0, 10)
        self.slider_u3.setSliderPosition(5)
        
        # Left
        self.slider_u4 = QtGui.QSlider(QtCore.Qt.Horizontal, tab_user)
        self.slider_u4.setGeometry(680, 380, 400, 30)
        self.slider_u4.setRange(0, 10)
        self.slider_u4.setSliderPosition(5)
        
        # Function get slider value
        self.slider_u1.valueChanged.connect(self.slider_up_change_value)
        self.slider_u2.valueChanged.connect(self.slider_right_change_value)
        self.slider_u3.valueChanged.connect(self.slider_down_change_value)
        self.slider_u4.valueChanged.connect(self.slider_left_change_value)
        
        # Label for sensitive slider
        label_sens_u = QtGui.QLabel('Sensitive Adjustment', tab_user)
        label_sens_u.setGeometry(600, 150, 400, 60)
        label_sens_u.setFont(QtGui.QFont('Times', 30))     
        
        label_u1 = QtGui.QLabel('Up', tab_user)
        label_u1.setGeometry(620, 230, 200, 30)
        label_u1.setFont(QtGui.QFont('Times', 15))
        
        label_u2 = QtGui.QLabel('Right', tab_user)
        label_u2.setGeometry(620, 280, 200, 30)
        label_u2.setFont(QtGui.QFont('Times', 15))
        
        label_u3 = QtGui.QLabel('Down', tab_user)
        label_u3.setGeometry(620, 330, 200, 30)
        label_u3.setFont(QtGui.QFont('Times', 15))
        
        label_u4 = QtGui.QLabel('Left', tab_user)
        label_u4.setGeometry(620, 380, 200, 30)
        label_u4.setFont(QtGui.QFont('Times', 15))
        
        ''' Serial interface '''
        # Label for serial interface
        label_ser_u = QtGui.QLabel('Serial Configuration', tab_user)
        label_ser_u.setGeometry(600, 0, 400, 60)
        label_ser_u.setFont(QtGui.QFont('Times', 30))  
        
        # Frame for serial interface
        frame_u3 = QtGui.QFrame(tab_user)
        frame_u3.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_u3.move(600, 60)
        frame_u3.resize(500, 90)
        
        # Label for serial configuration
        label_u5 = QtGui.QLabel('COM Port', tab_user)
        label_u5.setGeometry(620, 70, 200, 30)
        label_u5.setFont(QtGui.QFont('Times', 15))
        
        label_u6 = QtGui.QLabel('Baud rate', tab_user)
        label_u6.setGeometry(860, 70, 200, 30)
        label_u6.setFont(QtGui.QFont('Times', 15))
        
        # Combo box for serial configuration
        # COM port combobox
        self.combo_u1 = QtGui.QComboBox(tab_user)
        self.combo_u1.setGeometry(720, 70, 120, 30)
        self.combo_u1.addItem('COM24')
        self.combo_u1.addItem('COM25')
        self.combo_u1.addItem('COM6')
        self.combo_u1.addItem('COM11')
        self.combo_u1.addItem('COM3')
        self.combo_u1.addItem('COM31')
        
        # Baud rate combobox
        self.combo_u2 = QtGui.QComboBox(tab_user)
        self.combo_u2.setGeometry(950, 70, 120, 30)
        self.combo_u2.addItem('9600')
        self.combo_u2.addItem('19200')
        self.combo_u2.addItem('38400')
        self.combo_u2.addItem('57600')
        self.combo_u2.addItem('115200')
        
        # Get string from combo box
        self.combo_u1.activated[str].connect(self.change_port)
        self.combo_u2.activated[str].connect(self.change_baudrate)
        
        # Button connect
        self.btn_u1 = QtGui.QPushButton('Connect', tab_user)
        self.btn_u1.setGeometry(620, 110, 120, 30)
        self.btn_u1.clicked.connect(self.connect_button)
        
        ''' Add tabs to tabs object '''
        self.tabs.addTab(tab_train, "Train")
        self.tabs.addTab(tab_user, "User")
    
        self.show()
    
    ''' Record function '''
    ''' COLLECT NEUTRAL SIGNALS '''
    def record_t1(self):
        print 'COLLECTING NEUTRAL SIGNALS'
        thread_record_1 = threading.Thread(target=self.record_train_1)
        thread_record_1.start()
        thread_display_1 = threading.Thread(target=self.display_progbar_1)
        thread_display_1.start()
    
    # Thread collect data of NEUTRAL signals    
    def record_train_1(self):
        init.input_temp, init.output_temp = dat2.feature_extraction(5)
        init.input_temp = np.array(init.input_temp, dtype = float)
        init.output_temp = np.array(init.output_temp, dtype = float)
        
        if init.INPUT_DATASETs.shape[0] is not 0:
            init.INPUT_DATASETs = np.concatenate((init.INPUT_DATASETs, init.input_temp), axis = 0)
            init.OUTPUT_DATASETs = np.concatenate((init.OUTPUT_DATASETs, init.output_temp), axis = 0)
        else:
            init.INPUT_DATASETs = init.input_temp
            init.OUTPUT_DATASETs = init.output_temp
        
        print init.INPUT_DATASETs.shape
        print init.INPUT_DATASETs
        print
        print init.OUTPUT_DATASETs.shape
        print init.OUTPUT_DATASETs
        print
        
    # Display progress on progress bar
    def display_progbar_1(self):
        completed = 0
        
        while completed < 100:
            completed += 1
            self.value_progbar_1.emit(completed)
            time.sleep(0.1)        
        
    ''' COLLECT UP SIGNALS '''
    def record_t2(self):
        print 'COLLECTING UP SIGNALS'
        thread_record_2 = threading.Thread(target=self.record_train_2)
        thread_record_2.start()
        thread_display_2 = threading.Thread(target=self.display_progbar_2)
        thread_display_2.start()
    
    # Thread collect data of UP signals    
    def record_train_2(self):
        init.input_temp, init.output_temp = dat2.feature_extraction(1)
        init.input_temp = np.array(init.input_temp, dtype = float)
        init.output_temp = np.array(init.output_temp, dtype = float)
        
        if init.INPUT_DATASETs.shape[0] is not 0:
            init.INPUT_DATASETs = np.concatenate((init.INPUT_DATASETs, init.input_temp), axis = 0)
            init.OUTPUT_DATASETs = np.concatenate((init.OUTPUT_DATASETs, init.output_temp), axis = 0)
        else:
            init.INPUT_DATASETs = init.input_temp
            init.OUTPUT_DATASETs = init.output_temp
        
        print init.INPUT_DATASETs.shape
        print init.INPUT_DATASETs
        print
        print init.OUTPUT_DATASETs.shape
        print init.OUTPUT_DATASETs
        print
        
    # Display progress on progress bar
    def display_progbar_2(self):
        completed = 0
        
        while completed < 100:
            completed += 1
            self.value_progbar_2.emit(completed)
            time.sleep(0.1)
    
    ''' COLLECT RIGHT SIGNALS '''            
    def record_t3(self):
        print 'COLLECTING RIGHT SIGNALS'
        thread_record_3 = threading.Thread(target=self.record_train_3)
        thread_record_3.start()
        thread_display_3 = threading.Thread(target=self.display_progbar_3)
        thread_display_3.start()
    
    # Thread collect data of UP signals    
    def record_train_3(self):
        init.input_temp, init.output_temp = dat2.feature_extraction(2)
        init.input_temp = np.array(init.input_temp, dtype = float)
        init.output_temp = np.array(init.output_temp, dtype = float)
        
        if init.INPUT_DATASETs.shape[0] is not 0:
            init.INPUT_DATASETs = np.concatenate((init.INPUT_DATASETs, init.input_temp), axis = 0)
            init.OUTPUT_DATASETs = np.concatenate((init.OUTPUT_DATASETs, init.output_temp), axis = 0)
        else:
            init.INPUT_DATASETs = init.input_temp
            init.OUTPUT_DATASETs = init.output_temp
        
        print init.INPUT_DATASETs.shape
        print init.INPUT_DATASETs
        print
        print init.OUTPUT_DATASETs.shape
        print init.OUTPUT_DATASETs
        print
        
    # Display progress on progress bar
    def display_progbar_3(self):
        completed = 0
        
        while completed < 100:
            completed += 1
            self.value_progbar_3.emit(completed)
            time.sleep(0.1)
            
    ''' COLLECT DOWN SIGNALS '''
    def record_t4(self):
        print 'COLLECTING DOWN SIGNALS'
        thread_record_4 = threading.Thread(target=self.record_train_4)
        thread_record_4.start()
        thread_display_4 = threading.Thread(target=self.display_progbar_4)
        thread_display_4.start()
    
    # Thread collect data of UP signals    
    def record_train_4(self):
        init.input_temp, init.output_temp = dat2.feature_extraction(3)
        init.input_temp = np.array(init.input_temp, dtype = float)
        init.output_temp = np.array(init.output_temp, dtype = float)
        
        if init.INPUT_DATASETs.shape[0] is not 0:
            init.INPUT_DATASETs = np.concatenate((init.INPUT_DATASETs, init.input_temp), axis = 0)
            init.OUTPUT_DATASETs = np.concatenate((init.OUTPUT_DATASETs, init.output_temp), axis = 0)
        else:
            init.INPUT_DATASETs = init.input_temp
            init.OUTPUT_DATASETs = init.output_temp
        
        print init.INPUT_DATASETs.shape
        print init.INPUT_DATASETs
        print
        print init.OUTPUT_DATASETs.shape
        print init.OUTPUT_DATASETs
        print
        
    # Display progress on progress bar
    def display_progbar_4(self):
        completed = 0
        
        while completed < 100:
            completed += 1
            self.value_progbar_4.emit(completed)
            time.sleep(0.1)
    
    ''' COLLECT LEFT SIGNALS '''
    def record_t5(self):
        print 'COLLECTING LEFT SIGNALS'
        thread_record_5 = threading.Thread(target=self.record_train_5)
        thread_record_5.start()
        thread_display_5 = threading.Thread(target=self.display_progbar_5)
        thread_display_5.start()
    
    # Thread collect data of UP signals    
    def record_train_5(self):
        init.input_temp, init.output_temp = dat2.feature_extraction(4)
        init.input_temp = np.array(init.input_temp, dtype = float)
        init.output_temp = np.array(init.output_temp, dtype = float)
        
        if init.INPUT_DATASETs.shape[0] is not 0:
            init.INPUT_DATASETs = np.concatenate((init.INPUT_DATASETs, init.input_temp), axis = 0)
            init.OUTPUT_DATASETs = np.concatenate((init.OUTPUT_DATASETs, init.output_temp), axis = 0)
        else:
            init.INPUT_DATASETs = init.input_temp
            init.OUTPUT_DATASETs = init.output_temp
        
        print init.INPUT_DATASETs.shape
        print init.INPUT_DATASETs
        print
        print init.OUTPUT_DATASETs.shape
        print init.OUTPUT_DATASETs
        print
        
    # Display progress on progress bar
    def display_progbar_5(self):
        completed = 0
        
        while completed < 100:
            completed += 1
            self.value_progbar_5.emit(completed)
            time.sleep(0.1)
    
    ''' TRAINING ANN '''
    def training_ANN(self):
        # Normalize because collective signals have E so high
        init.INPUT_DATASETs = np.divide(init.INPUT_DATASETs, 500)
        
        self.NN = ann.Neural_Network(Lambda = 0.0001)
        self.T = ann.trainer(self.NN)
        self.T.train(init.INPUT_DATASETs, init.OUTPUT_DATASETs)
        
        ''' Draw training data, relation between T and error E '''
        plt.figure(1)
        plt.plot(self.T.E, label = 'Train line', linewidth = 2.0)
        plt.legend()
        
        plt.grid(1)
        plt.xlabel('Epochs')
        plt.ylabel('Cost')
        plt.show()
    
    ''' RESET BUTTON '''
    def reset_button(self):
        init.INPUT_DATASETs = np.array([], dtype = float)
        print init.INPUT_DATASETs
        print
        self.progress_t1.setValue(0)
        self.progress_t2.setValue(0)
        self.progress_t3.setValue(0)
        self.progress_t4.setValue(0)
        self.progress_t5.setValue(0)
    
    ''' CONNECT BUTTON '''
    def connect_button(self):
        # Switch state of connect button
        if self.flag_connection == 0:
            self.flag_connection = 1
            self.btn_u1.setText('Disconnect')
        elif self.flag_connection == 1:
            self.flag_connection = 0
            self.btn_u1.setText('Connect')
        
        # Check connection
        if self.flag_connection==1:
            print
            print 'WE ARE CONNECTING'
            print
            self.ser = serial.Serial(self.serial_port, self.serial_baudrate)
            print 
            print self.ser.isOpen()
            print
            thread_acquire_online = threading.Thread(target=self.acquire_online)
            thread_acquire_online.start()
            thread_extract_online = threading.Thread(target=self.extract_online)
            thread_extract_online.start()
        elif self.flag_connection==0:
            print
            print 'WE WERE DISCONNECT'
            print
            time.sleep(0.5)
            self.ser.close()
            print
            print self.ser.isOpen()
            print
    
    # Acquire online signal
    def acquire_online(self):
        while self.flag_connection==1:
            init.ACQ_SIGNAL = dat2.online_signal(init.ACQ_SIGNAL)
            print 'Length of init.ACQ_SIGNAL is: ' + str(len(init.ACQ_SIGNAL))
            print
            time.sleep(1)
    
    # Extract online signal
    def extract_online(self):
        feedforward = np.array([], dtype = float)
        feedforward2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        init.WINDOW_SIGNAL = []
        init.BUFFER_FEATURES = []
        
        while self.flag_connection==1:
            if len(init.ACQ_SIGNAL)==256:
                init.WINDOW_SIGNAL = init.ACQ_SIGNAL
                init.BUFFER_FEATURES = dat2.online_features_extraction(init.WINDOW_SIGNAL)
                
                # Normalize input
                init.BUFFER_FEATURES = np.divide(init.BUFFER_FEATURES, 500)
                
                # Apply to ANN classification
                feedforward = self.NN.foward(init.BUFFER_FEATURES)
                
                print
                print 'FEED FORWARD BEFORE ADJUSTING SENSITIVE'
                print feedforward
                print
                '''
                feedforward2[0] = feedforward[0] + self.slider_up
                feedforward2[1] = feedforward[1] + self.slider_right
                feedforward2[2] = feedforward[2] + self.slider_down
                feedforward2[3] = feedforward[3] + self.slider_left
                feedforward2[4] = feedforward[4]
                '''
                print
                print 'FEED FORWARD AFTER ADJUSTING SENSITIVE'
                print feedforward2
                print
                
                # Check state
                if feedforward[0]==np.max(feedforward):
                    print
                    print 'ROBOT MOVE STRAINGHT'
                    print
                    self.ser.write('u')
                if feedforward[1]==np.max(feedforward):
                    print
                    print 'ROBOT TURN RIGHT'
                    print
                    self.ser.write('r')
                if feedforward[2]==np.max(feedforward):
                    print
                    print 'ROBOT MOVE BACK'
                    print
                    self.ser.write('d')
                if feedforward[3]==np.max(feedforward):
                    print
                    print 'ROBOT TURN LEFT' 
                    print
                    self.ser.write('l')
                if feedforward[4]==np.max(feedforward):
                    print
                    print 'ROBOT RELAX'
                    print
                    self.ser.write('n')
                time.sleep(0.25)
            else:
                pass
    
    ''' Sensitive function '''
    # Slider up
    def slider_up_change_value(self):
        self.slider_up = self.slider_u1.value()/50.0 - 0.1
        print self.slider_up
    
    # Slider right
    def slider_right_change_value(self):
        self.slider_right = self.slider_u2.value()/50.0 - 0.1
        print self.slider_right
    
    # Slider down
    def slider_down_change_value(self):
        self.slider_down = self.slider_u3.value()/50.0 - 0.1
        print self.slider_down
    
    # Slider left
    def slider_left_change_value(self):
        self.slider_left = self.slider_u4.value()/50.0 - 0.1
        print self.slider_left
    
    ''' Serial value '''
    def change_port(self, text):
        self.serial_port = str(text)
        print self.serial_port
    
    def change_baudrate(self, text):
        self.serial_baudrate = int(text)
        print self.serial_baudrate

#class ThreadWorker1()

def run():
    app = QtGui.QApplication(sys.argv)
    # mac, plastique, sgi, windows
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('mac'))
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

run()
