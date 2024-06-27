from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from PIL import Image
import io
import base64
import face_recognition
from pymongo import MongoClient

app = Flask(__name__)

# Set your MongoDB URI and database name
# app.config['MONGO_URI'] = 'mongodb+srv://nauman:fypcluster@cluster0.ascwljq.mongodb.net/people?retryWrites=true&w=majority'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/fyp'
mongo = PyMongo(app)

# Check if the MongoDB connection is successful
try:
    with app.app_context():
        mongo.db.list_collection_names()
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Directly initialize MongoClient
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    designation = request.form['designation']
    years_experience = request.form['years_experience']
    image = request.files['image']

    if image:
        image_data = image.read()

        # Open the image using PIL
        pil_image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Convert PIL image to numpy array
        image_array = face_recognition.api.load_image_file(
            io.BytesIO(image_data))

        # Detect face
        face_locations = face_recognition.face_locations(image_array)

        if face_locations:
            # Crop face
            top, right, bottom, left = face_locations[0]
            face_image = pil_image.crop((left, top, right, bottom))

            # Convert PIL image to base64-encoded string
            buffered = io.BytesIO()
            face_image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(
                buffered.getvalue()).decode('utf-8')

            # Create filename with additional information
            filename = f"{name}_{designation}_{years_experience}.jpg"

            # Store in MongoDB
            db.people.insert_one({
                'name': name,
                'designation': designation,
                'years_experience': years_experience,
                'image': f'data:image/jpeg;base64,{base64_image}',
                'filename': filename
            })

            return 'Upload successful!'
        else:
            return 'No face detected in the provided image.', 400
    else:
        return 'No image provided.', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
