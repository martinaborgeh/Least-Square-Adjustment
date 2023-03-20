import os
import re
import math as m
import numpy as np
class LocalGeoid:
    def __init__(self):
        self.inputdata = None
        self.Northings = None
        self.Eastings = None
        self.Othometric_heights = None
        self.Ellipsoidal_heights = None
        self.h=632.529
        self.H = 270.262
        self.centralpoint_h = 632.529-270.262
        self.centralpoint_N = 732921.9
        self.centralpoint_E = 700906.6
        self.positive_coeffi = None
        self.change_in_N = None
        self.change_in_E =None
        self.change_in_N_and_origin = None
        self.observationMatrix = None


    def readdata(self,path):
        with open(rf"{path}") as inputpath:
            cleaneddata = [data.strip().strip('/n').split(',') for data in inputpath.readlines()]
            cleaneddata.pop(0)
            self.Northings = [float(data[1]) for data in cleaneddata]
            self.Eastings  = [float(data[2]) for data in cleaneddata]
            self.Othometric_heights=[float(data[3]) for data in cleaneddata]
            self.Ellipsoidal_heights =[float(data[4]) for data in cleaneddata]
            self.inputdata=cleaneddata
            return  self.Northings,self.Eastings,self.Othometric_heights,self.Ellipsoidal_heights
    def change_in_parameters(self):
        change_in_orthometric  = [item[0]-item[1] for item in zip(self.Ellipsoidal_heights,self.Othometric_heights)]
        self.change_in_N_and_origin = [item-self.centralpoint_h for item in change_in_orthometric]
        self.change_in_N = [ item-self.centralpoint_N for item in self.Northings]
        self.change_in_E = [ item -self.centralpoint_E for item in self.Eastings]


    def observation_expression(self):
        coeeficients = []
        self.positive_coeffi = []
        for data in zip(self.change_in_N, self.change_in_E):
            item = f"{data[0]}N{-data[1] if data[1] > 0.0 else f'+{-data[1]}'}E"
            coeeficients.append(re.findall(r"[+-]?\d*\.?\d+", item))
        for item in coeeficients:
            for i, element in enumerate(item):
                item[i] = float(element)
            item.append(1)
            self.positive_coeffi.append(item)

        self.observationMatrix = np.array(self.positive_coeffi)

    def unknown(self):
        self.weigth_matrx = np.identity(len(self.observationMatrix),dtype=np.int64)
        self.N = np.linalg.inv(
            np.matmul(np.matmul(self.observationMatrix.transpose(), self.weigth_matrx), self.observationMatrix))
        B = np.matmul(np.matmul(self.observationMatrix.transpose(), self.weigth_matrx),
                      np.reshape(self.change_in_N_and_origin, (len(self.change_in_N_and_origin), 1)))
        self.Unknown = np.matmul(self.N, B)






    def geoid_model(self):
        height = []
        new_data = self.readdata(os.path.abspath('test_geoid.csv'))
        lat, lon, H, h =new_data[0],new_data[1],new_data[2],new_data[3]
        unknown = self.Unknown.flatten()
        for data in zip(lat,lon,h,H):
            change_N = (unknown[0]*(data[0]-self.centralpoint_N))-(unknown[1]*(data[1]-self.centralpoint_E))+unknown[2]
            Height = self.H + (data[2]-self.h)-change_N
            # print(Height)
            height.append(Height)
        print(H)
        print(height)






if __name__ == "__main__":
    obj = LocalGeoid()
    obj.readdata(os.path.abspath('Train_geoid_,model.csv'))
    obj.change_in_parameters()
    obj.observation_expression()
    obj.unknown()
    obj.geoid_model()