#!/usr/bin/python3
from datetime import datetime
from jsonmanager import JsonManager
import time
from termios import tcflush, TCIFLUSH
import sys
import os
import keyboard


class Printer:
    ESC = "\x1b"
    GS="\x1d"
    NUL="\x00"

    def __init__(self, printerpath):
        self.usbprinter = None
        self.printerpath = printerpath
        self.connect()
        
        # configura a impressora
        self.output = ""
        self.reset()
        self.output += Printer.ESC + "t" + chr(3)
        self.print()

    ### CONTROL METHODS ###

    def connect(self):
        print("Esperando conexao com impressora no caminho \033[1m\"" + self.printerpath + "\"\033[0m")
        while True:
            try:
                self.usbprinter = open(self.printerpath, 'w')
                print("Impressora conectada.")
                return True
            except:
                print("A conexao falhou. Certifique-se que o programa esta rodando como administrador.")

            time.sleep(2)

    def print(self):
        while True:
            try:
                self.usbprinter.write(self.output)
                self.usbprinter.flush()
                self.reset()
                return
            except:
                print("Impressora desconectada!")
                self.connect()
                time.sleep(2)

    def reset(self):
        self.output = Printer.ESC + "@" # Reset to defaults

    ### WRITING METHODS ###

    def onBold(self):
        self.output += Printer.ESC + "E" + chr(2); # Bold
    
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


def hello_world(printer):
    printer.alignCenter()
    printer.setTextSize(1)
    printer.addText("Impressora pronta!")
    printer.setTextSize(0)
    printer.addText(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    printer.addLine(4)
    printer.cut()
    printer.print()

def printClient(printer, ticket):
    printer.alignCenter()
    printer.setTextSize(2)
    printer.addText("Acai Express\n")
    printer.setTextSize(1)
    printer.addText("SENHA")
    printer.onBold()
    printer.setTextSize(6)
    printer.addText(ticket)
    printer.addLine(1)
    printer.setTextSize(1)
    printer.onUnderline()
    printer.addText("R$:         ")
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
    printer.addText("   1-1 Polpa de Acai   ")
    printer.addText("   2-2 Polpas de Acai  ")
    printer.addText("   3-Acai c/ banana    ")
    printer.addText("   4-Acai c/ maracuja  ")
    printer.addText("   5-Acai c/ chocolate ")
    printer.addText("   6-Acai c/ morango   ")
    printer.addText("   7-Acai c/ cupuacu   ")
    printer.addText("   8-Bomba c/          ")
    printer.addText("   9-Creme c/          ")
    printer.addText("   10-Acai c/          ")
    printer.offUnderline()

    printer.addText("")
    printer.addText("      S", False)
    printer.onUnderline()
    printer.addText("e", False)
    printer.offUnderline()
    printer.addText("m  Mu", False)
    printer.onUnderline()
    printer.addText("i", False)
    printer.offUnderline()
    printer.addText("to  Po", False)
    printer.onUnderline()
    printer.addText("u", False)
    printer.offUnderline()
    printer.addText("co")

    printer.onBold()
    printer.addText("Gelo", False)
    printer.offBold()

    printer.addText("  [", False)
    printer.onUnderline()
    printer.addText(" ", False)
    printer.offUnderline()
    printer.addText("]   [", False)
    printer.onUnderline()
    printer.addText(" ", False)
    printer.offUnderline()
    printer.addText("]    [", False)
    printer.onUnderline()
    printer.addText(" ", False)
    printer.offUnderline()
    printer.addText("]")

    printer.onBold()
    printer.addText("Doce", False)
    printer.offBold()
    
    printer.addText("  [", False)
    printer.onUnderline()
    printer.addText(" ]", False)
    printer.offUnderline()
    printer.addText("   [", False)
    printer.onUnderline()
    printer.addText(" ", False)
    printer.offUnderline()
    printer.addText("]   ", False)
    printer.onUnderline()
    printer.addText(" [ ", False)
    printer.offUnderline()
    printer.addText("]")

    printer.onBold()
    printer.addText("Levar", False)
    printer.offBold()

    printer.addText("  [", False)
    printer.onUnderline()
    printer.addText(" ", False)
    printer.offUnderline()
    printer.addText("] Sim   [", False)
    printer.onUnderline()
    printer.addText(" ", False)
    printer.offUnderline()
    printer.addText("] Nao")

    printer.addLine(3)
    printer.cut()
    printer.print()


def kbevent(event):
    # print(event.name)
    if event.name == "enter":
        printevent()


def printevent():
    global _json, ticket, printer, lastenter

    if time.time() - lastenter < 1.5:
        return

    lastenter = time.time()

    # reseta contagem de tickets caso o programa não seja reiniciado
    lastdate = datetime.strptime(_json.get("data"), "%Y-%m-%d %H:%M:%S.%f")
    if lastdate.date() < datetime.now().date():
        ticket = 1
        
    now = datetime.now()
    printClient(printer, ticket)
    printCompany(printer, ticket)
    print("Gerou senha " + str(ticket) + " em " + now.strftime("%d/%m/%Y as %H:%M:%S"))

    # salva ticket gerado e hora
    _json.set("ticket", ticket)
    _json.set("data", str(now))
    ticket += 1
    
    tcflush(sys.stdin, TCIFLUSH)


if __name__ == "__main__":
    time.sleep(5)  # espera o sistema terminar de acordar
    _json = JsonManager("contador")
    ticket = _json.get("ticket") + 1
    printerpath = _json.get("printer")
    print("O programa se conectara com a impressora no caminho \"" + printerpath + "\".")
        
    printer = Printer(printerpath)

    print("Pressione enter para gerar proximas senhas (proxima: %d)" % ticket)

    hello_world(printer)

    lastenter = time.time()
    keyboard.on_press(kbevent)

    while True:
        time.sleep(0.01)