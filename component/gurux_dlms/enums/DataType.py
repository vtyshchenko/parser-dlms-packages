#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright = c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from ..GXIntEnum import GXIntEnum


class DataType(GXIntEnum):
    """
    DataType enumerates usable types of data in GuruxDLMS.
    """
    #pylint: disable=too-few-public-methods

    # By default, no data type is set.
    NONE = 0x00

    # Data type is Array.
    ARRAY = 0x01

    # Data type is Structure.
    STRUCTURE = 0x02

    # Data type is Boolean.
    BOOLEAN = 0x03

    # Data type is Bit string.
    BITSTRING = 0x04

    # Data type is Int32.
    INT32 = 0x05

    # Data type is UInt32.
    UINT32 = 0x06

    # Data type is Octet string.
    OCTET_STRING = 0x09

    # Data type is String.
    STRING = 0x0A

    # Data type is UTF8 String.
    STRING_UTF8 = 0x0C

    # Data type is Binary coded decimal.
    BCD = 0x0D

    # Data type is Int8.
    INT8 = 0x0F

    # Data type is Int16.
    INT16 = 0x10

    # Data type is UInt8.
    UINT8 = 0x11

    # Data type is UInt16.
    UINT16 = 0x12

    # Data type is Compact array.
    COMPACT_ARRAY = 0x13

    # Data type is Int64.
    INT64 = 0x14

    # Data type is UInt64.
    UINT64 = 0x15

    # Data type is enumerator.
    ENUM = 0x16

    # Data type is Float32.
    FLOAT32 = 0x17

    # Data type is Float64.
    FLOAT64 = 0x18

    # Data type is DateTime.
    DATETIME = 0x19

    # Data type is Date.
    DATE = 0x1a

    # Data type is Time.
    TIME = 0x1b
