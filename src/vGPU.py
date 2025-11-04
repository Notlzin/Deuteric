# vGPU.py: virtual GPU for Deuteric, screen size= 160px by 80px #
class vGPU:
    def __init__(self,w=160,h=80):
        self.width = w
        self.height = h
        self.cursorX = 0
        self.cursorY = 0
        self.framebuffer = [[' ']*self.width for _ in range(self.height)]

    def clear(self):
        self.framebuffer = [[' ']*self.width for _ in range(self.height)]
        self.cursorX = 0
        self.cursorY = 0
        print("\033[2J\033[H", end="")

    def drawChar(self,char):
        if char=='\n':
            self.cursorX = 0
            self.cursorY += 1
        else:
            if self.cursorY < self.height:
                self.framebuffer[self.cursorY][self.cursorX] = char
                self.cursorX += 1
                if self.cursorX >= self.width:
                    self.cursorY = 0
                    self.cursorY += 1
        if self.cursorY >= self.height:
            self.cursorY = self.height - 1
        # render directly in terminal #
        print(char,end='',flush=True)

    def receive(self,value):
        # receive a byte (integer) or str from vCPU and render it #
        if isinstance(value,int):
            char=chr(value&0xFF)
        else:
            char=str(value)
        for ch in char:
            self.drawChar(ch)
