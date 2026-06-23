from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["HM_DB"]

print("Povezana baza:", db.name)

print(client.list_database_names())

print("Articles:", db["articles"].count_documents({}))
print("Customers:", db["customers"].count_documents({}))
#za  transactions_train kolekciju sam obrisala jer dugo traje, ali proverila sam okej je