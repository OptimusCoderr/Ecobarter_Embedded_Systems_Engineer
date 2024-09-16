import cv2
import numpy as np
import tensorflow as tf

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Load the labels
with open("labels_tflite.txt", "r") as file:
    class_names = file.readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

# Set camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    if not ret:
        print("Failed to grab image")
        break

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and normalize it
    image = cv2.resize(image, (224, 224))  # Resize directly to model input size
    image = np.asarray(image, dtype=np.float32)
    image = (image / 127.5) - 1
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Set the tensor to point to the input data
    input_details = interpreter.get_input_details()[0]
    interpreter.set_tensor(input_details['index'], image)

    # Run the model
    interpreter.invoke()

    # Get the output tensor
    output_details = interpreter.get_output_details()[0]
    prediction = interpreter.get_tensor(output_details['index'])[0]
    
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[index]

    # Print prediction and confidence score
    print(f"Class: {class_name}, Confidence Score: {confidence_score:.2%}")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()

