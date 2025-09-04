# 🔐 dag-tagging-frontend

JWT 기반의 내부망/외부망 태깅 시스템입니다.  
사용자의 공인 IP를 기준으로 태깅 정책을 분기하며, 보안 검증을 위해 JWT 서명 및 IP 일치 여부를 확인합니다.

### 🧭 시스템 구성
- 프론트엔드서버: `user.cloude.co.kr` (nginx + flask)
- 백엔드서버: `secure.cloude.co.kr` (nginx + flask)
- 내부망 기준 IP: `211.58.74.253`

### 🗺️ 피지컬 처리 플로우
<img width="2878" height="2094" alt="image" src="https://github.com/user-attachments/assets/f93204a5-e9bf-4aed-b4b4-faa87001d7a8" />

### 🗺️ 논리적 처리 플로우
<img width="962" height="1048" alt="image" src="https://github.com/user-attachments/assets/006762cf-bba4-4174-8a8a-e62a51d55be2" />

### 고려사항
- XFF 신뢰성 : XFF 헤더는 중간 프록시나 NAT 환경에 따라 조작 가능성이 있음으로 첫 번쨰 XFF 헤더에 담기는 IP를 정확하게 파싱할 수 있어야 함.
- URL 로그 기반 DAG 태깅 : Prisma Access가 URL 로그를 기반으로 DAG 태깅을 해야 함. 따라서 백엔드서버의 태깅 URL 호출 트랜잭션은 사용자단에서 수행되어져야 함. 
- 보안성 : 사용자가 태깅 URL을 인증 토큰 없이도 가능하다면 사용자가 직접 호출해서 DAG 태깅을 유도할 수 있음. 이 URL 호출은 반드시 인증된 사용자만 가능하도록 제한해야 함.
- 정책 적용 시점 : DAG 태깅이 실시간으로 반영되지 않으면 정책 적용에 딜레마가 생길 수 있음. 이 부분은 로그 처리 속도와 Prisma Access의 DAG 업데이트 주기를 고려해야 함.

### ⚙️ 주요 기능
- 'https://api.ipify.org/?format=json'을 이용하여 사용자의 XFF IP 정보를 획득. Prisma Access Split Tunnel에 해당 도메인 예외처리
- XFF IP 정보를 토대로 내부/외부 태깅 API
- 보안성 강화를 위한 JWT 기반 태깅 토큰 생성 및 검증
- 태깅 종료 처리

### 🧪 보안 검증
- IP 일치 (`X-Forwarded-For`)
- 태그 일치 (`internal` / `external`)
- Origin 검증 (`user.cloude.co.kr`)
- JWT 서명 및 만료 검증

### 📦 설치
Coming soon


