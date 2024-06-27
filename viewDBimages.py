

from pymongo import MongoClient
from PIL import Image
from io import BytesIO
import base64

# Connect to MongoDB
# client = MongoClient("mongodb+srv://nauman:fypcluster@cluster0.ascwljq.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient("mongodb://localhost:27017/fyp")
db = client["fyp"]
collection = db["people"]

# Iterate through documents in the collection
for document in collection.find():
    # Retrieve the image data from the "image" field
    image_data = document["image"]

    # Extract the Base64 encoded part
    _, encoded_data = image_data.split(',', 1)

    # Decode the image data (assuming it's Base64 encoded)
    decoded_image_data = BytesIO(base64.b64decode(encoded_data))

    # Display or save the image
    image = Image.open(decoded_image_data)
    image.show()

# Close the MongoDB connection
client.close()
