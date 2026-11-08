# Jenkins 이메일 알림 설정

잡에 E-mail Notification을 붙였다고 해서 메일이 저절로 나가지는 않는다. Jenkins가 메일을 보내려면 "누구 이름으로, 어느 메일 서버를 통해" 보낼지 알아야 한다. 이 문서는 Manage Jenkins에서 관리자 이메일과 SMTP 서버를 설정하고, 시험 메일을 보내 확인하는 과정을 정리한다.

SMTP(Simple Mail Transfer Protocol)는 메일을 보내는 데 쓰는 규약이고, SMTP 서버는 그 서비스를 제공하는 우체국 같은 서버다. Jenkins는 편지를 쓰기만 하고, 부치는 일은 이 우체국에 맡긴다. 원서는 Gmail의 SMTP 서버를 쓴다.

---

## 1. 시스템 관리자 이메일 주소

1. Jenkins 대시보드에서 Manage Jenkins 메뉴를 누른다. Manage Jenkins 페이지가 열린다.
2. Configure System 옵션을 누른다. System Configuration 페이지로 이동한다.
3. 아래로 내려 Jenkins Location 섹션을 찾는다.
4. System Admin e-mail address 입력란에 이메일 주소를 쓴다.

이 주소는 Jenkins가 보낸 메일의 보낸 사람(From)으로 표시된다. 원서는 `pranoday.dingare@gmail.com`을 넣었다. 받은 편지함의 From 열에 이 주소가 보이게 된다.

## 2. SMTP 서버 설정

같은 페이지를 더 내려 E-mail Notification 섹션으로 간다.

1. SMTP server 입력란에 메일 서버 주소를 쓴다. 회사에 자체 SMTP 서버가 있으면 그 IP 주소를 넣어도 된다. 원서는 Gmail을 쓰므로 `smtp.gmail.com`을 입력했다.
2. Advanced 버튼을 눌러 추가 설정을 연다.
3. Use SMTP Authentication 체크박스를 선택하고 User Name과 Password에 유효한 Gmail 계정 정보를 입력한다. Gmail의 SMTP 서버가 이 정보로 접근을 인증한다.
4. Use SSL 체크박스를 선택하고 SMTP Port에 `465`를 입력한다.

회사 도메인의 SMTP 서버 주소를 쓴 경우에도 User Name과 Password에는 그 서버에서 쓰는 사용자 정보를 넣어야 한다. 원서는 이 점을 별도 Note로 강조한다.

| 항목 | 원서에서 넣은 값 | 설명 |
| --- | --- | --- |
| System Admin e-mail address | pranoday.dingare@gmail.com | 보낸 사람으로 보이는 주소 |
| SMTP server | smtp.gmail.com | Gmail의 메일 서버 |
| Use SMTP Authentication | 체크 | 사용자 이름과 비밀번호로 인증 |
| User Name, Password | Gmail 계정 정보 | 메일 서버가 확인하는 로그인 |
| Use SSL | 체크 | 암호화 연결 사용 |
| SMTP Port | 465 | SSL용 포트 번호 |

User Name과 Password는 메일을 보내는 계정의 정보다. 원서에서는 dpranoday@gmail.com 계정으로 메일을 보냈다.

## 3. 시험 메일로 확인하기

설정이 맞는지 직접 확인한다.

1. Test configuration by sending test e-mail 체크박스를 선택한다.
2. 받을 이메일 주소를 입력한다.
3. Test configuration 버튼을 누른다.

원서에서는 첫 시도에서 오류가 났다.

```
javax.mail.AuthenticationFailedException: UserName and Password not accepted
```

이 오류는 사용자 이름과 비밀번호를 서버가 받아 주지 않았다는 뜻이다. 원서의 해결 방법은 보내는 Gmail 계정에서 보안 수준이 낮은 앱의 접근을 허용하는 것이다.

## 4. Gmail 보안 설정 바꾸기

1. 보내는 계정(dpranoday@gmail.com)으로 Gmail에 접속해 Manage your Google Account 옵션을 누른다.
2. 왼쪽 메뉴에서 Security를 누른다.
3. 아래로 내려 Less secure app access 섹션을 찾는다.
4. Turn on access (not recommended) 링크를 누른다. Less secure app access 페이지가 열린다.
5. Allow less secure apps: OFF 라디오 버튼을 눌러 켠다.
6. Jenkins로 돌아가 Test configuration 버튼을 다시 누른다. 이번에는 메일이 정상적으로 발송된다.

| 시도 | 결과 | 원인과 조치 |
| --- | --- | --- |
| 첫 번째 | AuthenticationFailedException | Gmail이 접근을 막음 |
| Less secure apps 허용 후 | 메일 발송 성공 | 설정 변경으로 해결 |

원서가 보여 준 이 방법은 Google이 스스로 "권장하지 않음(not recommended)"이라고 표시하는 설정이다. 이 노트는 원서의 서술 시점(2022년)을 따르며, 이 Gmail 메뉴와 정책은 이후 바뀌었을 수 있다. 실제 환경에서는 회사 SMTP 서버를 쓰거나 최신 Gmail 인증 방식을 확인해서 쓰는 편이 안전하다.

## 5. 정리

| 순서 | 위치 | 할 일 |
| --- | --- | --- |
| 1 | Manage Jenkins → Configure System → Jenkins Location | 관리자 이메일 입력 |
| 2 | 같은 페이지 E-mail Notification | SMTP 서버, 인증, SSL, 포트 입력 |
| 3 | Test configuration | 시험 메일 발송 |
| 4 | Gmail 보안 설정 | 인증 오류가 나면 접근 허용 |

이제 잡이 실패하면 지정한 주소로 메일이 갈 준비가 끝났다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
