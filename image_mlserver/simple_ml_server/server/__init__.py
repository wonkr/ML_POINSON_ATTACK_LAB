from flask import Flask, send_from_directory
import numpy as np
from .poison_attack.util_one_shot_kill_attack_modified import train_last_layer_of_inception, test
import imageio

def create_app(test_config=None):
      app = Flask(__name__, instance_relative_config=True)

      # # Load the configuration 
      # if test_config is None:
      #     app.config.from_object(Config)
      # else:
      #     app.config.from_mapping(test_config)

      @app.route('/')
      @app.route('/index.html')
      def send_index():
            return send_from_directory('static', 'index.html')

      #load the data from file
      directorySaving = 'server/poison_attack/Test_Data/XY/'
      all_datas = ['X_tr_feats', 'X_tst_feats', 'X_tr_inp', 'X_tst_inp', 'Y_tr', 'Y_tst']
      app.X_tr = np.load(directorySaving+all_datas[0]+'.npy')
      app.X_test = np.load(directorySaving+all_datas[1]+'.npy')
      app.Y_tr = np.load(directorySaving+all_datas[4]+'.npy')
      app.Y_test = np.load(directorySaving+all_datas[5]+'.npy')

      print('done loading data!')

      
      app.sess = train_last_layer_of_inception( X_tr=app.X_tr,
                                                Y_tr=app.Y_tr,
                                                Y_validation=app.Y_test,
                                                X_validation=app.X_test)

      # Load the blockchain Blueprint
      from . import general 
      app.register_blueprint(general.bp)

      return app
