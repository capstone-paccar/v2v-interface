# *Raspberry Pi Setup*
***
***This document describes the process for setting up*** **batman-adv,** ***which configures an Ad-Hoc mesh network on a Raspberry Pi.***
***

## Background
Standing for "better approach to mobile ad-hoc networking," B.A.T.M.A.N Advanced or **batman-adv** is the linux-based network routing protocol used to manage Ad-Hoc mesh networks in the Vehicle-to-Vehicle Update Delivery System. To learn more about this protocol, here is the [official documentation](https://www.open-mesh.org/projects/batman-adv/wiki/Doc-overview).

### Some Things to Note
* When running on multiple Pis, ensure that all programming files are the same and that the hostname is different for each Pi.
* You may also need to change the first line of **update.txt** for each Pi for the program to function.
* To test further, try pinging another device by using the **ping** command in the terminal followed by the IP address of another Pi.
* Ethernet must be unplugged for the v2v_interface program to run correctly.
* Following this guide will disable your Pi's integrated WiFi.
***

## Performing Initial Raspberry Pi Setup
See the [official setup documentation](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up) to set up and start up your Pi.

Instead of using a wall-to-usbc adapter, you may want to use a high mAh capacity power bank to make the module portable. Additionally, you may want a 3.5 inch touchscreen to connect to the top of the Pi as a display for program statistics and progress.

## Setting up batman-adv
We will configure **batman-adv** such that it takes over the WiFi interface **wlan0** and sets up a tandem WiFi interface **bat0**. This enables the Pi to send network sockets over the wlan0 antenna while using IP addresses set by bat0 and deploys a mesh network.

1. Install **batctl**

    batctl is a control tool for batman-adv. To install, use the command:
    ```bash
    sudo apt-get install batctl
    ```
    * If the batctl present in the Raspberry Pi repository is out of date, run this command to install the "latest version" (as of June 1, 2021):
        ```bash
        sudo apt purge batctl -y &&  \
        sudo apt install libnl-genl-3-dev libnl-3-dev -y && \
        wget https://downloads.open-mesh.org/batman/releases/batman-adv-2020.4/batctl-2020.4.tar.gz &&  \
        tar -xvf batctl-2020.4.tar.gz && \
        cd batctl-2020.4 && \
        make -j 4 && \
        sudo make install
        ```

2. Create **start-batman-adv**
    
    start-batman-adv will serve as an executable that runs the necessary commands to start the mesh network. Use the following commands to create and edit the executable:
    ```bash
    cd ~ && touch start-batman-adv.sh && chmod +x start-batman-adv.sh
    sudo nano start-batman-adv.sh
    ```

    On the nano editor, add the following to start-batman-adv:
    ```bash
    #!/bin/bash

    # Tell batman-adv which interface to use
    sudo batctl if add wlan0
    sudo ifconfig bat0 mtu 1400
    sudo ifconfig wlan0 mtu 1500

    # Activates the interfaces for batman-adv
    sudo ifconfig wlan0 up
    sudo ifconfig bat0 up
    ```

3. Configure Interfaces **wlan0** and **bat0**

    First ensure that the interfaces are set up correctly by opening the interfaces file using the following command:
    ```bash
    sudo nano /etc/network/interfaces
    ```
    And ensure the following line is written in the file:
    ```bash
    # Include files from /etc/network/interfaces.d
    source-directory /etc/network/interfaces.d
    ```

    Next, create/find **wlan0**:
    ```bash
    sudo nano /etc/network/interfaced.d/wlan0
    ```
    And ensure the following is written in the file:
    ```d
    auto bat0
    iface bat0 inet6 auto
        pre-up /usr/sbin/batctl if add eth0
        pre-up /usr/sbin/batctl if add wlan0
    ```

    Finally, create **bat0**:
    ```bash
    sudo nano /etc/network/interfaced.d/bat0
    ```
    And ensure the following is written in the file:
    ```d
    auto wlan0
    iface wlan0 inet6 manual
        mtu 1532
        wireless-channel 1
        wireless-essid my-mesh-network
        wireless-mode ad-hoc
        wireless-ap 02:12:34:56:78:9A
    ```

4. Enabling **Automatic Run-on-Startup**

    Running the following commands will enable the Pi to start deploying a mesh network on boot:
    ```bash
    # Starts batman-adv at boot
    echo 'batman-adv' | sudo tee --append /etc/modules

    # Prevents DHCPCD from automatically configuring wlan0
    echo 'denyinterfaces wlan0' | sudo tee --append /etc/dhcpcd.conf
    
    # Enables start-batman-adv to execute at boot
    echo "$(pwd)/start-batman-adv.sh" >> ~/.bashrc
    ```

5. **Reboot**

    Reboot with the following command to put all changes into effect:
    ```bash
    sudo reboot
    ```

6. **Test** for a Functioning Mesh Network

    Test by running the following two commands:
    ```bash
    sudo batctl if
    sudo batctl n
    ```
    If the first command gives the following response, then the network is functioning:
    ```bash
    wlan0: active
    ```
    If the second command gives at least one MAC address, those devices are connected to the mesh network.

## Setting Program to Run on Startup
Assuming the program was downloaded, to set the v2v_interface program to run on boot, run the following command:
```bash
sudo nano ~/.bashrc
```
And scroll to the bottom of the file. At the very bottom of the file, add two lines which contain the following:
```bash
sleep 15
cd v2v_interface
python3 main.py
```
Then run the following command:
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
And at the very bottom of the file, add a line which contains the following:
```bash
@lxterminal
```
Then reboot to put the changes into effect:
```bash
sudo reboot
```

## Setting up the Touchscreen
Depending on which screen you use, instructions may very. The following instructions use an UCTRONICS 3.5 Inch Touchscreen for program input.

1. Install **UCTRONICS Drivers**

    See the official [instructions](https://www.uctronics.com/download/Amazon/B0106.pdf) to set up the Raspberry Pi for the touchscreen.

    After the driver installation process reboots your Pi, you may have to change the display resolution. To do this on Raspberry Pi OS, click the Raspberry Pi button in the upper-left corner and go to **Preferences -> Rasbperry Pi Configuration -> Display**. Click the button titled **Set Resolution...** and set the resolution to **CEA Mode 2 720x480 60Hz 4:3**. When you exit or press **OK**, the Pi will restart with a better resolution. If you get a black border around your screen, go back to **Raspberry Pi Configuration -> Display** and check **Disable** where it says **Overscan:**.

2. **Rotate Display** 90°

    Since the program has a vertical GUI, rotating the screen 90° will allow it to be displayed. To do this, run the following command:
    ```bash
    sudo nano /boot/config.txt
    ```
    And scroll to the bottom of the file. At the very bottom of the file, add one line which contains the following:
    ```bash
    display_rotate=1
    ```
    Do not reboot yet. We must also rotate the touch interfaces. To do this, run the following command:
    ```bash
    sudo nano ~/.bashrc
    ```
    And again scroll to the bottom of the file. At the very bottom of the file, add one line which contains the following:
    ```bash
    xinput set-prop 'ADS7846 Touchscreen' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1
    ```
    Then reboot to put the changes into effect:
    ```bash
    sudo reboot
    ```
