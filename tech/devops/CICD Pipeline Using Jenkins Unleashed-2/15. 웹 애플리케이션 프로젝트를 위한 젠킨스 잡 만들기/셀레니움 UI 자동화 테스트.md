# 셀레니움 UI 자동화 테스트

배포한 웹 앱이 제대로 동작하는지 사람이 매번 눌러 보면 시간이 많이 든다. 이 장은 Selenium WebDriver(셀레니움 웹드라이버, 브라우저를 코드로 조종하는 도구)와 Python으로 UI 테스트를 만들어 두고, 젠킨스가 그 테스트를 대신 돌리게 한다.

이 문서는 종단 간(E-E, End-to-End) 테스트와 UI 자동화의 개념, 예제 테스트 프로젝트의 구조, 필요한 소프트웨어, 직접 실행하는 순서를 정리한다. 젠킨스 잡이 나중에 자동으로 하게 될 일을 먼저 손으로 해 보는 부분이다.

---

## 1. E-E 테스트와 UI 자동화

E-E 테스트는 사용자 입장에서 업무 흐름 전체를 따라가 보는 테스트다. 정상 흐름과 오류 흐름을 모두 돌리면서 앱이 올바르게 반응하는지 본다. 이 과정에서 앱 안의 여러 부품이 서로 잘 맞물리는지, 데이터베이스나 웹 서버, 애플리케이션 서버 같은 외부 소프트웨어와 잘 연결되는지도 함께 확인된다.

UI 자동화 테스트는 이 E-E 흐름을 도구가 대신 수행하게 하는 방식이다. 도구가 사람처럼 화면의 입력 칸과 버튼을 만지면서 시나리오를 확인한다.

| 구분 | 도구 이름 |
| --- | --- |
| 유료(상용) | UFT, TestComplete, Ranorex 등 |
| 오픈 소스 | Selenium, Protractor, WebDriver IO 등 |

이 장은 오픈 소스인 Selenium을 쓴다.

## 2. UI 자동화 도구가 일하는 방식

도구는 타이핑, 클릭, 드롭다운 선택 같은 동작을 하는 라이브러리를 갖고 있고, 우리는 지원되는 스크립트 언어로 명령을 준다. 어떤 화면 요소를 다루든 도구에는 두 가지 지시가 필요하다.

| 지시 | 설명 |
| --- | --- |
| 요소 식별 | 화면의 많은 요소 중 어느 것인지 고른다. ID, name, class 같은 고유한 속성값을 쓴다 |
| 동작 수행 | 찾은 요소에 입력, 클릭 같은 동작을 시킨다 |

택배 기사에게 "3층 301호 문 앞에 두세요"라고 알려 주는 것과 같다. 301호라는 주소가 식별이고, 문 앞에 두는 것이 동작이다.

Selenium WebDriver는 Java, C#, JavaScript, Python 등 여러 언어용 라이브러리를 제공한다. 저자는 Python 라이브러리로 `CalculatorWebApplication`의 UI 테스트를 만들었다.

## 3. 예제 테스트 프로젝트 구조

테스트 프로젝트 이름은 `TestCalculatorWebApplicationUsingSeleniumPython`이고 `D:\JenkinsBookExamples`에 있다. 원서가 짧게 소개한 주요 파일과 패키지는 다음과 같다.

| 파일 또는 패키지 | 역할 |
| --- | --- |
| `EnvVars.csv` | 경로, 애플리케이션 URL 같은 환경 설정값. chromedriver.exe 경로와 ObjectRepositories 폴더 경로, 앱 URL이 들어 있다 |
| `ObjectRepositories/CalculatorPage.csv` | UI 테스트에서 다룰 요소의 식별 정보를 모아 둔 파일 |
| `AutomationFramework` 패키지 | EnvVars.csv와 CalculatorPage.csv를 읽고 브라우저와 UI 요소를 조작하는 공통 코드 |
| `CalculatorWebApp_Pages` 패키지 | `BasePage.py`(BasePage 클래스)와 `CalculatorPage.py`(CalculatorPage 클래스) |
| `CalculatorWebApp_TestCases` 패키지 | 기능별 테스트 케이스 파일. 예: `test_AdditionFunctionality.py` |
| `Drivers` 폴더 | `chromedriver.exe`가 들어 있다 |

EnvVars.csv의 경로와 URL은 독자의 환경에 맞게 고쳐야 한다. `CalculatorPage` 클래스에는 `DoAddition()`, `DoSubtraction()` 같은 함수가 있어서 계산기 기능별 흐름을 자동으로 수행한다.

`Utils.py`의 `InitializeEnvVars()` 함수는 EnvVars.csv를 한 줄씩 읽어 이름과 값을 `Utils.EnvVars` 사전에 저장한다. 원서 Listing 15-2의 핵심은 아래와 같다. 추출 텍스트에서 긴 경로가 잘려 있어, 경로 부분은 복원한 것이다.

```python
@classmethod
def InitialiseEnvVars(cls):
    with open('D:\\JenkinsBookExamples\\TestCalculatorWebApplicationUsingSeleniumPython\\EnvVars.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            Utils.EnvVars[row[0]] = row[1]
```

CSV의 첫 열이 이름(예: `ChromeDriverPath`), 둘째 열이 값이다. 프로젝트를 `D:\JenkinsBookExamples`가 아닌 곳에 두었다면 이 경로를 고쳐야 한다. 함수 이름은 소제목에서 `InitializeEnvVars`, 코드에서 `InitialiseEnvVars`로 철자가 다르게 나오는데, 원서의 표기를 그대로 따른 것이다.

## 4. 테스트 그룹과 용어

테스트 케이스는 검사 범위에 따라 RegressionTest, SmokeTest 같은 그룹으로 묶인다. 뒤의 잡들이 이 그룹 이름을 파라미터로 받아 일부만 골라 돌린다.

| 용어 | 뜻 |
| --- | --- |
| 스모크 테스트 | 개발자에게 새 빌드를 받았을 때, 더 본격적인 테스트를 받을 최소한의 상태인지 확인하는 테스트 |
| 회귀(리그레션) 테스트 | 변경 때문에 기존 기능이 나빠지지 않았는지 확인하는 테스트 |

스모크는 "전원은 들어오나" 정도의 빠른 점검이고, 회귀는 "고친 뒤에도 예전 기능이 멀쩡한가"를 넓게 보는 점검이다.

## 5. 테스트 실행에 필요한 소프트웨어

| 소프트웨어 | 설명 |
| --- | --- |
| Python | 설치 후 PATH 환경 변수에 추가한다 |
| pip | Python 패키지 관리자. 자바의 mvnrepository.com 같은 pip 레지스트리에서 패키지를 받는다. Python 설치 폴더의 Scripts 안에 함께 설치되며 PATH에도 있어야 한다 |
| Chrome 브라우저 | 테스트가 열 브라우저 |
| Chrome Driver | Selenium 호출을 Chrome 고유의 UI 자동화 호출로 바꿔 주는 Chrome용 WebDriver 구현체. 설치된 Chrome과 호환되는 버전을 받는다 |
| Selenium Python 라이브러리 | `pip install selenium` |
| Pytest | 테스트 실행 프레임워크이며 실행 결과를 HTML 리포트로 만든다. `pip install pytest` |

Chrome Driver는 `https://chromedriver.chromium.org/downloads`에서 받는다고 원서는 안내한다. Python과 pip을 PATH에 넣는 화면은 Figure 15-4의 환경 변수 편집 창이다.

## 6. 직접 실행하는 순서

1. 명령 프롬프트를 열고 `cd`로 `TestCalculatorWebApplicationUsingSeleniumPython` 프로젝트 폴더에 들어간다.
2. 가상 환경 도구를 설치한다.

   ```text
   pip install virtualenv
   ```

3. 가상 환경을 만든다. 형식은 `virtualenv <가상환경이름>`이고, 저자는 `TestCalculatorWebApplication`이라는 이름을 썼다.

   ```text
   virtualenv TestCalculatorWebApplication
   ```

4. 가상 환경을 활성화한다.

   ```text
   TestCalculatorWebApplication\Scripts\activate
   ```

5. 가상 환경 안에서 필요한 패키지 세 개를 설치한다. 프로젝트 폴더 안에서 실행한다.

   ```text
   pip install pytest
   pip install selenium
   pip install pytest-html
   ```

6. 테스트를 실행한다.

   ```text
   pytest --html=TestsResult.html
   ```

7. 현재 폴더에 생긴 `TestsResult.html`을 열어 결과를 본다.

`pytest`는 이름이 `test_`로 시작하는 파일 안에서 `test`로 시작하는 함수를 찾아 실행하고, 결과를 `--html`로 지정한 파일에 담는다. 실행이 시작되면 브라우저 캐시를 먼저 지운 뒤, 브라우저를 열어 계산기 앱을 직접 눌러 본다.

## 7. 가상 환경을 쓰는 이유

가상 환경은 프로젝트 전용 파이썬 환경이다. 시스템 전체에 깔린 파이썬을 쓰지 않고 별도 공간을 만든다.

| 이점 | 설명 |
| --- | --- |
| 라이브러리 격리 | 필요한 버전의 Selenium, pytest 등을 다른 프로젝트에 영향을 주지 않고 설치한다 |
| 이식성 | 자동화 테스트용 라이브러리를 기계마다 들고 다닐 필요가 없다 |
| 젠킨스 자동화 | 코드를 받아 온 뒤 젠킨스 잡이 가상 환경 생성, 라이브러리 설치, 테스트 실행을 사람 손 없이 처리한다 |

이 마지막 이점 때문에 뒤에 나오는 TestCalculatorWebApplication 잡은 가상 환경을 만드는 단계로 시작한다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
