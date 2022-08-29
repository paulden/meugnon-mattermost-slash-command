from meugnon import app
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host="0.0.0.0", port=8000)
