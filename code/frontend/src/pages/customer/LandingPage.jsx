import React from 'react';
import { Bot, ShieldCheck, Truck, Sparkles, MessageCircle, ArrowRight, Heart, PackageCheck, Award, CheckCircle2, BriefcaseBusiness } from 'lucide-react';
import { Button } from '../../components/common/Button';

export function LandingPage({ onNavigate }) {
  const handleStartChat = () => {
    onNavigate('chat');
  };

  const handleLogin = () => {
    onNavigate('login');
  };

  const handleRegister = () => {
    onNavigate('register');
  };

  const handleStaffLogin = () => {
    onNavigate('staff-login');
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] text-[#2B2523] selection:bg-[#930500] selection:text-[#FFF8E7]">
      {/* 1. Header / Navigation Bar */}
      <header className="sticky top-0 z-40 bg-[#FFF8E7]/90 backdrop-blur-md border-b border-[#EFE7D3] transition-all">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => onNavigate('landing')}>
            <div className="w-10 h-10 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center font-serif-editorial text-xl shadow-diffused-sm">
              🐾
            </div>
            <div>
              <span className="font-serif-editorial text-2xl font-bold tracking-tight text-[#2B2523]">PetHome</span>
              <span className="text-[10px] block uppercase tracking-widest text-[#930500] font-semibold -mt-1">Organic & AI Care</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
            <a href="#features" className="hover:text-[#930500] transition-colors">Tính Năng AI</a>
            <a href="#products" className="hover:text-[#930500] transition-colors">Sản Phẩm Nổi Bật</a>
            <a href="#policies" className="hover:text-[#930500] transition-colors">Chính Sách</a>
            <a href="#about" className="hover:text-[#930500] transition-colors">Về PetHome</a>
          </nav>

          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" onClick={handleLogin}>
              Đăng Nhập
            </Button>
            <Button variant="soft" size="sm" icon={BriefcaseBusiness} onClick={handleStaffLogin}>
              Nhân Viên
            </Button>
            <Button variant="outline" size="sm" onClick={handleRegister}>
              Đăng Ký
            </Button>
            <Button variant="primary" size="sm" icon={MessageCircle} onClick={handleStartChat}>
              Chat AI 24/7
            </Button>
          </div>
        </div>
      </header>

      {/* 2. Hero Section - Editorial Style */}
      <section className="relative pt-12 pb-20 md:pt-20 md:pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            <div className="lg:col-span-7 flex flex-col items-start gap-6">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#95BBEA]/30 border border-[#95BBEA] text-[#2B2523] text-xs font-semibold uppercase tracking-widest">
                <Sparkles className="w-4 h-4 text-[#930500]" />
                Trợ Lý Trực Tuyến RAG AI Thế Hệ Mới
              </div>

              <h1 className="font-serif-editorial text-4xl sm:text-5xl md:text-6xl font-normal leading-[1.15] text-[#2B2523]">
                Chăm Sóc Thú Cưng Với Sự <span className="italic text-[#930500]">Ân Cần</span> & Công Nghệ AI 24/7
              </h1>

              <p className="text-base sm:text-lg text-[#2B2523]/80 leading-relaxed max-w-2xl font-light">
                Hệ thống hỗ trợ thông minh giải đáp ngay lập tức về tồn kho sản phẩm, tư vấn dinh dưỡng chuẩn xác, chính sách đổi trả minh bạch và kết nối nhân viên tư vấn tức thì.
              </p>

              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Button variant="primary" size="lg" icon={ArrowRight} onClick={handleStartChat}>
                  Hỏi Trợ Lý AI Ngay
                </Button>
                <Button variant="soft" size="lg" onClick={handleRegister}>
                  Đăng Ký Khách Hàng
                </Button>
              </div>

              {/* Trust Badges */}
              <div className="pt-8 border-t border-[#EFE7D3] w-full grid grid-cols-3 gap-6 text-center sm:text-left">
                <div>
                  <p className="font-serif-editorial text-3xl font-bold text-[#930500]">24/7</p>
                  <p className="text-xs text-[#2B2523]/70 font-medium">Hỗ trợ tức thì</p>
                </div>
                <div>
                  <p className="font-serif-editorial text-3xl font-bold text-[#2B2523]">100%</p>
                  <p className="text-xs text-[#2B2523]/70 font-medium">Chính xác trích dẫn</p>
                </div>
                <div>
                  <p className="font-serif-editorial text-3xl font-bold text-[#930500]">10.000+</p>
                  <p className="text-xs text-[#2B2523]/70 font-medium">Khách hàng tin dùng</p>
                </div>
              </div>
            </div>

            {/* Visual Art Block */}
            <div className="lg:col-span-5 relative">
              <div className="relative bg-[#95BBEA] rounded-[3rem] p-8 md:p-10 shadow-editorial-hover border border-[#95BBEA]/40 overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-[#FFF8E7]/30 rounded-full blur-2xl pointer-events-none" />
                
                <div className="relative z-10 flex flex-col gap-6">
                  <div className="flex items-center justify-between">
                    <span className="px-3 py-1 bg-[#FFF8E7] text-[#930500] rounded-full text-xs font-semibold uppercase tracking-wider">
                      Live AI Demo
                    </span>
                    <span className="flex items-center gap-1.5 text-xs text-[#2B2523] font-medium">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                      Trực tuyến
                    </span>
                  </div>

                  <div className="space-y-4">
                    <div className="bg-[#FFF8E7] rounded-2xl p-4 shadow-diffused-sm border border-[#EFE7D3]">
                      <p className="text-xs text-[#2B2523]/60 font-semibold mb-1">Khách hàng hỏi:</p>
                      <p className="text-sm text-[#2B2523] font-medium">"Hạt Nutrience SubZero 2.5kg còn hàng ở showroom Hà Nội không ạ?"</p>
                    </div>

                    <div className="bg-[#FFF8E7]/90 backdrop-blur-sm rounded-2xl p-4 shadow-diffused-sm border border-[#930500]/10">
                      <p className="text-xs text-[#930500] font-semibold mb-1 flex items-center gap-1">
                        <Bot className="w-3.5 h-3.5" /> Trợ lý PetHome AI:
                      </p>
                      <p className="text-sm text-[#2B2523] leading-relaxed">
                        "Dạ chào bạn! Hạt Nutrience SubZero 2.5kg hiện <strong>còn 15 gói</strong> tại showroom PetHome Cầu Giấy (Hà Nội) với giá niêm yết <strong>680.000đ</strong>. Áp dụng Freeship đơn từ 500k ạ!"
                      </p>
                      <div className="mt-2 text-[11px] text-[#930500] bg-[#930500]/5 px-2.5 py-1 rounded-full inline-block font-medium">
                        📌 Nguồn: catalog_pethome_2026.pdf (Trang 14)
                      </div>
                    </div>
                  </div>

                  <div className="pt-2">
                    <Button variant="primary" className="w-full justify-center" icon={MessageCircle} onClick={handleStartChat}>
                      Thử Trò Chuyện Trực Tiếp
                    </Button>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 3. Features Section - 4 Core Pillars */}
      <section id="features" className="py-20 bg-[#95BBEA]/20 border-y border-[#EFE7D3]">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs uppercase tracking-widest text-[#930500] font-semibold">Công Nghệ Hỗ Trợ Toàn Diện</span>
            <h2 className="font-serif-editorial text-3xl sm:text-4xl text-[#2B2523] mt-2">
              4 Trụ Cột Trải Nghiệm Khách Hàng Xuất Sắc
            </h2>
            <p className="text-sm sm:text-base text-[#2B2523]/70 mt-3 font-light">
              Kết hợp sức mạnh trí tuệ nhân tạo RAG với sự tận tâm của đội ngũ chăm sóc khách hàng truyền thống.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            
            {/* Feature 1 */}
            <div className="bg-[#FFF8E7] rounded-3xl p-8 border border-[#EFE7D3] shadow-editorial-hover flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#95BBEA] text-[#2B2523] flex items-center justify-center mb-6">
                  <PackageCheck className="w-6 h-6" />
                </div>
                <h3 className="font-serif-editorial text-xl font-bold text-[#2B2523] mb-3">
                  Tra Cứu Giá & Tồn Kho Real-time
                </h3>
                <p className="text-sm text-[#2B2523]/75 leading-relaxed font-light">
                  Kiểm tra tức thì giá sản phẩm, tình trạng còn hàng theo từng địa điểm showroom cửa hàng.
                </p>
              </div>
              <div className="mt-6 pt-4 border-t border-[#EFE7D3] text-xs font-semibold text-[#930500] flex items-center gap-1">
                Dữ liệu đồng bộ SQL <CheckCircle2 className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Feature 2 */}
            <div className="bg-[#FFF8E7] rounded-3xl p-8 border border-[#EFE7D3] shadow-editorial-hover flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#930500] text-[#FFF8E7] flex items-center justify-center mb-6">
                  <Truck className="w-6 h-6" />
                </div>
                <h3 className="font-serif-editorial text-xl font-bold text-[#2B2523] mb-3">
                  Chính Sách Đổi Trả & Giao Hàng
                </h3>
                <p className="text-sm text-[#2B2523]/75 leading-relaxed font-light">
                  Giải đáp chi tiết quy định freeship đơn từ 500k, chính sách đổi hàng 1-đổi-1 trong 7 ngày.
                </p>
              </div>
              <div className="mt-6 pt-4 border-t border-[#EFE7D3] text-xs font-semibold text-[#930500] flex items-center gap-1">
                Tự động trích dẫn PDF <CheckCircle2 className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Feature 3 */}
            <div className="bg-[#FFF8E7] rounded-3xl p-8 border border-[#EFE7D3] shadow-editorial-hover flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#95BBEA] text-[#2B2523] flex items-center justify-center mb-6">
                  <Heart className="w-6 h-6" />
                </div>
                <h3 className="font-serif-editorial text-xl font-bold text-[#2B2523] mb-3">
                  Giám Sát Cảm Xúc & Chuyển Người
                </h3>
                <p className="text-sm text-[#2B2523]/75 leading-relaxed font-light">
                  Tự động phát hiện tâm lý không hài lòng của khách hàng và chuyển giao cho tư vấn viên tiếp quản.
                </p>
              </div>
              <div className="mt-6 pt-4 border-t border-[#EFE7D3] text-xs font-semibold text-[#930500] flex items-center gap-1">
                AI Auto-Triage Engine <CheckCircle2 className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Feature 4 */}
            <div className="bg-[#FFF8E7] rounded-3xl p-8 border border-[#EFE7D3] shadow-editorial-hover flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#930500] text-[#FFF8E7] flex items-center justify-center mb-6">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <h3 className="font-serif-editorial text-xl font-bold text-[#2B2523] mb-3">
                  Trích Dẫn Minh Bạch 100%
                </h3>
                <p className="text-sm text-[#2B2523]/75 leading-relaxed font-light">
                  Mọi câu trả lời của AI đều đính kèm trích đoạn tài liệu gốc (tên file, số trang, điều khoản cụ thể).
                </p>
              </div>
              <div className="mt-6 pt-4 border-t border-[#EFE7D3] text-xs font-semibold text-[#930500] flex items-center gap-1">
                Citations Drawer <CheckCircle2 className="w-3.5 h-3.5" />
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 4. Product Showcase */}
      <section id="products" className="py-20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12">
            <div>
              <span className="text-xs uppercase tracking-widest text-[#930500] font-semibold">Danh Mục Chọn Lọc</span>
              <h2 className="font-serif-editorial text-3xl sm:text-4xl text-[#2B2523] mt-1">
                Sản Phẩm Được Thú Cưng Yêu Thích
              </h2>
            </div>
            <Button variant="outline" size="sm" className="mt-4 md:mt-0" onClick={handleStartChat}>
              Hỏi Trợ Lý Giá Sản Phẩm Khác
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                name: "Hạt Nutrience SubZero Cát Hồi",
                weight: "2.5 kg",
                price: "680.000đ",
                tag: "Bán chạy nhất",
                desc: "Đạm cao cấp từ thịt tươi đông khô",
                bg: "bg-[#95BBEA]/30",
              },
              {
                name: "Royal Canin Kitten Dành Cho Mèo Con",
                weight: "2.0 kg",
                price: "420.000đ",
                tag: "Dinh dưỡng chuẩn",
                desc: "Hỗ trợ hệ miễn dịch giai đoạn đầu",
                bg: "bg-[#FFF8E7]",
              },
              {
                name: "Cát Đậu Nành Organic Cature",
                weight: "6.0 L",
                price: "155.000đ",
                tag: "Freeship đơn 500k",
                desc: "Thâm hút vượt trội, xả được bồn cầu",
                bg: "bg-[#95BBEA]/30",
              },
              {
                name: "Pate Monge Vị Cá Thủy Cung",
                weight: "85 g",
                price: "35.000đ",
                tag: "Nhập khẩu Ý",
                desc: "Bổ sung Omega-3 & Taurine cho mắt",
                bg: "bg-[#FFF8E7]",
              },
            ].map((p, idx) => (
              <div
                key={idx}
                className={`${p.bg} rounded-3xl p-6 border border-[#EFE7D3] shadow-editorial-hover flex flex-col justify-between`}
              >
                <div>
                  <span className="px-3 py-1 bg-[#930500] text-[#FFF8E7] rounded-full text-[10px] font-semibold uppercase tracking-wider">
                    {p.tag}
                  </span>
                  <h4 className="font-serif-editorial text-lg font-bold text-[#2B2523] mt-4 mb-1">
                    {p.name}
                  </h4>
                  <p className="text-xs text-[#2B2523]/70 mb-3">{p.desc}</p>
                </div>
                <div>
                  <div className="flex items-center justify-between pt-4 border-t border-[#EFE7D3]/60 mb-4">
                    <span className="text-xs text-[#2B2523]/60">Quy cách: {p.weight}</span>
                    <span className="font-serif-editorial text-xl font-bold text-[#930500]">{p.price}</span>
                  </div>
                  <Button variant="soft" size="sm" className="w-full justify-center" onClick={handleStartChat}>
                    Hỏi Trợ Lý AI Về Món Này
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5. CTA Banner Section */}
      <section className="py-16 bg-[#930500] text-[#FFF8E7]">
        <div className="max-w-5xl mx-auto px-6 text-center flex flex-col items-center gap-6">
          <Award className="w-12 h-12 text-[#95BBEA]" />
          <h2 className="font-serif-editorial text-3xl sm:text-5xl font-normal leading-tight">
            Sẵn Sàng Trải Nghiệm Dịch Vụ Chăm Sóc Thú Cưng Đẳng Cấp?
          </h2>
          <p className="text-sm sm:text-base text-[#FFF8E7]/80 max-w-2xl font-light">
            Không cần chờ đợi lâu. Đội ngũ AI Bot và tư vấn viên PetHome luôn túc trực 24/7 để phục vụ bạn và thú cưng.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <Button
              variant="secondary"
              size="lg"
              icon={MessageCircle}
              onClick={handleStartChat}
              className="bg-[#FFF8E7] text-[#930500] hover:bg-[#EFE7D3]"
            >
              Trò Chuyện Ngay Bây Giờ
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={handleRegister}
              className="border-[#FFF8E7] text-[#FFF8E7] hover:bg-[#FFF8E7] hover:text-[#930500]"
            >
              Tạo Tài Khoản Khách Hàng
            </Button>
          </div>
        </div>
      </section>

      {/* 6. Footer */}
      <footer className="bg-[#FFF8E7] border-t border-[#EFE7D3] py-12">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="font-serif-editorial text-2xl font-bold text-[#2B2523]">PetHome</span>
            </div>
            <p className="text-xs text-[#2B2523]/70 leading-relaxed font-light">
              Chuỗi cửa hàng cung cấp đồ dùng, thức ăn & phụ kiện thú cưng chính hãng với trợ lý tư vấn AI 24/7.
            </p>
          </div>

          <div>
            <h4 className="font-serif-editorial text-base font-bold text-[#2B2523] mb-3">Showroom Hà Nội</h4>
            <p className="text-xs text-[#2B2523]/70 leading-relaxed font-light">
              124 Cầu Giấy, Q. Cầu Giấy<br />
              45 Mễ Trì, Q. Nam Từ Liêm<br />
              Hotline: 1900 6868
            </p>
          </div>

          <div>
            <h4 className="font-serif-editorial text-base font-bold text-[#2B2523] mb-3">Chính Sách</h4>
            <ul className="text-xs text-[#2B2523]/70 space-y-2 font-light">
              <li>Miễn phí giao hàng đơn từ 500k</li>
              <li>Đổi trả 1-đổi-1 trong vòng 7 ngày</li>
              <li>Bảo mật thông tin khách hàng</li>
            </ul>
          </div>

          <div>
            <h4 className="font-serif-editorial text-base font-bold text-[#2B2523] mb-3">Bản Quyền</h4>
            <p className="text-xs text-[#2B2523]/60 font-light">
              © 2026 PetHome Support System.<br />
              Tất cả quyền được bảo lưu.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
