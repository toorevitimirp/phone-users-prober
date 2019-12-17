import requests
resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('./test_gakki.jpeg','rb')})
print(resp.text)