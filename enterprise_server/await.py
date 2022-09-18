from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/ans_callback', methods=['POST'])
def await_callback():
  if request.method == "POST":
    print(str(request.data))
    return "Received"