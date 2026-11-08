# Python-Jenkins로 제어하기

curl은 REST API를 확인하기엔 좋지만, 프로그램 안에서 결과를 가공하며 쓰려면 번거롭다. 이때 언어별 래퍼(wrapper, REST 호출을 그 언어의 함수와 객체로 감싼 라이브러리)를 쓴다. 래퍼를 쓰면 응답이 그 언어의 변수 형태로 바뀌어 돌아온다. 자바 래퍼라면 자바 객체로, 파이썬 래퍼라면 딕셔너리나 문자열로 받아 평소 다루던 방식 그대로 쓸 수 있다.

이 문서는 파이썬 래퍼 중 Python-Jenkins로 앞의 실습과 같은 일을 하는 방법을 정리한다. 책은 Ruby나 Java 래퍼도 선호에 따라 써 볼 수 있다고 언급만 하고 다루지 않는다.

---

## 1. 파이썬 래퍼 종류와 준비물

책이 소개하는 파이썬 래퍼는 JenkinsAPI, Python-Jenkins, api4jenkins, aiojenkins 네 가지다. 모두 객체지향 방식으로 Jenkins를 파이썬답게 제어하게 해 준다. 책은 이 중 Python-Jenkins를 쓴다.

| 준비물 | 설명 |
|---|---|
| Python 인터프리터 | `https://www.python.org/downloads/`에서 알맞은 버전을 내려받는다 |
| PyCharm | 파이썬 코드 편집기. 프로페셔널 버전(30일 무료 체험)이나 무료인 커뮤니티 에디션 |
| Python-Jenkins 패키지 | Pip와 Python을 PATH에 등록한 뒤 설치 |

Pip와 Python을 PATH 환경 변수에 넣는 방법은 책의 15장에서 설명했다고 한다. PATH에 Pip가 잡혀 있으면 다음 명령으로 설치한다.

```
pip install Python-jenkins
```

---

## 2. 예제 코드 둘러보기

책은 PyCharm에 파이썬 프로젝트를 만들고 `WorkingWithJenkinsJobs.py` 파일에 코드를 작성했다. 코드는 Listing 20-1부터 20-9까지 조각으로 나뉜다. 한 파일에 위에서부터 이어 붙인 것이다.

### 서버에 연결하기

```python
import jenkins
server = jenkins.Jenkins('http://192.168.43.10:8080', username="Pranodayd", password="<API토큰>")
```

`jenkins.Jenkins(...)`는 클래스 생성자를 호출하는 코드다. Jenkins 서버 URL, 사용자 이름, 비밀번호를 넘기면 서버 인스턴스를 다룰 수 있는 참조 변수 `server`가 만들어진다. 이후 모든 호출은 이 변수를 통한다. 책에서는 password 자리에 curl과 같은 API 토큰을 쓴 것으로 보인다(원문 추출본에서 값이 잘려 정확한 값은 확인되지 않는다).

### 로그인한 사용자 정보 얻기

```python
user = server.get_whoami()
version = server.get_version()
print('Hello %s from Jenkins %s' % (user['fullName'], version))
```

`get_whoami()`는 현재 로그인한 사용자 정보를, `get_version()`은 서버 버전을 돌려준다. 위 코드는 이름과 버전을 함께 출력한다.

### 기존 잡 설정 가져오기와 새 잡 만들기

```python
DemoJobConfiguration = server.get_job_config("Demo")
server.create_job('JobCreatedUsingPythonJenkins', DemoJobConfiguration)
```

첫 줄은 Demo 잡의 설정 XML을 변수에 담는다. 둘째 줄은 `create_job`으로 그 설정을 이용해 새 잡 JobCreatedUsingPythonJenkins를 만든다. 책에서는 이 생성 코드를 작은따옴표 세 개(`'''`)로 감싸 주석 처리한 형태로 보여 준다. 파이썬에서 이 문법은 여러 줄 문자열이라 사실상 주석처럼 쓰인다.

### 전체 잡 목록 보기

```python
jobs = server.get_jobs()
print(jobs)
```

모든 잡의 정보를 가져온다. 잡 하나하나는 딕셔너리(키와 값 쌍) 객체이고 `name`, `url`, `color`, `fullname` 키를 가진다.

### 잡 실행하기

```python
server.build_job('ReleaseCalculatorAPI')
```

파라미터가 없는 잡의 빌드를 시작한다.

```python
server.build_job('BuildAndDeployCalculatorWebApplication',
  {'CalculatorWebApplicationDeploymentDirectory': 'D:\\JenkinsBookExamples\\DeployedCalculatorWebApp\\',
   'TypeOfTestsToRun': 'AllTests'})
```

파라미터가 있는 잡이다. `build_job`의 첫 인자는 잡 이름, 둘째 인자는 파라미터를 `이름: 값`으로 담은 딕셔너리다. 경로의 역슬래시는 파이썬 문자열에서 `\\`로 두 번 써야 한다.

### 잡 삭제와 마지막 빌드 번호 조회

```python
server.delete_job('JobCreatedUsingPythonJenkins')
last_build_number = server.get_job_info('BuildAndDeployCalculatorWebApplication')['lastCompletedBuild']['number']
```

첫 줄은 앞에서 만든 잡을 지운다. 둘째 줄은 잡 정보에서 `lastCompletedBuild`(마지막으로 끝난 빌드)의 `number`(빌드 번호)를 꺼낸다.

책에서는 둘째 줄이 지면 때문에 두 줄로 나뉘어 있지만 실제로는 한 줄 코드다.

---

## 3. 함수 한눈에 정리

| 하려는 일 | curl 방식 | Python-Jenkins 함수 |
|---|---|---|
| 서버에 연결 | `-u 사용자:토큰` | `jenkins.Jenkins(url, username, password)` |
| 로그인 사용자 확인 | 다루지 않음 | `get_whoami()` |
| 서버 버전 확인 | 다루지 않음 | `get_version()` |
| 잡 설정 조회 | GET `config.xml` | `get_job_config("잡")` |
| 잡 생성 | POST `createItem` | `create_job("이름", 설정)` |
| 전체 잡 목록 | 다루지 않음 | `get_jobs()` |
| 일반 잡 빌드 | POST `/build` | `build_job("잡")` |
| 파라미터 잡 빌드 | POST `/buildWithParameters` | `build_job("잡", {딕셔너리})` |
| 잡 삭제 | 다루지 않음 | `delete_job("잡")` |
| 마지막 빌드 번호 | 다루지 않음 | `get_job_info("잡")['lastCompletedBuild']['number']` |

curl에서는 파라미터 유무에 따라 주소가 달랐는데, Python-Jenkins에서는 같은 `build_job` 함수에 딕셔너리를 줄지 말지로 구분한다. 표에서 curl 칸이 비어 있는 항목은 책이 curl로는 보여 주지 않은 기능이라는 뜻이며 curl로 불가능하다는 뜻은 아니다.

---

## 4. 예제 코드 저장소

책 저자는 이 파이썬 프로젝트 전체를 GitLab 공개 저장소 `https://gitlab.com/Pranoday/python_jenkins.git`에 올렸다고 밝힌다. 전체 흐름을 한 번에 확인하고 싶으면 이 저장소를 참고하면 된다.

## 5. 실습 순서 정리

1. Python, PyCharm을 설치하고 Pip를 PATH에 등록한다.
2. `pip install Python-jenkins`로 패키지를 설치한다.
3. PyCharm에서 프로젝트와 `WorkingWithJenkinsJobs.py`를 만든다.
4. `jenkins.Jenkins(...)`로 서버에 연결한다.
5. 필요한 API(`get_job_config`, `create_job`, `build_job` 등)를 차례로 호출한다.
6. Jenkins 대시보드에서 잡이 생기고 빌드가 도는지 확인한다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
