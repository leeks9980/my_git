select * from member;  -- 데이터 조회  select 이름 from 데이블 명
select * from member where member_name = '아이유';  -- where문 조건문 
create view member_view as select * from member;  -- view는 가상의 데이터
select * from member_view;  -- 만든 가상의 데이터 출력
-- view는 원본데이터에 접근하지 않고 데이터 가공 가능

use market_db; -- 특정 데이터 베이스르 사용하겠다
select * from member; -- member안에 있는 모든 열을 불러 오겠다
select * from market_db.member; -- use를 사용하지 않고 원하는 데이터베이스 데이블 값 불러오기
select mem_name from member; -- member테이블에서 mem_name열 만 출력
select mem_name, height, addr from member; -- 여러개의 열 또한 가능
select * from member where mem_name = '블랙핑크'; -- 조건을 추가해서 출력
select * from member where mem_number = 4; -- mem_number값이 4인 행 만 출력
select * from member where height >= 162; -- 논리 연사자, 관계 연사자 또한 사용가능
select * from member where height >= 162 and mem_number > 6; -- 2가지 이상의 조건식도 가능

SELECT * FROM member WHERE height >= 163 AND height <= 165;
SELECT * FROM member WHERE height BETWEEN 163 AND 165; -- between (원하는 값) and (원하는 값) 값의 사이에 속하는 행만 출력

SELECT * FROM member WHERE addr = '경기' OR addr = '전남' OR addr = '경남' ;
SELECT * FROM member WHERE addr IN ('경기' , '전남' , '경남'); -- IN(원하는 값), 원하는 값이 포함된 행만 출력

select * from member where mem_name like '엔%'; -- 첫글자가 '엔'으로 시작 하는 값 찾기
select * from member where mem_name like '%티'; -- 마지막 글자가 '티'로 끝나는 값 찾기 %는  그 뒤는 무엇이든 허용 한다는 의미

select * from member where mem_name like '__핑크'; -- 앞 뒤글자는 상관없이 뒤에 있는 '핑크'가 있는 값 찾기 '_'는 글자가 몇개 인지 지정

select * from member where height > (select height from member where mem_name = '에이핑크'); -- select문 안에 또 다른 select문이 들어갈수 있다

-- 과제
use market_db;
select * from member where mem_number >= 5 and mem_name like '%핑크';

select * from member order by debut_date; -- order by절은 결과가 출력되는 순서를 조절 (빠른 순서대로)
select * from member order by debut_date desc; -- 늦은 순서대로 desc(descending) 내림차순, asc(ascending) 오름차순;

SELECT * FROM member WHERE height >= 164 ORDER BY height DESC; -- where 문과 같이 사용가능

-- 과제
SELECT * FROM member WHERE height >= 164 ORDER BY height, debut_date;

select * from member limit 3; -- 상위 3개의 값만 출력함
select * from member ORDER BY debut_date limit 3; -- 데뷔일자가 빠른 3개의 값 출력

select * from member order by height desc limit 3,2; -- limit 3만 작성하면 0,3과 동일 3,2를 하면 3번쨰로 있는 값 부터 2개만 출력하겠다

SELECT addr FROM member;
select distinct addr from member; -- 중복값을 제거해줌

select mem_id, amount from buy;
select mem_id, sum(amount) from buy group by mem_id; -- group by절은 보통 집계함수와 같이 쓰임

-- having절 부터



