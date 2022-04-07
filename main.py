from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Variables are defined here
goal=Entity(model=None, collider=None)
length=7
width=3
platforms=[] #list to store the platform cubes
left_right=[]
maxima=15 #Maximum distance that the platforms can go to
speed=1
level=1
flag=1 #To toggle hud
gravity=0.4
fs=1 #To toggle fullscreen

txt=Text(text=None)

def createGround():
    # Level text
    global txt
    txt=Text(text="Level: "+str(level), scale=1.8, x=-0.8, y=0.45, color=color.black, texture='brick')

    # Spawn
    ground=Entity(model='cube', color=color.white, texture='grass', collider='box', scale_y=0.5)
    ground.scale_x=width
    ground.scale_z=length
    ground.x=0
    ground.z=0
    ground.y=0

    # Final Destination
    global goal
    l=len(platforms)    
    goal=Entity(model='cube', color=color.rgb(209, 165, 165), texture='brick', collider='box')
    goal.scale_x=width
    goal.scale_z=length
    goal.x=platforms[l-1].x+width+1
    goal.z=platforms[l-1].z
    goal.y=platforms[l-1].y+1      

def createPlatforms(n):
    for j in range(n):

        # If level>4 then the lenght and width of the moving platforms are decreased
        # The logic is simple. Might me changed in the future updates
        if level>4:
            platform_length=random.randint(1,2)
            platform_width=random.randint(2,3)
        else:
            platform_length=random.randint(3,6)
            platform_width=random.randint(2,4)

        # Creates the moving platforms
        platform=Entity(model='cube', texture='white_cube', collider='box')
        platform.scale_x=platform_width
        platform.scale_z=platform_length
        platform.scale_y=0.5
        if len(platforms)>0:
            l=len(platforms)
            platform.x=platforms[l-1].x+width+1
        else:
            platform.x=width+1

        platform.y=j+1.5 #Change this to change the height of platforms spawning
        platform.z=0
        
        # This logic here assigns a random platform with special privileges. 
        # Creation of special platforms
        selection=random.randint(0,3)
        if selection==2:
            platform.tagValue=1
            platform.color=color.rgb(82, 156, 217)
        else:
            platform.tagValue=0
            platform.color=color.rgb(200, 0, 0)
        platforms.append(platform) #The newly created platform is appended to a list of platforms

        # This here determines the speed of the moving platform and also the direction of movement depends on the value
        decision=random.randint(3,7)
        left_right.append(decision)

# Reset the platforms
def resetPlatforms():
    global platforms, left_right, speed
    for i in range(len(platforms)):
        destroy(platforms[i])
    destroy(goal)
    destroy(txt)
    platforms=[]
    left_right=[]
    player.z=0
    player.x=0
    player.y=0
    player.gravity=gravity
    speed=1

     

app=Ursina()
# Window Properties are defined here
window.title="Basic Parkour 3D"
window.exit_button.visible = False
window.fps_counter.enabled = False
window.cog_button.enabled=False



#Define audio files here
jump=Audio('assets/jump.mp3', autoplay=False, loop=False)
win=Audio('assets/win.mp3', autoplay=False, loop=False)
lose=Audio('assets/lose.mp3', autoplay=False, loop=False)
bg=Audio('assets/bg.mp3', loop=True)

bg.play() #plays background music


# HUD Text
Text.default_resolution = 1080 * Text.size
txt1=Text(text='Press H to hide the text on screen', origin=(0,-6,0), scale=1.1, color=color.black)
txt2=Text(text='Press F once to enter fullscreen mode. Press F thrice to return to window mode', origin=(0,-3,0), scale=1.1, color=color.black)
txt3=Text(text="Use W,A,S,D to move around. Space to jump", origin=(0,0,0), scale=1.1, color=color.black)
txt4=Text(text="If the game glitches, press R to restart the level",  origin=(0,3,0), scale=1.1, color=color.black)
txt5=Text(text="Press ESC to exit",  origin=(0,6,0), scale=1.1, color=color.black)

def input(key):
    global flag, gravity, fs
    if key=='escape':
        quit()
    if key=='space':
        jump.play()
    if key=='h':
        flag=flag*-1
    if key=='r':
        resetPlatforms()
        createPlatforms(level)
        createGround()
    if key=='f':
        fs=fs*-1
        if fs==-1:
            window.fullscreen=True
        elif fs==1:
            window.fullscreen=False
        resetPlatforms()
        createPlatforms(level)
        createGround()
        
        
    # This Flag variable controls whether to show the HUD or not
    if flag==1:
        txt1.enable()
        txt2.enable()
        txt3.enable()
        txt4.enable()
        txt5.enable()
    elif flag==-1:
        txt1.disable()
        txt2.disable()
        txt3.disable()
        txt4.disable()
        txt5.disable()
        


def update():
    global speed, level

    for i in range(len(platforms)):
        if abs(platforms[i].z)>maxima:
                speed=speed*-1

        if left_right[i]%2==0: #Left movement
            platforms[i].z=platforms[i].z+time.dt*left_right[i]*speed

        elif left_right[i]%2!=0: #Right movement
            platforms[i].z=platforms[i].z-time.dt*left_right[i]*speed
        
        if player.intersects(platforms[i]).hit: #Checks if the player lands on a moving platform ot not
            if left_right[i]%2==0:
                player.z += left_right[i]*time.dt*speed
            elif left_right[i]%2!=0:
                player.z -= left_right[i]*time.dt*speed

            if(platforms[i].tagValue==1): #checks for the availability of a special platform
                player.gravity=gravity/2
            elif(platforms[i].tagValue==0):
                player.gravity=gravity

        if player.intersects(goal).hit: #Checks if the player lands on the final platform or not
            win.play() #plays the win music
            level=level+1
            resetPlatforms()
            createPlatforms(level)
            createGround()
        
        if player.y<-40:
            quit()

            
    
sky=Sky() #creates a default sky
createPlatforms(level) #Creates the moving platforms
createGround() #Creates the spawn, updates the level and creates the final platform


player=FirstPersonController(collider='box')
player.gravity=gravity
player.z=0
player.x=0
player.cursor.enabled=False #Disables the default cursor



app.run()