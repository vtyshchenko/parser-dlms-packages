from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType


# pylint: disable=too-many-instance-attributes
class NIKMeterFunction(GXDLMSObject, IGXDLMSBase):

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.NIK_METER_FUNCTION, ln, sn)

    def cumulative_demand(self, client):
        return client.method(self, 1, int(0), DataType.INT8)

    def generate_identification(self, client):
        return client.method(self, 2, int(0), DataType.UINT32)

    def clear_register_time_integral(self, client):
        return client.method(self, 3, int(0), DataType.UINT8)

    def clear_max_demand(self, client):
        return client.method(self, 4, int(0), DataType.INT8)

    def getValues(self):
        return [self.logicalName]

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        return attributes

    def getAttributeCount(self):
        return 1

    def getMethodCount(self):
        return 4

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        pass

    def save(self, writer):
        pass
