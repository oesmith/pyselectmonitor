import struct
import threading
import time

import serial

SELECT_MONITOR_FIELDS = {
    0x7: ["Battery Voltage", "V", lambda x: x*0.08],
    0x8: ["Vehicle Speed", "mph", lambda x: x*2.0],
    0x9: ["Engine Speed", "rpm", lambda x: x*25],
    0xa: ["Coolant Temperature", "deg C", lambda x: x-50],
    0xb: ["Ignition Advance", "deg", lambda x: x],
    0xc: ["Airflow Sensor", "V", lambda x: x*5.0/256.0],
    0xd: ["Engine Load", "", lambda x: x],
    0xf: ["Throttle Position", "V", lambda x: x*5.0/256.0],
    0x10: ["Injector Pulse Width", "ms", lambda x: x*256.0/1000.0 ],
    0x11: ["ISU Duty Valve", "% DC", lambda x: x*100.0/256.0 ],
    0x12: ["O2 Average", "mV", lambda x: x*5000.0/512.0],
    0x13: ["O2 Minimum", "mV", lambda x: x*5000.0/256.0],
    0x14: ["O2 Maximum", "mV", lambda x: x*5000.0/256.0],
    0x15: ["Knock Correction", "deg", lambda x: x],
    0x1c: ["A/F Correction", "%", lambda x: x-128],
    0x1f: ["Atmospheric Pressure", "mmHg", lambda x: x*8],
    0x20: ["Manifold Pressure", "Bar", lambda x: (x-128)/85.0],
    0x22: ["Boost Solenoid Duty Cycle", "% DC", lambda x: x*100.0/256.0]
}

class SelectMonitor(object):
    """An interface for the Subaru Select Monitor protocol"""
    
    def __init__(self, port, callback):
        """
        ctor.
        """
        super(SelectMonitor, self).__init__()
        self.port = port
        self.serial = serial.Serial(port=self.port, 
                                    baudrate=1953,
                                    bytesize=serial.EIGHTBITS, 
                                    parity=serial.PARITY_EVEN, 
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=1.0)
        self.callback = callback
        if not self.serial.isOpen():
            raise Error("Unknown serial port error..")
        self.running = True
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.__reader)
        self.thread.start()
    
    def close(self):
        """
        Stop the reader thread and close the serial port.
        """
        self.running = False
        self.thread.join(1.0)
        self.serial.close()
    
    def __reader(self):
        """
        A worker thread to read from the port and send the data to the
        callback.
        """
        while self.running:
            # using the mutex..
            with self.lock:
                # get the number of bytes waiting on the port..
                count = self.serial.inWaiting()
                if count > 0:
                    # then send those bytes to the callback
                    bytes = self.serial.read(count)
                    self.callback(bytes)
            # sleep if there was nothing waiting
            if count == 0:
                time.sleep(0.1)
    
    def send_command(self, command):
        """
        Write a command to the port.
        
        A command is a packed byte string (as produced by the struct.pack
        method).
        """
        with self.lock:
            self.serial.write(command)
    
    def stop(self):
        """
        Issue a STOP command.
        """
        self.send_command(struct.pack('!BBBB', 0x12, 0, 0, 0))
    
    def get_rom_id(self):
        """
        Issue a ROM ID command.
        """
        self.send_command(struct.pack('!BBBB', 0, 0x46, 0x48, 0x49))
    
    def read(self, address, count=0):
        """
        Issue a READ command with the given address and count parameters.
        """
        self.send_command(struct.pack('!BHB', 0x78, address, count))
        