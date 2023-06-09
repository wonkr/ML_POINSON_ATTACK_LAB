# CIS700 2023 - FINAL PROJECT 
## Contents
1. [ML_POISON_ATTACK_LAB](#ml_poison_attack_lab)
2. [Evaluation](#evaluation-on-different-image-other-than-dog_and_fish)

# ML_POISON_ATTACK_LAB

## Prepare Data 

### (Option 1) Download pre-processed data ( `target` and `base` )
- dog and fish : https://drive.google.com/file/d/1VUPwV-w-gN9YCOeNjPHvdGUsX9YF-7d-/view?usp=sharing
- <s>mouse and cat : https://drive.google.com/file/d/1k4Vn7RIasNT_qcpXGH18om-1iNG_oysa/view?usp=sharing</s> : accuracy low - futher investigation needed.
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

## summary
```
/bin/python3 /home/parallels/ML_POINSON_ATTACK_LAB/parse_eval_result.py

======= dog_and_cat_eval =======
# Final test accuracy
before poisoned :  97.0
after poisoned :  96.28999999999988
avg poison classified accuracy :  0.9768275262000004
avg target misclassified accuracy :  0.9732625192849003
======= mouse_and_cat_eval =======
# Final test accuracy
before poisoned :  99.0
after poisoned :  98.21
avg poison classified accuracy :  0.9867806270000002
avg target misclassified accuracy :  0.9634084135
======= dog_and_mouse_eval =======
# Final test accuracy
before poisoned :  99.5
after poisoned :  99.04
avg poison classified accuracy :  0.9781913498459999
avg target misclassified accuracy :  0.9542935317161799

```


## 1) dog and cat
- base image : cat

<img width="401" alt="image" src="https://user-images.githubusercontent.com/19922651/236390928-37df1f5c-21c7-4f36-83d9-dfad7a32259d.png">

- target image : dog
- total elapsed time on creating 100 poisoned images  : ~2h
	- depends on which base_image being used.
```
out of 100 poisons, 100 got correctly classified!
out of 100 targets, 100 got misclassified!
```
- colab link
https://colab.research.google.com/drive/1xCFJ86tA8lo7_vThehxUmaT_Y4KisiIH?usp=sharing

- detailed result
https://github.com/wonkr/ML_POINSON_ATTACK_LAB/blob/main/dog_and_cat_eval 

## 2) mouse and cat
- base image : cat

<img width="482" alt="image" src="https://user-images.githubusercontent.com/19922651/236390818-4306bb7d-e446-46d4-bc2b-96e4406b2c1e.png">

- target image : mouse

target sample
<img width="479" alt="image" src="https://user-images.githubusercontent.com/19922651/236391053-d7f59074-613f-4c92-93aa-421228a87f33.png">

- total elapsed time on creating 100 poisoned images  : ~6h
```
out of 100 poisons, 100 got correctly classified!
out of 100 targets, 100 got misclassified!
```
- colab link
https://colab.research.google.com/drive/10wnT0R-fNmGC_P0AB6ozKFtnPcJFtz4f?usp=sharing
- detailed result
https://github.com/wonkr/ML_POINSON_ATTACK_LAB/blob/main/mouse_and_cat_eval

## 3) dog and mouse
- base image : mouse
<img width="489" alt="image" src="https://user-images.githubusercontent.com/19922651/236456244-bfb5f441-f655-4611-9093-945e308fd832.png">

- target image : dog
- total elapsed time on creating 100 poisoned images  : ~5h
- colab link
https://colab.research.google.com/drive/1tQLNCcVdFs1laOTigg-gW2NzsBWiLm8z?usp=sharing
- detailed result 
https://github.com/wonkr/ML_POINSON_ATTACK_LAB/blob/main/dog_and_mouse_eval


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


