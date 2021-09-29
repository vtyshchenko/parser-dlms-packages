import traceback

# from component.gurux_common.io import Parity, StopBits, BaudRate
from component.gurux_dlms.enums import ObjectType
from component.gurux_net import GXNet
# from component.gurux_serial import GXSerial
from controller.interface import SerialInterface

from controller.GXSettings import GXSettings
from controller.GXDLMSReader import GXDLMSReader


class GuruxClient:
    def __init__(self, args):
        # args: the command line arguments
        self.settings = GXSettings()
        try:
            # //////////////////////////////////////
            #  Handle command line parameters.
            ret = self.settings.getParameters(args)
            if ret == 0:
                # //////////////////////////////////////
                #  Initialize connection settings.
                if isinstance(self.settings.media, SerialInterface):
                    self.settings.media.stopbits = 0
                    if self.settings.iec:
                        self.settings.media.baudrate = 300
                        self.settings.media.bytesize = 7
                        self.settings.media.parity = 1
                    else:
                        self.settings.media.baudrate = 9600
                        self.settings.media.bytesize = 8
                        self.settings.media.parity = 0
                elif not isinstance(self.settings.media, GXNet):
                    raise Exception("Unknown media type.")
            # //////////////////////////////////////
        except Exception:
            traceback.print_exc()
        return

    def __call__(self, *args, **kwargs):
        """ Documentation for a method __call__:. Added: 21.01.2020 16:15 volodymyr.tyshchenko

        """
        reader = None
        self.settings.media.open()
        try:
            reader = GXDLMSReader(self.settings.client, self.settings.media, self.settings.trace, self.settings.iec)
            if self.settings.readObjects:
                reader.initializeConnection()
                reader.getAssociationView()
                for k, v in self.settings.readObjects:
                    val = reader.read(self.settings.client.objects.findByLN(ObjectType.NONE, k), v)
                    reader.showValue(v, val)
            else:
                reader.readAll()
        except Exception:
            traceback.print_exc()
        finally:
            if reader:
                try:
                    reader.close()
                except Exception:
                    traceback.print_exc()
#         send = b'/?!\r\n'
# resp = b'/NIK5\\2 NIK 2104ARPx\r\n'
# send = b'\x06252\r\n'
# resp = b''
# 300
# 600
# 1200
# 2400
# 4800
# 9600
# 19200
# [b'', b'', b'', b'', b'',
# b'
# ~\xa0\x1f\x05\x02!s\xe9\t\x81\x80\x12\x05\x01\x90\x06\x01\x90\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\x0b\xc0~
# ', b'']
# def run():
# 	ser.baudrate = 300
# 	ser.bytesize = 7
# 	ser.parity = 'E'
# 	ser.stopbits = 1
# 	ser.port = 'COM3'
# 	ser.timeout = 5
# 	data = b"\x2F\x3F\x21\x0D\x0A"
# 	print(f"send = {data}")
# 	ser.write(data)
# 	resp = ser.read_until('\n')
# 	print(f"resp = {resp}")
#
# 	data = b'\x06\x32\x35\x32\x0D\x0A'
# 	print(f"send = {data}")
# 	ser.write(data)
# 	resp = ser.read_until('\n')
# 	print(f"resp = {resp}")
#
# 	time.sleep(2)
# 	resp = list()
# 	data=b'\x7E\xA0\x08\x02\x21\x05\x93\x56\x95\x7E'
# 	for baud in [300, 600, 1200, 2400, 4800, 9600, 19200]:
# 		ser.close()
# 		ser.bytesize = 8
# 		ser.parity = 'N'
# 		print(f"{baud}")
# 		ser.baudrate = baud
# 		ser.open()
# 		ser.write(data)
# 		resp.append(ser.read_until('\n'))
# 	print(f"{resp}")
#
# def get_resp(data):
#  	resp = list()
#  	for baud in [300, 600, 1200, 2400, 4800, 9600, 19200]:
#  		ser.close()
#  		print(f"{baud}\n")
#  		time.sleep(2)
#  		ser.baudrate = baud
#  		ser.open()
#  		ser.write(data)
#  		resp.append(ser.read_until('\n'))
#  	print(f"{resp}")
