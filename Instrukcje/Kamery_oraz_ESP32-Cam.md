## Kamery i pakiet od podazania
### Kamery USB
Podstawowa sprawa bylu uzycie kamer USB by pakiet ar_track_alvar [https://wiki.ros.org/ar_track_alvar], mogl odbierac dane z (any topic in an image format) (sensor_msgs/Image) dopiero na tej podstawie moze wykonac operacje przy uzyciu biblioteki OpenCV by poznac polozenie markerow.

Pierwsze zostalo zainstalowanie dla sprawdzenia czy kamera USB jest podpieta zainstalowane zostalo narzedzie v4l-utils (video for linux), pozwala to nasprawdzanie obecnosci urzadzen (mozna tez przy uzyciu VLC)
- Komenda instalacji:
-       sudo apt-get install v4l-utils
- Wysietlenie podpietych kamer
-        v4l2-ctl --list-devices
- Po tej komendzie dostaje sie informacje pod jakim urzadzeniem jest jaka kamera np.
- Brio100 pod /dev/video0 (i na podstawie tej informacji ustawione zostaly pliki by odbierac dane z kamer)

Dla sprawdzenia samej poprawnosci kamer najszybciej bylo mi uzyc ffmpeg, instalacja:
-       sudo apt install ffmpeg
- A dokladniej komedny:
-       ffplay /dev/video0


Sam ROS noetic uzywa paczki usb_cam [https://wiki.ros.org/usb_cam], który sam w sobie **potrzebuje miec zaintalowane v4l-utils**, ta paczka pozwala na obsluge kamer w obrebie ROSa

### Pakiet ar_track_alvar
[https://github.com/ros-perception/ar_track_alvar]
Krotka notka o samymy pakiecie, nie udawalo mi sie go zainstalowac prostym zainstalowanie do wspolnych bibliotek, musialem recznie go dodac do projektu (co w dalejsz kolejnosci wymaga zawsze budownia go, ze wzgledu na niestandardowe wiadomosci).

Beda w workspace/src:
-       git clone -b noetic-devel https://github.com/ros-perception/ar_track_alvar.git
-       cd ..
-       rosdep install --from-paths src --ignore-src -r -y
-       catkin_make
W workspace/src, potrzebne jest zarowno paczka od obslugi nodow oraz paczka od obslugiwania wiadomosci

Sam node ar_tag_tracker.py (od podazania) zostaw zmodyfikowany z ar_tag_toolbox:
- [https://github.com/atomoclast/ar_tag_toolbox]
- [https://realitybytes.blog/2017/06/02/detecting-and-tracking-ar-tags/]

### Uzycie ESP32-CAM
W projekcie jest zawart ale nie uzytu node obslugujacy wykorzystanie streamowania obrazu przy uzyciu esp32-cam.

Samo ESP32-CAM oraz program wgrany jest w glownej mierze opary na bibliotece *Micro-RTSP* [https://github.com/geeksville/Micro-RTSP], ktora pozwala na skorzystanie z protokolu RTSP (Real Time Streaming Protocol), ktora w dalszej mierze jestesmy wstanie odbrac w ROSie za pomoca pakietu video_stream_opencv [https://wiki.ros.org/video_stream_opencv]. Ta wstawka jest tylko jako PoC, ktora dziala ale jest z nia kilka problemow.

#### ESP32-CAM
Program wgrany zostal przy uzyciu Arduino IDE, wraz z zainstalowana odpowiednia biblioteka do plytek ESP32 (jest duzo tutoriali wszystkie robia to samo) oraz z wczesniej wspomniana biblioteka Micro-RTSP. Szukajac rozwiazan natrafilem na takze pewnego rodzaju PoC:
- [https://www.youtube.com/watch?v=IL-tCeTqJqM&list=PLAFdwozmDOrdp8WOconq7zoiOWfSOrHFo&index=8]
- [https://github.com/inaciose/esp32-cam-rtsp]

Kod na esp udostepniony tam takze opiera sie na Micro-RTSP ale na wersji tej biblioteki sprzed 6 lat, musialem wrocic po odpowiednich commit do odpowiedniej wersji. Zarowno kod jak i odpowiednia wersja Micro-RTSP, bedzie zawarta w folderze dla esp. W przyszlosci mozna pomysle o zaktualizowaniu tej wersji kodu na najnowsza wersje biblioteki.

Po wgraniu kodu na ESP, uruchomieniu serwera oraz strumienia, znajac IP ESP mozna podejrzec obraz wyswietlany z esp, jest on odpowiedniego formatu by byc uzywany przez ar_track_alvar, wiec jest tez odpowiedniego formatu by uzyc biblioteki OpenCV.

Natomiast glowne problemu korzystania z ESP32-CAM i dlaczego to jest tylko PoC:
- Aby korzystac w roznych sieciach (U siebie vs w laboratorium), za kazdym razem trzeba wgrywac wersje na ESP z odpowiednimi danymi do sieci (nazwa, haslo), co samo w sobie jest upierdliwe (a tym bardziej dla 4 ESP32-CAM)
- Dla kogos moze bardziej obeznanego w EPS moze da sie to robic dynamicznie (ja tak tego nie zglebilem)
- Przechodza miedzy sieciami nawet nie mam pewnosci czy udalo sie polaczyc z inna siecia, gdyz potrzebne jest podlacznie sie po UART z esp, by tam dopiero poznac IP (chyba ze jest ustawione takie samo nie zalezne od sieci)
- Jakosc obrazu z kamery ESP32-CAM, nawet z OV2640, byla zla, moze to wynikalo z ustawien jakie zostaly dane do kamery, natomiast widocznosc byla tragiczna
- Ostatni problem i to ten najbardziej znaczaczy to opoznienie przesylu obrazu. Samo opoznienie wahalo sie, od takiego w miare ok, do opoznienia o 3 sekundy. W sytuacji podazania jaka miala miec w tym projekcie wrzucanie kolejnego zaklocenia w postaci opoznienia przesylu obrazu z kamery, prawdopodobnie nie pozwoliloby na wykowanie badania. 

Samo korzystanie z tego rozwiazania, po wgraniu kodu na esp, jesli mu nic nie przeszkadza i zacznie cos wyswietlac na terminalu z polaczeniem szeregowym to poda swoje IP, np.:

---
Serial connected \
...WiFi connected

192.168.1.20

---
Przy pomocy np. VLC mozna sprawdzic poprawnosc streamowanego obrazu:
- Wlaczyc VLC
- W zakladce: Media -> Open Network Stream
- wpisac:
-       rtsp://192.168.1.20:8554/mjpeg/1
- Dac play, jest obraz sie pojawia ROS takze bedzie mogl go zobaczyc przy uzyciu video_stream_opencv

Jeśli strumień jest, w rosie, zainstalowac video_stream_opencv:

        sudo apt-get install ros-noetic-video-stream-opencv

Ja zrobilem osobna paczke by zawrzec zaleznosc od tej biblioteki (wiec powinno samo sie zainstalowac)

Aby uruchomic w wersji ktora pozwala na dalsze wykorzysywanie:

        roslaunch esp32_cam_rtsp esp32_cam.launch

I jest obraz, mozna to zobaczyc gdyz sa odpowiednie topic, na:

        rostopic list

i tam bedzie:

        /esp32_cam/image_raw

Ktore mozna podejrzec:

        rqt_image_view

I wybrac /esp32_cam/image_raw

Potwierdza to mozliwosc wykrzystania ESP32-CAM jako kamery, nawet zostala zamodelowana obudowa laczaca sie z gimbalem.

