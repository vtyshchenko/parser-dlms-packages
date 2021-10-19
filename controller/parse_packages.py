from component.gurux_dlms.enums.DataType import DataType
from component.gurux_dlms.enums import RequestTypes, Command

from component.gurux_dlms.GXByteBuffer import GXByteBuffer
from component.gurux_dlms.GXReplyData import GXReplyData
from component.gurux_dlms.GXDLMSSettings import GXDLMSSettings
from component.gurux_dlms.GXDLMS import GXDLMS

from component.gurux_dlms.internal._GXCommon import _GXCommon
from component.gurux_dlms.internal._GXDataInfo import _GXDataInfo


class ParsePackage:
    def __init__(self, package=None):
        self.package = package
        self.package_length = len(self.package) - 2 if package is not None else 0

        self.dlms = GXDLMS()

        # head
        self.head = None
        self.address_from = 0
        self.address_to = 0
        self.number = 0
        self.crc_head = 0

        # body
        self.body = None
        self.body_dict = {}
        self.body_length = 0
        self.type_ = 0
        self.type_name = None
        self.type_command = Command.NONE
        self.more_data = RequestTypes.NONE
        self.pack_type = 0
        self.is_last = 0
        self.frame_number = 0
        self.object_type = 0
        self.crc_body = 0

        self.position = 0
        self.data_packages = dict()
        self.data_dict = dict()

    def get_byte_from_package(self):
        self.position += 1
        return self.package[self.position] if self.position <= len(self.package) else None

    def _get_address(self):
        """ Documentation for a method _get_address. Added: 29.09.21 23:59 volodymyr.tyshchenko

        :return address list and next element index in data
        :rtype tuple
        """
        address = list()
        data = 0
        while bin(data)[-1] == '0':
            data = self.get_byte_from_package()
            address.append(data)
        return address

    def parse_package(self):
        """ Documentation for a method parse_package. Added: 04.10.2021 11:17 volodymyr.tyshchenko
        """
        if self.package is None:
            raise "package is not set"

        # head_len =  5 + addr_len
        self.parse_head()
        self.head = self.package[1:self.position+1]
        self.body = self.package[self.position+1:-1]
        # body_len = package_len - 2 - head_len
        self.body_length = len(self.body)

        b2 = int.from_bytes(self.body[-2], byteorder='big', signed=False) if isinstance(self.body[-2], bytes) \
            else self.body[-2]
        b1 = int.from_bytes(self.body[-1], byteorder='big', signed=False) if isinstance(self.body[-1], bytes) \
            else self.body[-1]
        self.crc_body = b2 << 8 + b1
        self.parse_body()

    def parse_head(self):
        # TX:  7E A0 1C 02 21 05 32 85 B8
        # RX:  7E A0 11 05 02 21 52 DA 58
        self.position = 1                                                   # 7E A0
        self.package_length = self.get_byte_from_package()               # 11           1C
        self.address_from = self._get_address()                          # 05           02 21
        self.address_to = self._get_address()                            # 02 21        05
        self.number = self.get_byte_from_package()                       # 52           32
        crc_high = self.get_byte_from_package()                          # DA           85
        crc_low = self.get_byte_from_package()                           # 58           B8
        self.crc_head = (crc_high << 8) + crc_low

    def parse_body(self):
        # gurux parse
        if self.package is None:
            raise "package is not set"
        if self.body is None:
            raise "package body is not set"
        LLC_SEND_BYTES = bytearray([0xE6, 0xE6, 0x00])
        LLC_REPLY_BYTES = bytearray([0xE6, 0xE7, 0x00])
        self.position += 2                                                # E6
        self.type_ = self.get_byte_from_package()                         # E7
        self.type_name = "req" if self.type_ == 0xE6 else "res"
        self.position += 1                                                # 00
        self.type_command = self.get_byte_from_package()                  # C5
        self.more_data = self.get_byte_from_package()                     # 01
        self.pack_type = self.get_byte_from_package()                     # C1
        self.is_last = self.get_byte_from_package()                       # 00
        self.body_dict["body_value"] = self.body
        self.position += 1

        # req -> res
        # TX -> RX
        # C0 -> C4
        # C1 -> C5
        # C2 -> C6
        # C3 -> C7

        self.body_dict["result"] = self.body[self.position:-3]
        self.body_dict["cs"] = (self.body[-3] << 8) + self.body[-2]
        reply = _GXDataInfo()
        settings = GXDLMSSettings(False)
        if self.type_name == "res":
            if self.pack_type == Command.GET_RESPONSE:
                # 7E A0 13 05 02 21 52 52 4E E6 E7 00 C4 01 C1 00 16 00 13 00 7E
                # 7E A0 13 05 02 21 74 66 0A E6 E7 00 C4 01 C1 00 11 01 92 5C 7E
                # 7E A0 16 05 02 21 96 2E E8 E6 E7 00 C4 01 C1 00 05 00 00 03 E8 9F 44 7E
                # 7E A0 1F 05 02 21 52 62 39 E6 E7 00 C4 01 C1 00 09 0C FF FF FF FF 06 00 00 00 FF 80 00 00 2E 57 7E
                # 7E A0 16 05 02 21 74 32 2C E6 E7 00 C4 01 C1 00 06 00 00 00 00 7D 18 7E

                # 7E A0 93 05 02 21 1E 6F 4C E6 E7 00 C4 02 C1 00 00 00 00 B7 00 7C 03 09 0C 07 E7 08 1F 04 00 00 00 00 00 00 00 11 07 06 04 1F 08 E7 02 03 09 0C 07 E7 08 1F 04 17 00 00 00 00 00 00 11 07 06 04 1F 08 E7 02 03 09 0C 07 E7 09 01 05 00 00 00 00 00 00 00 11 07 06 05 01 09 E7 02 03 09 0C 07 E7 09 01 05 17 00 00 00 00 00 00 11 07 06 05 01 09 E7 02 03 09 0C 07 E7 09 02 06 00 00 00 00 00 00 00 11 07 06 06 02 09 E7 02 03 09 0C 07 E7 09 02 06 17 AC 39 7E
                # 7E A0 93 05 02 21 30 13 84 E6 E7 00 C4 02 C1 00 00 00 00 B8 00 7C 00 00 00 00 00 00 11 07 06 06 02 09 E7 02 03 09 0C 07 E7 09 03 07 00 00 00 00 00 00 00 11 07 06 07 03 09 E7 02 03 09 0C 07 E7 09 03 07 17 00 00 00 00 00 00 11 07 06 07 03 09 E7 02 03 09 0C 07 E7 09 04 01 00 00 00 00 00 00 00 11 07 06 01 04 09 E7 02 03 09 0C 07 E7 09 04 01 17 00 00 00 00 00 00 11 07 06 01 04 09 E7 02 03 09 0C 07 E7 09 05 02 00 00 00 00 00 00 00 11 07 06 B8 BC 7E
                # 7E A0 60 05 02 21 52 6D 46 E6 E7 00 C4 02 C1 01 00 00 00 B9 00 49 02 05 09 E7 02 03 09 0C 07 E7 09 05 02 17 00 00 00 00 00 00 11 07 06 02 05 09 E7 02 03 09 0C 07 E7 09 06 03 00 00 00 00 00 00 00 11 07 06 03 06 09 E7 02 03 09 0C 07 E7 09 06 03 01 00 00 00 00 00 00 11 07 06 03 06 09 E7 CF DD 7E

                # self.data_dict[key]["result"] = pack[i + 3]
                #                 self.data_dict[key]["type"] = {"value": pack[i + 4], "name": self.data_type[pack[i + 4]]}
                #                 data = list()
                #                 for j in range(i + 5, len(pack) - 3):
                #                     data.append(pack[j])
                #                 self.data_dict[key]["value"] = data
                if self.more_data == RequestTypes.FRAME:
                    # прочитати всі пакети (від №1 до self.is_last == 1)
                    # вийняти всі дані і з'єднати
                    # розпарсити дані в self.body_dict["body_value"]
                    while self.is_last == 0:
                        self.is_last = 1
                    pass
                elif self.more_data == RequestTypes.DATABLOCK:
                    while self.position < self.body_length:
                        self.body_dict["body_value"] = _GXCommon.getData(settings=settings, data=self.body, info=reply)
            elif self.pack_type == Command.SET_RESPONSE:
                # 7E A0 11 05 02 21 52 DA 58
                # E6 E7 00 C5 01 C1
                # 00
                # 50 89
                # 7E
                self.body_dict["body_value"] = self.package[self.position-3]
            elif self.pack_type == Command.METHOD_RESPONSE:
                # 7E A0 18 05 02 21 B8 EA 41 E6 E7 00 C7 01 C1 00
                # 01 00 05 00 00 9C 40
                # 34 3E
                # 7E
                while self.position < self.body_length:
                    self.body_dict["body_value"] = _GXCommon.getData(settings=settings, data=self.body, info=reply)

        # if self.type_name == "req":
        else:

            if self.pack_type == Command.GET_REQUEST:
                # 7E A0 1A 02 21 05 FE 7D 8F E6 E6 00 C0 01 C1 00 70 00 00 13 0A 02 FF 01 00 34 9E 7E
                # 7E A0 1A 02 21 05 32 1D 83 E6 E6 00 C0 01 C1 00 70 00 00 13 0A 02 FF 0B 00 44 63 7E
                # 7E A0 1A 02 21 05 54 2D 85 E6 E6 00 C0 01 C1 00 03 01 00 02 07 00 FF 02 00 B3 0E 7E
                # 7E A0 1A 02 21 05 10 0D 81 E6 E6 00 C0 01 C1 00 70 00 00 13 0A 02 FF 02 00 5C B4 7E
                # 7E A0 1A 02 21 05 32 1D 83 E6 E6 00 C0 01 C1 00 70 00 00 13 0A 02 FF 03 00 84 AD 7E
                if self.more_data == RequestTypes.FRAME:
                    # 7E A0 14 02 21 05 32 A5 E2 E6 E6 00 C0 02 C1 00 00 00 B8 1B 96 7E
                    self.body_dict["package_number"] = self.get_byte_from_package() << 8 << 8 << 8 + \
                                                       self.get_byte_from_package() << 8 << 8 + \
                                                       self.get_byte_from_package() << 8 + \
                                                       self.get_byte_from_package()
                elif self.more_data == RequestTypes.DATABLOCK:
                    self.body_dict["body_value"] = dict()
                    self.body_dict["body_value"]["type"] = self.get_byte_from_package()
                    self.body_dict["body_value"]["obis"] = ""
                    for i in range(6):
                        self.body_dict["body_value"]["obis"] += f"{self.get_byte_from_package()}"
                        if i < 5:
                            self.body_dict["body_value"]["obis"] += "."
            elif self.pack_type == Command.SET_REQUEST:
                # 7E A0 1C 02 21 05 32 85 B8 E6 E6 00 C1 01 C1 00 70 00 00 13 0A 02 FF 03 00 16 00 6F 13 7E
                if self.body_length == 1:
                    self.body_dict["body_value"] = self.get_byte_from_package()
                else:
                    self.body_dict["body_value"] = dict()
                    self.body_dict["body_value"]["type"] = self.get_byte_from_package()
                    self.body_dict["body_value"]["obis"] = ""
                    for i in range(6):
                        self.body_dict["body_value"]["obis"] += f"{self.get_byte_from_package()}"
                        if i < 5:
                            self.body_dict["body_value"]["obis"] += "."
                    self.body_dict["body_value"]["data"] = ""
                    while self.position < self.package_length - 3:
                        self.body_dict["body_value"]["obis"] += f"{self.get_byte_from_package()}"
                        if self.position < self.package_length - 4:
                            self.body_dict["body_value"]["obis"] += " "

            elif self.pack_type == Command.EVENT_NOTIFICATION:
                pass
            elif self.pack_type == Command.METHOD_REQUEST:
                # 7E A0 1F 02 21 05 98 19 AF
                # E6 E6 00 C3 01 C1 00
                # 70 00 00 13 0A 02 FF 02 01 05 00 03 0D 40
                # 0A E0
                # 7E

                pass
            else:
                self.position += 2
                self.object_type = self.package[self.position]

    # GXDLMS.getHdlcFrame(settings, id_, None)

    def parse_data_package(self, obj, key):
        res = True
        reply = GXByteBuffer(obj)
        data = GXReplyData()
        self.data_dict[key]["Length"] = self.package_length

        self.data_dict[key]["addr_from"] = self.address_from
        self.data_dict[key]["addr_to"] = self.address_to
        self.data_dict[key]["data"]["data"] = data
        notify = GXReplyData()
        settings = GXDLMSSettings(isServer=True)
        settings.skipFrameCheck = True
        try:
            self.dlms.getData(settings=settings, reply=reply, data=data, notify=notify)
            pack = GXByteBuffer(obj)
            # pack = pack[:pack.getCapacity()-10]
            self.package = reply
            self.parse_package()

            # data_item = self.GXDLMSClient.parseObjects(data=GXByteBuffer(self.parse_package.body))
            # pack = pack.array()
        except Exception as exc:
            res = False
            print(f"exc = {exc}")
        return res

    def parse_packages(self):
        self.data_dict = dict()
        for key in sorted(list(self.data_packages)):
            self.package = self.data_packages[key]
            self.parse_package()

            self.data_dict[key] = dict()
            self.data_dict[key]["data"] = dict()
            self.data_dict[key]["data"]["package"] = self.package
            # res = self.parse_data_package(obj=self.package, key=key)

    # def parse_dlms(self):
    #     """ Documentation for a method parseDLMS. Added: 29.09.21 20:52 volodymyr.tyshchenko
    #     parse DLMS packages
    #     """
    #     try:
    #         for key, obj in self.data_dict.items():
    #             is_c4_last = True
    #             pack = GXByteBuffer(obj["data"]["package"]).array()
    #             i = self.parse_head(pack=pack, key=key)
    #             if pack[i] == 0xC5:
    #                 self.data_dict[key]["result"] = pack[i + 3]
    #             elif pack[i] == 0xC4:
    #                 self.data_dict[key]["result"] = pack[i + 3]
    #                 self.data_dict[key]["type"] = {"value": pack[i + 4], "name": self.data_type[pack[i + 4]]}
    #                 data = list()
    #                 for j in range(i + 5, len(pack) - 3):
    #                     data.append(pack[j])
    #                 self.data_dict[key]["value"] = data
    #             elif pack[i] == 0xC0:
    #                 if key == 480:
    #                     print("")
    #                 if pack[i + 1] == 0x01:
    #                     self.data_dict[key]["type"] = {
    #                         "value": pack[i + 4], "name": self.object_type[pack[i + 4]]
    #                         }
    #                     obis = f"{pack[i + 5]}.{pack[i + 6]}.{pack[i + 7]}.{pack[i + 8]}.{pack[i + 9]}.{pack[i + 10]}"
    #                     self.data_dict[key]["obis"] = obis
    #                     self.data_dict[key]["attribute"] = pack[i + 11]
    #                 elif pack[i + 1] == 0x02:
    #                     self.data_dict[key]["number"] = {
    #                         "data":  [pack[i + 3], pack[i + 4], pack[i + 5], pack[i + 6]],
    #                         "value": (pack[i + 3] >> 3) + (pack[i + 4] >> 2) + (pack[i + 5] >> 1) + pack[i + 6]
    #                         }
    #             # elif pack[i + 6] == 0xC1:
    #             #     is_c1_last = False
    #     except Exception as exc:
    #         print(f"{exc}")
