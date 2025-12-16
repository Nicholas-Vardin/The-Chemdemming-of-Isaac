'''
Menu Widget Classes

By Nicholas Vardin

This file contains widgets like text boxes and buttons that can be used for menus and UI
'''


import basicFunctionsAndClasses as bFC
import pygame as p
import numpy as np
import pygameBasic as pb
import basicGameInfo as bGI

class textBox(bFC.drawableRect):
    '''Widget that displays text in a box'''
    def __init__(self, screen, clr:tuple, fontClr:tuple = (0,0,0), points = np.array([]), tLPos = np.array([]), width = -1,height = -1,
                 drawFilled:bool = True, drawBorder:bool = False, borderWidth:int =1,text:str = '',fontType:str = bGI.normalFont, textSize:int = 20):
        '''Initializes text box'''
        super().__init__(screen,clr,points = points, tLPos=tLPos,width = width,
                         height = height,drawFilled=drawFilled,borderWidth=borderWidth)
        
        self.drawBorder = drawBorder
        self.text = text
        self.font = p.font.SysFont(fontType, textSize)
        self.fontClr = fontClr

    def drawText(self):
        '''Draws text on text box'''
        textSurface = self.font.render(self.text,True,self.fontClr)
        textRect = textSurface.get_rect(center = bFC.npArrayIntoTuple(self.getCenter()))
        self.screen.blit(textSurface,textRect)

        
    def draw(self):
        '''draws the text box'''
        if self.drawFilled:
            self.drawFilledIn()
        elif self.drawBorder:
            self.drawOutline()
        self.drawText()
        

class button(textBox):
    '''Button widget that has text and contains its clicked status'''
    def __init__(self, screen, clr, fontClr:tuple = (0,0,0), points=np.array([]), tLPos=np.array([]), 
                    width=-1, height=-1, drawFilled = True, drawBorder = False, 
                    borderWidth = 1, text = '', fontType = 'Arial', textSize = 20):
        '''Initializes button'''
        super().__init__(screen, clr, fontClr, points, tLPos, width, height, drawFilled, drawBorder, 
                            borderWidth, text, fontType, textSize)
        
        self.mouseDown = p.mouse.get_pressed()[0]
        self.state = None
        self.clicked = False
        self.obtainMouseInfo()
        

    def update(self):
        '''updates button'''
        self.obtainMouseInfo()

        if not self.prevMouseDown and not self.mouseDown:
            self.state = 'untouched'
    
        elif not self.prevMouseDown and self.mouseDown and self.mouseAbove:
            self.state = 'clicked'
            self.clicked = True
        
        elif self.prevMouseDown and self. mouseDown and self.clicked:
            self.state = 'held'
        
        elif self.prevMouseDown and not self.mouseDown and self.clicked:
            self.state = 'released'
            self.clicked = False
            


    def obtainMouseInfo(self):
        '''Obtains if mouse is hovering and clicking over the button''' 
        self.prevMouseDown = self.mouseDown
        self.mouseDown = p.mouse.get_pressed()[0]
        self.mouseAbove = self.pointIn(bFC.tupleIntoNPArray(p.mouse.get_pos()))
        

#testing code
class test:
    def __init__(self):
        self.screen, self.clock = pb.setup(600,600)
        self.tBox = textBox(self.screen,(255,0,0),tLPos=bFC.tupleIntoNPArray((100,100)),width = 200,height = 100,drawFilled=False,drawBorder=True,text = 'Test',textSize= 60)
        self.testButton = button(self.screen,(0,255,0),tLPos= bFC.tupleIntoNPArray((300,300)),width = 200,height = 100,drawFilled=True,text = 'I am a button', textSize= 40)
    
    def update(self):
        self.screen.fill((255,255,255))
        self.testButton.update()

    def draw(self):
        self.screen.fill((255,255,255))
        self.tBox.draw()
        self.testButton.draw()

def main():
    oTest = test()
    pb.run(oTest)

if __name__ == '__main__':
    main()