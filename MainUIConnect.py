import sys
from PyQt6.QtWidgets import QApplication,QMainWindow,QHeaderView,QTableWidgetItem
from PyQt6 import uic

from Computation import BackgroundComputation
class MainUIClass(QMainWindow):
    def __init__(self):
        super(MainUIClass,self).__init__()
        self.paramui =uic.loadUi(r'C:\Users\Martin Aborgeh\Desktop\Adjustment\Addparamui.ui')
        uic.loadUi(r'C:\Users\Martin Aborgeh\Desktop\Adjustment\MainUI.ui',self)
        self.Inputtable.horizontalHeader().setStretchLastSection(True)
        self.Inputtable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pushButton.clicked.connect(self.compute)
        self.comp = BackgroundComputation()
        self.actionAdd.triggered.connect(self.openAddParamUI)
        self.paramui.elevation.clicked.connect(self.elevationDetails)
        self.show()

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
