# ArcadePi
A system to play MS-DOS, Sega, Win98, GameBoy, or any other videogame using arcade controllers and a DYI arcade station!

If you plan on using Arcade controls, start by installing [QJoyPad 4.1.0](http://qjoypad.sourceforge.net/#download). 

    sudo apt install libxtst-dev libqt4-dev
    wget http://downloads.sourceforge.net/qjoypad/qjoypad-4.1.0.tar.gz
    tar -zxvf qjoypad-4.1.0.tar.gz 
    cd qjoypad-4.1.0/src
    ./config
    vim Makefile
        LIBS = $(SUBLIBS)  -L/usr/lib/arm-linux-gnueabihf -lXtst -lQtGui -lQtCore -lpthread -lX11
    make
    sudo make install
    
Next, get the emulators. Currently, we are only using RetroPie's [DosBox](https://www.dosbox.com/), but there are instructions for RetroPie's [Mame](http://mamedev.org/) and [VisualByAdvance](https://sourceforge.net/projects/vba/) here too:
    
    sudo apt install libsdl1.2-dev automake libsdl2-ttf-dev
    
    cd
    git clone https://github.com/RetroPie/mame4all-pi
    cd mame4all-pi
    make -j4
    
    cd
    wget https://files.retropie.org.uk/archives/dosbox-r3876.tar.gz
    tar zxvf dosbox-r3876.tar.gz
    cd dosbox
    ./autogen.sh
    ./configure --disable-opengl
    vim config.h
        #define C_DYNREC 1
        #define C_TARGETCPU ARMV7LE
        #define C_UNALIGNED_MEMORY 1
    make -j4
    sudo make install
    
    cd
    git clone https://github.com/x3ro/VisualBoyAdvance
    cd VisualBoyAdvance
    ./configure
    vim src/prof/Prof.cpp    # line 274
        profWrite32(fd, atoi(seg->tos[toindex].selfpc)) ||
    vim src/Util.cpp         # line 995
        utilGzWriteFunc = (int (ZEXPORT *)(gzFile_s *,void * const, unsigned int))gzwrite;
    make -j4
    sudo make install
    
    
If you're using Raspberry Pi, I suggest overclock it (although I don't take responsability if it melts)

    echo "performance" |sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    vim /boot/config.txt
        arm_freq=1400
        sdram_freq=500
        gpu_freq=550
        over_voltage=5
        temp_limit=80
        gpu_mem=128
    
Get and configure this repository for your username (`pi` in this case) and for your controllers (in my case, changing Axis 4 to Axis 2)

    cd
    git clone https://github.com/bluemoon93/ArcadePi/
    cd ArcadePi
    sed -i 's/Axis 4/Axis 2/g' GameConfigs/*.lyt
    sed -i 's/Axis 4/Axis 2/g' Gui.lyt
    sed -i 's/david/pi/g' RunGame.py
    
If desired, set things to run at start-up
    
    cd
    sudo apt install xautomation
    vim start_game.sh
        #!/bin/bash
        xte 'mousermove 1000 1000'
        cd /home/pi/ArcadePi
        python3 Arcade.py
    chmod +x start_game.sh 
    vim ~/.config/autostart/start_arcade.desktop
        [Desktop Entry]
        Name=start_arcade
        Exec=/home/pi/start_game.sh
        Type=Application
        X-GNOME-Autostart-enabled=true

    
Now, download some games, put them in the Games folder (some are already configured), and, to actually run the game

    sudo pip3 install pynput
    sudo apt install python3-pil.imagetk
    python3 Arcade.py


