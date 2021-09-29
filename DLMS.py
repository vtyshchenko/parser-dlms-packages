from os import mkdir
from os.path import abspath, join, exists, isfile

from component.gurux_common.io import BaudRate, Parity, StopBits
from component.gurux_dlms.enums import DataType, ObjectType, DateTimeSkips
from component.gurux_dlms.objects import GXDLMSData
from component.gurux_net import GXNet
from component.gurux_serial import GXSerial

from controller.GXDLMSReader import GXDLMSReader
from controller.GXSettings import GXSettings


class Dlms:

    def __init__(self, *args, **params):
        self.loger = None if 'loger' not in params.keys() else params['loger']
        self.ans_err = 0
        self.ans_data = None

        settings = GXSettings()
        try:
            #  Handle command line parameters.
            ret = settings.getParameters(*args)
            if ret != 0:
                return
            self.reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.iec)
        except Exception as exc:
            self.log('error', f'{exc}')
            return

    def log(self, level, mess):
        """ Documentation for a method log. Added: 26.02.2020 9:54 volodymyr.tyshchenko
        Logging message

        :param level: message level
        :type level: string
        :param mess: message
        :type mess: string
        """
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
        if self.loger is not None:
            self.loger.log(level_code[level.upper()], mess)

    def init_connection(self, def_baud, prop_baud):
        """ Documentation for a method init_connection. Added: 20.02.2020 16:02 vladimir.silin
        Initialize connection settings
        """
        res = True
        if isinstance(self.reader.media, GXSerial):
            self.reader.media.stopbits = StopBits.ONE
            if self.reader.iec:
                self.reader.media.baudRate = def_baud
                self.reader.media.dataBits = 7
                self.reader.media.parity = Parity.EVEN
            else:
                self.reader.media.baudRate = prop_baud
                self.reader.media.dataBits = 8
                self.reader.media.parity = Parity.NONE
        elif not isinstance(self.reader.media, GXNet):
            res = False
            self.log('error', 'Unknown media type.')
        return res

    def authoriz(self, def_baud=BaudRate.BAUD_RATE_300, prop_baud=BaudRate.BAUD_RATE_9600):
        """ Documentation for a method authoriz. Added: 20.02.2020 11:01 vladimir.silin
        SNRM + AARQ (connect and autorization)

        :return: authorization result
        :rtype: bool
        """
        res = False
        self.log('info', 'Trying authorization!')
        connect = self.init_connection(def_baud, prop_baud)
        if connect:
            try:
                self.reader.initializeConnection()
                self.log('info', 'Login was successful!')
                res = True
            except Exception as exc:
                self.log('info', f'Login FAIL: {exc}!')
        return res

    def discon(self):
        """ Documentation for a method discon. Added: 20.02.2020 11:03 vladimir.silin
        Sending <disconnect> command to device

        :return: disconnect result
        :rtype: bool
        """

        self.log('info', 'Disconnecting from device!')
        res = True
        try:
            self.reader.close()
            self.log('info', 'Ended. Goodbye!')
        except Exception as exc:
            res = False
            self.log('info', f'Disconnecting FAIL: {exc}!')
        return res

    def action(self, obis, method, data_type=18, data=0):
        """ Documentation for a method action. Added: 20.02.2020 10:46 vladimir.silin
        Send Action to the meter 
    
        :param obis: string obis separated with '.'
        :type obis: str
        :param method: method number to be executed
        :type method: int
        :param data_type: method data type, by default = 18 (UINT16)
        :type data_type: int
        :param data: method data, by default = 0
        :type data: int
    
        :return: Error code
        :rtype:  int
        """

        self.log('info', 'ACTION')
        obis = str(obis)
        method = int(method)
        # data = int(data)
        data_type = DataType(int(data_type))
        item = self.reader.client.objects.findByLN(ObjectType.NONE, obis)
        action = self.reader.client.method(item, method, data, data_type)
        ans_err = self.reader.readDLMSPacket(action)
        if ans_err == 0:
            self.log('info', f'ACTION SUCCESSFUL - obis: {obis}, attribute: {method}, data: {data}')
        else:
            self.log('error', f'ACTION FAIL - {ans_err}')
        return ans_err

    def set(self, obis, attribute, data_type, data, ignore=None):
        """ Documentation for a method set. Added: 20.02.2020 11:04 vladimir.silin
        Send SET Request to the meter

        :param obis: string obis separated with '.'
        :type obis: str
        :param attribute: attribute number to be set
        :type attribute: int
        :param data_type: data type to set
        :type data_type: int
        :param data: data to set
        :type data: int, datetime, str (depending on the set parameter)

        :return: operation error code (0 - no errors)
        :rtype: int
        """
        self.log('info', f"Trying SET obis: {obis}, attribute: {attribute}, data: {data}")
        obis = str(obis)
        attribute = int(attribute)
        item = self.reader.client.objects.findByLN(ObjectType.NONE, obis)
        item.setDataType(attribute, DataType(data_type))
        if data_type == DataType.DATETIME:
            if ignore == DateTimeSkips.DEVITATION:
                item.deviation = 0
        data = self.reader.client.updateValue(target=item, attributeIndex=attribute, value=data)
        mess = ""
        try:
            ans_err = self.reader.write(item=item, attributeIndex=attribute)
        except Exception as exc:
            ans_err = 2
            mess = f"{exc}"
        if ans_err == 0:
            self.log('info', f"SET SUCCESSFUL - obis: {obis}, attribute: {attribute}, data: {data}")
        else:
            self.log('error', f"SET FAIL - {ans_err},\nmess: '{mess}'")
        return ans_err

    def set_object(self, obis, attribute, item):
        """ Documentation for a method set. Added: 20.02.2020 11:04 vladimir.silin
        Send SET Request to the meter

        :param obis: string obis separated with '.'
        :type obis: str
        :param attribute: attribute number to be set
        :type attribute: int
        :param item: object to set
        :type item: object

        :return: operation error code (0 - no errors)
        :rtype: int
        """
        # self.log('info', f'Trying SET obis: {obis}, attribute: {attribute}, data: {item}')
        self.log('info', f'Trying SET obis: {obis}, attribute: {attribute}')
        obis = str(obis)
        attribute = int(attribute)
        ans_err = self.reader.write(item=item, attributeIndex=attribute)
        if ans_err == 0:
            self.log('info', f'SET SUCCESSFUL - obis: {obis}, attribute: {attribute}, data: {item}')
        else:
            self.log('error', f'SET FAIL - {ans_err}')
        return ans_err

    def get_object(self, obis: str):
        """ Documentation for a method get. Added: 20.02.2020 11:12 vladimir.silin
        Send GET Request to the meter

        :param obis: string obis separated with '.'
        :type obis: str

        :return: data
        :rtype: read object DataType (bool, bytearray or other)
        """

        self.log('info', f'GET Request - obis: {obis}')
        obis = str(obis)
        item = self.reader.client.objects.findByLN(ObjectType.NONE, obis)
        ans_data = dict()
        for attr in item.getAttributeIndexToRead(True):
            data = self.reader.read(item=item, attributeIndex=attr)
            self.log('info', f'GET Response - obis: {obis}, value: {data}')
            ans_data[f"{attr}"] = data
        return ans_data

    def get(self, obis: str, attribute: int):
        """ Documentation for a method get. Added: 20.02.2020 11:12 vladimir.silin
        Send GET Request to the meter

        :param obis: string obis separated with '.'
        :type obis: str
        :param attribute: attribute number to read
        :type attribute: int

        :return: data
        :rtype: read object DataType (bool, bytearray or other)
        """

        self.log('info', f'GET Request - obis: {obis}, attribute: {attribute}')
        obis = str(obis)
        item = self.reader.client.objects.findByLN(ObjectType.NONE, obis)
        if item is not None:
            ans_data = self.reader.read(item=item, attributeIndex=attribute)
        else:
            ans_data = None
        self.log('info', f'GET Response - obis: {obis}, attribute: {attribute}, value: {ans_data}')
        return ans_data

    def read_association(self):
        """ Documentation for a method read_association. Added: 20.02.2020 11:24 vladimir.silin
        Read associations from meter

        :return: read result
        :rtype: bool
        """
        res = True
        try:
            self.log('info', 'Read association')
            self.reader.getAssociationView()
            self.reader.readScalerAndUnits()
            self.reader.getProfileGenericColumns()
            self.reader.getReadOut()
            self.reader.getProfileGenerics()
            self.log('info', 'Read association complete')
        except Exception as exc:
            res = False
            self.log('error', f'Error read association: {exc}')
        return res

    def save_association(self, file=None):
        """ Documentation for a method save_association. Added: 20.02.2020 11:26 vladimir.silin
        Saving read associations from the meter to the directory 'associations'

        :param file: file name, by default = None. If file = None, associations will be save with name firmware version
        :type file: str

        :return: save result
        :rtype: bool
        """
        res = True
        try:
            self.log('info', 'Trying save association')
            file_path = join(abspath('.'), 'associations')
            if not exists(file_path):
                mkdir(file_path)
            file_name = file if file else self.read_firmware_version()
            self.reader.client.objects.save(join(file_path, file_name))
            self.log('info', 'Save association - OK!')
        except Exception as exc:
            res = False
            self.log('error', f'Error save association: {exc}')
        return res

    def load_association(self, file=None):
        """ Documentation for a method load_association. Added: 20.02.2020 11:36 vladimir.silin
        Download a saved association from the 'associations' directory

        :param file: file name, by default = None. If file = None, associations will be load with name firmware version
        :type file: str

        :return: load result
        :rtype: bool
        """

        res = True
        self.log('info', 'Trying load association')
        file_path = join(abspath('.'), 'associations')
        if file is None:
            file_name = join(file_path, self.read_firmware_version())
        else:
            file_name = join(file_path, file)
        if isfile(file_name):
            try:
                load_objects = self.reader.client.objects.load(file_name)
                for item in load_objects:
                    if str(item) not in str(self.reader.client.objects):
                        self.reader.client.objects.append(item)
            except FileNotFoundError as err:
                self.log('error', f'Error associations file: {err}')
                res = False
            self.log('info', 'Load association - OK!')
        else:
            self.log('info', f"Error associations file: '{file_name}' not exists!!!")
            res = False
        return res

    def read_firmware_version(self):
        """ Documentation for a method read_firmware_version. Added: 20.02.2020 11:42 vladimir.silin
        Reading the firmware version from the meter
    
        :return: firmware version
        :rtype: str
        """
        fw_item = GXDLMSData(ln='1.0.0.2.0.255')
        fw_item.description = 'Ch. 0 Active firmware identifier'
        if str(fw_item) not in str(self.reader.client.objects):
            self.reader.client.objects.append(fw_item)
        firmware = (self.reader.read(item=fw_item, attributeIndex=2)).decode()
        return firmware
