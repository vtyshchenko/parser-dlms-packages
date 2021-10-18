# from component.gurux_dlms.enums.DataType import DataType
# from component.gurux_dlms.GXByteBuffer import GXByteBuffer
from component.gurux_dlms.internal._GXCommon import _GXCommon
from component.gurux_dlms.internal._GXDataInfo import _GXDataInfo

from component.gurux_dlms.GXDLMSSettings import GXDLMSSettings
from component.gurux_dlms.enums import RequestTypes, Command


class ParsePackage:
    def __init__(self, package=None):
        self.package = package
        self.package_length = len(self.package) - 2 if package is not None else 0

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

    def get_byte_from_package(self):
        self.position += 1
        return self.package[self.position] if self.position <= self.package_length else None

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
        # ------------------------------------------------------------------------
        # TX: 22:07:28	7E A0 1A 02 21 05 FE 7D 8F E6 E6 00 C0 01 C1 00 03 01 00 02 07 00 FF 02 00 B3 0E 7E
        # RX: 22:07:28	7E A0 16 05 02 21 1E 6E E0 E6 E7 00 C4 01 C1 00 06 00 00 00 00 7D 18 7E
        # TX: 22:07:28	7E A0 71 02 21 05 10 52 67 E6 E6 00 C0 01 C1 00 07 01 00 63 01 00 FF 02 01 01 02 04 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 02 12 00 00 09 0C 07 E7 01 0D 05 15 00 00 00 80 00 00 09 0C 07 E7 09 06 03 00 00 00 00 80 00 00 01 02 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 02 12 00 00 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 04 12 00 00 9F 78 7E
        # RX: 22:07:31	7E A0 93 05 02 21 30 13 84 E6 E7 00 C4 02 C1 00 00 00 00 01 00 7C 01 82 03 D7 02 02 09 0C 07 E7 01 0D 05 13 00 00 00 00 00 00 11 07 02 02 09 0C 07 E7 01 0D 05 14 00 00 00 00 00 00 11 07 02 02 09 0C 07 E7 01 0D 05 15 00 00 00 00 00 00 11 07 02 02 09 0C 07 E7 01 0D 05 16 00 00 00 00 00 00 11 07 02 02 09 0C 07 E7 01 0D 05 17 00 00 00 00 00 00 11 07 02 02 09 0C 07 E7 01 0E 06 00 00 00 00 00 00 00 11 07 02 02 09 0C 07 E7 01 0E 06 01 00 00 0F 0A 7E
        # ...
        # TX: 22:09:28	7E A0 14 02 21 05 10 B5 E0 E6 E6 00 C0 02 C1 00 00 00 B7 EC 6E 7E
        # RX: 22:09:28	7E A0 93 05 02 21 30 13 84 E6 E7 00 C4 02 C1 00 00 00 00 B8 00 7C 00 00 00 00 00 00 11 07 06 06 02 09 E7 02 03 09 0C 07 E7 09 03 07 00 00 00 00 00 00 00 11 07 06 07 03 09 E7 02 03 09 0C 07 E7 09 03 07 17 00 00 00 00 00 00 11 07 06 07 03 09 E7 02 03 09 0C 07 E7 09 04 01 00 00 00 00 00 00 00 11 07 06 01 04 09 E7 02 03 09 0C 07 E7 09 04 01 17 00 00 00 00 00 00 11 07 06 01 04 09 E7 02 03 09 0C 07 E7 09 05 02 00 00 00 00 00 00 00 11 07 06 B8 BC 7E
        # TX: 22:09:28	7E A0 14 02 21 05 32 A5 E2 E6 E6 00 C0 02 C1 00 00 00 B8 1B 96 7E
        # RX: 22:09:28	7E A0 60 05 02 21 52 6D 46 E6 E7 00 C4 02 C1 01 00 00 00 B9 00 49 02 05 09 E7 02 03 09 0C 07 E7 09 05 02 17 00 00 00 00 00 00 11 07 06 02 05 09 E7 02 03 09 0C 07 E7 09 06 03 00 00 00 00 00 00 00 11 07 06 03 06 09 E7 02 03 09 0C 07 E7 09 06 03 01 00 00 00 00 00 00 11 07 06 03 06 09 E7 CF DD 7E
        # TX: 22:09:43	7E A0 1A 02 21 05 54 2D 85 E6 E6 00 C0 01 C1 00 03 01 00 02 07 00 FF 02 00 B3 0E 7E
        # RX: 22:09:43	7E A0 16 05 02 21 74 32 2C E6 E7 00 C4 01 C1 00 06 00 00 00 00 7D 18 7E
        # ------------------------------------------------------------------------
        if self.package is None:
            raise "package is not set"
        self.parse_head()
        self.head = self.package[1:self.position+1]
        self.body = self.package[self.position+1:-1]
        self.body_length = len(self.body)
        self.crc_body = int.from_bytes(self.body[-2], byteorder='big', signed=False) << 8 \
            + int.from_bytes(self.body[-1], byteorder='big', signed=False)
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
