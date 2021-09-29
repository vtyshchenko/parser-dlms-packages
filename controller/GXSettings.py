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
#  Copyright (c) Gurux Ltd
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
from component.gurux_dlms.enums import InterfaceType, Authentication
from component.gurux_dlms import GXDLMSClient
from component.gurux_dlms.secure import GXDLMSSecureClient
from component.gurux_common.enums import TraceLevel
from component.gurux_common.io import Parity
from component.gurux_net.enums import NetworkType
from component.gurux_net import GXNet
from component.gurux_serial.GXSerial import GXSerial
from .GXCmdParameter import GXCmdParameter


class GXSettings:
    """
    GXSettings
    """
    def __init__(self):
        """ Documentation for a method __init__.
        Constructor.
        """
        self.media = None
        self.trace = TraceLevel.VERBOSE
        self.iec = True
        self.client = GXDLMSSecureClient(True)
        #  Objects to read.
        self.readObjects = []

    #
    # Show help.
    #
    @classmethod
    def showHelp(cls):
        print("GuruxDlmsSample reads data from the DLMS/COSEM device.")
        print("GuruxDlmsSample -h [Meter IP Address] -p [Meter Port No] -c 16 -s 1 -r SN")
        print(" -h \t host name or IP address.")
        print(" -p \t port number or name (Example: 1000).")
        print(" -S \t serial port.")
        print(" -i IEC is a start protocol.")
        print(" -a \t Authentication (None, Low, High).")
        print(" -P \t Password for authentication.")
        print(" -c \t Client address. (Default: 16)")
        print(" -s \t Server address. (Default: 1)")
        print(" -n \t Server address as serial number.")
        print(" -r [sn, ln]\t Short name or Logican Name (default) referencing is used.")
        print(" -w WRAPPER profile is used. HDLC is default.")
        print(" -t [Error, Warning, Info, Verbose] Trace messages.")
        print(" -g \"0.0.1.0.0.255:1; 0.0.1.0.0.255:2\" Get selected object(s) with given attribute index.")
        print("Example:")
        print("Read LG device using TCP/IP connection.")
        print("GuruxDlmsSample -r SN -c 16 -s 1 -h [Meter IP Address] -p [Meter Port No]")
        print("Read LG device using serial port connection.")
        print("GuruxDlmsSample -r SN -c 16 -s 1 -S COM1 -i")
        print("Read Indian device using serial port connection.")
        print("GuruxDlmsSample -S COM1 -c 16 -s 1 -a Low -P [password]")
        print("------------------------------------------------------")
        print("Available serial ports:")
        print(GXSerial.getPortNames())

    @classmethod
    def __getParameters(cls, args, optstring):
        """ Documentation for a method __getParameters.
        Returns command line parameters.

        :param args: Command line parameters.
        :type args: str
        :param opt_string:  Expected option tags
        :type opt_string: str

        :return: List of command line parameters
        :rtype: list
        """
        list_ = list()
        skipNext = False
        for index in range(1, len(args)):
            if skipNext:
                skipNext = False
            else:
                if args[index][0] != '-' and args[index][0] != '/':
                    raise ValueError(f"Invalid parameter: {args[index]}")

                pos = optstring.index(args[index][1])
                if pos == - 1:
                    raise ValueError(f"Invalid parameter: {args[index]}")

                c = GXCmdParameter()
                c.tag = args[index][1]
                list_.append(c)
                if pos < len(optstring) - 1 and optstring[1 + pos] == ':':
                    skipNext = True
                    if len(args) <= index:
                        c.missing = True
                    c.value = args[1 + index]
        return list_

    def getParameters(self, args):
        """ Documentation for a method get_parameters.

        :param args: Command line parameters.
        :type args: str

        :return: 0 if errors else 1
        :rtype: int
        """
        parameters = GXSettings.__getParameters(args, "h:p:c:s:r:it:a:p:wP:g:S:n:")
        for it in parameters:
            if it.tag == 'w':
                self.client.interfaceType = InterfaceType.WRAPPER
            elif it.tag == 'r':
                if it.value == "sn":
                    self.client.useLogicalNameReferencing = False
                elif it.value == "ln":
                    self.client.useLogicalNameReferencing = True
                else:
                    raise ValueError("Invalid reference option.")
            elif it.tag == 'h':
                #  Host address.
                if not self.media:
                    self.media = GXNet(NetworkType.TCP, it.value, 0)
                else:
                    self.media.hostName = it.value
            elif it.tag == 't':
                #  Trace.
                if it.value == "Off":
                    self.trace = TraceLevel.OFF
                elif it.value == "Error":
                    self.trace = TraceLevel.ERROR
                elif it.value == "Warning":
                    self.trace = TraceLevel.WARNING
                elif it.value == "Info":
                    self.trace = TraceLevel.INFO
                elif it.value == "Verbose":
                    self.trace = TraceLevel.VERBOSE
                else:
                    raise ValueError("Invalid trace level(Off, Error, Warning, Info, Verbose).")
            elif it.tag == 'p':
                #  Port.
                if not self.media:
                    self.media = GXNet(NetworkType.TCP, None, int(it.value))
                else:
                    self.media.port = int(it.value)
            elif it.tag == 'P':
                #  Password
                self.client.password = it.value
            elif it.tag == 'i':
                #  IEC.
                self.iec = True
            elif it.tag == 'g':
                #  Get (read) selected objects.
                for o in it.value.split(";,"):
                    tmp = o.split(":")
                    if len(tmp) != 2:
                        raise ValueError("Invalid Logical name or attribute index.")
                    self.readObjects.append((tmp[0].strip(), int(tmp[1].strip())))
            elif it.tag == 'S':#Serial Port
                self.media = GXSerial(None)
                tmp = it.value.split(':')
                self.media.port = tmp[0]
                if len(tmp) > 1:
                    self.media.baudRate = int(tmp[1])
                    self.media.dataBits = int(tmp[2][0: 1])
                    self.media.parity = Parity(tmp[2][1: len(tmp[2]) - 2] .Substring(1, tmp[2].Length - 2))
                    self.media.stopBits = int(tmp[2][len(tmp[2]) - 1:])
            elif it.tag == 'a':
                try:
                    it.value = it.value.upper()
                    if it.value != "HIGH" and it.value.startswith("HIGH"):
                        it.value = "HIGH_" + it.value[4:]
                    self.client.authentication = Authentication[it.value]
                except Exception:
                    raise ValueError(f"Invalid Authentication option: '{it.value}'. (None, Low, High, HighGmac)")
            elif it.tag == 'o':
                pass
            elif it.tag == 'c':
                self.client.clientAddress = int(it.value)
            elif it.tag == 's':
                self.client.serverAddress = int(it.value)
            elif it.tag == 'n':
                self.client.serverAddress = GXDLMSClient.getServerAddress(int(it.value))
            elif it.tag == '?':
                if it.tag == 'c':
                    raise ValueError("Missing mandatory client option.")
                if it.tag == 's':
                    raise ValueError("Missing mandatory server option.")
                if it.tag == 'h':
                    raise ValueError("Missing mandatory host name option.")
                if it.tag == 'p':
                    raise ValueError("Missing mandatory port option.")
                if it.tag == 'r':
                    raise ValueError("Missing mandatory reference option.")
                if it.tag == 'a':
                    raise ValueError("Missing mandatory authentication option.")
                if it.tag == 'S':
                    raise ValueError("Missing mandatory Serial port option.\n")
                if it.tag == 't':
                    raise ValueError("Missing mandatory trace option.\n")
                self.showHelp()
                return 1
            else:
                self.showHelp()
                return 1

        if not self.media:
            GXSettings.showHelp()
            return 1
        return 0
