from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType


class NIKMenuList(GXDLMSObject, IGXDLMSBase):

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.NIK_MENU_LIST, ln, sn)
        self.list = list()
        self.mask_list = None
        self.inactivity_timeout = None
        self.scroll_timeout = None
        self.name_list = None

    def run_script(self, client):
        return client.method(self, 1, int(0), DataType.UINT8)

    def getValues(self):
        return [self.logicalName,
                self.list,
                self.mask_list,
                self.inactivity_timeout,
                self.scroll_timeout,
                self.name_list]

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  list
        if all_ or self.canRead(2):
            attributes.append(2)
        #  mask_list
        if all_ or self.canRead(3):
            attributes.append(3)
        #  inactivity_timeout
        if all_ or self.canRead(4):
            attributes.append(4)
        #  scroll_timeout
        if all_ or self.canRead(5):
            attributes.append(5)
        #  name_list
        if all_ or self.canRead(6):
            attributes.append(6)
        return attributes

    def getAttributeCount(self):
        return 6

    def getMethodCount(self):
        return 1

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.UINT32
        elif index == 4:
            ret = DataType.UINT8
        elif index == 5:
            ret = DataType.UINT8
        elif index == 6:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.list
        if e.index == 3:
            return self.mask_list
        if e.index == 4:
            return self.inactivity_timeout
        if e.index == 5:
            return self.scroll_timeout
        if e.index == 6:
            return self.name_list
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.list = []
            if e.value:
                for it in e.value:
                    self.list.append([[_GXCommon.toLogicalName(it[0][0])] + it[0][1:],
                                      [_GXCommon.toLogicalName(it[1][0])] + it[1][1:]])
        elif e.index == 3:
            self.mask_list = e.value
        elif e.index == 4:
            self.inactivity_timeout = e.value
        elif e.index == 5:
            self.scroll_timeout = e.value
        elif e.index == 6:
            self.name_list = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.list = []
        if reader.isStartElement("List", True):
            while reader.isStartElement("Item", True):
                d = reader.readElementContentAsString("Data")
                v = reader.readElementContentAsString("Value")
                self.list.append((d, v))
            reader.readEndElement("List")
        self.mask_list = reader.readElementContentAsInt("MaskList")
        self.inactivity_timeout = reader.readElementContentAsInt("InactivityTimeout")
        self.scroll_timeout = reader.readElementContentAsInt("ScrollTimeout")
        self.name_list = reader.readElementContentAsInt("NameList")

    def save(self, writer):
        if self.list:
            writer.writeStartElement("List")
            for k, v in self.list:
                writer.writeStartElement("Item")
                writer.writeElementString("Data", k)
                writer.writeElementString("Value", v)
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("MaskList", self.mask_list)
        writer.writeElementString("InactivityTimeout", self.inactivity_timeout)
        writer.writeElementString("ScrollTimeout", self.scroll_timeout)
        writer.writeElementString("NameList", self.name_list)
