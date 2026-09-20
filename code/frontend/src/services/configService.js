import axios from 'axios';

// Giả định API base url. Nếu dự án đang dùng một axios instance cấu hình sẵn, 
// bạn nên import instance đó (ví dụ: import api from './api').
const API_BASE_URL = 'http://localhost:8000/api/v1'; 

export const getConfig = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/configs/alerts`);
        return response.data;
    } catch (error) {
        console.error("Lỗi khi tải cấu hình:", error);
        throw error;
    }
};

export const updateConfig = async (configData) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/configs/alerts`, configData);
        return response.data;
    } catch (error) {
        console.error("Lỗi khi cập nhật cấu hình:", error);
        throw error;
    }
};
