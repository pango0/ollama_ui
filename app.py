from flask import Flask, jsonify, request, render_template, Response
import psutil
import GPUtil
import platform
import requests
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/hardware_information')
def hardware_information():
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
        "current_frequency": f"{psutil.cpu_freq().current:.2f}Mhz",
    }
    
    memory = psutil.virtual_memory()
    ram_info = {
        "total": f"{memory.total / (1024**3):.2f} GB",
        "available": f"{memory.available / (1024**3):.2f} GB",
        "used": f"{memory.used / (1024**3):.2f} GB",
        "percentage": f"{memory.percent}%",
    }
    
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "id": gpu.id,
            "name": gpu.name,
            "memory_total": f"{gpu.memoryTotal} MB",
            "memory_used": f"{gpu.memoryUsed} MB",
            "memory_free": f"{gpu.memoryFree} MB",
            "load": f"{gpu.load*100}%",
        })
    
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    
    hardware_info = {
        "cpu": cpu_info,
        "ram": ram_info,
        "gpu": gpu_info,
        "system": system_info
    }
    

    return render_template('hardware.html', hardware_info=hardware_info)

@app.route('/api/available_models')
def get_available_models():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        models = response.json().get('models', [])
        return jsonify(models)  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/available_models')
def available_models():
    return render_template('available_models.html')

@app.route('/pull_models')
def pull_models():
    return render_template('pull_models.html')

@app.route('/running_models')
def running_models():
    return render_template('running_models.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)