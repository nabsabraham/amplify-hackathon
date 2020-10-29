import os
import pickle
import json
import joblib
import numpy as np
import torch
from azureml.core.model import Model
from torchvision import transforms
from PIL import Image 

transform = transforms.Compose([            
 transforms.Resize(256),                    
 transforms.CenterCrop(224),                
 transforms.ToTensor(),                     
 transforms.Normalize(                  
 mean=[0.485, 0.456, 0.406],                
 std=[0.229, 0.224, 0.225]                  
 )])


def preprocess_data(img):
    print(f' Image shape in preprocess data: {img.shape}')
    img = Image.fromarray(img, 'RGB')
    print(f' Image type: {type(img)}')
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    return batch_t

def init():
    global model
    # retrieve the path to the model file using the model name
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'alexnet_model.pkl')
    model = joblib.load(model_path)

def run(raw_data):

    try:
        print('in the try, received data')
        data = np.array(json.loads(raw_data)['data'])
        print('after the read')
        # make prediction
        print(f'Length of the data list: {len(list(data))}')
        img = preprocess_data(data)
        print('after the preprocess')
        y = model(img)
        print('after inference')
        #prob = F.softmax(y, dim=1)[0]
        #_, ind = torch.topk(y, 1) 
        return y.tolist()[0]
    
    except Exception as e:
        error = str(e)
        return error
