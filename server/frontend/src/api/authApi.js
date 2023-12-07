import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL

axios.defaults.withCredentials = true;

const authApi = {
    Activate: async (uid, token) => {
        try {
            const response = await axios.post(
                `${BASE_URL}/api/auth/users/activation/`,
                { uid, token }
            );
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    ResendActivation: async (data) => {
        try {
            const response = await axios.post(
                `${BASE_URL}/api/auth/users/resend_activation/`,
                data,
            );
            return response;
        } catch (error) {
            throw error;
        }
    },
}

export default authApi
