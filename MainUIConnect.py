import sys
from PyQt6.QtWidgets import QApplication,QMainWindow,QHeaderView,QTableWidgetItem,QTableWidget,QLabel,QSizePolicy
from PyQt6 import uic
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from Computation import BackgroundComputation
class MainUIClass(QMainWindow):
    def __init__(self):
        super(MainUIClass,self).__init__()
        self.paramui =uic.loadUi(r'C:\Users\Martin Aborgeh\Desktop\Adjustment\Addparamui.ui')
        uic.loadUi(r'C:\Users\Martin Aborgeh\Desktop\Adjustment\MainUI.ui',self)
        self.Inputtable.horizontalHeader().setStretchLastSection(True)
        self.Inputtable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stylesheet = "::section{Background-color:rgb(73, 79, 85);color:rgb(0,0,0);font-size:14px;font-weight:bold;border-radius:14px;}"
        self.Inputtable.horizontalHeader().setStyleSheet(stylesheet)
        self.comboBoxitem.currentIndexChanged.connect(self.Comboitem)
        self.pushButton.clicked.connect(self.compute)
        self.comp = BackgroundComputation()
        self.actionAdd.triggered.connect(self.openAddParamUI)
        self.paramui.elevation.clicked.connect(self.elevationDetails)
        self.show()

    def initial_table_results(self):
        self.change_Outputwidget()
        output_table = QTableWidget()
        output_table.setRowCount(500)
        output_table.setColumnCount(5)
        output_table.setHorizontalHeaderLabels(["STATION","RISE","FALL","CHANGE IN HEIGHT","PROVISIONAL HEIGHT"])
        output_table.horizontalHeader().setStretchLastSection(True)
        output_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stylesheet = "::section{Background-color:rgb(73, 79, 85);color:rgb(0,0,0);font-size:14px;font-weight:bold;border-radius:14px;}"
        output_table.horizontalHeader().setStyleSheet(stylesheet)
        self.output_widget.addWidget(output_table)


    def change_Outputwidget(self):
        for i in reversed(range(self.output_widget.count())):
            widget_item_to_remove = self.output_widget.itemAt(i).widget()
            self.output_widget.removeWidget(widget_item_to_remove)
            widget_item_to_remove.setParent(None)

    def Comboitem(self):
        current_comboitem = self.comboBoxitem.currentText()
        if current_comboitem == 'Initial Results':
            self.initial_table_results()
        elif current_comboitem == 'Observation Matrix':
            pass
        elif current_comboitem == 'Absolute Terms':
            pass
        elif current_comboitem == 'Most Probable Heights':
            pass
        elif current_comboitem == 'Residuals':
            pass
        elif current_comboitem == 'Units Variance':
            pass
        elif current_comboitem == '99% Confidence Level':
            pass
        elif current_comboitem == 'Error Ellipse':
            pass
        else:
            self.change_Outputwidget()
            label = QLabel("OUTPUT DATA APPEARS HERE")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
            label.setFont(QFont('Arial',14))
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
            print('Computation successful')
        except Exception:
            self.errorMessage()

    def openAddParamUI(self):
        self.paramui.show()

    def errorMessage(self):
        print(' Something went wrong,please refer to the the video for appropriate data entry')
        print('If issue still persist,please contact the developer on 0549238257')

    def elevationDetails(self):
        initial_Elevation = self.paramui.lineEdit.text()
        final_Elevation = self.paramui.lineEdit_2.text()
        self.comp.getElevationdetails(initial_Elevation,final_Elevation)



if __name__=="__main__":
    def my_exception(type, value, tback):
        print(tback, value, tback)
        sys.__excepthook__(type, value, tback)
    sys.excepthook = my_exception
    app = QApplication(sys.argv)
    mainuiobj = MainUIClass()
    app.exec()
