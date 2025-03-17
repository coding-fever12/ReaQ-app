export const validateImage = (image) => {
    if (!image || !image.uri) {
      throw new Error('Invalid image');
    }
  
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!allowedTypes.includes(image.type)) {
      throw new Error('Unsupported image format');
    }
  
    return true;
  };
  
  export const formatPrediction = (prediction) => {
    return prediction.charAt(0).toUpperCase() + prediction.slice(1).toLowerCase();
  };