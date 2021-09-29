"""
http://jira.nikel.loc/browse/UNIKTEST-185
"""

from math import acos, asin, pow, pi, sqrt


class CalculationError(Exception):
    """
    class calculation exception
    """
    pass


class Computation:
    """
    class calculation operations
    """

    @staticmethod
    def calc_active_power(voltage, current, cos_):
        """calculating active power
        :param: voltage, type int, voltage
        :param: current, type int, current
        :param: cos, type int, cosine
        :return: active power
        :rtype int
        """
        return voltage * current * cos_

    @staticmethod
    def calc_reactive_power(voltage, current, sin_):
        """calculating  reactive power
        :param: voltage, type int, voltage
        :param: current, type int, current
        :param: sin, type int, sine
        :return: reactive power
        :rtype int
        """
        return voltage * current * sin_

    @staticmethod
    def calc_active_power_all(voltage, current, cos_):
        """calculating active power by every phase
        :param: voltage, type int, voltage
        :param: current, type int, current
        :param: cos, type int, cosine
        :return: active power summary by all phases,
        :rtype int
        """
        return (voltage * current * cos_) * 3

    @staticmethod
    def calc_reactive_power_all(voltage, current, sin_):
        """calculating  reactive power by every phase
        :param: voltage, type int, voltage
        :param: current, type int, current
        :param: sin, type int, sine
        :return: active power summary by all phases
        :rtype int
        """
        return (voltage * current * sin_) * 3

    @staticmethod
    def calc_full_power(active_power, reactive_power):
        """calculating  full power
        :param: active_power, type int, active power
        :param: reactive_power, type int, reactive power
        :return: active power summary by all phases
        :rtype: type float
        """
        return sqrt(pow(active_power, 2)) + sqrt(pow(reactive_power, 2))

    # @staticmethod
    # def calc_power_factor(voltage, current, cos_):
    #     """calculating  power factor
    #     :param: voltage, type int, voltage
    #     :param: current, type int, current
    #     :param: cos, type int, cosine
    #     :return: power factor
    #     :rtype: type int
    #     ???????????????????????????????????????????????????????
    #     """
    #     return voltage * current * cos_ / (voltage * current)

    @staticmethod
    def deviation_minus(value, deviation=0.01):
        """calculating deviation from the given parameter in minus
        :param value: any value
        :type value: float
        :param deviation: should be in percent 0.01 = 1%
        :type deviation: float
        :return value which depends from deviation in minus
        :rtype type float
        """
        deviation_sum = value * deviation
        return value - deviation_sum

    @staticmethod
    def deviation_plus(value, deviation=0.01):
        """calculating deviation from the given parameter in plus
        :param value: any value
        :type value: float
        :param deviation: should be in percent 0.01 = 1%
        :type deviation: float
        :return value wich depends from deviation in plus
        :rtype type float
        """
        deviation_sum = value * deviation
        return value + deviation_sum

    @staticmethod
    def sin_to_degree(sin_):
        """converting from radians to degree
        :param: sin, type int, radians
        :return: degree
        :rtype: type float
        """
        sin_ = float(sin_)
        if sin_ > 1 or sin_ < -1:
            raise CalculationError("sin degree value not correct")
        return round(asin(sin_) * 180 / pi)

    @staticmethod
    def cos_to_degree(cos_):
        """converting from radians to degree
        :param cos_: radians
        :param cos_: float
        :return: degree
        :rtype: type float
        """
        cos_ = float(cos_)
        if cos_ > 1 or cos_ < -1:
            raise CalculationError("cos degree value not correct")
        return round(acos(cos_) * 180 / pi)

    @staticmethod
    def get_quadrant(angle):
        """defining quadrant
        :param: angle, type int, degree
        :return: quadrant
        :rtype: type int
        """
        n = int(angle / 360)
        angle -= n * 360

        if angle < 0:
            angle += 360

        res = int(angle / 90) + 1
        return res

    @staticmethod
    def check_quadrant(result, quadrant):
        """checks quadrant between calculated value and read from meter
        :param: result, type int, read from meter (for all phase)
        :param: calculated_quadrant, type int, calculated quadrant
        :return: True if correct quadrant else False
        :rtype: type bool
        """
        count = 0
        for i in result:
            count += 1
            if i > 0:
                break
        if count == quadrant:
            res = True
        else:
            res = False
        return res

    @staticmethod
    def calc_active_energ_1p(voltage, current, cos_):
        # returns value in watts
        """calculating active energy by one phase
        :param: voltage, type int, input voltage
        :param: current, type int, input current
        :param: cos, type float, input cosine
        :return: active energy by one phase
        :rtype: type int
        """
        result = (voltage * current * cos_) / 3600
        return result * 64  # 64 because at 64 seconds 100 watts winds up (a round number is convenient to debug)

    @staticmethod
    def calc_active_energ_3p(voltage, current, cos_):
        """calculating  active energy by all phases
        :param: voltage, type int, input voltage
        :param: current, type int, input current
        :param: cos, type float, input cosine
        :return: active energy by all phase
        :rtype: type int
        """
        result = (voltage * current * cos_) / 3600
        return result * 64 * 3

    @staticmethod
    def calc_reactive_energ_1p(voltage, current, sin_):
        """calculating  reactive energy by one phase
        :param: voltage, type int, input voltage
        :param: current, type int, input current
        :param: sin, type float, input sine
        :return: reactive energy by one phase
        :rtype: type int
        """
        result = (voltage * current * sin_) / 3600
        return result * 64

    @staticmethod
    def calc_reactive_energ_3p(voltage, current, sin_):
        """calculating reactive energy by all phases
        :param: voltage, type int, input voltage
        :param: current, type int, input current
        :param: sin, type float, input sine
        :return: reactive energy by one phase
        :rtype: type int
        """
        result = (voltage * current * sin_) / 3600
        return result * 64 * 3

    @staticmethod
    def calc_full_energ(active_power, reactive_power):
        """calculating  full energy
        :param: active_power, type int, active power
        :param: reactive_power, type int, reactive power
        :return: full energy
        :rtype: type int
        """
        result = (sqrt(pow(active_power, 2) + pow(reactive_power, 2))) / 3600 * 64
        return result

    @staticmethod
    def calc_time_active_energy(voltage, max_current, impulses, phase):
        """calculating time for active energy
        :param voltage, type int, input voltage
        :param max_current, type int, input current
        :param impulses, type int, input amount of impulses
        :param phase, type int, number of phase
        :return time to test run for current meter
        :rtype int
        """
        numerator = 600 * pow(10, 6)
        denominator = phase * impulses * voltage * max_current
        result = numerator * 60 / denominator
        return result

    @staticmethod
    def calc_time_reactive_energy(voltage, max_current, impulses, phase):
        """calculating time for reactive energy
        :param voltage, type int, input voltage
        :param max_current, type int, input current
        :param impulses, type int, input amount of impulses
        :param phase, type int, number of phase
        :return time to test run for current meter
        :rtype int
        """
        numerator = 480 * pow(10, 6)
        denominator = impulses * voltage * max_current * phase
        result = round(numerator / denominator) * 60
        return result

    @staticmethod
    def calc_time_sensivity_transformer_switch(voltage, current, impulses):
        """ calculate time sensivity for transformer switch
        :param voltage, input voltage
        :param current, input current
        :param impulses, amount of impulses
        :return time
        :rtype int
        """
        numerator = 2.2 * 3600000
        denominator = impulses * voltage * current
        result = round(numerator / (denominator * sqrt(3)))
        return result

    @staticmethod
    def calc_time_sensivity_direct_switch(voltage, current, impulses, phase):
        """ calculate time sensivity direct switch
        :param voltage, type int, input voltage
        :param current, type int, input current
        :param impulses, type int, amount of impulses
        :param  phase, type int, number of phase
        :return time
        :rtype int
        """
        numerator = 2.2 * 3600000
        denominator = impulses * voltage * current * phase
        result = round(numerator / denominator)
        return result


if __name__ == '__main__':
    pass
