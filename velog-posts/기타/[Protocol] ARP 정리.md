<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c607b1d1-d083-41d6-b4a8-a2aa6f9949ad/image.png" /></p>
<hr />
<h3 id="1-arp란">1. ARP란?</h3>
<p><strong>ARP (Address Resolution Protocol)</strong> = <strong>주소 해석 프로토콜</strong></p>
<h4 id="1-1-역할">1-1. 역할</h4>
<ul>
<li>데이터 링크 계층(Layer 2)과 네트워크 계층(Layer 3)의 <strong>다리 역할</strong>을 하는 프로토콜</li>
<li><strong>IP 주소 → MAC 주소 변환</strong> 담당</li>
</ul>
<h4 id="1-2-계층-위치">1-2. 계층 위치</h4>
<ul>
<li>두 계층의 중간에 위치하지만, 일반적으로 <strong>데이터 링크 계층(Layer 2) 프로토콜</strong>로 분류</li>
<li>이유: MAC 주소를 다루고, 이더넷 프레임으로 전송되기 때문</li>
</ul>
<hr />
<h2 id="2-주소의-개념적-구분">2. 주소의 개념적 구분</h2>
<h4 id="2-1-논리-주소-logical-address">2-1. 논리 주소 (Logical Address)</h4>
<ul>
<li><strong>네트워크 계층(Layer 3) 주소</strong> = <strong>IP 주소</strong></li>
<li>OS상에 설정된 논리적인 주소</li>
<li>변경 가능</li>
<li>예: <code>192.168.1.100</code></li>
</ul>
<h4 id="2-2-물리-주소-physical-address">2-2. 물리 주소 (Physical Address)</h4>
<ul>
<li><strong>데이터 링크 계층(Layer 2) 주소</strong> = <strong>MAC 주소</strong></li>
<li>NIC(네트워크 카드) 자체에 내장되어 있는 물리적인 주소</li>
<li>제조 시 고정됨 (일반적으로 변경 불가)</li>
<li>48비트 (6바이트)</li>
<li>예: <code>AA:BB:CC:DD:EE:FF</code></li>
</ul>
<h4 id="2-3-왜-arp가-필요한가">2-3. 왜 ARP가 필요한가?</h4>
<p><strong>문제 상황:</strong></p>
<pre><code>송신지: IP 주소는 알고 있음
       MAC 주소도 알고 있음 (자신의 NIC에 내장)

수신지: IP 주소는 알고 있음 ✅
       MAC 주소는 모름 ❌

→ 이더넷 프레임을 만들 수 없음!
  (프레임 헤더에 목적지 MAC 주소가 필요)</code></pre><p><strong>해결:</strong></p>
<pre><code>ARP를 사용하여 IP 주소 → MAC 주소 변환!</code></pre><hr />
<h3 id="3-arp-프레임-포맷">3. ARP 프레임 포맷</h3>
<h4 id="3-1-이더넷-프레임-내-arp-위치">3-1. 이더넷 프레임 내 ARP 위치</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c607b1d1-d083-41d6-b4a8-a2aa6f9949ad/image.png" /></p>
<pre><code>┌──────────────────────────────────────────┐
│ 이더넷 헤더 (14바이트)                  │
│  - 목적지 MAC (6바이트)                 │
│  - 송신지 MAC (6바이트)                 │
│  - EtherType: 0x0806 (2바이트)  ← ARP  │
├──────────────────────────────────────────┤
│ ARP 메시지 (28바이트)                   │
│  - 하드웨어 타입                        │
│  - 프로토콜 타입                        │
│  - 하드웨어 주소 길이                   │
│  - 프로토콜 주소 길이                   │
│  - 오퍼레이션 코드                      │
│  - 송신지 MAC 주소                     │
│  - 송신지 IP 주소                      │
│  - 목표 MAC 주소                       │
│  - 목표 IP 주소                        │
└──────────────────────────────────────────┘</code></pre><h4 id="3-2-arp-필드-상세">3-2. ARP 필드 상세</h4>
<table>
<thead>
<tr>
<th>필드</th>
<th>크기</th>
<th>설명</th>
<th>일반적인 값</th>
</tr>
</thead>
<tbody><tr>
<td><strong>하드웨어 타입</strong></td>
<td>2바이트</td>
<td>Layer 2 프로토콜 종류</td>
<td>0x0001 (이더넷)</td>
</tr>
<tr>
<td><strong>프로토콜 타입</strong></td>
<td>2바이트</td>
<td>Layer 3 프로토콜 종류</td>
<td>0x0800 (IPv4)</td>
</tr>
<tr>
<td><strong>하드웨어 주소 길이</strong></td>
<td>1바이트</td>
<td>MAC 주소 길이</td>
<td>6 (바이트)</td>
</tr>
<tr>
<td><strong>프로토콜 주소 길이</strong></td>
<td>1바이트</td>
<td>IP 주소 길이</td>
<td>4 (바이트)</td>
</tr>
<tr>
<td><strong>오퍼레이션 코드</strong></td>
<td>2바이트</td>
<td>ARP 메시지 종류</td>
<td>1 (Request), 2 (Reply)</td>
</tr>
<tr>
<td><strong>송신지 MAC 주소</strong></td>
<td>6바이트</td>
<td>송신자의 MAC 주소</td>
<td>AA:BB:CC:DD:EE:FF</td>
</tr>
<tr>
<td><strong>송신지 IP 주소</strong></td>
<td>4바이트</td>
<td>송신자의 IP 주소</td>
<td>192.168.1.10</td>
</tr>
<tr>
<td><strong>목표 MAC 주소</strong></td>
<td>6바이트</td>
<td>목적지 MAC 주소</td>
<td>00:00:00:00:00:00 (Request 시)</td>
</tr>
<tr>
<td><strong>목표 IP 주소</strong></td>
<td>4바이트</td>
<td>목적지 IP 주소</td>
<td>192.168.1.20</td>
</tr>
</tbody></table>
<hr />
<h3 id="4-arp-동작-과정">4. ARP 동작 과정</h3>
<h3 id="4-1-기본-동작-request와-reply">4-1. 기본 동작: Request와 Reply</h3>
<p>ARP는 <strong>2개의 메시지</strong>만으로 주소 변환을 수행합니다:</p>
<ol>
<li><p><strong>ARP Request (요청)</strong></p>
<ul>
<li>같은 네트워크에 있는 모든 단말에게 <strong>브로드캐스트</strong></li>
<li>&quot;이 IP 주소를 가진 사람, MAC 주소 알려줘!&quot;</li>
</ul>
</li>
<li><p><strong>ARP Reply (응답)</strong></p>
<ul>
<li>해당 IP를 가진 장치만 <strong>유니캐스트</strong>로 응답</li>
<li>&quot;나야! 내 MAC 주소는 이거야!&quot;</li>
</ul>
</li>
</ol>
<hr />
<h3 id="4-2-구체적인-예시">4-2. 구체적인 예시</h3>
<p><strong>시나리오:</strong></p>
<ul>
<li>PC1 (192.168.1.10, MAC: AA:AA:AA:AA:AA:AA)</li>
<li>PC2 (192.168.1.20, MAC: BB:BB:BB:BB:BB:BB)</li>
<li>PC3 (192.168.1.30, MAC: CC:CC:CC:CC:CC:CC)</li>
<li>PC4 (다른 네트워크)</li>
</ul>
<p>PC1이 PC2와 통신하고 싶지만, PC2의 MAC 주소를 모르는 상황</p>
<hr />
<h4 id="step-1-arp-테이블-확인">Step 1: ARP 테이블 확인</h4>
<pre><code>PC1: ARP 테이블 검색
→ 192.168.1.20의 MAC 주소가 없음!
→ ARP Request 송신 결정</code></pre><hr />
<h4 id="step-2-arp-request-생성">Step 2: ARP Request 생성</h4>
<p><strong>이더넷 헤더:</strong></p>
<pre><code>목적지 MAC: FF:FF:FF:FF:FF:FF  (브로드캐스트)
송신지 MAC: AA:AA:AA:AA:AA:AA  (PC1)
EtherType:  0x0806              (ARP)</code></pre><p><strong>ARP 메시지:</strong></p>
<pre><code>하드웨어 타입:     0x0001 (이더넷)
프로토콜 타입:     0x0800 (IPv4)
하드웨어 주소 길이: 6
프로토콜 주소 길이: 4
오퍼레이션 코드:   1 (Request)
송신지 MAC:        AA:AA:AA:AA:AA:AA
송신지 IP:         192.168.1.10
목표 MAC:          00:00:00:00:00:00  (모르니까 더미)
목표 IP:           192.168.1.20       (찾고 싶은 IP)</code></pre><hr />
<h4 id="step-3-arp-request-브로드캐스트">Step 3: ARP Request 브로드캐스트</h4>
<pre><code>PC1 → [스위치] → 모든 포트로 전송
         ↓
    ┌────┴────┬────────┐
    ↓         ↓        ↓
   PC2      PC3      (PC4는 다른 네트워크)

PC2: &quot;이거 내 IP네!&quot; → 받아들임 ✅
PC3: &quot;내 IP 아니네&quot; → 무시하고 폐기 ❌</code></pre><hr />
<h4 id="step-4-arp-reply-생성-pc2">Step 4: ARP Reply 생성 (PC2)</h4>
<p><strong>이더넷 헤더:</strong></p>
<pre><code>목적지 MAC: AA:AA:AA:AA:AA:AA  (PC1, 유니캐스트)
송신지 MAC: BB:BB:BB:BB:BB:BB  (PC2)
EtherType:  0x0806              (ARP)</code></pre><p><strong>ARP 메시지:</strong></p>
<pre><code>하드웨어 타입:     0x0001
프로토콜 타입:     0x0800
하드웨어 주소 길이: 6
프로토콜 주소 길이: 4
오퍼레이션 코드:   2 (Reply)
송신지 MAC:        BB:BB:BB:BB:BB:BB  (PC2의 MAC)
송신지 IP:         192.168.1.20
목표 MAC:          AA:AA:AA:AA:AA:AA  (PC1)
목표 IP:           192.168.1.10</code></pre><hr />
<h4 id="step-5-arp-reply-수신-pc1">Step 5: ARP Reply 수신 (PC1)</h4>
<pre><code>PC1: ARP Reply 받음
→ PC2의 MAC 주소 확인: BB:BB:BB:BB:BB:BB
→ ARP 테이블에 저장</code></pre><p><strong>PC1의 ARP 테이블:</strong></p>
<pre><code>IP 주소          MAC 주소              타입
192.168.1.20    BB:BB:BB:BB:BB:BB    동적</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/878100c6-41f9-4927-ae3d-50a29563dba9/image.png" /></p>
<hr />
<h4 id="step-6-통신-시작">Step 6: 통신 시작</h4>
<pre><code>이제 PC1은 이더넷 프레임을 만들 수 있음!

목적지 MAC: BB:BB:BB:BB:BB:BB  (PC2)
송신지 MAC: AA:AA:AA:AA:AA:AA  (PC1)
→ 데이터 전송 가능! ✅</code></pre><hr />
<h3 id="4-3-넥스트-홉-next-hop-처리">4-3. 넥스트 홉 (Next Hop) 처리</h3>
<p><strong>같은 네트워크:</strong></p>
<pre><code>목표 IP = 수신지 IP
(직접 통신 가능)</code></pre><p><strong>다른 네트워크:</strong></p>
<pre><code>목표 IP = 게이트웨이(라우터) IP
(라우터를 거쳐야 함)</code></pre><p><strong>예시:</strong></p>
<pre><code>PC1: 192.168.1.10
목적지: 10.0.0.50 (다른 네트워크)
게이트웨이: 192.168.1.1

→ ARP Request의 목표 IP: 192.168.1.1 (게이트웨이)
→ 게이트웨이의 MAC 주소를 얻음
→ 패킷을 게이트웨이로 보냄
→ 게이트웨이(라우터)가 10.0.0.50으로 전달</code></pre><hr />
<h3 id="5-arp-캐시-arp-cache">5. ARP 캐시 (ARP Cache)</h3>
<h3 id="5-1-문제점">5-1. 문제점</h3>
<p><strong>브로드캐스트의 단점:</strong></p>
<ul>
<li>같은 네트워크의 모든 장치에게 메시지 전송</li>
<li>네트워크 트래픽 증가</li>
<li>비효율적</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>PC가 100대 있는 네트워크에서
매번 통신할 때마다 100대 모두에게 브로드캐스트?
→ 엄청난 낭비! 💸</code></pre><hr />
<h3 id="5-2-해결책-캐시">5-2. 해결책: 캐시</h3>
<p><strong>ARP 캐시 (ARP Cache) = ARP 테이블 (ARP Table)</strong></p>
<ul>
<li>한 번 알아낸 &quot;IP - MAC&quot; 쌍을 메모리에 저장</li>
<li>일정 시간 동안 재사용</li>
<li>캐시에 있으면 ARP Request 송신 안 함!</li>
</ul>
<hr />
<h3 id="5-3-동작-방식">5-3. 동작 방식</h3>
<pre><code>1. 통신 필요
   ↓
2. ARP 테이블 확인
   ├─ 있음? → 바로 사용 (ARP 안 씀!) ✅
   └─ 없음? → ARP Request 송신
               ↓
            ARP Reply 받음
               ↓
            테이블에 저장 (캐시)
               ↓
            사용
               ↓
        일정 시간 경과 (타임아웃)
               ↓
            테이블에서 삭제</code></pre><hr />
<h3 id="5-4-arp-캐시-타임아웃">5-4. ARP 캐시 타임아웃</h3>
<p><strong>동적 엔트리 (Dynamic Entry):</strong></p>
<ul>
<li>ARP를 통해 자동으로 학습한 항목</li>
<li>일정 시간 후 자동 삭제</li>
<li>Windows: 약 2분 (활성) / 10분 (비활성)</li>
<li>Linux: 약 60초</li>
</ul>
<p><strong>정적 엔트리 (Static Entry):</strong></p>
<ul>
<li>관리자가 수동으로 설정한 항목</li>
<li>삭제되지 않음 (재부팅 전까지)</li>
</ul>
<hr />
<h3 id="5-5-arp-테이블-명령어">5-5. ARP 테이블 명령어</h3>
<p><strong>Windows:</strong></p>
<pre><code class="language-bash"># ARP 테이블 확인
arp -a

# 특정 엔트리 추가 (정적)
arp -s 192.168.1.20 AA-BB-CC-DD-EE-FF

# 특정 엔트리 삭제
arp -d 192.168.1.20

# 전체 삭제
arp -d *</code></pre>
<p><strong>Linux/Mac:</strong></p>
<pre><code class="language-bash"># ARP 테이블 확인
arp -n
# 또는
ip neigh

# 특정 엔트리 추가 (정적)
sudo arp -s 192.168.1.20 AA:BB:CC:DD:EE:FF

# 특정 엔트리 삭제
sudo arp -d 192.168.1.20

# ARP 캐시 플러시
sudo ip neigh flush all</code></pre>
<hr />
<h3 id="6-garp-gratuitous-arp">6. GARP (Gratuitous ARP)</h3>
<p><strong>GARP (Gratuitous ARP)</strong> = 자발적 ARP</p>
<p><strong>특징:</strong></p>
<ul>
<li>목표 IP 주소에 <strong>자신의 IP 주소</strong>를 설정한 특수한 ARP</li>
<li>요청하지 않았는데 자발적으로 보내는 ARP Request</li>
</ul>
<hr />
<h3 id="6-1-용도-1-ip-주소-중복-감지">6-1. 용도 1: IP 주소 중복 감지</h3>
<p><strong>문제:</strong></p>
<pre><code>네트워크에 이미 같은 IP 주소를 사용하는 장치가 있으면?
→ IP 충돌! 💥</code></pre><p><strong>해결:</strong></p>
<pre><code>새로운 장치가 네트워크에 연결될 때:
1. GARP를 브로드캐스트
   &quot;192.168.1.100 사용하는 사람 있어요?&quot;

2-1. 응답 없음 → 안전하게 사용 ✅
2-2. ARP Reply 받음 → IP 중복! ❌
     → 에러 메시지 표시
     → 다른 IP 사용하도록 요청</code></pre><p><strong>GARP 메시지:</strong></p>
<pre><code>송신지 IP: 192.168.1.100
목표 IP:   192.168.1.100  ← 자기 자신!</code></pre><hr />
<h3 id="6-2-용도-2-인접-기기의-arp-테이블-업데이트">6-2. 용도 2: 인접 기기의 ARP 테이블 업데이트</h3>
<p><strong>상황 1: NIC 교체</strong></p>
<pre><code>서버의 NIC를 교체
→ MAC 주소가 변경됨
→ 다른 장치들의 ARP 테이블에는 여전히 옛날 MAC 주소!
→ 통신 실패! ❌</code></pre><p><strong>해결:</strong></p>
<pre><code>교체된 서버가 네트워크에 연결되자마자:
1. GARP 송신 (브로드캐스트)
   &quot;내 IP는 192.168.1.50이고, MAC은 새로 XX:XX:XX:XX:XX:XX야!&quot;

2. 모든 장치가 GARP 받음
   → ARP 테이블 자동 업데이트 ✅</code></pre><hr />
<p><strong>상황 2: 가상 IP 이동 (HA, High Availability)</strong></p>
<pre><code>이중화 구성:
- 서버1: 대기 (Standby)
- 서버2: 활성 (Active) → 가상 IP: 192.168.1.100

서버2 장애 발생!
→ 서버1이 가상 IP 인수
→ 하지만 다른 장치들은 여전히 서버2의 MAC 주소로 패킷 전송
→ 통신 실패! ❌</code></pre><p><strong>해결:</strong></p>
<pre><code>서버1이 가상 IP 인수 시:
1. GARP 송신
   &quot;192.168.1.100은 이제 내(서버1) MAC 주소야!&quot;

2. 모든 장치가 ARP 테이블 업데이트
   → 서버1으로 패킷 전송 ✅
   → 무중단 서비스 유지</code></pre><hr />
<h3 id="6-3-garp의-특징">6-3. GARP의 특징</h3>
<table>
<thead>
<tr>
<th>특징</th>
<th>일반 ARP Request</th>
<th>GARP</th>
</tr>
</thead>
<tbody><tr>
<td><strong>목표 IP</strong></td>
<td>찾고 싶은 다른 IP</td>
<td>자기 자신의 IP</td>
</tr>
<tr>
<td><strong>목적</strong></td>
<td>MAC 주소 알아내기</td>
<td>자신의 MAC 알리기</td>
</tr>
<tr>
<td><strong>응답</strong></td>
<td>Reply 필요</td>
<td>Reply 불필요 (보통)</td>
</tr>
<tr>
<td><strong>전송 방식</strong></td>
<td>브로드캐스트</td>
<td>브로드캐스트</td>
</tr>
<tr>
<td><strong>사용 시점</strong></td>
<td>통신 전</td>
<td>부팅 시, NIC 교체 시, IP 변경 시</td>
</tr>
</tbody></table>
<hr />
<h2 id="7-arp-보안-이슈">7. ARP 보안 이슈</h2>
<h3 id="7-1-arp-spoofing-arp-스푸핑">7-1. ARP Spoofing (ARP 스푸핑)</h3>
<p><strong>공격 방법:</strong></p>
<pre><code>공격자가 거짓 ARP Reply를 보냄
→ 피해자의 ARP 테이블을 조작
→ 트래픽을 공격자에게 전송
→ 중간자 공격 (Man-in-the-Middle, MITM)</code></pre><p><strong>예시:</strong></p>
<pre><code>정상:
PC1 → 게이트웨이(192.168.1.1, MAC: AA:AA:AA) → 인터넷

공격:
공격자가 PC1에게 거짓 ARP Reply 전송
&quot;192.168.1.1의 MAC은 BB:BB:BB(공격자)야!&quot;
→ PC1의 ARP 테이블 변조
→ PC1 → 공격자 → 게이트웨이 → 인터넷
         ↑ 트래픽 가로채기! 🕵️</code></pre><hr />
<h3 id="7-2-대응-방법">7-2. 대응 방법</h3>
<p><strong>1. 정적 ARP 엔트리 설정</strong></p>
<pre><code class="language-bash"># 중요한 장치(게이트웨이 등)는 수동 설정
arp -s 192.168.1.1 AA-BB-CC-DD-EE-FF</code></pre>
<p><strong>2. DAI (Dynamic ARP Inspection)</strong></p>
<ul>
<li>스위치 기능</li>
<li>ARP 패킷의 유효성 검사</li>
<li>신뢰할 수 없는 포트의 ARP를 필터링</li>
</ul>
<p><strong>3. ARP 감시 도구</strong></p>
<ul>
<li>arpwatch (Linux)</li>
<li>XArp (Windows)</li>
<li>비정상적인 ARP 트래픽 탐지</li>
</ul>
<hr />
<h2 id="8-정리">8. 정리</h2>
<h3 id="핵심-요약">핵심 요약</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>내용</th>
</tr>
</thead>
<tbody><tr>
<td><strong>프로토콜 이름</strong></td>
<td>ARP (Address Resolution Protocol)</td>
</tr>
<tr>
<td><strong>역할</strong></td>
<td>IP 주소 → MAC 주소 변환</td>
</tr>
<tr>
<td><strong>계층</strong></td>
<td>Layer 2 (데이터 링크 계층)</td>
</tr>
<tr>
<td><strong>주요 메시지</strong></td>
<td>ARP Request (브로드캐스트), ARP Reply (유니캐스트)</td>
</tr>
<tr>
<td><strong>캐시</strong></td>
<td>일정 시간 동안 변환 결과 저장</td>
</tr>
<tr>
<td><strong>특수 기능</strong></td>
<td>GARP (IP 중복 감지, 테이블 업데이트)</td>
</tr>
<tr>
<td><strong>보안 위협</strong></td>
<td>ARP Spoofing (스푸핑)</td>
</tr>
<tr>
<td><strong>EtherType</strong></td>
<td>0x0806</td>
</tr>
</tbody></table>
<h3 id="동작-흐름">동작 흐름</h3>
<pre><code>1. 통신 필요 (IP는 알지만 MAC 모름)
   ↓
2. ARP 테이블 확인
   ├─ 있음? → 바로 사용
   └─ 없음? ↓
3. ARP Request 브로드캐스트
   &quot;이 IP 가진 사람 MAC 알려줘!&quot;
   ↓
4. 해당 장치만 ARP Reply (유니캐스트)
   &quot;내 MAC은 이거야!&quot;
   ↓
5. ARP 테이블에 저장 (캐시)
   ↓
6. 통신 시작 (이더넷 프레임 생성 가능)</code></pre><h3 id="기억할-점">기억할 점</h3>
<ul>
<li><strong>ARP는 Layer 2 프로토콜</strong> (IP는 Layer 3)</li>
<li><strong>같은 네트워크 내에서만 동작</strong> (라우터 넘어가면 불가)</li>
<li><strong>브로드캐스트 사용</strong> → 캐시로 효율 향상</li>
<li><strong>보안에 취약</strong> → 스푸핑 공격 주의</li>
<li><strong>GARP는 자신의 MAC을 알리는 용도</strong></li>
</ul>