import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime
import pandas as pd
from EdenOffLattice import *

class DiscAnalysis:
    """class used to analyse data generated by the Ballistic Deposition Class"""

    def __init__(self):
        analysis_array1 = np.array([])
        analysis_array2 = np.array([])
        analysis_array3 = np.array([])
        analysis_array4 = np.array([])
        self.analysis_array1 = analysis_array1
        self.analysis_array2 = analysis_array2
        self.analysis_array3 = analysis_array3
        self.analysis_array4 = analysis_array4

    def add_data(self, data, target_array):
        """filling data into separate roughness array and creating the matching time array; need to enter numpy array as the parameter"""
        for i in np.arange(0, data.size):
            target_array = np.append(target_array, data[i])
        return target_array

    def standard_deviations(self, errors_array):
        """works out the standard deviations for each set of data values stored in a 2D array"""
        x = np.array([])
        for i in np.arange(0, len(errors_array), 1):
            x = np.append(x, np.std(errors_array[i]))
        return x

    def roughness_dynamics(self, other, tracker, initial_power,data_points):  # generates a series of roughness values for a series of matrices
        """iterates the BD forward in time, depositing n particles for each of the iterations; takes instance of the EdenCDisc or EdenADisc class"""
        x = np.array([])
        m = initial_power + 1
        print "1"
        while m <= data_points + initial_power:
            print m
            other.deposit_particles(2 ** m)
            tracker.update(data_point_number=m - initial_power)
            x = np.append(x,other.roughness_2())  # appending the roughnesses of system after each set of 2**m particles have been deposited
            tracker.display(other)
            m = m + 1

        return x

    def create_time_array(self, initial_power, data_points):
        """creating the number of data points required; equally spaced on a log-log plot"""
        t = np.array([])
        m = initial_power + 1
        y = 0
        while m <= data_points + initial_power:
            y = y + 2 ** m
            t = np.append(t, y)
            m = m + 1
        return t

    #####################################################################################################################################################################
    def roughness_dynamics_partial(self, other, tracker, initial_power, data_points, simulations):
        """same as roughness_dynamics_average(), but stores all data points, allowing for data from other sessions to be collated"""
        z = np.zeros((data_points, simulations))
        for i in np.arange(0, simulations, 1):
            tracker.update(simulation_number=i + 1)
            other.reset_system()
            other.generate_disc(10., 0., 0.)  # plants the seed
            y = self.roughness_dynamics(other, tracker, initial_power, data_points)
            for j in np.arange(0, data_points, 1):
                z[j][i] = y[j]
        t = self.create_time_array(initial_power, data_points)
        return t, z

    def log_log_origin_partial(self, other, initial_power, data_points, simulations):
        start = np.datetime64(datetime.datetime.now())
        tracker = IterationTracker(total_data_points=data_points,total_simulations=simulations)
        t, z = self.roughness_dynamics_partial(other, tracker, initial_power, data_points, simulations)
        log_t = np.log(t)
        log_z = np.log(z)
        text_list = []
        text_list.append(log_t)
        for i in np.arange(0, simulations, 1):
            text_list.append(log_z[:, i])
        date = np.datetime64(datetime.datetime.now())
        ts = pd.to_datetime(str(date))
        d = ts.strftime('%d.%m.%Y, %H.%M.%S')
        np.savetxt("(%s, %g, %g, %g, %s).txt" % (other.__class__.__name__, initial_power, data_points, simulations, d), np.transpose(text_list))
        end = np.datetime64(datetime.datetime.now())
        print start, end



####################################################################################################################
####################################################################################################################

class IterationTracker:
    """class to track all the relevant stats during the simulation process"""

    def __init__(self, total_data_points=None, total_simulations=None):
        self.__total_data_points = total_data_points
        self.__total_simulations = total_simulations
        self.__data_point_number = 0
        self.__simulation_number = 0

    def update(self, data_point_number=None, simulation_number=None):
        if data_point_number != None:
            self.__data_point_number = data_point_number
        if simulation_number != None:
            self.__simulation_number = simulation_number

    def display(self, other):
        print "%s %g %s %g, %s %g %s %g" % ("simulation number", self.__simulation_number, "out of", self.__total_simulations, "data point", self.__data_point_number, "out of", self.__total_data_points)