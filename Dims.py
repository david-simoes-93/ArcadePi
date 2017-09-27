import numpy as np


def getPlaneEq(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # These two vectors are in the plane
    v1 = p3 - p1
    v2 = p2 - p1

    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp

    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    d = np.dot(cp, p3)

    #print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))

    return [a,b,c,d]

# x1,y1 is the center of the first circle, with radius r1
# x2,y2 is the center of the second ricle, with radius r2
def intersectTwoCircles(x1,y1,r1, x2,y2,r2):
    centerdx = x1 - x2;
    centerdy = y1 - y2;
    R = np.sqrt(centerdx * centerdx + centerdy * centerdy);
    if (not (np.abs(r1 - r2) <= R and R <= r1 + r2)): # no intersection
      return [] # empty list of results
    # intersection(s) should exist

    R2 = R*R;
    R4 = R2*R2;
    a = (r1*r1 - r2*r2) / (2 * R2);
    r2r2 = (r1*r1 - r2*r2);
    c = np.sqrt(2 * (r1*r1 + r2*r2) / R2 - (r2r2 * r2r2) / R4 - 1);

    fx = (x1+x2) / 2 + a * (x2 - x1);
    gx = c * (y2 - y1) / 2;
    ix1 = fx + gx;
    ix2 = fx - gx;

    fy = (y1+y2) / 2 + a * (y2 - y1);
    gy = c * (x1 - x2) / 2;
    iy1 = fy + gy;
    iy2 = fy - gy;

    # note if gy == 0 and gx == 0 then the circles are tangent and there is only one solution
    # but that one solution will just be duplicated as the code is currently written
    return [[ix1, iy1], [ix2, iy2]]

# return sum of element-wise multiplication of vectors
def scalarProduct(v1, v2):
    val = 0
    for (a,b) in zip(v1, v2):
        val += a*b
    return val

# return vector of p2 to p1
def vectorize(p1, p2):
    val = []
    for (a,b) in zip(p1, p2):
        val.append(a-b)
    return val

# return distance between 2 points
def dist(p1, p2):
    d = 0
    for l in vectorize(p1,p2):
        d += l*l
    return np.sqrt(d)


def getSideLengthOfTrapezium(bot, top, height):
	return np.sqrt( ((bot-top)/2)**2 + height**2)

def getClosestPointOnPlane(planeA, planeB, planeC, planeD, pointX, pointY, pointZ):
    # we want to find a point (pointX, pointY, pointZ)+t(planeA, planeB, planeC)
    # x = pointX + t*planeA
    # y = pointY + t*planeB
    # z = pointZ + t*planeC
    # planeA*x + planeB*y + planeC*z = planeD
    # planeA*pointX + t*planeA*planeA + planeB*pointY + t*planeB*planeB + planeC*pointZ + t*planeC*planeC = planeD
    # t = (planeD - planeA*pointX - planeB*pointY - planeC*pointZ) / (planeA*planeA + planeB*planeB + planeC*planeC)
    t = (planeD - planeA * pointX - planeB * pointY - planeC * pointZ) / \
        (planeA * planeA + planeB * planeB + planeC * planeC)
    return [pointX + t*planeA,pointY + t*planeB,pointZ + t*planeC]


botWidth = 50
topWidth = 35
height = 35
length = 40

baseHeight = 5
topLength = 5

joyPanelHeight = 20
screenPanelHeight = 30    # screen is 24*30

thickness = 1

print("Plank = 61 * 122 * 1")

print("Front Base ",botWidth,"*",baseHeight)

print("Joystick Panel ",botWidth,"*",joyPanelHeight)

screenPanelSide = getSideLengthOfTrapezium(botWidth, topWidth, screenPanelHeight)               # trapezium side length
print("Screen Panel [",botWidth,"to",topWidth,"]*",screenPanelHeight, ", side length of",screenPanelSide)

panelsIntersection = intersectTwoCircles(0,baseHeight,joyPanelHeight, length-topLength,height,screenPanelHeight)
if panelsIntersection == []:
    print("Configuration invalid!")
    exit()
panelsIntersection = panelsIntersection[0] if panelsIntersection[0][1]<panelsIntersection[1][1] else panelsIntersection[1] #pick lowest point
if panelsIntersection[1]<baseHeight:
    print("Configuration barely invalid!")
    exit()

sidePanelsIntersection = np.sqrt(panelsIntersection[1]**2+(length-panelsIntersection[0])**2)   # line between both side panels
print("Side Bottom Panel ",length,"*",baseHeight,"*",joyPanelHeight,"*",sidePanelsIntersection,". Peak at ",panelsIntersection)

sideTopPanelBack = np.sqrt(height**2+((botWidth-topWidth)/2)**2)                         # line between top side panel and back wall
basePoint = [length,0,0]
sidePoint = [panelsIntersection[0],panelsIntersection[1],0]
topFrontPoint = [length-topLength,height,(topWidth-botWidth)/2]
planeEq = getPlaneEq(basePoint, sidePoint, topFrontPoint)                   # plane formed by side top panel
topBackPoint = [length,height,(planeEq[3]-planeEq[0]*length-planeEq[1]*height)/planeEq[2]]

topPanelSide = getSideLengthOfTrapezium(topWidth, botWidth+topBackPoint[2]*2, topLength)              # trapezium side length
print("Top Panel [",topWidth,"to",botWidth+topBackPoint[2]*2,"] *",topLength, "side length of",topPanelSide)

angle = np.arccos(scalarProduct(vectorize(basePoint,sidePoint), vectorize(basePoint,topBackPoint))/(sideTopPanelBack*sidePanelsIntersection)) #*180/math.pi
sidePoint2d = [sidePanelsIntersection*np.cos(angle), sidePanelsIntersection*np.sin(angle)]
sideCorner2d = intersectTwoCircles(sidePoint2d[0],sidePoint2d[1],screenPanelSide, sideTopPanelBack,0,topPanelSide)
sideCorner2d = sideCorner2d[0] if sideCorner2d[0][1]>sideCorner2d[1][1] else sideCorner2d[1] #pick highest point
print("Side Top Panel ",sideTopPanelBack,"*",sidePanelsIntersection,"*",screenPanelSide,"*",topLength,". Peaks at ",sidePoint2d,"and",sideCorner2d)

baseOutPoint = [length,0,-thickness]
pointInPlane = getClosestPointOnPlane(planeEq[0],planeEq[1],planeEq[2],planeEq[3],
                                      baseOutPoint[0],baseOutPoint[1],baseOutPoint[2])     # get point in plane closest to baseOutPoint
dist1 = dist(basePoint, pointInPlane)                           # get distance of basePoint to pointInPlane
dist2 = dist(sidePoint, pointInPlane)                           # get distance of sidePoint to pointInPlane
baseOutPoint2d = intersectTwoCircles(0,0,dist1, sidePoint2d[0],sidePoint2d[1],dist2)[0]
print("    The first peak and bottom-right corner have a disjoint of ",baseOutPoint2d,"to account for thickness in a rotated plane")
#Front Base  rectangle 50 * 5
#Joystick Panel  rectangle 50 * 20
#Screen Panel trapezium [ 50 to 35 ]* 30 , side length of 30.9232921921
#Top Panel  rectangle 35 * 5
#Side Bottom Panel  (base, clockwise) 40 * 5 * 20 * 22.4779188619 . 
#    Peak at  [19.533561785152958, 9.294177917321548]
#Side Top Panel  (base, clockwise) 22.4779188619 * 30.9232921921 * 5 * 35.7945526582 . 
#    Peaks at  [9.0878696044219591, 20.558877946376406] and [34.65799234194052, 4.8691098413904044]