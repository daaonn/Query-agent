# metadata.py

TABLE_NAME = "ecommerce-analysis-491016.ecommerce.ecommerce_sample"

METADATA = """
테이블명: ecommerce_sample
설명: 2023-01-01 ~ 2024-06-30 뷰티 이커머스 주문 데이터 (2,000건)

컬럼 정의:
  - order_id       : 주문 고유 ID (예: ORD-2023000)
  - order_date     : 주문 일자 (DATE, 예: 2023-04-25)
  - customer_id    : 고객 고유 ID (예: CUS-13478)
  - gender         : 성별 ('F' = 여성, 'M' = 남성)
  - age            : 나이 (숫자, 18~55세, 결측 47건)
  - region         : 지역 ('서울', '경기', '부산', '대구', '광주', '인천', '대전', '기타', 결측 76건)
  - category       : 제품 카테고리 ('스킨케어', '메이크업', '헤어케어', '건강기능식품', '향수')
  - product_name   : 제품명 (예: 선크림 SPF50, 헤어오일 100ml)
  - channel        : 구매 채널 ('네이버쇼핑', '자사몰', '카카오쇼핑', '쿠팡', '인스타그램광고')
  - quantity       : 구매 수량 (1~5)
  - unit_price     : 단가 (원, 12000~88000)
  - discount_rate  : 할인율 (0.0~0.2, 예: 0.05 = 5% 할인)
  - total_price    : 최종 결제 금액 (원)
  - payment_method : 결제 수단 ('카드', '카카오페이', '네이버페이', '무통장입금', '포인트', 결측 52건)
  - is_returned    : 반품 여부 (TRUE = 반품, FALSE = 정상)
  - return_reason  : 반품 사유 ('품질불량', '사이즈불일치', '오배송', '단순변심', 반품 아닌 경우 NULL)
  - device_type    : 구매 기기 ('mobile', 'tablet', 'desktop')

주의사항:
  - 날짜 필터는 EXTRACT 또는 DATE 함수 사용
  - region, age, payment_method는 결측값 존재
  - return_reason은 is_returned = TRUE인 경우만 값 존재
"""