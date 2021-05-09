#To Accomplish: Communication between two pis --> send frequency from one pi to another
''' PSEUDOCODE FOR SIMPLE FREQ SHARING
USE THE PROGRAM FOR BINKING-LED and just share it with the other pi
'''
import py2p, time
print("\nProgram starts here")
sock = py2p.MeshSocket('0.0.0.0', 4444)
sock.connect('10.0.0.201', 4567)
time.sleep(1)
assert sock.routing_table

print("Program ends here\n")



''' PSEUDOCODE FOR COMPLEX SHARING
have a variable say 'version =1' in the program 

WHILE LOOP
    blinking LED
    ------
    identify pi around?
        if found then go to FOUND_METHOD
        not found -- keep going


FOUND_METHOD [we are here because we found a pi]
    check the "version" variable and compare the versions
    if the pi we are using version is less than that of other then
        PERFORM_UPDATE(piOther, thisPi)
    else
        PERFORM_UPDATE(thisPi, piOther)
    return

PERFORM_UPDATE(needs_update_Pi, have_update_Pi)
    synch the files --> maybe by ????

    return

'''





