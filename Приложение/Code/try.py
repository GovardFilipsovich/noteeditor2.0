from mido import Message, MidiFile, MidiTrack, second2tick

class MidiPlayer:
    """Проигрывает файлы midi"""
    def __init__(self):
        self.state = 0
        self.pos = 0
        self.cur = ""

        
    def setMedia(self, file):
        """Устанавливает нужную композицию"""
        self.file = file
        self.melody = mido.MidiFile(file)

        
    def Play(self):
        self.state = 1
        self.port = mido.open_output()
        t = threading.Thread(target=self.start)


    def start(self):
        if self.state == 1:
            for i in self.melody.play():
                self.cur = i.hex()
                self.port.send(i)  
        else:
            self.port.close()
                
                
        
    def position(self):
        """"""
        

    def Pause(self):
        self.state = 2
                    

    def duration(self):
        return self.melody.length

    
    def state(self):
        """Возращает состояние текущего файла"""
        return self.state        
        
        
        
