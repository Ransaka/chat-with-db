from flask import Flask, send_file, request
from langchain_utils import agent
from utils import get_file_names


app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return "Hello, world"

@app.route("/support", methods=['POST'])
def support_bot():
    data = request.get_json()
    query = data['query']
    response = agent.invoke({"input":query})
    processed_response = get_file_names(response['output'])
    if processed_response.endswith(".csv"):
        return send_file(processed_response, as_attachment=True)
    else:
        return processed_response
    return response

if __name__ == '__main__':
    app.run()
