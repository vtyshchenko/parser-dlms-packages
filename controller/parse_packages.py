# from component.gurux_dlms.enums.DataType import DataType
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
        self.parse_head()
        self.head = self.package[1:self.position+1]
        self.body = self.package[self.position+1:-1]
        self.body_length = len(self.body)

        b2 = int.from_bytes(self.body[-2], byteorder='big', signed=False) if isinstance(self.body[-2], bytes) \
            else self.body[-2]
        b1 = int.from_bytes(self.body[-1], byteorder='big', signed=False) if isinstance(self.body[-1], bytes) \
            else self.body[-1]
        self.crc_body = b2 << 8 + b1
        self.parse_body()

    def parse_head(self):
        # TX:  7E A0 1C 02 21 05 32 85 B8 E6 E6 00 C1 01 C1 00 70 00 00 13 0A 02 FF 03 00 16 00 6F 13 7E
        # RX:  7E A0 11 05 02 21 52 DA 58 E6 E7 00 C5 01 C1 00 50 89 7E
        self.position = 1                                                   # 7E A0
        self.package_length = self.get_byte_from_package()               # 11           1C
        self.address_from = self._get_address()                          # 05           02 21
        self.address_to = self._get_address()                            # 02 21        05
        self.number = self.get_byte_from_package()                       # 52           32
        crc_high = self.get_byte_from_package()                          # DA           85
        crc_low = self.get_byte_from_package()                           # 58           B8
        self.crc_head = (crc_high << 8) + crc_low

        # self.data_dict[key]["Length"] = pack[2]
        #
        # self.data_dict[key]["addr_from"], i = self.get_addr(idx=3, data=pack)
        # self.data_dict[key]["addr_to"], i = self.get_addr(idx=i, data=pack)
        # self.data_dict[key]["next"] = pack[i]
        #
        # self.data_dict[key]["in_out"] = {"value": pack[10], "direction": "out" if pack[10] == 0xE6 else "in"}
        # self.data_dict[key]["pack_type"] = pack[i + 6]

    def parse_body(self):
        # gurux parse
        if self.package is None:
            raise "package is not set"
        if self.body is None:
            raise "package body is not set"

        self.position += 2                                                   # E6
        self.type_ = self.get_byte_from_package()                         # E7
        self.type_name = "req" if self.type_ == 0xE6 else "res"
        self.position += 1                                                   # 00
        self.type_command = self.get_byte_from_package()                  # C5
        self.more_data = self.get_byte_from_package()                     # 01
        self.pack_type = self.get_byte_from_package()                     # C1
        self.is_last = self.get_byte_from_package()                       # 00

        if self.type_name == "res":
            if self.pack_type == 0xC1:
                if self.body_length == 1:
                    self.body_dict["value"] = self.body[self.position:-2]
                else:
                    reply = _GXDataInfo()
                    settings = GXDLMSSettings(False)
                    while self.position < self.body_length:
                        self.body_dict["body_value"] = _GXCommon.getData(settings=settings, data=self.body, info=reply)
        else:
            self.body_dict["body_value"] = self.body

        if self.type_name == "req":
            self.position += 2
            self.object_type = self.package[self.position]

    # def get_value(self):
    #     """ Documentation for a method get_value. Added: 04.10.2021 12:27 volodymyr.tyshchenko
    #     """
    #     type_ = self.body[self.position]
    #     if type_ == DataType.NONE:  # 0x00
    #         pass
    #     elif type_ == DataType.ARRAY:  # 0x01
    #         pass
    #     elif type_ == DataType.STRUCTURE:  # 0x02
    #         pass
    #     elif type_ == DataType.BOOLEAN:  # 0x03
    #         pass
    #     elif type_ == DataType.BITSTRING:  # 0x04
    #         pass
    #     elif type_ == DataType.INT32:  # 0x05
    #         val = self.body.getInt32(index=self.position)
    #     elif type_ == DataType.UINT32:  # 0x06
    #         val = self.body.getUInt32(index=self.position)
    #     elif type_ == DataType.OCTET_STRING:  # 0x09
    #         pass
    #     elif type_ == DataType.STRING:  # 0x0A
    #         count = self.body[self.position + 1]
    #         val = self.body.getString(index=self.position, count=count)
    #     elif type_ == DataType.STRING_UTF8:  # 0x0C
    #         pass
    #     elif type_ == DataType.BCD:  # 0x0D
    #         pass
    #     elif type_ == DataType.INT8:  # 0x0F
    #         val = self.body.getInt8(index=self.position)
    #     elif type_ == DataType.INT16:  # 0x10
    #         val = self.body.getUInt16(index=self.position)
    #     elif type_ == DataType.UINT8:  # 0x11
    #         val = self.body.getUInt8(index=self.position)
    #     elif type_ == DataType.UINT16:  # 0x12
    #         val = self.body.getUInt16(index=self.position)
    #     elif type_ == DataType.COMPACT_ARRAY:  # 0x13
    #         pass
    #     elif type_ == DataType.INT64:  # 0x14
    #         val = self.body.getInt64(index=self.position)
    #     elif type_ == DataType.UINT64:  # 0x15
    #         val = self.body.getUInt64(index=self.position)
    #     elif type_ == DataType.ENUM:  # 0x16
    #         pass
    #     elif type_ == DataType.FLOAT32:  # 0x17
    #         pass
    #     elif type_ == DataType.FLOAT64:  # 0x18
    #         pass
    #     elif type_ == DataType.DATETIME:  # 0x19
    #         pass
    #     elif type_ == DataType.DATE:  # 0x1a
    #         pass
    #     elif type_ == DataType.TIME:  # 0x1b
    #         pass
    #     return ''

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
            obj = self.data_packages[key]
            self.data_dict[key] = dict()
            self.data_dict[key]["data"] = dict()
            self.data_dict[key]["data"]["package"] = obj
            res = self.parse_data_package(obj=obj, key=key)

            # print(f"key = {key}\nobj = {obj}\nexc = {exc}")
            pack = GXByteBuffer(obj).array()
            if not res:
                continue
            idx = 0
            for j in range(len(pack)):
                if pack[j] == 0xE6 and (pack[j + 1] == 0xE6 or pack[j + 1] == 0xE7):
                    idx = j + 3
                    break
            if len(pack) - 2 == pack[2]:
                body_idx = (idx + 4) * 3
                if pack[idx] == 0xC0:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                elif pack[idx] == 0xC1:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                elif pack[idx] == 0xC2:
                    pass
                elif pack[idx] == 0xC3:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                elif pack[idx] == 0xC4:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                    if pack[idx+1] == 0x02:
                        pass
                elif pack[idx] == 0xC5:
                    self.data_dict[key]["data"]["result"] = obj[body_idx:body_idx+3]
                    self.data_dict[key]["data"]["body"] = obj[body_idx:body_idx+3]
                elif pack[idx] == 0xC6:
                    pass
                elif pack[idx] == 0xC7:
                    self.data_dict[key]["data"]["result"] = obj[body_idx:body_idx+3]
                    self.data_dict[key]["data"]["body"] = obj[body_idx:body_idx+3]
            else:
                pass

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
