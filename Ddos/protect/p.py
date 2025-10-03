from flask import Flask, request, jsonify, abort  
from collections import defaultdict  
import time  

app = Flask(__name__)  

# Blacklisted IPs and request logs  
blacklist = set()  
request_log = defaultdict(list)  

# Rate limiting parameters  
RATE_LIMIT = 10         # Maximum 10 requests per 10 seconds  
BLOCK_DURATION = 60     # Block duration in seconds  

# Function for IP blocking and rate limiting  
def rate_limit():  
    client_ip = request.remote_addr  

    # Block if IP is in blacklist  
    if client_ip in blacklist:  
        abort(403, description="You are temporarily blocked.")  

    # Current time  
    current_time = time.time()  

    # Update request log for this IP  
    request_log[client_ip].append(current_time)  
    request_log[client_ip] = [t for t in request_log[client_ip] if current_time - t < 10]  

    # If rate limit exceeded, block the IP  
    if len(request_log[client_ip]) > RATE_LIMIT:  
        print(f"{client_ip} blocked for {BLOCK_DURATION} seconds!")  
        blacklist.add(client_ip)  

        # Remove IP from blacklist after block duration  
        time.sleep(BLOCK_DURATION)  
        blacklist.remove(client_ip)  

# Home page route  
@app.route('/')  
def home():  
    rate_limit()  
    return jsonify({'message': 'Secure website is running!'}), 200  

# Heavy load page route  
@app.route('/heavy')  
def heavy():  
    rate_limit()  
    time.sleep(2)  # Simulating CPU-intensive processing  
    return jsonify({'message': 'Heavy processing done'}), 200  

# Logs route  
@app.route('/logs')  
def logs():  
    return jsonify({'blacklist': list(blacklist), 'requests': dict(request_log)})  

# About page route  
@app.route('/about')  
def about():  
    rate_limit()  
    return jsonify({'message': 'About Us Page'}), 200  

# Contact page route  
@app.route('/contact')  
def contact():  
    rate_limit()  
    return jsonify({'message': 'Contact Us Page'}), 200  

# Run the Flask app on port 3000  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=3000, threaded=True)  
