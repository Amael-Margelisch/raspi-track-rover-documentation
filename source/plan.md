(plan)=
```{figure} img/rover_track.jpg
---
width: 70%
---

```
# Plan 

:::{contents}
:::

## Présentation du projet

Ma principale motivation est d'explorer un nouveau système d'exploitation différent de Windows, en l'occurrence Linux. Je voulais aussi découvrir une technologie comme le Raspberry Pi et expérimenter avec des concepts de Machine Learning et de Computer Vision grâce à OpenCV. Je voulais également découvrir un peu la robotique et ce projet me permet de faire exactement cela. J'avais également envie de voir comment un ordinateur peut interagir avec le monde physique. En somme, ce projet me permet de m’essayer à la robotique et à d'autres technologies.

## Manuel / conseils d'utilisation

Pour entrer dans le Raspberry Pi il faut soit y connecter le cable HDMI et un clavier et une souris plus son cable d'alimentation ou alors soit s'y connecter par SSH (utilisation d'une application comme RealVNC Viewer). 

```{admonition} Informations de login
User : amael / Password : 123456 / Wifi : Youxipass / Password Wifi : nbkd5841
```

L'utilisation du rover est assez simple : le fichier permettant de lancer le programme est situé sur le Raspberry Pi et peut être exécuté soit via le terminal en utilisant la commande
```{code-block} python
---
linenos: false
---
 amael@raspberrypi:~ $ python /home/amael/Desktop/raspi_rover_main.py
```
soit en ouvrant un éditeur de code et en lançant le code à partir de là. Lors du lancement, l'utilisateur est invité à spécifier la tolérance, cette tolérance fait référence au nombre de pixel qui séparent les bord de l'image et la zone centrale qui est considérée comme le point d'équilibre que le rover voudra atteindre (Pour une explication plus imagée voir le schéma la tolérance y est représentée par les double flèches).

```{figure} img/rover_vision_schematic.png
---
width: 100%
---
Schéma de la vision du rover
```

Il est important de choisir une valeur de tolérance appropriée : une valeur trop grande rendrait la zone centrale de détection trop étroite, ce qui rendrait le comportement du rover instable car il ne parviendrait jamais à atteindre cette zone avec ses paramètres de correction (axe haut-bas 5°; axe droite-gauche 10°). Des valeur trop petites sont également à proscrire, en effet, le code prend la valeur centrale du rectangle de détection comme point de référence pour les corrections et si les valeurs sont trop petites alors le rover ne fera jamais rien car le visage sera à cheval et ne se fera donc pas detecter par l'algorithme et donc le point central n'existera pas et donc le rover ne pourra rien reconnaitre dans ces zones limites. Des valeurs de tolérance généralement recommandées pour cette caméra se situent entre 220 et 290 pixels.

Une fois le programme lancé, il suffit de se placer devant la caméra pour démarrer la reconnaissance et le suivi. Il est important de noter que vu que la reconnaissance tourne sur Raspberry Pi elle n'est pas très vive et donc il vaut mieux éviter les mouvements brusques. De plus, l'algorithme utilisé pour la reconnaissance est très sensible à l'éclairage ce qui parfois le rend peu précis et instable (il peut penser avoir reconnu un visage dans un mur ou dans un rideau par exemple). Une fois le programme lancé il suffit de se déplacer devant le rover pour que la caméra et le rover suivent.

:::{note}

Il est possible que la caméra effectue parfois un mouvement brusque vers la droite ou la gauche. Pour corriger ce problème, il suffit de se placer devant la caméra et elle se réalignera automatiquement par rapport au robot.
:::

## Explication du fonctionnement du code

Le fichier d'entrée de ce projet est raspi_rover_main.py, il se situe dans /home/amael/Desktop, il permet de lancer le projet.

Pour ce projet j'utilise OpenCV, qui est une librairie python qui regroupe les algorithmes utiles dans la Computer Vision,  j'utilise le Haar Cascade c'est un modèle pré-entrainé mis à disposition par OpenCV pour la detection de visage et le Raspberry Pi et son extension Build HAT qui permet une communication plus facile avec les moteurs LEGO Technique.

Explication de certaines parties du code.

```{code-block} python
---
#emphasize-lines: 3-4
linenos: false
---
import cv2 as cv
from picamera2 import Picamera2
from buildhat import Motor
from buildhat import MotorPair
```
Cette partie importe les différente librairies nécessaires au fonctionnement du code.

```{code-block} python
---
emphasize-lines: 3-4
linenos: false
---
while True:
  frame = picam2.capture_array()
  gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  face_rect = haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=4, minSize=(80,80))
```
Cette partie permet de prendre une image depuis la caméra du Raspberry Pi sous la forme d'un tableau numpy (numpy array) cette image est désormais stocké sous la variable ''frame'' puis pour que la detection de visage avec haar_cascade fonctionne il faut passer cette image en échelle de gris, c'est ce que cv.cvtColor(frame, cv.COLOR_BGR2GRAY) fait. On récupère ensuite l'image en échelle de gris dans la variable ''gray_frame'' et on la fait passer dans la fonction  haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=4, minSize=(80,80)) qui prend en paramètre une image, scale Factor - un facteur qui spécifie dans quelle mesure la taille de l’image est réduite à chaque échelle d’image, minNeighbors - détermine la quantité de voisins que chaque rectangle doit avoir pour le conserver, en bref, c'est un paramètre qui permet de régler la qualité de la détection de visage et minSize qui est un paramètre qui défini la taille minimum d'un visage pour qu'il soit détecté (il permet de limiter la détection erronée de visage dans des petits détails ce qui limite le parasitage des données mais ne l'élimine pas complètement, ici seul les visages détectés plus grand que 80 sur 80 sont validés), cette fonction retourne une liste avec les coordonnées du visage par rapport à l'image ainsi que sa hauteur et sa largeur, en bref, des rectangles.

```{code-block} python
---
linenos: false
---
for (x,y,w,h) in face_rect:
  # Trace moving entities
  cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
  cv.circle(frame, (x + (w // 2), y + (h // 2)), 1, (255, 255, 0), 4)
```
Cette partie trace le rectangle qui représente la détection du visage par l'algorithme, et le cercle qui représente le centre de ce rectangle et le point qui sera utilisé pour déterminer sa position et faire les décisions nécessaires pour le remettre au milieu de l'image.

```{code-block} python
---
linenos: false
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
        # When camera turn x degrees motor movement must turn for 3x (experimental values)

        lr1_mot = 10 * max_amplitude_motpiv * 3
        lr2_mot = 10 * max_amplitude_motpiv * 3
           
    ''' 
    #If unindexed that part make the robot react when target is up or down from the boundaries area by either reversing or advancing, but as the rover is bound by it's alimentation cable that functionality cannot be implemented as intended.

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
Ce code permet de vérifier si le visage se trouve dans la zone centrale de l'image délimitée par la tolérance fixée par l'utilisateur. Si le visage s'y trouve alors on vérifie si le premier moteur de la tourelle est incliné à gauche ou à droite si il est incliné à gauche alors on fait passer des instructions pour les moteurs de mouvement qui feront tourner le rover a gauche ce qui l'alignera avec sa cible et inversement à droite. Puis on refait venir le moteur à la position 0 pour que lui aussi soit réaligné avec le corps du rover et la cible.

```{code-block} python
---
linenos: false
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
Des variables sont incrémentées et décrémentées ces variables permettent de s'assurer que l'inclinaison de la camera ne dépasse pas 125 degrees en haut (amplitude_motcam_high) ou en bas (amplitude_motcam_low).

```{code-block} python
---
linenos: false
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
Pareil pour cette partie, sauf qu'elle gère l'inclinaison et le suivi si la cible (visage) se trouve à droite de la caméra. Elle comporte aussi une sécurité pour éviter une trop grande amplitude de la caméra et bride le moteur à 60 degrees de liberté. 

Les éléments que j'ai trouvé compliqué ont été les suivants: installer toutes les dépendances et le faire fonctionner ensembles, devoir s'adapter aux contraintes du monde et adapter le code en fonction. 
Par exemple trouver les bonnes valeurs pour tourner les moteurs ou encore les valeurs de sécurités ont été assez amusantes à trouver. Il y a aussi les valeurs dans la fonction qui détecte les visages oû il a été nécessaire d'expérimenter un peu avec plusieurs valeurs pour avoir des résultats satisfaisants.

Les technologies utilisées dans ce projet sont les suivantes: Raspberry Pi, OpenCV (haar_cascade) et les moteurs LEGO Technique. La technologie qui demande le plus d'explication est sans aucun doute OpenCV et ses dépendances. 

OpenCV est une librairie open source qui regroupe de nombreux algorithmes de Computer Vision et de modification et altération d'images. L'algorithme que j'utilise dans mon projet se nomme Haar Cascade, c'est un modèle pré-entrainé mis à disposition par OpenCV pour la reconnaissance de visage en temps réel. Ce modèle à été proposé en premier par Paul Viola et Michael Jones dans leur publication, "Rapid Object Detection using a Boosted Cascade of Simple Features" en 2001. Ce modèle est une approche utilisant du machine learning qui entraine une fonction dite de cascade à reconnaitre des visages. Cette approche utilise des images en noir en blanc c'est pourquoi dans notre code nous devons transformer les images BGR (contrairement à la majorité des logiciels OpenCV n'utilise pas le format RGB pour les images mais le BGR) en échelle de gris pour que le modèle puisse fonctionner.

## Regard critique et améliorations

Dans l'ensemble je pense avoir plutôt répondu à mes objectifs initiaux. Le robot fait ce que lui demande et suit le visage d'une personne et corrige sa position par rapport à elle pour continuer à la suivre. Je pourrais cependant lever une critique concernant le choix de l'ordinateur, en effet je n'avais pas réaliser que ce genre de processus consomme beaucoup de ressources et que le RaspberryPi lui en a peu ce qui fait que parfois le framerate n'est pas très haut ce qui entraine un préjudice sur la qualité du suivi des visages, de plus, je pense que bien que haar_cascade est performant, ses limitations lors de mauvaises conditions rendent la détection parfois difficile et inconsistante.

J'ai aussi sous-estimé le fait d'apprendre un nouveau système d'exploitation pour faire ce projet, apprendre la logique de Linux m'a pris plus de temps que j'avais initialement anticipé. Et j'ai aussi rencontré de nombreux imprévus pour lier les différents systèmes ensembles et les faire fonctionner tous ensembles. Et vu que le projet nécessite de faire fonctionner un ordinateur avec les contrainte du monde physique il était nécessaire de faire plusieurs pour trouver la solution la plus viable. Une autres amélioration que je pourrais proposer et dans la manière que j'ai désigné la vision du rover avec la vision actuelle les zones proches du bord de l'image sont plus sujettes à l'erreur que les autres et j'aurais pu penser à une autre façons de procéder qui limiterais ces problèmes dans ses zones limites (voir schéma).

```{figure} img/ame_rover_vision.png
---
width: 100%
---
Amélioration de la vision incluant une zone morte permettant une plus grande précision dans la détection aux zones limites
```

## Discussion

Je pense que j'aurais dû mieux planifier mon temps par rapport aux potentiels imprévus qui aurait pu arrivés. J'ai aussi sous-estimé l'aspect temporel de certains aspects de mon projet, la construction du rover par exemple ainsi que la conception. Mais malgré ces problème j'ai aussi trouvé que faire un projet de A à Z est vraiment une expérience intéressante et relever les obstacles qui se présentent est vraiment très intéressant. Sur l'aspect de potentielles améliorations que mon projet pourrait bénéficier pour une V2 il y a par exemple le fait que le robot puisse bouger et suivre une personne en la suivant même quand elle marche. le changement du moyen d'alimentation électrique du rover d'un cable lié à une prise à une batterie pourrait permettre au rover de s'affranchir de ses limitations dans ses mouvements.