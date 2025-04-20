-- 관계 연산자(>, <, >=, <=, =)
select * from member where height >= 162; --키가 162과 같거나 큰
select * from member where height <= 162; --키가 162과 같거나 작은
select * from member where height < 162;  --키가 162보다 작은
select * from member where height > 162;  --키가 162보다 큰
select * from member where height = 162;  --키가 162와 같은

-- 논리 연산자(or, and)
select * from member where height >= 162 and mem_number > 8;  -- 두가지 조건 모두
select * from member where height >= 162 or mem_number > 8;   -- 둘중 한가지 조건에 충족되면

-- between ~ and
SELECT * FROM member WHERE height >= 163 AND height <= 165; --논리 연산자를 사용해 같은 문장을 만들수 있음
SELECT * FROM member WHERE height BETWEEN 163 AND 165; -- 두값 사이에 있는 값만 출력

-- in()
SELECT * FROM member WHERE addr IN ('경기' , '전남' , '경남');   -- 문자형 데이터는 범위를 지정할수 없기 떄문에 사용
SELECT * FROM member WHERE addr = '경기' OR addr = '전남' OR addr = '경남' ; -- 깉은 기능의 문장

-- like
select * from member where mem_name like '엔%';   -- like는 열에서 원하는 값을 찾아줌, '엔%'은 '엔'뒤에 무엇이든 허용
select * from member where mem_name like '엔%';  -- 반대로 사용가능_'엔%' '엔'앞에는 무엇이든 허용

select * from member where mem_name like '__핑크';  -- '__핑크'는 핑크 앞에 2글자가 들어간다 라는 의미 
select * from member where mem_name like '블랙__';  -- '_'는 어디든(중간) 들어갈수 있음
select * from member where mem_name like '블_핑_';

-- 서브 쿼리
SELECT * FROM member
    WHERE height > (SELECT height FROM member WHERE mem_name = '에이핑크');  -- select문 안에 다른 select문이 들어갈수 있음

-- insert문
insert into toy values (1000, '스파이더맨', 7);  -- 테이블명 뒤에 열 이름 생략 가능(생략 하면 순서 및 개수를 테이블 정의 할때 열 순서대로 해줘야함)
insert into toy(toy_name, age) values ('스파이더맨', 7); -- 열 이름을 지정해주면 지정해준 열로 값이 들어감
insert into toy(age, toy_name) values (7, '스파이더맨'); -- 열 순서를 바꾼다면 값의 순서도 따라서 변경해주면 됨

-- Auto_increment
CREATE TABLE toy2 (toy_id INT AUTO_INCREMENT PRIMARY KEY,  -- 만약 열을 AUTO_INCREMENT으로 지정 했다면 PK(기본키)로 지정 해야함
    toy_name CHAR(5),
    age INT);

INSERT INTO toy2 VALUES (NULL,'우디', 8);
INSERT INTO toy2 VALUES (NULL,'버즈', 9);
INSERT INTO toy2 VALUES (NULL,'제시', 8);  -- toy_id값을 auto_increment으로 지정했다면 null값이 들어가도 자동으로 1부터 값을 넣음

-- select into ~ select
INSERT INTO japan SELECT dest, population FROM city WHERE country= "Japan"; --select into ~ select를 사용해서 다른 테이블 값을 가져올수 있다

-- update
UPDATE japan SET city_name = "도쿄" WHERE city_name = "Tokyo";  -- 테이블의 원하는 값을 지정한 다른 값으로 변경할수 있다
UPDATE japan SET city_name = "도쿄";  -- where를 생략하면 지정한 열의 모든 값을 변경함 

update city set population = population/10000; -- where 없이 쓰는 경우(인구수를 10,000단위로 수정, 모든 열값에 대해 수정을 원할떄)

-- 제약 조건
-- Primary Key: 테이블은 기본키 1개만 가질수 있고  입력값은 중복,NULL값을 가질수 없다
-- Foreign Key: 참조 하려는 값은 항상 기준 테이블에서 기본키, 고유키 으로 설정 되있어야함
-- Unique: 기본키와 비슷하지만 NULL값을 허용
-- Check: 입력된 데이터를 점검
ALTER TABLE member ADD CONSTRAINT CHECK (phone1 IN ('02','031','063'));  -- '02','031','063' 값 외 다른 값이 들어오면 오류가 남
-- Default: 값을 입력하지 않았을떄 NULL값 대신 지정된 값이 들어감
-- NULL 값 허용: NULL은  공백, 0과 다름 값이 없음을 의미함

--외부 조인(outer join): 선택된 테이블을 기준으로 여집합
select m.mem_id, m.mem_name, b.prod_name, m.addr from buy b  
    left outer join member m  -- buy테이블에 member테이블을 외부 조인 하겠다
    on m.mem_id = b.mem_id
    order by m.mem_id;  -- 출력값은 buy테이블 전부와 member테이블에서 buy테이블과 같은 값이 있는 항목만 가져옴

select m.mem_id, m.mem_name, b.prod_name, m.addr from buy b  
    right outer join member m  -- member테이블에 buy테이블을 외부 조인 하겠다
    on m.mem_id = b.mem_id
    order by m.mem_id;  -- 위의 출력값과 정반대의 출력값을 가지고 감

-- 내부 조인(inner join): 2개의 테이블 간의 교집합
SELECT b.mem_id, m.mem_name, b.prod_name, m.addr FROM buy b
    INNER JOIN member m 
    ON b.mem_id = m.mem_id
    ORDER BY b.mem_id;  -- 출력값은 member테이블과 buy테이블에서 서로 같은 값만 출력