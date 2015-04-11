#TEST VALUES:
# BOUNCE OFF WALLS
# mass: 0.107
# force: 108
# gravity: 9.81
# friction: 0.2
# angle: 0

#BALL-BALL collision
# mass: 0.107
# force: 108
# gravity: 9.81
# friction: 0.2
# angle: 27
import Tkinter
import PIL.Image
from Tkinter import *
from visual import *
from visual.graph import *
import tkMessageBox
import math

scene=display()
scene.title='Billiards Simulation'
scene.autoscale=1
scene.fullscreen=0
scene.forward=(0,-1,-1)

running = True;
sidingLeft = 0
sidingRight = 0
sidingBottom = 0
sidingTop = 0
cueball = 0
collision = 0
ballMass = 0
initialForce = 0
worldGravity = 0
tableFriction = 0
shotAngle = 0
deltaT = 0
f1 = 0
f2 = 0

#Import Ball Textures
ballTex = [None] * 16
ballImage = [None] * 16
for x in xrange(0,16):
	ballImage[x] = PIL.Image.open('Textures/PoolBalls/'+str(x)+'.jpg')
	ballImage[x] = ballImage[x].resize((256,256), PIL.Image.ANTIALIAS)
	ballTex[x] = materials.texture(data=ballImage[x], mapping="rectangular")

#Simulation stuff
def drawTable():
	global f1
	global f2
	table = box(pos=(0,0,0), length=12.63, height=0.2, width=24.3, material=materials.rough, color=color.green)
	f1 = gcurve(color=color.cyan)
	global sidingLeft
	global sidingRight 
	global sidingBottom 
	global sidingTop
	global cueball
	global collision

	#average size in ft(9.32x4.65) * 2.5 +1 to scale up and allow for width of siding
	sidingLeft = box(pos=(-5.815,0.5,0), length=1, height=1, width=24.30, material=materials.wood)
	sidingRight = box(pos=(5.815,0.5,0), length=1, height=1, width=24.30, material=materials.wood)
	sidingBottom = box(pos=(0,0.5,11.65), length=12.63, height=1, width=1, material=materials.wood)
	sidingTop = box(pos=(0,0.5,-11.65), length=12.63, height=1, width=1, material=materials.wood)
	#0.203 ft is r of cueball
	cueball = sphere(pos = (0,0.4,-8), radius=0.203, material=ballTex[0], zCheck=False, xCheck=False, name="cueball")
	collision = [None]*15
	collision[0] = sphere(pos = (0,0.4,5), radius=0.203, material=ballTex[1], zCheck=False, xCheck=False, name="collision")
	collision[1] = sphere(pos = (0.5,0.4,5), radius=0.203, material=ballTex[15], zCheck=False, xCheck=False, name="collision2")
	collision[2] = sphere(pos = (1,0.4,5), radius=0.203, material=ballTex[2], zCheck=False, xCheck=False, name="collision3")
	collision[3] = sphere(pos = (-0.5,0.4,5), radius=0.203, material=ballTex[14], zCheck=False, xCheck=False, name="collision4")
	collision[4] = sphere(pos = (-1,0.4,5), radius=0.203, material=ballTex[3], zCheck=False, xCheck=False, name="collision5")
	collision[5] = sphere(pos = (0.25,0.4,4.5), radius=0.203, material=ballTex[13], zCheck=False, xCheck=False, name="collision6")
	collision[6] = sphere(pos = (-0.25,0.4,4.5), radius=0.203, material=ballTex[4], zCheck=False, xCheck=False, name="collision7")
	collision[7] = sphere(pos = (0.75,0.4,4.5), radius=0.203, material=ballTex[12], zCheck=False, xCheck=False, name="collision8")
	collision[8] = sphere(pos = (-0.75,0.4,4.5), radius=0.203, material=ballTex[5], zCheck=False, xCheck=False, name="collision9")
	collision[9] = sphere(pos = (-0.5,0.4,4), radius=0.203, material=ballTex[11], zCheck=False, xCheck=False, name="collision10")
	collision[10] = sphere(pos = (0,0.4,4), radius=0.203, material=ballTex[8], zCheck=False, xCheck=False, name="collision11")
	collision[11] = sphere(pos = (0.5,0.4,4), radius=0.203, material=ballTex[10], zCheck=False, xCheck=False, name="collision12")
	collision[12] = sphere(pos = (0.25,0.4,3.5), radius=0.203, material=ballTex[7], zCheck=False, xCheck=False, name="collision13")
	collision[13] = sphere(pos = (-0.25,0.4,3.5), radius=0.203, material=ballTex[9], zCheck=False, xCheck=False, name="collision14")
	collision[14] = sphere(pos = (-0,0.4,3), radius=0.203, material=ballTex[6], zCheck=False, xCheck=False, name="collision15")

	#graph setup
	f2 = [None]*15
	f2[0] = gcurve(color=color.red)
	f2[1] = gcurve(color=color.green)
	f2[2] = gcurve(color=color.blue)
	f2[3] = gcurve(color=color.yellow)
	f2[4] = gcurve(color=color.orange)
	f2[5] = gcurve(color=color.magenta)
	f2[6] = gcurve(color=color.white)
	f2[7] = gcurve(color=color.hsv_to_rgb((130,22,87)))
	f2[8] = gcurve(color=color.hsv_to_rgb((10,100,87)))
	f2[9] = gcurve(color=color.hsv_to_rgb((40,22,87)))
	f2[10] = gcurve(color=color.hsv_to_rgb((270,22,87)))
	f2[11] = gcurve(color=color.hsv_to_rgb((100,22,87)))
	f2[12] = gcurve(color=color.hsv_to_rgb((300,22,87)))
	f2[13] = gcurve(color=color.hsv_to_rgb((180,22,87)))
	f2[14] = gcurve(color=color.hsv_to_rgb((220,22,87)))


	return

#clculates x for velocity
def calcXComponent(hyp, angle):
	xVelocity = math.cos(math.radians(angle))*hyp
	return xVelocity

#calculates z fro velocity
def calcZComponent(hyp, angle):
	zVelocity = math.sin(math.radians(angle))*hyp
	return zVelocity

def calculateVelocity():
	global cueball
	global ballMass
	global initialForce
	global worldGravity
	global tableFriction
	global shotAngle
	global deltaT

	#velocity should start at 0,0,0
	#first is momentum using initial force
	# (F*deltaT+mv1)/m = v2
	v2 = ((initialForce*deltaT)+(ballMass*0))/ballMass

	#convert to ft/s to match table dimensions
	v2 = v2*3.2
	cueball.velocity = vector(calcXComponent(v2, shotAngle), 0, calcZComponent(v2, shotAngle))
	if cueball.velocity.x>0 and shotAngle<271 and shotAngle>89:
		cueball.velocity.x = -cueball.velocity.x
		cueball.xCheck = True
	else:
		cueball.xCheck = False

	if cueball.velocity.z>0 and shotAngle<361 and shotAngle>179:
		cueball.velocity.z = -cueball.velocity.z
		cueball.zCheck = True
	else:
		cueball.zCheck = False

	return v2
#this updates velocity for each time interval based on physics
def updateVelocity(ball, v2):
	global ballMass
	global initialForce
	global worldGravity
	global tableFriction
	global shotAngle
	global deltaT

	if v2<0.2 and v2>-0.2:
		v2 = 0
	else:
		#velocity needs to be updated with friction
		#friction coefficient for billiard table is 0.2
		forceFriction = tableFriction*worldGravity*ballMass
		v2 = v2/3.2 #ft/s - m/s
		v2 = ((-forceFriction*deltaT)+(ballMass*v2))/ballMass
		v2 = v2*3.2 #back to ft/s

		ball.velocity = vector(calcXComponent(v2, ball.angle), 0, calcZComponent(v2, ball.angle))
		if ball.zCheck == True:
			ball.velocity.z = -ball.velocity.z
		if ball.xCheck == True:
			ball.velocity.x = -ball.velocity.x
		ball.v2 = v2
	return ball

def hitWall(ball):
	if ball.pos.z > (sidingBottom.pos.z - sidingBottom.width):
		
		ball.pos.z = sidingBottom.pos.z - sidingBottom.width
		ball.velocity.z = -ball.velocity.z
		if ball.zCheck == False:
			ball.zCheck = True
		else:
			ball.zCheck = False
	if ball.pos.z < (sidingTop.pos.z + sidingTop.width):
		
		ball.pos.z = sidingTop.pos.z + sidingTop.width
		ball.velocity.z = -ball.velocity.z
		if ball.zCheck == True:
			ball.zCheck = False
		else:
			ball.zCheck = True

	#check if ball hits left or right
	if ball.pos.x < (sidingLeft.pos.x + sidingLeft.length):
		
		ball.pos.x = sidingLeft.pos.x + sidingLeft.length
		ball.velocity.x = -ball.velocity.x
		if ball.xCheck == True:
			ball.xCheck = False
		else:
			ball.xCheck = True
	if ball.pos.x > (sidingRight.pos.x - sidingRight.length):
		
		ball.pos.x = sidingRight.pos.x - sidingRight.length
		ball.velocity.x = -ball.velocity.x
		if ball.xCheck == True:
			ball.xCheck = False
		else:
			ball.xCheck = True
	return ball

def findDistance(ball1, ball2):
	distance = math.sqrt(math.pow((ball2.pos.x - ball1.pos.x), 2) + math.pow((ball2.pos.z - ball1.pos.z), 2))
	return distance

def checkCollision(ball1, ball2):
	if(ball1.radius+ball2.radius>findDistance(ball1, ball2)):
		return True

	return False

def recalculateVel(ball1, ball2):
	normal = (ball1.pos - ball2.pos)/(abs(ball1.pos-ball2.pos))
	dot1 = sum(p*q for p,q in zip(ball1.velocity, -normal))
	ball1.normalVel = dot1*(-normal)
	dot2 = sum(p*q for p,q in zip(ball2.velocity, normal))
	ball2.normalVel = dot2*normal
	ball1.tanCom = ball1.normalVel - ball1.velocity
	ball2.tanCom = ball2.normalVel - ball2.velocity
	ball1.velocity = ball1.tanCom + ball2.normalVel
	ball2.velocity = ball2.tanCom + ball1.normalVel
	
	return [ball1, ball2]

def recalcV2(ball):
	ball.v2 = math.sqrt(math.pow(ball.velocity.x, 2) + math.pow(ball.velocity.z, 2))
	ball.angle = math.degrees(math.acos(ball.velocity.x/ball.v2))
	return ball

def origAng(ball):
	ball.v2 = math.sqrt(math.pow(ball.velocity.x, 2) + math.pow(ball.velocity.z, 2))
	ball.angle = math.degrees(math.acos(ball.velocity.x/ball.v2))
	return ball
def giveChecks(ball):
		##calculate ball.angle
	ball = origAng(ball)
	if ball.velocity.x>0 and ball.angle<271 and ball.angle>89:
		ball.velocity.x = -ball.velocity.x
		ball.xCheck = True
	else:
		ball.xCheck = False

	if ball.velocity.z>0 and ball.angle<361 and ball.angle>179:
		ball.velocity.z = -ball.velocity.z
		ball.zCheck = True
	else:
		ball.zCheck = False
	return ball

def animate():
	global cueball
	global collision
	global deltaT

	deltaT = 0.005
	t = 0
	cueball.angle = shotAngle
	cueball.v2 = calculateVelocity()
	for x in xrange(0,15):
		collision[x].velocity=vector(0,0,0)
		collision[x].v2 = 0
		collision[x].xCheck = 42
		collision[x].zCheck = 42
	
	while running == True:
		while t<20:
			rate(100)
			end = 0
			#nothing to do with here
			#doesnt collide second time
			for x in xrange(0,15):
				if checkCollision(collision[x], cueball) :
					L = recalculateVel(cueball, collision[x])
					cueball = L[0]
					collision[x] = L[1]
					if(collision[x].xCheck == 42):
						collision[x] = giveChecks(collision[x])
					cueball = recalcV2(cueball)

					collision[x] = recalcV2(collision[x])

			for x in xrange(0,15):
				for z in xrange(0, 15):
					if x!= z:
						if checkCollision(collision[x], collision[z]) :

							L = recalculateVel(collision[z], collision[x])
							collision[z] = L[0]

							collision[x] = L[1]
							if(collision[x].xCheck == 42):
								if(collision[x].velocity.x !=0 or collision[x].velocity.z !=0):
									collision[x] = giveChecks(collision[x])
							if collision[z].xCheck ==42:
								if(collision[z].velocity.x !=0 or collision[z].velocity.z !=0):
									collision[z] = giveChecks(collision[z])

							if collision[z].velocity.z !=0 or collision[z].velocity.x !=0:
								collision[z] = recalcV2(collision[z])

							if collision[x].velocity.z !=0 or collision[x].velocity.x !=0:
								collision[x] = recalcV2(collision[x])


			
			for x in xrange(0,15):
				collision[x] = updateVelocity(collision[x], collision[x].v2)
				f2[x].plot(pos=(t,collision[x].v2))
				if(collision[x].v2<0.2 and collision[x].v2>-0.2):
					collision[x].v2 = 0
				end = end+collision[x].v2

			cueball = updateVelocity(cueball, cueball.v2)
			if(cueball.v2<0.2 and cueball.v2>-0.2):
				cueball.v2 = 0
			f1.plot(pos = (t, cueball.v2))
			end = end+cueball.v2
			for x in xrange(0,15):
				collision[x] = hitWall(collision[x])
			cueball = hitWall(cueball)

			cueball.pos = cueball.pos + cueball.velocity*deltaT

			for x in xrange(0,15):
				collision[x].pos = collision[x].pos+ collision[x].velocity*deltaT
			t=t+deltaT
			if end == 0:
				break
	return

#when start is pressed
def startSimulation():

	global ballMass
	global initialForce
	global worldGravity
	global tableFriction
	global shotAngle

	#gets the user inputted values
	ballMass = float(massname.get())
	initialForce = float(forcename.get())
	worldGravity = float(gravname.get())
	tableFriction = float(frictionname.get())
	shotAngle = float(anglename.get())

	
	drawTable()
	animate()
	return

#when stop is pressed 
def stopSimulation():
	running = False;

# GUI part
app = Tkinter.Tk()
app.title("Billiards Simulation")
app.geometry('400x500+200+200')

#label for top of simulation
labelText = StringVar()
labelText.set("Input Values For Simulation:")
label1 = Tkinter.Label(app, textvariable=labelText, font="bold",height=4)
label1.grid(row = 0, column = 0, padx=(10, 0), columnspan = 2)

#mass label
labelText=StringVar()
labelText.set("Mass of Balls (Kg): ")
labelMass=Tkinter.Label(app, textvariable=labelText, height=4)
labelMass.grid(row = 1, column = 0)

#textview for mass
mass=StringVar(None)
massname=Tkinter.Entry(app,textvariable=mass,width=10)
massname.grid(row = 1, column = 1)

#label for force
labelText=StringVar()
labelText.set("Initial Force (N): ")
labelForce=Tkinter.Label(app, textvariable=labelText, height=4)
labelForce.grid(row = 2, column = 0)

#textview for force
force=StringVar(None)
forcename=Tkinter.Entry(app,textvariable=force,width=10)
forcename.grid(row = 2, column = 1)

#label for gravity
labelText=StringVar()
labelText.set("Gravity (m/(s*s)): ")
labelGrav=Tkinter.Label(app, textvariable=labelText, height=4)
labelGrav.grid(row = 3, column = 0)

#textview for gravity
grav=StringVar(None)
gravname=Tkinter.Entry(app,textvariable=grav,width=10)
gravname.grid(row = 3, column = 1)

#label for friction
labelText=StringVar()
labelText.set("Table Friction Coefficient (~ 0.2): ")
labelFriction=Tkinter.Label(app, textvariable=labelText, height=4)
labelFriction.grid(row = 4, column = 0)

#textview for friction
friction=StringVar(None)
frictionname=Tkinter.Entry(app,textvariable=friction,width=10)
frictionname.grid(row = 4, column = 1)

#label for shot angle
labelText=StringVar()
labelText.set("Shot Angle (Degrees): ")
labelAngle=Tkinter.Label(app, textvariable=labelText, height=4)
labelAngle.grid(row = 5, column = 0)

#textview for friction
angle=StringVar(None)
anglename=Tkinter.Entry(app,textvariable=angle,width=10)
anglename.grid(row = 5, column = 1)

#start simulation button
start = Tkinter.Button(app, text="Start Simulation", width=17, command=startSimulation)
start.grid(row = 6, column = 0, padx=(10,0))

#stop simulation button
stop = Tkinter.Button(app, text="Stop Simulation", width=17, command=stopSimulation)
stop.grid(row = 6, column = 1, padx=(10,0))

app.mainloop()

