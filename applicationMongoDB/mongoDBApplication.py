import datetime
import pprint

import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://noelneridev:mongoNoel01@cluster0.talkrdp.mongodb.net/?retryWrites=true&w=majority")

db = client.test
collection = db.test_collection
print(db.test_collection)

# definição de infor para compor o doc
post = {
    "cliente": "José Bétio",
    "Endereço": "Rua dos Bobos, número zero",
    "Profissao": ["pedreiro", "pintor", "eletricista"],
    "date": datetime.datetime.utcnow()
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

# print(db.posts.find_one())
pprint.pprint(db.posts.find_one())

#bulk inserts
new_posts = [{
            "cliente": "João Bétio",
            "Endereço": "Rua dos Bobos, número 01",
            "Profissao": ["pedreiro2", "pintor2", "eletricista2"],
            "date": datetime.datetime.utcnow()},
            {
            "cliente": "Arlindo Bétio",
            "Endereço": "Rua dos Bobos, número 02",
            "Profissao": ["pedreiro3", "pintor3", "eletricista3"],
            "date": datetime.datetime.utcnow()}]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

print("\nRecuperação final")
pprint.pprint(db.posts.find_one({"cliente": "João Bétio"}))

print("\n Documentos presentes na coleção posts")
for post in posts.find():
    pprint.pprint(post)
