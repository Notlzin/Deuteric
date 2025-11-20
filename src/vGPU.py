# vGPU.py: virtual GPU for Deuteric, screen size= 160px by 80px #
import sys
import re
sys.stdout.reconfigure(encoding='utf-8') # type: ignore

class vGPU:
    ANSI_PATTERN = re.compile(r'\033\[(.*?)m')
    def __init__(self,w=160,h=80):
        self.width = w
        self.height = h
        self.cursorX = 0
        self.cursorY = 0
        self.framebuffer = [[' ']*self.width for _ in range(self.height)]
        self.fg_color = None
        self.bg_color = None

    def clear(self):
        self.framebuffer = [[' ']*self.width for _ in range(self.height)]
        self.cursorX = 0
        self.cursorY = 0
        print("\033[2J\033[H", end="")

    def drawChar(self, char, color=None):
        if char == '\n':
            self.cursorX = 0
            self.cursorY += 1
        else:
            if self.cursorY < self.height:
                if color:
                    print(f"{color}{char}\033[0m", end='', flush=True)
                else:
                    print(char, end='', flush=True)
                self.framebuffer[self.cursorY][self.cursorX] = char
                self.cursorX += 1
                if self.cursorX >= self.width:
                    self.cursorX = 0         # go to start of next line
                    self.cursorY += 1        # move down one line
        if self.cursorY >= self.height:
            self.cursorY = self.height - 1

    def receive(self,value):
        # receive a byte (integer) or str from vCPU and render it
        if isinstance(value,int):
            char=chr(value&0xFF)
        else:
            char=str(value)

        # checker
        if not hasattr(self, "_gpuStdout"):
            self.hookStdout() # auto creator

        # uses new function
        self._gpuStdout.write(char)


    def hookStdout(self):
        class GPUStdout:
            def __init__(self, v_gpu):
                self.vgpu = v_gpu
                self.buffer = ''
            def write(self, string):
                parts = vGPU.ANSI_PATTERN.split(string)
                i = 0
                current_color = None
                while i < len(parts):
                    text = parts[i]
                    for char in text:
                        # drawChar handles '\n' internally
                        self.vgpu.drawChar(char, color=current_color)
                    i += 1
                    if i < len(parts):
                        seq = parts[i]
                        current_color = f'\033[{seq}m'
                        i += 1

            def flush(self):
                pass

        self._gpuStdout = GPUStdout(self)
        # sys.stderr = GPUStdout(self)
