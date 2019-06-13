from datetime import datetime
from jsonmanager import JsonManager
import time
from termios import tcflush, TCIFLUSH
import sys


class Printer:
    ESC = "\x1b"
    GS="\x1d"
    NUL="\x00"

    def __init__(self):
        try:
            self.usbprinter = open("/dev/usb/lp0", 'w')
        except:
            print("Impressora não alcançável.")
        
        # configura a impressora
        self.output = ""
        self.reset()
        self.output += Printer.ESC + "t" + chr(3)
        self.print()

    ### CONTROL METHODS ###

    def print(self):
        try:
            self.usbprinter.write(self.output)
            self.usbprinter.flush()
            self.reset()
        except:
            print("Não é possível escrever na impressora!")

    def reset(self):
        self.output = Printer.ESC + "@" # Reset to defaults

    ### WRITING METHODS ###

    def onBold(self):
        self.output += Printer.ESC + "E" + chr(1); # Bold
    
    def offBold(self):
        self.output += Printer.ESC + "E" + chr(0); # Not Bold

    def onUnderline(self):
        self.output += Printer.ESC + "\x2d" + chr(2)

    def offUnderline(self):
        self.output += Printer.ESC + "\x2d" + chr(0)

    def addText(self, text, newline=True):
        self.output += str(text) + ("\n" if newline else "")

    def setTextSize(self, width, height=None):
        if height == None: height = width
        if (0 <= width <= 7) and (0 <= height <= 7):
            self.output += Printer.GS + "!" + chr(16*width+height)
        else:
            raise ValueError('Width and height should be between 0 and 7 '
                    '(1x through 8x of magnification); got: '
                    'width={!r}, height={!r}'.format(width, height))

    def addLine(self, number=1):
        self.output += Printer.ESC + "d" + chr(number); # Blank line

    def alignCenter(self):
        self.output += Printer.ESC + "a" + chr(1); # Centered printing
    
    def alignLeft(self):
        self.output += Printer.ESC + "a" + chr(0); # Left printing

    def alignRight(self):
        self.output += Printer.ESC + "a" + chr(2); # Right printing

    def addBarcode(self, text):
        self.output += Printer.GS + "k" + chr(4) + text + Printer.NUL; # Print barcode

    def cut(self):
        self.output += Printer.GS + "V\x41" + chr(3); # Cut


def printClient(printer, ticket):
    printer.alignCenter()
    printer.setTextSize(1)
    printer.addText("SENHA")
    printer.onBold()
    printer.onUnderline()
    printer.setTextSize(6)
    printer.addText(ticket)
    printer.offUnderline()
    printer.offBold()
    printer.addLine(2)
    printer.setTextSize(0)
    printer.addText(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    printer.addLine(4)
    printer.cut()
    printer.print()

def printCompany(printer, ticket):
    printer.alignLeft()
    printer.setTextSize(1)
    printer.addText("Senha:", False)
    printer.onBold()
    printer.addText(ticket)
    printer.offBold()
    printer.setTextSize(0)
    printer.addText(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    printer.setTextSize(1)
    printer.onUnderline()
    printer.addText("                       ")
    printer.addText("1 - 1 Polpa de Acai    ")
    printer.addText("2 - 2 Polpas de Acai   ")
    printer.addText("3 - Acai c/ banana     ")
    printer.addText("4 - Acai c/ maracuja   ")
    printer.addText("5 - Acai c/ chocolate  ")
    printer.addText("6 - Acai c/ morango    ")
    printer.addText("7 - Acai c/ cupuacu    ")
    printer.addText("8 - Bomba c/           ")
    printer.addText("9 - Creme c/           ")
    printer.addText("10 - Acai c/           ")
    printer.offUnderline()
    printer.addText("")
    printer.onUnderline()
    printer.onBold()
    printer.addText("Gelo", False)
    printer.offBold()
    printer.addText("   Sem   P   M   G")
    printer.onBold()
    printer.addText("Doce", False)
    printer.offBold()
    printer.addText("   Sem   P   M   G")
    printer.offUnderline()
    printer.onBold()
    printer.addText("Levar", False)
    printer.offBold()
    printer.addText("  Sim    Nao")
    printer.addLine(4)
    printer.cut()
    printer.print()


if __name__ == "__main__":
    # printer = Printer()
    json = JsonManager("contador")
    ticket = json.get("ticket") + 1
    lastdate = datetime.strptime(json.get("data"), "%Y-%m-%d %H:%M:%S.%f")
    if lastdate.date() < datetime.now().date():
        print("Bom dia!")
        ticket = 1

    print("Pressione enter para gerar próximas senhas (próxima: %d)" % ticket)

    while True:
        input()  # faz esperar um enter
        now = datetime.now()
        # printClient(printer, ticket)
        # printCompany(printer, ticket)
        print("Gerou senha " + str(ticket) + " em " + now.strftime("%d/%m/%Y às %H:%M:%S"))
        # salva ticket gerado e hora
        json.set("ticket", ticket)
        json.set("data", str(now))
        ticket += 1
        time.sleep(1)
        tcflush(sys.stdin, TCIFLUSH)