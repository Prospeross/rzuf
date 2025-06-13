## Projekt RZUF, na inzynierke
R.Z.U.F
Roboty Zwarcie Utrzymujące Formację

Jeszcze WIP, zostało dodanie opisówm, poprawki oraz ustawienie pidow

Trzeba pamiętać o robieniu: sudo chmod 666 /dev/(rosserial oraz hoverboard)

jakos nie dziala wprost git clone <to repo>
Kopiowanie:
na kompie z ubuntu 20.04 oraz rosem noetic, z sorsowac rosa
tam gdzie pasuje zrobic workspaca

        mkdir catkin_ws/src
        cd catkin_ws
        catkin_make

teraz w innym miejscu zrobic sb tymczasowe dir

        mkdir ~/rozne/temp
        cd ~/rozne/temp
        git clone <to repo>
        cd rzuf/src
        rm CMakeList.txt

Zapisac sb patha do tego 
        pwd

wrocic do poprawnego workspaca

        cd ~/droga/do/catkin_ws/src

skopiowac rzuf/src

        cp <co i skad> <gdzie skopiowac>

        cp ~/rozne/temp/rzuf/src/* .
gwiazdka ozancza wszyskto z src
kropka oznacza ze do aktualnego dira (ja tak zawyczaj robie bo przechodze do catkin_ws/src)
alternatywa

        cp ~/rozne/temp/rzuf/src/* ~/droga/do/catkin_ws/src/
nw czy / ma byc na koncu (chyba tak)


Dla ulatwienia, wlaczanie:

- Odlaczyć wszustko od kompa
- Wlaczy kompa
- Poczekac az sie zaladuje ubuntu
--(tego co ma bootloader rozwalony trzeba recznie poprawnie zbootwaoc)
- Polaczyć sie ssh/shh+VNC/VNC/lub maualnie monitor,klawa, myszka
--(dla VNC, musi byc monitor podpiety lub dummy plug)
--(mozna zrobi sztuczke, podpiszan monitor, laczysz sie, odpalasz wszystko, odpinasz monitor, mozna uzywac)
- na kazdym jest juz zsorsowany ROS
- przejsc do catkin_ws(na kompach catkin_ws, tutaj sam rzuf)
-       catkin_make
- Zsorsowac workspaca
- odpalic potrzebna ilosc terminali (ja robie 3)
- kazdy odpalony terminal trzeba budowac i sorsowac (trzeba budowac dla ar_track_msgs)
- W 1 roscore, w 2 lider/podazajacy, w 3 rostopic sprawdzac
- zanim wszystko wlaczy w 2 termianlu ustawic uprawnienia dla usb(tam gdzie masterlauncha sie odapal)
- podlaczyc arduino (zeby bylo na /dev/ttyUSB0 bo tak jest w plikach)
-       sudo chmod 666 /dev/ttyUSB0
- podlaczyc konwerter hovera
-       sudo chmod 666 /dev/ttyUSB1
mozna juz wszystko wlaczac
- 1 terminal:       roscore
- 2 terminal:       roslaunch master_launcher robot_startup.launch
- lub dla podazajcych:      roslaunch master_launcher line_follower.launch
dla kazdego nastpengo odpowiednio jak pisze w master-launcher
- no i powinno wszystko dziala 

Dla samych robot trzeba jeszcze pidy ustawic, wiec nalezy je odpalic jako lidera oraz uzyc 
        rosrun rqt_reconfigure rqt_reconfigure

[https://wiki.ros.org/rqt_reconfigure]

W plikach dla podazajacy jest ustawione, tak jakby podazajacy nie mial arduino, i ma miec tylko konweter usb-uart dla hover oraz kamera to w plikach, jest tam pprostu ze hover jest na /dev/ttyUSB0 a nie na USB1.
Onacza to ze trzbe tylko dac upraw dla USB0