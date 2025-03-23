import random
import keras
from keras.layers import Dense , Flatten , Dropout , BatchNormalization
import numpy as np
from keras.preprocessing import image
import time
class predictor():
    def __init__(self):

        #pre=keras.models.load_model("Model/mobilenetv2.keras")
        #print(pre.summary().encode("utf-8"))
        #input_img = keras.Input(shape=(224,224,3))

        #z1=pre(input_img)
        #z1=keras.Model(inputs=input_img, outputs=z1)
        #z2=Flatten(name='000')(z1(input_img)[0])
        #z3=BatchNormalization(name='00506')(z2)
        #d1=Dense(units = 64 , activation = 'relu' ,name='some_unique_name'  , kernel_regularizer=keras.regularizers.L2(),bias_regularizer=keras.regularizers.L2())(z3)
        #d2=Dense(units = 64 , activation = 'relu',name='2000'   , kernel_regularizer=keras.regularizers.L2(),bias_regularizer=keras.regularizers.L2())(d1)
        #dr1=Dropout(0.2,name='0006')(d2)
        #outputs=Dense(units = 3 , activation = 'softmax',name='0070',kernel_regularizer=keras.regularizers.L2(),bias_regularizer=keras.regularizers.L2())(dr1)
        #self.model=keras.Model(inputs=input_img, outputs=outputs)

        #self.model.compile(optimizer = keras.optimizers.Adam(learning_rate=1e-4) , loss  = keras.losses.CategoricalCrossentropy(from_logits=False,reduction="sum") , metrics = ["accuracy"])
        #self.model.summary()
        #self.model.load_weights("Model/best_model.keras",skip_mismatch=True)
        self.model=keras.models.load_model("Model/best_model.keras")
        

    def predict(self,data):
        print(data.shape)
        img=image.array_to_img(data)

        img = preprocess_image(img)

        # Make a prediction
        before=time.time()
        prediction = self.model.predict(img[:,:,:,:3],verbose=0)
        print("time for prediction="+str(time.time()-before))
        validity=False
        print(prediction)
        #print(prediction)
        # Decode the prediction
        # For example, if the self.model is a classification self.model with softmax activation, you can decode the prediction as follows:
        #predicted_class = prediction>0.5
        predicted_class = np.argmax(prediction)
        validity=prediction[0][predicted_class]
        
        if predicted_class==0:
            predicted_class="rosso" 
        elif predicted_class==1:
            predicted_class="verde"
        else:
            predicted_class="giallo"
        print(" Predicted class:", predicted_class)
        return predicted_class ,validity

    # Define a function to preprocess the image
def preprocess_image(img):
    img = image.smart_resize(img, (224, 224))
    img_array = image.img_to_array(img)/255
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

