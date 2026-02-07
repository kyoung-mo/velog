<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8868d84f-7d66-48db-8844-86c682180eb2/image.png" /></p>
<hr />
<h2 id="📚-목차">📚 목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-tcp%EB%9E%80">1. TCP란?</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-tcp-%EC%BB%A4%EB%84%A5%EC%85%98-tcp-connection">2. TCP 커넥션 (TCP Connection)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-tcp-%ED%8C%A8%ED%82%B7-%ED%8F%AC%EB%A7%B7">3. TCP 패킷 포맷</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-tcp-%EC%83%81%ED%83%9C-%EC%A0%84%EC%9D%B4-3%EB%8B%A8%EA%B3%84-%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4">4. TCP 상태 전이 3단계 프로세스</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-tcp-%EA%B3%A0%EA%B8%89-%EC%98%B5%EC%85%98-%EA%B8%B0%EB%8A%A5">5. TCP 고급 옵션 기능</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-%EB%B0%A9%ED%99%94%EB%B2%BD%EC%9D%98-%EB%8F%99%EC%9E%91-tcp">6. 방화벽의 동작 (TCP)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-%EC%A0%95%EB%A6%AC">7. 정리</a></li>
</ol>
<hr />
<h3 id="1-tcp란">1. TCP란?</h3>
<p><strong>TCP (Transmission Control Protocol)</strong> = <strong>전송 제어 프로토콜</strong></p>
<h4 id="1-1-주요-특징">1-1. 주요 특징</h4>
<ul>
<li><strong>신뢰성 있는 연결형 프로토콜</strong></li>
<li>데이터 전송의 신뢰성을 보장</li>
<li>순서 보장, 오류 검출, 재전송 기능 제공</li>
</ul>
<h4 id="1-2-사용-분야">1-2. 사용 분야</h4>
<ul>
<li><strong>메일</strong> (SMTP, POP3, IMAP)</li>
<li><strong>파일 전송</strong> (FTP, SFTP)</li>
<li><strong>웹 브라우저</strong> (HTTP, HTTPS)</li>
<li>데이터 전송의 신뢰성을 요구하는 모든 애플리케이션</li>
</ul>
<p><strong>참고:</strong></p>
<ul>
<li>최근 유튜브, 페이스북 등은 <strong>QUIC(Quick UDP Internet Connections)</strong> 사용 (UDP 기반)</li>
<li>2020년 기준 인터넷 트래픽의 <strong>80% 이상이 TCP</strong></li>
</ul>
<hr />
<h3 id="2-tcp-커넥션-tcp-connection">2. TCP 커넥션 (TCP Connection)</h3>
<h4 id="2-1-개념">2-1. 개념</h4>
<ul>
<li>애플리케이션 데이터를 송신하기 전에 확립하는 <strong>논리적인 통신로</strong></li>
<li><strong>송신 파이프</strong>와 <strong>수신 파이프</strong>로 구성</li>
<li><strong>전이중(Full-Duplex)</strong> 통신: 양방향 동시 통신 가능</li>
</ul>
<h4 id="2-2-동작-방식">2-2. 동작 방식</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9d9c1070-ae1f-4a65-a327-f37e9c4fa3ff/image.png" /></p>
<pre><code>클라이언트 ←─────────→ 서버
          송신 파이프
          수신 파이프
          (동시 사용 가능)</code></pre><hr />
<h3 id="3-tcp-패킷-포맷">3. TCP 패킷 포맷</h3>
<ul>
<li><strong>표준</strong>: RFC 793 &quot;Transmission Control Protocol&quot;</li>
<li><strong>IP 프로토콜 번호</strong>: 6</li>
<li><strong>헤더 길이</strong>: 최소 20바이트 (160비트), 최대 60바이트</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/07d49178-95c8-4198-b5e4-1a3e7388b19f/image.png" /></p>
<hr />
<h3 id="3-1-송신지수신지-포트-번호-각-16비트">3-1. 송신지/수신지 포트 번호 (각 16비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>애플리케이션(프로세스)의 식별</li>
<li>UDP와 동일한 개념</li>
</ul>
<p><strong>동작:</strong></p>
<ul>
<li><strong>클라이언트(송신지)</strong>: OS가 자동으로 무작위 할당 (동적 포트, 49152~65535)</li>
<li><strong>서버(수신지)</strong>: Well-Known Port 사용 (예: HTTP=80, HTTPS=443)</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>클라이언트 → 서버
송신지 포트: 54321 (무작위)
수신지 포트: 443 (HTTPS)</code></pre><hr />
<h3 id="3-2-시퀀스-번호-sequence-number-32비트">3-2. 시퀀스 번호 (Sequence Number, 32비트)</h3>
<h3 id="역할">역할</h3>
<ul>
<li>TCP 세그먼트를 <strong>올바른 순서로 정렬</strong></li>
<li>데이터의 순서 보장
<img alt="" src="https://velog.velcdn.com/images/mommers/post/8732c6b4-400b-48d7-936f-bf3afc150200/image.png" /></li>
</ul>
<hr />
<h3 id="동작">동작</h3>
<ol>
<li><strong>초기 시퀀스 번호(ISN, Initial Sequence Number)</strong> 설정<ul>
<li>3-way handshake 시 무작위 값으로 시작</li>
</ul>
</li>
<li>데이터 송신 시마다 <strong>송신한 바이트 수만큼 증가</strong>
<img alt="" src="https://velog.velcdn.com/images/mommers/post/24f0fb83-bc25-4f2b-aa04-44795ce51a55/image.png" /></li>
</ol>
<p><strong>예시:</strong></p>
<pre><code class="language-bash">ISN = 1000 (무작위 초기값)

세그먼트 1: Seq=1000, 데이터 100바이트 전송
세그먼트 2: Seq=1100, 데이터 200바이트 전송
세그먼트 3: Seq=1300, 데이터 150바이트 전송</code></pre>
<p><strong>수신자 동작:</strong></p>
<ul>
<li>시퀀스 번호로 정렬</li>
<li>순서대로 애플리케이션에 전달</li>
</ul>
<hr />
<h3 id="3-3-확인-응답-번호-acknowledgment-number-ack-번호-32비트">3-3. 확인 응답 번호 (Acknowledgment Number, ACK 번호, 32비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>수신자가 다음에 받을 것으로 <strong>기대하는 시퀀스 번호</strong></li>
<li>&quot;여기까지 잘 받았어, 다음 것 보내!&quot;</li>
</ul>
<p><strong>조건:</strong></p>
<ul>
<li><strong>ACK 플래그가 1</strong>일 때만 유효</li>
</ul>
<p><strong>동작:</strong></p>
<pre><code>송신자 → 수신자
Seq=1000, 데이터 100바이트 전송

수신자 → 송신자
ACK=1100 (다음에 1100번부터 보내줘!)</code></pre><hr />
<h3 id="3-4-데이터-오프셋-data-offset-4비트">3-4. 데이터 오프셋 (Data Offset, 4비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>TCP 헤더의 길이를 나타냄</li>
<li>&quot;어디까지가 헤더고, 어디부터가 데이터인지&quot;</li>
</ul>
<p><strong>단위:</strong></p>
<ul>
<li><strong>4바이트(32비트) 단위</strong>로 표시</li>
</ul>
<p><strong>값:</strong></p>
<ul>
<li>최소값: <code>5</code> (5 × 4 = 20바이트, 옵션 없음)</li>
<li>최대값: <code>15</code> (15 × 4 = 60바이트, 옵션 40바이트)</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>Data Offset = 5 → 헤더 20바이트
Data Offset = 8 → 헤더 32바이트 (옵션 12바이트 포함)</code></pre><hr />
<h3 id="3-5-컨트롤-비트-control-flags-8비트">3-5. 컨트롤 비트 (Control Flags, 8비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>TCP 커넥션의 상태를 제어</li>
</ul>
<p><strong>8개 플래그:</strong></p>
<table>
<thead>
<tr>
<th>비트</th>
<th>이름</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>CWR</td>
<td>Congestion Window Reduced</td>
<td>혼잡 윈도우 축소</td>
</tr>
<tr>
<td>ECE</td>
<td>ECN-Echo</td>
<td>명시적 혼잡 통지 에코</td>
</tr>
<tr>
<td>URG</td>
<td>Urgent</td>
<td>긴급 포인터 유효</td>
</tr>
<tr>
<td><strong>ACK</strong></td>
<td><strong>Acknowledgment</strong></td>
<td><strong>확인 응답 번호 유효</strong></td>
</tr>
<tr>
<td>PSH</td>
<td>Push</td>
<td>즉시 애플리케이션에 전달</td>
</tr>
<tr>
<td>RST</td>
<td>Reset</td>
<td>커넥션 강제 종료</td>
</tr>
<tr>
<td><strong>SYN</strong></td>
<td><strong>Synchronize</strong></td>
<td><strong>커넥션 확립 요청</strong></td>
</tr>
<tr>
<td><strong>FIN</strong></td>
<td><strong>Finish</strong></td>
<td><strong>커넥션 종료 요청</strong></td>
</tr>
</tbody></table>
<p><strong>주요 플래그 사용:</strong></p>
<ul>
<li><strong>SYN</strong>: 커넥션 시작</li>
<li><strong>ACK</strong>: 데이터 수신 확인</li>
<li><strong>FIN</strong>: 커넥션 종료</li>
<li><strong>RST</strong>: 비정상 종료</li>
</ul>
<hr />
<h3 id="3-6-윈도우-크기-window-size-16비트">3-6. 윈도우 크기 (Window Size, 16비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>수신자가 받을 수 있는 데이터 크기를 송신자에게 알림</li>
<li><strong>흐름 제어(Flow Control)</strong>에 사용</li>
</ul>
<p><strong>의미:</strong></p>
<ul>
<li>수신자 버퍼에 남은 공간</li>
<li>&quot;확인 응답을 기다리지 않고 보낼 수 있는 데이터 크기&quot;</li>
</ul>
<p><strong>범위:</strong></p>
<ul>
<li>최소: 0 (더 이상 받을 수 없음, 잠시 기다려!)</li>
<li>최대: 65,535바이트 (2^16 - 1)</li>
</ul>
<p><strong>예시:</strong></p>
<pre><code>Window Size = 8192바이트
→ 송신자는 ACK 없이 최대 8192바이트까지 전송 가능</code></pre><hr />
<h3 id="3-7-체크섬-checksum-16비트">3-7. 체크섬 (Checksum, 16비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>TCP 세그먼트의 <strong>정합성(무결성) 검사</strong></li>
<li>전송 중 데이터가 손상되었는지 확인</li>
</ul>
<p><strong>동작:</strong></p>
<ul>
<li><strong>1의 보수 연산</strong> 사용</li>
<li>TCP 헤더 + 페이로드 + 의사 헤더(Pseudo Header) 포함</li>
</ul>
<p><strong>의사 헤더:</strong></p>
<pre><code>- 송신지 IP 주소
- 수신지 IP 주소
- 프로토콜 번호 (6)
- TCP 세그먼트 길이</code></pre><hr />
<h3 id="3-8-긴급-포인터-urgent-pointer-16비트">3-8. 긴급 포인터 (Urgent Pointer, 16비트)</h3>
<p><strong>역할:</strong></p>
<ul>
<li>긴급 데이터의 위치를 가리킴</li>
</ul>
<p><strong>조건:</strong></p>
<ul>
<li><strong>URG 플래그가 1</strong>일 때만 유효</li>
</ul>
<p><strong>사용 예:</strong></p>
<ul>
<li>Telnet에서 Ctrl+C (강제 중단)</li>
<li>현재는 거의 사용 안 함</li>
</ul>
<hr />
<h3 id="3-9-옵션-options-가변-길이">3-9. 옵션 (Options, 가변 길이)</h3>
<ul>
<li>TCP 확장 기능 제공</li>
<li>4바이트(32비트) 단위로 변화</li>
<li>다양한 옵션 존재
<img alt="" src="https://velog.velcdn.com/images/mommers/post/9bc8e670-1c0b-4312-9644-27028842e817/image.png" /></li>
</ul>
<hr />
<h3 id="mss-maximum-segment-size">MSS (Maximum Segment Size)</h3>
<p><strong>정의:</strong></p>
<ul>
<li>TCP 페이로드(애플리케이션 데이터)의 최대 크기</li>
<li>MTU는 IP 패킷의 최대 크기</li>
</ul>
<p><strong>계산:</strong></p>
<pre><code class="language-bash">IPv4: MSS = MTU - 40바이트 (IP 헤더 20 + TCP 헤더 20)

예시:
MTU = 1500바이트 
//       ㄴ IP 패킷의 최대 크기
MSS = 1500 - 40 = 1460바이트
//                  ㄴ 애플리케이션 데이터의 최대 크기</code></pre>
<p><strong>동작:</strong></p>
<ul>
<li>3-way handshake 시 서로 지원하는 MSS 값 교환</li>
<li>작은 값 사용</li>
</ul>
<p><strong>관계:</strong></p>
<pre><code>┌─────────────────────────────────────┐
│          MTU (1500바이트)            │
├──────────┬───────────┬──────────────┤
│ IP 헤더  │ TCP 헤더  │   MSS        │
│ (20바이트)│(20바이트) │ (1460바이트) │
└──────────┴───────────┴──────────────┘</code></pre><hr />
<h3 id="sack-selective-acknowledgment">SACK (Selective Acknowledgment)</h3>
<ul>
<li><strong>선택적 확인 응답</strong></li>
<li>사라진 TCP 세그먼트만 재전송</li>
<li>RFC 2018 &quot;TCP Selective Acknowledgment Options&quot;
<img alt="" src="https://velog.velcdn.com/images/mommers/post/d90f677e-daa5-49f3-8f1b-a48a61603e23/image.png" /></li>
</ul>
<hr />
<h3 id="4-tcp-상태-전이-3단계-프로세스">4. TCP 상태 전이 3단계 프로세스</h3>
<p>TCP 커넥션은 3단계로 구성:</p>
<ol>
<li><strong>접속 시작 단계</strong> (Connection Establishment)</li>
<li><strong>접속 확립 단계</strong> (Data Transfer)</li>
<li><strong>접속 종료 단계</strong> (Connection Termination)</li>
</ol>
<hr />
<h3 id="4-1-접속-시작-단계-3-way-handshake⭐">4-1. 접속 시작 단계: 3-Way Handshake⭐</h3>
<ul>
<li>TCP 커넥션 확립</li>
<li>양측의 시퀀스 번호 동기화
<img alt="" src="https://velog.velcdn.com/images/mommers/post/33a9ab06-04c8-4773-b2e8-bda04dde4377/image.png" /></li>
</ul>
<p><strong>상태:</strong></p>
<ul>
<li><strong>LISTEN</strong>: 연결 요청 대기</li>
<li><strong>SYN_SENT</strong>: SYN 전송 후 대기</li>
<li><strong>SYN_RCVD</strong>: SYN 수신 후 SYN+ACK 전송</li>
<li><strong>ESTABLISHED</strong>: 연결 확립 완료</li>
</ul>
<hr />
<h3 id="4-2-접속-확립-단계-데이터-전송">4-2. 접속 확립 단계: 데이터 전송</h3>
<p>이 단계에서 TCP는 3가지 주요 메커니즘 사용:</p>
<h3 id="1-흐름-제어-flow-control---슬라이딩-윈도우">1) 흐름 제어 (Flow Control) - 슬라이딩 윈도우</h3>
<ul>
<li>수신자가 처리할 수 있는 속도로 데이터 전송</li>
<li>버퍼 오버플로 방지
<img alt="" src="https://velog.velcdn.com/images/mommers/post/bf01907c-5fd5-443b-8544-add12e09420a/image.png" /></li>
</ul>
<hr />
<h3 id="2-혼잡-제어-congestion-control">2) 혼잡 제어 (Congestion Control)</h3>
<ul>
<li>네트워크 혼잡 방지</li>
<li>패킷 손실 최소화</li>
</ul>
<p><strong>문제 상황:</strong>
<img alt="" src="https://velog.velcdn.com/images/mommers/post/1ef3d0ad-7b62-4b35-badd-02046d2f2b28/image.png" /></p>
<p><strong>해결:</strong>
<img alt="" src="https://velog.velcdn.com/images/mommers/post/914acd02-fa6d-4fcc-9385-65fd3faa4e61/image.png" /></p>
<p><strong>주요 알고리즘:</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9d0d4123-3c38-4013-b02a-577906d95092/image.png" /></p>
<p><strong>동작 단계:</strong></p>
<ol>
<li><strong>Slow Start</strong>: 지수적 증가 (1 → 2 → 4 → 8...)</li>
<li><strong>Congestion Avoidance</strong>: 선형 증가 (n → n+1 → n+2...)</li>
<li><strong>Fast Retransmit</strong>: 빠른 재전송</li>
<li><strong>Fast Recovery</strong>: 빠른 회복</li>
</ol>
<hr />
<h3 id="3-재전송-제어-retransmission-control">3) 재전송 제어 (Retransmission Control)</h3>
<ul>
<li>손실된 세그먼트 재전송</li>
<li>신뢰성 보장</li>
<li>두 가지 방법이 존재</li>
</ul>
<hr />
<h3 id="a-중복-ack-duplicate-ack-→-fast-retransmit">a) 중복 ACK (Duplicate ACK) → Fast Retransmit</h3>
<ul>
<li>중복 ACK <strong>3개</strong> 수신 시 즉시 재전송
<img alt="" src="https://velog.velcdn.com/images/mommers/post/855d2101-5142-4d61-97e1-44920aa20d49/image.png" /></li>
</ul>
<hr />
<h4 id="b-재전송-타임아웃-retransmission-timeout-rto">b) 재전송 타임아웃 (Retransmission Timeout, RTO)</h4>
<p><strong>RTO 계산:</strong></p>
<ul>
<li>RTT(Round Trip Time) 기반</li>
<li>동적으로 조정
<img alt="" src="https://velog.velcdn.com/images/mommers/post/6ba749e0-8c8d-4016-bff4-dedd6ac8ea64/image.png" /></li>
</ul>
<hr />
<h3 id="4-3-접속-종료-단계-4-way-handshake">4-3. 접속 종료 단계: 4-Way Handshake</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a06abf98-72a1-478c-b017-42eebcf88576/image.png" /></p>
<p><strong>상태:</strong></p>
<ul>
<li><strong>FIN_WAIT_1</strong>: FIN 전송 후 ACK 대기</li>
<li><strong>FIN_WAIT_2</strong>: ACK 수신 후 상대 FIN 대기</li>
<li><strong>CLOSE_WAIT</strong>: FIN 수신 후 애플리케이션 종료 대기</li>
<li><strong>LAST_ACK</strong>: FIN 전송 후 ACK 대기</li>
<li><strong>TIME_WAIT</strong>: 2MSL(Maximum Segment Lifetime) 대기</li>
<li><strong>CLOSED</strong>: 완전 종료</li>
</ul>
<p><strong>TIME_WAIT의 목적:</strong></p>
<ul>
<li>지연된 패킷 처리</li>
<li>마지막 ACK가 손실되었을 경우 재전송 대비</li>
</ul>
<hr />
<h2 id="5-tcp-고급-옵션-기능">5. TCP 고급 옵션 기능</h2>
<h3 id="5-1-tcp-fast-open-tfo">5-1. TCP Fast Open (TFO)</h3>
<ul>
<li>3-way handshake 시간 단축
<img alt="" src="https://velog.velcdn.com/images/mommers/post/6f4b6f3e-ad73-43ae-a270-f09ae5ea1e90/image.png" /></li>
</ul>
<p><strong>장점:</strong></p>
<ul>
<li>연결 확립 시간 감소</li>
<li>웹 페이지 로딩 속도 향상</li>
</ul>
<hr />
<h3 id="5-2-nagle-알고리즘">5-2. Nagle 알고리즘</h3>
<ul>
<li>작은 패킷 전송 방지</li>
<li>네트워크 효율 향상
<img alt="" src="https://velog.velcdn.com/images/mommers/post/8846093f-bb61-4ccb-8094-be7625d06b44/image.png" /></li>
</ul>
<p><strong>조건:</strong></p>
<ul>
<li>미전송 데이터가 MSS 미만이면 대기</li>
<li>ACK가 오면 즉시 전송</li>
</ul>
<p><strong>문제:</strong></p>
<ul>
<li>실시간 애플리케이션에서는 지연 발생</li>
<li>TCP_NODELAY 옵션으로 비활성화 가능</li>
</ul>
<hr />
<h3 id="5-3-지연-ack-delayed-ack">5-3. 지연 ACK (Delayed ACK)</h3>
<ul>
<li>ACK 전송 횟수 감소</li>
<li>네트워크 트래픽 절감
<img alt="" src="https://velog.velcdn.com/images/mommers/post/8daa9e48-274f-4f78-a0f5-2e07607795f0/image.png" /></li>
</ul>
<p><strong>문제:</strong></p>
<ul>
<li>Nagle 알고리즘과 함께 사용 시 성능 저하</li>
</ul>
<hr />
<h3 id="5-4-early-retransmit">5-4. Early Retransmit</h3>
<ul>
<li>중복 ACK 3개를 기다리지 않고 조기 재전송
<img alt="" src="https://velog.velcdn.com/images/mommers/post/3a433cdd-32be-4573-900e-7ac996eb58cd/image.png" /></li>
</ul>
<p><strong>조건:</strong></p>
<ul>
<li>미전송 데이터가 적을 때</li>
<li>중복 ACK 3개를 받기 어려운 상황
<img alt="" src="https://velog.velcdn.com/images/mommers/post/bf2945b6-3e56-49d6-af40-0b3d7319ca40/image.png" /></li>
</ul>
<hr />
<h3 id="5-5-tail-loss-probe-tlp">5-5. Tail Loss Probe (TLP)</h3>
<ul>
<li>마지막 세그먼트 손실 시 빠른 재전송
<img alt="" src="https://velog.velcdn.com/images/mommers/post/39cc88d1-dd46-4ee8-8721-3eb2d74797e7/image.png" /></li>
</ul>
<hr />
<h3 id="6-방화벽의-동작-tcp">6. 방화벽의 동작 (TCP)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2db32447-7c2f-4588-9e11-ec915b669f9c/image.png" /></p>
<h3 id="6-1-스테이트풀-인스펙션-stateful-inspection">6-1. 스테이트풀 인스펙션 (Stateful Inspection)</h3>
<p><strong>개념:</strong></p>
<ul>
<li>커넥션 상태를 추적하여 통신 제어</li>
<li>5-tuple로 커넥션 식별</li>
</ul>
<p><strong>5-tuple:</strong></p>
<ol>
<li>송신지 IP 주소</li>
<li>수신지 IP 주소</li>
<li>프로토콜 (TCP=6)</li>
<li>송신지 포트 번호</li>
<li>수신지 포트 번호</li>
</ol>
<hr />
<h3 id="6-2-필터링-규칙--커넥션-테이블">6-2. 필터링 규칙 &amp; 커넥션 테이블</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/629ad610-6870-4bc8-b9f9-8e6cb9f7a342/image.png" /></p>
<hr />
<h3 id="동작-1"><strong>동작:</strong></h3>
<h4 id="1-syn-패킷-수신-클라이언트-→-서버">1) SYN 패킷 수신 (클라이언트 → 서버)</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a6fa11ff-05f6-4087-96b3-a91389992f3f/image.png" /></p>
<h4 id="2-거부reject인-경우">2) 거부(Reject)인 경우</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b4674d12-3306-408a-b63f-54ddcff3d58e/image.png" /></p>
<h4 id="3-드롭drop인-경우">3) 드롭(Drop)인 경우</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/431001a4-166b-4d2c-b464-dc3a18f34a92/image.png" /></p>
<hr />
<h3 id="6-3-반환-통신-제어">6-3. 반환 통신 제어</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6ca4e261-0de5-40eb-87ef-c83265496fee/image.png" /></p>
<p><strong>자동 생성된 규칙:</strong></p>
<pre><code>Inside → Outside, TCP, 송신지 포트 80 → 허가</code></pre><hr />
<h3 id="6-4-커넥션-종료-처리">6-4. 커넥션 종료 처리</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/66ff4e2f-487b-448c-8825-817a571cd370/image.png" /></p>
<hr />
<h3 id="tcp-vs-udp-비교">TCP vs UDP 비교</h3>
<p>TCP는 신뢰성을 보장하는 연결형 프로토콜입니다. 빠른 전송이 필요한 경우 UDP를 사용하며, 신뢰성이 중요한 경우 TCP를 사용합니다.</p>
<table>
<thead>
<tr>
<th>특징</th>
<th>TCP</th>
<th>UDP</th>
</tr>
</thead>
<tbody><tr>
<td>연결</td>
<td>연결형</td>
<td>비연결형</td>
</tr>
<tr>
<td>신뢰성</td>
<td>보장</td>
<td>미보장</td>
</tr>
<tr>
<td>순서</td>
<td>보장</td>
<td>미보장</td>
</tr>
<tr>
<td>속도</td>
<td>느림</td>
<td>빠름</td>
</tr>
<tr>
<td>용도</td>
<td>웹, 메일, 파일 전송</td>
<td>스트리밍, DNS, VoIP</td>
</tr>
</tbody></table>
<hr />
<h2 id="7-정리">7. 정리</h2>
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
<td>TCP (Transmission Control Protocol)</td>
</tr>
<tr>
<td><strong>계층</strong></td>
<td>Layer 4 (트랜스포트 계층)</td>
</tr>
<tr>
<td><strong>특징</strong></td>
<td>연결형, 신뢰성, 순서 보장, 흐름 제어</td>
</tr>
<tr>
<td><strong>헤더 크기</strong></td>
<td>최소 20바이트, 최대 60바이트</td>
</tr>
<tr>
<td><strong>IP 프로토콜 번호</strong></td>
<td>6</td>
</tr>
<tr>
<td><strong>주요 필드</strong></td>
<td>포트, Seq, ACK, Window, Flags</td>
</tr>
<tr>
<td><strong>연결 확립</strong></td>
<td>3-way handshake (SYN, SYN+ACK, ACK)</td>
</tr>
<tr>
<td><strong>연결 종료</strong></td>
<td>4-way handshake (FIN, ACK, FIN, ACK)</td>
</tr>
</tbody></table>
<h3 id="기억할-점">기억할 점</h3>
<ul>
<li><strong>3-way handshake</strong>: SYN → SYN+ACK → ACK</li>
<li><strong>4-way handshake</strong>: FIN → ACK → FIN → ACK</li>
<li><strong>시퀀스 번호</strong>: 순서 보장</li>
<li><strong>ACK 번호</strong>: 다음에 받을 것 기대</li>
<li><strong>윈도우 크기</strong>: 흐름 제어</li>
<li><strong>MSS</strong>: TCP 데이터 최대 크기 = MTU - 40</li>
<li><strong>SACK</strong>: 선택적 재전송</li>
<li><strong>방화벽</strong>: 5-tuple + 상태 추적</li>
</ul>
<blockquote>
<p><em>Reference : <a href="http://www.tcpipguide.com/free/t_TCPConnectionTermination-4.htm">http://www.tcpipguide.com/free/t_TCPConnectionTermination-4.htm</a></em></p>
</blockquote>