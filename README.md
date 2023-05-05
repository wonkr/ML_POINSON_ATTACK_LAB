# ML_POINSON_ATTACK_LAB

## Download pre-processed data ( `target` and `base` )
- dog and fish : https://drive.google.com/file/d/1VUPwV-w-gN9YCOeNjPHvdGUsX9YF-7d-/view?usp=sharing
- cat and mouse : https://drive.google.com/file/d/1k4Vn7RIasNT_qcpXGH18om-1iNG_oysa/view?usp=sharing
- dog and cat : https://drive.google.com/file/d/1raqv8F9-4IitiwL169t6z3aw0FwUBSkT/view?usp=share_link

## Untar pre-processed data
- untar the folder `/XY` under `image_mlserver/simple_ml_server/server/poison_attack/Test_Data`

```bash
$ cd image_mlserver/simple_ml_server/server/poison_attack/Test_Data
$ tar -zxvf XY.tar.gz
```

## Download raw data
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

