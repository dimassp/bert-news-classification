from datetime import date
news_portal = [
    {"id": "detiknewsjabar","name": "Detik News Jabar"},
    {"id": "antaranewsjabar","name": "Antara News Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
]
total_rows = 0
if len(news_portal)%3 ==0:
    total_rows = int(len(news_portal)/ 3)
else:
    total_rows = int(len(news_portal) / 3) +1
print("total rows: {0}\ntotal portal: {1}".format(total_rows,len(news_portal)))

today = date.today()
print(f"Date: {type(str(today))}")