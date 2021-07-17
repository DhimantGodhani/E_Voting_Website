import pymongo


class db_connection:
    def connect_to_mongodb(self):
        connection_string = "mongodb+srv://dbUser:admin@cluster0.3zkhv.mongodb.net/db_college?retryWrites=true"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["db_e_voting"]
        return db
