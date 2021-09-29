"""
common functions
"""
import datetime

from controller.__calculations import Computation
from tests.DLMS.globals import add_to_dict


def _correction_timeout_connection(test):
    """correction timeout connection by optoport
    :param test: object for work with meter
    :type test: class
    """
    timeout_connection_obis = [0, 0, 22, 0, 0, 255, 23, 8]
    before_ = test.Get(attr=timeout_connection_obis)
    if before_ < 80:
        test.Set(attr=timeout_connection_obis, data=[18, 100])


def switch_on_installation(calmet, meter_type, voltage, current, cos_=None, sin_=None):
    """switch channel by every phase with help Calmet installation
    :param calmet: object for work with calmet
    :type calmet: class
    :param meter_type: meter_type
    :type meter_type: str
    :param voltage: input voltage
    :type voltage: int
    :param current: input current
    :type current: int
    :param cos_: input cosine
    :type cos_: float
    :param sin_: input sine
    :type sin_: float
    """
    angle = None
    if cos_ is not None:
        angle = Computation.cos_to_degree(cos_=cos_)
    if sin_ is not None:
        angle = Computation.sin_to_degree(sin_=sin_)

    if meter_type == '1':
        calmet.set_voltage(volt_p1=voltage)
        calmet.set_current(cur_1p=current)
        if angle is not None:
            calmet.set_angle(u1i1=angle)
    elif meter_type == '3':
        calmet.set_voltage(volt_p1=voltage, volt_p2=voltage, volt_p3=voltage)
        calmet.set_current(cur_1p=current, cur_2p=current, cur_3p=current)
        if angle is not None:
            calmet.set_angle(u1i1=angle, u2i2=angle, u3i3=angle)

    one_phase_meter = (0, 1, 1, 0) if meter_type == '1' else (0, 0, 0, 0, 0, 0)
    calmet.set_standby_or_operate(*one_phase_meter)
    calmet.get_response()


def check_data(deviation_minus, deviation_plus, value):
    """checking correctness by input parameters
    :param deviation_minus: measurement deviation minus value
    :type deviation_minus: float
    :param deviation_plus: measurement deviation plus value
    :type deviation_plus: float
    :param value: measured value
    :type value: float
    :return True if correct measured value else False
    :rtype bool
    """
    res = False
    if deviation_minus is not None and deviation_plus is not None and value is not None:
        res = deviation_minus > value or value > deviation_plus
    return res


def switch_calmet_parameters(calmet, meter_type, n_voltage, m_current, a_impulses, t_delay, cos_=None, sin_=None):
    """switch channel by every phase with help Calmet installation
    :param calmet: object for work with calmet
    :type calmet: class
    :param meter_type: meter_type
    :type meter_type: str
    :param n_voltage: nominal voltage
    :type n_voltage: int
    :param m_current: minimal current
    :type m_current: int
    :param a_impulses: amount of impulses
    :type a_impulses: int
    :param t_delay: time delay
    :type t_delay: float
    :param cos_: input cosine
    :type cos_: float
    :param sin_: input sine
    :type sin_: float
    """
    res = False
    val = None
    if meter_type == '3':
        if cos_:
            val = Computation.cos_to_degree(cos_=cos_)
        if sin_:
            val = Computation.sin_to_degree(sin_=sin_)
        if val is not None:
            calmet.set_angle(u1i1=val, u2i2=val, u3i3=val)
            calmet.set_input_setting_impulses(inp=0, register=2, impulses=a_impulses)
            calmet.set_input_setting_impulses(inp=0, register=0, impulses=t_delay)
            calmet.set_voltage(volt_p1=n_voltage, volt_p2=n_voltage, volt_p3=n_voltage)
            calmet.set_current(cur_1p=m_current, cur_2p=m_current, cur_3p=m_current)
            res = True

    if meter_type == '1':
        if cos_:
            val = Computation.cos_to_degree(cos_=cos_)
        if sin_:
            val = Computation.sin_to_degree(sin_=sin_)
        if val is not None:
            calmet.set_angle(u1i1=val)
            calmet.set_voltage(volt_p1=n_voltage)
            calmet.set_input_setting_impulses(inp=0, register=2, impulses=a_impulses)
            calmet.set_input_setting_impulses(inp=0, register=0, impulses=t_delay)
            calmet.set_current(cur_1p=m_current)
            res = True
    return res


def run_proc(self, test_number, proc, mess, params=None):
    """ Documentation for a method run_proc. Added: 03.11.20 12:42 volodymyr.tyshchenko
    run procedure

    :param self: class object
    :type self: class
    :param test_number: test number
    :type test_number: str
    :param proc: function for run
    :type proc: function
    :param mess: message if error
    :type mess: str
    :param params: parameters to run function
    :type params: dict
    """
    try:
        self.log("info", test_number)
        self.start_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        if params is None:
            proc()
        else:
            proc(**params)
    except Exception as exc:
        self.tests_res[test_number] = [mess, 'ERROR', f"{exc}"]
    finally:
        self.stop_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        add_to_dict(self, test_number)
