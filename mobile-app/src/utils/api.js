import { API_URL } from '../config';

export const predictDisaster = async (imageData) => {
  try {
    const formData = new FormData();
    formData.append('image', {
      uri: imageData.uri,
      type: 'image/jpeg',
      name: 'image.jpg',
    });

    const response = await fetch(`${API_URL}/api/predict`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    const data = await response.json();
    if (!data.success) {
      throw new Error(data.error || 'Prediction failed');
    }

    return data.prediction;
  } catch (error) {
    throw error;
  }
};

export const checkServerHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/api/health`);
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    return false;
  }
};