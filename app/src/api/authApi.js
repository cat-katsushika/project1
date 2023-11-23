import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api'

axios.defaults.withCredentials = true;

const authApi = {
    Activate : async (uid, token) => {
        try {
            const response = await axios.post(
                `${BASE_URL}/auth/users/activation/`,
                { uid, token }
            );
            return response.data;
        } catch (error) {
            throw error;
        }
    },
}

export default authApi
