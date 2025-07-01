from enum import Enum
from typing import List

class Color(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"

    def __str__(self):
        return self.value
    
class Signal:
    duration_seconds: int
    min_duration_seconds: int
    max_duration_seconds: int
    color: Color
    def __init__(self, duration_seconds: int, color: Color, min_duration_seconds: int, max_duration_seconds: int):
        self.color = color
        self.duration_seconds = duration_seconds
        self.min_duration_seconds = min_duration_seconds
        self.max_duration_seconds = max_duration_seconds
    def __str__(self):
        return "Signal{{duration_seconds: {}, color: {}, min_duration_seconds: {}, max_duration_seconds: {}}}".format(self.duration_seconds, self.color, self.min_duration_seconds, self.max_duration_seconds)
    def __repr__(self):
        return "Signal{{duration_seconds: {}, color: {}, min_duration_seconds: {}, max_duration_seconds: {}}}".format(self.duration_seconds, self.color, self.min_duration_seconds, self.max_duration_seconds)

class Phase:
    id: int
    total_seconds: int
    signals: list[Signal]
    def __init__(self, id: int, signals: list[Signal]):
        self.id = id
        self.signals = signals
        self.total_seconds = sum([signal.duration_seconds for signal in signals])
    def __str__(self):
        return "Phase{{id: {}, total_seconds: {}}}".format(self.id, self.total_seconds)
    def __repr__(self):
        return "Phase{{id: {}, total_seconds: {}}}".format(self.id, self.total_seconds)

class GreenInterval:
    phase_idx: int
    start_seconds: int
    end_seconds: int
    def __init__(self, phase_idx: int, start_seconds: int, end_seconds: int):
        self.phase_idx = phase_idx
        self.start_seconds = start_seconds
        self.end_seconds = end_seconds
    def __str__(self):
        return "GreenInterval{{phase_idx: {}, start: {}, end: {}}}".format(self.phase_idx, self.start, self.end)
    def __repr__(self):
        return "GreenInterval{{phase_idx: {}, start: {}, end: {}}}".format(self.phase_idx, self.start, self.end)
    
class Junction:
    id: int
    name: str
    full_cycle: list[Phase]
    full_cycle_seconds: int
    cycle_offset_seconds: int
    def __init__(self, _id: int, _name: str, _x: float, _y: float, _full_cycle: list[Phase]):
        self.id = _id
        self.name = _name
        self.full_cycle = _full_cycle
        self.full_cycle_seconds = sum([phase.total_seconds for phase in _full_cycle])
        self.cycle_offset_seconds = 0
    def set_offset(self, offset_seconds: int):
        self.cycle_offset_seconds = offset_seconds
    def get_offset(self) -> int:
        return self.cycle_offset_seconds
    def __str__(self):
        return "Junction{{id: {}, name: {}, x: {}, y: {}, full_cycle_duration: {}}}".format(self.id, self.name, self.x, self.y, self.full_cycle_duration)
    def __repr__(self):
        return "Junction{{id: {}, name: {}, x: {}, y: {}, full_cycle_duration: {}}}".format(self.id, self.name, self.x, self.y, self.full_cycle_duration)
    
    def get_green_intervals(self) -> List[GreenInterval]:
        ans = []
        #
        # Реализовать поиск зеленых интервалов для светофора
        #
        return ans

    def get_signal_at(self, time: int) -> Signal:
        # Возвращает сигнал, который будет активен в заданный момент времени.
        pass
