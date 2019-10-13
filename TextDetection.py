import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Credentials.json"

full_text = ""
recieptInventory = []

class Reciept:
    #storeName = ""
    path = ""
    full_text = ""
    #experationDate = ""
    #datePrinted = ""
    def __init__(self):
        #self.storeName = ""
        self.path = ""
        self.full_text = ""
        #self.experationDate = ""
        #self.datePrinted = ""
        
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    full_text=  ""
    for text in texts:
        full_text += str('\n"{}"'.format(text.description)) + " "
        print('\n"{}"'.format(text.description))
        
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        
    print(full_text)
    return full_text
        
def fileConstruction():
       # The name of the image file to annotate
    file_name = input("Please input exact picture file path: ")
    
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
       # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    image = types.Image(content=content)
    
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    labelList = {""}

    for label in labels:
        labelList.add(label.description)
        
    isReciept = False
    
    
    for label in labelList:
        if (label == "Receipt" or label == "receipt"):
            isReciept = True
            full_text = detect_text(file_name)
            reciept = Reciept()
            #reciept.storeName = 
            reciept.path = file_name
            reciept.full_text = full_text
            recieptInventory.append(reciept)
            break
        
    user_input_name = input("Please Enter Store you want Reciept from: ")
    adjustedRecieptInventory = []
    storeName = ""    
    for reciept in recieptInventory:
        if(reciept.full_text.find(user_input_name) != -1):
            storeName = user_input_name
            
        if(storeName == user_input_name):
            adjustedRecieptInventory.append(reciept)

    if (isReciept == False):
        print("Could not find receipt. Please take another photo.")
        
    print("Current Inventory")
    for reciept in recieptInventory:
        print(reciept.path)
        
    print("Adjusted Inventory")
    for reciept in adjustedRecieptInventory:
       print(reciept.path)

def main():
    continuation = 'Y'
    while (continuation == 'Y'):
        continuation = input("Do you want to input a file to add to your reciept inventory? Please enter Y or N")
        if (continuation == 'Y'):
            fileConstruction()

    print("Thanks for using E-Stash")
       
    
if __name__=="__main__":
    main()



 