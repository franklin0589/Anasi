from enum import IntEnum

def parse(text_file):
    with open(text_file) as f:
        for index, line in enumerate(f.readlines()):
            yield index, line.strip()
    
# State Changes 

#Comments->Title->Character->Dialogue
class StateEnum(IntEnum):
    Comments = 0
    Title = 1
    Character =  2
    Dialogue = 3
class DialogueStateEnum(IntEnum):
    Action = 0
    Dialogue = 1
    


unless = lambda object, case, call: call(object) if case(object) else object


class Script_Manager:
    def __init__(self, _SCRIPT):
        self.state = StateEnum.Comments 
        self.TITLE = []   
        self.castings = []
        self.CAST = []
        self.DIALOGUE = []
        self.STAGE = []
        
        self.buffer = []
        self.dialogue_state = DialogueStateEnum.Dialogue
        
        for i,li in parse(_SCRIPT):
            match self.state:
                case StateEnum.Comments:
                    self.state = self.next_state_on("****", li)
                case StateEnum.Title:
                    self.TITLE += [li]
                    self.state = self.next_state_on("=====", li)
                case StateEnum.Character:
                    self.castings += [li]
                    self.state = self.next_state_on("+++++", li)
                case StateEnum.Dialogue:
                    self.DIALOGUE += [li]
        self.TITLE.pop()
        self.castings.pop()
        self.DIALOGUE.pop()
        self.process_cast(self.castings)
        self.actor = None



    def read(self):
        for index, line in enumerate(self.DIALOGUE):    
            if "Enter" in line:
                line = line.lstrip("Enter: ")
                for char in line.split(","):
                    self.STAGE.append(self.CAST[char.strip()])
                    
            elif "Leaves" in line:
                line = line.rstrip(" Leaves.")
                for char in line.split(","):
                    self.STAGE.remove(self.CAST[char.strip()])
                ...
            elif ">:" in line:
                self.actor = line.split(": ")[0]
                self.dialogue_state = DialogueStateEnum.Action
                self.buffer += [line.split(": ")[-1]]        
            elif ":" in line:
                if self.buffer != []:
                    if self.dialogue_state == DialogueStateEnum.Dialogue:
                        if "(" in self.actor:
                            name, plly = self.actor.split("(")
                            name = name.strip()
                            yield [1, name, self.CAST[name], self.buffer, plly]
                        else:  
                            yield [1, self.actor, self.CAST[self.actor], self.buffer, None]
                    elif self.dialogue_state == DialogueStateEnum.Action:
                        yield [0, self.buffer] 
                    self.buffer = []

                self.actor = line.split(": ")[0].strip()
                self.dialogue_state = DialogueStateEnum.Dialogue
                self.buffer += [line.split(": ")[-1]]

            else:
                self.buffer += [line]
        
    def process_cast(self, castings):
        get_model = lambda x : self.load_model(x) if "*" in x else self.load_base_model(x)
        check_star = lambda i: "*" in i
        extract_actor = lambda i:i.split("*")[0].strip()
        self.CAST = { unless(i.strip(), check_star, extract_actor):get_model(i)for i in castings}

        
    def load_model(self, model):
        return None
    def load_base_model(self, model):
        return None

    def next_state_on(self, value, line): return (self.state+1) if value in line else self.state