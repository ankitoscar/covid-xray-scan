from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient
from .forms import ImageForm

# Create your views here.
def index(request):
    context = {'patient': Patient}
    return render(request,'classify/index.html',context)


from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf 
import numpy as np 

IMG_HEIGHT, IMG_WIDTH = 224,224

global graph, model 

graph = tf.compat.v1.get_default_graph()

print("Keras model loading .........")
model = load_model('models/covid-19-xray-model.hdf5')
print("Model loaded !!")

class_dict = {
    'COVID-19':0,
    'Pneumonia':1,
    'Normal':2
}

class_names = list(class_dict.keys())

def prediction(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            filePathName = img_obj.scan.url
            filePathName = '.'+filePathName
            img = image.load_img(filePathName, target_size=(IMG_HEIGHT, IMG_WIDTH))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img / 255
            with graph.as_default():
                preds = model.predict(img)
            preds = preds.flatten()
            m = max(preds)
            for index,item in enumerate(preds):
                if item == m:
                    result = class_names[index]
            return render(request,'classify/index.html',{'form':form,'img_obj':img_obj,'result':result})
    else:
        form = ImageForm()
        return render(request,'classify/index.html',{'form':form})