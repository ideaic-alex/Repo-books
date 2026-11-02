# 저장 프로시저와 SQL 최적화

SQL에서 한 걸음 더 나가면 저장 프로시저와 성능 최적화가 나온다. 저장 프로시저는 미리 준비해 저장해 두고 반복해서 부르는 SQL 코드이고, 최적화는 같은 결과를 더 빠르게 얻도록 코드를 고치거나 인덱스를 추가하는 일이다. 이 문서는 Copilot이 둘 모두에서 어떻게 도움이 되는지를 본다.

앞 문서와 같은 대학 수강 등록 스키마를 컨텍스트로 쓴다.

---

## 1. 저장 프로시저 만들기

채팅에 주석 대신 평범한 문장으로 요청해도 된다. 예를 들어 "define a stored procedure to get course enrollment by location."이라고 입력하면, 스키마를 컨텍스트로 삼아 쓸 만한 결과를 준다.

```sql
CREATE PROCEDURE GetCourseEnrollmentByLocation
    @CourseID INT
AS
BEGIN
    SELECT students.city, students.state, COUNT(*) AS enrollment_count
    FROM courses.students
    JOIN courses.registrations
    ON students.student_id = registrations.student_id
    JOIN courses.registration_items
    ON registrations.registration_id = registration_items.registration_id
    WHERE registration_items.course_id = @CourseID
    GROUP BY students.city, students.state;
END
```

강좌 번호를 `@CourseID` 매개변수로 받고, 학생의 도시와 주별로 등록 인원을 센다. 요청이 짧아도 매개변수와 집계 방식을 알아서 정한 셈이다. 다만 "location"을 학생의 도시와 주로 해석했다는 점은 사람이 확인해야 한다. 스키마에는 별도의 `location_id`가 있어서 의도와 다를 수 있다.

## 2. 프롬프트를 구체적으로 쓰면 결과가 좋아진다

프롬프트가 구체적일수록 더 나은 결과가 나온다. 책은 다음처럼 입력 매개변수와 포함할 정보를 모두 지정한 예를 든다.

```text
define a stored procedure to get instructor details associated with
a location include instructor details, location details, and courses
associated with the instructor use instructor_id as the input parameter
```

Copilot은 코드를 바로 내놓지 않고 먼저 계획(Plan)을 설명한 뒤 SQL을 만들었다. 계획은 다섯 단계였다.

| 단계 | 내용 |
| --- | --- |
| 1 | `GetInstructorDetailsByLocation`라는 새 저장 프로시저를 정의한다 |
| 2 | `@InstructorID`를 입력 매개변수로 받는다 |
| 3 | 강사 정보, 위치 정보, 강사와 연결된 강좌를 조회한다 |
| 4 | `instructors`, `locations`, `courses` 테이블을 적절한 조인으로 묶는다 |
| 5 | 강사와 위치 정보 기준으로 결과를 그룹화한다 |

이어서 나온 SQL 코드는 핵심만 보면 이런 모양이다.

```sql
CREATE PROCEDURE GetInstructorDetailsByLocation
    @InstructorID INT
AS
BEGIN
    SELECT instructors.instructor_id, instructors.first_name,
        instructors.last_name, instructors.email,
        locations.city, locations.state, courses.course_id, courses.course_name
    FROM courses.instructors
    JOIN courses.locations ON instructors.location_id = locations.location_id
    JOIN courses.course_instructors
    ON instructors.instructor_id = course_instructors.instructor_id
    JOIN courses.courses ON course_instructors.course_id = courses.course_id
    WHERE instructors.instructor_id = @InstructorID;
END;
```

강사 테이블과 위치 테이블을 조인하고, 강사와 강좌를 잇는 `course_instructors`를 거쳐 `courses`까지 연결했다. 프롬프트가 요구한 세 가지 정보(강사, 위치, 강좌)가 모두 결과 열에 들어 있다.

참고로 계획의 5단계는 그룹화를 말하지만, 실제 코드에는 `GROUP BY`가 없다. 계획과 코드가 어긋날 수 있으므로 생성된 코드를 읽고 확인하는 습관이 필요하다.

| 프롬프트 | 결과 특징 |
| --- | --- |
| 짧은 요청 ("get course enrollment by location") | 매개변수와 집계 방식을 Copilot이 추정한다 |
| 구체적 요청 (입력 매개변수, 포함할 정보까지 지정) | 계획을 먼저 보여 주고 요구한 열을 모두 담는다 |

## 3. 최적화의 두 가지 방식

Copilot은 만들어 둔 코드를 더 효율적으로 만드는 일도 돕는다. 크게 두 방식이다.

| 방식 | 설명 | 이 장의 예 |
| --- | --- | --- |
| 최적화용 구성 요소로 새 코드 쓰기 | 언어나 프레임워크가 제공하는 내장 최적화 장치를 활용하는 코드를 만든다 | 인덱스 생성 |
| 기존 코드 최적화 | 이미 있는 코드를 같은 결과를 내는 더 효율적인 코드로 바꾼다 | 날짜 조건 다시 쓰기 |

## 4. 인덱스 만들기

SQL에는 연산을 빠르게 하는 인덱스(색인)가 있다. 앞서 만든 "강좌에 등록한 모든 학생" 쿼리를 열어 둔 상태에서 주석으로 요청한다.

```sql
-- write an index to improve the performance of the query
```

Copilot은 다음과 같은 SQL을 제안할 수 있다.

```sql
create index idx_registration_status_date on courses.registrations
(registration_status, registration_date);
```

앞의 쿼리와 마찬가지로 현재 열려 있는 코드를 컨텍스트로 삼아 기존 테이블 이름과 칼럼 이름을 썼다. 제안일 뿐이므로, 이 인덱스가 정말 해당 쿼리에 도움이 되는지는 쿼리의 조건 칼럼과 대조해 보는 것이 좋다. 예를 들어 이 쿼리의 WHERE 조건은 `registration_items.course_id`인데, 제안된 인덱스는 `registrations`의 상태와 날짜 칼럼에 걸려 있다.

## 5. 기존 쿼리 최적화

두 번째 방식은 이미 있는 쿼리를 고치는 것이다. 2024년 9월의 수강 등록을 모두 가져오는 쿼리가 있다고 하자.

```sql
select * from courses.registrations where year(registration_date) = 2024 and month(registration_date) = 9;
```

이 쿼리를 선택하고 채팅에 "optimize this query"라고 요청한다. Copilot은 연도와 월을 뽑아내는 대신 시작일과 종료일을 직접 비교하는 쿼리를 제안한다.

```sql
SELECT * FROM courses.registrations WHERE registration_date >= '2023-09-01' AND registration_date < '2023-10-01'
```

책에 실린 제안의 날짜는 2023년으로 되어 있어서 원래 쿼리의 2024년과 어긋난다. 제안을 그대로 쓰지 말고 날짜 값이 의도와 맞는지 직접 확인해야 한다는 좋은 예다.

Copilot은 같은 응답에서 왜 이 방식이 낫다고 보는지도 설명했다. 요지는 WHERE 절에서 칼럼에 함수를 씌우면 인덱스를 쓰지 못해 쿼리가 느려질 수 있다는 것이다. `registration_date`에 인덱스가 있다면 `YEAR()`와 `MONTH()` 함수를 피하고 날짜 범위로 비교하는 쪽이 낫다는 말이다.

| 비교 | 원래 쿼리 | 최적화 제안 |
| --- | --- | --- |
| 조건 방식 | `year()`와 `month()` 함수로 칼럼을 가공 | 날짜 범위(이상, 미만)로 직접 비교 |
| 인덱스 활용 | 칼럼에 함수가 걸려 인덱스를 못 쓸 수 있다 | `registration_date`에 인덱스가 있으면 쓸 수 있다 |

Copilot이 제안만 한 것이 아니라 왜, 어떤 조건에서 최적화가 되는지까지 알려 준다는 점이 쓸모 있다. "인덱스가 있다면"이라는 전제가 붙은 이유를 이해하면 다른 쿼리에도 같은 원리를 적용할 수 있다.

## 6. 정리

- 저장 프로시저는 채팅에 문장으로 요청하며, 요청이 구체적일수록 결과가 낫다.
- 구체적 요청에는 Copilot이 계획을 먼저 보여 주기도 하지만, 계획과 코드가 어긋나지 않았는지 읽어 본다.
- 최적화는 인덱스 같은 내장 장치를 쓰는 방식과, 기존 코드를 고치는 방식 두 가지다.
- 날짜나 이름 같은 값이 제안에서 바뀌어 나오기도 하므로 반드시 확인한다.

<br>
<br>
<br>

[Learning GitHub Copilot](../)
