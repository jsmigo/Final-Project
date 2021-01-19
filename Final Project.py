# John Smigo
# Section 0201
# Final Project

import random
import PySimpleGUI as sg    # To intall using pip: python -m pip install pysimplegui

"""
This game is meant to be a challenging experience with different ways to go about it. 
You are a crew member on a transport ship that has been attacked by an unknown group.
You were asleep during the abduction and murder of the rest of the crew and you must do what you can to get home with the cryogenically frozen people on board

runner() is the main function for the game that processes events and takes input for movement through the map.
This function will update the main game window as necessary to present all possible paths and options.
The details of your location is passed into turn() which processes combat and loot collection
and returns updated stats and exits for the room.

Enjoy!
"""
def runner():
    rows, cols = (5,6)      # The game map is contained in a 5 x 6 array

    # The following lines are to initialize all the maps info so they can be filled later
    M = [[None for i in range(cols)] for j in range(rows)]
    enemy = [[False for i in range(cols)] for j in range(rows)]
    loot = [[False for i in range(cols)] for j in range(rows)]
    diff =[[0 for i in range(cols)] for j in range(rows)]
    loot_type = [[None for i in range(cols)] for j in range(rows)]
    item_types = ['Hlth','Dmg','Def','Spd']
    events1 = [[False for i in range(cols)] for j in range(rows)]
    event_list = [[None for i in range(cols)] for j in range(rows)]
    exits = [[None for i in range(cols)] for j in range(rows)]
    text = [[None for i in range(cols)] for j in range(rows)]
    avoid = [[True for i in range(cols)] for j in range(rows)]

    sg.theme('DarkAmber')

    # The next block of code makes up the coordinates and name for each of the exits in each room
    CQ1 = [(0,3,'Hallway 1')]
    Hlwy1 = [(0,1,'Rec Room'), (0,2,'Crew Quarters 2'), (0,4,'Hallway 2'), (2,4,'Cafeteria'), (0,0,'Crew Quarters 1')]
    RecRoom = [(0,3,'Hallway 1')]
    CQ2 = [(0,3,'Hallway 1')]
    Hlwy2 = [(0,5,'Library'), (1,0,'Classroom'), (1,1,'Hallway 3'), (0,3,'Hallway 1')]
    Lib = [(0,4,'Hallway 2')]
    Classroom = [(0,4,'Hallawy 2')]
    Hlwy3 = [(1,2,'Hallway 4'), (2,4,'Cafeteria'), (0,4,'Hallway 2'), (2,1,'Hallway 5')]
    Hlwy4 = [(1,3,'Engineering'), (1,5,'Holding Cell'), (2,0,'Cryogenics'),(1,1,'Hallway 3')]
    HC = [(1,2,'Hallway 4')]
    Cryogenics = [(1,2,'Hallway4')]
    Eng = [(1,2,'Hallway 4'), (1,4,'Engine Room')]
    EngineRoom = [(1,3,'Engineering')]
    Cafeteria = [(0,3,'Hallway 1'), (1,1,'Hallway 3'), (3,1,'Hallway 6'), (3,3,'Hallway 7'), (2,5,'Kitchen')]
    Kitchen = [(2,4,'Cafeteria'), (3,0,'Food Storage')]
    FoodStorage = [(2,5,'Kitchen')]
    Hlwy5 = [(1,1,'Hallway 3'), (2,2,'Agriculture'), (2,3,'Med Bay'), (3,1,'Hallway 6')]
    Ag = [(2,1,'Hallway 5')]
    MedBay = [(2,1,'Hallway 5')]
    Hlwy6 = [(2,1,'Hallway 5'), (3,2,'Crew Quarters 3'), (2,4,'Cafeteria'), (3,3,'Hallway 7'), (3,5,'Hallway 8')]
    CQ3 = [(3,1,'Hallway 6')]
    Hlwy7 = [(2,4,'Cafeteria'), (3,1,'Hallway 6'), (3,4,'Combat Training'), (4,2,'Navigation')]
    CmbtTraining = [(3,3,'Hallway 7'), (3,5,'Hallway 8')]
    Hlwy8 = [(3,1,'Hallway 6'), (3,4,'Combat Training'), (4,0,'Starboard Lounge'), (4,1,'Security')]
    StarboardLounge = [(3,5,'Hallway 8')]
    Security = [(3,5,'Hallway 8'), (4,2,'Navigation')]
    Nav = [(3,3,'Hallway 7'), (4,1,'Security'), (4,3,'Captains Quarters'), (4,4,'Bridge')]
    CptQ = [(4,2,'Navigation')]
    Bridge = [(4,2,'Navigation')]
    
    # This line combines the exits into a 5 x 6 array so it can be passed on later
    exits2D = [[CQ1,RecRoom,CQ2,Hlwy1,Hlwy2,Lib],[Classroom,Hlwy3,Hlwy4,Eng,EngineRoom,HC],[Cryogenics,Hlwy5,Ag,MedBay,Cafeteria,Kitchen],[FoodStorage,Hlwy6,CQ3,Hlwy7,CmbtTraining,Hlwy8],[StarboardLounge,Security,Nav,CptQ,Bridge,[(5,5,'None')]]]
    
    # List of each event within the game in order of how they appear in the map array
    event_type = ['Get book on fuel tanks and engines','Patch fuel leak','Select coordinates','Engage and head to you destination']

    """
    There are three different classes, each with a different way to play.
    The scout will be able to avoid enemies much easier but have very little health and defense comparitively.
    The soldier class offers a character capable of withstanding long fights but their damage is more reliant on dice rolls.
    The guardian class is a happy medium with moderate health and more consistent damage.
    """
    SoldierStats = {'Hlth': 60.0, 'Dmg': 18.0, 'Def': 8.0, 'Spd': 2.0, 'Skill': 2.0, 't': 0.0, 'Max Hlth': 60.0}
    ScoutStats = {'Hlth': 25.0, 'Dmg': 8.0, 'Def': 4.0, 'Spd': 10.0, 'Skill': 10.0, 't': 0.0, 'Max Hlth': 20.0}
    GuardianStats = {'Hlth': 40.0, 'Dmg': 10.0, 'Def': 8.0, 'Spd': 5.0, 'Skill': 6.0, 't': 0.0, 'Max Hlth': 40.0}
    
    # Coordinates for the previously listed events in order as shown above
    events1[0][5] = True
    events1[1][4] = True
    events1[4][2] = True
    events1[4][4] = True
    
    # The following block is for the in game text that appears under the room name in the game window
    text[0][0] = 'You are awakened by a blaring alarm. \nLEAK DETECTED IN ENGINE ROOM PLEASE REPAIR AT ONCE.'
    text[0][1] = 'You enter the Rec Room to investigate. \nPeople had clearly been here recently as there \nseems to be a game of pool in play with drinks on the surrounding tables.'
    text[0][2] = 'You check the other crew quarters on this side of the ship, \nbut it seems that no one is here.'
    text[0][3] = 'The alarm continues in the background, \nbut you cannot hear or see anyone else.'
    text[0][4] = 'You notice signs on the wall directing you down \nthe next hallway to the engine room.'
    text[0][5] = 'You enter the library to check for signs of the crew, \n but like everywhere else there is no one here.'
    text[1][0] = 'You check the classroom and notice the projecter is still on. \nIt seems that anyone who had been here left in a rush or was abrubtly taken.'
    text[1][1] = 'You hear noises coming from within the cafeteria, \nhowever the signs continue to point further down the hall to the engine room.'
    text[1][2] = 'As you approach the engine room you begin to ponder \nhow you managed to survive.'
    text[1][3] = 'You enter engineering where your attention is filled with warnings screens. \nWARNING FAILING SYSTEMS IN CRYOGENICS. \nFAILURE TO RETURN SOON WILL LEAD TO LOSS OF LIFE.'
    text[1][4] = 'You locate the source of the leak and prepare to fix it.'
    text[1][5] = 'In the holding cells you see the first human since waking up. \nToo bad he is already dead.'
    text[2][0] = 'In cryogenics you notice that one of the pods life support has already failed. \nIt seems the situation here is deteriorating,\ntaking too long could have serious side effects.'
    text[2][1] = 'You are hit with a bit of familiarity when you enter the hallway, \nremembering that odd mix of smells from Agriculture and Med Bay.'
    text[2][2] = 'The smell of the greenery takes your mind back home.'
    text[2][3] = 'You take a second to enter the Med Bay which \ngives you an opportunity to heal any wounds.'
    text[2][4] = 'The cafeteria is eerily silent compared to its usual candor.'
    text[2][5] = 'The familiar smell of the kitchen overtakes you, \nbringing you back to simpler times.'
    text[3][0] = 'Wondering why you decided to come in here, \nyou spot a bit of your favorite snack out of the corner of your eye.'
    text[3][1] = 'It must have gotten violent here as the walls are covered in blood.'
    text[3][2] = 'You are overcome with grief, \nrealizing that you are you only person left alive onboard.'
    text[3][3] = 'The hallways start to become monotonous but it seems you are nearing the end.'
    text[3][4] = 'You go into the combat room and immediately notice \nthat something has bitten off the training dummies head, \n while you are here you decide to grab a new weapon.'
    text[3][5] = 'The blood stained walls continue down the corridor.'
    text[4][0] = 'The Lounge was always one your favorite place to blow off steam, \nunfortunately you dont have any time right now.'
    text[4][1] = 'When you enter security you notice a stream from the bridge. \nOn it you can see what looks like an incredibly powerful foe.'
    text[4][2] = 'You reach navigation with a slight sense of relief, \nrealizing that you have almost completed your goal.'
    text[4][3] = 'You step into the Captains Quarters just to have a look, \nand you are amazed at how luxurious it is.'
    text[4][4] = 'You have finally reached the bridge and can get out of here.'

    # Loop to randomly generate what rooms have enemys, loot, both, or none and what the difficulty multiplier for these rooms are
    for x in range(rows):
        for y in range(cols):
            en = random.randint(0,2)
            if en == 1:
                enemy[x][y] = True
                loot[x][y] = True
            item = random.randint(0,5)
            if item == 1:
                loot[x][y] = True
            diff[x][y] = float(random.randint(1,3))

    # This set of assignments is to force certain rooms to either have an enemy or not
    # For example enemy[4][4] is set to True so the Bridge always has an enemy to act as a final boss
    enemy[0][0] = False
    loot[0][0] = False
    leak = False
    enemy[4][4] = True
    loot[4][4] = True
    diff[4][4] = 5.0        # Difficulty of the bride is set to 5 to differentiate it from the rest of the rooms (diff is normally from 1 to 3)
    enemy[0][3] = False
    loot[0][3] = False
    enemy[1][3] = True
    loot[1][3] = True
    enemy[2][4] = True
    loot[2][4] = True
    enemy[1][4] = False
    loot[1][4] = False
    enemy[1][5] = False
    loot[1][5] = False
    enemy[2][0] = False
    loot[2][0] = False

    evt = 0     # variable to cycle through events
    # This loop assigns a loot type for any room with loot in the game and
    # puts each event in the proper room
    for x in range(rows):
        for y in range(cols):        
            if loot[x][y]:
                z = random.randint(0,3)
                loot_type[x][y] = item_types[z]
            if events1[x][y]:
                event_list[x][y] = event_type[evt]
                evt += 1

    # This loop runs through each room in the map array and passes it into the Room class so this info is accessible later
    for x in range(rows):
        for y in range(cols):
            M[x][y] = Room(enemy[x][y],loot[x][y],diff[x][y],loot_type[x][y],exits2D[x][y],events1[x][y],event_list[x][y],text[x][y],avoid[x][y])
    
    # Set up layout for the main game window, inital screen is included to select class
    # The max number of buttons is included as they are just made invisible and visible as necessary
    layout = [[sg.Text('Please Select a Class.', size=(100,0),key = '0')],
              [sg.Text('', size = (100,0), key = 'q', visible = False)],
              [sg.Col([[sg.Button('1')]]),sg.Text('Soldier', size = (100,0), key = 'a')],
              [sg.Col([[sg.Button('2')]]),sg.Text('Scout', size = (100,0), key = 'b')],
              [sg.Col([[sg.Button('3')]]),sg.Text('Guardian (Recommended)', size = (100,0), key = 'c')],
              [sg.Col([[sg.Button('4',visible = False)]]),sg.Text('', size = (100,0), key = 'd')],
              [sg.Col([[sg.Button('5',visible = False)]]),sg.Text('', size = (500,0), key = 'e')],
              [sg.Exit()]]

    # The following variables are being initialized here to be used throughout the game loop
    t_leak = 0.0
    n_heals = 3
    txtkey = ['a','b','c','d','e']      # keys for each button text
    btnkey = ['1','2','3','4','5']      # keys for each button
    x, y = (0,0)
    currroom = 'Crew Quarters 1'
    z = 0
    events = [False,None]
    weapon = True
    second = False
    book = False
    done = False
    loc = False
    leave = False
    nav = True
    dest = 'None'
    engage = True
    running = True

    window = sg.Window('Game Window',layout,size=(500,350))     # Create window with desired layout

    # This is the game loop where you pick your paths and calls the turn function as necessary
    while running:
        # The next two if statements prevent event buttons from being persistent after being pressed
        if not nav:
            window['5'].update(visible = False)
            nav = True
        if not engage:
            window['2'].update(visible = False)
            engage = True
        
        # Main check of what button was pressed as long as the button wasn't for an event
        if not leave:
            event, values = window.read()
        
        # Sets the event check bool to False to prevent inability to progress
        if leave:
            leave = False
        
        # Check whether window was closed
        if event in (sg.WIN_CLOSED,'Exit'):
            break

        # Removes event buttons
        if events[0] and done:
            for i in range(5):
                if i < len(exits):
                    window[btnkey[i]].update(visible = True)
                    window[txtkey[i]].update(visible = True)
                    window[txtkey[i]].update('Go to ' + exits[i][2])
                else:
                    window[btnkey[i]].update(visible = False)
                    window[txtkey[i]].update(visible = False)
                second = True

        # Set initial player stats based on class selection, this is only run once
        if z == 0:
            if event == '1':
                PlayerStats = SoldierStats
            elif event == '2':
                PlayerStats = ScoutStats
            else:
                PlayerStats = GuardianStats
            z += 1
            PlayerStats, exits, events, window, text = turn(M[x][y],PlayerStats,window)
            window['q'].update(visible = True)

        # Standard turn loop, only used if the event in the room is not progressed
        # Calls turn() to progress based on input    
        if z > 1 and not events[0]:
            x = exits[int(event)-1][0]
            y = exits[int(event)-1][1]
            currroom = exits[int(event)-1][2]
            PlayerStats, exits, events, window, text = turn(M[x][y],PlayerStats,window)
            # Check if player died in combat and present death window
            if PlayerStats['Hlth'] <= 0:
                window.close()
                layout = [[sg.Text('In space no one can hear you scream.\n \nYOU DIED\n \n', size = (150,4), justification = 'center')], 
                          [sg.Button('Play Again'), sg.Button('Exit')]]
                window2 = sg.Window('Game Over',layout, size = (250,125))
                event, values = window2.read()
                if event in (sg.WIN_CLOSED,'Exit'):
                    window2.close()
                    break
                else:
                    window2.close()
                    runner()        # call runner() if play again is selected

        window['0'].update(currroom)

        # Turn loop for after an event
        if events[0] and second:
            if leak or loc or book:
                M[x][y].set_event()
                second = False
                done = False
                PlayerStats, exits, events, window, text = turn(M[x][y],PlayerStats,window)
                # Check if player died
                if PlayerStats['Hlth'] <= 0:
                    window.close()
                    layout = [[sg.Text('In space no one can hear you scream.\n \nYOU DIED\n \n', size = (150,4), justification = 'center')], 
                            [sg.Button('Play Again'), sg.Button('Exit')]]
                    window2 = sg.Window('Game Over',layout, size = (250,125))
                    event, values = window2.read()
                    if event in (sg.WIN_CLOSED,'Exit'):
                        window2.close()
                        break
                    else:
                        window2.close()
                        runner()
        # Loop to change what buttons are visible based on the number of exits in the room
        for i in range(5):
            if i < len(exits):
                window[btnkey[i]].update(visible = True)
                window[txtkey[i]].update(visible = True)
                window[txtkey[i]].update('Go to ' + exits[i][2])
            else:
                window[btnkey[i]].update(visible = False)
                window[txtkey[i]].update(visible = False)
            if book and leak:       # Check to let player know the book event helped cut down on time
                window['b'].update(visible = True)
                window['b'].update('Thanks to the book from the library you were able to patch the leak quicker than ususal')
                book = False

        # Heals player if they go to Med Bay, but only if they havent already been 3 times
        if n_heals != 0 and x == 2 and y == 3:
            PlayerStats['Hlth'] = PlayerStats['Max Hlth']
            n_heals -= 1
        # Increases damage from weapon in combat room
        if weapon and x == 3 and y == 4:
            PlayerStats['Dmg'] += random.randint(2,5)
            weapon = False
        
        window['q'].update(text)    # Updates room text

        # Check if current room has an event
        if events[0]:
            # Booleans included in each event are here to prevent indexing errors, remove events once completed, and adjust the display
            if x == 0 and y == 5:       # Library event
                window['2'].update(visible = True)
                window['b'].update(visible = True)
                window['b'].update(events[1])
                event, values = window.read()
                if event == (sg.WIN_CLOSED,'Exit'):
                    break
                if event == '2':
                    book = True
                    done = True
                    leave = True
                else:
                    events[0] = False
                    leave = True
            
            if x == 1 and y == 4:       # Engine Room event
                window['2'].update(visible = True)
                window['b'].update(visible = True)
                window['b'].update(events[1])
                event, values = window.read()
                if event == (sg.WIN_CLOSED,'Exit'):
                    break
                if event == '2' and book:
                    leak = True
                    done = True
                    t_leak = PlayerStats['t'] - 2
                    leave = True
                elif event == '2':
                    leak = True
                    done = True
                    t_leak = PlayerStats['t']
                    leave = True
                else:
                    events[0] = False
                    leave = True

            if x == 4 and y == 2:       # Navigation event
                window['5'].update(visible = True)
                window['e'].update(visible = True)
                window['e'].update(events[1])
                event, values = window.read()
                if event == (sg.WIN_CLOSED,'Exit'):
                    break
                if event == '5':
                    if t_leak == 0:
                        window['e'].update('Warning fuel leak not patched, navigation locked')
                        events[0] = False
                        nav = False
                    else:
                        window['a'].update('Earth')
                        window['b'].update('Moon Colony')
                        window['c'].update('Mars Colony')
                        window['4'].update(visible = False)
                        window['d'].update(visible = False)
                        window['5'].update(visible = False)
                        window['e'].update(visible = False)
                        event, values = window.read()
                        # This set of if statements checks whether the fuel leak was patched quickly enough and selects destination
                        # If the leak was not patched quickly enough for user selection it displays a warning
                        # That destination may still be selected but doing so will cause the bad ending
                        # The checks for event == 2 and event == 3 must also check the previous selections if pressed
                        # ie if 2 is selected it may display the error, but it is already past the check for 1 it must check it separately
                        if event == '1':
                            if t_leak <= 5.0:
                                dest = 'Earth'
                                done = True
                                loc = True
                                fuel = True
                                leave = True
                            else:
                                window['a'].update('Warning fuel not sufficient for destination, please confirm or select another location')
                                event, values = window.read()
                                if event == (sg.WIN_CLOSED,'Exit'):
                                    break
                                if event == '1':
                                    dest = 'Earth'
                                    done = True
                                    loc = True
                                    fuel = False
                                    leave = True
                        if event == '2':
                            if t_leak < 7.5:
                                dest = 'Moon Colony'
                                done = True
                                loc = True
                                fuel = True
                                leave = True
                            else:
                                window['b'].update('Warning fuel not sufficient for destination, please confirm or select another location')
                                event, values = window.read()
                                if event == (sg.WIN_CLOSED,'Exit'):
                                    break
                                if event == '2':
                                    dest = 'Moon Colony'
                                    done = True
                                    loc = True
                                    fuel = False
                                    leave = True
                                if event == '1':
                                    window['a'].update('Warning fuel not sufficient for destination, please confirm or select another location')
                                    event, values = window.read()
                                    if event == (sg.WIN_CLOSED,'Exit'):
                                        break
                                    if event == '1':
                                        dest = 'Earth'
                                        done = True
                                        loc = True
                                        fuel = False
                                        leave = True
                        if event == '3':
                            if t_leak < 12.5:
                                dest = 'Mars Colony'
                                done = True
                                loc = True
                                fuel = True
                                leave = True
                            else:
                                window['c'].update('Warning fuel not sufficient for destination, please confirm or select another location')
                                event, values = window.read()
                                if event == (sg.WIN_CLOSED,'Exit'):
                                    break
                                if event == '3':
                                    dest = 'Mars Colony'
                                    done = True
                                    loc = True
                                    fuel = False
                                    leave = True
                                if event == '2':
                                    window['b'].update('Warning fuel not sufficient for destination, please confirm or select another location')
                                    event, values = window.read()
                                    if event == (sg.WIN_CLOSED,'Exit'):
                                        break
                                    if event == '2':
                                        dest = 'Moon Colony'
                                        done = True
                                        loc = True
                                        fuel = False
                                        leave = True
                                if event == '1':
                                    window['a'].update('Warning fuel not sufficient for destination, please confirm or select another location')
                                    event, values = window.read()
                                    if event == (sg.WIN_CLOSED,'Exit'):
                                        break
                                    if event == '1':
                                        dest = 'Earth'
                                        done = True
                                        loc = True
                                        fuel = False
                                        leave = True
                else:
                    events[0] = False
                    leave = True

            if x == 4 and y == 4:           # Bridge event
                window['2'].update(visible = True)
                window['b'].update(visible = True)
                window['b'].update(events[1])
                event, values = window.read()
                if event == (sg.WIN_CLOSED,'Exit'):
                    break
                if event == '2':
                    if dest == 'None':
                        window['b'].update('No destination selected.')
                        events[0] = False
                        engage = False
                    # These are all the possible endings taking into account destination, the amount of time before repairing the fuel leak, and the total time
                    # it took to determine outcome of cryogenic pods giving 7 total endings
                    else:
                        window.close()
                        if dest == 'Earth' and fuel and PlayerStats['t'] <= 23.0:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Within a few short hours you are safely landed back home.\n'
                                      + 'Thanks to your time managment there were no further casualties in cryogenics!\nTake it Sleazy!', size = (200,4), justification = 'center')], 
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        elif dest == 'Earth' and fuel:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Within a few short hours you are safely landed back home.\n'
                                      + 'However, due to your lack of urgency over half of the pods life support systems failed.', size = (200,3), justification = 'center')], 
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        elif dest == 'Moon Colony' and fuel and PlayerStats['t'] <= 23.0:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Within a few short hours you are landed on the moon being greeted by disgruntled colonists. \n'
                                      + 'While not ideal, landing on the moon gives you a small piece of respite and safety \n while you wait a short while for a ship to take you home.\n'
                                      + 'Thanks to your urgency everyone in the pods made it. \nHowever due to limitations only around half the pods were properly thawed.', size = (200,5), justification = 'center')], 
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        elif dest == 'Moon Colony' and fuel:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Within a few short hours you are landed on the moon being greeted by disgruntled colonists. \n'
                                      + 'While not ideal, landing on the moon gives you a small piece of respite and safety \n while you wait a short while for a ship to take you home.\n'
                                      + 'Unfortunately, due to tech limitations at the colony no one in the pods survived', size = (200,4), justification = 'center')], 
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        elif dest == 'Mars Colony' and fuel and PlayerStats['t'] <= 26.0:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Within a few short hours you are landed safely on Mars. \n'
                                      + 'Due to the urgency on board you land hours away from the colony. \n While the wait is long, you are eventually rescued, but with no return home in sight \n'
                                      + 'you spend the rest of your days stranded at the colony.\nLuckily the colony has the necessary equipment to thaw the pods,\n leaving minimal casualties', size = (200,6), justification = 'center')], 
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        elif dest == 'Mars Colony' and fuel:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Within a few short hours you are landed safely on Mars. \n'
                                      + 'Due to the urgency on board you land hours away from the colony. \n While the wait is long, you are eventually rescued, but with no return home in sight \n'
                                      + 'you spend the rest of your days stranded at the colony.\nUnfortunately you were not fast enough and around half the pods life support failed,\n'
                                      + 'thankfully the colonists were able to thaw the remaining without issue.', size = (200,6), justification = 'center')], 
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        else:
                            layout = [[sg.Text('The sound of the thrusters fill the air. \n Due to a shortage in fuel because of the leak \n you cant make it back home stranding you in space. \n'
                                      + 'You spend the rest of your days alone, floating through space', size = (200,4), justification = 'center')],
                                      [sg.Button('Play Again'), sg.Button('Exit')]]
                        window = sg.Window('',layout, size = (550,150),no_titlebar = True)
                        event, values = window.read()
                        if event in (sg.WIN_CLOSED,'Exit'):
                            break
                        else:
                            window.close()
                            runner()
                else:
                    events[0] = False
                    leave = True
        z += 1
    window.close()      # close window when you exit the game

"""
This is the turn function which processes movement, combat, and loot.
It takes in the current room in the form of M[x][y], the players current stats, and the window variable so it can be hidden during combat to prevent cluttering
It returns the rooms exits, the players updated stats, the events boolean, the window variable (now unhidden), and the text for the room
"""
def turn(Room,PlayerStats,window): 
    exits = Room.get_exits()
    events = Room.get_events()
    text = Room.get_text()
    t = PlayerStats['t']
    t += 0.5            # Increase time increment by .5 on every call of turn()

    if Room.get_enemy():
        avoid = Room.get_avoid()
        EnemyStats = Room.get_enemy_obj().get_stats()
        # Read in Enemy and Player stats
        HlthE = float(EnemyStats['Hlth'])
        DmgE = float(EnemyStats['Dmg'])
        DefE = float(EnemyStats['Def'])
        SpdE = float(EnemyStats['Spd'])
        Per = float(EnemyStats['Per'])
        HlthP = float(PlayerStats['Hlth'])
        DmgP = float(PlayerStats['Dmg'])
        DefP = float(PlayerStats['Def'])
        SpdP = float(PlayerStats['Spd'])
        Skill = float(PlayerStats['Skill'])
        # Create layout for combat window
        combat_layout = [[sg.Text('You encountered an enemy!')],
                         [sg.Text('Player Health: ' + str(round(HlthP,3)), size = (100,1), key = 'P')],
                         [sg.Text('Enemy Health: ' + str(HlthE), size = (100,1), key = 'E')],
                         [sg.Text('', size = (100,1), key = 'D')],
                         [sg.Button('Ok', visible = True)]]
        combat_window = sg.Window('',combat_layout,size = (300,200),no_titlebar=True)
        window.Hide()          # Hide main game window to declutter
        event, values = combat_window.read()
        # Check whether the enemies perception matches or betters players skill
        # If players skill is higher and they haven't already met the enemy before you skip combat
        # Once a player has avoided an enemy once they can't avoid the same enemy again
        if Per >= Skill or not avoid:
            # Check whose speed is faster to determine who attacks first
            if SpdE >= SpdP:
                while HlthE > 0:
                    # Enemy attacks first
                    if event == 'Ok':
                        t += 0.25
                        HlthP -= DmgE*DmgE/(DefP*2.0)       # Damage calculation for enemy
                        # Update window with damage and updated health
                        combat_window['D'].update('Enemy attacks for ' + str(round(DmgE*DmgE/(2.0*DefP),3)) + ' damage!')
                        combat_window['P'].update('Player Health: ' + str(round(HlthP,3)))
                        PlayerStats['Hlth'] = HlthP
                        # Check if players health reaches 0
                        if HlthP <= 0:
                            PlayerStats['t'] = t
                            combat_window.close()
                            window.UnHide()     
                            return PlayerStats, exits, events, window, text
                        mult = float(random.randint(0,5))       # Generate multiplier for this turn in combat
                    event, values = combat_window.read()
                    if event == 'Ok':
                        if mult != 0:
                            DmgP = DmgP*DmgP*(Skill/mult)            # Calculate Dmg stat for this turn based on the multiplier
                        combat_window['D'].update('You attack for ' + str(round(DmgP/(DefE*4.0),3)) + ' damage!')
                        # Check if the multiplier generates 0 resulting in a missed attack
                        if mult == 0:
                            DmgP = 0      
                            combat_window['D'].update('Your attack missed!') 
                        HlthE -= DmgP/(DefE*4.0)           # Damage calculation for player
                        DmgP = float(PlayerStats['Dmg'])
                        combat_window['E'].update('Enemy Health: ' + str(round(HlthE,3)))
                    event, values = combat_window.read()
            else:
                while HlthE > 0:
                    # Same process as before but now player attack then enemy attack
                    if event == 'Ok':
                        t += .25
                        mult = float(random.randint(0,5))
                        if mult != 0:
                            DmgP = DmgP*DmgP*(Skill/mult)
                        combat_window['D'].update('You attack for ' + str(round(DmgP/(DefE*4.0),3)) + ' damage!')
                        if mult == 0:
                            DmgP = 0
                            combat_window['D'].update('Your attack missed!')
                        HlthE -= DmgP/(DefE*4.0)
                        DmgP = float(PlayerStats['Dmg'])
                        combat_window['E'].update('Enemy Health: ' + str(round(HlthE,3)))
                    event, values = combat_window.read()
                    if event == 'Ok' and HlthE > 0:
                        HlthP -= DmgE*DmgE/(2.0*DefP)
                        combat_window['D'].update('Enemy attacks for ' + str(round(DmgE*DmgE/(2.0*DefP),3)) + ' damage!')
                        combat_window['P'].update('Player Health: ' + str(round(HlthP,3)))
                        PlayerStats['Hlth'] = HlthP
                        if HlthP <= 0:
                            PlayerStats['t'] = t
                            combat_window.close()
                            window.UnHide()
                            return PlayerStats, exits, events, window, text  
                        event, values = combat_window.read() 
            PlayerStats['t'] = t
            PlayerStats, amount = Room.loot(PlayerStats)        # Loot the room
            Room.set_enemy()        # Remove enemy from room
            combat_window['D'].update('You defeated the enemy! Press Ok to continue')
            combat_window['Ok'].update(visible = True)
            if event == 'Ok':
                if Room.get_loot():
                    loot_type = Room.get_loot_type()
                    Room.set_loot()     # Remove loot from room
                    combat_window['D'].update('You found some loot to raise your ' + loot_type + ' by ' + str(amount))
                    event, values = combat_window.read()
                    if event == 'Ok':
                        combat_window.close()
                        window.UnHide()
                        return PlayerStats, exits, events, window, text
                else:
                    Room.set_loot()
                    combat_window.close()
                    window.UnHide()
                    return PlayerStats, exits, events, window, text
        else:
            # For when you avoid enemy
            if event == 'Ok':
                combat_window.close()
            PlayerStats, amount = Room.loot(PlayerStats)
            loot_type = Room.get_loot_type()
            loot = Room.get_loot()
            Room.set_avoid()        # Make it so enemy is not avoidable
            if loot:
                # Display if there is loot in room
                combat_layout2 = [[sg.Text('You avoided combat and found some loot!', size = (200,1))],
                                  [sg.Text('Your ' + loot_type + ' increased by ' + str(amount))],
                                  [sg.Button('Ok')]]
            else:
                # Display if no loot in room
                combat_layout2 = [[sg.Text('You avoided combat!', size = (200,1))],
                                  [sg.Button('Ok')]]
            Room.set_loot()
            PlayerStats['t'] = t
            combat_window2 = sg.Window('',combat_layout2,size = (300,100),no_titlebar=True)
            event, values = combat_window2.read()
            if event == 'Ok':
                combat_window2.close()
                window.UnHide()
                return PlayerStats, exits, events, window, text
    if Room.get_loot():
        # For if there is only loot and no enemy in the room
        window.Hide()
        PlayerStats['t'] = t
        PlayerStats, amount = Room.loot(PlayerStats)
        Room.set_loot()
        loot_type = Room.get_loot_type()
        loot_layout = [[sg.Text('You found some loot!')],
                       [sg.Text('Your ' + loot_type + ' increased by ' + str(amount))],
                       [sg.Button('Ok')]]
        loot_window = sg.Window('',loot_layout,size = (300,100),no_titlebar=True)
        event, values = loot_window.read()
        if event == 'Ok':
            loot_window.close()
            window.UnHide()
            return PlayerStats, exits, events, window, text
    PlayerStats['t'] = t
    return PlayerStats, exits, events, window, text

#Enemy class to generate the stats for each enemy in the game
class Enemy:
    def __init__(self,diff):
        self.diff = diff
        self.EnemyStats = self.newenemy()

    # Set enemy stats through random number generation
    def newenemy(self): 
        self.EnemyStats = {}     
        self.EnemyStats['Hlth'] = float(random.randint(15,25)*self.diff)
        self.EnemyStats['Dmg'] = float(random.randint(2,6)*self.diff)
        self.EnemyStats['Def'] = float(random.randint(2,4)*self.diff)

        if self.EnemyStats['Def'] <= 4.0:
            self.EnemyStats['Def'] = 2.0 + self.EnemyStats['Def']

        self.EnemyStats['Spd'] = float(random.randint(1,5)*self.diff)
        self.EnemyStats['Per'] = float(random.randint(2,5)*self.diff)

        if self.diff == 5.0:        # For the final boss only
            self.EnemyStats['Per'] = 1000.0     # Set perception so high so you can't avoid the final boss

        return self.EnemyStats

    def get_stats(self):        
        return self.EnemyStats

# Room class to create the map and all the loot and enemies in it
class Room:
    def __init__(self,enemy,Loot,diff,loot_type,exits,event,event_list,text,avoid):
        if enemy:
            self.enemy = enemy
            self.foe = Enemy(diff)      # Create enemy obj in the room
        else:
            self.enemy = enemy
        self.avoid = avoid
        self.text = text
        self.Loot = Loot
        self.diff = diff
        self.exits = exits
        self.loot_type = loot_type
        self.event = event
        self.event_list = event_list

    # Function to adjust player stats with the loot in the room
    def loot(self,PlayerStats):
        amount = 0
        if self.Loot:
            i = self.loot_type
            amountH = float(random.randint(3,6)*self.diff)
            amount = float(random.randint(1,2)*self.diff)
            # Seperate check for health items because it is a different amount and there is a limit to how high the health can go
            # to prevent the possibility of health ballooning to a ridiculous number
            if i == 'Hlth':
                difference = PlayerStats['Max Hlth'] - PlayerStats[i]
                amount = amountH
                if difference >= amount:
                    PlayerStats[i] += amount
                else:
                    PlayerStats[i] = PlayerStats['Max Hlth']
                    amount = difference
            else:
                PlayerStats[i] = PlayerStats[i] + amount
        return (PlayerStats,amount)

    def get_enemy(self):    # Get enemy boolean
        return self.enemy
    def get_enemy_obj(self):    # Get the enemy itself
        return self.foe
    def get_loot(self):     # Get loot boolean
        return self.Loot
    def get_loot_type(self):
        return self.loot_type
    def get_events(self):       # Get event boolean and which event it is and return as list
        return [self.event,self.event_list]
    def get_exits(self):        # Returns list of exits
        return self.exits
    def get_text(self):         # Returns the rooms text
        return self.text
    def get_avoid(self):
        return self.avoid
    def set_enemy(self):
        self.enemy = False
    def set_loot(self):
        self.Loot = False
    def set_event(self):
        self.event = False
    def set_avoid(self):
        self.avoid = False

if __name__ == '__main__':
    runner()