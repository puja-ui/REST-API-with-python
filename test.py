import requests

BASE = "http://127.0.0.1:5000/"




response = requests.get(BASE + "job/0")
print(response.json())
input()

data = [{"job_title":"and dev", "company":"freedae", "location": "us", "rating": 9, "job_description":"bla bla123", "emstatus":"helloworld"}]

for i in range(len(data)):
    response = requests.put(BASE + "job/" + str(i), data[i])
    print(response.json())
input()
response = requests.patch(BASE + "job/0",{"rating":10})
print(response.json())
input()

response = requests.delete(BASE + "job/0")
print(response)