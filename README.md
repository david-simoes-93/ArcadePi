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
    
Get and configure this repository for your controllers (in my case, changing Axis 4 to Axis 2)

    cd
    git clone https://github.com/bluemoon93/ArcadePi/
    cd ArcadePi
    sed -i 's/Axis 4/Axis 2/g' GameConfigs/*.lyt
    sed -i 's/Axis 4/Axis 2/g' Gui.lyt
    
Next, get the emulators. Currently, we are only using [DosBox](https://www.dosbox.com/), [Gambatte](https://github.com/sinamas/gambatte), and [gameplaySP](https://github.com/gizmo98/gpsp), but there are instructions for [Mame](http://mamedev.org/), [VisualBoyAdvance-M](https://github.com/visualboyadvance-m/visualboyadvance-m) and [Mednafen](https://mednafen.github.io/) too:
    
    sudo apt install libsdl1.2-dev automake libsdl2-ttf-dev libsndfile1-dev scons
    
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
    git clone https://github.com/sinamas/gambatte.git
    cd gambatte
    ./build_sdl.sh
    sudo mv gambatte_sdl/gambatte_sdl /usr/bin/
    
    cd
    git clone https://github.com/gizmo98/gpsp.git
    cd gpsp/raspberrypi
    make -j4
    sudo mv gpsp /usr/bin/
    wget http://mirror1.freeroms.com/gameboy_advance_roms/gba_bios.zip
    unzip gba_bios.zip
    mv gba.bin ~/ArcadePi/gba_bios.bin
    mv ../game_config.txt ~/ArcadePi/

    # You can skip the next ones if you want to, we don't really use them
    
    cd
    git clone https://github.com/visualboyadvance-m/visualboyadvance-m
    cd visualboyadvance-m
    ./installdeps
    mkdir build && cd build
    cmake ..
    make -j4`
    
    cd
    wget https://mednafen.github.io/releases/files/mednafen-0.9.48.tar.xz
    tar xvf mednafen-0.9.48.tar.xz
    cd megnafen
    ./autogen.sh
    ./configure
    make -j4
    sudo make install
    mednafen
    sed -i 's/259/110/g' ~/.mednafen/*.cfg
    sed -i 's/258/109/g' ~/.mednafen/*.cfg
    sed -i 's/261/111/g' ~/.mednafen/*.cfg
    sed -i 's/262/112/g' ~/.mednafen/*.cfg
    sed -i 's/96/122/g' ~/.mednafen/*.cfg
    sed -i 's/13+alt/120/g' ~/.mednafen/*.cfg
    sed -i 's/sound.device default/sound.device sexyal-literal-default/g' ~/.mednafen/*.cfg
    sed -i 's/sound.driver default/sound.driver sdl/g' ~/.mednafen/*.cfg
    echo "flash 128" > ~/.mednafen/sav/"Pokemon - Emerald Version (USA, Europe).type"
    
    cd
    git clone https://github.com/RetroPie/mame4all-pi
    cd mame4all-pi
    make -j4
    
If you're using Raspberry Pi, I suggest overclocking it (although I don't take responsability if it melts)

    echo "performance" |sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    vim /boot/config.txt
        arm_freq=1400
        sdram_freq=500
        gpu_freq=550
        over_voltage=5
        temp_limit=80
        gpu_mem=128
    
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

    
Now, download some games, put them in the Games folder (some are already configured), and, to actually run the arcade

    sudo pip3 install pynput
    sudo apt install python3-pil.imagetk
    cd ~/ArcadePi
    python3 Arcade.py


