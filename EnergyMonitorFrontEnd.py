import json

from flask import Flask, render_template, request, jsonify
import UsageData
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("base.html")


@app.route("/usage")
def usage():
    phase = request.args.get('phase', '')
    start_timestamp = request.args.get('start', 0)
    end_timestamp = request.args.get('end', 0)

    data = UsageData.get_usage(phase, start_timestamp, end_timestamp)
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
