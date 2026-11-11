from .help import *
from threading import Thread
from enum import IntEnum

class Event(IntEnum):
    MouseUp   = 0
    MouseDown = 1
    MouseMove = 2
    MouseDragged = 3
    Display = 4
create_register = lambda self : setattr(self, "reg", [])
EVENT_REGISTER = type("EVENT_REGISTER",(object,),{"__init__":create_register, "add":lambda s, v: s.reg.append(v)})

EVENT_REGISTRY = {
    Event.MouseDown:EVENT_REGISTER(),
    Event.MouseUp:EVENT_REGISTER(),
    Event.MouseMove:EVENT_REGISTER(),
    Event.MouseDragged:EVENT_REGISTER(),
    Event.Display:EVENT_REGISTER(),
}

EVENT_QUEUE: list[tuple[Event,list]] = []

trigger_event = lambda event_id, event_args: [event_name(event_args) for event_name in EVENT_REGISTRY[event_id].reg]
manage_queue = lambda: trigger_event(*EVENT_QUEUE.pop(0))
signal = lambda event, args: EVENT_QUEUE.append((event, args))
slot = lambda event, callback: EVENT_REGISTRY[event].add(callback)

class ThreadEventManager:
    thread_exit:bool = False
    def thread_continuity(self):
        while True:
            while len(EVENT_QUEUE) == 0:
                sleep(0.25) 
            manage_queue()
            if self.thread_exit:
                break
    def launch(self):
        self.thread = Thread(target=self.thread_continuity, daemon=True)
        self.thread.start()

