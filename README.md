📌 NOTICE

공지사항

깃랩 사용법


Code Server 사용시, 꼭 HTTPS 프로토콜로 Remote 레포지 토리를 연결 해주세요! (공용 Code Server 에 SSH 인증시 보안 취약)

Code Server 사용시, GIT ID 를 --local 로 설정해주세요.
레포지토리 세팅 수정은 관리자만 가능합니다. 레포지토리 생성시, 박민규 프로(김윤민 프로, 송지원 프로)에게 요청 해주세요.


[깃랩 명령어] 레포지토리 복사

# 리모트 레포지토리 클론
git remote add origin [리모트 레포지토리명] 
git clone [리모트 레포지토리명]

# 유저 설정
git config --local user.email [깃랩 이메일]
git config --local user.name [깃랩 이름]

#설정 확인
git config --list

# 리모트 레포지토리 PUSH
git commit -am [설명]
git push origin main



오류 대응 리스트

error: src refspec main does not match any.

로컬 GIT의 레포지토리의 branch 와 리모트레포지토리(깃랩)의 branch 가 달라서 오류 발생


# 로컬 레포지토리의 `branch` 확인
git branch

# 깃랩과 동일한 브랜치 생성(main)
git branch main
# 생성한 브랜치 이동
git checkout main



[관리자] 깃랩 레포지토리 권한 관리


Developers 사용자는 레포지토리 생성 권한이 없다. Maintainers 사용자가 생성해주어야한다.
레포지토리 생성후 Settings - Repository - Protected branches 의 Allowed to merge 과 Allowed to push 를 Maintainers + Developers 로 설정해준다.

