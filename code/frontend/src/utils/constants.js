export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const MODE = {
  BOT: 'BOT',
  HUMAN: 'HUMAN',
  WAITING_HUMAN: 'WAITING_HUMAN',
  CLOSED: 'CLOSED',
};

export const CONVERSATION_STATUS = {
  ACTIVE: 'ACTIVE',
  WAITING_HUMAN: 'WAITING_HUMAN',
  CLOSED: 'CLOSED',
};

export const SUGGESTION_PROMPTS = [
  "Chính sách miễn phí vận chuyển áp dụng như thế nào?",
  "Giá Hạt Royal Canin Kitten 2kg bao nhiêu?",
  "Quy định đổi trả hàng bị lỗi trong vòng 7 ngày",
  "Cửa hàng PetHome Hà Nội mở cửa đến mấy giờ?",
  "Tư vấn thức ăn cho mèo Anh lông ngắn 3 tháng tuổi",
];
