
from typing import List

class GreenWaveInterval:
    phase_idx: int
    start: int
    end: int
    def __init__(self, phase_idx: int, start: int, end: int):
        self.phase_idx = phase_idx
        self.start = start
        self.end = end
    def __str__(self):
        return "GreenWaveInterval{{phase_idx: {}, start: {}, end: {}}}".format(self.phase_idx, self.start, self.end)
    def __repr__(self):
        return "GreenWaveInterval{{phase_idx: {}, start: {}, end: {}}}".format(self.phase_idx, self.start, self.end)
    def clone(self):
        return GreenWaveInterval(self.phase_idx, self.start, self.end)    

class GreenWave:
    interval_j1: GreenWaveInterval
    interval_j2: GreenWaveInterval
    distance_meters: float
    time_drive_seconds: float
    band_size: float
    def __init__(self, interval_j1: GreenWaveInterval, interval_j2: GreenWaveInterval, distance_meters: float, time_drive_seconds: float):
        self.interval_j1 = interval_j1
        self.interval_j2 = interval_j2
        self.distance_meters = distance_meters
        self.time_drive_seconds = time_drive_seconds
        self.band_size = interval_j1.end - interval_j1.start
    def __str__(self):
        return f"GreenWave{{Intervals: {self.interval_j1}, {self.interval_j2}, band_size: {self.band_size}}}"
    def __repr__(self):
        return f"GreenWave{{Intervals: {self.interval_j1}, {self.interval_j2}, band_size: {self.band_size}}}"
    def clone(self):
        return GreenWave(self.interval_j1.clone(), self.interval_j2.clone(), self.distance_meters, self.time_drive_seconds)

class GreenWavesChain:
    green_waves: List[GreenWave]
    def __init__(self, green_waves: List[GreenWave]):
        self.green_waves = green_waves
    def __str__(self):
        return "GreenWavesChain{{green_waves: {}}}".format(self.green_waves)
    def __repr__(self):
        return "GreenWavesChain{{green_waves: {}}}".format(self.green_waves)
    
class ThroughGreenWave:
    def __init__(self, intervals: List[GreenWaveInterval]):
        self.intervals = intervals
        self.depth = len(intervals)
        # Критерий для оптимизации
        self.band_size = self._calculate_band_size()
    def __str__(self):
        return f"ThroughGreenWave{{Intervals: {self.intervals}, BandSize: {self.band_size}}}"
    def __repr__(self):
        return f"ThroughGreenWave{{Intervals: {self.intervals}, BandSize: {self.band_size}}}"
    def _calculate_band_size(self) -> float:
        # Миниммальный интервал зеленой волны
        return min(interval.end - interval.start for interval in self.intervals)

class GreenWavesResult:
    green_waves: List[GreenWave]
    chained_green_waves: List[ThroughGreenWave]
    def __init__(self, green_waves: List[GreenWave], chained_green_waves: List[ThroughGreenWave]):
        self.green_waves = green_waves
        self.chained_green_waves = chained_green_waves