# What is it?

SinkNode is a a data ingestor with a very simple structure. Read stuff in and spit stuff out the other end. When you need to read in a data stream from somewhere and put it somewhere else, use SinkNode.

# All the bits

SinkNode is made up of 2 main things: Readers, and Writers (fancy that!). 

## Readers
 They read in from a stream, file, website, whatever and split the data into individual entries, then are squeezed out in JSON format. They read stuff.

Active modules:
    SerialReader - Read in from a Serial stream
    XBeeReader - Read in from XBee API packets
    WalkerReader - A custom XBee reader for a sensor network project

## Writers
Writers write things. Water is wet. Trucks are weird. Jokes aside, writing is a vague term. Writing data can mean archiving, uploading, sending to a display; basically any data on the way out. Basically pushing data to an endpoint.

Active modules:
    LogFileWriter - Writes data to a specified log file
    ThingSpeakWriter - Uploads data entries to Thingspeak

### Formatter
Readers are at the 'in' point, Writers are at the 'out' point. Formatters are the guts of this code puppy. They hide as a thread inside each writer to format the data from readers into something that can be used by a writer.

    e.g: Serial data from arduino >> (SerialReader) >> (ThingspeakFormatter) >> (ThingspeakWriter) >> Data uploaded on the web

# Install it

## The easy way (pip)

SinkNode is available on pip. Install by using the following command in a terminal.

    sudo pip install sinknode

## The other way 

The other way to install the package is to use the regular python installer.
Using a command line (like bash), grab the git repository and install the package by typing in the following:
    
    git clone git://github.com/Leenix/SinkNode
    python setup.py install

If you're using a Windows environment, you may need to use absolute paths for python and the setup file. 
i.e:
    
    c:\Python27\python.exe <path to repo>\SinkNode\setup.py install

# Use it

    Coming soon...

# Add to it

    Coming soon...