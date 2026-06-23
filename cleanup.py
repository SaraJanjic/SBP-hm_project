from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["HM_DB"]
customers = db["customers"]
articles = db["articles"]
transactions = db["transactions_train"]

result = db.customers.update_many(
    {"fashion_news_frequency": "None"},
    {"$set": {"fashion_news_frequency": "NONE"}}
)

print("Izmenjeno:", result.modified_count)

#provera da na pocetku nisu postojali indeksi, da bismo mogli da merimo vreme izvrsavanja upita sa i bez indeksa
print(list(transactions.list_indexes()))
print(list(customers.list_indexes()))
print(list(articles.list_indexes()))

print(customers.count_documents({"age": None}))
print(articles.count_documents({"product_type_name": None}))
print(customers.distinct("fashion_news_frequency"))

print(customers.distinct("fashion_news_frequency"))
print(customers.distinct("club_member_status"))
print(articles.count_documents({"colour_group_name": None}))
print(articles.count_documents({"department_name": None}))
print(transactions.count_documents({"price": None}))