## Instalowanie SSH

### Windows
Na Windowsie (windows jest klientem) windows -> ubunt \
[https://www.youtube.com/watch?v=3hbJZZ4c1io] \
[https://www.youtube.com/watch?v=pucicb_qQ0g] 

W funkcje opcjonalne (Optional features) dodac:
OpenSSH Client

Jesli już jest to w terminal (cmd lub Windows PowerShell) po wpisaniu

        ssh 
powinno cos wyskoczyc

### Ubuntu

Na ubuntu trzeba zainstalować openSSH server (bo jest servem) 

[https://documentation.ubuntu.com/server/how-to/security/openssh-server/index.html] \
[https://www.youtube.com/watch?v=Wlmne44M6fQ] 

Zanim cokolwiek:

        sudo apt update

        sudo apt upgrade

W terminalu komenda:

        sudo apt install openssh-server


Zeby sprawdzić czy zostalo zainstalowane:

        sudo systemctl status ssh

Potem trzeba mu dac pzowolenie na interakcje w siecie przez firewall:

        sudo ufw allow ssh

### Laczenie sie

Już powinno dzialac, potrzeba jeszcze tylko ip samego ubuntu i jego nazwy, nazwa to jak jesteś w terminalu to pisze 
        nazwa@uzytkownik:~$
No i nazwa to nazwa a dalej by uzyska ip w terminalu komenda

        ip a
I tam gdzies bedzie podane IP np. 192.168.1.4

Aby się polaczy to oba komputery musza być wlaczaone, w terminalu na windowsie (czy to cmd, czy Windows PowerShell):

        ssh nazwa@ip 
czyli np.:

        ssh ubuntu@192.168.1.4

Za pierwszym razem zapyta się o fingerprinty, które trzeba zaakceptowac

Po stronie windowsa, który chce sie polaczyc z ubuntu podczas proby zalogowania sie do ubuntu zapyta o haslo tego uzytkownika (ogolnie to tworzy nowa sesje uzytkownika)

Zeby wyjsc w terminalu windowsa:

        exit

Mozna jeszcze na stale dac kulcz ssh jesli sie komus chce, wtedy nie trzeba wpisywac hasla

#### **WAZNE**
Z tego co mi sie wydaje otworzenie nowego okna oraz polaczenie sie spowoduje utworzenie nowej sesji uzytkownika, co nie pozwala na korzystanie w taki sposobu z:
- W 1 terminalu ssh: roscore
- W 2 terminalu ssh: roslaunch master_launcher robot_startup.launch

Nie powinno to dzialac, nie testowalem, poniewaz odrazu zakladam, ze nie dziala.

Aby uzywac SSH do operowania robotami **nalezy** skorzystac z multiplexerow terminali:
- GNU Screen
- tmux

Wyzej wymienione dzialaja prawie na takiej samej zasadzie ale inaczej sie je obsluguje. Oba w obrebie jednej sesji (jednego terminalu) dodaja "nowe" terminale miedzy ktorymi przemieszcza sie uzytkownika, ja korzystalem z multiplexera *screen*, podstawowe komendy:
- Utworzenie nowego okna (window) w obrebie jednego screena
- ctrl + a -> c
- Przemieszcanie sie miedzy oknami, do przodu:
- ctrl + a -> n
- Przemieszcanie sie miedzy oknami, do tylu:
- ctrl + a -> p

Te komendy wystarcza aby uruchomic robota, mozna na nich debugowac i tak dalej, ale jest to meczace, gdyz aby cokolwiek zobaczy trzeba uzywac komend: *cat plik.py* oraz wprowadzac zmiany przy uzyciu *nano plik.py*, strasznie meczace.

Tutorial do screen'a:
[https://www.youtube.com/watch?v=I4xVn6Io5Nw]

#### Tunelowanie przez ssh

Aby tunelowac przez ssh nalezy pierw sie polaczyc po ssh oraz nadac odpowiedni lokalny port przez ktory bedzie potem sie laczy w VNC np. po stronie windowsa:

        ssh -L 5900:localhost:5900 nazwa@ip

np.

        ssh -L 5900:localhost:5900 developer@192.168.1.21


Potem w thightVNC się laczysz z localhost:5900, a haslo jest to samo co zostalo stworzone po stronie ubuntu dla VNC.

## Instalowanie ThightVNC
Instalacja na windows \
[https://www.youtube.com/watch?v=mIdF7K3Nmlw&list=PLAFdwozmDOrcAbTYORyu_Elsh-Fc-gNDo&index=5] 

Instalacja na ubuntu \
[https://www.youtube.com/watch?v=3K1hUwxxYek&list=PLAFdwozmDOrcAbTYORyu_Elsh-Fc-gNDo&index=6] 

### Windows

Windows znowu jest klientem:\
W internecie wpisujesz ThightVNC, pobierasz i instalujesz odpowiednią wersję (zapewne windows x64)

wpisz hasla:\
- Remote access to jest jakby ktos chcial się DO windowsa polaczyc
- Admin pass to jest haslo potrzebne do wprowadzania zmian oraz do wylaczania/wlaczania vnc


### Ubuntu
        sudo apt update
        sudo apt upgrade


### Ponizsze komendy z filmiku wyzej.

#### Commands:
---
-       sudo apt update

-       sudo apt install lightdm
-       sudo reboot

-       sudo apt install x11vnc

-       sudo nano /lib/systemd/system/x11vnc.service

<--!Copy and paste these commands - change the password--> \
[Unit]
Description=x11vnc service
After=display-manager.service network.target syslog.target

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -forever -display :0 -auth guess -passwd password
ExecStop=/usr/bin/killall x11vnc
Restart=on-failure

[Install]
WantedBy=multi-user.target

<--!Save file and run these commands:-->

-       systemctl daemon-reload
-       systemctl enable x11vnc.service
-       systemctl start x11vnc.service
-       systemctl status x11vnc.service


---

Great website:
Website: https://bit.ly/2IOJUd8

----------------------------------------

IP mogly ulec zmianie, takie byly podczas testow, hasla do polaczenia zapisane na robotach

- developer@192.168.1.21
- agv2@192.168.1.23
- agv1@192.168.1.22

Aby podlaczyc sie przy uzyciu ThightVNC na windowsie nalezy wlaczyc aplikacje ThightVNC Viewer, tam w zaleznosci czy tunelowane przez ssh to po lokalnym porcie, jesli odrazu bez szyfrowania powyzszym ip (tylko IP sie podaje), nalezy wpisac hasla takie jakie sa do odpowiedniego robota.

Hasla mozna takze podejrzec na kazdym komputerze jakie zostaly zapisane w pliku, przy uzyciu komendy:
-       sudo nano /lib/systemd/system/x11vnc.service


------------------------------------