# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 14:27:00 2017

@author: nikita.gladkikh
"""
import logging
import serial
import socket
import threading

from abc import ABCMeta, abstractmethod
from time import sleep

# from component.gurux_common.io import Parity, StopBits, BaudRate


class Interface(metaclass=ABCMeta):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def put(self, data=None):
        pass

    @abstractmethod
    def get(self):
        pass

    def __enter__(self):
        try:
            logging.debug(f"Open {self.__class__.__name__}")
            return self.open()
        except Exception as e:
            logging.exception(f'Exception in Interface {self.__class__.__name__}: {e}')

    def __exit__(self, ex_type=None, ex_value=None, ex_traceback=None):
        if ex_type:
            logging.exception(f'Exception in Interface!\n{ex_type}\n{ex_value}\n{ex_traceback}\n')
            return ex_type, ex_value, ex_traceback
        try:
            self.close()
        except:
            pass


class SocketInterface(Interface):

    def __init__(self, host, port, timeout):
        self.timeout = timeout
        self.host = host
        self.port = port
        self.sock = None

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        logging.debug(f'Start socket connection with: {self.host}: {self.port}.\n')
        return self
        
    def close(self):
        self.sock.close()
        logging.debug(f'Close connection with: {self.host}: {self.port}.\n')

    def put(self, data=None):
        try:
            logging.debug(f"REQ: {data.hex()}")
            self.sock.send(data)
        except ConnectionError:
            logging.exception('Exception in SocketInterface.put ConnectionError')
            self.close()
            self.open()
        except:
            logging.exception('Exception in SocketInterface.put')
            raise

    def get(self, min_length=0, max_tries=5):
        buff_size = min_length if min_length else 1024
        try:
            try_number = 0
            res = self.sock.recv(buff_size)
            while len(res) < min_length:
                res += self.sock.recv(buff_size)
                try_number += 1
                if try_number >= max_tries:
                    break
        except ConnectionError:
            logging.exception('ConnectionError in SocketInterface.get')
            raise
        # except TimeoutError:
        except socket.timeout:
            logging.exception('SocketInterface.get Timeout')
            res = bytes()
        except:
            logging.exception('SocketInterface.get Exception')
            raise
        logging.debug(f"RES: {res.hex()}")
        return res


class SerialInterface(Interface):

    def __init__(self, port='', timeout=1, baudrate=9600, bytesize=8, parity=1, stopbits=0):
        self.port = port
        self.ser = None
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.eop = None
        self.tsl = 0.1
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.__lock = None

    def open(self):
        self.ser = serial.Serial()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port
        self.ser.timeout = self.timeout
        self.ser.bytesize = self.bytesize
        self.ser.parity = self.ser.PARITIES[self.parity]
        self.ser.stopbits = self.ser.STOPBITS[self.stopbits]
        self.__lock = threading.Lock()
        logging.debug(f'Open serial {self.ser.port} on {self.ser.baudrate}')
        self.ser.open()
        return self

    def close(self):
        logging.debug(f'Close connection on {self.ser.port}')
        self.__lock = None
        self.ser.close()

    def put(self, data=None):
        self.ser.write(data)

    def get(self, min_length=0, max_tries=5):
        try:
            res = self.ser.read(self.ser.inWaiting())
            try_num = 0
            while len(res) < min_length:
                sleep(self.tsl)
                try_num += 1
                res += self.ser.read(self.ser.inWaiting())
                if try_num > max_tries:
                    break
            return res
        except Exception:
            logging.exception('Exception in SerialInterface.get')
            raise

    def receive(self, args):
        try:
            reply = self.ser.read_until('\n')
            args.reply = reply
            try_num = 0
            while args.reply == b'':
                sleep(self.tsl)
                reply = self.ser.read_until('\n')
                args.reply += reply
                if try_num < 5:
                    break
                try_num += 1
            return args.reply != b''
        except Exception:
            logging.exception('Exception in SerialInterface.receive')
            raise

    def getSynchronous(self):
        return self.__lock

    # pylint: disable=no-member
    def getIsSynchronous(self):
        return self.__lock.locked()

    def is_open(self):
        return self.ser.is_open
