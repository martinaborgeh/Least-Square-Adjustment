import os
import re
import math as m
import numpy as np
from sympy.abc import e,n
class Horizontal_Cordinate_Adjustment():
    def __init__(self):
        self.Northings = None
        self.Eastings = None
        self.calculated_bearing = None
        self.distance = None
        self.included_angle = None
        self.observed_Bearing = None
        self.ci = None
        self.si = None
        self.positive_coeffi = None
        self.observationMatrix = None
    def readdata(self):
        with open(rf"{os.path.abspath('coordinate_raw_input.csv')}") as inputpath:
            cleaneddata = [data.strip().strip('/n').split(',') for data in inputpath.readlines()]
            cleaneddata.pop(0)
            self.Northings = [float(item[1]) for item in cleaneddata]
            self.Eastings = [float(item[2]) for item in cleaneddata]
    def Bearing_computation_and_distance(self):
        self.distance = []
        self.calculated_bearing = []
        zipped = list(zip(self.Northings,self.Eastings))
        for i,item in enumerate(zipped):
            try:
                bearing = m.degrees(m.atan2(zipped[i+1][1]-item[1],zipped[i+1][0]-item[0]))
                self.calculated_bearing.append(bearing+float(360)) if bearing <float(0) else self.calculated_bearing.append(bearing)
                self.distance.append(m.sqrt(pow(zipped[i+1][1]-item[1],2)+pow(zipped[i+1][0]-item[0],2)))



            except Exception:
                pass
        # print(zipped)
        # print(self.distance)

    def included_angle_Computation(self):
        self.included_angle = [ (self.calculated_bearing[i+1]-bearing)+360 if self.calculated_bearing[i+1]-bearing < float(0) else self.calculated_bearing[i+1]-bearing  for i,bearing in enumerate(self.calculated_bearing) if i+1!=len(self.calculated_bearing)]


    def observed_bearing(self):
        self.observed_Bearing = []
        for i,item in enumerate(self.calculated_bearing):
            try:
                self.observed_Bearing.append((item+self.included_angle[i])-float(360) if item+self.included_angle[i]>float(360) else item+self.included_angle[i])
            except Exception:
                pass
        self.observed_Bearing.insert(0,self.calculated_bearing[0])
        # print(self.observed_Bearing)

    def difference_in_bearing(self):
        self.difference_bearing = [bearing[0]-bearing[1] for bearing in zip(self.observed_Bearing,self.calculated_bearing)]


    def ciciplus1(self):
        self.ci = [(m.cos(m.radians(item[0])))/(item[1]*m.sin(m.radians(0.00027777777))) for item in zip(self.calculated_bearing,self.distance)]
        self.si = [(m.sin(m.radians(item[0])))/(item[1]*m.sin(m.radians(0.00027777777))) for item in zip(self.calculated_bearing,self.distance)]


    def observation_expression(self):
        coeeficients =[]
        self.positive_coeffi = []
        for data in zip(self.ci,self.si):
            item = f"{-data[0]}e{data[1] if data[1]<0.0 else f'+{data[1]}'}n{data[0] if data[0]<0.0 else f'+{data[0]}'}e{-data[1] if data[1]>float(0.0) else f'+{-data[1]}'}n"
            coeeficients.append(re.findall(r"[+-]?\d*\.?\d+",item))
        for item in coeeficients:
            for i,element in enumerate(item):
                item[i]=float(element)
            self.positive_coeffi.append(item)
     


    def observation_matrix(self):
        self.observationMatrix = np.array(self.positive_coeffi)



    def unknown(self):
        self.weigth_matrx = np.identity(len(self.observationMatrix), dtype=np.int64)
        # print(np.matmul(np.matmul(self.observationMatrix.transpose(), self.weigth_matrx), self.observationMatrix))
        self.N = np.matrix(np.matmul(np.matmul(self.observationMatrix.transpose(), self.weigth_matrx), self.observationMatrix))
        print(self.N.I)
        # B = np.matmul(np.matmul(self.observationMatrix.transpose(), self.weigth_matrx),
        #               np.reshape(self.difference_bearing, (len(self.difference_bearing), 1)))
        # self.unknown = np.matmul(self.N, B)
        # print(self.unknown)

    def most_probable(self):
        pass

    def residual_unit_variance(self):
        pass

    def standard_residual(self):
        pass














if __name__ =='__main__':
    obj = Horizontal_Cordinate_Adjustment()
    obj.readdata()
    obj.Bearing_computation_and_distance()
    obj.included_angle_Computation()
    obj.observed_bearing()
    obj.difference_in_bearing()
    obj.ciciplus1()
    obj.observation_expression()
    obj.observation_matrix()
    obj.unknown()