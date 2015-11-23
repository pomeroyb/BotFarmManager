import botFarmManagerAPI
import botoConfig
import boto
from simples3.bucket import S3Bucket

# ---------------------------------
#           S3 INTEGRATION
# ---------------------------------
# Creating a simple connection
#boto.set_stream_logger('boto')
#s3 = boto.connect_s3(botoConfig.aws_access_key_id, botoConfig.aws_secret_access_key)
#s3 = boto.s3.connect_to_region('us-west-2', aws_access_key_id=botoConfig.aws_access_key_id, aws_secret_access_key=botoConfig.aws_secret_access_key)
#bucket = s3.get_bucket('www.i3dbotfarm.xyz')

s = S3Bucket(name='www.i3dbotfarm.xyz', access_key=botoConfig.aws_access_key_id, secret_key=botoConfig.aws_secret_access_key, base_url='https://s3-us-west-2.amazonaws.com/www.i3dbotfarm.xyz')

print s
# ---------------------------------
# ---------------------------------

# Create a Bot Farm Manager object
manager = botFarmManagerAPI.BotFarmManager()
# This manager holds the config file IO and barcode reader
# Our config was automatically loaded.

# Some things (like updating bots) require us to remember
# what we previously scanned. 
output = None
oldOutput = None

# Some vars to decide when to end our program
ended = False
count = 0

while not ended:
    # Update the reader's input
    # This is the first thing we should always do
    manager.reader.getInput()
    
    # Check if the reader has a full barcode
    if manager.reader.done:
        # Display the reader's output
        print manager.reader.output
        output = manager.reader.output
        code = output[0:3]
        print code
        if code == 'bot':
            # Just remember the serial
            oldOutput = output
        elif code == 'prb' or code == 'evt' or code == 'nme'or code == 'typ' or code == 'clr' or code == 'cmd':
            if oldOutput is not None:
                # If our output is one of these commmands, update the bot
                manager.UpdateBot(oldOutput, output)
                
                #Save our new data
                manager.config.save()
                # Uploading our new data.js to AWS
                #key = boto.s3.key.Key(bucket, 'data.js')
                #with open('data.js') as f:
                #    key.send_file(f)
                s.put('data.js', 'data.js')
                print "Uploaded data.js to S3"
                oldOutput = None

        # Make sure you clear the reader immediately after grabbing data from it.
        manager.reader.clear()
        count += 1
        



    


