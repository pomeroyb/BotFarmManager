import sys
import os
import json


class BotFarmManager(object):
    """ Overarching class for interacting with the API
    
    """
    
    def __init__(self):
        self.config = Config()
        self.config.load()
        self.reader = BarcodeReader()
        
    
    def UpdateBot(self, serial, input):
        """ Updates a bot if it exists
        
            Returns: True if the bot was updated, false if not
        """
    
        # find out what kind of update we were sent
        # Input should always have a 3 string identifier.
        checkStr = input[0:3]
        cleanInput = input[3:]
        print cleanInput
        
        if checkStr == 'cmd':
            # Command updates don't necessarily need an existing bot
            # so we don't check that a serial exists
            if cleanInput == 'addbot':
                ret = self.AddBot(serial)
                print "Added machine " + serial + " to farm"
                return ret
            elif cleanInput == 'removebot':
                ret = self.RemoveBot(serial)
                print "Removed machine " + serial + " from farm"
                return ret
       
        elif serial in self.config.data['farm']:
            if checkStr == 'prb':
                #This is a problem update
                if cleanInput in self.config.data['farm'][serial]['problems']:
                    # Problem updates always set problems to True.
                    self.config.data['farm'][serial]['problems'][cleanInput] = True
                    print "Machine " + serial + " now has " + cleanInput
                    self.UpdateBotStatus(serial)
                    return True
            elif checkStr == 'evt':
                # This is an event update
                if cleanInput in self.config.data['farm'][serial]['events']:
                    # Event updates always add one to the event
                    self.config.data['farm'][serial]['events'][cleanInput] = self.config.data['farm'][serial]['events'][cleanInput] + 1
                    print "Machine " + serial + " has had " + str(self.config.data['farm'][serial]['events'][cleanInput]) + ' ' + cleanInput + " events!"
                    self.UpdateBotStatus(serial)
                    return True
            elif checkStr == 'nme':
                # This is a bot name update. We don't do any input checking yolo
                self.config.data['farm'][serial]['name'] = cleanInput
                print "Machine " + serial + " is now named " + cleanInput
                self.UpdateBotStatus(serial)
                return True
            elif checkStr == 'typ':
                # This is a bot type update. We don't do any input checking here either yolox2
                self.config.data['farm'][serial]['type'] = cleanInput
                print "Machine " + serial + " is now a " + cleanInput
                self.UpdateBotStatus(serial)
                return True
            elif checkStr == 'clr':
                # This is a clear update. We're either clearing status or events
                if cleanInput == 'botproblems':
                    # Set all bot problems to false
                    for key in self.config.data['farm'][serial]['problems']:
                        self.config.data['farm'][serial]['problems'][key] = False
                    ## We know that a bot with no problems is online
                    self.config.data['farm'][serial]['status'] = 'online'
                    print "Machine " + serial + " doesn't have any problems!"
                    return True
                if cleanInput == 'botevents':
                    # Set all bot events to 0
                    for key in self.config.data['farm'][serial]['events']:
                        self.config.data['farm'][serial]['events'][key] = 0
                    print "Machine " + serial + " doesn't have any events!"
                    return True
        else:
            print input + " was not recognized!"
            return False
    
    def UpdateBotStatus(self, serial):
        """ Updates the bot status to either Online, Offline, or Faulty
        
        """
        
        print 'Updating Bot Status'
        print 'Current status: ' + self.config.data['farm'][serial]['status']

        if self.config.data['farm'][serial]['problems']['extruderFanFailure']:
            self.config.data['farm'][serial]['status'] = 'offline'
            print 'Extruder Fan Failure! Setting bot to "offline"'
        if self.config.data['farm'][serial]['problems']['xStepperFailure']:
            self.config.data['farm'][serial]['status'] = 'offline'  
            print 'X Stepper Failure! Setting bot to "offline"'                
        if self.config.data['farm'][serial]['problems']['hotEndFailure']:
            print 'Hot End Failure! Setting bot to "offline"'
            self.config.data['farm'][serial]['status'] = 'offline'
        if self.config.data['farm'][serial]['status'] is not 'offline':
            ## First check anything that can make a bot Faulty
            ## We also check that the bot is already online, since it doesn't make
            ## sense to override an offline bot as faulty.
            if self.config.data['farm'][serial]['problems']['tornInsulation']:
                self.config.data['farm'][serial]['status'] = 'faulty'
                print 'Torn Insulation! Setting bot to "faulty"'
            if self.config.data['farm'][serial]['problems']['wornYCarriage']:
                self.config.data['farm'][serial]['status'] = 'faulty'
                print 'Worn Y Carriage Failure! Setting bot to "faulty"'
            if self.config.data['farm'][serial]['problems']['xEndstopFailure']:
                self.config.data['farm'][serial]['status'] = 'faulty'
                print 'X Endstop Failure! Setting bot to "faulty"'
        print 'New status: ' + self.config.data['farm'][serial]['status']
        
    def RemoveBot(self, serial):
        """Removes a serial from the config data if it exists.
        
            Returns: true if the bot was removed, false if not
        """
        
        #check to make sure the first three chars of the serial code is 'bot'
        checkStr = serial[0:3]
        if checkStr == 'bot':
            print 'valid serial'
            if serial in self.config.data['farm']:
                del self.config.data['farm'][serial]
                return True
            else:
                return False
        else:
            return False
        
    def AddBot(self, serial):
        """ Adds a serial to the config data. If the serial already exists,
            nothing happens
        
            Returns: true if the bot was added, false if not.
        """
        
        #The infoDict contains the overall status of a bot
        infoDict = {"status" : "online",
                    "type" : "Replicator 2",
                    "name" : "Default",
                    "problems" : {                
                        "tornInsulation" : False,
                        "xEndstopFailure" : False,
                        "xStepperFailure" : False,
                        "extruderFanFailure" : False,
                        "hotEndFailure" : False,
                        "wornYCarriage" : False
                        },
                    "events" : {
                        "underExtrusion" : 0,
                        "layerShift" : 0,
                        "highResUnderExtrusion" : 0,
                        "ovalHoles": 0}
                    }
        
        #check to make sure the first three chars of the serial code is 'bot'
        checkStr = serial[0:3]
        if checkStr == 'bot':
            print 'valid serial'
            if serial not in self.config.data['farm']:
                self.config.data['farm'][serial] = infoDict
                return True
            else:
                #Serial already exists!
                print serial + ' is already present!'
                return False
        else:
            #Not a valid serial. You scanned the wrong thing!
            print serial + ' is not a valid machine serial!'
            return False
        
    

class Config(object):
    """ This class loads and saves json configs that represent
        the printer farm status
    
    """
    
    def __init__(self):
        self.fname = 'config.json'
        self.dataName = 'data.js'
        self.emptyConfig = {'farm': {}}
        self.data = None
        
    def load(self):
        """ Loads a json config representing the status of our
            3D printer farm
            
        """
        if os.path.isfile(self.fname):
            # File exists, load it
            print 'found config'
            with open(self.fname) as json_data_file:
                try:
                    self.data = json.load(json_data_file)
                    print 'Loaded config'
                except ValueError, e:
                    print 'Not a valid JSON config file!'
        else:
            print 'No config.json found. Creating empty config'
            with open(self.fname, 'w') as outfile:
                try:
                    json.dump(self.emptyConfig, outfile)
                    self.data = self.emptyConfig
                    print 'Created config'
                except ValueError, e:
                    print 'Could not create config'
    
    def save(self):
        """Saves a BotFarmManager Config.  If no config.json exists, it will create one.
        This method completely overwrites the old config.json, so make sure to run config.load()
        before this if you want your old data saved. Also saves a data.js file, which is what will
        be sent the server
        
        """
        with open(self.fname, 'w') as outfile:
            try:
                json.dump(self.data, outfile)
                print 'Saved config'
            except ValueError, e:
                print 'Could not save config'
        with open(self.dataName, 'w') as outFileData:
            try:
                outFileData.write('var data = ')
                json.dump(self.data, outFileData)
                ## outFileData.write('}')
            except ValueError, e:
                print 'could not save data.js'
        

class BarcodeReader(object):
    """This class grabs data from the HIDRAW0 and converts
        it to easy to use text.    
    
    """
    
    def __init__(self):
        # We assume the keyboard is HIDRAW0... this may not be the
        # case for all hardware.
        self.fname = '/dev/hidraw0'
        self.shift = False
        self.fp = open(self.fname, 'rb')
        self.done = False
        self.output = ""
        
        self.hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g',
        11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
        17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's',
        23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
        29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5',
        35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
        45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' ,
        52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }
        
        self.hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G',
         11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N',
         18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U',
         25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@',
         32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(',
         39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|',
         51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }

    def clear(self):
        self.output = ""
        self.done = False
    
    def getInput(self):
       ## Get the character from the HID
       buffer = self.fp.read(8)
       for c in buffer:
          if ord(c) > 0:

             ##  40 is carriage return which signifies
             ##  we are done looking for characters
             if int(ord(c)) == 40:
                self.done = True
                break;

             ##  If we are shifted then we have to 
             ##  use the hid2 characters.
             if self.shift: 

                ## If it is a '2' then it is the shift key
                if int(ord(c)) == 2 :
                   self.shift = True

                ## if not a 2 then lookup the mapping
                else:
                   self.output += self.hid2[ int(ord(c)) ]
                   self.shift = False

             ##  If we are not shifted then use
             ##  the hid characters

             else:

                ## If it is a '2' then it is the shift key
                if int(ord(c)) == 2 :
                   self.shift = True

                ## if not a 2 then lookup the mapping
                else:
                   self.output += self.hid[ int(ord(c)) ]    
     
