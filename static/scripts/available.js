document.addEventListener('DOMContentLoaded', fetchAvailableModels);
async function fetchAvailableModels() {
    const modelListDiv = document.getElementById('model-list');
    modelListDiv.innerHTML = '<p class="loading">Fetching available models...</p>';
      
    try {
        const response = await axios.get('/api/available_models');
        modelListDiv.innerHTML = '';
        response.data.forEach(model => {
            const modelItem = document.createElement('div');
            modelItem.className = 'model-item';
            modelItem.innerHTML = `
                <strong>${model.name}</strong>
                <p>Size: ${formatSize(model.size)}</p>
            `;
            modelListDiv.appendChild(modelItem);
        });
    } catch (error) {
        modelListDiv.innerHTML = '<p style="color: red;">Error fetching models: ' + error.message + '</p>';
    }
}

function formatSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}