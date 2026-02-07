<h3 id="1-ipv4-패킷-구조">1. IPv4 패킷 구조</h3>
<h4 id="1-1-ip-패킷이란">1-1. IP 패킷이란?</h4>
<p><strong>IP 패킷</strong> = <strong>IP 헤더</strong> + <strong>IP 페이로드(데이터)</strong></p>
<pre><code>┌─────────────────────────────────────┐
│ IP 헤더 (20~60바이트)              │
│  - 버전, 헤더 길이, TTL, 프로토콜 등 │
├─────────────────────────────────────┤ 
│ IP 페이로드                       │
│  - 실제 데이터 (TCP, UDP, ICMP 등) │
└─────────────────────────────────────┘</code></pre><hr />
<h2 id="2-ipv4-헤더-필드-상세">2. IPv4 헤더 필드 상세</h2>
<h3 id="2-1-전체-헤더-구조">2-1. 전체 헤더 구조</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cb3e67ec-0800-4ef6-9c6c-e1e8de0ea79c/image.png" /></p>
<hr />
<h3 id="2-2-각-필드-설명">2-2. 각 필드 설명</h3>
<h4 id="버전-version-4비트"><strong>버전 (Version, 4비트)</strong></h4>
<ul>
<li>IP 프로토콜 버전 번호</li>
<li>IPv4: <code>4 (0100)</code></li>
<li>IPv6: <code>6 (0110)</code></li>
</ul>
<h4 id="헤더-길이-ihl-internet-header-length-4비트"><strong>헤더 길이 (IHL, Internet Header Length, 4비트)</strong></h4>
<ul>
<li>IP 헤더의 길이를 <strong>4바이트 단위</strong>로 표시</li>
<li>최소값: <code>5</code> (5 × 4 = 20바이트, 옵션 없음)</li>
<li>최대값: <code>15</code> (15 × 4 = 60바이트, 옵션 40바이트)</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>IHL = 5 → 헤더 길이 = 20바이트 (일반적인 경우)
IHL = 6 → 헤더 길이 = 24바이트 (옵션 4바이트)</code></pre><h4 id="tos-type-of-service-8비트"><strong>ToS (Type of Service, 8비트)</strong></h4>
<ul>
<li>패킷의 우선순위 및 QoS(Quality of Service) 정보</li>
<li>현재는 <strong>DSCP (Differentiated Services Code Point)</strong>로 주로 사용</li>
<li>용도: VoIP, 스트리밍 등 실시간 데이터 우선 처리</li>
</ul>
<p><strong>구성:</strong></p>
<pre><code>0 1 2 3 4 5 6 7
├─ DSCP ─┤ ECN │
  (6비트)  (2비트)

DSCP: 우선순위 (0~63)
ECN: 혼잡 통지 (Explicit Congestion Notification)</code></pre><h4 id="패킷-길이-total-length-16비트"><strong>패킷 길이 (Total Length, 16비트)</strong></h4>
<ul>
<li><strong>IP 패킷 전체 길이</strong> (헤더 + 페이로드)</li>
<li>단위: 바이트</li>
<li>최소: 20바이트 (헤더만 있는 경우)</li>
<li>최대: 65,535바이트 (2^16 - 1)</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>Total Length = 1500바이트
IP 헤더 = 20바이트
→ 페이로드 = 1480바이트</code></pre><hr />
<h3 id="2-3-단편화-fragmentation-관련-필드">2-3. 단편화 (Fragmentation) 관련 필드</h3>
<h4 id="배경-mtu-maximum-transmission-unit"><strong>배경: MTU (Maximum Transmission Unit)</strong></h4>
<p><strong>MTU</strong>란?</p>
<ul>
<li>한 번에 전송할 수 있는 최대 패킷 크기</li>
<li>이더넷 MTU: 일반적으로 <strong>1500바이트</strong></li>
</ul>
<p><strong>문제:</strong></p>
<pre><code>큰 패킷(예: 3000바이트)을 작은 MTU(1500바이트) 네트워크로 보내려면?
→ 패킷을 작게 쪼개야 함! (Fragmentation, 단편화)</code></pre><hr />
<h3 id="식별자-identification-16비트"><strong>식별자 (Identification, 16비트)</strong></h3>
<ul>
<li>같은 원본 패킷에서 나온 단편들을 식별하기 위한 고유 번호</li>
<li>송신자가 패킷마다 다른 값 할당</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>원본 패킷 (3000바이트, ID=12345)
   ↓ 단편화
단편1 (1500바이트, ID=12345) ← 같은 ID
단편2 (1500바이트, ID=12345) ← 같은 ID</code></pre><hr />
<h3 id="플래그-flags-3비트"><strong>플래그 (Flags, 3비트)</strong></h3>
<table>
<thead>
<tr>
<th>비트</th>
<th>이름</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>0</td>
<td>Reserved</td>
<td>예약 (항상 0)</td>
</tr>
<tr>
<td>1</td>
<td><strong>DF (Don't Fragment)</strong></td>
<td>단편화 금지</td>
</tr>
<tr>
<td>2</td>
<td><strong>MF (More Fragments)</strong></td>
<td>뒤에 단편이 더 있음</td>
</tr>
</tbody></table>
<p><strong>플래그 조합:</strong></p>
<pre><code>DF=0, MF=0: 단편화되지 않음 또는 마지막 단편
DF=0, MF=1: 중간 단편 (뒤에 더 있음)
DF=1, MF=0: 단편화 금지 (쪼개지 말고 보내!)</code></pre><hr />
<h3 id="프래그먼트-오프셋-fragment-offset-13비트"><strong>프래그먼트 오프셋 (Fragment Offset, 13비트)</strong></h3>
<ul>
<li>원본 패킷에서 이 단편의 위치</li>
<li>단위: <strong>8바이트</strong></li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>원본 패킷: 3000바이트

단편1: 오프셋 = 0   (0 × 8 = 0바이트부터)
       데이터 = 0~1479바이트

단편2: 오프셋 = 185 (185 × 8 = 1480바이트부터)
       데이터 = 1480~2999바이트</code></pre><hr />
<h3 id="2-4-ttl-time-to-live-8비트">2-4. TTL (Time To Live, 8비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>패킷이 네트워크에서 무한정 순환하는 것을 방지</li>
<li><strong>라우터를 지날 때마다 1씩 감소</strong></li>
<li>TTL이 0이 되면 패킷 폐기</li>
</ul>
<p><strong>동작:</strong></p>
<pre><code>송신자: TTL = 64
   ↓
라우터1: TTL = 63 (1 감소)
   ↓
라우터2: TTL = 62 (1 감소)
   ↓
라우터3: TTL = 61 (1 감소)
   ...
   ↓
TTL = 0 → 패킷 폐기 + ICMP Time Exceeded 메시지 송신</code></pre><p><strong>일반적인 초기값:</strong></p>
<ul>
<li>Linux: 64</li>
<li>Windows: 128</li>
<li>Cisco 장비: 255</li>
</ul>
<p><strong>활용:</strong></p>
<ul>
<li><strong>Traceroute 명령어</strong>: TTL을 1부터 증가시켜 경로 추적</li>
<li><strong>네트워크 진단</strong>: 라우팅 루프 탐지</li>
</ul>
<hr />
<h3 id="2-5-프로토콜-번호-protocol-8비트">2-5. 프로토콜 번호 (Protocol, 8비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>IP 페이로드에 어떤 상위 계층 프로토콜이 들어있는지 표시</li>
</ul>
<p><strong>주요 프로토콜 번호:</strong></p>
<table>
<thead>
<tr>
<th>번호</th>
<th>프로토콜</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>1</td>
<td><strong>ICMP</strong></td>
<td>인터넷 제어 메시지 프로토콜 (ping, traceroute)</td>
</tr>
<tr>
<td>6</td>
<td><strong>TCP</strong></td>
<td>전송 제어 프로토콜 (신뢰성 있는 연결)</td>
</tr>
<tr>
<td>17</td>
<td><strong>UDP</strong></td>
<td>사용자 데이터그램 프로토콜 (빠른 전송)</td>
</tr>
<tr>
<td>41</td>
<td>IPv6</td>
<td>IPv6 터널링</td>
</tr>
<tr>
<td>47</td>
<td>GRE</td>
<td>Generic Routing Encapsulation</td>
</tr>
<tr>
<td>50</td>
<td>ESP</td>
<td>IPsec 암호화</td>
</tr>
<tr>
<td>89</td>
<td>OSPF</td>
<td>라우팅 프로토콜</td>
</tr>
<tr>
<td>112</td>
<td>VRRP</td>
<td>기본 게이트웨이 이중화를 위한 가상 라우터 프로토콜</td>
</tr>
</tbody></table>
<p><strong>동작:</strong></p>
<pre><code>수신자가 IP 패킷 받음
   ↓
프로토콜 필드 확인
   ├─ 1 (ICMP) → ICMP 모듈로 전달
   ├─ 6 (TCP)  → TCP 모듈로 전달
   └─ 17 (UDP) → UDP 모듈로 전달</code></pre><hr />
<h3 id="2-6-icmp-internet-control-message-protocol">2-6. ICMP (Internet Control Message Protocol)</h3>
<h3 id="icmp란"><strong>ICMP란?</strong></h3>
<ul>
<li>네트워크 계층(Layer 3)에서 동작하는 <strong>제어 및 오류 보고 프로토콜</strong></li>
<li>IP의 일부로 동작 (프로토콜 번호 1)</li>
</ul>
<h3 id="icmp-메시지-구조"><strong>ICMP 메시지 구조</strong></h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4f80a228-72d3-4510-a82c-4678e526cf4e/image.png" /></p>
<p><strong>주요 용도:</strong></p>
<ol>
<li>오류 보고 (Destination Unreachable, Time Exceeded)</li>
<li>네트워크 진단 (Ping, Traceroute)</li>
<li>라우터 정보 (Redirect)</li>
</ol>
<p><strong>필드 설명:</strong></p>
<ul>
<li><strong>Type</strong>: ICMP 메시지 유형 (8비트)</li>
<li><strong>Code</strong>: Type의 세부적인 내용 (8비트)</li>
<li><strong>Checksum</strong>: 메시지 오류 검사 (16비트)</li>
<li><strong>가변 길이</strong>: Type에 따라 추가되는 메시지</li>
<li><strong>데이터</strong>: 실제 데이터 (보통 원본 IP 패킷의 헤더 + 8바이트)</li>
</ul>
<h4 id="주요-icmp-메시지"><strong>주요 ICMP 메시지</strong></h4>
<table>
<thead>
<tr>
<th>Type</th>
<th>Code</th>
<th>이름</th>
<th>설명</th>
<th>사용 예</th>
</tr>
</thead>
<tbody><tr>
<td>0</td>
<td>0</td>
<td><strong>Echo Reply</strong></td>
<td>Ping 응답</td>
<td>ping 명령어</td>
</tr>
<tr>
<td>3</td>
<td>0~15</td>
<td><strong>Destination Unreachable</strong></td>
<td>목적지 도달 불가</td>
<td>호스트/네트워크/포트 불가</td>
</tr>
<tr>
<td>3</td>
<td>3</td>
<td>Port Unreachable</td>
<td>포트 닫힘</td>
<td>UDP 포트 닫힘</td>
</tr>
<tr>
<td>5</td>
<td>0~3</td>
<td><strong>Redirect</strong></td>
<td>더 좋은 경로 알림</td>
<td>라우터가 최적 경로 안내</td>
</tr>
<tr>
<td>8</td>
<td>0</td>
<td><strong>Echo Request</strong></td>
<td>Ping 요청</td>
<td>ping 명령어</td>
</tr>
<tr>
<td>11</td>
<td>0</td>
<td><strong>Time Exceeded</strong></td>
<td>TTL 초과</td>
<td>traceroute 명령어</td>
</tr>
<tr>
<td>11</td>
<td>1</td>
<td>Fragment Reassembly Time Exceeded</td>
<td>단편 재조립 시간 초과</td>
<td>단편화된 패킷</td>
</tr>
</tbody></table>
<hr />
<h3 id="ping-동작-원리"><strong>Ping 동작 원리</strong></h3>
<pre><code>PC1                              PC2
 │                                │
 ├─ ICMP Echo Request (Type 8) ──→│
 │  &quot;살아있어?&quot;                    │
 │                                │
 │←─ ICMP Echo Reply (Type 0) ────┤
    &quot;응, 살아있어!&quot;</code></pre><hr />
<h3 id="traceroute-동작-원리"><strong>Traceroute 동작 원리</strong></h3>
<pre><code>1. TTL=1로 패킷 전송
   → 첫 번째 라우터에서 TTL=0
   → ICMP Time Exceeded (Type 11) 응답
   → 첫 번째 라우터 IP 확인!

2. TTL=2로 패킷 전송
   → 두 번째 라우터에서 TTL=0
   → ICMP Time Exceeded 응답
   → 두 번째 라우터 IP 확인!

3. TTL=3, 4, 5... 계속
   → 목적지 도달 시 ICMP Echo Reply 또는 Destination Unreachable</code></pre><hr />
<h3 id="2-7-헤더-체크섬-header-checksum-16비트">2-7. 헤더 체크섬 (Header Checksum, 16비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li><strong>IP 헤더의 오류 검사</strong></li>
<li>페이로드는 체크섬 대상이 아님 (상위 계층에서 검사)</li>
</ul>
<p><strong>동작:</strong></p>
<ol>
<li>송신자: 헤더의 모든 16비트 워드를 합산 → 보수 계산 → 체크섬 필드에 저장</li>
<li>수신자: 헤더의 모든 16비트 워드 합산 → 결과가 0xFFFF이면 정상</li>
</ol>
<p><strong>특징:</strong></p>
<ul>
<li>라우터를 지날 때마다 TTL이 변경되므로 체크섬도 <strong>다시 계산</strong>해야 함</li>
</ul>
<hr />
<h3 id="2-8-송신지수신지-ipv4-주소-각-32비트">2-8. 송신지/수신지 IPv4 주소 (각 32비트)</h3>
<p><strong>송신지 IP 주소 (Source IP Address):</strong></p>
<ul>
<li>패킷을 보낸 장치의 IP 주소</li>
<li>32비트 (4바이트)</li>
<li>예: <code>192.168.1.10</code></li>
</ul>
<p><strong>수신지 IP 주소 (Destination IP Address):</strong></p>
<ul>
<li>패킷을 받을 장치의 IP 주소</li>
<li>32비트 (4바이트)</li>
<li>예: <code>8.8.8.8</code></li>
</ul>
<hr />
<h3 id="2-9-옵션-options-가변-길이">2-9. 옵션 (Options, 가변 길이)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>추가적인 기능 제공 (선택사항)</li>
<li>거의 사용되지 않음 (성능 저하 우려)</li>
</ul>
<p><strong>주요 옵션:</strong></p>
<ul>
<li><strong>Record Route</strong>: 패킷이 거쳐간 라우터 IP 기록</li>
<li><strong>Timestamp</strong>: 각 라우터를 통과한 시간 기록</li>
<li><strong>Source Routing</strong>: 송신자가 경로를 지정</li>
</ul>
<p><strong>문제점:</strong></p>
<ul>
<li>옵션 처리 시 라우터 부담 증가</li>
<li>보안 위협 (경로 정보 노출)</li>
<li>현대 네트워크에서는 거의 사용 안 함</li>
</ul>
<hr />
<h3 id="2-10-패딩-padding-가변-길이">2-10. 패딩 (Padding, 가변 길이)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>IP 헤더를 <strong>32비트(4바이트)의 배수</strong>로 맞추기 위한 채우기</li>
<li>옵션이 있을 때만 필요</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>기본 헤더: 20바이트 (32비트 × 5 = 160비트) ✅
옵션: 6바이트 추가
→ 총 26바이트 (32비트의 배수 아님) ❌
→ 패딩 2바이트 추가
→ 총 28바이트 (32비트 × 7 = 224비트) ✅</code></pre><hr />
<h3 id="3-ipv4-주소-체계">3. IPv4 주소 체계</h3>
<h3 id="3-1-ipv4-주소-구조">3-1. IPv4 주소 구조</h3>
<p><strong>IPv4 주소:</strong></p>
<ul>
<li>32비트 (4바이트)</li>
<li>10진수 표기: <code>192.168.1.10</code></li>
<li>2진수 표기: <code>11000000.10101000.00000001.00001010</code></li>
</ul>
<p><strong>구성:</strong></p>
<pre><code>┌──────────────────┬──────────────────┐
│  네트워크 부분    │   호스트 부분    │
│ (Network Part)  │  (Host Part)   │
└──────────────────┴──────────────────┘
       ↑                    ↑
    어느 네트워크?      네트워크 내 어떤 장치?</code></pre><hr />
<h3 id="3-2-서브넷-마스크-subnet-mask">3-2. 서브넷 마스크 (Subnet Mask)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>IP 주소에서 <strong>네트워크 부분</strong>과 <strong>호스트 부분</strong>을 구분</li>
</ul>
<p><strong>동작 원리:</strong></p>
<pre><code>IP 주소:        192.168.1.10
               11000000.10101000.00000001.00001010

서브넷 마스크:  255.255.255.0
               11111111.11111111.11111111.00000000
                    ↑                      ↑
                 네트워크 부분           호스트 부분
                 (1로 표시)              (0으로 표시)</code></pre><p><strong>AND 연산으로 네트워크 주소 계산:</strong></p>
<pre><code>IP 주소:        192.168.  1. 10
서브넷 마스크:  255.255.255.  0
              ─────────────────────
네트워크 주소:  192.168.  1.  0  ✅</code></pre><hr />
<h3 id="3-3-cidr-표기법">3-3. CIDR 표기법</h3>
<p><strong>CIDR (Classless Inter-Domain Routing):</strong></p>
<ul>
<li>IP 주소와 서브넷 마스크를 간결하게 표기</li>
<li>형식: <code>IP주소/접두어길이</code></li>
</ul>
<p><strong>예시:</strong></p>
<table>
<thead>
<tr>
<th>10진수 표기</th>
<th>CIDR 표기</th>
<th>네트워크 비트</th>
<th>호스트 비트</th>
<th>사용 가능 호스트 수</th>
</tr>
</thead>
<tbody><tr>
<td>255.0.0.0</td>
<td>/8</td>
<td>8비트</td>
<td>24비트</td>
<td>16,777,214개</td>
</tr>
<tr>
<td>255.255.0.0</td>
<td>/16</td>
<td>16비트</td>
<td>16비트</td>
<td>65,534개</td>
</tr>
<tr>
<td>255.255.255.0</td>
<td>/24</td>
<td>24비트</td>
<td>8비트</td>
<td>254개</td>
</tr>
<tr>
<td>255.255.255.128</td>
<td>/25</td>
<td>25비트</td>
<td>7비트</td>
<td>126개</td>
</tr>
<tr>
<td>255.255.255.252</td>
<td>/30</td>
<td>30비트</td>
<td>2비트</td>
<td>2개 (P2P 연결)</td>
</tr>
</tbody></table>
<p><strong>계산 예시:</strong></p>
<pre><code>192.168.1.0/24

/24 = 앞에서 24비트가 네트워크 부분
    = 255.255.255.0

네트워크 주소: 192.168.1.0
브로드캐스트:  192.168.1.255
사용 가능:     192.168.1.1 ~ 192.168.1.254 (254개)</code></pre><hr />
<h3 id="4-ipv4-주소-분류">4. IPv4 주소 분류</h3>
<h3 id="4-1-클래스풀-어드레싱-classful-addressing">4-1. 클래스풀 어드레싱 (Classful Addressing)</h3>
<p><strong>구식 방법</strong> (현재는 거의 사용 안 함)</p>
<p><strong>클래스 구분:</strong></p>
<table>
<thead>
<tr>
<th>클래스</th>
<th>시작 비트</th>
<th>범위</th>
<th>기본 서브넷 마스크</th>
<th>용도</th>
</tr>
</thead>
<tbody><tr>
<td><strong>A</strong></td>
<td>0</td>
<td>0.0.0.0 ~ 127.255.255.255</td>
<td>/8 (255.0.0.0)</td>
<td>대규모 네트워크</td>
</tr>
<tr>
<td><strong>B</strong></td>
<td>10</td>
<td>128.0.0.0 ~ 191.255.255.255</td>
<td>/16 (255.255.0.0)</td>
<td>중규모 네트워크</td>
</tr>
<tr>
<td><strong>C</strong></td>
<td>110</td>
<td>192.0.0.0 ~ 223.255.255.255</td>
<td>/24 (255.255.255.0)</td>
<td>소규모 네트워크</td>
</tr>
<tr>
<td><strong>D</strong></td>
<td>1110</td>
<td>224.0.0.0 ~ 239.255.255.255</td>
<td>-</td>
<td>멀티캐스트</td>
</tr>
<tr>
<td><strong>E</strong></td>
<td>1111</td>
<td>240.0.0.0 ~ 255.255.255.255</td>
<td>-</td>
<td>예약 (실험용)</td>
</tr>
</tbody></table>
<p><strong>문제점:</strong></p>
<ul>
<li>IP 주소 낭비 (예: 500대 필요한데 Class B를 받으면 65,534개 할당)</li>
<li>비효율적</li>
</ul>
<hr />
<h3 id="4-2-클래스리스-어드레싱-classless-addressing">4-2. 클래스리스 어드레싱 (Classless Addressing)</h3>
<p><strong>현대적 방법</strong> (CIDR 사용)</p>
<p><strong>특징:</strong></p>
<ul>
<li>클래스 구분 없이 <strong>필요한 만큼만</strong> 할당</li>
<li>서브넷 마스크를 자유롭게 설정</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>500대 필요?
→ /23 (255.255.254.0, 510개 호스트) 할당 ✅
→ 낭비 최소화</code></pre><hr />
<h3 id="4-3-사용-장소에-따른-분류">4-3. 사용 장소에 따른 분류</h3>
<h4 id="글로벌-ipv4-주소-public-ip"><strong>글로벌 IPv4 주소 (Public IP)</strong></h4>
<p><strong>특징:</strong></p>
<ul>
<li>인터넷에서 <strong>전 세계적으로 유일</strong>한 주소</li>
<li>ISP(인터넷 서비스 제공자)가 할당</li>
<li>인터넷 통신에 필수</li>
</ul>
<p><strong>용도:</strong></p>
<ul>
<li>웹 서버, 메일 서버</li>
<li>공용 서비스 제공</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>8.8.8.8 (Google DNS)
1.1.1.1 (Cloudflare DNS)</code></pre><hr />
<h4 id="프라이빗-ipv4-주소-private-ip"><strong>프라이빗 IPv4 주소 (Private IP)</strong></h4>
<p><strong>특징:</strong></p>
<ul>
<li><strong>내부 네트워크 전용</strong> 주소</li>
<li>인터넷에서 <strong>라우팅되지 않음</strong></li>
<li>여러 조직이 동시에 사용 가능 (중복 OK)</li>
</ul>
<p><strong>범위:</strong></p>
<table>
<thead>
<tr>
<th>클래스</th>
<th>범위</th>
<th>CIDR</th>
<th>개수</th>
</tr>
</thead>
<tbody><tr>
<td>A</td>
<td>10.0.0.0 ~ 10.255.255.255</td>
<td>10.0.0.0/8</td>
<td>16,777,216개</td>
</tr>
<tr>
<td>B</td>
<td>172.16.0.0 ~ 172.31.255.255</td>
<td>172.16.0.0/12</td>
<td>1,048,576개</td>
</tr>
<tr>
<td>C</td>
<td>192.168.0.0 ~ 192.168.255.255</td>
<td>192.168.0.0/16</td>
<td>65,536개</td>
</tr>
</tbody></table>
<p><strong>사용 예:</strong></p>
<pre><code>가정/소규모: 192.168.1.0/24
중소기업:    172.16.0.0/16
대기업:      10.0.0.0/8</code></pre><p><strong>NAT (Network Address Translation):</strong></p>
<ul>
<li>프라이빗 IP → 공인 IP 변환</li>
<li>라우터가 담당</li>
<li>하나의 공인 IP로 여러 프라이빗 IP 사용 가능</li>
</ul>
<pre><code>내부 네트워크 (Private)       |    인터넷 (Public)
192.168.1.10 ─┐              |
192.168.1.20 ─┼→ [NAT 라우터] ─→ 203.0.113.1
192.168.1.30 ─┘              |</code></pre><hr />
<h3 id="4-4-예외-주소-특수-목적-주소">4-4. 예외 주소 (특수 목적 주소)</h3>
<h4 id="1-네트워크-주소-network-address"><strong>1. 네트워크 주소 (Network Address)</strong></h4>
<p><strong>정의:</strong></p>
<ul>
<li>호스트 부분이 <strong>모두 0</strong>인 주소</li>
<li>네트워크 자체를 식별</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>192.168.1.0/24
           ↑
        호스트 부분 = 0

→ 192.168.1.0은 네트워크 주소
→ 호스트에 할당 불가 ❌</code></pre><p><strong>용도:</strong></p>
<ul>
<li>라우팅 테이블</li>
<li>네트워크 식별</li>
</ul>
<hr />
<h3 id="2-브로드캐스트-주소-broadcast-address"><strong>2. 브로드캐스트 주소 (Broadcast Address)</strong></h3>
<p><strong>정의:</strong></p>
<ul>
<li>호스트 부분이 <strong>모두 1</strong>인 주소</li>
<li>네트워크 내 <strong>모든 장치</strong>에게 전송</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>192.168.1.255/24
            ↑
        호스트 부분 = 255 (11111111)

→ 192.168.1.255는 브로드캐스트 주소
→ 호스트에 할당 불가 ❌</code></pre><p><strong>용도:</strong></p>
<ul>
<li>ARP Request</li>
<li>DHCP Discover</li>
<li>네트워크 내 모든 장치에게 메시지 전송</li>
</ul>
<p><strong>종류:</strong></p>
<ul>
<li><strong>Limited Broadcast</strong>: <code>255.255.255.255</code> (현재 네트워크만)</li>
<li><strong>Directed Broadcast</strong>: <code>192.168.1.255</code> (특정 네트워크)</li>
</ul>
<hr />
<h3 id="3-루프백-주소-loopback-address"><strong>3. 루프백 주소 (Loopback Address)</strong></h3>
<p><strong>범위:</strong></p>
<ul>
<li><code>127.0.0.0/8</code> (127.0.0.0 ~ 127.255.255.255)</li>
<li>일반적으로 <code>127.0.0.1</code> 사용</li>
</ul>
<p><strong>역할:</strong></p>
<ul>
<li><strong>자기 자신</strong>을 가리키는 주소</li>
<li>네트워크 카드를 거치지 않음 (OS 내부에서 처리)</li>
</ul>
<p><strong>용도:</strong></p>
<ul>
<li>로컬 서버 테스트</li>
<li>네트워크 스택 진단</li>
<li>애플리케이션 간 통신 (같은 컴퓨터 내)</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code class="language-bash"># 웹 서버를 로컬에서 실행
http://127.0.0.1:8080
http://localhost:8080  (localhost = 127.0.0.1)

# Ping 테스트 (자기 자신)
ping 127.0.0.1
→ 네트워크 스택이 정상 동작하는지 확인</code></pre>
<p><strong>특징:</strong></p>
<ul>
<li>패킷이 실제 네트워크로 나가지 않음</li>
<li>외부에서 접근 불가 (보안)</li>
</ul>
<hr />
<h3 id="4-기타-특수-주소"><strong>4. 기타 특수 주소</strong></h3>
<table>
<thead>
<tr>
<th>주소</th>
<th>용도</th>
</tr>
</thead>
<tbody><tr>
<td>0.0.0.0/8</td>
<td>&quot;이 네트워크&quot; (현재 네트워크)</td>
</tr>
<tr>
<td>0.0.0.0</td>
<td>기본 라우트, DHCP에서 IP 요청 시</td>
</tr>
<tr>
<td>169.254.0.0/16</td>
<td>APIPA (자동 프라이빗 IP 할당)</td>
</tr>
<tr>
<td>224.0.0.0/4</td>
<td>멀티캐스트 (Class D)</td>
</tr>
<tr>
<td>255.255.255.255</td>
<td>Limited Broadcast</td>
</tr>
</tbody></table>
<hr />
<h3 id="5-정리">5. 정리</h3>
<h3 id="핵심-요약">핵심 요약</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>내용</th>
</tr>
</thead>
<tbody><tr>
<td><strong>프로토콜</strong></td>
<td>IPv4 (Internet Protocol version 4)</td>
</tr>
<tr>
<td><strong>계층</strong></td>
<td>Layer 3 (네트워크 계층)</td>
</tr>
<tr>
<td><strong>주소 길이</strong></td>
<td>32비트 (4바이트)</td>
</tr>
<tr>
<td><strong>헤더 크기</strong></td>
<td>최소 20바이트, 최대 60바이트</td>
</tr>
<tr>
<td><strong>주요 필드</strong></td>
<td>버전, TTL, 프로토콜, 송신지/수신지 IP</td>
</tr>
<tr>
<td><strong>단편화</strong></td>
<td>식별자, 플래그, 오프셋</td>
</tr>
<tr>
<td><strong>오류 제어</strong></td>
<td>헤더 체크섬, ICMP</td>
</tr>
<tr>
<td><strong>주소 표기</strong></td>
<td>10진수 (192.168.1.10), CIDR (/24)</td>
</tr>
</tbody></table>
<h3 id="ipv4-주소-종류">IPv4 주소 종류</h3>
<pre><code>IPv4 주소
├─ 공인 IP (Public) - 인터넷 통신
├─ 사설 IP (Private) - 내부 네트워크
│   ├─ 10.0.0.0/8
│   ├─ 172.16.0.0/12
│   └─ 192.168.0.0/16
└─ 특수 주소
    ├─ 네트워크 주소 (호스트 부분 = 0)
    ├─ 브로드캐스트 주소 (호스트 부분 = 1)
    └─ 루프백 주소 (127.0.0.0/8)</code></pre><h3 id="기억할-점">기억할 점</h3>
<ul>
<li><strong>TTL</strong>: 라우터 지날 때마다 1 감소, 0이 되면 폐기</li>
<li><strong>프로토콜 번호</strong>: 1=ICMP, 6=TCP, 17=UDP</li>
<li><strong>단편화</strong>: MTU보다 큰 패킷을 작게 쪼갬</li>
<li><strong>ICMP</strong>: Ping(Type 8/0), Traceroute(Type 11)</li>
<li><strong>서브넷 마스크</strong>: 네트워크/호스트 구분</li>
<li><strong>CIDR</strong>: /24 = 255.255.255.0</li>
<li><strong>사설 IP</strong>: 192.168.x.x (가정용)</li>
<li><strong>루프백</strong>: 127.0.0.1 (자기 자신)</li>
</ul>