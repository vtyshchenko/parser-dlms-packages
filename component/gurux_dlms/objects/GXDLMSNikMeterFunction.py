from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType


# pylint: disable=too-many-instance-attributes
class GXDLMSNikMeterFunction(GXDLMSObject, IGXDLMSBase):
    def __init__(self, ln="0.0.130.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.NIK_METER_FUNCTION, ln, sn)

    def getMethodCount(self):
        return 8

    def getAttributeCount(self):
        return 1

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        raise ValueError("getDataType failed. Invalid attribute index.")

    def getValues(self):
        return [self.logicalName]

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        else:
            ret = None
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        return attributes

    def load(self, reader):
        pass

    def save(self, writer):
        pass
