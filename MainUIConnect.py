import sys
from PyQt6.QtWidgets import QApplication,QMainWindow,QHeaderView,QTableWidgetItem,QTableWidget,QLabel,QSizePolicy,QFileDialog
from PyQt6 import uic
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import os

from Computation import BackgroundComputation

class MainUIClass(QMainWindow):
    def __init__(self):
        super(MainUIClass,self).__init__()
        self.paramui =uic.loadUi(rf"{os.path.abspath('Addparamui.ui')}")
        self.exportui =uic.loadUi(rf"{os.path.abspath('ExportUi.ui')}")
        uic.loadUi(rf"{os.path.abspath('MainUI.ui')}",self)
        self.Inputtable.horizontalHeader().setStretchLastSection(True)
        self.Inputtable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stylesheet = "::section{Background-color:rgb(73, 79, 85);color:rgb(0,0,0);font-size:14px;font-weight:bold;border-radius:14px;}"
        self.Inputtable.horizontalHeader().setStyleSheet(stylesheet)
        self.comboBoxitem.currentIndexChanged.connect(self.Comboitem)
        self.pushButton.clicked.connect(self.compute)
        self.comp = BackgroundComputation()
        self.actionAdd.triggered.connect(self.openAddParamUI)
        self.actionExport.triggered.connect(self.export)
        self.actionImport.triggered.connect(self.Import)
        self.paramui.elevation.clicked.connect(self.elevationDetails)
        self.exportui.openpath.clicked.connect(self.openexportpath)
        self.exportui.okbtn.clicked.connect(self.okexport)
        self.table_widget = QTableWidget()
        self.outputpath = None
        self.show()



    def initial_table_results(self,row,column,header):
        self.change_Outputwidget()
        self.table_widget.setRowCount(row)
        self.table_widget.setColumnCount(column)
        self.table_widget.setHorizontalHeaderLabels(header)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stylesheet = "::section{Background-color:rgb(73, 79, 85);color:rgb(0,0,0);font-size:14px;font-weight:bold;border-radius:14px;}"
        self.table_widget.horizontalHeader().setStyleSheet(stylesheet)
        self.output_widget.addWidget(self.table_widget)


    def change_Outputwidget(self):
        for i in reversed(range(self.output_widget.count())):
            widget_item_to_remove = self.output_widget.itemAt(i).widget()
            self.output_widget.removeWidget(widget_item_to_remove)
            widget_item_to_remove.setParent(None)

    def Comboitem(self):
        current_comboitem = self.comboBoxitem.currentText()
        if current_comboitem == 'Initial Results':
            lines = self.comp.remarks
            change_in_height = self.comp.Change_in_height
            self.initial_table_results(len(lines)+1,2,["Lines","Change in Height"])
            inputdata = zip(lines,change_in_height)
            for i, row in enumerate(inputdata, start=1):
                try:
                    self.table_widget.setItem(i, 0, QTableWidgetItem(row[0]))
                    self.table_widget.setItem(i, 1, QTableWidgetItem(f'{row[1]}'))
                except Exception:
                    pass

        elif current_comboitem == 'Observation Matrix':
            row,column = self.comp.observation_matrix.shape
            self.retrievedata()
            matrix_headers = self.comp.tabledata
            del matrix_headers[0]
            del matrix_headers[-1]
            self.initial_table_results(row+1,column,[data[2] for data in matrix_headers])
            inputdata = self.comp.observation_matrix
            for i, row in enumerate(inputdata, start=1):
                for j,column in enumerate(row):
                    try:
                        self.table_widget.setItem(i,j , QTableWidgetItem(f'{column}'))
                    except Exception:
                        pass

        elif current_comboitem == 'Absolute Terms':
            row = len(self.comp.absolute_term)
            self.initial_table_results(row+1,1,["Absolute Term"])
            inputdata = self.comp.absolute_term
            for i, row in enumerate(inputdata, start=1):
                try:
                    self.table_widget.setItem(i, 0, QTableWidgetItem(f'{row}'))
                except Exception:
                    pass

        elif current_comboitem == 'Most Probable Heights':
            self.retrievedata()
            matrix_headers = self.comp.tabledata
            del matrix_headers[0]
            del matrix_headers[-1]
            point_names = [data[2] for data in matrix_headers]
            prov_height =self.comp.provisional_heights
            corrections = self.comp.unknown
            mpv = self.comp.most_probable_height
            self.initial_table_results(len(point_names)+1, 4, ["points","Provisional Height","Correction","Most Probable Height"])
            inputdata = zip(point_names,prov_height,corrections,mpv)
            for i, row in enumerate(inputdata, start=1):
                try:
                    self.table_widget.setItem(i, 0, QTableWidgetItem(row[0]))
                    self.table_widget.setItem(i, 1, QTableWidgetItem(f'{row[1]}'))
                    self.table_widget.setItem(i, 2, QTableWidgetItem(f'{row[2][0]}'))
                    self.table_widget.setItem(i, 3, QTableWidgetItem(f'{row[3][0]}'))
                except Exception:
                    pass
        elif current_comboitem == 'Residuals':
            row,columns = self.comp.residual.shape
            self.initial_table_results(row+1, columns,["Residuals"])
            inputdata = self.comp.residual
            for i, row in enumerate(inputdata, start=1):
                try:
                    self.table_widget.setItem(i, 0, QTableWidgetItem(f'{row[0]}'))
                except Exception:
                    pass
        elif current_comboitem == 'Units Variance':
            variance = self.comp.unitvariance
            self.setoutputLabel(f'{variance}')
        elif current_comboitem == '99% Confidence Level':
            confidence_level = self.comp.perc_confidence_level
            self.setoutputLabel(f'{confidence_level}')
        elif current_comboitem == 'Final Accuracy Assessment':
            final_output = self.comp.final_output
            self.initial_table_results(len(list(final_output))+1, 6,["Lines", "Residual", "Qxixj", "Residual Mean","95% Confidence Level", "Accepted/Rejected"])
            inputdata = final_output
            for i, row in enumerate(inputdata, start=1):
                try:
                    self.table_widget.setItem(i, 0, QTableWidgetItem(f'{row[0]}'))
                    self.table_widget.setItem(i, 1, QTableWidgetItem(f'{row[1]}'))
                    self.table_widget.setItem(i, 2, QTableWidgetItem(f'{row[2]}'))
                    self.table_widget.setItem(i, 3, QTableWidgetItem(f'{row[3]}'))
                    self.table_widget.setItem(i, 4, QTableWidgetItem(f'{row[4]}'))
                    self.table_widget.setItem(i, 5, QTableWidgetItem(f'{row[5]}'))
                except Exception:
                    pass
        else:
            self.setoutputLabel("OUTPUT DATA APPEARS HERE")
    def setoutputLabel(self,text):
        self.change_Outputwidget()
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        label.setFont(QFont('Arial', 14))
        label.setStyleSheet("font-weight:bold")
        self.output_widget.addWidget(label)


    def retrievedata(self):
        backsight,foresight,remarks,IB = [],[],[],[]
        cellrow = self.Inputtable.rowCount()
        for row in range(1,cellrow):
            try:
                a = self.Inputtable.takeItem(row,0).text()
                self.Inputtable.setItem(row,0,QTableWidgetItem(a))
                backsight.append(a)
            except Exception:
                backsight.append('')
            try:
                a = self.Inputtable.takeItem(row,1).text()
                self.Inputtable.setItem(row,1,QTableWidgetItem(a))
                foresight.append(a)
            except Exception:
                foresight.append('')
            try:
                a = self.Inputtable.takeItem(row, 2).text()
                self.Inputtable.setItem(row, 2, QTableWidgetItem(a))
                remarks.append(a)
            except Exception:
                remarks.append('')
        self.comp.readDataFromFile([data for data in zip(backsight,foresight,remarks) if data[0]!='' or data[1]!='' or data[2]!=''])

    def compute(self):
        try:

            self.retrievedata()
            self.comp.change_in_Height_Calculation()
            self.comp.provisionHeightComputation()
            self.comp.absolute_Terms()
            self.comp.formObservationEquation()
            self.comp.computeUnkown()
            self.comp.computeMostProbableHeight()
            self.comp.computeResidual()
            self.comp.computeUniteVariance()
            self.comp.varianceVisualization()
            self.comp.standard_correction_for_residuals()
            self.statuslabel.setText("Computation successful")
        except Exception:
            self.statuslabel.setText("There is an issue due to wrong data entry. If issue still persists contact the developer on 0549238257(Martin Aborgeh)")


    def openAddParamUI(self):
        self.paramui.show()

    def errorMessage(self):
        print(' Something went wrong,please refer to the the video for appropriate data entry')
        print('If issue still persist,please contact the developer on 0549238257')

    def elevationDetails(self):
        initial_Elevation = self.paramui.lineEdit.text()
        final_Elevation = self.paramui.lineEdit_2.text()
        self.comp.getElevationdetails(initial_Elevation,final_Elevation)

    def openexportpath(self):
        save, check1 =QFileDialog.getSaveFileName(None,"QFileDialog.getOSaveFileNames()","","All Files(*)")
        link1=None
        if check1:
            link1 = f"{save}{'.csv'}"
        self.outputpath = link1
        self.exportui.path.setText(self.outputpath)


    def export(self):
        self.exportui.show()

    def okexport(self):
        comboitem = self.exportui.exportcomboBox.currentText()
        if comboitem:
            if comboitem == 'Input Table':
                self.retrievedata()
                self.comp.output(self.outputpath,self.comp.tabledata,("Backsight","Foresight","Remarks"))
            elif comboitem =='Export Final Output':
                self.comp.output(self.outputpath,self.comp.final_output,("lines","residuals","qxixi","residual_bar","rejected/accepted"))
            elif comboitem == 'Initial Results Table':
                lines = self.comp.remarks
                change_in_height = self.comp.Change_in_height
                self.comp.output(self.outputpath,zip(lines,change_in_height),("Lines","Change in Heights"))
            elif comboitem == 'Observation Matrix Table':
                self.retrievedata()
                matrix_headers = self.comp.tabledata
                del matrix_headers[0]
                del matrix_headers[-1]
                self.comp.output(self.outputpath,[tuple(item) for item in self.comp.observation_matrix],[data[2] for data in matrix_headers])
            elif comboitem == 'Absolute Terms':
                self.comp.output(self.outputpath,[(item,) for item in self.comp.absolute_term],["Absolute Terms"])
            elif comboitem =='Most Probable Height':
                self.retrievedata()
                matrix_headers = self.comp.tabledata
                del matrix_headers[0]
                del matrix_headers[-1]
                point_names = [data[2] for data in matrix_headers]
                prov_height = self.comp.provisional_heights
                corrections = self.comp.unknown
                mpv = self.comp.most_probable_height
                inputdata = zip(point_names, prov_height, corrections.flatten(), mpv.flatten())
                self.comp.output(self.outputpath,inputdata,("points","Provisional Height","Correction","Most Probable Height"))
            elif comboitem == 'Residuals':
                self.comp.output(self.outputpath,[(item,) for item in self.comp.residual.flatten()],["Residual"])
            elif comboitem == 'Unit Variance':
                self.comp.output(self.outputpath,[(self.comp.unitvariance,)],["Unit Variance"])
            elif comboitem == '99 per Confidence Level':
                self.comp.output(self.outputpath,[(self.comp.perc_confidence_level,)],["Confidence Level",])


        else:
            print('choose input item')

    def Import(self):
        save, check1 = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files(*)")
        link1 = None
        if check1:
            link1 = save
        inputdata = self.comp.Input(link1)
        for i,row in enumerate(inputdata,start=1):
            try:
                self.Inputtable.setItem(i, 0, QTableWidgetItem(row[0]))
                self.Inputtable.setItem(i, 1, QTableWidgetItem(row[1]))
                self.Inputtable.setItem(i, 2, QTableWidgetItem(row[2]))
            except Exception:
                pass










if __name__=="__main__":
    def my_exception(type, value, tback):
        print(tback, value, tback)
        sys.__excepthook__(type, value, tback)
    sys.excepthook = my_exception
    app = QApplication(sys.argv)
    mainuiobj = MainUIClass()
    app.exec()
