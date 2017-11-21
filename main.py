import pygame
import sys
import os
import socket
import time


BUFFER_SIZE = 20

#--------------------------CAN IDS-----------------------
#NODE
CAN_NODE_3_ID = 0x300

#
CAN_GRP_PS3_ID = 0x30

# PS3
CAN_JOYSTICK_ID=0x10
CAN_DPAD_ID=0x20
CAN_BUTTONS_ID=0x30


CAN3_PS3_JOYSTICK_ID = (CAN_NODE_3_ID | CAN_GRP_PS3_ID | CAN_JOYSTICK_ID )
CAN3_PS3_BUTTONS_ID = (CAN_NODE_3_ID | CAN_GRP_PS3_ID | CAN_BUTTONS_ID )
CAN3_PS3_DPAD_ID = ( CAN_NODE_3_ID | CAN_GRP_PS3_ID | CAN_DPAD_ID )


os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(('can0', ))

#print('Initialised Joystick : %s' % joystick.get_name())



# get count of joysticks=1, axes=27, buttons=19 for DualShock 3

joystick_count = pygame.joystick.get_count()
#print("joystick_count")
#print(joystick_count)
#print("--------------")

numaxes = joystick.get_numaxes()
#print("numaxes")
#print(numaxes)
#print("--------------")

numbuttons = joystick.get_numbuttons()
#print("numbuttons")
#print(numbuttons)
#print("--------------")



loopQuit = False
while loopQuit == False:

    l = 16
    result = [0] * l
    datalen = 4
    for i  in range(0, 4):
       pygame.event.pump()
       axis = int(100*joystick.get_axis(i)+100)
       #print("Axis " + str(i) + " = " + str(axis))

       canbus = (0 & 0x10) >> 4
       canid0 = 0x0f+i
       canid1 = 0x00

       result[0] = int(0x31)
       result[1] = 3
       result[4] = datalen

       result[8+i] = axis
       #print("Result " + str(i) + " = " + str(result[8+i]))

    s.send(bytes(result))
    #print('Sending')
    time.sleep(0.1)
    #print("--------------")




    result = [0] * l

    for i in range(10, 12):
        pygame.event.pump()
        button = joystick.get_button(i)
        #print("Button " + str(i) + " = " + str(button))
        canbus = (0 & 0x10) >> 4
        canbus = (0 & 0x10) >> 4
        canid0 = 0x0f+i
        canid1 = 0x00

        result[0] = int(0x33)
        result[1] = 3
        result[4] = datalen

        result[8+i-10] = button
    s.send(bytes(result))
    #print('Sending')
    time.sleep(0.1)
    #print("--------------")


    result = [0] * l

    for i in range(4, 8):
        pygame.event.pump()
        button = joystick.get_button(i)
        #print("DPAD " + str(i) + " = " + str(button))

        result[0] = int(0x32)
        result[1] = 3
        result[4] = datalen

        result[8+i-4] = button
    s.send(bytes(result))
    #print('Sending')
    time.sleep(0.2)
    #print("--------------")

pygame.quit()

sys.exit()