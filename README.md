# BotFarmManager
Keep track of the status of your 3D printers.

## Project Goals
- Provide an easy to use interface for maintaining the status of your 3D printer bot farm
- Utilize standard barcode readers to update a bot farm database
- Send bot farm status to a server on change
- Pretty :sparkles: website that reads bot farm status and updates accordingly

## Barcode Specifications
Since the Pi runs headless, all interaction with the manager is done using the barcode scanner. There are four different types of barcodes:

| Type   | Description |
|--------|--------|
|   BotSerial     | Unique 3D printer identifier. Affixed to the Bot  |
|  Commands       | Barcodes that let you modify the printers in your farm|
|  Status         | Boolean values that define diagnosed problems |
|  Events         | Values the keep tallies of the number of times certain symptoms are seen|

All codes will be encoded using the [Code 128](https://en.wikipedia.org/wiki/Code_128) standard.


## Languages
- The backend code will be primarily Python 2.7 (Running on a Raspberry Pi)
- The frontend code will be CSS and HTML, with maybe a sprinkle of JS if we want to get really fancy

