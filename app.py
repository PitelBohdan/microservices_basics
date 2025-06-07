import requests

response = requests.post(
    "http://127.0.0.1:5000/post-msg",
    json={"msg": "Це моє повідомлення"}
)
print(response.text)
