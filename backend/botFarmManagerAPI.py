import sys
import json


class BotFarmManager(object):
    """ Overarching class for interacting with the API
    
    """
    
    def __init__(self):
        self.config = Config()
        self.reader = BarcodeReader()
        
    

class Config(object):
    """ This class loads and saves json configs that represent
        the printer farm status
    
    """
    
    def __init__(self):
        self.fname = 'config.json'
        self.emptyConfig = {'farm': {}}
        self.data = None
        
    def load(self):
        """ Loads a json config representing the status of our
            3D printer farm
            
        """
        if os.path.isFile(self.fname):
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
        before this if you want your old data saved.
        
        """
        with open(self.fname, 'w') as outfile:
            try:
                json.dump(self.data, outfile)
                print 'Saved config'
            except ValueError, e:
                print 'Could not save config'
        

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
     
