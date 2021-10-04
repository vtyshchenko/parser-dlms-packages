from component.gurux_dlms.enums.DataType import DataType
from component.gurux_dlms.GXByteBuffer import GXByteBuffer
from component.gurux_dlms.internal._GXCommon import _GXCommon

from component.gurux_dlms.GXDLMSSettings import GXDLMSSettings
from component.gurux_dlms.internal._GXDataInfo import _GXDataInfo


class ParsePackage:
    def __init__(self, ):
        # TX:  7E A0 1C 02 21 05 32 85 B8 E6 E6 00 C1 01 C1 00 70 00 00 13 0A 02 FF 03 00 16 00 6F 13 7E
        # RX:  7E A0 11 05 02 21 52 DA 58 E6 E7 00 C5 01 C1 00 50 89 7E
        self.package = None
        self.length = 0
        self.address_from = 0
        self.address_to = 0
        self.number = 0
        self.type_ = 0
        self.type_name = None
        self.pack_type = 0
        self.position = 0
        self.index = 0
        self.crc_head = 0
        self.object_type = 0
        
        self.body = None
        self.body_dict = {}
        self.body_length = 0
        self.crc_body = 0

    def _get_address(self, idx: int, data: bytearray):
        """ Documentation for a method get_addr. Added: 29.09.21 23:59 volodymyr.tyshchenko

        :param idx: data element index
        :type idx: int
        :param data:
        :type data: bytearray

        :return address list and next element index in data
        :rtype tuple
        """
        is_end = '0'
        address = list()
        self.index = idx
        while is_end == '0':
            is_end = bin(data[self.index])[-1]
            address.append(data[self.index])
            self.index += 1
        return address

    def parse_package(self):
        """ Documentation for a method parse_package. Added: 04.10.2021 11:17 volodymyr.tyshchenko
        """
        if self.package is None:
            raise "package is not set"
        # 7E A0
        # 11
        self.length = self.package[2]

        # 05 02 21
        self.address_from = self._get_address(idx=3, data=self.package)
        self.address_to = self._get_address(idx=self.index, data=self.package)
        # 52
        self.number = self.package[self.index]
        self.index += 1
        # DA 58
        self.crc_head = self.package[self.index] << 8 + self.package[self.index + 1]
        self.index += 3

        # E6 E7
        self.type_ = self.package[self.index]
        self.type_name = "req" if self.package[10] == 0xE6 else "res"
        # 00 C5
        # 01

        self.index += 4
        # C1
        self.pack_type = self.package[self.index]

        if self.type_name == "req":
            self.index += 2
            self.object_type = self.package[self.index]
        self.index += 1
        val = self.package.array()[self.index:-3]
        self.body = GXByteBuffer(value=val)
        self.body_length = self.length - self.index - 1
        self.crc_body = int.from_bytes(self.package[-3:-2], byteorder='big', signed=False) << 8 \
            + int.from_bytes(self.package[-2:-1], byteorder='big', signed=False)

    def parse_body(self):
        # gurux parse
        if self.package is None:
            raise "package is not set"
        if self.body is None:
            raise "package body is not set"
        if self.type_name == "res":
            if self.pack_type == 0xC1:
                if self.body_length == 1:
                    self.body_dict["value"] = self.body
                else:
                    reply = _GXDataInfo()
                    settings = GXDLMSSettings(False)
                    while self.position < self.body_length:
                        self.body_dict["body_value"] = _GXCommon.getData(settings=settings, data=self.body, info=reply)
        else:
            self.body_dict["body_value"] = self.body

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
