# SPDX-License-Identifier: MIT
"""
SGP30 I2C driver for CPython (Linux / Raspberry Pi)

Ported from Adafruit CircuitPython SGP30 driver.
"""

import time
from math import exp
from typing import List, Tuple, Optional

from smbus2 import SMBus, i2c_msg


_SGP30_DEFAULT_I2C_ADDR = 0x58
_SGP30_FEATURESETS = (0x0020, 0x0022)

_SGP30_CRC8_POLYNOMIAL = 0x31
_SGP30_CRC8_INIT = 0xFF
_SGP30_WORD_LEN = 2


class SGP30:
    """SGP30 gas sensor driver for CPython"""

    def __init__(self, bus: int = 1, address: int = _SGP30_DEFAULT_I2C_ADDR):
        """
        :param bus: I2C bus number (default 1 on Raspberry Pi)
        :param address: I2C address (default 0x58)
        """
        self.address = address
        self.bus = SMBus(bus)

        # Read serial number (48 bits)
        self.serial = self._i2c_read_words_from_cmd([0x36, 0x82], 0.01, 3)

        # Check feature set
        featureset = self._i2c_read_words_from_cmd([0x20, 0x2F], 0.01, 1)
        if featureset[0] not in _SGP30_FEATURESETS:
            raise RuntimeError("SGP30 not detected")

        self.iaq_init()

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def eCO2(self) -> int:
        """CO₂ equivalent in ppm"""
        return self.iaq_measure()[0]

    @property
    def TVOC(self) -> int:
        """Total VOC in ppb"""
        return self.iaq_measure()[1]

    @property
    def baseline_eCO2(self) -> int:
        return self.get_iaq_baseline()[0]

    @property
    def baseline_TVOC(self) -> int:
        return self.get_iaq_baseline()[1]

    @property
    def H2(self) -> int:
        """Raw H₂ signal"""
        return self.raw_measure()[0]

    @property
    def Ethanol(self) -> int:
        """Raw Ethanol signal"""
        return self.raw_measure()[1]

    # ------------------------------------------------------------------
    # High-level commands
    # ------------------------------------------------------------------

    def iaq_init(self) -> None:
        """Initialize IAQ algorithm"""
        self._run_profile(("iaq_init", [0x20, 0x03], 0, 0.01))

    def iaq_measure(self) -> List[int]:
        """Measure eCO2 and TVOC"""
        return self._run_profile(("iaq_measure", [0x20, 0x08], 2, 0.05))

    def raw_measure(self) -> List[int]:
        """Measure raw H2 and Ethanol signals"""
        return self._run_profile(("raw_measure", [0x20, 0x50], 2, 0.025))

    def get_iaq_baseline(self) -> List[int]:
        """Read IAQ baseline values"""
        return self._run_profile(("iaq_get_baseline", [0x20, 0x15], 2, 0.01))

    def set_iaq_baseline(self, eCO2: int, TVOC: int) -> None:
        """Restore IAQ baseline"""
        if eCO2 == 0 and TVOC == 0:
            raise ValueError("Invalid baseline")

        buffer = []
        for value in (TVOC, eCO2):
            data = [value >> 8, value & 0xFF]
            data.append(self._generate_crc(data))
            buffer.extend(data)

        self._run_profile(("iaq_set_baseline", [0x20, 0x1E] + buffer, 0, 0.01))

    def set_iaq_humidity(self, grams_pm3: float) -> None:
        """Set absolute humidity in g/m³"""
        value = int(grams_pm3 * 256)
        data = [value >> 8, value & 0xFF]
        data.append(self._generate_crc(data))
        self._run_profile(("iaq_set_humidity", [0x20, 0x61] + data, 0, 0.01))

    def set_iaq_relative_humidity(self, celsius: float, relative_humidity: float):
        """
        Set humidity using temperature (°C) and relative humidity (%)
        """
        numerator = ((relative_humidity / 100.0) * 6.112) * exp(
            (17.62 * celsius) / (243.12 + celsius)
        )
        humidity = 216.7 * (numerator / (273.15 + celsius))
        self.set_iaq_humidity(humidity)

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _run_profile(
        self, profile: Tuple[str, List[int], int, float]
    ) -> Optional[List[int]]:
        _, command, signals, delay = profile
        return self._i2c_read_words_from_cmd(command, delay, signals)

    def _i2c_read_words_from_cmd(
        self, command: List[int], delay: float, reply_size: int
    ) -> Optional[List[int]]:
        """Send command and read response words with CRC"""
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

        time.sleep(delay)

        if reply_size == 0:
            return None

        read_len = reply_size * (_SGP30_WORD_LEN + 1)
        read = i2c_msg.read(self.address, read_len)
        self.bus.i2c_rdwr(read)

        data = list(read)
        result = []

        for i in range(reply_size):
            word = data[3 * i : 3 * i + 2]
            crc = data[3 * i + 2]
            if self._generate_crc(word) != crc:
                raise RuntimeError("CRC mismatch")
            result.append((word[0] << 8) | word[1])

        return result

    def _generate_crc(self, data: List[int]) -> int:
        """8-bit CRC for SGP30"""
        crc = _SGP30_CRC8_INIT
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ _SGP30_CRC8_POLYNOMIAL
                else:
                    crc <<= 1
        return crc & 0xFF
