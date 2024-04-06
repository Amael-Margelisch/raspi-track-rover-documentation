(plan)=

# Plan 

:::{contents}
:::

## Présentation du projet

Ma principale motivation est d'explorer un nouveau système d'exploitation différent de Windows, en l'occurrence Linux. Je voulais aussi découvrir une technologie comme le Raspberry Pi et expérimenter avec des concepts de Machine Learning et de Computer Vision grâce à OpenCV. Je voulais également découvrir un peu la robotique et ce projet me permet de faire exactement cela. J'ai également hâte de voir comment l'ordinateur peut interagir avec le monde physique. En somme, ce projet me permet de m’essayer à la robotique et de voir comment un ordinateur peut interagir avec le monde.

## Manuel / conseils d'utilisation

Pour entrer dans le Raspberry Pi il faut soit y connecter le cable HDMI et un clavier et une souris plus son cable d'alimentation soit s'y connecter par SSH. 

```{tip}
Les informations de login sont les suivantes -->
user : amael, password : 123456, wifi : Youxipass, password wifi : nbkd5841
```

L'utilisation du rover est assez simple : le fichier permettant de lancer le programme est situé sur le Raspberry Pi et peut être exécuté soit via le terminal en utilisant la commande amael@raspberrypi:~ $ python /home/amael/Desktop/raspi_rover_main.py, soit en ouvrant Thonny et en lançant le code à partir de là. Lors du lancement, l'utilisateur est invité à spécifier la tolérance, qui correspond à la distance en pixels séparant la zone de détection des bords de l'image (voir schéma).

```{figure} img/rover_vision_schematic.png
---
width: 100%
---
Schéma de la vision du rover et de la forme que prend la tolérance.
```

Il est important de choisir une valeur de tolérance appropriée : une valeur trop grande rendrait la zone centrale de détection trop étroite, ce qui rendrait le comportement du robot instable car il ne parviendrait jamais à atteindre cette zone avec ses paramètres de correction. Des valeurs de tolérance généralement recommandées se situent entre 220 et 290 pixels.

Une fois le programme lancé, il suffit de se placer devant la caméra pour démarrer la reconnaissance et le suivi. Il est important de noter que vu que la reconnaissance tourne sur Raspberry Pi elle n'est pas très vive et donc il vaut mieux éviter les mouvements brusques. De plus, l'algorithme utilisé pour la reconnaissance est très sensible à l'éclairage et aux conditions environmentales ce qui parfois le rend peu précis et instable. Une fois le programme lancé il suffit de se deplacer devant le rover pour que la caméra suive.

:::{note}

Notez qu'il est possible que la caméra effectue parfois un mouvement brusque vers la droite ou la gauche. Pour corriger ce problème, il suffit de se placer devant la caméra et elle se réalignera automatiquement par rapport au robot.
:::

## Explication du fonctionnement du code

Le fichier d'entrée de ce projet est raspi_rover_main.py, il se situe dans /home/amael/Desktop, il permet de lancer le projet.

Pour ce projet j'utilise OpenCV, qui est une librairie python qui regroupe les algorithmes utiles dans le Computer Vision,  j'utilise le Haar Cascade c'est un modèle préentraine de OpenCV pour la detection de visage, et le Raspberry Pi et des moteurs LEGO techniques.

Explication de certaines parties du code.

```{code-block} python
---
#emphasize-lines: 3-4
linenos: true
---
import cv2 as cv
from picamera2 import Picamera2
from buildhat import Motor
from buildhat import MotorPair
```
Cette partie importe les différente librairies nécessaires au fonctionement du code.

```{code-block} python
---
emphasize-lines: 3-4
linenos: true
---
while True:
  frame = picam2.capture_array()
  gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  face_rect = haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=4, minSize=(80,80))
```
Cette partie permet de prendre une image depuis la camera du Raspberry Pi sous la forme d'un tableau numpy (numpy array) cette image est désormais stocké sous la variable ''frame'' puis pour que la detection de visage avec haar_cascade fonctionne il faut passer cette image en échelle de gris, c'est ce que cv.cvtColor(frame, cv.COLOR_BGR2GRAY) fait. On récupère ensuite l'image en échelle de gris dans la variable ''gray_frame'' et on la fait passer dans la fonction  haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=4, minSize=(80,80)) qui prend en paramètre une image, scale Factor - un facteur qui spécifie dans quelle mesure la taille de l’image est réduite à chaque échelle d’image, minNeighbors - détermine la quantité de voisins que chaque rectangle doit avoir pour le conserver, en bref, c'est un paramètre qui permet de rêgler la qualité de la détection de visage et minSize est un paramètre qui défini la taille minimum d'un visage pour qu'il soit détecté, cette fonction retourne une liste avec les coordonnées du visage par rapport à l'image ainsi que sa hauteur et sa largeur.

```{code-block} python
---
linenos: true
---
for (x,y,w,h) in face_rect:
  # Trace moving entities
  cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
  cv.circle(frame, (x + (w // 2), y + (h // 2)), 1, (255, 255, 0), 4)
```
Cette partie trace le rectangle qui représente la détection du visage par l'algorithme, et le cercle qui représente le centre de ce rectangle.

```{code-block} python
---
linenos: true
---
pos = -1 # error signal / no object detected
  
if x + (w // 2) > corx and y + (h // 2) > cory and x + (w // 2) < width-corx and  y + (h // 2) < height-cory:
            
    r1_mot, lr2_mot = 0, 0
    up1_mot, up2_mot = 0, 0
             
    if pimot.get_aposition() > 0: # if camera is tilted to the right - instruction for movement motor to correct heading (turning right)
        # first motor negative degrees
        lr1_mot = (10 * max_amplitude_motpiv * 3) * (-1)
        # second motor positive degrees
        lr2_mot = (10 * max_amplitude_motpiv * 3)
                
    elif pimot.get_aposition() < 0: # if camera is tilted to the left - instruction for movement motor to correct heading (turning left)
        # first motor positive degrees and second motor positive degrees
        # When camera turn x degrees motor movement must turn for 2x (experimental values -> is currently working on)

        lr1_mot = 10 * max_amplitude_motpiv * 3
        lr2_mot = 10 * max_amplitude_motpiv * 3
           
    ''' 
    #If unindexed that part make the robot react when target is up or down from the boundaries area by either reversing or advancing

    if camot.get_aposition() > 0: # camera look up
        up1_mot = -30
        up2_mot = -30
                
    elif camot.get_aposition() < 0: # camera look down
        up1_mot = 30
        up2_mot = 30
    '''
             
    print('// AllRobot Alignment To Target')

    '''
    # Optional additional informations

    print(pimot.get_aposition(), ' = pos. abs. deg. motor C')
    print(camot.get_aposition(), ' = pos. abs. deg. motor D')
    print(max_amplitude_motcam_high,'//', max_amplitude_motcam_low, ' = cam slope (first = 0 -> h, second = 0 -> l')
    '''
            
    pimot.run_to_position(0)
    max_amplitude_motpiv = 0
            
    if lr1_mot != 0 or lr2_mot != 0:    
        pair.run_for_degrees(lr1_mot, lr2_mot) #execute turn
                
    if up1_mot != 0 or up2_mot != 0:    
        pair.run_for_degrees(up1_mot, up2_mot) #execute retreat to take distance or advance to close the gap 
                
    pos = 0
```
Ce code permet de vérifier si le visage se trouve dans la zone centrale de l'image délimitée par la tolérance fixée par l'utilisateur. Si le visage s'y trouve alors on vérifie si le premier moteur de la tourelle est incliné à gauche ou à droite si il est incliné à gauche alors on fait passer des instructions pour les moteurs de mouvement qui feront tourner le rover a gauche ce qui l'alignera avec sa cible et inversement à droite. Et on refait venir le moteur à la position 0 pour que lui aussi soit réaligner avec le corps du rover et la cible.

```{code-block} python
---
linenos: true
---
elif y + (h // 2) < cory: # up
            
  if amplitude_motcam_high <= 25:
    camot.run_for_degrees(5)
    amplitude_motcam_high += 1
    amplitude_motcam_low -= 1
  elif amplitude_motcam_high >= 25:
    camot.run_to_position(0, 10)
    amplitude_motcam_high = 0
    amplitude_motcam_low = 0
    pair.run_for_degrees(-90, -90, 10)

  pos = 1
            
```
Ce code permet de réaligner la caméra par rapport au sujet si celui-ci se situe en haut de l'image. Le réalignement s'effectue avec le mouvement du deuxième moteur de la tourelle.
Des variables sont incrémenter et décrementer ces variables permettent de s'assurer que l'inclinaison de la camera ne dépasse 125 degrées en haut (amplitude_motcam_high) ou en bas (amplitude_motcam_low).

```{code-block} python
---
linenos: true
---
elif x + (w // 2) > width-corx: # right
            
  if max_amplitude_motpiv <= 6:
    pimot.run_for_degrees(10)
    max_amplitude_motpiv += 1
  elif max_amplitude_motpiv >= 6:
    pimot.run_to_position(0)
    max_amplitude_motpiv = 0
    pair.run_for_degrees(30, 30)

  pos = 3
```
Pareil pour cette partie, sauf qu'elle gère l'inclinaison et le suivi si la cible (visage) se trouve à droite de la caméra. Elle comporte aussi une sécurité pour éviter une trop grande amplitude de la caméra et bride le moteur a 60 degrées de liberté. 

Les éléments que j'ai trouvé compliqué ont été les suivants: installer toutes les dépendances et le faire fonctionner ensembles, devoir s'adapter aux contraintes du monde et adapter le code en fonction. 
Par exemple trouver les bonnes valeurs pour tourner les moteurs ou encore les valeurs de sécurités ont été assez amusante à trouver. Il y a aussi les valeurs dans la fonction qui détecte les visages oû il a été nécessaire d'expérimenter un peu avec plusieurs valeurs pour avoir des résultats satisfaisants.

Les technologies utilisées dans ce projet sont les suivantes: Raspberry Pi, OpenCV (haar_cascade) et les moteurs LEGO Technique. La technologie qui demande le plus d'explication est sans aucun doute OpenCV et ses dépendances. 

OpenCV est une librairie open source qui regroupe de nombreux algorithmes de Computer Vision et de modification et altération d'images. L'algorithme que j'utilise dans mon projet se nomme Haar Cascade, c'est un modèle pré-entrainé mis a disposition par OpenCV pour la reconnaissance de visage en temps réel. Ce modèle à été proposé en premier par Paul Viola et Michael Jones dans leur publication, "Rapid Object Detection using a Boosted Cascade of Simple Features" en 2001. Ce modèle est une approche utilisant du machine learning qui entraine une fonction dite de cascade à reconnaitre des visages. Cette approche utilise des images en noir en blanc c'est pourquoi dans notre code nous devons transformer les images BGR en échelle de gris pour que le modèle puisse fonctionner.

## Regard critique et améliorations

Dans l'ensemble je pense avoir plutôt répondu à mes objectifs initiaux. Le robot fait ce que lui demande et suit le visage d'une personne et corrige sa position par rapport a elle pour continuer à la suivre. Je pourrais cependant lever une critique sur l'ordinateur, en effet je n'avais pas réaliser que ce genre de processus consomme beaucoup de ressources et le RaspberryPi lui en a peu ce qui fait que parfois le framerate n'est pas très haut ce qui impère sur la qualité du suivi de visage, de plus je pense que bien que haar_cascade est plutot performant ces limitation lors de mauvais condition rendent la détection parfois difficile et inconsistente.

J'ai aussi sous-estime le fait d'apprendre un nouveau système d'exploitation pour faire ce projet, apprendre la logique de Linux m'a pris plus de temps que j'avais initialement anticipé. Et j'ai aussi rencontré de nombreux imprévus pour lier les système ensemble et le faire fonctionner en symbiose tous ensemble. Il y a aussi le fait que vu que je fait interface entre le monde et l'ordinateur il faut modifier certaines valeurs par rapport a l'expérience que on en a, savoir si il faut plus 20 ou 30 degré pour tourner par exemple est que la valeur négative va me permmettre de tourner ou fait il une valeur positive à la place etc ...

## Discussion

Je pense que j'aurais du mieux planifier mon temps par arpport au potentiels imprévues qui aurait pu arriver.  J'ai aussi sous-estimer l'aspect temporel de certains aspects de mon projet, la construction du rover par exemple et la conception. Mais malgré ces problème j'ai aussi trouvé que faire un projet de A a Z peut-etre vraiment sympa et relever les obstacles est vraiment tres interessant. Mon projet aurait pu aussi bénéficier de certains amélioration pour une version 2 par exemple le fait que le robot puisse bouger et suivre une personne en la suivant meme quand elle marche par exemple avec une batterie cela serait possible mais maitenant le rover est lié a une prise ce qui limite ses mouvements. 