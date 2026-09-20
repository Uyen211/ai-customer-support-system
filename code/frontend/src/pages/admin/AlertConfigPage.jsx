import React, { useState, useEffect } from 'react';
import { getConfig, updateConfig } from '../../services/configService';
import logoAsset from '../../assets/logo.png';

const AlertConfigPage = () => {
    const [config, setConfig] = useState({
        instruction_prompt: '',
        p1_threshold: -0.60,
        p2_threshold: -0.30
    });
    const [originalConfig, setOriginalConfig] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState('');

    useEffect(() => {
        fetchConfig();
    }, []);

    const fetchConfig = async () => {
        try {
            setLoading(true);
            const data = await getConfig();
            setConfig(data);
            setOriginalConfig(data);
            setError(null);
        } catch (err) {
            setError("Không thể tải cấu hình từ máy chủ.");
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setConfig(prev => ({
            ...prev,
            [name]: name.includes('threshold') ? parseFloat(value) || 0 : value
        }));
    };

    // Kiểm tra tính hợp lệ: P1 phải nhỏ hơn P2 một cách nghiêm ngặt
    const isInvalid = config.p1_threshold >= config.p2_threshold;
    
    // UX Polish: Kiểm tra xem có thay đổi gì chưa
    const isDirty = originalConfig && (
        config.instruction_prompt !== originalConfig.instruction_prompt ||
        config.p1_threshold !== originalConfig.p1_threshold ||
        config.p2_threshold !== originalConfig.p2_threshold
    );

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isInvalid || !isDirty) return;
        
        try {
            setSubmitting(true);
            setError(null);
            setSuccessMsg('');
            const data = await updateConfig(config);
            setOriginalConfig(data);
            setSuccessMsg("Cập nhật cấu hình thành công!");
            setTimeout(() => setSuccessMsg(''), 3000); // Ẩn toast sau 3 giây
        } catch (err) {
            setError(err.response?.data?.detail || "Lỗi khi cập nhật cấu hình.");
        } finally {
            setSubmitting(false);
        }
    };

    const handleCancel = () => {
        if (originalConfig) {
            setConfig(originalConfig);
            setError(null);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-[#FFF8E7] flex items-center justify-center text-[#2B2523]">
                Đang tải cấu hình...
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#FFF8E7] text-[#2B2523] p-8 md:p-16 font-sans">
            <div className="max-w-4xl mx-auto">
                <header className="mb-12 flex items-center justify-between">
                    <div>
                        <h1 className="text-4xl font-serif text-[#2B2523] tracking-tight mb-2">Cấu hình Quy tắc Cảnh báo</h1>
                        <p className="text-sm font-medium tracking-wide uppercase text-[#2B2523] opacity-60">
                            Quản lý hệ thống phân loại sự cố AI
                        </p>
                    </div>
                    <div className="flex items-center gap-3">
                        <img src={logoAsset} alt="PetHome Logo" className="w-12 h-12 object-cover rounded-full shadow-diffused border border-[#930500]/20" />
                        <span className="font-serif-editorial text-2xl font-bold text-[#2B2523]">PetHome</span>
                    </div>
                </header>

                <form onSubmit={handleSubmit} className="bg-white/40 backdrop-blur-md rounded-[32px] p-8 md:p-12 shadow-[0_24px_50px_rgba(147,5,0,0.04)] border border-[#EFE7D3]">
                    {/* Hướng dẫn phân loại */}
                    <div className="mb-10">
                        <label className="block text-lg font-semibold mb-3 text-[#2B2523]">
                            Hướng dẫn phân loại sự cố (Prompt)
                        </label>
                        <p className="text-sm opacity-70 mb-4">
                            Ngôn ngữ tự nhiên để hướng dẫn AI cách nhận diện các sự cố đặc thù.
                        </p>
                        <textarea 
                            name="instruction_prompt"
                            value={config.instruction_prompt}
                            onChange={handleChange}
                            rows="4"
                            className="w-full bg-[#FFF8E7]/50 rounded-[20px] p-5 border border-[rgba(147,5,0,0.08)] focus:outline-none focus:ring-1 focus:ring-[#95BBEA] transition-all duration-300 ease-out resize-none text-[#2B2523]"
                            placeholder="Ví dụ: Nếu khách hàng phản ánh sai kích thước sản phẩm..."
                        ></textarea>
                    </div>

                    {/* Khối Ngưỡng Điểm */}
                    <div className="bg-[#95BBEA]/20 rounded-[24px] p-8 mb-10 flex flex-col md:flex-row gap-8">
                        <div className="flex-1">
                            <label className="block text-md font-semibold mb-2">
                                Ngưỡng khẩn cấp (P1)
                            </label>
                            <p className="text-xs opacity-70 mb-3">Mặc định: -0.60</p>
                            <input 
                                type="number" 
                                step="0.01" 
                                max="0"
                                name="p1_threshold"
                                value={config.p1_threshold}
                                onChange={handleChange}
                                className="w-full bg-white rounded-full px-6 py-3 border border-transparent focus:outline-none focus:border-[#95BBEA] text-[#2B2523]"
                            />
                        </div>
                        <div className="flex-1">
                            <label className="block text-md font-semibold mb-2">
                                Ngưỡng trung bình (P2)
                            </label>
                            <p className="text-xs opacity-70 mb-3">Mặc định: -0.30</p>
                            <input 
                                type="number" 
                                step="0.01" 
                                max="0"
                                name="p2_threshold"
                                value={config.p2_threshold}
                                onChange={handleChange}
                                className="w-full bg-white rounded-full px-6 py-3 border border-transparent focus:outline-none focus:border-[#95BBEA] text-[#2B2523]"
                            />
                        </div>
                    </div>

                    {/* Validation Error Message */}
                    {isInvalid && (
                        <div className="mb-8 text-[#930500] font-medium px-4">
                            Cảnh báo: Ngưỡng P1 ({config.p1_threshold}) phải nhỏ hơn ngưỡng P2 ({config.p2_threshold}).
                        </div>
                    )}
                    {error && (
                        <div className="mb-8 text-[#930500] font-medium px-4">
                            Lỗi: {error}
                        </div>
                    )}
                    {successMsg && (
                        <div className="mb-8 text-green-700 font-medium px-4">
                            {successMsg}
                        </div>
                    )}

                    {/* Actions */}
                    <div className="flex items-center justify-end gap-4 mt-8 pt-6 border-t border-[rgba(147,5,0,0.05)]">
                        {isDirty && (
                            <button 
                                type="button" 
                                onClick={handleCancel}
                                className="px-8 py-3 rounded-full text-[#2B2523] font-medium hover:bg-[rgba(147,5,0,0.05)] transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]"
                            >
                                Hủy
                            </button>
                        )}
                        <button 
                            type="submit" 
                            disabled={isInvalid || !isDirty || submitting}
                            className={`px-10 py-3 rounded-full font-medium transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] shadow-[0_8px_20px_rgba(147,5,0,0.15)]
                                ${isInvalid || !isDirty || submitting 
                                    ? 'bg-gray-300 text-gray-500 shadow-none cursor-not-allowed' 
                                    : 'bg-[#930500] hover:bg-[#7a0400] text-white hover:-translate-y-[1px] hover:shadow-[0_12px_24px_rgba(147,5,0,0.2)]'
                                }`}
                        >
                            {submitting ? 'Đang lưu...' : 'Lưu thay đổi'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AlertConfigPage;
