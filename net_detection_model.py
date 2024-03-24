import cv2 as cv
import numpy as np
import matplotlib.pyplot as m
from tensorflow.keras import datasets, layers, models 
from sklearn.model_selection import train_test_split
import os

def load_and_preprocess_images(folder_path):
    # Initialize lists to store images and labels
    images = []
    labels = []

    # Load and preprocess images from the "Net" folder (class 0)
    net_folder = os.path.join(folder_path, "Net")
    for filename in os.listdir(net_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(net_folder, filename)
            image = cv.imread(image_path)
            preprocessed_image = cv.resize(image, (32, 32)) / 255.0
            images.append(preprocessed_image)
            labels.append(0)

    # Load and preprocess images from the "Background" folder (class 1)
    background_folder = os.path.join(folder_path, "Background")
    for filename in os.listdir(background_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(background_folder, filename)
            image = cv.imread(image_path)
            preprocessed_image = cv.resize(image, (32, 32)) / 255.0
            images.append(preprocessed_image)
            labels.append(1)

    # Convert lists to NumPy arrays
    images = np.array(images)
    labels = np.array(labels)

    # Split the data into training and testing sets
    training_images, testing_images, training_labels, testing_labels = train_test_split(
        images, labels, test_size=0.25, random_state=42, stratify=labels)

    return training_images, training_labels, testing_images, testing_labels


def train_model():
     #os.remove("/Users/macos/team25/net_detection_model.h5")
     training_images, training_labels, testing_images, testing_labels = load_and_preprocess_images("/Users/macos/team25/BasketBot_img")

     class_names = ['Net', 'BackGround']

     # for i in range(16):
     #      m.subplot(4,4,i+1)
     #      m.xticks([])
     #      m.yticks([])
     #      m.imshow(training_images[i], cmap = m.cm.binary)
     #      m.xlabel(class_names[training_labels[i]])

     # m.show()


     model = models.Sequential()
     model.add(layers.Conv2D(32, (3,3), activation= "relu", input_shape = (32,32,3)))
     model.add(layers.MaxPooling2D((2,2)))
     model.add(layers.Conv2D(64, (3,3), activation= "relu"))
     model.add(layers.MaxPooling2D((2,2)))
     model.add(layers.Conv2D(64, (3,3), activation= "relu"))
     model.add(layers.Flatten())
     model.add(layers.Dense(64, activation = "relu"))
     model.add(layers.Dense(64, activation = "softmax"))

     model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])

     model.fit(training_images, training_labels, epochs = 10, validation_data = (testing_images, testing_labels))

     loss, accuracy = model.evaluate(testing_images, testing_labels)
     print(f"Loss: {loss}, Accuracy: {accuracy}")

     model.save("/Users/macos/team25/net_detection_model.keras")



def net_prediction(img):
     model = models.load_model("/Users/macos/team25/net_detection_model.keras")
     #img = cv.imread("/Users/macos/team25/test_net2.png")
     #m.imshow(img, cmap = m.cm.binary)
     prediction = model.predict(np.array([img])/255)
     index = np.argmax(prediction)
     #print(f"Prediction: {class_names[index]}")
     return index


# def net_prediction(path):
#     class_names = ['Net', 'BackGround']

#     model = models.load_model("/Users/macos/team25/net_detection_model.keras")
#     img = cv.imread(path)
#     m.imshow(img, cmap = m.cm.binary)
#     prediction = model.predict(np.array([img])/255)
#     index = np.argmax(prediction)
#     print(f"Prediction: {class_names[index]}")
#     #return index


#train_model()
imgs =[]
pic1_net = "/Users/macos/team25/test_net.png"
imgs.append(cv.imread(pic1_net))
pic2_net = "/Users/macos/team25/test_net2.png"
imgs.append(cv.imread(pic2_net))
pic3_bg = "/Users/macos/team25/test_background.png"
imgs.append(cv.imread(pic3_bg))
pic4_bg = "/Users/macos/team25/test_background2.png"
imgs.append(cv.imread(pic4_bg))
i = []

i.append(net_prediction(imgs[0]))
i.append(net_prediction(imgs[1]))
i.append(net_prediction(imgs[2]))
i.append(net_prediction(imgs[3]))

class_names = ['Net', 'BackGround']

for id in range(4):
     m.subplot(2,2,id+1)
     m.xticks([])
     m.yticks([])
     m.imshow(imgs[id], cmap = m.cm.binary)
     m.xlabel(class_names[i[id]])

m.show()