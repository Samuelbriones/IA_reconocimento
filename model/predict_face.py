from keras.models import load_model
from mtcnn.mtcnn import MTCNN
import cv2
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), 'vgg16_faces.keras')
model = load_model(model_path)
detector = MTCNN()  

def crop_and_resize(image, target_w=224, target_h=224):
    if image.ndim == 2:
        img_h, img_w = image.shape             
    elif image.ndim == 3:
        img_h, img_w, channels = image.shape   
    target_aspect_ratio = target_w/target_h
    input_aspect_ratio = img_w/img_h

    if input_aspect_ratio > target_aspect_ratio:
        resize_w = int(input_aspect_ratio*target_h)
        resize_h = target_h
        img = cv2.resize(image, (resize_w , resize_h))
        crop_left = int((resize_w - target_w)/2)  
        crop_right = crop_left + target_w
        new_img = img[:, crop_left:crop_right]
    if input_aspect_ratio < target_aspect_ratio:
        resize_w = target_w
        resize_h = int(target_w/input_aspect_ratio)
        img = cv2.resize(image, (resize_w , resize_h))
        crop_top = int((resize_h - target_h)/4)  
        crop_bottom = crop_top + target_h
        new_img = img[crop_top:crop_bottom, :]
    if input_aspect_ratio == target_aspect_ratio:
        new_img = cv2.resize(image, (target_w, target_h))

    return new_img

y_label_dict = {0: 'Corazón', 1: 'Oblongo', 2: 'Ovalado', 3: 'Redondo', 4: 'Cuadrado'}

def extract_face(img, target_size=(224,224)):
    results = detector.detect_faces(img)
    if len(results) != 1:
        new_img = crop_and_resize(img, target_size[0], target_size[1])
        return new_img, False
    else:
        x1, y1, width, height = results[0]['box']
        x2, y2 = x1+width, y1+height
        face = img[y1:y2, x1:x2]  

        adj_h = 10
        
        if y1-adj_h <10:
            new_y1=0
        else:
            new_y1 = y1-adj_h

        if y1+height+adj_h < img.shape[0]:
            new_y2 = y1+height+adj_h
        else:
            new_y2 = img.shape[0]
        new_height = new_y2 - new_y1

        adj_w = int((new_height-width)/2)    

        if x1-adj_w < 0:
            new_x1=0
        else:
            new_x1 = x1-adj_w
            
        if x2+adj_w > img.shape[1]:
            new_x2 = img.shape[1]
        else:
            new_x2 = x2+adj_w
        new_face = img[new_y1:new_y2, new_x1:new_x2] 

    sqr_img = cv2.resize(new_face, target_size)   
    return sqr_img, True

def predict_face_shape(img_array):
    try:
        face_img, cond = extract_face(img_array) 
        if not cond:
          print("No hay rostros en la imagén, o hay más de un rostro")
          return face_img, None, None
      
        new_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)        
        test_img = np.array(new_img, dtype=float)
        test_img = test_img/255
        test_img = np.array(test_img).reshape(1, 224, 224, 3)  
        pred = model.predict(test_img)        
        label = np.argmax(pred,axis=1)
        shape = y_label_dict[label[0]]
        print(f'Tu tipo de rostro es {shape}')
        pred = np.max(pred)
        print(f'Probabilidad: {np.around(pred*100,2)}')
        return face_img, shape, pred * 100
    except Exception as e:
        print(f'Ocurrio un error: {e}')
        return None, None, None