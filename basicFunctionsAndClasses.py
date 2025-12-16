'''
Basic Functions and Classes

By: Nicholas Vardin

A program the contains basic functions and classes for simple
games and simulations using pygame and pymunk.
'''
import pygame as p
import pygame.gfxdraw
import numpy as np
import pygameBasic as pb
import math
import npVectorMath as npVM
import basicGameInfo as bGI
import pymunk as pk



'''Numpy and Tuple Functions'''
def npArrayIntoTuple(ar:np.ndarray):
    '''Takes in a single 1 by 2 np array and puts it into a tuple'''
    return (ar[0],ar[1])

def tupleIntoNPArray(t:tuple):
    '''Turns a tuple of length 2, into a 1x2 np array'''
    return np.array([t[0],t[1]])

def tuplesIntoNpArray(tuples:list):
    '''Turns iterable of tuples into a np array of np arrays'''
    array = np.array([np.array([float(t[0]),float(t[1])]) for t in tuples])
    return array

def NParraysIntoTuples(arrays:list):
    "Takes in an iterable of np arrays with 2 rows 1 collumn and turns it into a list of tuples with 2 elements"
    t = [(float(arrays[i][0]),float(arrays[i][1])) for i in range(len(arrays))]
    return t

def getTuplesFromLine(line:str,dataTypeInTuple = str):
    '''Extracts data in the form of tuples from a str
    - Data type in tuple is the data type object that is not called
    - ex float or int without brackets'''
    lTuples = [] #initializes list of tuple
    currentTuple = ''
    tupleState = 'None' #state variable to know when the tuple is open or closed
    for s in line: #go through the string looking for brackets and the characters in the tuple
        if s == '(' and tupleState == 'None':
            tupleState = 'open'
        if tupleState == 'open':
            currentTuple += s
        if s == ')': #if the close bracket is found add the tuple to the list of tuples and continue going parsing the string
            tupleState ='None'
            lTuples.append(getTuplefromString(currentTuple,dataTypeInTuple)) 
            currentTuple = ''
    return lTuples
               
def getTuplefromString(sTuple:str,dataTypeInTuple = str):
    '''Turns a tuple that is in string form into a tuple.
    - Does Not Work on tuples inside tuples
    - Data type in tuple is the data type object that is not called
    - ex float or int without brackets'''
    if not ('(' in sTuple and ',' in sTuple and ')' in sTuple): #makes sure string can be a tuple
        raise Exception('Inputted string is not a tuple:', sTuple)
    lTuple = []
    commaLookStart = 1 #starts at the first character thats not the bracket
    for i in range(sTuple.count(',')):
        commaIndex = sTuple[commaLookStart:].index(',') +commaLookStart #get the index value of the comma
        lTuple.append(dataTypeInTuple(sTuple[commaLookStart:commaIndex]))
        commaLookStart = commaIndex +1
    
    lTuple.append(dataTypeInTuple(sTuple[commaLookStart:-1]))#doesnt include end bracket
    
    return tuple(lTuple)



'''Geometry Functions

Most collision algorithms are obtained from
https://www.jeffreythompson.org/collision-detection/line-line.php'''

def getRectPointsFromTLPos(tLPos: np.ndarray,width,height):
    '''Turns a tlPos into a np.array with ordered points going
    Top Left
    Top Right
    Bottom Right
    Bottom Left'''
    tLPos = np.array([float(tLPos[0]),float(tLPos[1])]) 
    return np.array([tLPos,[tLPos[0]+width,tLPos[1]],
                     [tLPos[0]+width,tLPos[1]+height],
                     [tLPos[0],tLPos[1]+height]])

def pointLineCollision(point,p1,p2):
    '''Returns if a point is colliding with a line within a threshold to handle float point errors'''
    tPoint = npArrayIntoTuple(point)
    dist1 = math.dist(npArrayIntoTuple(p1),tPoint) #distances from end points of line to point
    dist2 = math.dist(npArrayIntoTuple(p2),tPoint)
    
    length = math.dist(npArrayIntoTuple(p1),npArrayIntoTuple(p2))

    buffer = .001 #the threshold amount used to handle float point errors

    return dist1+dist2 >= length-buffer and dist1+dist2 <= length+buffer #returns if point is on the line

def lineLineCollision(p1:np.ndarray,p2:np.ndarray,p3:np.ndarray,p4:np.ndarray):
    '''Checks if two straight lines intersect, returns true if they do and false if they dont,
    p1 and p2 are for line 1, p3 and p4 are for line 2'''
    x1,x2,x3,x4 = p1[0],p2[0],p3[0],p4[0] #renames the variables
    y1,y2,y3,y4 = p1[1],p2[1],p3[1],p4[1]

    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1) 
    if denom == 0: #avoids div by 0 error
        return False

    else:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    
        if 0<=uA<=1 and 0<=uB<=1:
            return True
        return False

def pointInPolygon(lPoints:np.ndarray,point :np.ndarray):
    '''Checks if a point is inside a polygon by checking how many times 
    a ray drawn from the point infinitely to the right collidies with the edges of the polygon, 
    returns true or false'''
    numberOfCollisions = 0

    for i in range(len(lPoints)): #check if the drawn ray collides with each edge
        current = i
        if i == len(lPoints)-1:
            next = 0
        else:
            next = i+1

        if lineLineCollision(point,np.array([point[0]+10000000000,point[1]]),
                                    lPoints[current],lPoints[next]):
            numberOfCollisions +=1
        
    if numberOfCollisions%2 == 0: #checks if num collisions is even or odd
        return False
    return True       

def pointInCircle(point:np.ndarray, center:np.ndarray,radius:float):
    '''Returns if a point is inside a circle'''
    distance = math.dist(npArrayIntoTuple(point),npArrayIntoTuple(center))
    return distance <= radius

def linePolygonCollision(p1,p2,lPoints):
    '''Returns true or false if a line is colliding with a polygon'''
    current = lPoints[-1]
    for next in lPoints: #checks if the line and any of the polygons edges are colliding
        if lineLineCollision(p1,p2,current,next):
            return True
        current = next
    if pointInPolygon(lPoints,p1): #checks if whole line is in polygon
        return True
    return False


def circleCircleCollision(center1:np.ndarray,radius1:float,center2:np.ndarray, radius2:float):
    '''Returns true or false if 2 circles are colliding'''
    distance = math.dist(npArrayIntoTuple(center1),npArrayIntoTuple(center2))
    return distance <= radius1+radius2

def polygonPolygonCollision(lPoints1:np.ndarray,lPoints2:np.ndarray):
    '''Checks if 2 polygons are colliding with eachother, returns true or false'''
    #check if edges collide
    current1 = lPoints1[-1]
    for next1 in lPoints1:
        current2 = lPoints2[-1]
        for next2 in lPoints2:
            if lineLineCollision(current1,next1,current2,next2):
                return True
            current2 = next2
        current1 = next1
    #check if any points are inside eachother
    #rect 1 inside rect 2
    if pointInPolygon(lPoints2,getCenter(lPoints1)):
        return True
    #rect2 inside rect1
    if pointInPolygon(lPoints1,getCenter(lPoints2)):
        return True
    return False

def getCenter(lPoints:np.ndarray):
    '''Gets the center point of a polygon
    - returns a numpy array'''
    total = np.array([0.0,0.0])
    for point in lPoints:
        total = np.add(total,point)
    return np.divide(total,np.array([len(lPoints),len(lPoints)]))

def lineCircleCollision(p1,p2,center,radius):
    '''Returns true or false if a circle is colliding with a line'''

    #checks if circle is colliding with ends of line
    inside1 = pointInCircle(p1,center,radius)
    inside2 = pointInCircle(p2,center,radius)

    if inside1 or inside2: return True

    length = math.dist(npArrayIntoTuple(p1),npArrayIntoTuple(p2))
    dot = (((center[0]-p1[0])*(p2[0]-p1[0])) + ((center[1]-p1[1])*(p2[1]-p1[1])))/(length**2)

    #gets the closest point on the line to the circle
    closestX = p1[0] +(dot*(p2[0]-p1[0]))
    closestY = p1[1] + (dot*(p2[1]-p1[1]))

    #check if circles closest point is on the line
    onSegment = pointLineCollision(tupleIntoNPArray((closestX,closestY)),p1,p2)
    if not onSegment: 
        return False
    

    #checks if distance between the center and the closest point on the line is <= radius
    distance = math.dist(tupleIntoNPArray(center),(closestX,closestY))
    # print(distance,radius)
    return distance<= radius

def polygonCircleCollision(lPoints:np.ndarray,center:np.ndarray,radius):
    '''Returns true or false if a circle is colliding with a polygon'''
    #check if the circle is colliding with any edge
    prev = lPoints[-1]
    
    for point in lPoints:
        if lineCircleCollision(point,prev,center,radius):
            return True
        prev = point
    
    #check if circle is inside polygon
    if pointInPolygon(lPoints,center):
        return True
    return False

def getPosDifBetweenRectCircle(lPoints,center,radius):
    '''Returns the delta pos vector starting from rectangle edge going to circle center
    based on the rectangles closest point on its edge to the circle
    -Rectangle cannot be rotated and must have the point order TL,TR,BR,BL'''
    
    closestPoint = getClosestPointOnRectToCircle(lPoints,center,radius)

    return getDistanceVectorBetween2Points(closestPoint,center)
    
       
def getClosestPointOnRectToCircle(lPoints,center,radius):
    '''Gets the closest point on rectange to a cicle
    Rectangle cannot be rotated and must have the points in order TL, TR,BR,BL
    Returns numpy array [x,y]'''
    if lPoints[0][0] < center[0]<  lPoints[1][0]: #if circle center is inbetween horizontal bounds
        closestX = center[0] #current x is closest
    else:
        if abs(lPoints[0][0]-center[0]) < abs(lPoints[1][0]-center[0]): # if circle is outside horizontal bounds
            closestX = lPoints[0][0]
        else:   
            closestX = lPoints[1][0] #closest corner x is closest
            
    if lPoints[0][1] < center[1]<  lPoints[3][1]: #if circle center is inbetween vertical bounds
        closestY = center[1] #current y is closest
    else: # if circle is outside vertical bounds
        if abs(lPoints[0][1]-center[1]) < abs(lPoints[3][1]-center[1]):
            closestY = lPoints[0][1] #closest corner y is closest
        else:
            closestY = lPoints[3][1]
    return np.array([closestX,closestY])
    

def getDistanceVectorBetween2Points(p1,p2):
    '''Gets the direction vector from point 1 to point 2'''
    return np.subtract(p2,p1)

def getXAndYOverlapsBetweenRects(lPoints1,lPoints2):
    '''returns 2 boul for x and y overlap
    Rectangles must have the points in order TL, TR,BR,BL and cannot be rotated'''
    #check for x overlap
    if lPoints2[0][0] <= lPoints1[0][0] <= lPoints2[1][0] or lPoints2[0][0]<=lPoints1[1][0] <= lPoints2[1][0]:
        xOverlap = True
    else:
        xOverlap = False
    
    #check for y overlap
    if lPoints2[0][1]<=lPoints1[0][1] <= lPoints2[3][1] or lPoints2[0][1] <= lPoints1[3][1] <= lPoints2[3][1]:
        yOverlap = True
    else:
        yOverlap = False
    
    return xOverlap,yOverlap
    

def getDistanceBetween2RectsEdges(lPoints1,lPoints2):
    '''Returns the distance between the closest points on the edges of 2 rectangles
    - Rectangles must have the points in order TL, TR,BR,BL
    -rectangles cannot be rotated
    -if rectangles are inside eachother returns a distance of 0'''
    
    xOverlap,yOverlap = getXAndYOverlapsBetweenRects(lPoints1,lPoints2)
    
    if xOverlap and yOverlap: #if rectangles are completely overlapping eachother
        return 0
        
    elif xOverlap and not yOverlap:
        return min(abs(lPoints1[0][1]-lPoints2[3][1]),abs(lPoints1[3][1]-lPoints2[0][1]))
    elif not xOverlap and yOverlap:
        return min(abs(lPoints1[0][0]-lPoints2[1][0]),abs(lPoints1[1][0]-lPoints2[0][0]))
    else: #find smallest distance between corners
        return min(math.dist(lPoints1[0],lPoints2[2]),
                   math.dist(lPoints1[1],lPoints2[3]),
                   math.dist(lPoints1[2],lPoints2[0]),
                   math.dist(lPoints1[3],lPoints2[1]))

def getLineIntersectRowColQuadrants(p1,p2):
    '''gets the tile index values that a line overlaps,
    used for enemy vision'''
    p1 = np.array([p1[0]/bGI.basicTileWidth,p1[1]/bGI.basicTileHeight]) #turns points in tile coordinates
    p2 = np.array([p2[0]/bGI.basicTileWidth,p2[1]/bGI.basicTileHeight])
    
    startRowCol = (int(p1[1]),int(p1[0])) #starting rows and collumns that to iterate from
    endRowCol = (int(p2[1]),int(p2[0])) #ending rows and collumns to iterate to
    
    intersectedRowCols = {startRowCol,endRowCol} #adds the starting and end row cols to the overlapped set

    if p1[0]<= p2[0]: #if first point is left of second point
        slope = (p2[1]-p1[1])/(p2[0]-p1[0]) # get slope
        currentRow = startRowCol[0]
        for col in range(startRowCol[1]+1,endRowCol[1]+1): #go through the collumns and check which rows the line goes through
            calculatedRow = p1[1] + slope*(col-p1[0])
            calculatedRow = int(calculatedRow)
            if currentRow <= calculatedRow:
                for row in range(currentRow,calculatedRow+1):
                    intersectedRowCols.add((row,col-1))
            else:
                for row in range(calculatedRow,currentRow+1):
                    intersectedRowCols.add((row,col-1))
            currentRow = calculatedRow
        if currentRow< endRowCol[0]: #adds the ending rowcols
            for row in range(currentRow,endRowCol[0]+1):
                intersectedRowCols.add((row,endRowCol[1]))
        else:
            for row in range(endRowCol[0],currentRow+1):
                intersectedRowCols.add((row,endRowCol[1]))
    elif p1[0]> p2[0]: #do the same thing as above except start from endrowcol and go to startrowcol 
        slope = (p1[1]-p2[1])/(p1[0]-p2[0])
        currentRow = endRowCol[0]
        for col in range(endRowCol[1]+1,startRowCol[1]+1):
            calculatedRow = p2[1] + slope*(col-p2[0])
            calculatedRow = int(calculatedRow)
            if currentRow <= calculatedRow:
                for row in range(currentRow,calculatedRow+1):
                    intersectedRowCols.add((row,col-1))
            else:
                for row in range(calculatedRow,currentRow+1):
                    intersectedRowCols.add((row,col-1))
            currentRow = calculatedRow
        if currentRow< endRowCol[0]: 
            for row in range(currentRow,startRowCol[0]+1):
                intersectedRowCols.add((row,startRowCol[1]))
        else:
            for row in range(startRowCol[0],currentRow+1):
                intersectedRowCols.add((row,startRowCol[1]))
 
    return intersectedRowCols #returns the set of all intersected tiles row col values

'''Other Functions'''
def xYNPArrayIntoRoomLayoutRowColTuple(xYArray):
    '''turns pos np array into tile values'''
    x = xYArray[0]
    y = xYArray[1]
    if x == 0:
        col = 0
    else:
        col =int(x//bGI.basicTileWidth)
    if y == 0:
        row = 0
    else:
        row = int(y//bGI.basicTileHeight)
    return (row,col)

def getObjectFromListUsingUniqueBody(body,lObjects):
    '''Return the object with that has the inputted body'''
    for object in lObjects:
        if object.body ==body:
            return object
    return False
'''Classes'''

class rect:
    '''Basic Rectangle object for other classes to be based off'''
    geometry = 'rect' #shape identifier
    def __init__(self,points : np.ndarray= np.array([]) , tLPos: np.ndarray = np.array([]), width = -1,height = -1):
        '''Rectangle is defined using points that are stored in order in a numpy array or top left position occompanied by height and width.
        If both are given, points will trumpt top left position
        - If points are given, they can be rotated'''
        self.checkCorrectPointDeclaration(points,tLPos,height,width) #makes sure points or tLPos is properly declared
        
        if len(points) != 0: #if rectangle is defined by ordered points
            self.points = points
        
        else: #If rectangle is defined by top left point
            self.points = getRectPointsFromTLPos(tLPos,width,height)

    def getWidth(self):
        '''Returns the largest x distance from 2 points'''
        return max(abs(self.points[0][0]-self.points[2][0]),
                   abs(self.points[1][0]-self.points[3][0]))

    def getHeight(self):
        '''Returns the y distance from top'''
        return max(abs(self.points[0][1]-self.points[2][1]),
            abs(self.points[1][1]-self.points[3][1]))
    
    def getAvgWidth(self):
        '''returns the width of the rectangle as if its not rotated'''
        return (abs(self.points[0][0]-self.points[2][0])+abs(self.points[1][0]-self.points[3][0]))/2

    def getAvgHeight(self):
        '''returns the height of the rectangle as if its not rotated'''
        return (abs(self.points[0][1]-self.points[2][1])+abs(self.points[1][1]-self.points[3][1]))/2


    def getCenter(self):
        '''Returns 1x2 numpy array center position of rect'''
        return getCenter(self.points)
    
    def teleportBasedOnTLPos(self,tLPos:np.ndarray):
        '''Teleports the rectangle based on the top left position'''
        self.points = getRectPointsFromTLPos(tLPos,self.getWidth(),self.getHeight())
    
    def teleportBasedOnCenter(self,center:np.ndarray):
        '''Teleports the rectangle based on the center position'''
        newTLPos = np.subtract(center,np.array([self.getWidth()/2,self.getHeight()/2]))
        self.points = getRectPointsFromTLPos(newTLPos,self.getWidth(),self.getHeight())
    
    def checkCorrectPointDeclaration(self,points,tLPos,width,height):
        
        if (len(points) == 0 or type(points) == np.ndarray) and (len(tLPos) == 0 or width <0 or height <0 or type(tLPos) != np.ndarray): #checks if rectange points are properly defined for one of the two options
            raise Exception(f'Points are not properly defined for rectangle object points: {points}, tLPos: {tLPos}, width: {width}, height:{height}')
        return True

    def pointIn(self,point:np.ndarray):
        '''Checks if a point is inside the rectangle, returns true or false using the point in polygon function'''
        return pointInPolygon(self.points,point)  
       
class drawableRect(rect):
    '''A child of the rect class that can be drawn to the screen'''
    def __init__(self,screen:p.display, clr:tuple, points :np.ndarray = np.array([]), tLPos :np.ndarray = np.array([]),
                width=-1, height=-1, drawFilled = True,borderWidth:int = 1):
        super().__init__(points, tLPos, width, height)
        '''initializes object'''
        self.screen = screen
        self.clr = clr
        self.drawFilled = drawFilled
        self.borderWidth = borderWidth
    

    def drawFilledIn(self):
        '''Method to forcefully draw a filled rectangle even if it is not defined as filled'''
        drawablePoints = NParraysIntoTuples(self.points)
        pygame.gfxdraw.filled_polygon(self.screen,drawablePoints,self.clr)


    def drawOutline(self):
        '''Method to forcefully draw an outline of rectangle even if it is as filled'''
        drawablePoints = NParraysIntoTuples(self.points)
        pygame.draw.lines(self.screen,self.clr,True,drawablePoints, self.borderWidth)

    def draw(self):
        '''draw the rect to the screen'''
        if self.drawFilled:
            self.drawFilledIn()
        else:
            self.drawOutline()

class physicsRect:
    '''rect that is compatible with the physics engine pymunk,
    elasticity - how well object bounces off other 0-1,
    objects are automatically set to not being able to rotate'''
    geometry = 'rect' #shape identifier
    def __init__(self,screen,space,clr,center,width,height,collisionType:int,bodyType = pk.Body.STATIC,mass = 1,inertia = math.inf,elasticity =.6):
        '''initalize object'''
        #instantiates variables
        self.screen = screen
        self.clr = clr
        self.space = space
        self.width = width
        self.height = height

        if not (bodyType == pk.Body.DYNAMIC or bodyType == pk.Body.STATIC or bodyType == pk.Body.KINEMATIC): #checks for correct body type input 
            raise Exception('Body type is not valid')
        
        if bodyType != pk.Body.DYNAMIC: #defines the body
            self.body = pk.Body(body_type=bodyType)
        else:
            self.body = pk.Body(mass,inertia)
        
        self.body.position = pk.Vec2d(*center)
        
        self.shape = pk.Poly.create_box(self.body,(width,height)) #creates shape
        self.shape.elasticity = elasticity 
        self.shape.collision_type = collisionType #integer value used for the collision handler
        
    def addToSpace(self):
        '''adds the object to pymunk space'''
        self.space.add(self.body,self.shape)
    
    def removeFromSpace(self):
        '''removes the object from pymunk space'''
        self.space.remove(self.body,self.shape)
        
    def getLPoints(self):
        '''Returns np array of points in order of TL,TR,BR,BL'''
        lPoints = np.array([[self.body.position[0]-self.width/2,self.body.position[1]-self.height/2],
                            [self.body.position[0]+self.width/2,self.body.position[1]-self.height/2],
                            [self.body.position[0]+self.width/2,self.body.position[1]+self.height/2],
                            [self.body.position[0]-self.width/2,self.body.position[1]+self.height/2]])
        return lPoints
    
    def teleportBasedOnCenter(self,center):
        '''Teleports the object to a new center position
        - Center must have 2 sequential elements '''
        self.body.position = pk.Vec2d(*center)
    
    def draw(self):
        '''draws itself to the screen'''
        p.draw.rect(self.screen,self.clr,(self.body.position[0]-self.width/2,self.body.position[1]-self.height/2,self.width,self.height))
        
class circle:
    geometry = 'circle' #shape identifier
    def __init__(self,center:np.ndarray,radius:float):
        '''initialize function'''
        self.center = center
        self.radius = radius
    
    def pointIn(self,point:np.ndarray):
        '''Method to check if a point is inside self'''
        return pointInCircle(point,self.center,self.radius)

class drawableCircle(circle):
    '''a child of the circle class that can be drawn to the screen'''
    def __init__(self,screen:p.display, clr:tuple, center:np.ndarray, radius:float, drawFilled = True):
        super().__init__(center, radius)
        '''initialize object'''
        self.screen = screen
        self.clr = clr
        self.drawFilled = drawFilled

    def drawFilledIn(self):
        '''Method to forcefully draw a filled circle even if it is not defined as filled'''
        drawableCenter = npArrayIntoTuple(self.center)
        p.draw.circle(self.screen,self.clr,drawableCenter,self.radius)


    def drawOutline(self):
        '''Method to forcefully draw an outline of circle even if it is as filled'''
        pygame.gfxdraw.circle(self.screen,int(self.center[0]),int(self.center[1]),self.radius,self.clr)

    
    def draw(self):
        '''draws itself to screen'''
        if self.drawFilled:
            self.drawFilledIn()
        else:
            self.drawOutline()

class physicsCircle:
    '''A circle that is compatible with the pymunk physics engine
    elasiticiy - how well it bounces off things 0-1,
    by default cannot rotate'''
    geometry = 'circle'
    def __init__(self, screen,space,clr, center, radius, collisionType:int, bodyType = pk.Body.STATIC, mass = 1, inertia = math.inf,elasticity = .6):
        '''initialize object'''
        self.screen = screen
        self.clr = clr
        self.radius = radius
        self.space = space
        
        if not (bodyType == pk.Body.DYNAMIC or bodyType == pk.Body.STATIC or bodyType == pk.Body.KINEMATIC):
            raise Exception('Body type is not valid')
        
        if bodyType != pk.Body.DYNAMIC: #defines the circes body
            self.body = pk.Body(body_type=bodyType)
        else:
            self.body = pk.Body(mass,inertia)
            
        self.body.position = pk.Vec2d(*center)
        self.shape = pk.Circle(self.body,radius)
        self.shape.elasticity = elasticity
        self.shape.collision_type = collisionType #sets the collision type as an int used for the collision handler
            
    def addToSpace(self):
        '''adds itself to physics space'''
        self.space.add(self.body,self.shape)
    
    def removeFromSpace(self):
        '''removes itself from physics space'''
        self.space.remove(self.body,self.shape)
        
    def teleportBasedOnCenter(self,center):
        '''Teleports the object to a new center position,
        outdated however some functions may still use it'''
        self.body.position = pk.Vec2d(*center)
    
    def draw(self):
        '''Draws itself to screen'''
        p.draw.circle(self.screen,self.clr,self.body.position,self.radius)
    
class test:
    '''a test class used to test various features of this file,
    currently tests the distance between 2 rect edges function'''
    def __init__(self):
        self.screen, self.clock = pb.setup(600,600)
        self.rect1 = drawableRect(self.screen,(255,0,0),tLPos = np.array([100.0,200.0]), width = 100, height = 100)
        self.rect2 = drawableRect(self.screen,(0,255,0), tLPos = np.array([100.0,200.0]), width = 100, height = 100)
    def update(self):
        self.rect1.teleportBasedOnCenter(np.array([p.mouse.get_pos()[0],p.mouse.get_pos()[1]]))
        print(getDistanceBetween2RectsEdges(self.rect1.points,self.rect2.points))
    def draw(self):
        self.screen.fill((255,255,255))
        self.rect1.draw()
        self.rect2.draw()

def main():
    oTest = test()
    pb.run(oTest)

if __name__ == '__main__':
    main()