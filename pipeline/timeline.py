"""Pure timeline math: raw event times stay independent of narration and rendering."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Segment:
    raw_start: float
    raw_end: float
    edited_start: float
    edited_end: float
    kind: str

    @property
    def speed(self):
        return (self.raw_end-self.raw_start)/(self.edited_end-self.edited_start)

def build_timeline(duration, waits, max_wait=5.0):
    """Compress explicitly verified noninstructional waits only; reject ambiguity."""
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('duration must be positive and finite')
    if not math.isfinite(max_wait) or max_wait <= 0:
        raise ValueError('max_wait must be positive and finite')
    intervals = sorted(tuple(w) for w in waits)
    cursor=0.0; edited=0.0; result=[]
    for start,end in intervals:
        if not all(math.isfinite(v) for v in (start,end)) or not 0 <= start < end <= duration:
            raise ValueError('wait outside recording or empty')
        if start < cursor:
            raise ValueError('overlapping waits require explicit reconciliation')
        if start > cursor:
            result.append(Segment(cursor,start,edited,edited+start-cursor,'action'))
            edited += start-cursor
        length=min(end-start,max_wait)
        result.append(Segment(start,end,edited,edited+length,'wait'))
        edited += length;cursor=end
    if cursor < duration:
        result.append(Segment(cursor,duration,edited,edited+duration-cursor,'action'))
    return result

def map_time(segments, raw_time):
    if not math.isfinite(raw_time) or raw_time < 0 or raw_time > segments[-1].raw_end:
        raise ValueError('event outside timeline')
    for s in segments:
        if s.raw_start <= raw_time <= s.raw_end:
            return s.edited_start+(raw_time-s.raw_start)/s.speed
    raise ValueError('timeline has a gap')

def map_highlight(segments, start, end):
    if end <= start:
        raise ValueError('highlight must have positive duration')
    return [map_time(segments,start),map_time(segments,end)]
