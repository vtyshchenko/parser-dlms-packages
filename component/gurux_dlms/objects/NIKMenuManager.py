from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType


class NIKMenuManager(GXDLMSObject, IGXDLMSBase):
    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.NIK_MENU_MANAGER, ln, sn)
        self.pool_menu = list()
        self.current_list = 0
        self.current_index = 0

    def popup_window(self, client):
        return client.method(self, 1, int(0), DataType.STRUCTURE)

    def next_index(self, client):
        return client.method(self, 2, int(0), DataType.UINT8)

    def preview_index(self, client):
        return client.method(self, 3, int(0), DataType.UINT8)

    def run_script(self, client):
        return client.method(self, 4, int(0), DataType.INT8)

    def getValues(self):
        return [self.logicalName,
                self.pool_menu,
                self.current_list,
                self.current_index]

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  pool_menu
        if all_ or self.canRead(2):
            attributes.append(2)
        #  current_list
        if all_ or self.canRead(3):
            attributes.append(3)
        #  current_index
        if all_ or self.canRead(4):
            attributes.append(4)
        return attributes

    def getAttributeCount(self):
        return 4

    def getMethodCount(self):
        return 4

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.UINT8
        elif index == 4:
            ret = DataType.UINT8
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.pool_menu
        if e.index == 3:
            return self.current_list
        if e.index == 4:
            return self.current_index
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.pool_menu = []
            if e.value:
                for it in e.value:
                    self.pool_menu.append((_GXCommon.changeType(it[0], DataType.OCTET_STRING),
                                           _GXCommon.changeType(it[1], DataType.OCTET_STRING)))
        elif e.index == 3:
            self.current_list = e.value
        elif e.index == 4:
            self.current_index = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.pool_menu = []
        if reader.isStartElement("PoolMenu", True):
            while reader.isStartElement("Item", True):
                d = reader.readElementContentAsString("Data")
                v = reader.readElementContentAsString("Value")
                self.pool_menu.append((d, v))
            reader.readEndElement("PoolMenu")
        self.current_list = reader.readElementContentAsInt("CurrentList")
        self.current_index = reader.readElementContentAsInt("CurrentIndex")

    def save(self, writer):
        if self.pool_menu:
            writer.writeStartElement("PoolMenu")
            for k, v in self.pool_menu:
                writer.writeStartElement("Item")
                writer.writeElementString("Data", k)
                writer.writeElementString("Value", v)
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("CurrentList", self.current_list)
        writer.writeElementString("CurrentIndex", self.current_index)
