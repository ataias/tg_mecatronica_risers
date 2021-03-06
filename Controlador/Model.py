# -*- coding: utf-8 -*-
import numpy
from ReducedModel import ReducedModel
from DelayBlock import DelayBlock
from Controller import Controller
from PlantOrig import PlantOrig


class Model:
    def __init__(self, n, A, B, C, D, Ak, Bk, Ck, Q, R, Kp, Ki, epsilon, Ts, plant):
        self.reduced_model = ReducedModel(n, A, B, C, D)
        self.feedback_controller = Controller(Kp, Ki, n, Ak, Bk, Ck, Q, R)
        self.delay_block = DelayBlock(epsilon, Ts)
        self.plant = plant
        self.y_err = 0.0
        self.y = 0.0
        self.rm_out = 0.0
        self.u = 0.0

    def closed_loop(self, y_top, y_bottom):
        self.rm_out = self.reduced_model.compute_y(self.u)
        self.y_err = (self.rm_out - self.delay_block.get_last_entry()) + y_bottom - self.y
        self.delay_block.update(self.rm_out)
        controller_out = self.feedback_controller.compute_next_u(self.y_err)
        self.u = y_top + controller_out
        self.y = self.plant.compute_y(self.u)
        return self.y


if __name__ == "__main__":
    Kp = numpy.matrix([0.0101, 0.0123, -0.0050, -0.0022])
    Ki = 0.2326
    n = 4
    A = numpy.matrix([[0.993175847266250, 0.0997676389875316, 0.00447446153612418, 0.000154491807255262],
                      [-0.266442692060039, 0.989506934720158, 0.0794137333776907, 0.00441443534842949],
                      [-7.61331011046535, -0.371277877313592, 0.407916221277208, 0.0776985503560236],
                      [-134.001998512554, -9.45851595845769, -10.6078657460473, 0.377727256243161]])
    B = numpy.matrix([0.674742463375352, 3.50238796155364, -32.6963528822316, -364.795682866366]).transpose()
    C = numpy.matrix([1.0, 0.0, 0.0, 0.0])
    D = numpy.matrix([0])
    Ak = numpy.matrix([[0.993175847266250, 0.0997676389875316, 0.00447446153612418, 0.000154491807255262],
                       [-0.266442692060039, 0.989506934720158, 0.0794137333776907, 0.00441443534842949],
                       [-7.61331011046535, -0.371277877313592, 0.407916221277208, 0.0776985503560236],
                       [-134.001998512554, -9.45851595845769, -10.6078657460473, 0.377727256243161]])

    Bk = numpy.matrix([0.674742463375352, 3.50238796155364, -32.6963528822316, -364.795682866366]).transpose()
    Ck = numpy.matrix([1.0, 0.0, 0.0, 0.0])
    Q = 0.01 ** 2 * numpy.eye(4)
    R = 0.1 ** 2
    epsilon = 0.3
    Ts = 0.1
    plant = PlantOrig()
    model = Model(n, A, B, C, D, Ak, Bk, Ck, Q, R, Kp, Ki, epsilon, Ts, plant)
    print(model.delay_block.dim)
    lst = []
    for i in range(0, 6):
        lst.append(model.reduced_model.compute_y(1))
    print(lst)
