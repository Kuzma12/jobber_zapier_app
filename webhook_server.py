from flask import Flask, request
from main import main as run_sync

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        run_sync()
        return {"status": "success", "message": "Data sync completed"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/", methods=["GET"])
def index():
    return '''
        <h2>Jobber-Zapier Sync Admin</h2>
        <form action="/webhook" method="post">
            <button type="submit">Run Manual Sync</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
