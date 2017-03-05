from flask import Flask, request, jsonify
app = Flask(__name__)

# sensor data
sensorData = dict()


@app.route('/api/')
def test():
    return 'Hello, world!'


@app.route('/api/words', methods=['POST'])
def main():

    # default keywords
    keywords = ['uh', 'uhm']

    # parse data
    text = request.form.get('text','')
    r_keywords = request.form.get('keywords', None)

    if r_keywords:
        keywords = r_keywords.split(',')
        keywords = [k.strip() for k in keywords]

    # analyze text
    occurances = dict()
    for word in keywords:
        occurances[word] = text.count(word)

    # send back
    return jsonify(occurances)


@app.route('/api/sensor', methods=['GET', 'POST'])
def sensor():

    global sensorData

    if request.method == 'POST':
        sensorData = request.form.copy()
        return 'OK', 200
    else:
        return jsonify(sensorData)
