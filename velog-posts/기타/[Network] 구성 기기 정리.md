<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3d6179d2-0d35-4125-895e-10495de362c0/image.png" /></p>
<hr />
<h3 id="네트워크-구성-기기">네트워크 구성 기기</h3>
<p>네트워크상에 존재하는 모든 네트워크 기기가 모든 계층의 프로토콜 정보를 보고 처리할 수는 없습니다. 각 기기는 특정 계층에서 동작하며, 해당 계층의 정보만을 처리합니다.</p>
<hr />
<h3 id="1-물리-계층-layer-1">1. 물리 계층 (Layer 1)</h3>
<p><strong>물리 계층</strong>은 케이블이나 커넥터 형태, 핀 할당(핀 배열) 등 물리적인 사양을 다룹니다.</p>
<p>물리 계층에서 동작하는 기기는 패킷을 <strong>광 신호/전기 신호로 변환</strong>하거나, <strong>전파로 변조</strong>하는 기능을 갖고 있습니다.</p>
<hr />
<h3 id="1-1-nic-network-interface-card">1-1. NIC (Network Interface Card)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/347245c7-a874-4f68-b808-d7ec7e8565c8/image.png" /></p>
<p><strong>역할:</strong> PC나 서버 등 컴퓨터를 네트워크에 연결하기 위해 필요한 하드웨어(부품)</p>
<p><strong>동작:</strong></p>
<ul>
<li>모든 네트워크 단말은 애플리케이션과 운영체제가 처리한 패킷을 NIC를 이용해 LAN 케이블이나 전파로 보냅니다</li>
<li>송신: 디지털 데이터를 전기 신호 또는 광 신호로 변환</li>
<li>수신: 전기 신호 또는 광 신호를 디지털 데이터로 변환</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li>각 NIC는 고유한 <strong>MAC 주소</strong>를 가짐 (48비트, 예: <code>00:1A:2B:3C:4D:5E</code>)</li>
<li>MAC 주소 확인: <code>ipconfig /all</code> (Windows) 또는 <code>ifconfig</code> (Linux/Mac)</li>
</ul>
<hr />
<h3 id="1-2-리피터-repeater">1-2. 리피터 (Repeater)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8bff2b36-e506-46e0-baa6-7c11162cb7d1/image.png" /></p>
<p><strong>역할:</strong> 신호를 증폭하여 전송 거리를 연장</p>
<p><strong>동작:</strong></p>
<ul>
<li>전송 중 약해진 신호의 파형을 한 번 더 증폭해서 정돈한 뒤 다른 쪽으로 전송</li>
<li>신호 감쇠 문제를 해결하여 장거리 통신 가능</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li>단순히 신호만 증폭 (데이터 내용은 확인하지 않음)</li>
<li>현재는 거의 사용되지 않음 (스위치나 다른 장비로 대체됨)</li>
</ul>
<hr />
<h3 id="1-3-리피터-허브-repeater-hub--dummy-hub">1-3. 리피터 허브 (Repeater Hub / Dummy Hub)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/723662fe-1fc6-493e-8d40-02f0727f45d7/image.png" /></p>
<p><strong>역할:</strong> 여러 장치를 연결하고 신호를 모든 포트로 전달</p>
<p><strong>동작:</strong></p>
<ul>
<li>전달받은 패킷(비트)의 복사본을 그대로 <strong>다른 모든 포트</strong>에 전송</li>
<li>어떤 포트에서 신호가 들어오면, 나머지 모든 포트로 브로드캐스트</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li>지능이 없는 &quot;멍청한(dumb)&quot; 장비</li>
<li>모든 장치가 같은 네트워크 대역폭을 공유 → <strong>충돌(Collision) 발생 가능</strong></li>
<li>보안 취약 (모든 장치가 모든 트래픽을 받음)</li>
<li>현재는 거의 사용되지 않음 (스위치로 대체됨)</li>
</ul>
<hr />
<h3 id="1-4-미디어-컨버터-media-converter">1-4. 미디어 컨버터 (Media Converter)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/915c69f7-b7c1-4984-849d-06a30cc4868c/image.png" /></p>
<p><strong>역할:</strong> 서로 다른 전송 매체 간의 신호 변환</p>
<p><strong>동작:</strong></p>
<ul>
<li><strong>전기 신호</strong>와 <strong>광 신호</strong>를 서로 교환</li>
<li>예: 구리선(UTP 케이블) ↔ 광섬유 케이블</li>
</ul>
<p><strong>사용 예:</strong></p>
<ul>
<li>연결 기기와 기기 사이에 미디어 컨버터를 추가</li>
<li>중간에서 광신호를 이용해 멀리까지 보내 네트워크를 연장</li>
</ul>
<p><strong>장점:</strong></p>
<ul>
<li>광섬유는 장거리 전송에 유리 (수 km 이상)</li>
<li>전자기 간섭(EMI)에 강함</li>
</ul>
<hr />
<h3 id="1-5-액세스-포인트-access-point-ap">1-5. 액세스 포인트 (Access Point, AP)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bd70e312-9b4a-4eaf-a5d4-91fc2966eae7/image.png" /></p>
<p><strong>역할:</strong> 유선 네트워크와 무선 네트워크를 연결</p>
<p><strong>동작:</strong></p>
<ul>
<li>패킷을 <strong>전파로 변조/복조</strong></li>
<li>무선 클라이언트(노트북, 스마트폰)를 유선 네트워크에 연결</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li>Wi-Fi 네트워크의 핵심 장비</li>
<li>SSID(네트워크 이름) 브로드캐스트</li>
<li>보안: WPA2, WPA3 등의 암호화 프로토콜 지원</li>
</ul>
<hr />
<h3 id="2-데이터링크-계층-layer-2">2. 데이터링크 계층 (Layer 2)</h3>
<p><strong>데이터링크 계층</strong>은 같은 네트워크 내에서 MAC 주소를 기반으로 프레임을 전달합니다.</p>
<hr />
<h3 id="2-1-브리지-bridge">2-1. 브리지 (Bridge)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2cadd8da-388e-47ca-819a-d0ee2c4a64d7/image.png" /></p>
<p>사진 출처 : <a href="https://docs.oracle.com/cd/E37933_01/html/E36608/rbridgesoverview.html">oracle</a>
<strong>역할:</strong> 포트와 포트 사이의 다리 역할, MAC 주소 기반 전송</p>
<p><strong>동작:</strong></p>
<ul>
<li><strong>MAC 주소 테이블</strong>로 주소를 관리하고 전송을 처리</li>
<li>목적지 MAC 주소를 확인하여 해당 포트로만 프레임 전송</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li>허브와 달리 <strong>선택적 전송</strong> (불필요한 트래픽 감소)</li>
<li>네트워크를 여러 세그먼트로 분할</li>
<li>충돌 도메인(Collision Domain) 분리</li>
</ul>
<p><strong>MAC 주소 학습 과정:</strong></p>
<ol>
<li>프레임 수신 시 송신자 MAC 주소를 테이블에 저장</li>
<li>목적지 MAC 주소가 테이블에 있으면 해당 포트로만 전송</li>
<li>목적지 MAC 주소가 테이블에 없으면 모든 포트로 플러딩(Flooding)</li>
</ol>
<hr />
<h3 id="2-2-l2-스위치-switching-hub">2-2. L2 스위치 (Switching Hub)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/79e0fd99-5236-48ac-b68f-e734f583608b/image.png" /></p>
<p><strong>역할:</strong> 브리지의 진화형, 다중 포트 지원</p>
<p><strong>동작:</strong></p>
<ul>
<li>단말에서 받아들인 프레임의 <strong>MAC 주소</strong>를 MAC 주소 테이블로 관리하고 전송</li>
<li>각 포트는 독립적인 대역폭을 가짐 (전이중 통신 지원)</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li><strong>기본 기능은 브리지와 동일</strong>하지만, 포트 수가 많고 성능이 향상됨</li>
<li>ASIC(Application-Specific Integrated Circuit) 하드웨어로 빠른 처리</li>
<li>VLAN(Virtual LAN) 기능 지원 → 논리적 네트워크 분할</li>
</ul>
<p><strong>MAC 주소 확인 방법:</strong></p>
<ul>
<li>Windows: <code>ipconfig /all</code></li>
<li>Linux/Mac: <code>ifconfig</code> 또는 <code>ip addr</code></li>
</ul>
<p><strong>MAC 주소 테이블 확인:</strong></p>
<ul>
<li>Cisco 스위치: <code>show mac address-table</code></li>
</ul>
<hr />
<h3 id="3-네트워크-계층-layer-3">3. 네트워크 계층 (Layer 3)</h3>
<p><strong>네트워크 계층</strong>은 네트워크와 네트워크를 연결하는 계층입니다.</p>
<hr />
<h3 id="3-1-라우터-router">3-1. 라우터 (Router)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b75e4480-2040-4beb-9cc1-0ba5d346e770/image.png" /></p>
<p><strong>역할:</strong> 서로 다른 네트워크 간의 패킷 전달</p>
<p><strong>동작:</strong></p>
<ol>
<li>단말로부터 받아들인 <strong>IP 패킷의 IP 주소</strong>를 확인</li>
<li><strong>라우팅 테이블(Routing Table)</strong>을 참조하여 최적의 경로 결정</li>
<li>해당 경로로 패킷을 <strong>릴레이(Relay)</strong> 방식으로 전송 → <strong>라우팅(Routing)</strong></li>
</ol>
<p><strong>주요 기능:</strong></p>
<ul>
<li><strong>라우팅:</strong> IP 패킷을 목적지까지 전달</li>
<li><strong>NAT(Network Address Translation):</strong> 사설 IP ↔ 공인 IP 주소 변환</li>
<li><strong>IPsec VPN:</strong> 인터넷 상에 가상적인 전용선(터널)을 만들어 안전한 통신</li>
<li><strong>PPPoE:</strong> ISP(인터넷 서비스 제공자)와의 연결 프로토콜</li>
</ul>
<p><strong>라우팅 방식:</strong></p>
<ul>
<li><strong>정적 라우팅(Static Routing):</strong> 관리자가 수동으로 경로 설정</li>
<li><strong>동적 라우팅(Dynamic Routing):</strong> RIP, OSPF, BGP 등의 프로토콜로 자동 경로 학습</li>
</ul>
<p><strong>라우팅 테이블 예시:</strong></p>
<pre><code>목적지 네트워크    넥스트 홉      인터페이스
192.168.1.0/24    직접 연결       eth0
10.0.0.0/8        192.168.1.1    eth0
0.0.0.0/0         192.168.1.254  eth0  (기본 게이트웨이)</code></pre><hr />
<h3 id="3-2-l3-스위치-layer-3-switch">3-2. L3 스위치 (Layer 3 Switch)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5bb01a9f-9bcf-4eeb-bbf2-0ceb3bcdc18e/image.png" /></p>
<p><strong>역할:</strong> 스위칭 + 라우팅 기능을 모두 제공</p>
<p><strong>동작:</strong></p>
<ul>
<li><strong>MAC 주소 테이블</strong>과 <strong>라우팅 테이블</strong>을 조합한 정보를 FPGA나 ASIC 등의 패킷 전송 처리 전용 하드웨어에 기록</li>
<li>그 정보를 기반으로 <strong>스위칭</strong> 또는 <strong>라우팅</strong>을 수행</li>
</ul>
<p><strong>특징:</strong></p>
<ul>
<li>같은 네트워크: L2 스위칭 (MAC 주소 기반)</li>
<li>다른 네트워크: L3 라우팅 (IP 주소 기반)</li>
<li>라우터보다 빠른 처리 속도 (하드웨어 기반)</li>
<li>주로 기업 내부 네트워크에서 사용</li>
</ul>
<p><strong>라우터 vs L3 스위치:</strong></p>
<table>
<thead>
<tr>
<th>특징</th>
<th>라우터</th>
<th>L3 스위치</th>
</tr>
</thead>
<tbody><tr>
<td>처리 방식</td>
<td>소프트웨어 기반</td>
<td>하드웨어(ASIC) 기반</td>
</tr>
<tr>
<td>속도</td>
<td>상대적으로 느림</td>
<td>매우 빠름</td>
</tr>
<tr>
<td>고급 기능</td>
<td>NAT, VPN, QoS 등 풍부</td>
<td>제한적</td>
</tr>
<tr>
<td>사용 환경</td>
<td>WAN, 인터넷 연결</td>
<td>LAN, 내부 네트워크</td>
</tr>
</tbody></table>
<hr />
<h3 id="4-트랜스포트-계층-layer-4">4. 트랜스포트 계층 (Layer 4)</h3>
<p><strong>트랜스포트 계층</strong>은 애플리케이션을 식별하고, 그 요건에 맞게 통신을 제어하는 계층입니다.</p>
<p>트랜스포트 계층에서 작동하는 기기는 <strong>TCP 또는 UDP의 헤더</strong>에 포함된 <strong>포트 번호</strong>에 기반하여 패킷을 전송합니다.</p>
<hr />
<h3 id="4-1-방화벽-firewall">4-1. 방화벽 (Firewall)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/086c550f-b34b-45e2-890e-47e13818c544/image.png" />
사진 출처 : <a href="https://ko.wikipedia.org/wiki/%EB%B0%A9%ED%99%94%EB%B2%BD_%28%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%29">위키백과</a>
<strong>역할:</strong> 네트워크 보안, 허가되지 않은 통신 차단</p>
<p><strong>동작:</strong></p>
<ul>
<li>단말 사이에 교환되는 패킷의 <strong>IP 주소</strong>나 <strong>포트 번호</strong>를 확인</li>
<li>미리 정의된 규칙(Rule)에 따라 통신을 <strong>허가</strong> 또는 <strong>차단</strong></li>
</ul>
<p><strong>동작 원리:</strong></p>
<ol>
<li>패킷 수신</li>
<li>송신지/목적지 IP 주소 확인</li>
<li>송신지/목적지 포트 번호 확인</li>
<li>방화벽 정책과 비교</li>
<li>허용(Allow) 또는 차단(Deny)</li>
</ol>
<p><strong>방화벽 정책 예시:</strong></p>
<pre><code>규칙 1: 외부 → 내부 웹서버(80번 포트) 허용
규칙 2: 외부 → 내부 SSH(22번 포트) 차단
규칙 3: 내부 → 외부 모든 트래픽 허용</code></pre><p><strong>방화벽 종류:</strong></p>
<ul>
<li><strong>패킷 필터링 방화벽:</strong> IP, 포트 번호 기반 필터링</li>
<li><strong>상태 기반 방화벽(Stateful):</strong> 연결 상태 추적</li>
<li><strong>프록시 방화벽:</strong> 중계 방식</li>
</ul>
<hr />
<h2 id="5-애플리케이션-계층-layer-7">5. 애플리케이션 계층 (Layer 7)</h2>
<p><strong>애플리케이션 계층</strong>은 사용자에게 애플리케이션을 제공하는 영역입니다.</p>
<hr />
<h3 id="5-1-차세대-방화벽-next-generation-firewall-ngfw">5-1. 차세대 방화벽 (Next-Generation Firewall, NGFW)</h3>
<p><strong>역할:</strong> 전통적인 방화벽의 진화형, 고급 보안 기능 통합</p>
<p><strong>특징:</strong></p>
<ul>
<li>IP 주소나 포트 번호뿐만 아니라, <strong>애플리케이션 레벨</strong>에서 다양한 정보를 해석</li>
<li>전통적인 방화벽보다 높은 차원의 보안, 운용성, 관리성 제공</li>
</ul>
<p><strong>주요 기능:</strong></p>
<ul>
<li><strong>애플리케이션 인식 및 제어:</strong> HTTP, FTP 등 프로토콜별 세밀한 제어</li>
<li><strong>침입 방지 시스템(IPS):</strong> 악성 트래픽 탐지 및 차단</li>
<li><strong>안티바이러스/안티멀웨어:</strong> 파일 스캔</li>
<li><strong>URL 필터링:</strong> 악성 웹사이트 차단</li>
<li><strong>SSL/TLS 복호화:</strong> 암호화된 트래픽 검사</li>
</ul>
<hr />
<h3 id="5-2-waf-web-application-firewall-웹-방화벽">5-2. WAF (Web Application Firewall, 웹 방화벽)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b38c9d61-193d-41c0-b19f-850ca4d53e2f/image.png" />
사진 출처: <a href="https://www.jungbo.net/security/?page=waf">정보넷</a>
<strong>역할:</strong> 웹 애플리케이션 보호</p>
<p><strong>동작:</strong></p>
<ul>
<li>클라이언트와 웹 서버 사이에서 교환되는 HTTP/HTTPS 트래픽을 <strong>애플리케이션 레벨</strong>에서 검사</li>
<li>필요에 따라 악성 요청을 차단</li>
</ul>
<p><strong>보호 대상 공격 (OWASP Top 10):</strong></p>
<ul>
<li><strong>SQL Injection:</strong> 데이터베이스 공격</li>
<li><strong>XSS(Cross-Site Scripting):</strong> 악성 스크립트 삽입</li>
<li><strong>CSRF(Cross-Site Request Forgery):</strong> 위조 요청</li>
<li><strong>파일 업로드 공격</strong></li>
<li><strong>경로 탐색(Path Traversal)</strong></li>
</ul>
<p><strong>참고:</strong> <a href="https://owasp.org/www-project-top-ten/">OWASP Top Ten</a></p>
<hr />
<h3 id="5-3-부하-분산-장치-load-balancer-l7-스위치">5-3. 부하 분산 장치 (Load Balancer, L7 스위치)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b3fad039-745e-42fc-a4f9-5ed766ce4749/image.png" /></p>
<p><strong>역할:</strong> 여러 서버로 트래픽을 분산하여 성능 향상 및 가용성 확보</p>
<p><strong>배경:</strong></p>
<ul>
<li>서버 1대로 처리할 수 있는 트래픽(통신 데이터)의 양은 제한적</li>
<li>대용량 트래픽 처리를 위해 여러 서버 필요</li>
</ul>
<p><strong>동작:</strong></p>
<ol>
<li>클라이언트로부터 받은 패킷을 <strong>부하 분산 방식(Load Balancing)</strong>에 따라 처리</li>
<li>뒤쪽에 있는 여러 서버로 트래픽을 나눔</li>
<li>시스템 전체적으로 처리 가능한 트래픽 양을 확장</li>
</ol>
<p><strong>부하 분산 알고리즘:</strong></p>
<ul>
<li><strong>라운드 로빈(Round Robin):</strong> 순서대로 분배</li>
<li><strong>최소 연결(Least Connection):</strong> 연결 수가 가장 적은 서버로 분배</li>
<li><strong>IP 해시(IP Hash):</strong> 클라이언트 IP 기반 고정 분배</li>
<li><strong>가중치(Weighted):</strong> 서버 성능에 따라 비율 조정</li>
</ul>
<p><strong>헬스 체크(Health Check):</strong></p>
<ul>
<li>정기적으로 서버 상태를 감시</li>
<li>장애가 발생한 서버를 부하 분산 대상에서 자동 제외</li>
<li>서비스 가용성 향상</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>클라이언트 요청 → L7 로드 밸런서
                    ├→ 웹서버 1 (정상)
                    ├→ 웹서버 2 (정상)
                    └→ 웹서버 3 (장애, 제외됨)</code></pre><hr />
<h2 id="6-모든-기기를-연결하기">6. 모든 기기를 연결하기</h2>
<p><strong>온프레미스 환경</strong>에서 HTTPS 웹 서버를 인터넷에 공개하는 경우의 일반적인 구성:</p>
<h3 id="네트워크-구성-순서-인터넷-→-웹서버">네트워크 구성 순서 (인터넷 → 웹서버):</h3>
<pre><code>인터넷
  ↓
미디어 컨버터 (광신호 ↔ 전기신호 변환)
  ↓
L3 스위치 (라우팅)
  ↓
방화벽 (보안, 접근 제어)
  ↓
L2 스위치 (스위칭)
  ↓
부하 분산 장치 (L7 스위치, 트래픽 분산)
  ↓
L2 스위치 (서버 연결)
  ↓
웹 서버 (HTTPS 서비스 제공)</code></pre><h3 id="각-단계의-역할">각 단계의 역할:</h3>
<ol>
<li><strong>미디어 컨버터:</strong> ISP로부터 온 광케이블을 전기 신호로 변환</li>
<li><strong>L3 스위치:</strong> 내부 네트워크로 라우팅</li>
<li><strong>방화벽:</strong> 외부 공격 차단, 허가된 트래픽만 통과</li>
<li><strong>L2 스위치:</strong> DMZ 영역 내부 스위칭</li>
<li><strong>부하 분산 장치:</strong> 여러 웹 서버로 트래픽 분산</li>
<li><strong>L2 스위치:</strong> 실제 웹 서버들과 연결</li>
<li><strong>웹 서버:</strong> 최종적으로 HTTPS 요청 처리</li>
</ol>
<hr />
<h3 id="7-용어-정리">7. 용어 정리</h3>
<p><strong>온프레미스(On-Premise):</strong></p>
<ul>
<li>자체 서버실에 물리적 서버를 구축하여 운영하는 방식</li>
<li>클라우드와 대비되는 개념</li>
<li>장점: 완전한 통제권, 보안</li>
<li>단점: 높은 초기 비용, 유지보수 부담</li>
</ul>
<p><strong>DMZ (Demilitarized Zone):</strong></p>
<ul>
<li>내부 네트워크와 외부 네트워크 사이의 중간 영역</li>
<li>웹 서버, 메일 서버 등 외부에 공개되는 서버를 배치</li>
<li>내부 네트워크 보호 목적</li>
</ul>
<p><strong>ASIC (Application-Specific Integrated Circuit):</strong></p>
<ul>
<li>특정 용도를 위해 설계된 주문형 반도체</li>
<li>L2/L3 스위치에서 빠른 패킷 처리를 위해 사용</li>
</ul>
<p><strong>FPGA (Field-Programmable Gate Array):</strong></p>
<ul>
<li>프로그래밍 가능한 하드웨어</li>
<li>ASIC보다 유연하지만 성능은 약간 낮음</li>
</ul>