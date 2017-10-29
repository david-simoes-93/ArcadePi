# ArcadePi
A system to play MS-DOS, Sega, Win98 or any other videogame using arcade controllers and a DYI arcade station!

If you plan on using Arcade controls, start by installing [QJoyPad 4.1.0](http://qjoypad.sourceforge.net/#download). 

    sudo apt install libxtst-dev libqt4-dev
    wget http://downloads.sourceforge.net/qjoypad/qjoypad-4.1.0.tar.gz
    tar -zxvf qjoypad-4.1.0.tar.gz 
    cd qjoypad-4.1.0/src
    ./config
    Edit the Makefile line `LIBS = $(SUBLIBS)  -L/usr/lib/arm-linux-gnueabihf -lXtst -lQtGui -lQtCore -lpthread` to `LIBS = $(SUBLIBS)  -L/usr/lib/arm-linux-gnueabihf -lXtst -lQtGui -lQtCore -lpthread -lX11` (basically, append `-lX11`)
    make
    sudo make install
    
Next, get the emulators. Currently, only FastDosbox is being used.

    sudo apt install libsdl1.2-dev
    git clone https://github.com/slacka/FastDosbox
    cd FastDosbox/fastdosbox-1.6
    ./configure
    make
    sudo make install
    
If you're using Raspberry Pi, then overclock it

    vim /boot/config.txt
        arm_freq=1400
        sdram_freq=500
        over_voltage=5
        temp_limit=80
        gpu_mem=128
    
Now, download some games, put them in the Games folder (some are already configured), and, to actually run the game

    sudo pip3 install pynput
    sudo apt install python3-pil.imagetk
    python3 Arcade.py


