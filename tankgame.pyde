# -----------------------------------------------------------------------------------------------------------------------------------------------
# Project Name: Tank Game
#
# Author's: Ammar & Darren
#
# Last Edit Date: Friday June 4 2021
# Last Edit Time: 12:38
#
# Program Function/Description: Tanks move up and down. Sound when shoot, sound when play game, sound when win screen. E & CTRL to shoot
#
# Planning Document: N/A
#
# ------------------------------------------------------------------------------------------------------------------------------------------------

add_library('minim')
minim = Minim(this)

def loadFileInfo( fileName ):
    file = open( fileName )
    fileInfo = []
    text = file.readlines()
    
    for line in text:
        line = line.strip()
        line = line.split(",")
        fileInfo.append( line )
        
    numItems = len( fileInfo )
    file.close()
                                          
    return fileInfo, numItems 
    
def setup():
    global tank1, tank2, wall, bg, start_screen_image, red_win, blue_win, help_screen_image, red_score_board_image, blue_score_board_image, blow_up
    global objX, objY, objWidth, objHeight, objIncr, objImage, hitCount, boundaryPos, wallPos, losing_screen, tankControls, moveUp, moveDown, shootBullet, bulletDirection, current_tank, bulletDimensions
    global tank_info, wall_info, bulletList, top_bound, bottom_bound, right_bound, left_bound, win_count
    global controlKeys, whichKey, game_start, asciiList, mode
    global sound, blow_up, end_screen_blue, end_screen_red, shotSound, allSoundInfo, sound, winSound, numItems
    
    # loading sound and image files
    sound = minim.loadFile("game.mp3")
    winSound = minim.loadFile("winsound.mp3")
    
    # size of canvas / screen
    size (800,800)
    screenHeight = 799
    screenWidth = 799
    
    # load images
    tank1 = loadImage("tank1.png")
    tank2 = loadImage("tank2.png")
    wall = loadImage("brick wall.png")
    bg = loadImage("dirt.jpg")
    start_screen_image = loadImage("start screen.png")
    red_win = loadImage("winner screenred.png")
    blue_win = loadImage("winner screenblue.png")
    help_screen_image = loadImage("help screen.png")
    red_score_board_image = loadImage("red scoreboard.png")
    blue_score_board_image = loadImage("blue scoreboard.png")
    blow_up = loadImage("blowup.png")
    
    #variables
    bulletDimensions = 8 
    current_tank = 0
    
    bulletDirection = 0
    objX = 0
    objY = 1
    objWidth = 2
    objHeight = 3
    objIncr = 4
    objImage = 5
    hitCount = 6
    boundaryPos = 7
    wallPos = 8
    losing_screen = 9
    tankControls = 10
    moveUp = 0
    moveDown = 1
    shootBullet = 2
    
    # data list
    tank_info = [ [ 160, 400, 80, 80, 10, tank1, 0, 799, 350, red_win, [ UP, DOWN, CONTROL ] ] , [ 540, 400, 80, 80, 10, tank2, 0, 0, 395, blue_win, [ "w" , "s", "e" ] ] ]
    wall_info = [ 370, 170, 45, 480 ]
    bulletList = [ [1], [-1] ]
    
    
    # different modes and screen
    # start screen, game screen, help screen
    game_start = False
    mode = ""
    
    # boundaries 
    top_bound = 0
    left_bound = 0
    right_bound = screenWidth - bulletDimensions
    bottom_bound = screenHeight - tank_info[ 0 ][ objHeight ]
    
    # keys
    asciiList = "abcdefghijklmnopqrstuvwxyz"
    controlKeys = [ UP, LEFT, DOWN, RIGHT, CONTROL ]
    whichKey = ""
      
    # win count
    win_count = 6
    fill( 250 )
    
    # sound
    numFields = 0
    allSoundInfo = []
    shotSound = 1
    allSoundInfo, numItems = loadFileInfo("soundlist.txt")
    print( "the all sound info list", allSoundInfo )
    
    for i in range( numItems ):
        for j in range( 0 ):
            allSoundInfo[ i ][ j ] = int(  allSoundInfo[ i ][ j ] )
    for i in range( 1 ):
        allSoundInfo[ i ][ shotSound ] =  minim.loadSample( allSoundInfo[ i ][ shotSound ], 512)   
        
def end_screen( info_list, loser ): 
    global tank_info, losing_screen, hitCount, winSound, allSoundInfo
    
    image( info_list[loser][losing_screen], 0, 0, 800, 800 )
    winSound.play()
    textSize(37)
    textAlign(CENTER)
    text("Blue Score : %i" % (info_list[1][hitCount])  + "|Red Score: %i" % (info_list[0][hitCount]) , 400, 700 )
        
            
def draw():
    global game_start, mode, whichKey, win_count, tank_info, end_screen_red, end_screen_blue, game_over
    global objX, objY, objWidth, objHeight, objIncr, objImage, hitCount, boundaryPos, wallPos, losing_screen, tankControls, moveUp, moveDown, shootBullet
              
    if whichKey == "P" or whichKey == "p": # p key
        mode = "game screen"
        game_start = True
    if whichKey == "H" or whichKey == "h": # h key
        mode = "help screen"
    if whichKey == "b" or whichKey == "B": # b key
        mode = "back clicked"
    
    # different modes
    if game_start == False:
        image(start_screen_image, 0, 0, 800, 800)
        mode == "start screen"
    if mode == "start screen":
        image(start_screen_image, 0, 0, 800, 800)
        if mode == "back clicked" and game_start == False:
            image(start_screen_image, 0, 0, 800, 800)
    elif mode == "back clicked" and game_start == True:
        draw_game()
    if mode == "game screen" and game_start == True:
        draw_game()
    if mode == "help screen":
        image(help_screen_image, 0, 0, 800, 800)
        
    for i in range(2): # length of the tank list
        if tank_info[i][hitCount] == win_count:
            game_over = True
            end_screen( tank_info, i )
            
def draw_game():
    global whichKey, tank_info, wall_info, bulletList, current_tank, top_bound, bottom_bound, left_bound, right_bound, bulletDimensions, sound, blow_up
    global asciiList, current_tank, objX, objY, objWidth, objHeight, objIncr, objImage, hitCount, boundaryPos, wallPos, losing_screen, tankControls, moveUp, moveDown, shootBullet, bulletDirection
    global win_count, mode, end_screen_red, end_screen_blue, allSoundInfo, numItems, shotSound, sound, win_count, hitCount , game_start
    
    image(bg, 0, 0, 800, 800)
    game_over = False
    
    if game_over == False:
        sound.play()
    else:
        sound.stop()
        
    if tank_info[ 0 ][ hitCount ] <= win_count and tank_info[ 1 ][ hitCount ] <= win_count:
        for i in range( 2 ): # determining current tank based on controls used
            if whichKey != "" and whichKey in tank_info[ i ][ tankControls ]:
                current_tank = i
            
        if whichKey == tank_info[ current_tank ][ tankControls ][ moveUp ]:
            tank_info[ current_tank ][ objY ] -= tank_info[ current_tank ][ objIncr ]
            if tank_info[ current_tank ][ objY ] < top_bound:
                tank_info[ current_tank ][ objY ] = top_bound    
    
        elif whichKey == tank_info[ current_tank ][ tankControls ][ moveDown ]:
            tank_info[ current_tank ][ objY ] += tank_info[ current_tank ][ objIncr ]
            if tank_info[ current_tank ][ objY ] > bottom_bound:
                tank_info[ current_tank ][ objY ] = bottom_bound 
    
        elif whichKey == tank_info[ current_tank ][ tankControls ][ shootBullet ]:
            allSoundInfo[0][shotSound].trigger()
            bulletList[ current_tank ].append( [ tank_info[current_tank][objX] + tank_info[current_tank][objWidth] // 2, tank_info[current_tank][objY] + tank_info[current_tank][objHeight] // 2 ] )
            print(bulletList)
        
        for subBulletList in bulletList:
            for bullet in subBulletList[ 1: ]:
                bullet[objX] += 5 * subBulletList[ bulletDirection ]
                opposite_tank = 1 if (subBulletList[ bulletDirection ] == 1) else 0 
                wall_y_range = wall_info[ objY ] - bulletDimensions < bullet[ objY ] < wall_info[ objY ] + wall_info[objHeight]
                if wall_y_range and tank_info[0][ wallPos ] < bullet[ objX ] < tank_info[1][ wallPos]:
                    print("wall hit")
                    image(blow_up, bullet[objX]-10, bullet[objY]-10, 70, 50)
                    subBulletList.pop(subBulletList.index(bullet))
                
                elif bullet[objX] > right_bound or bullet[objX] < left_bound: #out of bounds
                    image(blow_up, bullet[objX]-10, bullet[objY]-10, 70, 50)
                    subBulletList.pop(subBulletList.index(bullet))
                    print(bulletList)
                
                tank_y_range = tank_info[ opposite_tank ][ objY ] < bullet[ objY ] < tank_info[ opposite_tank ][ objY ] + tank_info[ opposite_tank ][objHeight]
                if subBulletList[ bulletDirection ] == 1:
                    hit_tank = bullet[ objX ] > tank_info[ opposite_tank ][ objX ]
                elif subBulletList[ bulletDirection ] == -1:
                    hit_tank = bullet[ objX ] < tank_info[ opposite_tank ][ objX ] + tank_info[ opposite_tank ][ objWidth ]
                
                if tank_y_range and hit_tank: 
                    print("hit a tank")
                    image(blow_up, bullet[objX]-30, bullet[objY]-10, 70, 50)
                    subBulletList.pop(subBulletList.index(bullet))
                    tank_info[ opposite_tank ][ hitCount ] += 1
                    print( "red score",  "- blue score"  )
                
                
                rect( bullet[objX], bullet[objY], bulletDimensions, bulletDimensions )
    
    image (wall, wall_info[objX], wall_info[objY], wall_info[objWidth], wall_info[objHeight] )
    image (tank1, tank_info[0][objX], tank_info[0][objY], tank_info[0][objWidth], tank_info[0][objHeight] )
    image (tank2, tank_info[1][objX], tank_info[1][objY], tank_info[1][objWidth], tank_info[1][objHeight] )
    image (red_score_board_image, 655, -30, 200, 220)
    image (blue_score_board_image, -40, -50, 250, 250)
            
    textSize(76)
    redscoreboardtext = tank_info[ 1 ][ hitCount ]
    text(redscoreboardtext, 30, 125)
    
    textSize(76)
    bluescoreboardtext = tank_info[ 0 ][ hitCount ]
    text(bluescoreboardtext, 720, 125)
    
        
    whichKey = ""
    
def keyPressed():
    global mode, whichKey, asciiList, controlKeys, game_start

    if key == CODED:
       if keyCode in controlKeys:
        whichKey = keyCode
    elif key in asciiList:
        whichKey = key
    else:
        whichKey = ""
        
