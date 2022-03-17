import subprocess
from django.shortcuts import render, redirect
from MLApp.models import *
from .forms import ImageForm, MLForm
import os
from tensorflow import keras
import sys
#here we can find all the required informations in order to build to ML model
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import  Dense, Conv2D, MaxPool2D , Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
# from tensorflow.python.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
from pymongo import MongoClient
import shutil 
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import tensorflowjs as tfjs
from tensorflow import keras
from tensorflow.python.keras import layers
from tensorflow.python.keras.models import Sequential
import boto3
from botocore.exceptions import NoCredentialsError

import random
import string
def getPassword(length):
    """Générer une chaîne aléatoire de longueur fixe"""
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))
    
print ("La chaine aleatoire est :", getPassword(8) )


#j'ai des problèmes dans les importations de mon modèle car j'ai en fait fait le gros imbécile en mélangeant 2 librairies utilisées afin de créer des modèles de ML => Je vais simplifier mon modèle et ça me permettra de correctement importé ce putain de truc, je vais tout faire en utilisant 
#installation de la database nosql afin d'avoir les images là-bas afin d'entrainer le modèle de ML, ces DB seront en permanence vidées après chaque entrainement d'algorithme ML, la database Django sera elle aussi vidée.


def home(request):
    if 'user_id' in request.session:
        print('je suis au bon endroit')
           ## la partie pour la création de nos algorithmes par rapport à l'utilisateur qui le fait, sauf que je dois mettre un champ en hidden field parce que les gens ne doivent pas pouvoir le voir
        if request.method == "POST" and 'ml_name_train' in request.POST:
            ml_name = request.POST.get("ml_name_train", "")  
            ##sur base de ça je dois filter la database afin de prendre uniquement les photos liées au nom du modèle de ML   
            model_involved = MLalgorithm.objects.get(name = ml_name)
            model_labbelized_images = Labellized_Images.objects.filter(ml_name = model_involved)
            for i in model_labbelized_images:
                print(i.label)
            password_1 = getPassword(8)
            list_label = image_machine_learning_model(model_labbelized_images,request.session['user_id'], password_1)  
            form_Image=ImageForm()
            form_ML = MLForm() 
            user_connected = User.objects.get(id=request.session['user_id'])
            Ml_list = MLalgorithm.objects.filter(user = user_connected)
            password = '{}_{}'.format(request.session['user_id'], password_1)
            return render(request, "MLApp/home.html",  {"form_Image":form_Image, "form_ML":form_ML, "ml_names":Ml_list, "password":password, "list_label":list_label}) 
        ## la partie pour la création des images basées sur l'algorithme que l'on choisit  
        
        if request.method == "POST" and 'label' in request.POST:
           
            label = request.POST.get("label", "")
            print(label)
            images = request.FILES.getlist('images')
            print(images)
            ml_name_1 = request.POST.get("ml_name", "")
            ml_name = MLalgorithm.objects.get(name = ml_name_1)
            print(ml_name)
            for image in images:
                photo = Labellized_Images.objects.create(image=image,label=label, ml_name = ml_name)
                photo.save()
            label2 = request.POST.get("label2", "")
            images2 = request.FILES.getlist('images2')
            for image in images2:
                print(image)
                print('image printed ')
                photo = Labellized_Images.objects.create(image=image,label=label2, ml_name = ml_name)
                photo.save()    
            form_Image=ImageForm()
            form_ML = MLForm()
            user_connected = User.objects.get(id=request.session['user_id'])    
            Ml_list = MLalgorithm.objects.filter(user = user_connected)
            return render(request, "MLApp/home.html", {"form_Image":form_Image, "form_ML":form_ML, "ml_names":Ml_list})

        if request.method == "POST":
            print('je rentre pas du tout la ou il faut')
            form_ML=MLForm(data=request.POST,files=request.FILES)
            if form_ML.is_valid():
                form_ML.save()
                form_Image=ImageForm()
                form_ML = MLForm()
                user_connected = User.objects.get(id=request.session['user_id'])
                Ml_list = MLalgorithm.objects.filter(user = user_connected)
                return render(request,"MLApp/home.html",  {"form_Image":form_Image, "form_ML":form_ML,"ml_names":Ml_list } )
       
    # if request.method == "POST":
    #     form_Image=ImageForm(data=request.POST,files=request.FILES)
    #     if form_Image.is_valid():
    #         form_Image.save()
    #         form_Image=ImageForm()
    #         form_ML = MLForm()
    #         return render(request,"MLApp/home.html", {"form_Image":form_Image, "form_ML":form_ML})     
        else:
            form_Image=ImageForm()
            form_ML = MLForm()
            ## je dois dabord retrieve le user et puis seulement je serai capable d'aller chercher les algorithmes qui lui appartiennent 
            user_connected = User.objects.get(id=request.session['user_id'])
            Ml_list = MLalgorithm.objects.filter(user = user_connected)
            return render(request,"MLApp/home.html", {"form_Image":form_Image, "form_ML":form_ML, "ml_names":Ml_list})
    else:
         return redirect(login) 


def signup(request):
        if 'user_id' in request.session:
            return redirect(home)
        else:
            if 'email' in request.GET:
                errors = []
                if len(User.objects.filter(email=request.GET['email'])) == 0:
                    if request.GET['password'] == request.GET['confirmPassword']:
                        user = User(firstname=request.GET['firstname'],
                                    lastname = request.GET['lastname'],
                                    email = request.GET['email'],
                                    phone = request.GET['phone'],
                                    password=request.GET['password'])
                        user.save()
                        return redirect(login)
                    else:
                        errors.append('Password and password confirmation does not match!')
                        return render(request, 'MLApp/signup.html', {'errors': errors})
                else:
                    errors.append('Email adress already used')
                    return render(request, 'MLApp/signup.html', {'errors': errors})
            else:
                return render(request, 'MLApp/signup.html')    

def login(request):
    if 'user_id' in request.session:
        return redirect(home)
    else:    
        errors = []
        if 'email' in request.GET:
                if len(User.objects.all().filter(email=request.GET['email'], password=request.GET['password'])) == 1:
                    user = User.objects.get(email=request.GET['email'])
                    #this line is to keep the user data in session cookies, dont forget to allow the cookies in the settings
                    request.session['user_id'] = user.id
                    return redirect(home)
                elif len(User.objects.all().filter(email=request.GET['email'])) == 0:
                    errors.append('Email not found')
                    return render(request, 'MLApp/login.html', {'errors': errors})
                else:
                    errors.append('Password not correct')
                    return render(request, 'MLApp/login.html', {'errors': errors})
        else:
            return render(request, 'MLApp/login.html', {'errors': errors})            





def image_machine_learning_model(labellized_data, session, password):
    print('je rentre correctement dans la fonction')
    
    ## c'est ici que ça va être chaud parce que je dois aussi jouer avec la structure de mes fichiers, je dois avoir 2 fichiers CSV 
    #la première chose que je dois faire c'est load les pictures en fonction de leurs labels 
    list_label_with_duplicate = []
    #petite list compréhension avec lambda function pour éviter les doublons et ça sera bcp plus clean
    for i in labellized_data: 
        list_label_with_duplicate.append(i.label)
    #j'ai ici de manière absolument correcte une liste avec les 2 différents labels     
    list_label = list(dict.fromkeys(list_label_with_duplicate))
    print(list_label)
    #va falloir 
    #j'ai pas l'impression que c'est quelque chose que je peux faire, je vais devoir ruser et faire cela autrement. Soous quelle forme est ce que je veux mes datas
    list_label_category_1 = [image for image in labellized_data if image.label == list_label[0]]
    print(list_label_category_1)
    list_label_category_2 = [image for image in labellized_data if image.label == list_label[1]]
    counter = 0
    for i in (list_label):
        directory = "{}".format(list_label[counter])
        # Parent Directory path
        parent_dir = "media\ML_models"
        # Path
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
        counter +=1
   
    for image in list_label_category_1:
        print('ok')
        shutil.copy("media/{}".format(str(image.image)), "media/Ml_models/{}".format(list_label[0]))

    for image in list_label_category_2:
        print('ok2')
        shutil.copy("media/{}".format(str(image.image)), 'media/Ml_models/{}'.format(list_label[1]))

    import pathlib
    data_dir = "media/Ml_models/"
    data_dir = pathlib.Path(data_dir)

    batch_size = 32
    img_height = 180
    img_width = 180

    train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.3,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    class_names = train_ds.class_names
    print(class_names)

    for image_batch, labels_batch in train_ds:
        print(image_batch.shape)
        print(labels_batch.shape)
        break

    #those parameters are related to performance, in order to avoid some bottleneck
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)    

    #ici on s'occupe de normaliser les données afin que l'algo ai toujours a dealer avec les mêmes formats d'images
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))
    first_image = image_batch[0]
    print(np.min(first_image), np.max(first_image))

    num_classes = len(class_names)

    #ici je vais devoir faire rentrer du Machine Learning et du data augmentation mais je vais y arriver ça va être kool
    model = Sequential([
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

    epochs=10
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
    )

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    # plt.figure(figsize=(8, 8))
    # plt.subplot(1, 2, 1)
    # plt.plot(epochs_range, acc, label='Training Accuracy')
    # plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    # plt.legend(loc='lower right')
    # plt.title('Training and Validation Accuracy')

    # plt.subplot(1, 2, 2)
    # plt.plot(epochs_range, loss, label='Training Loss')
    # plt.plot(epochs_range, val_loss, label='Validation Loss')
    # plt.legend(loc='upper right')
    # plt.title('Training and Validation Loss')
    # plt.show()

    #mes photos sont effacées du fichier afin qu'il n'y a pas de problème avec cela, mais je ne pense pas que ça soit très sécurisé de faire ça mais on verra bien ce qu'il se passe dans la console haha
    dir_path_1 = "media/Ml_models/{}".format(list_label[0])
    try:
        shutil.rmtree(dir_path_1)
    except OSError as e:
        print("Error: %s : %s" % (dir_path_1, e.strerror))

    dir_path_2= "media/Ml_models/{}".format(list_label[1])
    try:
        shutil.rmtree(dir_path_2)
    except OSError as e:
        print("Error: %s : %s" % (dir_path_2, e.strerror))  
        
    #c'est parfait le modèle est sauvé, je pense par contre que je vais devoir utiliser une base de donnée externe afin de sauver le modèle parce que c'est impossible de faire rentrer cette merde dans une DB django   
    directory = "ML_algo"
    # Parent Directory path
    parent_dir = "media"
    # Path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    print("Directory '% s' created" % directory)
    model.save('media/Ml_algo/my_model/model.h5')
    subprocess.call('tensorflowjs_converter --input_format keras media/Ml_algo/my_model/model.h5 media/Ml_algo/my_model/converted_model/')

    ACCESS_KEY = 'AKIAZ7AJKNHRWXG6V2PJ'
    SECRET_KEY = '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'

    def uploadDirectory(path,bucketname):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        for root,dirs,files in os.walk(path):
            for file in files:
                s3.upload_file(os.path.join(root,file),bucketname, 'models/{}_{}_{}'.format(session, password, file))

    uploadDirectory('media\ML_algo\my_model\converted_model', 'capture-static')       
    print('le transfert a été fait') 

    dir_path_3 = "media/Ml_algo/"
    try:
        shutil.rmtree(dir_path_3)
    except OSError as e:
        print("Error: %s : %s" % (dir_path_3, e.strerror))

    return list_label

    # def upload_to_aws(local_file, bucket, s3_file):
    #     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
    #                     aws_secret_access_key=SECRET_KEY)
    #     try:
    #         s3.upload_file(local_file, bucket, s3_file)
    #         print("Upload Successful")
    #         return True
    #     except FileNotFoundError:
    #         print("The file was not found")
    #         return False
    #     except NoCredentialsError:
    #         print("Credentials not available")
    #         return False

    # upload_to_aws('MLApp\ML_algo\my_model\converted_model\model.json' , 'capture-static', 'models/model.json')


#ça ça a l'air pas mal pour permettre d'avoir une option de download de l'algorithme
# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404

# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404

# ca peut toujours être une idée mais peut-être pas aujourd'hui
# #Connection à la base de donnée, MONGOdb NoSQL que je vais populer en fonction de mes datas et qui me servira pour le modèle de machine learning
#     uri = 'mongodb://uzjarzixxbx5m8xznvh3:5Bb8gkq7O800UlA05GX4@bqwwnmbw1haxvsa-mongodb.services.clever-cloud.com:27017/bqwwnmbw1haxvsa'
#     client = MongoClient(uri)
#     print(client.stats)
#     db = client['bqwwnmbw1haxvsa']
#     print(client.list_database_names())


