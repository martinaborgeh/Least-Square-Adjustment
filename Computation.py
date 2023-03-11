# Least Squared Reduction
import numpy as np
from sympy import symbols
import math as m
import matplotlib.pyplot as plt
class BackgroundComputation:
    def __init__(self):
        self.tabledata = None
        self.Change_in_height = []
        self.rise,self.fall = [],[]
        self.error_message = None
        self.initial_Elevation = None
        self.final_Elevation = None
        self.provisional_heights =[]
        self.absolute_term = None
        self.observation_matrix = None
        self.weigth_matrx = None
        self.unknown = None
        self.residual = None
        self.unitvariance =  None
        self.N = None
        self.qij = None

    def readDataFromFile(self,data):
        self.tabledata = data

    def getElevationdetails(self,initial_elev,final_elev):
        self.initial_Elevation = float(initial_elev)
        self.final_Elevation = float(final_elev)
        self.provisional_heights.clear()
        self.provisional_heights.append(initial_elev)


    def change_in_Height_Calculation(self):
        self.Change_in_height.clear()
        self.rise.clear()
        self.fall.clear()
        i=0
        for i, item in enumerate(self.tabledata):
            try:
                if ((item[0] != '' and item[1]=='') or (item[0]!='' and item[1]!='')) and i + 1 != len(self.tabledata):
                    difference_in_height = float(item[0]) - float(self.tabledata[i + 1][1])
                    self.Change_in_height.append(difference_in_height)
                    if difference_in_height<float(0):
                        self.fall.append(difference_in_height)
                    else:
                        self.rise.append(difference_in_height)
                else:self.error_message ='Wrong Entry'
            except Exception:
                self.error_message = 'Check your entry, there must be something wrong'
        i+=2


    def provisionHeightComputation(self):
        self.provisional_heights.clear()
        self.provisional_heights.append(self.initial_Elevation)
        initial_elev = self.initial_Elevation
        for data in self.Change_in_height:
            prov_heights = data+initial_elev
            self.provisional_heights.append(prov_heights)
            initial_elev = prov_heights

    def absolute_Terms(self):
        change_in_provisional_heights = [data-self.provisional_heights[i+1] for i,data in enumerate(self.provisional_heights) if i+1!= len(self.provisional_heights)]
        self.absolute_term=np.array([data[0]+data[1] for data in zip(self.Change_in_height,change_in_provisional_heights)])


    def formObservationEquation(self):
        coefficient=[]
        remarks = [f'{self.tabledata[i + 1][2]}-{data[2]}'for i,data in enumerate(self.tabledata) if i + 1!=len(self.tabledata)]
        varinstance = vars()
        for item in remarks:
            varinstance[item[0]], varinstance[item[2]] = symbols(f"{item[0]},{item[2]}")
            expr = eval(item)
            coefficient.append([expr.coeff(item[0]),expr.coeff(item[2])])
        del coefficient[0][1]
        del coefficient[-1][0]
        size = len(coefficient)
        # print(len(self.tabledata))
        matrix = np.zeros((size, len(self.tabledata)-2), dtype=np.int64)

        j = 0
        for i, item in enumerate(coefficient):
            try:
                if len(item) == 1:
                    if i == 0:
                        matrix[i][j] = item[0]
                    else:
                        matrix[i][-1] = item[0]

                elif len(item) == 2:
                    if i == 1:
                        matrix[i][j] = item[0]
                        matrix[i][j + 1] = item[1]
                    else:
                        j += 1
                        matrix[i][j] = item[0]
                        matrix[i][j + 1] = item[1]

            except Exception : pass
        # print(matrix)
        self.observation_matrix = matrix
    def computeUnkown(self):

        self.weigth_matrx=np.identity(len(self.observation_matrix),dtype=np.int64)
        self.N = np.linalg.inv(np.matmul(np.matmul(self.observation_matrix.transpose(), self.weigth_matrx),self.observation_matrix))
        B = np.matmul(np.matmul(self.observation_matrix.transpose(), self.weigth_matrx),np.reshape(self.absolute_term,(len(self.absolute_term),1)))
        self.unknown = np.matmul(self.N,B)

    def computeMostProbableHeight(self):
        self.provisional_heights.pop(0)
        self.provisional_heights.pop()
        most_probable_height = self.unknown + np.reshape(np.array(self.provisional_heights),(len(self.provisional_heights),1))


    def computeResidual(self):
        self.residual = np.matmul(self.observation_matrix,self.unknown)-np.reshape(self.absolute_term,(len(self.absolute_term),1))


    def computeUniteVariance(self):
        self.unitvariance = np.matmul(self.residual.transpose(),np.matmul(self.weigth_matrx,self.residual))[0][0]/(len(self.observation_matrix)-len(self.unknown))
        # print(self.unitvariance)


    def varianceVisualization(self):
        plt.plot(self.residual.flatten())
        plt.show()

    def standard_correction_for_residuals(self):
        cx_diagonals_square =[m.sqrt(item) for item in self.unitvariance*self.N.diagonal()]
        cv = self.unitvariance*np.subtract(np.linalg.inv(self.weigth_matrx),np.matmul(np.matmul(self.observation_matrix,self.N),self.observation_matrix.transpose()))
        cv_diagonals_square = [m.sqrt(item) for item in cv.diagonal()]
        self.qij = np.subtract(np.linalg.inv(self.weigth_matrx),np.matmul(np.matmul(self.observation_matrix,self.N),self.observation_matrix.transpose()))



