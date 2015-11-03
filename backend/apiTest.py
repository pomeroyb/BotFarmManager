import barcodeReaderAPI

ended = False
reader = barcodeReaderAPI.BarcodeReader
count = 0

while not ended:
    if (count > 5):
        ended = True
    reader.getInput()
    if (reader.done):
        print reader.output
        reader.clear()
        count++
    