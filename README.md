# ML_POINSON_ATTACK_LAB

## Prepare Data 

### (Option 1) Download pre-processed data ( `target` and `base` )
- dog and fish : https://drive.google.com/file/d/1VUPwV-w-gN9YCOeNjPHvdGUsX9YF-7d-/view?usp=sharing
- mouse and cat : https://drive.google.com/file/d/1k4Vn7RIasNT_qcpXGH18om-1iNG_oysa/view?usp=sharing
- dog and cat : https://drive.google.com/file/d/1raqv8F9-4IitiwL169t6z3aw0FwUBSkT/view?usp=share_link

Untar pre-processed data

- untar the folder `/XY` under `image_mlserver/simple_ml_server/server/poison_attack/Test_Data`

```bash
$ cd image_mlserver/simple_ml_server/server/poison_attack/Test_Data
$ tar -zxvf XY.tar.gz
```

### (Option 2) Download raw data
You can use another classes by using rawImages of them instead of using the pre-processed data

- lookup imagenet id
  - dog : n02084071
  - fish : n02512053
  - cat : n02121808
  - mouse : n02352591
  
- curl https://image-net.org/data/winter21_whole/`id`.tar > `class`.tar

```bash
$ curl https://image-net.org/data/winter21_whole/n02084071.tar > main_dog.tar
$ cd image_mlserver/simple_ml_server/server/poison_attack/Test_Data/rawImages/main_dog
$ tar -xvf main_dog.tar

$ curl https://image-net.org/data/winter21_whole/n02512053.tar > fish.tar
$ cd image_mlserver/simple_ml_server/server/poison_attack/Test_Data/rawImages/fish
$ tar -xvf fish.tar
```

## Specify what image classes to use.
The following example uses `dog_and_cat`. 
### set base_image.jpeg to cat and set target_image.jpeg to dog.
```bash
$ cd ML_POINSON_ATTACK_LAB/image_attacker/Attacker/baseImage
$ cp base_image_cat.jpeg base_image.jpeg

$ cd ~/ML_POINSON_ATTACK_LAB/image_attacker/Attacker/targetImage/
$ cp target_image_dog.jpeg target_image.jpeg
```

### image_mlserver/simple_ml_server/server/general.py
1) 
https://github.com/wonkr/ML_POINSON_ATTACK_LAB/blob/main/image_mlserver/simple_ml_server/server/general.py#L32-L34
Enable one of them
```python
#class_identifier = "dog_and_fish"
class_identifier = "dog_and_cat"
#class_identifier = "mouse_and_cat"
```

2)
https://github.com/wonkr/ML_POINSON_ATTACK_LAB/blob/main/image_mlserver/simple_ml_server/server/general.py#L55-L59

```python
class_dog_fish = {"dog":0., "fish":1.}
class_dog_cat = {"dog":0., "cat":1.}
class_mouse_cat = {"mouse":0., "cat":1.}

app.X_tr, app.Y_tr = append_train_data(app.sess, X_tr=app.X_tr, Y_tr=app.Y_tr, newInpImage=newInpImage, newInpClass=class_dog_cat[params['class']])
# app.X_tr, app.Y_tr = append_train_data(app.sess, X_tr=app.X_tr, Y_tr=app.Y_tr, newInpImage=newInpImage, newInpClass=class_dog_fish[params['class']])
# app.X_tr, app.Y_tr = append_train_data(app.sess, X_tr=app.X_tr, Y_tr=app.Y_tr, newInpImage=newInpImage, newInpClass=class_mouse_cat[params['class']])
```

## How to run Docker Containers
### requirements : docker
- install docker and docker-compose
```bash
sudo apt-get install docker
sudo apt-get install docker-compose
```
- please proceed docker postinstall steps
 https://docs.docker.com/engine/install/linux-postinstall/
 
### docker build and docker container up
```bash
$ cd ML_POINSON_ATTACK_LAB
$ docker-compose build .
$ docker-compose up
```

### how to stop docker containers
```bash
$ ctrl+c
$ docker-compose down
```


### how to get bash shell inside the container
1) Get Container ID that you want
```bash
$ docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS          PORTS                                       NAMES
c9ca64ef1bd7   image-mlserver     "/start.sh"              30 minutes ago   Up 30 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   mlserver-10.9.0.7
d17ccfca9bcb   seed-image-www     "/bin/sh -c 'service…"   30 minutes ago   Up 30 minutes                                               elgg-10.9.0.5
dd36c72f8a0d   image-attacker     "/start.sh"              30 minutes ago   Up 30 minutes                                               attacker-10.9.0.8
6054a952d0e5   seed-image-mysql   "docker-entrypoint.s…"   30 minutes ago   Up 30 minutes   3306/tcp, 33060/tcp                         mysql-10.9.0.6
```

2) run docker exec command to get bash shell
The following example shows how to get image-attacker container
```bash
$ docker exec -it dd36c72f8a0d /bin/bash
root@dd36c72f8a0d:/# 
```
## How to create poisoned image
1) Get attacker container shell

```bash
$ docker exec -it dd36c72f8a0d /bin/bash
root@dd36c72f8a0d:/# 
```
2) Run `generate_poison_image.py` script under `/Attacker` folder

```bash
root@dd36c72f8a0d:/# ls
Attacker  bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  poisonImg  proc  root  run  sbin  srv  start.sh  sys  tmp  usr  var
root@dd36c72f8a0d:/# cd Attacker/
root@dd36c72f8a0d:/Attacker# ./generate_poison_image.py
```

3) Once the script run, the poisoned Img will be created. And you can access to that image in the host pc as well as in the container.
```bash
~/ML_POINSON_ATTACK_LAB$ ls
docker-compose.yml  image_attacker  image_mlserver  image_mysql  image_www  mysql_data  poisonImg  README.md
parallels:~/ML_POINSON_ATTACK_LAB$ cd poisonImg/
parallels:~/ML_POINSON_ATTACK_LAB/poisonImg$ ls
2.83605.png
```

4) Need to change the owner of the poisoned image from ROOT to $USER in order to upload this image to the elgg web server
```bash
$ sudo chown $USER 2.83605.png 
```

### Poisoned Image example.
- The image shown as a cat image but it contains dog's feature.
<img width="461" alt="image" src="https://user-images.githubusercontent.com/19922651/236377873-63e273f2-eeee-45a1-8c2c-2419c2ff266e.png">


## Access to elgg web server
- Add hostname in /etc/hosts
```bash
$ sudo echo "10.9.0.5 www.seed-server.com" >> /etc/hosts
```
- elgg account (id : alice, pw: seedalice )

Now you can access to ML web server via url 'http://www.seed-server.com'
You can upload poisoned image at 'http://www.seed-server.com/file'
Once you upload the image, it will be crawled and used for train_data in the ML_SERVER by the crawler.py script running inside the ML_SERVER.

### Before training the poisoned data
<img width="395" alt="image" src="https://user-images.githubusercontent.com/19922651/236377795-8e6987d6-c534-45e8-8789-538962dcc366.png">

### After training the poisoned data
<img width="312" alt="image" src="https://user-images.githubusercontent.com/19922651/236377648-b5776143-486c-4112-a7d0-435c721185f4.png">


# Evaluation on different image other than (dog_and_fish)

- image data : imageNet (500 of images from each classes)
- machine learning model : inceptionv3 (2015)
- the number of poisoned image generated : 100


## 1) dog and cat
- base image : cat

<img width="401" alt="image" src="https://user-images.githubusercontent.com/19922651/236390928-37df1f5c-21c7-4f36-83d9-dfad7a32259d.png">

- target image : dog


- duration of time when generating poisoned images : ~2hours
	- depends on which base_image being used.
```
out of 100 poisons, 100 got correctly classified!
out of 100 targets, 100 got misclassified!
```
https://colab.research.google.com/drive/1xCFJ86tA8lo7_vThehxUmaT_Y4KisiIH?usp=sharing

<details>
<summary>result details</summary>
done loading data!
(100,)
******************0********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4467005
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.02643231 0.9735677 ]]
The poison is now classified correctly: [ True] class probs: [[0.00895907 0.991041  ]]
Dist in feat space: 2.8763123
******************1********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.41624364
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00275836 0.9972416 ]]
The poison is now classified correctly: [ True] class probs: [[0.00424331 0.9957567 ]]
Dist in feat space: 2.8914275
******************2********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4568528
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00163707 0.99836296]]
The poison is now classified correctly: [ True] class probs: [[0.00245338 0.9975466 ]]
Dist in feat space: 2.7779605
******************3********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.37055838
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00308023 0.99691975]]
The poison is now classified correctly: [ True] class probs: [[0.00312797 0.996872  ]]
Dist in feat space: 2.8571613
******************4********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.47715735
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.02186958 0.97813046]]
The poison is now classified correctly: [ True] class probs: [[0.00547746 0.9945226 ]]
Dist in feat space: 2.8784714
******************5********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49746192
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00814471 0.99185526]]
The poison is now classified correctly: [ True] class probs: [[0.0047219 0.9952781]]
Dist in feat space: 2.9224966
******************6********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5431472
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.01266819 0.9873318 ]]
The poison is now classified correctly: [ True] class probs: [[0.00737733 0.99262273]]
Dist in feat space: 2.8587651
******************7********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5076142
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00171306 0.9982869 ]]
The poison is now classified correctly: [ True] class probs: [[0.00269552 0.99730444]]
Dist in feat space: 2.9070218
******************8********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5431472
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00121521 0.99878484]]
The poison is now classified correctly: [ True] class probs: [[0.00141709 0.99858296]]
Dist in feat space: 2.7601862
******************9********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6345178
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.01378647 0.9862135 ]]
The poison is now classified correctly: [ True] class probs: [[0.00591892 0.9940811 ]]
Dist in feat space: 2.6342044
******************10********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5532995
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00215513 0.9978448 ]]
The poison is now classified correctly: [ True] class probs: [[0.0024649 0.9975351]]
Dist in feat space: 2.760352
******************11********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5888325
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[6.6078582e-04 9.9933916e-01]]
The poison is now classified correctly: [ True] class probs: [[7.011456e-04 9.992988e-01]]
Dist in feat space: 3.0854838
******************12********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.51269037
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00359658 0.99640346]]
The poison is now classified correctly: [ True] class probs: [[0.00190499 0.998095  ]]
Dist in feat space: 2.6393907
******************13********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.37563452
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00360383 0.99639624]]
The poison is now classified correctly: [ True] class probs: [[0.00250852 0.9974915 ]]
Dist in feat space: 2.8954177
******************14********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.3604061
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[8.834267e-04 9.991166e-01]]
The poison is now classified correctly: [ True] class probs: [[5.6769454e-04 9.9943227e-01]]
Dist in feat space: 3.4160075
******************15********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.56345177
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00105908 0.9989409 ]]
The poison is now classified correctly: [ True] class probs: [[0.00267524 0.9973247 ]]
Dist in feat space: 2.8726828
******************16********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.46700507
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00291305 0.99708694]]
The poison is now classified correctly: [ True] class probs: [[0.00174407 0.9982559 ]]
Dist in feat space: 2.9050255
******************17********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.55837566
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[1.03220365e-04 9.99896765e-01]]
The poison is now classified correctly: [ True] class probs: [[9.3715964e-05 9.9990630e-01]]
Dist in feat space: 2.9609962
******************18********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49238577
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.00985938 0.9901406 ]]
The poison is now classified correctly: [ True] class probs: [[0.00594824 0.99405175]]
Dist in feat space: 2.881316
******************19********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5482234
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.01080101 0.989199  ]]
The poison is now classified correctly: [ True] class probs: [[0.00562558 0.9943744 ]]
Dist in feat space: 2.7325385
******************20********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.52791876
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00558539 0.99441457]]
The poison is now classified correctly: [ True] class probs: [[0.00382506 0.99617493]]
Dist in feat space: 2.804499
******************21********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49238577
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.00420758 0.9957924 ]]
The poison is now classified correctly: [ True] class probs: [[0.00283065 0.9971693 ]]
Dist in feat space: 2.8458076
******************22********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5177665
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00294754 0.99705243]]
The poison is now classified correctly: [ True] class probs: [[0.00223958 0.9977604 ]]
Dist in feat space: 2.7673054
******************23********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.3857868
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.01066015 0.9893399 ]]
The poison is now classified correctly: [ True] class probs: [[0.00467728 0.99532276]]
Dist in feat space: 2.8846862
******************24********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6903553
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00154631 0.9984536 ]]
The poison is now classified correctly: [ True] class probs: [[0.00125638 0.9987436 ]]
Dist in feat space: 2.90597
******************25********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.39593908
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00651785 0.9934822 ]]
The poison is now classified correctly: [ True] class probs: [[0.00392734 0.99607265]]
Dist in feat space: 3.1100547
******************26********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.56345177
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[9.3865074e-04 9.9906141e-01]]
The poison is now classified correctly: [ True] class probs: [[0.0012579  0.99874216]]
Dist in feat space: 2.8753715
******************27********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.45177665
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00814133 0.99185866]]
The poison is now classified correctly: [ True] class probs: [[0.00606504 0.9939349 ]]
Dist in feat space: 2.7872388
******************28********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6294416
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.0016945  0.99830544]]
The poison is now classified correctly: [ True] class probs: [[0.00173054 0.99826944]]
Dist in feat space: 2.872014
******************29********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5177665
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00130647 0.9986935 ]]
The poison is now classified correctly: [ True] class probs: [[0.00138698 0.998613  ]]
Dist in feat space: 2.751678
******************30********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5482234
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.01183711 0.98816293]]
The poison is now classified correctly: [ True] class probs: [[0.0069106 0.9930894]]
Dist in feat space: 2.8847475
******************31********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.60913706
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[4.6224415e-04 9.9953783e-01]]
The poison is now classified correctly: [ True] class probs: [[8.212567e-04 9.991787e-01]]
Dist in feat space: 2.961033
******************32********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49746192
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.01143344 0.9885666 ]]
The poison is now classified correctly: [ True] class probs: [[0.00709406 0.992906  ]]
Dist in feat space: 3.0621905
******************33********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4720812
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.0081024 0.9918976]]
The poison is now classified correctly: [ True] class probs: [[0.00251328 0.9974867 ]]
Dist in feat space: 2.851767
******************34********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5076142
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00793086 0.9920691 ]]
The poison is now classified correctly: [ True] class probs: [[0.00448983 0.9955102 ]]
Dist in feat space: 2.8645806
******************35********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.67005074
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.0275095  0.97249055]]
The poison is now classified correctly: [ True] class probs: [[0.00480553 0.9951945 ]]
Dist in feat space: 2.8413806
******************36********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.3248731
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00262673 0.9973732 ]]
The poison is now classified correctly: [ True] class probs: [[0.00290916 0.9970908 ]]
Dist in feat space: 2.873189
******************37********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4720812
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.14053816 0.85946184]]
The poison is now classified correctly: [ True] class probs: [[0.01120279 0.9887971 ]]
Dist in feat space: 2.8992057
******************38********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.47715735
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[3.5777575e-04 9.9964225e-01]]
The poison is now classified correctly: [ True] class probs: [[0.00175975 0.99824023]]
Dist in feat space: 3.5839834
******************39********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49746192
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.01328416 0.98671585]]
The poison is now classified correctly: [ True] class probs: [[0.00405421 0.99594575]]
Dist in feat space: 2.8892996
******************40********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6497462
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00177573 0.9982243 ]]
The poison is now classified correctly: [ True] class probs: [[0.00131448 0.99868554]]
Dist in feat space: 2.9077003
******************41********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.40609136
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.0024542 0.9975458]]
The poison is now classified correctly: [ True] class probs: [[0.00251968 0.99748033]]
Dist in feat space: 3.0273674
******************42********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.42639595
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00314632 0.99685365]]
The poison is now classified correctly: [ True] class probs: [[0.00308952 0.9969105 ]]
Dist in feat space: 2.7539809
******************43********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.52284265
Final test accuracy = 94.9%
The target is now classified correctly: [False] class probs: [[0.00243334 0.9975667 ]]
The poison is now classified correctly: [ True] class probs: [[0.00235495 0.9976451 ]]
Dist in feat space: 2.8953528
******************44********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.52284265
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00483963 0.9951604 ]]
The poison is now classified correctly: [ True] class probs: [[0.00402733 0.9959727 ]]
Dist in feat space: 2.6966884
******************45********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5888325
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00217417 0.9978258 ]]
The poison is now classified correctly: [ True] class probs: [[0.00319495 0.9968051 ]]
Dist in feat space: 3.3073533
******************46********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5431472
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00364753 0.99635243]]
The poison is now classified correctly: [ True] class probs: [[0.00313172 0.9968683 ]]
Dist in feat space: 2.8465116
******************47********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5482234
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00191185 0.9980882 ]]
The poison is now classified correctly: [ True] class probs: [[0.00129207 0.9987079 ]]
Dist in feat space: 2.8773758
******************48********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5532995
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[9.2551758e-04 9.9907446e-01]]
The poison is now classified correctly: [ True] class probs: [[0.00108315 0.99891686]]
Dist in feat space: 3.2379763
******************49********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.48730963
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00174275 0.9982572 ]]
The poison is now classified correctly: [ True] class probs: [[0.00309616 0.99690384]]
Dist in feat space: 2.8016963
******************50********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5076142
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00104451 0.9989555 ]]
The poison is now classified correctly: [ True] class probs: [[5.174224e-04 9.994825e-01]]
Dist in feat space: 3.2033172
******************51********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5482234
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00177739 0.99822265]]
The poison is now classified correctly: [ True] class probs: [[0.00260734 0.99739265]]
Dist in feat space: 2.9155574
******************52********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5076142
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.02804329 0.9719567 ]]
The poison is now classified correctly: [ True] class probs: [[0.00719204 0.992808  ]]
Dist in feat space: 2.873533
******************53********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.41624364
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00549265 0.9945074 ]]
The poison is now classified correctly: [ True] class probs: [[0.00324114 0.9967589 ]]
Dist in feat space: 2.8888502
******************54********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5482234
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00624799 0.99375194]]
The poison is now classified correctly: [ True] class probs: [[0.00182418 0.99817586]]
Dist in feat space: 2.7738001
******************55********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4720812
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.0106479  0.98935217]]
The poison is now classified correctly: [ True] class probs: [[0.00270308 0.99729687]]
Dist in feat space: 2.8798754
******************56********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4822335
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00280147 0.9971986 ]]
The poison is now classified correctly: [ True] class probs: [[0.0040195 0.9959805]]
Dist in feat space: 2.9912806
******************57********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5329949
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.01597389 0.9840261 ]]
The poison is now classified correctly: [ True] class probs: [[0.00427482 0.99572515]]
Dist in feat space: 2.850621
******************58********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4720812
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00150445 0.9984956 ]]
The poison is now classified correctly: [ True] class probs: [[0.00167285 0.9983272 ]]
Dist in feat space: 2.789168
******************59********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.55837566
Final test accuracy = 94.9%
The target is now classified correctly: [False] class probs: [[0.01129048 0.9887095 ]]
The poison is now classified correctly: [ True] class probs: [[0.00498669 0.9950133 ]]
Dist in feat space: 2.853513
******************60********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.41624364
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.00670016 0.99329984]]
The poison is now classified correctly: [ True] class probs: [[0.00328134 0.9967186 ]]
Dist in feat space: 2.69318
******************61********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49746192
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00123263 0.9987674 ]]
The poison is now classified correctly: [ True] class probs: [[0.00261907 0.9973809 ]]
Dist in feat space: 2.9067793
******************62********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6395939
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00128216 0.9987179 ]]
The poison is now classified correctly: [ True] class probs: [[0.00154387 0.9984561 ]]
Dist in feat space: 3.4569068
******************63********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.46192893
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00251502 0.9974849 ]]
The poison is now classified correctly: [ True] class probs: [[0.00384791 0.9961521 ]]
Dist in feat space: 3.3797019
******************64********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.51269037
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00350007 0.9964999 ]]
The poison is now classified correctly: [ True] class probs: [[0.00260568 0.9973943 ]]
Dist in feat space: 2.9159567
******************65********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.48730963
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00530063 0.99469936]]
The poison is now classified correctly: [ True] class probs: [[0.00360598 0.996394  ]]
Dist in feat space: 2.7417665
******************66********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5989848
Final test accuracy = 94.9%
The target is now classified correctly: [False] class probs: [[0.00322408 0.9967759 ]]
The poison is now classified correctly: [ True] class probs: [[0.00319555 0.9968045 ]]
Dist in feat space: 2.8825164
******************67********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.51269037
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00246217 0.99753785]]
The poison is now classified correctly: [ True] class probs: [[0.00260414 0.9973959 ]]
Dist in feat space: 2.8656435
******************68********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5431472
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.01312816 0.98687184]]
The poison is now classified correctly: [ True] class probs: [[0.00589086 0.99410915]]
Dist in feat space: 2.8808386
******************69********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.53807104
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00148222 0.9985178 ]]
The poison is now classified correctly: [ True] class probs: [[0.00140881 0.9985911 ]]
Dist in feat space: 2.858272
******************70********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4822335
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[9.4088289e-04 9.9905914e-01]]
The poison is now classified correctly: [ True] class probs: [[0.00234128 0.9976587 ]]
Dist in feat space: 3.0784006
******************71********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.42639595
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.02700341 0.97299653]]
The poison is now classified correctly: [ True] class probs: [[0.00537162 0.99462837]]
Dist in feat space: 2.8321571
******************72********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5431472
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.01213901 0.987861  ]]
The poison is now classified correctly: [ True] class probs: [[0.00792653 0.9920735 ]]
Dist in feat space: 2.849793
******************73********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.41624364
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00400674 0.99599326]]
The poison is now classified correctly: [ True] class probs: [[0.00264435 0.9973557 ]]
Dist in feat space: 2.870025
******************74********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.40101522
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00497998 0.99502003]]
The poison is now classified correctly: [ True] class probs: [[0.00502935 0.9949706 ]]
Dist in feat space: 2.8818583
******************75********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.52791876
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00498378 0.9950163 ]]
The poison is now classified correctly: [ True] class probs: [[0.00208788 0.9979121 ]]
Dist in feat space: 2.7566652
******************76********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.52284265
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00340278 0.99659723]]
The poison is now classified correctly: [ True] class probs: [[0.00292424 0.9970758 ]]
Dist in feat space: 2.8682373
******************77********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4720812
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00155006 0.9984499 ]]
The poison is now classified correctly: [ True] class probs: [[0.00118941 0.99881065]]
Dist in feat space: 2.8883414
******************78********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5888325
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[2.4648511e-04 9.9975353e-01]]
The poison is now classified correctly: [ True] class probs: [[6.6019600e-04 9.9933976e-01]]
Dist in feat space: 2.9025211
******************79********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49238577
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00575529 0.99424475]]
The poison is now classified correctly: [ True] class probs: [[0.00330416 0.9966959 ]]
Dist in feat space: 2.8400774
******************80********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5076142
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[8.2226528e-04 9.9917775e-01]]
The poison is now classified correctly: [ True] class probs: [[8.7825116e-04 9.9912173e-01]]
Dist in feat space: 2.9837313
******************81********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.43654823
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[3.3349905e-04 9.9966645e-01]]
The poison is now classified correctly: [ True] class probs: [[4.2766056e-04 9.9957234e-01]]
Dist in feat space: 2.8883185
******************82********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5939086
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00391615 0.99608386]]
The poison is now classified correctly: [ True] class probs: [[0.00711858 0.9928814 ]]
Dist in feat space: 2.8104646
******************83********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.43654823
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00132785 0.9986721 ]]
The poison is now classified correctly: [ True] class probs: [[0.00305978 0.99694026]]
Dist in feat space: 2.8664718
******************84********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.40101522
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00223377 0.99776626]]
The poison is now classified correctly: [ True] class probs: [[0.00158154 0.99841845]]
Dist in feat space: 2.8762848
******************85********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.52791876
Final test accuracy = 97.5%
The target is now classified correctly: [False] class probs: [[0.01398796 0.98601204]]
The poison is now classified correctly: [ True] class probs: [[0.01068913 0.98931086]]
Dist in feat space: 2.7982361
******************86********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6294416
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.00923845 0.9907616 ]]
The poison is now classified correctly: [ True] class probs: [[0.00307063 0.99692935]]
Dist in feat space: 2.904368
******************87********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.46192893
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00189272 0.9981073 ]]
The poison is now classified correctly: [ True] class probs: [[0.00339105 0.996609  ]]
Dist in feat space: 2.9377825
******************88********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.37055838
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00632768 0.9936724 ]]
The poison is now classified correctly: [ True] class probs: [[0.00365421 0.9963458 ]]
Dist in feat space: 2.7377279
******************89********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.53807104
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[5.0549956e-05 9.9994946e-01]]
The poison is now classified correctly: [ True] class probs: [[6.333879e-05 9.999367e-01]]
Dist in feat space: 3.1622412
******************90********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.4314721
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.00322422 0.9967758 ]]
The poison is now classified correctly: [ True] class probs: [[0.00216953 0.99783045]]
Dist in feat space: 3.3452578
******************91********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.70558375
Final test accuracy = 97.0%
The target is now classified correctly: [False] class probs: [[0.0030377  0.99696225]]
The poison is now classified correctly: [ True] class probs: [[0.00436014 0.9956398 ]]
Dist in feat space: 2.8754156
******************92********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.42639595
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.00276935 0.9972307 ]]
The poison is now classified correctly: [ True] class probs: [[0.00242175 0.9975783 ]]
Dist in feat space: 2.912099
******************93********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5076142
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.00340275 0.99659723]]
The poison is now classified correctly: [ True] class probs: [[0.00350531 0.9964947 ]]
Dist in feat space: 2.7892742
******************94********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.56345177
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.00282577 0.99717426]]
The poison is now classified correctly: [ True] class probs: [[0.0011998  0.99880016]]
Dist in feat space: 2.856314
******************95********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.49238577
Final test accuracy = 95.4%
The target is now classified correctly: [False] class probs: [[0.00426096 0.9957391 ]]
The poison is now classified correctly: [ True] class probs: [[0.00293972 0.99706024]]
Dist in feat space: 2.764879
******************96********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.6294416
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[8.752646e-04 9.991247e-01]]
The poison is now classified correctly: [ True] class probs: [[6.2784296e-04 9.9937218e-01]]
Dist in feat space: 2.9161255
******************97********************
Y_target is: [[1. 0.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.61421317
Final test accuracy = 96.4%
The target is now classified correctly: [False] class probs: [[0.01399688 0.98600316]]
The poison is now classified correctly: [ True] class probs: [[0.00224558 0.9977544 ]]
Dist in feat space: 2.8266902
******************98********************
Y_target is: [[0. 1.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.5837563
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[0.9876737  0.01232627]]
The poison is now classified correctly: [ True] class probs: [[0.9980205  0.00197953]]
Dist in feat space: 2.8088589
******************99********************
Y_target is: [[0. 1.]]
********>>>>>> 0.4111675
cold start
********>>>>>> 0.680203
Final test accuracy = 95.9%
The target is now classified correctly: [False] class probs: [[9.9927133e-01 7.2868349e-04]]
The poison is now classified correctly: [ True] class probs: [[0.9972144  0.00278567]]
Dist in feat space: 3.0898132
##############################
out of 100 poisons, 100 got correctly classified!
out of 100 targets, 100 got misclassified!
<!-- summary 아래 한칸 공백 두어야함 -->

</details>

## 2) mouse and cat
- base image : cat

<img width="482" alt="image" src="https://user-images.githubusercontent.com/19922651/236390818-4306bb7d-e446-46d4-bc2b-96e4406b2c1e.png">

- target image : mouse

target sample
<img width="479" alt="image" src="https://user-images.githubusercontent.com/19922651/236391053-d7f59074-613f-4c92-93aa-421228a87f33.png">

- duration of time : 
```
```
https://colab.research.google.com/drive/10wnT0R-fNmGC_P0AB6ozKFtnPcJFtz4f?usp=sharing

	





# Reference
https://github.com/ashafahi/inceptionv3-transferLearn-poison
```latex
@ARTICLE{2018arXiv180400792S,
   author = {{Shafahi}, A. and {Ronny Huang}, W. and {Najibi}, M. and {Suciu}, O. and 
	{Studer}, C. and {Dumitras}, T. and {Goldstein}, T.},
    title = "{Poison Frogs! Targeted Clean-Label Poisoning Attacks on Neural Networks}",
  journal = {ArXiv e-prints},
archivePrefix = "arXiv",
   eprint = {1804.00792},
 primaryClass = "cs.LG",
 keywords = {Computer Science - Learning, Computer Science - Cryptography and Security, Computer Science - Computer Vision and Pattern Recognition, Statistics - Machine Learning},
     year = 2018,
    month = apr,
   adsurl = {http://adsabs.harvard.edu/abs/2018arXiv180400792S},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```


