import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for LLM calls
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`Response received:`, response.status);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const careerAPI = {
  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      throw new Error('Backend is not available');
    }
  },

  // Simple chat for testing
  async chat(message, context = null) {
    try {
      const requestBody = {
        message: message,
        ...(context && {
          conversation_history: context.conversation_history,
          current_learning_path: context.current_learning_path,
          is_follow_up: context.is_follow_up
        })
      };

      console.log('🌐 API: Sending request:', {
        message: message.substring(0, 50) + '...',
        has_context: !!context,
        context_keys: context ? Object.keys(context) : []
      });

      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      
      console.log('🌐 API: Received response:', {
        has_response: !!data.response,
        has_learning_path: !!(data.data && data.data.learning_path),
        response_length: data.response ? data.response.length : 0
      });

      return data;
    } catch (error) {
      console.error('API chat error:', error);
      throw error;
    }
  },

  // Full career planning
  async createCareerPlan(currentRole, targetRole, message) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/career-plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          current_role: currentRole,
          target_role: targetRole
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Career plan API error:', error);
      throw error;
    }
  },

  // Test backend connection
  async testConnection() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Backend connection test failed:', error);
      throw new Error(`Backend not available: ${error.message}`);
    }
  }
};

export default api; 