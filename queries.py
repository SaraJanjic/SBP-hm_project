from pymongo import MongoClient
import time
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["HM_DB"]

transactions = db["transactions_train"]
articles = db["articles"]
customers = db["customers"]

#fja koju cemo pozivati za izvrsavanje upita, da bismo mogli da merimo vreme izvrsavanja i da lepo ispisujemo rezultate
def run_query(name, collection, pipeline):
    print(f"\n{name}")
    print("-" * 50)

    start = time.time()
    #allowDiskUse=True je bitno za upite koji koriste $lookup, jer moze da se desi da se prekorači limit memorije i da baca gresku jer imamo veliku kolekciju
    result = list(collection.aggregate(pipeline, allowDiskUse=True)) 
    end = time.time()

    for r in result[:10]:
        pprint(r)

    print("Broj rezultata:", len(result))
    print("Vreme izvršavanja:", round(end - start, 4), "s")

    return result, round(end - start, 4)



# 1. Koje tipove proizvoda preferiraju različite starosne grupe kupaca?
pipeline_q2 = [
    {
        "$lookup": {
            "from": "customers",
            "localField": "customer_id",
            "foreignField": "customer_id",
            "as": "customer"
        }
    },
    {
        "$unwind": "$customer"
    },
    {
        "$lookup": {
            "from": "articles",
            "localField": "article_id",
            "foreignField": "article_id",
            "as": "article"
        }
    },
    {
        "$unwind": "$article"
    },
    {
        "$match": {
            "customer.age": {"$ne": None}
        }
    },
    {
        "$addFields": {
            "age_group": {
                "$switch": {
                    "branches": [
                        {"case": {"$lt": ["$customer.age", 20]}, "then": "0-19"},
                        {"case": {"$lt": ["$customer.age", 30]}, "then": "20-29"},
                        {"case": {"$lt": ["$customer.age", 40]}, "then": "30-39"},
                        {"case": {"$lt": ["$customer.age", 50]}, "then": "40-49"},
                        {"case": {"$lt": ["$customer.age", 60]}, "then": "50-59"}
                    ],
                    "default": "60+"
                }
            }
        }
    },
    {
        "$group": {
            "_id": {
                "age_group": "$age_group",
                "product_type": "$article.product_type_name"
            },
            "broj_kupovina": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "_id.age_group": 1,
            "broj_kupovina": -1
        }
    },
    {
        "$group": {
            "_id": "$_id.age_group",
            "najpopularniji_tipovi": {
                "$push": {
                    "product_type": "$_id.product_type",
                    "broj_kupovina": "$broj_kupovina"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "starosna_grupa": "$_id",
            "najpopularniji_tipovi": {"$slice": ["$najpopularniji_tipovi", 5]}
        }
    },
    {
        "$sort": {
            "starosna_grupa": 1
        }
    }
]

run_query(
    "Q2 - Koje tipove proizvoda preferiraju različite starosne grupe kupaca?",
    transactions,
    pipeline_q2
)