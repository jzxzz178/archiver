from collections import Counter
from decimal import Decimal, getcontext

getcontext().prec = 100 

class ArithmeticCoder:
    def __init__(self, data):
        self.data = data
        self.symbols = sorted(set(data))
        self.freq = Counter(data)
        self.total = sum(self.freq.values())
        self.cumulative = self._build_cumulative()

    def _build_cumulative(self):
        cumulative = {}
        cum = 0
        for sym in self.symbols:
            cumulative[sym] = (cum, cum + self.freq[sym])
            cum += self.freq[sym]
        return cumulative

    def encode(self):
        l, h = Decimal(0), Decimal(1)
        for symbol in self.data:
            sym_low, sym_high = self.cumulative[symbol] 
            range_ = h - l
            h = l + range_ * Decimal(sym_high) / self.total
            l = l + range_ * Decimal(sym_low) / self.total
        return (l + h) / 2 

    def decode(self, value, length):
        value = Decimal(value)
        result = []
        l, h = Decimal(0), Decimal(1)
        for _ in range(length):
            range_ = h - l 
            if range_ == 0:
                raise ZeroDivisionError("Error: range is 0")
            scaled_value = (value - l) / range_ * self.total
            for symbol in self.symbols:
                sym_low, sym_high = self.cumulative[symbol]
                if sym_low <= scaled_value < sym_high:
                    result.append(symbol)
                    h = l + range_ * Decimal(sym_high) / self.total
                    l = l + range_ * Decimal(sym_low) / self.total
                    break
        return result
