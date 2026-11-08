# SSH로 복제하고 곱셈 기능 올리기

키 등록을 마친 새 개발자는 이제 실제 개발 작업에 들어간다. 저장소를 SSH 주소로 복제하고, CalculatorAPI에 곱셈(Multiplication) 기능을 넣고, 단위 테스트를 만들고, 버전을 3.0으로 올린 뒤, 새 브랜치를 원격 저장소에 올려 병합 요청(merge request)을 만든다. 이 문서는 그 전체 개발 흐름을 정리한다.

이 흐름은 뒤에서 만들 자동 트리거 잡이 어떤 변경을 감지하는지 이해하는 바탕이기도 하다. 한 가지 눈여겨볼 점은 병합 요청을 만들어 놓고도 마지막 Merge 버튼은 누르지 않는다는 것이다. 이유는 마지막 절에서 설명한다.

---

## 1. 단계 1: 저장소 복제하기

이 개발자는 이 저장소에 처음 기여하므로 원격 저장소 전체를 자기 컴퓨터로 가져와야 한다. 이 작업이 복제(clone)이다. 복제는 소스 코드 파일뿐 아니라 커밋 이력까지 저장소 전체를 내려받는다.

복제하기 전에 한 가지 준비가 필요하다. 개인 키가 기본 위치(`$(user.name)\.ssh` 폴더)에 있으면 바로 `git clone`을 실행해도 된다. 그런데 원서는 키를 `D:\SSHKeys\MyGitlabKeys`에 따로 만들었으므로, SSH 클라이언트가 이 키를 쓰도록 아래 세 가지 방법 중 하나를 골라야 한다.

| 방법 | 어디에 설정하나 | 성격 |
| --- | --- | --- |
| 옵션 1 | known_hosts 파일에 도메인과 키 등록 | 한 번 접속해서 등록 |
| 옵션 2 | .ssh 폴더의 config 파일 | 호스트별 설정 파일 |
| 옵션 3 | Git 전역 설정 core.sshCommand | 명령 한 줄 |

원서는 세 방법을 모두 설명한다. 하나만 하면 되고, 원서는 이 중 어느 것이 가장 낫다고 권하지 않았다. 각 방법을 차례로 본다.

### 옵션 1: known_hosts에 개인 키 등록

개인 키 파일을 지정해서 gitlab.com에 한 번 접속하면 기록이 남는다. 원서에는 `ssh –I`로 적혀 있는데, 키 파일을 지정하는 옵션은 소문자 `-i`이므로 추출 과정의 오류로 보고 바로잡았다.

```
ssh -i D:\SSHKeys\MyGitlabKeys git@gitlab.com
```

1. 위 명령을 실행하면 "Are you sure you want to continue connecting (yes/no/[fingerprint])?"라고 묻는다. yes를 입력하고 Enter를 누른다.
2. passphrase를 물으면 키를 만들 때 정한 암호를 입력한다.
3. GitLab이 개인 키로 사용자를 인증했다는 메시지가 나오면 성공이다.
4. `$(user.name)\.ssh` 폴더에 known_hosts 파일이 생긴다. 열어 보면 git@gitlab.com 도메인에 대응해 등록된 내용이 있다.

이제 바로 저장소를 복제할 수 있다. 원서는 설명 과정에서 "known_hosts 파일에서 개인 키를 보내 준다"고 적었지만, 실제 known_hosts는 접속한 서버를 기록하는 파일이라서 이 서술은 엄밀하지 않을 수 있다. 원문 표현을 따르되 불확실한 해석임을 밝혀 둔다.

### 옵션 2: config 파일에 키 파일 지정

1. `.ssh` 폴더로 이동한다. 원서에서는 `C:\Users\magicuser\.ssh`이다.
2. 폴더에서 마우스 오른쪽 버튼을 눌러 Git Bash Here를 선택하면 Git Bash가 열린다.
3. `touch config` 명령으로 config 파일을 만든다.
4. 메모장으로 config 파일을 열어 다음 내용을 입력하고 저장한다.

```
# GITLAB
Host gitlab.com
   HostName gitlab.com
   PreferredAuthentications publickey
   IdentityFile D:\SSHKey\MyGitlabKeys
```

`Host`는 이 설정이 적용될 접속 대상 이름이다. `PreferredAuthentications publickey`는 공개 키 방식을 우선 쓰라는 뜻이고, `IdentityFile`은 사용할 개인 키 파일의 경로이다. 코드 속 경로는 원서 예시를 그대로 옮겼으므로, 자기 키 경로로 바꿔 써야 한다.

### 옵션 3: Git 전역 설정에 SSH 명령 지정

명령 프롬프트에서 다음 명령을 실행하면 Git 전역 설정 파일에 개인 키 파일이 기록된다.

```
git config --global core.sshCommand "ssh -i D:\\SSHKey\\MyGitlabKeys -F /dev/null"
```

`-i`는 사용할 키 파일을 가리키고, `-F /dev/null`은 다른 SSH 설정 파일을 읽지 않겠다는 뜻이다. 이 풀이는 일반적인 SSH 옵션 의미에 따른 것이며 원서는 설명하지 않았다.

## 2. SSH 주소로 복제 실행

준비가 끝났으면 저장소의 SSH 주소를 얻어 복제한다.

1. GitLab 저장소 페이지에서 Clone 버튼을 누른다.
2. Clone with SSH 항목의 Copy URL 버튼을 눌러 주소를 복사한다.
3. D: 드라이브에 NewDeveloper라는 빈 폴더를 만들고, 명령 프롬프트에서 `cd`로 `D:\NewDeveloper`로 이동한다.
4. 다음 명령을 실행한다.

```
git clone git@gitlab.com:Pranoday/jenkinsbookcalculatorapi.git
```

처음 접속하면 SSH 클라이언트가 gitlab.com을 아직 모르는 호스트로 보고 확인을 묻는다. yes를 입력하면 gitlab.com이 `.ssh` 폴더의 known_hosts 파일에 추가된다. 이어서 passphrase를 입력하면 프로젝트가 복제된다. 옵션 1을 이미 했다면 gitlab.com이 known_hosts에 들어 있으므로 이 확인 질문은 나오지 않는다.

## 3. 단계 2: Calculator 클래스에 곱셈 함수 추가

복제한 프로젝트를 Eclipse에서 연다. 원서는 빈 작업 공간(workspace)을 만들고 복제한 Maven 프로젝트를 가져온다.

1. Eclipse에서 File → Import를 선택한다.
2. Maven 항목의 Existing Maven Projects를 선택하고 Next를 누른다.
3. Root Directory 입력란에 복제한 프로젝트 경로를 넣고 Finish를 누른다.

Calculator.java 파일에 다음 메서드를 추가한다.

```java
public int Multiplication(int num1,int num2)
{
      int Res=num1*num2;
      return Res;
}
```

두 정수를 곱해서 결과를 돌려주는 단순한 메서드다. 지난 장까지 있던 덧셈(Addition)과 뺄셈(Subtraction) 옆에 곱셈이 늘어난다.

## 4. 단계 3: 곱셈 함수의 단위 테스트 추가

원서는 src/test/java의 Pranodayd.CalculatorAPI 패키지 안에 TestMultiplicationFunctionality.java 파일을 만들었다(Listing 13-1). TestNG를 쓰며, 핵심 구조는 아래와 같다.

```java
public class TestMultiplicationFunctionality
{
      Calculator Cal;
      int Result;
      @BeforeClass
      public void Init() { Cal=new Calculator(); }
      @BeforeMethod
      public void ReinitialisingResult() { Result=0; }
}
```

위는 클래스의 뼈대이고, 이 클래스 안에 들어가는 테스트 메서드는 다음과 같다.

```java
      @Test(priority=1,dataProvider="ProvidePositiveIntegerValues",
            groups={"RegressionTest"})
      public void TestMultiplicationWithPositiveValues(
            int Number1,int Number2,int ExpectedResult)
      {
            Result=Cal.Multiplication(Number1, Number2);
            Assert.assertEquals(Result, ExpectedResult);
      }
```

원문의 assertEquals에는 실패 시 보여 줄 메시지 인자가 하나 더 있고(양수에서 곱셈이 동작하지 않는다는 취지), 위 코드는 지면상 생략했다. 테스트 데이터는 `@DataProvider`가 `ProvidePositiveIntegerValues`라는 이름으로 공급한다.

| 세트 | 첫째 수 | 둘째 수 | 기대 결과 |
| --- | --- | --- | --- |
| SET 1 | 1 | 2 | 2 |
| SET 2 | 10 | 20 | 200 |
| SET 3 | 1000 | 2000 | 2000000 |
| SET 4 | 100 | 200 | 20000 |

테스트가 세트마다 한 번씩, 총 네 번 실행된다. 원서의 코드 안 주석 중 SET 4 줄은 SET 3과 같은 값(1000,2000,2000000)으로 잘못 적혀 있으나, 실제 배열에 넣는 값은 표와 같다.

| 어노테이션 | 역할 |
| --- | --- |
| `@BeforeClass` | 클래스 시작 때 한 번, Calculator 객체 생성 |
| `@BeforeMethod` | 각 테스트 전에 Result를 0으로 초기화 |
| `@Test` | 테스트 메서드 표시. priority와 groups 지정 |
| `@DataProvider` | 테스트에 넣을 값 묶음 제공 |

## 5. 단계 4: pom.xml 버전을 3.0으로 변경

곱셈 기능을 넣은 CalculatorAPI.jar를 3.0 버전으로 릴리스하려고 한다. pom.xml에서 버전을 2.0에서 3.0으로 바꾼다(Listing 13-2).

```xml
<groupId>Pranodayd</groupId>
<artifactId>CalculatorAPI</artifactId>
<version>3.0</version>
```

이 버전 값이 곧 Nexus에 올라가는 JAR 이름의 버전이 된다. 뒤에서 `CalculatorAPI3.0.jar`가 배포되는 것도 이 값 때문이다.

## 6. 단계 5: 단위 테스트와 회귀 테스트

`mvn test`를 실행해서 모든 단위 테스트를 돌린다. 새로 만든 곱셈 함수가 잘 동작하는지, 그리고 이전에 만든 덧셈과 뺄셈 기능이 망가지지 않았는지(회귀 테스트, regression test) 한꺼번에 확인한다.

1. 명령 프롬프트에서 `cd`로 프로젝트 폴더로 이동한다.
2. `mvn test`를 실행한다.
3. 모든 테스트 케이스가 통과했는지 확인한다.

## 7. 단계 6, 7: 브랜치를 만들어 커밋하고 올리기

새 기능은 master에 바로 넣지 않고 새 브랜치(branch)에 커밋한다. 브랜치는 원본과 분리된 작업 갈래를 뜻한다.

```
git checkout -b "MultiplicationFunction"
git add .
git commit -m "Multiplication function is added in Calculator API"
git push -u git@gitlab.com:Pranoday/jenkinsbookcalculatorapi.git MultiplicationFunction
```

원서 본문의 `git add.`는 `git add .`(점 앞 공백)로, `--m`은 `-m`으로 복원했다. 추출 과정에서 깨진 것으로 보인다.

| 명령 | 하는 일 |
| --- | --- |
| `git checkout -b` | MultiplicationFunction 브랜치를 만들고 이동 |
| `git add .` | 현재 폴더와 하위 폴더의 변경 파일을 스테이징 영역에 추가 |
| `git commit -m` | 스테이징한 변경을 메시지와 함께 커밋 |
| `git push -u` | 브랜치를 원격 저장소에 올림 |

push에서도 SSH 주소를 쓴다는 점이 중요하다. 실행하면 passphrase를 물어보고, 성공하면 브랜치가 원격에 올라간다. GitLab 저장소 페이지를 새로 고침하면 MultiplicationFunction 브랜치가 보이고 병합할 준비가 되어 있다.

## 8. 단계 8: 병합 요청 만들기

1. 페이지에 나타난 Create merge request 버튼을 누른다.
2. New merge request 페이지에서 Title과 Description을 채우고 Create merge request 버튼을 누른다.

이제 Merge 버튼만 누르면 변경이 master 브랜치로 합쳐진다. 하지만 원서는 아직 누르지 말라고 한다. 병합이 일어나는 순간 Jenkins 잡이 자동으로 돌면서 CalculatorAPI.jar의 새 버전을 만들어 Nexus에 배포해야 하기 때문이다. 그러려면 잡을 먼저 만들어 두어야 한다. 잡 만드는 방법은 다음 문서에서 다룬다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
