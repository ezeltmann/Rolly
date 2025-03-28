from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton

class SimpleMenu():
    def __init__(self):
        self.buttons = []
        self.backdrop = DirectFrame(frameSize = (-1, 1, -1, 1))

    def addButton(self, buttonText, buttonCommand):
        btn = DirectButton(text = buttonText,
                           frameSize = (-5, 5, -0.5, 1),
                           command = buttonCommand,
                           scale = 0.1,
                           parent = self.backdrop)
        self.buttons.append(btn)

    def layoutButtons(self):
        buttonSpacing = 0.2
        numButtons = len(self.buttons)

        topZ = (numButtons - 1) * 0.5 * buttonSpacing

        for btn in self.buttons:
            btn.setZ(topZ)

            topZ -= buttonSpacing

class SimpleGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.menu = SimpleMenu()

        self.menu.addButton("Kittens", self.kittenMethod)
        self.menu.addButton("Meowers", self.meowerMethod)
        self.menu.addButton("Add a Button", self.addButtonMethod)
        self.menu.layoutButtons()

    def kittenMethod(self):
        print ("Kittens!")

    def meowerMethod(self):
        print ("Meowers!")

    def addButtonMethod(self):
        self.menu.addButton("Cats!", self.catMethod)
        self.menu.layoutButtons()

    def catMethod(self):
        print ("Cats!")


game = SimpleGame()
game.run()