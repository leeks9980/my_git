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
-- sum(): 합계, avg(): 평균, min(): 최소값, max(): 최대값, count(): 행의 개수, count(distnct): 행의 개수(중복 1개만 인정)

select mem_id '회원 아이디', sum(amount *price) '총 구매 금액' from buy
	group by mem_id
    having sum(amount * price) >= 1000; -- 집계 합수 사용시 where절 대신 having절 사용
    
-- 과제
select mem_id, sum(amount*price) from buy
	group by mem_id
    having sum(amount * price) >= 1000
    order by sum(amount * price); 

USE market_db;
CREATE TABLE toy (toy_id INT, toy_name CHAR(5), age INT); -- 테이블 생성

insert into toy values (1000, '스파이더맨', 7); -- 값 추가
insert into toy(toy_name, age) values ('아이언맨', 7); -- 원하는 값만 선택해서 출력
INSERT INTO toy (age, toy_name, toy_id) VALUES (5, '티니핑', 1001); -- 순서를 바꿔서 값 입력

CREATE TABLE toy2 (toy_id INT AUTO_INCREMENT PRIMARY KEY,  -- AUTO_INCREMENT자동으로 숫자 증가, PRIMARY KEY 기본키로 지정
	toy_name CHAR(5),
	age INT);

INSERT INTO toy2 VALUES (NULL,'우디', 8);
INSERT INTO toy2 VALUES (NULL,'버즈', 9);
INSERT INTO toy2 VALUES (NULL,'제시', 8);

ALTER TABLE toy2 AUTO_INCREMENT=100; -- 다음부터 입력되는 값을 100부터 시작
INSERT INTO toy2 VALUES (NULL, "슬링키", 10);

ALTER TABLE toy2 AUTO_INCREMENT=1000; -- 다음부터 입력되는 값을 1000부터 시작
SET @@auto_increment_increment = 3; -- 다음부터 3씩 증가

INSERT INTO toy2 VALUES (NULL,'우디', 8);
INSERT INTO toy2 VALUES (NULL,'버즈', 9);
INSERT INTO toy2 VALUES (NULL,'제시', 8);
select * from toy2;

use world_db;
SELECT count(*) from world_db.city;
SELECT * from city LIMIT 5;
DESC city;

-- INSERT
CREATE TABLE japan (city_name VARCHAR(40), population INT);
INSERT INTO japan SELECT dest, population FROM city WHERE country= "Japan";  -- city 테이블의 country열이 'japan'인 dest,population을 입력한다

-- update
update japan set city_name = '도쿄' where city_name = 'Tokyo'; -- japan테이블에서 city_name이 'Tokyo'인 값을 '도쿄' 업대이트함
select * from japan; 

update japan set city_name='나고야', population = 0 where city_name = 'Nagoya'; -- 원하는 열을 찾고 그 열값을 지정해 업데이트 가능
select * from japan;

update japan set city_name='서울'; -- where절이 없으면 모든 깂을 전부 업데이트 함

UPDATE city SET population = population/10000; -- where절 없이 사용하는 경우(10,000명 단위로 인구수 수정)
select * from city;

-- delete
select * from city where country like 'New%';
delete from city where country like 'New%'; -- delete문은 원하는 값을 삭제하는 문이다(New으로 시작하는 나라이름 값을 삭제함)

-- 과제
select * from city where country_iso = 'AF' limit 5;
delete from city where country_iso = 'AF' limit 5;

-- 데이터 형식
-- 정수형
-- tinyint 1바이트 -128 ~ 127
-- smallint 2바이트 -32,768 ~ 32,767
-- int 4바이트 약 -21억 ~ 21억
-- bigint 8바이트 약 -900경 ~ 900경

use market_db;
create table test (   -- 데이터 형식을 확인하기 위한 테이블
	tiny_int tinyint,
    small_data smallint,
    int_data int,
    big_int bigint);

INSERT INTO test VALUES (127, 32676, 2147483647, 9000000000000000000); -- 테이블에 값 넣기
select * from test;
INSERT INTO test VALUES (128, 32677, 2147483648, 9000000000000000001); -- 을 실행 하면 값이 범위를 넘어가면 오류 발생

-- 문자형
-- char(최대 글자수), 1 ~ 255 바이트, 고정 길이 문자형
-- varhar(최대 글자수), 1 ~ 16383 바이트, 가변 길이 문자형
-- text, 1 ~ 65535바이트
-- longtext, 1 ~ 4294967295바이트
-- blob, 1 ~ 65535바이트
-- longblob, 1 ~ 4294967295바이트

-- 실수형
-- float, 4바이트, 소주점 아래 7자리까지 표현
-- double, 8바이트, 소수점 아래 15자리까지 표현

-- 변수 지정
set @myvar = 10; -- 변수 선언 및 값 대입
select @myvar; -- 변수 호출

select mem_name, height from member order by height limit @myvar; -- limit에는 변수를 넣을수 없음

-- join문
select * from buy b -- b은 buy의미
	inner join member m -- m은 member의미
    on b.mem_id = m.mem_id  -- 같은 행으로 조인 하겠다
    where b.mem_id ='GRL';

select * from buy b 
	inner join member m 
    on b.mem_id = m.mem_id; -- where절을 뺴면 모든 행 조인

select mem_id, mem_name, prod_name, addr, concat(phone1, phone2) '연락처' from buy -- mem_id가 두개의 테이블에 중복으로 있어
	inner join member
    on buy.mem_id = member.mem_id;
    
select buy.mem_id, mem_name, prod_name, addr, concat(phone1, phone2) '연락처' from buy -- mem_id가 어느 테이블에서 쓸건지 지정 해줘야함
	inner join member
    on buy.mem_id = member.mem_id;






