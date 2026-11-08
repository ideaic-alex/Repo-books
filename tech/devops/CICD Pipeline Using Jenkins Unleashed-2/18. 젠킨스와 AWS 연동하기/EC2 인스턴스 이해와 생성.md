# EC2 인스턴스 이해와 생성

요즘 애플리케이션은 회사 안의 서버보다 클라우드에 빌려 둔 서버에 올리는 경우가 많다. 그래서 AWS(Amazon Web Services, 아마존이 제공하는 클라우드 서비스)나 Azure 같은 클라우드 플랫폼을 이해하는 것이 DevOps 담당자에게 중요하다고 책은 말한다. 이 장의 목표는 젠킨스 잡(작업)으로 웹 애플리케이션을 AWS 위의 서버에 배포하고, 그 서버에서 Selenium 테스트까지 돌리는 것이다.

이 문서는 그 첫 단계로, 배포 대상이 되는 EC2 인스턴스가 무엇인지 알아보고 AWS에 가입해서 인스턴스를 만들고 접속하는 과정을 정리한다.

---

## 1. EC2 인스턴스란

EC2 인스턴스는 AWS에서 부르는 가상 서버의 이름이다. 호텔 방을 시간 단위로 빌리는 것과 비슷하다. 필요할 때 방을 잡고, 쓰는 동안만 요금을 내고, 안 쓰면 체크아웃한다. EC2는 Elastic Compute Cloud(탄력적인 컴퓨팅 클라우드)의 줄임말이다. AWS 가입자가 웹 서비스로 컴퓨터 서버를 요청해서 AWS 클라우드 안에 받아 쓰는 구조다.

| 특징 | 내용 |
| --- | --- |
| 요금 | 시간당으로 매기며, 고른 인스턴스 유형에 따라 단가가 다르다 |
| 사양 선택 | CPU와 메모리 요구량에 맞춰 만들 수 있다 |
| 사용 기간 | 필요한 만큼만 쓰고, 안 쓰면 종료(terminate)해서 비용을 아낀다 |
| 쓰임새 | 소프트웨어 애플리케이션을 배포하는 서버로 쓴다 |

표의 핵심은 쓴 만큼만 낸다는 점이다. 배포 실습이 끝나면 인스턴스를 종료해 두는 편이 비용 면에서 안전하다.

## 2. 인스턴스 유형 고르기

인스턴스를 만들 때 t2.micro, t2.medium, t2.large 같은 유형이 보인다. 유형마다 디스크 공간, 프로세서 속도, RAM이 다르므로 필요한 사양에 맞춰 골라야 한다. 원문은 이 유형들을 t2micro, t2medium처럼 점 없이 적었는데, 추출본의 표기 그대로 옮기면 혼동되므로 이 노트에서는 일반적인 표기인 t2.micro로 쓴다.

t2.micro처럼 무료로 쓸 수 있는 유형이 몇 가지 있고, 나머지는 유료다. 이 장의 실습에서는 Windows 이미지 검색 결과의 첫 번째 항목을 골랐고, 그 항목이 무료였다.

## 3. AWS 가입하기

가입은 AWS 가입 페이지(aws.amazon.com/account/sign-up)에서 시작한다. 책이 안내하는 순서는 다음과 같다.

1. Create a Free Account 버튼을 눌러 Sign Up for AWS 페이지를 연다.
2. 필요한 정보를 채우고 Continue (step 1 of 5)를 누른다.
3. 다음 화면 정보를 채우고 Continue (step 2 of 5)를 누르면 결제 정보(Billing Information) 페이지가 나온다.
4. 결제 수단 정보를 입력한다.
5. 본인 확인 화면에서 Text Message 라디오 버튼을 고르고 휴대폰 번호를 넣은 뒤 Continue (step 4 of 5)를 누른다. 문자로 온 인증 코드를 해당 페이지에 입력한다.
6. Continue (step 5 of 5)를 누르면 Select a Support Plan 페이지가 열린다. 여기서 Complete Sign Up을 누른다.
7. Go to AWS Management Console 버튼을 누르고, Role과 Interest 드롭다운을 고른 뒤 Submit을 누른다.

무료 계정이라도 결제 정보를 입력해야 가입이 진행된다는 점을 기억해 둔다. 그래서 위에서 말한 인스턴스 종료가 더 중요하다.

## 4. AWS에 로그인해서 EC2 화면 열기

1. Sign in to the Console 버튼을 누른다.
2. Root User Email Address 입력란에 가입한 이메일을 넣고 Next를 누른다.
3. 화면에 나온 CAPTCHA(사람인지 확인하는 문자 입력)를 입력하고 Submit을 누른다.
4. 가입할 때 정한 비밀번호를 Password 입력란에 넣고 Sign in을 누른다.
5. All Services 링크로 전체 서비스를 열고, Compute 영역의 첫 번째 항목인 EC2를 누른다.

## 5. 인스턴스 만들기

1. 화면을 내려 Launch Instance 드롭다운을 누르고 다시 Launch Instance를 고른다.
2. 검색란에 Windows를 입력하고 Enter를 누르면 Windows OS를 쓰는 이미지 목록이 나온다. 이 장은 Windows 서버를 배포 대상으로 쓴다.
3. 앞에서 말한 대로 첫 번째 항목(무료)을 고른다.
4. Review and Launch를 누르고, 이어서 Launch를 누른다.
5. Select an Existing Key Pair or Create a New Key Pair 창이 열린다. 여기서 인스턴스에 접속할 때 쓸 인증용 키 쌍(key pair)을 만든다.
6. Choose an Existing Key Pair 드롭다운에서 Create a New Key Pair를 고른다.
7. Key Pair Name 입력란에 이름을 넣는다. 책은 MyEC2Instance를 썼다.
8. Download Key Pair를 눌러 MyEC2Instance.pem 파일을 내려받는다.
9. Launch Instances를 누르고, 화면을 내려 View Instances 버튼을 누르면 Instances 페이지가 열린다.

.pem 파일은 개인 키(private key) 파일이다. 집 열쇠와 같아서, 이 파일이 있어야 인스턴스에 들어갈 수 있으므로 잘 보관해야 한다.

## 6. 인스턴스에 원격 데스크톱으로 접속하기

만든 인스턴스는 Windows 서버라서 RDP(Remote Desktop Protocol, 원격 데스크톱 연결 방식)로 접속한다. 처음 접속할 때 필요한 관리자 비밀번호는 방금 받은 키 파일로 풀어서 얻는다.

1. Instances 페이지에서 인스턴스 항목 첫 번째 열의 체크박스를 선택하고 Actions 버튼을 눌러 Connect를 고른다.
2. RDP Client 탭을 열고 Get Password 링크를 누른다.
3. Browse 버튼으로 MyEC2Instance.pem 파일을 고른다. 파일을 열면 개인 키 내용이 입력란에 표시된다.
4. Decrypt Password 버튼을 누르면 Password: 라벨 아래에 비밀번호가 만들어진다. 오른쪽 복사 버튼으로 복사한다.
5. Download Remote Desktop File 버튼으로 원격 데스크톱 파일을 받아 더블클릭하고 Connect를 누른다.
6. Password 입력란에 복사한 비밀번호를 붙여 넣고 OK를 누른다.
7. 확인 창에서 Yes를 누르면 EC2 인스턴스의 Windows 바탕화면이 열린다(원서 Figure 18-1).

### 정리 표

| 단계 | 하는 일 | 결과 |
| --- | --- | --- |
| 가입 | 계정 정보, 결제 정보, 문자 인증, 지원 플랜 선택 | AWS 계정 |
| 로그인 | 루트 사용자 이메일, CAPTCHA, 비밀번호 | AWS Management Console |
| 인스턴스 생성 | Windows 이미지와 무료 유형 선택, 키 쌍 생성 | 실행 중인 EC2 인스턴스와 .pem 파일 |
| 접속 | .pem으로 비밀번호 해독, RDP 파일 실행 | 인스턴스의 Windows 바탕화면 |

위 표처럼 이 문서의 실습은 가입, 로그인, 생성, 접속 네 덩어리로 나뉜다. 다음 문서에서는 접속한 인스턴스 안에 웹 서버를 설치한다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
