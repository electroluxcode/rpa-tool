

# data =  [{
#   "data":"xiaoming"
# },{
#   "data":"xiaoming2"
# }
# ]

# for i in data:
#     print(i["data"])

import json 
   
# Opening JSON file 
f = open('data.json', encoding='UTF-8') 
   
# returns JSON object as  
# a dictionary 
allData = json.load(f) 
   
# Iterating through the json 
# list 
for i in allData['data']: 
    print(i) 

print((allData['data'][0]))
