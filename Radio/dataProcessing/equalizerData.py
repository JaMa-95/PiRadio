class EqualizerReductionData:
    def __init__(self, reduction_60_hz: int = 1, reduction_170_hz: int = 1, reduction_310_hz: int = 1,
                 reduction_1_khz: int = 1, reduction_3_khz: int = 1, reduction_6_khz: int = 1,
                 reduction_12_hkz: int = 1):
        self.reduction_60_hz: int = reduction_60_hz
        self.reduction_170_hz: int = reduction_170_hz
        self.reduction_310_hz: int = reduction_310_hz
        self.reduction_1_khz: int = reduction_1_khz
        self.reduction_3_khz: int = reduction_3_khz
        self.reduction_6_khz: int = reduction_6_khz
        self.reduction_12_hkz: int = reduction_12_hkz

    def from_list(self, data: list):
        self.reduction_60_hz: int = data[0]
        self.reduction_170_hz: int = data[1]
        self.reduction_310_hz: int = data[2]
        self.reduction_1_khz: int = data[3]
        self.reduction_3_khz: int = data[4]
        self.reduction_6_khz: int = data[5]
        self.reduction_12_hkz: int = data[6]


class Equalizer:
    def __init__(self):
        self.value_60_hz: int = 0
        self.value_170_hz: int = 0
        self.value_310_hz: int = 0
        self.value_1_khz: int = 0
        self.value_3_khz: int = 0
        self.value_6_khz: int = 0
        self.value_12_hkz: int = 0

        self.reduction: EqualizerReductionData = EqualizerReductionData()

        self._iterator: int = 0

    def __iter__(self):
        return self

    def __next__(self):  # Python 2: def next(self)
        if self._iterator == 0:
            self._iterator += 1
            return self.value_60_hz
        if self._iterator == 1:
            self._iterator += 1
            return self.value_170_hz
        if self._iterator == 2:
            self._iterator += 1
            return self.value_310_hz
        if self._iterator == 3:
            self._iterator += 1
            return self.value_1_khz
        if self._iterator == 4:
            self._iterator += 1
            return self.value_3_khz
        if self._iterator == 5:
            self._iterator += 1
            return self.value_6_khz
        if self._iterator == 6:
            self._iterator += 1
            return self.value_12_hkz
        if self._iterator == 7:
            raise StopIteration

    def to_list(self) -> list:
        return [self.value_60_hz, self.value_170_hz, self.value_310_hz, self.value_1_khz,
                self.value_3_khz, self.value_6_khz, self.value_12_hkz]

    def calc_equalizer_with_reductions(self, value: int):
        if self.reduction.reduction_60_hz != -1:
            self.value_60_hz = value / self.reduction.reduction_60_hz
        if self.reduction.reduction_60_hz != -1:
            self.value_170_hz = value / self.reduction.reduction_170_hz
        if self.reduction.reduction_60_hz != -1:
            self.value_310_hz = value / self.reduction.reduction_310_hz
        if self.reduction.reduction_60_hz != -1:
            self.value_1_khz = value / self.reduction.reduction_1_khz
        if self.reduction.reduction_60_hz != -1:
            self.value_3_khz = value / self.reduction.reduction_3_khz
        if self.reduction.reduction_60_hz != -1:
            self.value_6_khz = value / self.reduction.reduction_6_khz
        if self.reduction.reduction_60_hz != -1:
            self.value_12_hkz = value / self.reduction.reduction_12_hkz

