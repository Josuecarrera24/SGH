from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas
app.config['MONGO_URI'] = 'mongodb+srv://facha1999:Carreraj22$@cluster0.gvzqbpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)


# Ruta para obtener todos los hoteles
@app.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = mongo.db.hotels.find()
    output = []
    for hotel in hotels:
        hotel_data = {'id': str(hotel['_id']), 'name': hotel['name'], 'address': hotel['address']}
        output.append(hotel_data)
    return jsonify({'hotels': output})


# Ruta para agregar un nuevo hotel
@app.route('/hotels', methods=['POST'])
def add_hotel():
    data = request.get_json()
    hotel = {'name': data['name'], 'address': data['address']}
    result = mongo.db.hotels.insert_one(hotel)
    return jsonify({'message': 'Hotel añadido exitosamente!', 'hotel_id': str(result.inserted_id)})


# Ruta para actualizar un hotel
@app.route('/hotels/<hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    data = request.get_json()
    result = mongo.db.hotels.update_one({'_id': ObjectId(hotel_id)}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'message': 'Hotel not found'})
    return jsonify({'message': 'Hotel actualizado exitosamente'})


# Ruta para eliminar un hotel
@app.route('/hotels/<hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    result = mongo.db.hotels.delete_one({'_id': ObjectId(hotel_id)})
    if result.deleted_count == 0:
        return jsonify({'message': 'Hotel not found'})
    return jsonify({'message': 'Hotel eliminado exitosamente'})

# Ruta para obtener todas las habitaciones
@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = mongo.db.rooms.find()
    output = []
    for room in rooms:
        room_data = {'id': str(room['_id']), 'hotel_id': room['hotel_id'], 'number': room['number'], 'price': room['price']}
        output.append(room_data)
    return jsonify({'rooms': output})


# Ruta para agregar una nueva habitación a un hotel
@app.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    room = {'hotel_id': data['hotel_id'], 'number': data['number'], 'price': data['price']}
    result = mongo.db.rooms.insert_one(room)
    return jsonify({'message': 'Habitacion añadida exitosamente!', 'room_id': str(result.inserted_id)})


# Ruta para actualizar una habitación
@app.route('/rooms/<room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    result = mongo.db.rooms.update_one({'_id': ObjectId(room_id)}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'message': 'Habitacion no encontrada'})
    return jsonify({'message': 'Habitacion actualizada exitosamente'})


@app.route('/rooms/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    result = mongo.db.rooms.delete_one({'_id': ObjectId(room_id)})
    if result.deleted_count == 0:
        return jsonify({'message': 'Habitacion no encontrada'})
    return jsonify({'message': 'Habitacion eliminada exitosamente'})

if __name__ == '__main__':
    app.run()