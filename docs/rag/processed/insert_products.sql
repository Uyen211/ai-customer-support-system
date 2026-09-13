-- Script Nạp Dữ Liệu Sản Phẩm Vào Bảng products (Supabase PostgreSQL)

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('CAT-ROYAL-INDOOR-2KG', 'Thức ăn hạt Royal Canin Indoor cho mèo trưởng thành 2kg', 'Thức ăn', 'CAT', 285000, NULL, 120, 'IN_STOCK', '{"brand": "Royal Canin", "weight": "2kg", "target_age": "ADULT", "origin": "Pháp"}'::jsonb, 'Thức ăn hạt dành cho mèo trưởng thành sống trong nhà, hỗ trợ tiêu hóa và kiểm soát búi lông.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('CAT-PETKIT-CATLIT-10L', 'Cát vệ sinh cho mèo PetKit Cat Litter 10L', 'Vệ sinh', 'CAT', 165000, 150000, 200, 'IN_STOCK', '{"brand": "PetKit", "volume": "10L", "target_age": "ALL", "type": "Tofu & Carbon"}'::jsonb, 'Cát vệ sinh vón cục nhanh, khử mùi tốt, ít bụi, an toàn cho mèo và người nuôi.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('DOG-ROYAL-MINI-4KG', 'Thức ăn hạt Royal Canin Mini Adult cho chó nhỏ 4kg', 'Thức ăn', 'DOG', 420000, NULL, 85, 'IN_STOCK', '{"brand": "Royal Canin", "weight": "4kg", "target_age": "ADULT", "suitable_breed": "Poodle, Pug, Corgi, Pom, Chihuahua (<10kg)"}'::jsonb, 'Thức ăn hạt cho chó trưởng thành giống nhỏ dưới 10kg, hỗ trợ tiêu hóa và lông da khỏe mạnh.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('DOG-KONG-CLASSIC-M', 'Đồ chơi Kong Classic size M cho chó', 'Đồ chơi', 'DOG', 320000, NULL, 60, 'IN_STOCK', '{"brand": "Kong", "size": "M", "material": "Cao su tự nhiên", "target_age": "ALL"}'::jsonb, 'Đồ chơi cao su tự nhiên bền bỉ, giúp chó giải trí, giảm stress và hạn chế cắn phá đồ đạc.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('CAT-PETKIT-FOUNTAIN-2L', 'Máy uống nước tự động PetKit Eversweet 2L cho mèo', 'Phụ kiện', 'CAT', 890000, 799000, 45, 'IN_STOCK', '{"brand": "PetKit", "capacity": "2L", "target_age": "ALL", "warranty": "12 tháng"}'::jsonb, 'Máy uống nước tự động giúp mèo uống nhiều nước hơn, hỗ trợ sức khỏe thận và tiết niệu.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('DOG-BIO-PETSHAMPOO-500ML', 'Sữa tắm Bio Pet Shampoo cho chó 500ml', 'Chăm sóc', 'DOG', 185000, NULL, 150, 'IN_STOCK', '{"brand": "Bio Pet", "volume": "500ml", "target_age": "ALL", "scent": "Thảo dược dịu nhẹ"}'::jsonb, 'Sữa tắm thảo dược giúp làm sạch, khử mùi và giảm ngứa cho chó, an toàn cho da nhạy cảm.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('BIRD-VERSELE-LAGA-PARROT-1KG', 'Thức ăn hạt Versele-Laga cho vẹt 1kg', 'Thức ăn', 'BIRD', 195000, NULL, 70, 'IN_STOCK', '{"brand": "Versele-Laga", "weight": "1kg", "target_age": "ADULT", "origin": "Bỉ"}'::jsonb, 'Thức ăn hỗn hợp hạt dinh dưỡng dành cho vẹt cảnh, hỗ trợ tiêu hóa và lông sáng khỏe.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('CAT-TRIXIE-SCRATCHER-L', 'Trụ cào móng Trixie cho mèo size L', 'Phụ kiện', 'CAT', 450000, 399000, 40, 'IN_STOCK', '{"brand": "Trixie", "size": "L (Cao 50cm)", "material": "Dây thừng Sisal tự nhiên", "target_age": "ALL"}'::jsonb, 'Trụ cào móng giúp mèo mài móng, bảo vệ sofa và đồ đạc trong nhà, kèm đồ chơi treo.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('DOG-FRONTLINE-SPOTON-3PIP', 'Thuốc nhỏ gáy Frontline Spot On cho chó 3 pipet', 'Chăm sóc', 'DOG', 350000, NULL, 90, 'IN_STOCK', '{"brand": "Frontline", "specification": "Hộp 3 ống (3 pipet)", "target_age": "ADULT (Trên 8 tuần tuổi)"}'::jsonb, 'Thuốc nhỏ gáy phòng và trị ve, bọ chét cho chó, hiệu quả kéo dài 1 tháng mỗi ống.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('CAT-WHISKAS-PATE-12GX12', 'Pate Whiskas cho mèo vị cá ngừ 12 gói x 80g', 'Thức ăn', 'CAT', 145000, 135000, 180, 'IN_STOCK', '{"brand": "Whiskas", "specification": "Hộp 12 gói x 80g", "flavor": "Cá ngừ", "target_age": "ADULT"}'::jsonb, 'Pate mềm cho mèo trưởng thành, vị cá ngừ thơm ngon, giàu dinh dưỡng và độ ẩm.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
VALUES ('DOG-PETKIT-FEEDER-6L', 'Máy cho ăn tự động PetKit Fresh Element 6L cho chó mèo', 'Phụ kiện', 'DOG', 1450000, 1390000, 30, 'IN_STOCK', '{"brand": "PetKit", "capacity": "6L", "target_age": "ALL", "connection": "Wi-Fi App Control", "warranty": "12 tháng"}'::jsonb, 'Máy cho ăn tự động 6L, hẹn giờ, điều khiển qua app điện thoại, phù hợp cho chó mèo.')
ON CONFLICT (sku) DO UPDATE SET
  price = EXCLUDED.price, sale_price = EXCLUDED.sale_price, stock_quantity = EXCLUDED.stock_quantity, updated_at = NOW();

