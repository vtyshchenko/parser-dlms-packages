import datetime

from component.gurux_dlms.enums import DateTimeSkips
# from excel_report import ExcelReport
# from send_mail import send_email

from component.gurux_dlms.enums import DataType
from component.gurux_dlms.GXDateTime import GXDateTime
from component.gurux_dlms.objects import GXDLMSActivityCalendar, GXDLMSCaptureObject, GXDLMSClock, GXDLMSDayProfile, \
    GXDLMSDayProfileAction, GXDLMSDemandRegister, GXDLMSRegister, GXDLMSSeasonProfile, GXDLMSSpecialDay, \
    GXDLMSSpecialDaysTable, GXDLMSWeekProfile, GXDLMSData, GXDLMSExtendedRegister, GXDLMSProfileGeneric
from component.gurux_dlms.manufacturersettings import GXAttributeCollection, GXAuthentication,\
    GXDLMSAttributeSettings, GXDLMSAttribute, GXManufacturer, GXManufacturerCollection,  GXObisCode, \
    GXObisCodeCollection, GXObisValueItem, GXObisValueItemCollection, GXServerAddress, HDLCAddressType, InactivityMode,\
    StartProtocolType

DEBUG = True

level_code = {
    'CRITICAL': 50,
    'FATAL':    50,
    'ERROR':    40,
    'WARN':     30,
    'WARNING':  30,
    'INFO':     20,
    'DEBUG':    10,
    'NOTSET':   0,
    }

DAY_OF_WEEK = {
    'MONDAY':    1,
    'TUESDAY':   2,
    'WEDNESDAY': 3,
    'THURSDAY':  4,
    'FRIDAY':    5,
    'SATURDAY':  6,
    'SUNDAY':    7
}

OBIS_ACTION_SCHEDULE                   = '0.0.15.0.0.255'
OBIS_ACTIVE_ENERGY_POSITIVE            = '1.0.1.8.0.255'
OBIS_ACTIVE_ENERGY_NEGATIVE            = '1.0.2.8.0.255'
OBIS_ACTIVE_POS_PLUS_NEGATIVE          = '1.0.15.8.0.255'
OBIS_ACTIVE_POS_MINUS_NEGATIVE         = '1.0.16.8.0.255'
OBIS_ACTIVE_ENERGY_AQ1                 = '1.0.17.8.0.255'
OBIS_ACTIVE_ENERGY_AQ2                 = '1.0.18.8.0.255'
OBIS_ACTIVE_ENERGY_AQ3                 = '1.0.19.8.0.255'
OBIS_ACTIVE_ENERGY_AQ4                 = '1.0.20.8.0.255'
OBIS_REACTIVE_ENERGY_POSITIVE          = '1.0.3.8.0.255'
OBIS_REACTIVE_ENERGY_NEGATIVE          = '1.0.4.8.0.255'
OBIS_REACTIVE_ENERGY_RQ1               = '1.0.5.8.0.255'
OBIS_REACTIVE_ENERGY_RQ2               = '1.0.6.8.0.255'
OBIS_REACTIVE_ENERGY_RQ3               = '1.0.7.8.0.255'
OBIS_REACTIVE_ENERGY_RQ4               = '1.0.8.8.0.255'
OBIS_TOTAL_ENERGY_POSITIVE             = '1.0.9.8.0.255'
OBIS_TOTAL_ENERGY_NEGATIVE             = '1.0.10.8.0.255'
OBIS_ACTIVITY_CALENDAR                 = '0.0.13.0.0.255'
OBIS_ALARM_LOG                         = '0.0.99.98.9.255'
OBIS_ALARM_REGISTER_1                  = '0.0.97.98.0.255'
OBIS_ALARM_REGISTER_2                  = '0.0.97.98.1.255'
OBIS_ALARM_DESCRIPTOR_1                = '0.0.97.98.20.255'
OBIS_ALARM_DESCRIPTOR_2                = '0.0.97.98.21.255'
OBIS_APPLICATION_CHECKSUM              = '1.0.0.2.8.255'
OBIS_ASSOCIATION_AMI                   = '0.0.40.0.2.255'
OBIS_ASSOCIATION_ADMIN                 = '0.0.40.0.3.255'
OBIS_ASSOCIATION_MANUFACTURE           = '0.0.40.0.4.255'
OBIS_AVERAGE_TOTAL_POWER               = '1.0.15.24.0.255'
OBIS_AVERAGE_IMPORT_POWER              = '1.0.1.24.0.255'
OBIS_PUBLIC_ASSOCIATION                = '0.0.40.0.1.255'    # OBIS_ASSOCIATION_LOGICAL_NAME
OBIS_BAT_VOLTAGE                       = '0.0.96.6.3.255'
OBIS_CLOCK                             = '0.0.1.0.0.255'
OBIS_CURRENT_QUADRANT                  = '1.0.96.50.0.255'
OBIS_CUMULATIVE_MAX_DENAND_ACTIVE      = '1.0.1.2.0.255'
OBIS_CUMULATIVE_MAX_DENAND_REACTIVE    = '1.0.3.2.0.255'
OBIS_DAILY_VALUES_PROFILE              = '1.0.98.2.0.255'
OBIS_DAILY_VALUES_PROFILE_STATUS       = '0.0.96.10.2.255'
OBIS_DATA_BILLING_PERIOD               = '0.0.98.1.0.255'
OBIS_DEMAND_REGISTER_ACTIVE_NEG        = "1.0.2.4.0.255"    # OBIS_DEMAND_REGISTER
OBIS_DEMAND_REGISTER_ACTIVE_POS        = "1.0.1.4.0.255"
OBIS_DEMAND_REGISTER_REACTIVE_POS      = "1.0.3.4.0.255"
OBIS_DEMAND_REGISTER_REACTIVE_NEG      = "1.0.4.4.0.255"
OBIS_DEVICE_TYPE                       = '0.0.96.1.3.255'   # OBIS_METER_TYPE
OBIS_DISCONNECTOR                      = '0.0.96.3.10.255'
OBIS_DISCONNECTOR_SCRIPT_TABLE         = '0.0.10.0.106.255'
OBIS_DURATION_LAST_LONG_POWER_FAILURE  = '0.0.96.7.19.255'
OBIS_DURATION_UNDERVOLTAGE_PHASE_L1    = '1.0.32.33.0.255'
OBIS_DURATION_UNDERVOLTAGE_PHASE_L2    = '1.0.52.33.0.255'
OBIS_DURATION_UNDERVOLTAGE_PHASE_L3    = '1.0.72.33.0.255'
OBIS_DURATION_OVERVOLTAGE_PHASE_L1     = '1.0.32.37.0.255'
OBIS_DURATION_OVERVOLTAGE_PHASE_L2     = '1.0.52.37.0.255'
OBIS_DURATION_OVERVOLTAGE_PHASE_L3     = '1.0.72.37.0.255'
OBIS_END_OF_BILLING_PERIOD             = '0.0.10.0.1.255'
OBIS_FRAUD_EVENT_LOG                   = '0.0.99.98.1.255'
OBIS_GENERAL_LOAD_PROFILE              = '1.0.99.1.0.255'
OBIS_GENERAL_LOAD_PROFILE_STATUS       = '0.0.96.10.1.255'
OBIS_INSTANTANEOUS_CURRENT             = '1.0.90.7.0.255'
OBIS_IEC_HDLC_LOCALPORT_SETUP          = '0.1.22.0.0.255'
OBIS_IEC_HDLC_INTERFACE_SETUP          = '0.0.22.0.0.255'   # OBIS_IEC_HDLC_SETUP
OBIS_IEC_LOCAL_PORT                    = '0.0.20.0.0.255'
OBIS_IMAGE_TRANSFER                    = '0.0.44.0.0.255'
OBIS_IMAGE_TRANSFER_CONFIGURATION      = '0.0.44.0.1.255'
OBIS_IMAGE_TRANSFER_ACTIVAT_SHEDULER   = '0.0.15.0.2.255'
OBIS_HIGH_LIMIT_THRESHOLD              = '1.0.12.35.0.255'
OBIS_HIGH_LIMIT_TIME_THRESHOLD         = '1.0.12.44.0.255'
OBIS_IC_COMPLIANT_SWITCH               = '0.128.43.128.128.255'
OBIS_FIRMWARE_VERSION                  = '1.0.0.2.0.255'
OBIS_LOCATION_INFORMATION              = '0.0.96.1.5.255'
OBIS_LOGICAL_NAME                      = '0.0.42.0.0.255'
OBIS_LOW_LIMIT_THRESHOLD               = '1.0.12.31.0.255'
OBIS_LOW_LIMIT_TIME_THRESHOLD          = '1.0.12.43.0.255'
OBIS_LIMITER                           = '0.0.17.0.0.255'
OBIS_MAGNITUDE_UNDERVOLTAGE_PHASE_L1   = '1.0.32.34.0.255'
OBIS_MAGNITUDE_UNDERVOLTAGE_PHASE_L2   = '1.0.52.34.0.255'
OBIS_MAGNITUDE_UNDERVOLTAGE_PHASE_L3   = '1.0.72.34.0.255'
OBIS_MAGNITUDE_OVERVOLTAGE_PHASE_L1    = '1.0.32.38.0.255'
OBIS_MAGNITUDE_OVERVOLTAGE_PHASE_L2    = '1.0.52.38.0.255'
OBIS_MAGNITUDE_OVERVOLTAGE_PHASE_L3    = '1.0.72.38.0.255'
OBIS_MAX_DEMAND_ACTIVE_POSITIVE        = '1.0.1.6.0.255'
OBIS_MAX_DEMAND_ACTIVE_NEGATIVE        = '1.0.2.6.0.255'
OBIS_MAX_DEMAND_REACTIVE_POSITIVE      = '1.0.3.6.0.255'
OBIS_MAX_DEMAND_REACTIVE_NEGATIVE      = '1.0.4.6.0.255'
OBIS_METER_FUNCTION                    = '0.0.130.0.0.255'
OBIS_STATUS_METROLOGY_CALLIBRATION     = '1.0.96.50.4.255'
OBIS_METROLOGY_VERSION                 = '1.0.0.2.1.255'
OBIS_MEASUREMENT_PERIOD_1              = '1.0.0.8.0.255'
OBIS_MEASUREMENT_PERIOD_3              = '1.0.0.8.2.255'
OBIS_MOMENT_ACTIVE_ENERGY_POS          = '1.0.1.7.0.255'
OBIS_MOMENT_ACTIVE_ENERGY_NEG          = '1.0.2.7.0.255'
OBIS_MOMENT_ACTIVE_POS_PLUS_NEG        = '1.0.15.7.0.255'
OBIS_MOMENT_ACTIVE_POS_MINUS_NEG       = '1.0.16.7.0.255'
OBIS_MOMENT_ACTIVE_ENERGY_AQ1          = '1.0.17.7.0.255'
OBIS_MOMENT_ACTIVE_ENERGY_AQ2          = '1.0.18.7.0.255'
OBIS_MOMENT_ACTIVE_ENERGY_AQ3          = '1.0.19.7.0.255'
OBIS_MOMENT_ACTIVE_ENERGY_AQ4          = '1.0.20.7.0.255'
OBIS_MOMENT_CURRENT                    = '1.0.11.7.0.255'
OBIS_MOMENT_FREQUENCY                  = '1.0.14.7.0.255'
OBIS_MOMENT_POWER_FACTOR               = '1.0.13.7.0.255'
OBIS_MOMENT_REACTIVE_ENERGY_POS        = '1.0.3.7.0.255'
OBIS_MOMENT_REACTIVE_ENERGY_NEG        = '1.0.4.7.0.255'
OBIS_MOMENT_REACTIVE_ENERGY_RQ1        = '1.0.5.7.0.255'
OBIS_MOMENT_REACTIVE_ENERGY_RQ2        = '1.0.6.7.0.255'
OBIS_MOMENT_REACTIVE_ENERGY_RQ3        = '1.0.7.7.0.255'
OBIS_MOMENT_REACTIVE_ENERGY_RQ4        = '1.0.8.7.0.255'
OBIS_MOMENT_TOTAL_ENERGY_POS           = '1.0.9.7.0.255'
OBIS_MOMENT_TOTAL_ENERGY_NEG           = '1.0.10.7.0.255'
OBIS_MOMENT_VOLTAGE                    = '1.0.12.7.0.255'
OBIS_MISSING_THRESHOLD                 = '1.0.12.39.0.255'
OBIS_MISSING_TIME_THRESHOLD            = '1.0.12.45.0.255'
OBIS_NOMINAL_VOLTAGE                   = '1.0.0.6.0.255'
OBIS_NOMINAL_CURRENT                   = '1.0.0.6.1.255'
OBIS_MAXIMUM_CURRENT                   = '1.0.0.6.3.255'
OBIS_NIK_SN                            = '0.0.96.1.4.255'
OBIS_NUMBER_POWER_FAILURE              = '0.0.96.7.21.255'
OBIS_NUMBER_LONG_POWER_FAILURE         = '0.0.96.7.9.255'
OBIS_NUMBER_UNDERVOLTAGE_PHASE_L1      = '1.0.32.32.0.255'
OBIS_NUMBER_UNDERVOLTAGE_PHASE_L2      = '1.0.52.32.0.255'
OBIS_NUMBER_UNDERVOLTAGE_PHASE_L3      = '1.0.72.32.0.255'
OBIS_NUMBER_OVERVOLTAGE_PHASE_L1       = '1.0.32.36.0.255'
OBIS_NUMBER_OVERVOLTAGE_PHASE_L2       = '1.0.52.36.0.255'
OBIS_NUMBER_OVERVOLTAGE_PHASE_L3       = '1.0.72.36.0.255'
OBIS_OUTPUT_PULSE_ACTIVE               = '1.0.0.3.3.255'
OBIS_POWER_QUALITY_EVENT_LOG           = '0.0.99.98.2.255'
OBIS_REGISTER_ACTIVATION               = '0.0.14.0.2.255'
OBIS_SAP_ASSIGNMENT                    = '0.0.41.0.0.255'
OBIS_SECURITY_SETUP                    = '0.0.43.0.0.255'
OBIS_PUBLIC_SECURITY_SETUP             = '0.0.43.0.1.255'
OBIS_SECURITY_SETUP_ADMIN              = '0.0.43.0.3.255'
OBIS_SECURITY_SETUP_AMI                = '0.0.43.0.2.255'
OBIS_SECURITY_SETUP_MANUFACTURE        = '0.0.43.0.4.255'
OBIS_SN_FOR_LCD                        = '0.129.96.1.4.255'
OBIS_SPECIAL_DAYS_TABLE                = '0.0.11.0.0.255'
OBIS_STANDART_EVENT_LOG                = '0.0.99.98.0.255'
OBIS_TARIFF                            = '0.0.96.14.0.255'
OBIS_TARIFF_EMERGENCY                  = '0.0.96.14.15.255'
OBIS_TARIFF_REGISTERS                  = '0.0.14.0.1.255'
OBIS_TARIFF_SCRIPT_TABLE               = '0.0.10.0.100.255'    # OBIS_SCRIPT_TABLE    OBIS_SCRIPT
OBIS_TEMPERATURE                       = '0.0.96.9.0.255'
OBIS_TIME_THRESHOLD_LONG_POWER_FAILURE = '0.0.96.7.20.255'
OBIS_TRILLIANT_SN                      = '0.0.96.1.0.255'    # OBIS_METER_BARCODE
OBIS_METER_MANUFACTURER                = '0.0.96.1.1.255'
OBIS_BOARD_SN                          = '0.0.96.1.2.255'
OBIS_TRILLIANT_MODULE_SN               = '0.0.96.1.8.255'
OBIS_CALLIBRATION_CURRENT_VALUE        = '1.0.96.50.6.255'
OBIS_CALLIBRATION_VOLTAGE_VALUE        = '1.0.96.50.7.255'
OBIS_CALLIBRATION_ACTIVE_POWER_VALUE   = '1.0.96.50.8.255'
OBIS_CALLIBRATION_REACTIVE_POWER_VALUE = '1.0.96.50.9.255'
OBIS_CALLIBRATION_1POINT_COEFFICIENT   = '1.0.96.50.10.255'
OBIS_CALLIBRATION_2POINT_COEFFICIENT   = '1.0.96.50.11.255'

Fraud_Event_Log_Description = {
        10: 'Standard Event log cleared',
        13: 'Alarm register cleared',
        14: 'Fraud Event log cleared',
        15: 'Power Quality Event log cleared',
        100: 'Load profile 1 cleared',
        101: 'Load profile 2 cleared',
        200: 'Meter cover closed',
        201: 'Meter cover removed',
        202: 'Terminal cover closed',
        203: 'Terminal cover removed',
        204: 'Strong magnetic field',
        205: 'Strong magnetic field no longer',
        446: 'Phase 1 Export mode start',
        447: 'Phase 2 Export mode start',
        448: 'Phase 3 Export mode start',
        449: 'Phase 1 Export mode end',
        450: 'Phase 2 Export mode end',
        451: 'Phase 3 Export mode end',
        1010: 'Disconnected due to tamper detect',
        1300: 'TOU calendar changed',
        1301: 'Passive TOU programmed',
        1302: 'One or more parameters changed',
        1303: 'Global key(s) changed',
        1500: 'Unauthorised Access request',
        1501: 'Meter password changed',
        1502: 'Meter HLS secret changed',
        1503: 'Decryption or authentication failure(n-time failure)',
        1600: 'Battery Cover Closed',
        1601: 'Battery Cover Removed',
        1602: 'Battery Failure',
        1603: 'Battery Low',
        1604: 'Battery ok',
        1605: 'Replace Battery',
        1606: 'Missing neutral',
        1607: 'Reverse energy detected',
        1608: 'Bypass detected',
        1700: 'Communication port error',
        1701: 'Communication port restored',
        1702: 'Communication port reset',
        2000: 'Device restart external',
        2001: 'Device restart internal',
        2002: 'Revert to factory setting',
        2100: 'Error: NV memory',
        2101: 'Error: Program execution',
        2102: 'Error: Program storage',
        2103: 'Error: RAM failure',
        2104: 'Error: unexpected reset',
        2105: 'Error: Watchdog',
        2106: 'Error: Meter fatal error'
}

Calibration_code_Description = {
    0x00: '',
    0x01: 'NIK_AFE_CALIBR_ERROR_P1_REQUIRED',
    0x02: 'NIK_AFE_CALIBR_ERROR_INPUT_DATA',
    0x11: 'NIK_AFE_CALIBR_ERROR_POWER_CH1',
    0x12: 'NIK_AFE_CALIBR_ERROR_POWER_CH2',
    0x13: 'NIK_AFE_CALIBR_ERROR_POWER_CH3',
    0x14: 'NIK_AFE_CALIBR_ERROR_VTG_CH1',
    0x15: 'NIK_AFE_CALIBR_ERROR_VTG_CH2',
    0x16: 'NIK_AFE_CALIBR_ERROR_VTG_CH3',
    0x17: 'NIK_AFE_CALIBR_ERROR_CUR_CH1',
    0x18: 'NIK_AFE_CALIBR_ERROR_CUR_CH2',
    0x19: 'NIK_AFE_CALIBR_ERROR_CUR_CH3',
    0x20: 'NIK_AFE_CALIBR_ERROR_PF_CH1',
    0x21: 'NIK_AFE_CALIBR_ERROR_PF_CH2',
    0x22: 'NIK_AFE_CALIBR_ERROR_PF_CH3'
}

Calibration_status_Description = {
    0: 'NONE',
    1: 'PROCCESS',
    2: 'FINISHED',
    3: 'ERROR',
    4: 'LOCKED'
}

simple_object = (str, int, datetime.datetime, dict)
gx_object = (GXDLMSActivityCalendar, GXDLMSCaptureObject, GXDLMSClock, GXDLMSDayProfile, GXDLMSDayProfileAction,
             GXDateTime, GXDLMSDemandRegister, GXDLMSRegister, GXDLMSSeasonProfile, GXDLMSSpecialDay,
             GXDLMSSpecialDaysTable, GXDLMSWeekProfile, GXAttributeCollection, GXDLMSAttributeSettings,
             GXAuthentication, GXDLMSAttributeSettings, GXDLMSAttribute, GXManufacturer, GXManufacturerCollection,
             GXObisCode, GXObisCodeCollection, GXObisValueItem, GXObisValueItemCollection, GXServerAddress,
             HDLCAddressType, InactivityMode, StartProtocolType, GXDLMSData, GXDLMSExtendedRegister,
             GXDLMSProfileGeneric)


def parse(data, level=0):
    data_lst = data
    if level < 15:
        if isinstance(data, gx_object):
            data_lst = data.__dict__
            for key, value in data_lst.items():
                if key == 'parent':
                    if value is not None:
                        data_lst[key] = list()
                    continue
                if isinstance(value, gx_object) or isinstance(value, list):
                    data_lst[key] = parse(value, level=level+1)
        elif isinstance(data, (list, tuple)):
            if len(data) > 0:
                data_lst = list()
                for d in data:
                    data_lst.append(parse(d, level=level+1))
    level -= 1
    return data_lst


def parse_result(res, number, name, tests_res):
    """ Documentation for a method __parse_result. Added: 20.03.2020 22:45 vladimir.silin
    Parse test result and add to self.tests_res

    :param res: test result with 2 element (result, result_description)
    :type res: tuple
    :param number: str with test number
    :type number: str
    :param name: test name
    :type name: str
    :param tests_res: tests result
    :type tests_res: dict
    """

    result = res[0]
    result_descript = res[1]
    tests_res[number] = list()
    tests_res[number].append(f'{name}')
    if isinstance(result, bool):
        tests_res[number].append('SUCCESS' if result else 'FAIL')
    elif isinstance(result, str):
        tests_res[number].append(result)
    tests_res[number].append(result_descript)
    mess = ('info', f'TEST# {number}.{name}, result: {result}, result description: {result_descript}')
    return tests_res, mess


def read_meter_info(dlms):
    """
    The method reads data from the meter.

    :return: meter info
    :rtype: dict
    """
    metrology_name = {
        "EM01": {"TYPE":    "BL", "PHASES": "1P"},
        "EM02": {"TYPE":    "BL", "PHASES": "1P"},
        "EM03": {"TYPE": "VANGO", "PHASES": "1P"},
        "EM0A": {"TYPE": "VANGO", "PHASES": "1P"},
        "EM36": {"TYPE":    "BL", "PHASES": "3P"},
        "EM41": {"TYPE":   "ADE", "PHASES": "1P"},
        "EM42": {"TYPE":    "BL", "PHASES": "1P"},
        "EM43": {"TYPE":    "BL", "PHASES": "1P"},
        "EM44": {"TYPE": "VANGO", "PHASES": "1P"},
        "EM51": {"TYPE":   "ADE_1point", "PHASES": "3P"},
        "EM52": {"TYPE":   "ADE_1point", "PHASES": "3P"},
        "EM5A": {"TYPE":   "ADE_1point", "PHASES": "3P"},
        "EM71": {"TYPE":   "ADE_1point", "PHASES": "3P"},
        "EM7A": {"TYPE":   "ADE_1point", "PHASES": "3P"},
        "EMA2": {"TYPE":    "BL", "PHASES": "3P"},
        "EMA3": {"TYPE": "VANGO", "PHASES": "3P"}
    }

    meter_type = 'N/A'
    meter_sn = 'N/A'
    board_sn = 'N/A'
    try:
        meter_type = dlms.get(obis=OBIS_DEVICE_TYPE, attribute=2)
        if meter_type is not None:
            meter_type = meter_type.decode()
        meter_sn = dlms.get(obis=OBIS_TRILLIANT_SN, attribute=2)
        if meter_sn is not None:
            meter_sn = meter_sn.decode()
        board_sn = dlms.get(obis=OBIS_BOARD_SN, attribute=2)
        if board_sn is not None:
            board_sn = board_sn.decode()
    except Exception as exc:
        print(f'Check meter parametrization: {exc}')
    meter_fv = dlms.read_firmware_version()
    try:
        metrology_param = metrology_name[meter_fv[:4]]
    except KeyError:
        raise Exception(f'Need check firmware version, current firmware version {meter_fv}')
    info_keys = 'Meter type', 'Serial number', 'Firmware version', 'Metrology MCU', 'PCB board number'
    info_values = meter_type or 'N/A', meter_sn or 'N/A', meter_fv, metrology_param['TYPE'], board_sn or 'N/A'
    meter_info = {key: value for key, value in zip(info_keys, info_values)}
    return meter_info


# def create_send_report(report_name, tests_res, e_mail, meter_info, tests_algorithm=None):
#     """ Reporting in Excel and sending by mail (if mail is specified in the configuration file)"""
#     report = ExcelReport()
#     result = False
#     error_log = ""
#     # meter_info = read_meter_info(dlms=dlms)
#     if report.create_report(report_name, meter_info, tests_res, tests_algorithm):
#         try:
#             if e_mail is not None:
#                 subject_to = f'{report_name} test report'
#                 text = f'Report performed {datetime.datetime.now().strftime("%d.%m.%Y %H_%M_%S")}'
#                 send_email(e_mail, subject_to, text, report.report_name)
#             result = True
#         except Exception as e:
#             error_log = str(e)
#     else:
#         error_log = report.error
#     return result, error_log


def send_report_to_bd(data, debug=False):
    import requests
    import json

    ddd = json.dumps(data)
    if debug:
        requests.post("http://127.0.0.1:8000/qa/test_progress", data=ddd)
    else:
        requests.post("http://emmet.nikel.loc/qa/test_progress", data=ddd)


def _set_datetime(value):
    """ Documentation for a method __set_datetime. Added: 07.04.20 13:36 volodymyr.tyshchenko
    set datetime in GXDatetime with skip

    :param value: date and time to det
    :type value: datetime, GXDateTime

    :return: value in GXDatetime
    :rtype: GXDateTime
    """
    if isinstance(value, datetime.datetime):
        result = GXDateTime(value=value)
    # isinstance(value, GXDateTime)
    else:
        result = value
    result.skip = DateTimeSkips.DEVITATION
    return result

def add_to_dict(self, key):
    """ Documentation for a method add_to_dict. Added: 19.10.2020 13:36 volodymyr.tyshchenko
    add to dictionary info by key

    :param self: test object with vars res_to_db and tests_res
    :type self: class
    :param key: test name
    :type key: string
    """
    self.res_to_db[key] = self.tests_res[key]
    self.res_to_db[key].append("")
    self.res_to_db[key].append(self.start_time)
    self.res_to_db[key].append(self.stop_time)
    self.res_to_db[key].append("")


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
        self.dlms.reader.log_file_name = f"{self.log_file_name}_all_{test_number}.txt"
        self.dlms.reader.log_file_new = True
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


def get_len(data):
    """ Documentation for a method get_len. Added: 02.11.2020 11:22 volodymyr.tyshchenko
    get length by type

    :param data: param type
    :type data: DataType

    :return: length
    :rtype: int
    """
    length = 0
    # DataType.BOOLEAN = 0x03, DataType.INT8 = 0x0F, DataType.UINT8 = 0x11, DataType.ENUM = 0x16
    if data in [DataType.BOOLEAN, DataType.INT8, DataType.UINT8, DataType.ENUM]:
        length = 1
    # DataType.INT16 = 0x10, DataType.UINT16 = 0x12
    elif data in [DataType.INT16, DataType.UINT16]:
        length = 2
    # DataType.INT32 = 0x05, DataType.UINT32 = 0x06, DataType.FLOAT32 = 0x17, DataType.TIME = 0x1b
    elif data in [DataType.INT32, DataType.UINT32, DataType.FLOAT32, DataType.TIME]:
        length = 4
    # DataType.INT64 = 0x14, DataType.UINT64 = 0x15, DataType.FLOAT64 = 0x18
    elif data in [DataType.INT64, DataType.UINT64, DataType.FLOAT64]:
        length = 8
    # DataType.DATETIME = 0x19
    elif data in [DataType.DATETIME]:
        length = 12
    # DataType.DATE = 0x1a
    elif data in [DataType.DATE]:
        length = 5
    # DataType.OCTET_STRING = 0x09
    elif data in [DataType.OCTET_STRING]:
        length = 0
    return length


if __name__ == '__main__':
    import serial

    from DLMS import Dlms
    from component.calmet_lib.calmet import Calmet
    from tests.DLMS.calmet_tester import CalmetTester

    drv = serial.Serial()
    drv.port = 'COM16'
    drv.baudrate = 57600
    drv.open()
    tester = Dlms()
    calmet_class = Calmet(driver=drv)
    params1 = {"calmet": calmet_class, "dlms": tester, "e_mail": ""}
    calmet_tester = CalmetTester(**params1)
    calmet_tester.set_point(voltage=220, current=5)
    calmet_tester.power_on(enable_channels=(0, 1, 1, 0, 1, 1))
