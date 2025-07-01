## Uruchamianie jednostk
Po poprawnym skopiowaniu projektu, w przypadku gdy nie wyskakują już żadne błędy można przejeść do uruchamiania poszczegłolnych jednostek

### Uruchamianie lidera

- Odlaczyc wszystko od mini komputera
- Wlaczy komputer
- Poczekac az poprawnie zaladuje sie ubuntu
- Polaczyc sie maunalne (klawiatura, myszka, monitor) lub przy pomocy ssh/shh+VNC/VNC (wymagane jest podlaczenie wyswietlacza/dummy plug'a)
- Zsorsowac ROS (Na kazdym z komputerów jest to juz wrzucone w .bashrc [Robi sie z kazdym nowym terminalnem])
-       source /opt/ros/noetic/setup.bash
- Przejsc do catkin_ws [Workspace] (Na komputerach catkin_ws, tutaj sam plik rzuf)
- Zbudować projekt komendą:
-       catkin_make
- Zsorsowac workspaca projektu, np.
-       source ~/workplace/rzuf/devel/setup.bash
- Wlaczyc odpowiednia ilosc terminali (Zazwyczaj min. 3 terminale)
- Kazdy nowy terminal trzeba zbudowac i sorsowac projekt (wynika to z uzycia paczki ar_track_alvar, jako że jest zainstalowana lokalnie)
- Przyklad uzycia terminali: W 1 roscore, w 2 lider/podazajacy, w 3 *rostopic list* lub *rostopic echo /temat*
- Zanim uruchomi sie lidera nalezy podlaczyc urzadzenia peryferyjne (Arduino, plyte hoverboarda, kamere, lidara)
- Dla arduino oraz hoverboarda nalezy jednorazowo podczas wlaczenia komputera nadac uprawnienia na przesylanie danych po USB, kolejnosc podlaczenia wynika z wpisanych sciezek do odpowiednich urzadzen USB
- **Do tego momentu uruchamianie dla jednostek podazajacych jest takie samo**
- Zanim zasili sie uklad majacy odbiornik RC (uklad zasilajacy go), to kontroler/nadajnik RC musi zostac wlaczany przed nim (nalezy takze pamietam o poprzednim zparowaniu kontrolera i odbiornika)
- Pierwsze nalezy podlaczyc arduino (zeby bylo na /dev/ttyUSB0 bo tak jest w plikach dla rosserial), komenda nadajaca uprawenia 
-       sudo chmod 666 /dev/ttyUSB0
- Następne nalezy podlaczyc konwerter UART-USB uzyty do plyty glownej hoverboarda
-       sudo chmod 666 /dev/ttyUSB1
- Po nadaniu uprawnieni mozna juz wszystko wlaczac:
- 1 terminal:
-       roscore
- 2 terminal:
-       roslaunch master_launcher robot_startup.launch
- W tym momencie sterownik z hoverboard_drive upomni sie, ze plyta glowna nie zostala wlaczona, i w tym momencie ja najczescie odchodzilem od komputera by zewrzec piny dla wlaczenia plyty (odwoluje do rysunku pinout plyty glownej)
- 3 terminal:
-       rostopic list       lub         rostopic echo /temat       

Dla samych robot pakiet hoverboard_driver pozwala na dynamiczne ustawienia wartości pid kol w 3 lub 4 terminale:

        rosrun rqt_reconfigure rqt_reconfigure

[https://wiki.ros.org/rqt_reconfigure]

---

Dla sprawdzenia czy kamera USB jest podpieta zainstalowane zostalo narzedzie v4l-utils (video for linux), pozwala to nasprawdzanie obecnosci urzadzen (mozna tez przy uzyciu VLC)
- Wysietlenie podpietych kamer
-        v4l2-ctl --list-devices

---

### Uruchamianie jednostek podazajacych

Dochodzac do momentu podlaczania urzadzen peryferyjnych, dla jednostek podazajacych zalozone zostalo ze nie jest uzyte arduino, wiec jedyne nadanie uprawnien dla USB wystepuje przy podlaczaniu plyty glownej hoverboarda za pomoca konwertera UART-USB. Wplywa to na kolejnosc jaka jest rejestrowana w ubuntu urzadzenia 
- Pierwsze co jest podlaczane to konwerter UART-USB uzyty do plyty glownej hoverboarda
-       sudo chmod 666 /dev/ttyUSB0
- Po nadaniu uprawnieni mozna juz wszystko wlaczac:
- 1 terminal:
-       roscore
- 2 terminal:
-       roslaunch master_launcher line_follower.launch
- W przypadku uruchomienia kolejnego robota podazajacego (trzeciego/czwartego), jedyna roznica jest w zawartosci plikow, zmienione sa tylko wartosci ID markerow, ktorych ma szukac ale dla uruchamianie tego tylko jedna linijka utworzone zostaly nowe pliki .launch
- Dla trzeciego robota, patrzy sie na marker o ID = 4
-       roslaunch master_launcher line_follower_trzeci.launch
- Dla czwartego robota, patrzy sie na marker o ID = 7 (ale chyba przez pomylke jest naklejony marker o ID = 6 na tyle robota trzeciego)
-       roslaunch master_launcher line_follower_czwarty.launch
- Jak wspomnianie wyzej roznej pliki z master_launch wskazuja na inne pliki .launch znajdujace sie w paczce ar_tag_tracker, a o sciezce /ar_tag_tracker/launch/* , tam zachodzi zmiana wartosci obserwowanego ID w tych plikach
- 3 terminal:
-       rostopic list       lub         rostopic echo /temat   
- 4 terminal: (jesli tylko podejrzenie do kamery, nie trzeba budowac i sorsowac)
-       rqt_image_view
- Wybrac odpowiednia sciezke dla obrazu (np. /usb_cam/image_raw)


### Rozne przydatne komendy

- Uruchomienie tylko noda z rosserial dla arduino (po nadaniu uprawnien):
-       rosrun rosserial_python serial_node.py /dev/ttyUSB0
- Komenda do uruchomienia plyty (po nadaniu uprawnien, w pliku hoverboard.launch wpisuje sie miejsce urzadzenia USB, lub w pliku config.h [Po zmianie trzeba na nowo zbudowac]):
-       roslaunch hoverboard_driver hoverboard.launch
- Uruchomienie tylko kamery:
-       roslanuch usb_cam_test usb_cam.launch
- W paczce usb_cam_test rozne pliki launch roznia sie tylko sciezkami do plikow z kalibracji (jedna byla moja, a reszta z laboratorium)
- Komenda do kalibracji kamery, szachownica 8x6, wielkosc czarnych kwadratow 25x25 [mm] (zapisywane jest to tymczasowo jako ostatnia kalibracja wiec trzeba skopiowac, a potem podac siezke do pliku .yaml)
-       rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.025 image:=/usb_cam/image_raw camera:=usb_cam
- kopiowanie kalibracji, zapisze sie wtedy w folderze calibration w paczce ucb_cam_test:
-       cp ~/.ros/camera_info/head_camera.yaml ~/catkin_ws/src/usb_cam_test/calibration/usb_cam.yaml
- Po uruchomieniu roscora oraz kamery, sprawdzenie dzialania paczki ar_track_alvar, mozna sprawdzic czy jest wgl widziny marker:
-       roslaunch  ar_track_alvar ar_track_alvar.launch
- Osobne sprawdzenie jest dla samego podazania czy wydaje poprawne komendy na /cmd_vel, po uruchomieniu roscore, kamery, ar_track_alvara:
-       rosrun ar_tag_tracker ar_tag_tracker.py
- lub, za pomoca launch tam mozna zmienia wartosci ID markerow
-       roslaunch ar_tag_tracker track_tag.py
-       roslaunch ar_tag_tracker track_tag_trzeci.py
-       roslaunch ar_tag_tracker track_tag_czwarty.py
- Uruchomienie LiDARa jest z gotowej paczki urg_node, wystarczy ja zainstalowac oraz komenda:
-       roslaunch urg_node_test lidar.launch
- Osobno dla obslugiwania noda z arduino powstaly rc_control oraz serco_control, po uruchomieniu recznym rosseriala mozna przetestowac:
-       rosrun rc_control rc_channels_to_cmd_vel.py
-       rosrun servo_control servo_angle_publisher.py
- Komenda ponizej z servo_control pozwala uzytkowniko na podawanie wartosci katow serw, by zobaczyc jak sie ustawi gimbal:
-       rosrun servo_control TEST_servo_angle_publisher.py
- Wszystkie dane z czujnikow mozna sprawdzac w rviz, komenda:
-       rviz
- Wczesniej wspomniane komendy z dla topic oraz nodow:
-       rostopic list
-       rostopic echo /topic
-       rosnode list
- Przypominajka, ze dla nowych plikow wykonawczych w paczka trzeba nadac uprawnien do wykonania (executable)
-       chmod +x plik_wykonujacy.py
- Po poprawnym zainstalowaniu ros noetic powinna byc mozliwosci korzystania z rosdep w workspacsie, wtedy mozemy uzyc:
-       rosdep install --from-paths src --ignore-src -r -y