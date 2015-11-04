import botFarmManagerAPI

# Create a Bot Farm Manager object
manager = botFarmManagerAPI.BotFarmManager()
# This manager holds the config file IO and barcode reader

# Some vars to decide when to end our program
ended = False
count = 0

while not ended:
    if (count > 5):
        ended = True
    # Update the reader's input
    manager.reader.getInput()
    
    # Check if the reader has a full barcode
    if (manager.reader.done):
        # Display the reader's output
        print manager.reader.output
        # Make sure you clear the reader immediately after grabbing data from it.
        manager.reader.clear()
        count += 1
    