export const API_URL = __DEV__ 
  ? 'http://10.0.2.2:5000'  // Android emulator localhost
  : 'http://your-production-api-url.com';

export const IMAGE_CONFIG = {
  maxWidth: 800,
  maxHeight: 800,
  quality: 0.8,
};

export const APP_CONFIG = {
  maxRetries: 3,
  timeoutSeconds: 30,
};