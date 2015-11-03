import barcodeReaderAPI

# Create a BarcodeReader object
reader = barcodeReaderAPI.BarcodeReader()

# Some vars to decide when to end our program
ended = False
count = 0

while not ended:
    if (count > 5):
        ended = True
    # Update the reader's input
    reader.getInput()
    
    # Check if the reader has a full barcode
    if (reader.done):
        # Display the reader's output
        print reader.output
        # Make sure you clear the reader immediately after grabbing data from it.
        reader.clear()
        count += 1
    