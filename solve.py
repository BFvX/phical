from chart import Chart
from note import Note
from typing import IO
import json
import math

def solve(chart: Chart):
    flick_start = -30
    flick_end = 30
    flick_scale_factor = 100

    frames: dict[int, list] = {}

    def insert(milliseconds: int, event: dict):
        if milliseconds not in frames:
            frames[milliseconds] = []
        frames[milliseconds].append(event)

    current_event_id = 0

    for line in chart.judge_lines:
        for note in line.notes_above + line.notes_below:
            ms = round(line.seconds(note.time) * 1000)
            if note.typ == Note.TAP:
                insert(ms, {
                    'a': 'tap',
                    'i': current_event_id
                })
            elif note.typ == Note.DRAG:
                insert(ms, {
                    'a': 'drag',
                    'i': current_event_id
                })
            elif note.typ == Note.FLICK:
                insert(ms + flick_end, {
                    'a': 'flick_end',
                    'i': current_event_id
                })
            elif note.typ == Note.HOLD:
                hold_ms = math.ceil(line.seconds(note.hold) * 1000)
                insert(ms + hold_ms, {
                    'a': 'hold_end',
                    'i': current_event_id
                })
            current_event_id += 1
    return frames
    #print(frames)

def serialize(frames: dict[int, list]):
    result: dict[int, list] = {}

    def ins(milliseconds: int, event: list):
        if milliseconds not in result:
            result[milliseconds] = []
        result[milliseconds].append(event)

    for ms, frame in sorted(frames.items()):
        ins(ms,frame)

    return result

def export_to_json(ans: dict[int, list], out_file: IO):
    json.dump(ans, out_file)

def load_from_json(in_file: IO) -> dict[int, list]:
    return {int(ts): [event for event in events] for ts, events in json.load(in_file).items()}

def solve_n_export(select_chart, select_level):
    #select_chart = "狂喜蘭舞.LeaF.0"
    #select_level = 'IN'
    chart = Chart.from_dict(json.load(open("C:\\Users\\yyt15\\Desktop\\phisap-main\\Assets\\Tracks\\"+select_chart+"\\Chart_"+select_level+".json")))

    ans_file = './Assets/Tracks/'+select_chart+"/Chart_"+select_level+'.json.note.json'
    ans = solve(chart)
    export_to_json(ans, open(ans_file,'w'))
    return ans


