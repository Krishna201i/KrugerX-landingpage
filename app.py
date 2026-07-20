import os
import httpx
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mystical-secret-key-12345'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
async def backend_status():
    """Asynchronously ping the FastAPI backend health endpoint"""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get('http://localhost:8000/api/v1/health')
            if response.status_code == 200:
                return jsonify({"status": "online", "message": "All Systems Operational"})
            return jsonify({"status": "degraded", "message": "Backend Connectivity Issues"})
    except httpx.RequestError:
        return jsonify({"status": "offline", "message": "Backend Offline"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
