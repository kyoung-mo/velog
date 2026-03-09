<h1 id="can-기반-분산-ecu-무인-배달-차량-시스템">CAN 기반 분산 ECU 무인 배달 차량 시스템</h1>
<h2 id="프로젝트-전체-정리-v90">프로젝트 전체 정리 v9.0</h2>
<p><strong>최종 업데이트: 2026년 3월 8일</strong></p>
<hr />
<h2 id="1-프로젝트-개요">1. 프로젝트 개요</h2>
<h3 id="한-줄-요약">한 줄 요약</h3>
<blockquote>
<p><strong>[ STM32 × 2 + Raspberry Pi × 3 ] 분산 ECU 아키텍처</strong>로 OpenCV 라인트레이싱 기반 자율 주행, PIN 인증 화물함 제어, Qt 기반 주문 클라이언트, MQTT 실시간 관제를 구현하는 무인 배달 차량 시스템</p>
</blockquote>
<h3 id="목적">목적</h3>
<p>실제 차량의 ECU 분산 구조(주행 / 미션 / 화물함)를 RC카로 재현하여 CAN 통신 기반 임베디드 시스템 설계 역량을 검증한다.</p>
<h3 id="비즈니스-가치">비즈니스 가치</h3>
<p>음식 배달, 캠퍼스 내 무인 배송, 물류 창고 자동화 등 반복적인 배달 업무를 자동화한다.
수신자 PIN 인증 기반 화물함 제어로 분실·오배달 사고를 원천 차단하여 배달 신뢰성을 확보한다.</p>
<h3 id="핵심-기술-선택-근거">핵심 기술 선택 근거</h3>
<table>
<thead>
<tr>
<th>기술</th>
<th>선택 이유</th>
</tr>
</thead>
<tbody><tr>
<td>CAN 통신 (250 kbps)</td>
<td>주행/미션/화물함 ECU 분리, 단일 버스로 확장 가능. 버스 점유율 1% 미만</td>
</tr>
<tr>
<td>STM32 주행 ECU (C)</td>
<td>모터 PWM / 엔코더 / PID는 마이크로초 정밀도 필요 — RPi로 대체 불가</td>
</tr>
<tr>
<td>RPi1 미션 ECU (C++)</td>
<td>OpenCV 라인트레이싱 + ArUco 마커 인식 + 복잡한 미션 로직 — MCU 처리 불가</td>
</tr>
<tr>
<td>STM103 화물함 ECU (C)</td>
<td>CAN + GPIO + I2C + PWM만 필요. bxCAN 내장으로 MCP2515 불필요. 인터럽트 기반 실시간 처리</td>
</tr>
<tr>
<td>MQTT</td>
<td>다수 차량 확장 시 브로커 연결만으로 통신 가능. 차량당 연결 1개(RPi1)로 관리 단순화</td>
</tr>
<tr>
<td>스키드 스티어링</td>
<td>서보 조향 불필요. L298N 1개로 좌우 바퀴를 탱크 방식으로 제어</td>
</tr>
<tr>
<td>ArUco 마커</td>
<td>카메라 1대로 라인트레이싱과 목적지 인식을 동시 처리. ID별 목적지 구분</td>
</tr>
<tr>
<td>PIN 인증</td>
<td>주문 시 4자리 설정, 수령 시 키패드 입력으로 수신자만 화물함 접근 가능</td>
</tr>
</tbody></table>
<hr />
<h2 id="2-전체-시스템-구조">2. 전체 시스템 구조</h2>
<h3 id="2-1-노드-구성">2-1. 노드 구성</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>보드</th>
<th>위치</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>STM32</td>
<td>B-L475E-IOT01A (STM32L4)</td>
<td>RC카 탑재</td>
<td>주행 ECU — 모터/엔코더/PID</td>
</tr>
<tr>
<td>RPi1</td>
<td>Raspberry Pi</td>
<td>RC카 탑재</td>
<td>미션 ECU — 라인트레이싱/ArUco/미션 로직/MQTT 게이트웨이</td>
</tr>
<tr>
<td>STM103</td>
<td>STM32F103 독립 보드</td>
<td>RC카 탑재</td>
<td>화물함 ECU — PIN 인증/서보/LCD/키패드</td>
</tr>
<tr>
<td>RPi3</td>
<td>Raspberry Pi</td>
<td>오프보드 (서버)</td>
<td>MQTT 브로커 / 관제 / DB</td>
</tr>
<tr>
<td>RPi4</td>
<td>Raspberry Pi</td>
<td>오프보드 (클라이언트)</td>
<td>Qt 주문 클라이언트 / 5인치 터치 디스플레이</td>
</tr>
<tr>
<td>서브 STM103</td>
<td>STM32F103 독립 보드</td>
<td>개발용</td>
<td>RPi1 대용 CAN 테스트 시뮬레이터</td>
</tr>
</tbody></table>
<h3 id="2-2-통신-구조">2-2. 통신 구조</h3>
<pre><code>┌─────────────────────────────────────────────┐
│               RC카 (온보드)                  │
│                                             │
│  STM32 (B-L475E) ─────┐                    │
│  (주행 ECU)             │                    │
│                       CAN 버스 (250 kbps)   │
│  RPi1 ────────────────┤                    │
│  (미션 ECU)             │   Wi-Fi/MQTT       │
│                       │   └──────────────── ┼──→ RPi3 (서버)
│  STM103 ──────────────┘                    │         │
│  (화물함 ECU)                                │         │ MQTT
└─────────────────────────────────────────────┘     RPi4 (클라이언트)

온보드 CAN:    STM32 ↔ RPi1 ↔ STM103  ← 단일 CAN 버스 250 kbps
오프보드 MQTT: RPi1  ↔ RPi3           ← 무선 (차량당 단일 연결)
               RPi3  ↔ RPi4           ← 무선</code></pre><h3 id="2-3-각-노드의-역할-분담-원칙">2-3. 각 노드의 역할 분담 원칙</h3>
<ul>
<li><strong>STM32 주행 ECU</strong>: &quot;판단하지 않는다.&quot; 명령 수행 + 센서 데이터 수집만 담당</li>
<li><strong>RPi1 미션 ECU</strong>: &quot;모든 판단은 여기서 한다.&quot; 서버와의 통신도 RPi1만 담당</li>
<li><strong>STM103 화물함 ECU</strong>: 주행 ECU와 완전 독립된 보안 영역. CAN만 사용. 외부 네트워크 직접 연결 없음</li>
<li><strong>RPi3 서버</strong>: &quot;실시간 제어에 절대 관여하지 않는다.&quot; 이벤트 기반 데이터 중계 및 저장</li>
<li><strong>RPi4 클라이언트</strong>: 고객 주문 접수 및 PIN 설정</li>
</ul>
<hr />
<h2 id="3-전체-배달-시나리오">3. 전체 배달 시나리오</h2>
<h3 id="3-1-전체-흐름-요약">3-1. 전체 흐름 요약</h3>
<pre><code>[① 고객 주문]
  RPi4 (Qt UI) → 목적지 + PIN 설정
  RPi4 → MQTT → RPi3: 주문정보 + PIN
  RPi3: DB 저장
  RPi3 → MQTT → RPi1: destination + pin + order_id
  RPi1 → CAN 0x012 → STM103: PIN(4자리) + 목적지 코드 전달
  RPi1: S_WAIT_CMD → S_FOLLOW (출발)

[② 자율 주행]
  RPi1: 카메라 → 라인트레이싱 → CAN 0x010 → STM32
  STM32: PID 속도제어 → L298N → 모터
  교차로 감지 시: 목적지별 교차로 행동 테이블에 따라 좌/우/직진

[③ 목적지 도착]
  RPi1: ArUco 마커 ID(1~4) 감지 → 즉시 정지
  RPi1 → CAN 0x013 → STM103: 도착 신호
  RPi1 → MQTT → RPi3: arrived 보고
  STM103: STATE_VERIFY_DEST 진입

[④ 화물함 인증 및 수령]
  소비자: LCD 확인 → 목적지 키(A/B/C/D) 입력 → PIN 4자리 입력 (#제출)

  [성공]
    STM103: 서보 열림 (5초 카운트다운) → 서보 닫힘
    STM103 → CAN 0x302=0x01 → RPi1: 인증 성공
    STM103 → CAN 0x301=0x00 → RPi1: 도어 닫힘
    RPi1 → MQTT alert(pin_success) → RPi3

  [실패 5회]
    STM103 → CAN 0x303=0x01 → RPi1: 잠금
    RPi1 → MQTT alert(pin_locked) → RPi3 로그
    10초 잠금 후 PIN 재입력 허용

  [오배달 / 미수령 타임아웃]
    STM103 → CAN 0x302=0x02 → RPi1: 즉시 유턴

[⑤ 귀환]
  RPi1: g_door_closed = true → S_UTURN (U턴)
  → S_REACQUIRE_AFTER_UTURN (직진, 라인 재탐색)
  → S_FOLLOW (returning=true, 귀환 교차로 행동 테이블)
  → ArUco ID=0 (출발지) 감지 → S_FINISHED
  RPi1 → MQTT → RPi3: completed</code></pre><h3 id="3-2-목적지별-교차로-행동-테이블">3-2. 목적지별 교차로 행동 테이블</h3>
<table>
<thead>
<tr>
<th>목적지</th>
<th>방향</th>
<th>교차로 1번</th>
<th>교차로 2번</th>
</tr>
</thead>
<tbody><tr>
<td>A (dest=1)</td>
<td>GO</td>
<td>좌회전</td>
<td>—</td>
</tr>
<tr>
<td>B (dest=2)</td>
<td>GO</td>
<td>우회전</td>
<td>—</td>
</tr>
<tr>
<td>C (dest=3)</td>
<td>GO</td>
<td>직진</td>
<td>좌회전</td>
</tr>
<tr>
<td>D (dest=4)</td>
<td>GO</td>
<td>직진</td>
<td>우회전</td>
</tr>
<tr>
<td>A (dest=1)</td>
<td>RETURN</td>
<td>우회전</td>
<td>—</td>
</tr>
<tr>
<td>B (dest=2)</td>
<td>RETURN</td>
<td>좌회전</td>
<td>—</td>
</tr>
<tr>
<td>C (dest=3)</td>
<td>RETURN</td>
<td>우회전</td>
<td>직진</td>
</tr>
<tr>
<td>D (dest=4)</td>
<td>RETURN</td>
<td>좌회전</td>
<td>직진</td>
</tr>
</tbody></table>
<hr />
<h2 id="4-can-프로토콜-최종-확정">4. CAN 프로토콜 (최종 확정)</h2>
<h3 id="4-1-통신-속도">4-1. 통신 속도</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>값</th>
<th>근거</th>
</tr>
</thead>
<tbody><tr>
<td>통신 속도</td>
<td>250 kbps</td>
<td>버스 점유율 1% 미만, 배선 노이즈 내성 유리</td>
</tr>
<tr>
<td>프레임 수</td>
<td>약 20~30개/초</td>
<td>50 ms 주기 메시지 기준</td>
</tr>
</tbody></table>
<h3 id="4-2-can-id-테이블">4-2. CAN ID 테이블</h3>
<table>
<thead>
<tr>
<th>CAN ID</th>
<th>내용</th>
<th>송신</th>
<th>수신</th>
<th>주기</th>
</tr>
</thead>
<tbody><tr>
<td><strong>0x010</strong></td>
<td>주행 명령 (dir + rpm)</td>
<td>RPi1</td>
<td>STM32</td>
<td>50 ms</td>
</tr>
<tr>
<td><strong>0x011</strong></td>
<td>E-Stop</td>
<td>RPi1</td>
<td>STM32</td>
<td>즉시</td>
</tr>
<tr>
<td><strong>0x012</strong></td>
<td>배달정보 (PIN + 목적지)</td>
<td>RPi1</td>
<td>STM103</td>
<td>이벤트</td>
</tr>
<tr>
<td><strong>0x013</strong></td>
<td>도착 신호 ★</td>
<td>RPi1</td>
<td>STM103</td>
<td>이벤트</td>
</tr>
<tr>
<td><strong>0x100</strong></td>
<td>현재 속도 피드백 (RPM×100)</td>
<td>STM32</td>
<td>RPi1</td>
<td>50 ms</td>
</tr>
<tr>
<td><strong>0x101</strong></td>
<td>전방 거리 (VL53L0X, mm)</td>
<td>STM32</td>
<td>RPi1</td>
<td>50 ms</td>
</tr>
<tr>
<td><strong>0x200</strong></td>
<td>ECU Heartbeat (0xAA)</td>
<td>STM32</td>
<td>RPi1</td>
<td>100 ms</td>
</tr>
<tr>
<td><strong>0x301</strong></td>
<td>도어 상태 (0x00=닫힘)</td>
<td>STM103</td>
<td>RPi1</td>
<td>이벤트</td>
</tr>
<tr>
<td><strong>0x302</strong></td>
<td>인증 결과 (0x01=성공, 0x02=오배달/미수령)</td>
<td>STM103</td>
<td>RPi1</td>
<td>이벤트</td>
</tr>
<tr>
<td><strong>0x303</strong></td>
<td>PIN 5회 실패 잠금 (0x01)</td>
<td>STM103</td>
<td>RPi1</td>
<td>이벤트</td>
</tr>
</tbody></table>
<blockquote>
<p>★ <strong>0x013 분리 배경</strong>: 기존 0x010(주행 명령)과 도착 신호를 같은 ID로 사용하면 STM32가 도착 신호를 모터 명령으로 오인하여 오동작. 0x013으로 분리하여 STM103만 수신하도록 변경.</p>
</blockquote>
<h3 id="4-3-can-페이로드-상세">4-3. CAN 페이로드 상세</h3>
<p><strong>0x010 — 주행 명령 (RPi1 → STM32, DLC=3)</strong></p>
<table>
<thead>
<tr>
<th>Byte</th>
<th>내용</th>
<th>값</th>
</tr>
</thead>
<tbody><tr>
<td>[0]</td>
<td>방향</td>
<td>0=정지, 1=전진, 2=후진, 3=좌, 4=우, 5=U턴</td>
</tr>
<tr>
<td>[1]</td>
<td>RPM×10 상위 바이트</td>
<td>uint8</td>
</tr>
<tr>
<td>[2]</td>
<td>RPM×10 하위 바이트</td>
<td>uint8</td>
</tr>
</tbody></table>
<p><strong>0x012 — 배달정보 (RPi1 → STM103, DLC=6)</strong></p>
<table>
<thead>
<tr>
<th>Byte</th>
<th>내용</th>
<th>값</th>
</tr>
</thead>
<tbody><tr>
<td>[0]</td>
<td>유효 패킷 식별</td>
<td>0x01</td>
</tr>
<tr>
<td>[1]</td>
<td>PIN[0] (숫자 0~9)</td>
<td>uint8</td>
</tr>
<tr>
<td>[2]</td>
<td>PIN[1]</td>
<td>uint8</td>
</tr>
<tr>
<td>[3]</td>
<td>PIN[2]</td>
<td>uint8</td>
</tr>
<tr>
<td>[4]</td>
<td>PIN[3]</td>
<td>uint8</td>
</tr>
<tr>
<td>[5]</td>
<td>목적지 코드</td>
<td>0x01=A, 0x02=B, 0x03=C, 0x04=D</td>
</tr>
</tbody></table>
<p><strong>0x013 — 도착 신호 (RPi1 → STM103, DLC=1)</strong></p>
<table>
<thead>
<tr>
<th>Byte</th>
<th>내용</th>
<th>값</th>
</tr>
</thead>
<tbody><tr>
<td>[0]</td>
<td>도착</td>
<td>0x01</td>
</tr>
</tbody></table>
<p><strong>0x301 — 도어 상태 (STM103 → RPi1, DLC=1)</strong></p>
<table>
<thead>
<tr>
<th>Data[0]</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>0x00</td>
<td>도어 닫힘 → RPi1 유턴 트리거</td>
</tr>
<tr>
<td>0x01</td>
<td>도어 열림</td>
</tr>
</tbody></table>
<p><strong>0x302 — 인증 결과 (STM103 → RPi1, DLC=1)</strong></p>
<table>
<thead>
<tr>
<th>Data[0]</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>0x01</td>
<td>PIN 인증 성공 → MQTT alert 송신</td>
</tr>
<tr>
<td>0x02</td>
<td>오배달 확인 / 미수령 타임아웃 → 즉시 유턴</td>
</tr>
</tbody></table>
<p><strong>0x303 — 잠금 (STM103 → RPi1, DLC=1)</strong></p>
<table>
<thead>
<tr>
<th>Data[0]</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>0x01</td>
<td>PIN 5회 실패 잠금 → MQTT alert 송신</td>
</tr>
</tbody></table>
<p><strong>0x100 — 속도 피드백 (STM32 → RPi1, DLC=8)</strong></p>
<table>
<thead>
<tr>
<th>Byte</th>
<th>내용</th>
<th>타입</th>
</tr>
</thead>
<tbody><tr>
<td>[0~1]</td>
<td>좌 RPM × 100</td>
<td>int16 Big-Endian</td>
</tr>
<tr>
<td>[2~3]</td>
<td>우 RPM × 100</td>
<td>int16 Big-Endian</td>
</tr>
<tr>
<td>[4~5]</td>
<td>좌 CCR (PWM 값)</td>
<td>uint16 Big-Endian</td>
</tr>
<tr>
<td>[6~7]</td>
<td>우 CCR (PWM 값)</td>
<td>uint16 Big-Endian</td>
</tr>
</tbody></table>
<hr />
<h2 id="5-mqtt-토픽-구조">5. MQTT 토픽 구조</h2>
<h3 id="5-1-전체-토픽-테이블">5-1. 전체 토픽 테이블</h3>
<table>
<thead>
<tr>
<th>Topic</th>
<th>방향</th>
<th>QoS</th>
<th>내용</th>
</tr>
</thead>
<tbody><tr>
<td><code>delivery/vehicle/vehicle_001/destination</code></td>
<td>RPi3 → RPi1</td>
<td>1</td>
<td>출동 명령 (destination + pin + order_id)</td>
</tr>
<tr>
<td><code>delivery/vehicle/vehicle_001/1to3</code></td>
<td>RPi1 → RPi3</td>
<td>1</td>
<td>배달 상태 보고 (in_transit / arrived / completed)</td>
</tr>
<tr>
<td><code>delivery/vehicle/vehicle_001/status</code></td>
<td>RPi1 → RPi3</td>
<td>0</td>
<td>Heartbeat (2초 주기)</td>
</tr>
<tr>
<td><code>delivery/vehicle/vehicle_001/alert</code></td>
<td>RPi1 → RPi3</td>
<td>1</td>
<td>이벤트 알림 (pin_locked / pin_success)</td>
</tr>
<tr>
<td><code>delivery/order/001</code></td>
<td>RPi4 → RPi3</td>
<td>1</td>
<td>주문 정보</td>
</tr>
<tr>
<td><code>delivery/pin/001/offboard</code></td>
<td>RPi4 → RPi3</td>
<td>2</td>
<td>PIN 정보</td>
</tr>
<tr>
<td><code>delivery/pin/001/onboard</code></td>
<td>RPi3 → RPi1</td>
<td>2</td>
<td>PIN 정보</td>
</tr>
<tr>
<td><code>delivery/complete/001/offboard</code></td>
<td>RPi3 → RPi4</td>
<td>1</td>
<td>배달 완료 알림</td>
</tr>
</tbody></table>
<h3 id="5-2-alert-토픽-페이로드-예시">5-2. alert 토픽 페이로드 예시</h3>
<pre><code class="language-json">// PIN 5회 실패 잠금 (0x303 수신 시)
{
  &quot;vehicle_id&quot;: &quot;vehicle_001&quot;,
  &quot;order_id&quot;: &quot;...&quot;,
  &quot;event&quot;: &quot;pin_locked&quot;,
  &quot;message&quot;: &quot;PIN 5회 실패 - 적재함 잠금 (10초)&quot;,
  &quot;timestamp&quot;: &quot;2026-03-08 10:20:00&quot;
}

// PIN 인증 성공 (0x302=0x01 수신 시)
{
  &quot;vehicle_id&quot;: &quot;vehicle_001&quot;,
  &quot;order_id&quot;: &quot;...&quot;,
  &quot;event&quot;: &quot;pin_success&quot;,
  &quot;message&quot;: &quot;PIN 인증 성공 - 도어 열림&quot;,
  &quot;timestamp&quot;: &quot;2026-03-08 10:20:05&quot;
}</code></pre>
<h3 id="5-3-mqtt-브로커-접속-정보">5-3. MQTT 브로커 접속 정보</h3>
<pre><code>브로커 IP: 10.42.0.1 (Pi5_MQTT_AP 핫스팟)
사용자명: hoji
비밀번호: 1234
포트: 1883</code></pre><p><strong>와이파이 재연결 명령:</strong></p>
<pre><code class="language-bash">sudo nmcli device wifi rescan
sudo nmcli device wifi connect &quot;Pi5_MQTT_AP&quot; password &quot;12345678&quot;
# 또는 간단히
sudo nmcli device wifi connect &quot;Pi5_MQTT_AP&quot;</code></pre>
<hr />
<h2 id="6-stm32-주행-ecu-상세-설계">6. STM32 주행 ECU 상세 설계</h2>
<h3 id="6-1-핀맵">6-1. 핀맵</h3>
<table>
<thead>
<tr>
<th>기능</th>
<th>핀</th>
<th>CubeMX 설정</th>
<th>연결 대상</th>
</tr>
</thead>
<tbody><tr>
<td>USART1_TX</td>
<td>PB6</td>
<td>USART1_TX</td>
<td>ST-LINK VCP (PC COM3)</td>
</tr>
<tr>
<td>USART1_RX</td>
<td>PB7</td>
<td>USART1_RX</td>
<td>ST-LINK VCP</td>
</tr>
<tr>
<td>CAN1_RX</td>
<td>PB8</td>
<td>CAN1_RX</td>
<td>SN65HVD230 RXD</td>
</tr>
<tr>
<td>CAN1_TX</td>
<td>PB9</td>
<td>CAN1_TX</td>
<td>SN65HVD230 TXD</td>
</tr>
<tr>
<td>TIM5_CH1</td>
<td>PA0</td>
<td>Encoder</td>
<td>왼쪽 엔코더 A (레벨시프터 경유)</td>
</tr>
<tr>
<td>TIM5_CH2</td>
<td>PA1</td>
<td>Encoder</td>
<td>왼쪽 엔코더 B (레벨시프터 경유)</td>
</tr>
<tr>
<td>TIM3_CH1</td>
<td>PA6</td>
<td>Encoder</td>
<td>오른쪽 엔코더 A (레벨시프터 경유)</td>
</tr>
<tr>
<td>TIM3_CH2</td>
<td>PA7</td>
<td>Encoder</td>
<td>오른쪽 엔코더 B (레벨시프터 경유)</td>
</tr>
<tr>
<td>TIM2_CH1</td>
<td>PA15</td>
<td>PWM</td>
<td>L298N ENA (왼쪽)</td>
</tr>
<tr>
<td>TIM2_CH3</td>
<td>PA2</td>
<td>PWM</td>
<td>L298N ENB (오른쪽)</td>
</tr>
<tr>
<td>GPIO_OUT</td>
<td>PC2</td>
<td>GPIO_Output</td>
<td>L298N IN1</td>
</tr>
<tr>
<td>GPIO_OUT</td>
<td>PC3</td>
<td>GPIO_Output</td>
<td>L298N IN2</td>
</tr>
<tr>
<td>GPIO_OUT</td>
<td>PC4</td>
<td>GPIO_Output</td>
<td>L298N IN3</td>
</tr>
<tr>
<td>GPIO_OUT</td>
<td>PC5</td>
<td>GPIO_Output</td>
<td>L298N IN4</td>
</tr>
<tr>
<td>I2C2_SCL</td>
<td>PB10</td>
<td>I2C2_SCL</td>
<td>VL53L0X (온보드)</td>
</tr>
<tr>
<td>I2C2_SDA</td>
<td>PB11</td>
<td>I2C2_SDA</td>
<td>VL53L0X (온보드)</td>
</tr>
</tbody></table>
<h3 id="6-2-cubemx-설정">6-2. CubeMX 설정</h3>
<pre><code>USART1: PB6(TX)/PB7(RX), 115200/8N1, NVIC Enable
CAN1:   PB8(RX)/PB9(TX), Prescaler=16, BS1=13TQ, BS2=2TQ → 250kbps
TIM2:   CH1(PA15)/CH3(PA2), Prescaler=79, Period=999 → 1kHz PWM
TIM5:   CH1(PA0)/CH2(PA1), Encoder Mode TI12, Period=65535
TIM3:   CH1(PA6)/CH2(PA7), Encoder Mode TI12, Period=65535 (우측)
TIM6:   Prescaler=79, Period=9999 → 10ms PID 인터럽트
TIM7:   HAL Timebase (SysTick 대체)
IWDG:   Prescaler=/32, Reload=300 → 300ms Watchdog
Clock:  HSI 16MHz → PLL → SYSCLK 80MHz
        SYS → Debug: Serial Wire (PA15 JTAG 해제 필수)</code></pre><h3 id="6-3-핵심-파라미터">6-3. 핵심 파라미터</h3>
<pre><code class="language-c">#define PWM_MAX             999
#define PWM_OFFSET          300.0f
#define PULSE_PER_REV       5280        // 실측값 확정
#define PID_INTERVAL_MS     10

#define TARGET_RPM_DEFAULT  100.0f
#define TARGET_RPM_MAX      350.0f

#define KP                  0.5f
#define KI                  0.05f       // 적분 게인 추가
#define KD                  0.0f
#define INTEGRAL_LIMIT      150.0f

#define PWM_FORWARD         400
#define PWM_TURN            900         // 회전 최대값
#define PWM_BACKWARD        320         // 후진 고정 PWM

#define CAN_CMD_TIMEOUT_MS  5000        // 5초간 CAN 미수신 시 자동 정지</code></pre>
<h3 id="6-4-모터-제어-정책">6-4. 모터 제어 정책</h3>
<table>
<thead>
<tr>
<th>방향</th>
<th>PID</th>
<th>동작</th>
</tr>
</thead>
<tbody><tr>
<td>전진 (DIR_FORWARD=1)</td>
<td>ON</td>
<td>pid_enable=1, target_rpm 추종</td>
</tr>
<tr>
<td>후진 (DIR_BACKWARD=2)</td>
<td>OFF</td>
<td>PWM 320 고정</td>
</tr>
<tr>
<td>좌회전 (DIR_LEFT=3)</td>
<td>OFF</td>
<td>왼쪽 후진(500) / 오른쪽 전진(PWM_TURN)</td>
</tr>
<tr>
<td>우회전 (DIR_RIGHT=4)</td>
<td>OFF</td>
<td>왼쪽 전진(PWM_TURN) / 오른쪽 후진(500)</td>
</tr>
<tr>
<td>U턴 (DIR_UTURN=5)</td>
<td>OFF</td>
<td>왼쪽 후진(500) / 오른쪽 전진(500)</td>
</tr>
<tr>
<td>정지 (DIR_STOP=0)</td>
<td>OFF</td>
<td>PWM=0, 모든 핀 LOW, PID 리셋</td>
</tr>
</tbody></table>
<pre><code>전진: IN1=H IN2=L / IN3=H IN4=L
후진: IN1=L IN2=H / IN3=L IN4=H
좌:   IN1=L IN2=H(후진) / IN3=H IN4=L(전진)
우:   IN1=H IN2=L(전진) / IN3=L IN4=H(후진)
U턴: IN1=L IN2=H(후진) / IN3=H IN4=L(전진)</code></pre><h3 id="6-5-타이밍-구조">6-5. 타이밍 구조</h3>
<pre><code>TIM6 인터럽트 (10ms)
├── pid_flag = 1
└── can_timeout_cnt 증가

메인 루프
├── CAN RX 처리 (can_rx_flag)
├── CAN 타임아웃 체크 (5초 → Motor_Stop)
└── pid_flag 처리
    ├── Encoder_Update() → RPM 계산
    ├── PID_Compute() → PWM 출력 (전진 시만 활성)
    ├── CAN TX: 속도 피드백 (50ms, 0x100)
    └── CAN TX: Heartbeat (100ms, 0x200)</code></pre><h3 id="6-6-fail-safe-iwdg-watchdog">6-6. Fail-safe (IWDG Watchdog)</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>값</th>
</tr>
</thead>
<tbody><tr>
<td>타임아웃</td>
<td>300 ms</td>
</tr>
<tr>
<td>동작</td>
<td>RPi1 다운 시 MCU 리셋 → 모터 즉시 정지</td>
</tr>
<tr>
<td>CAN 소프트웨어 타임아웃</td>
<td>5000 ms — IWDG와 별도 추가</td>
</tr>
</tbody></table>
<hr />
<h2 id="7-rpi1-미션-ecu-상세-설계">7. RPi1 미션 ECU 상세 설계</h2>
<h3 id="7-1-하드웨어-연결">7-1. 하드웨어 연결</h3>
<pre><code>RPi1
├── MCP2515 (SPI) → CAN 버스
│    ├── 오실레이터: 8 MHz (실물 확인 완료)
│    ├── 전원: 5V (RPi 5V 핀 공급) — 3.3V 직결 금지
│    ├── 트랜시버: TJA1050 내장 (5V 전용)
│    └── J1 점퍼 제거 (중간 노드 — 내장 120Ω 비활성화)
├── Wi-Fi → MQTT → RPi3 (브로커: Pi5_MQTT_AP / 10.42.0.1)
└── USB 카메라 (/dev/video0) — 라인트레이싱 + ArUco 마커 목적지 인식</code></pre><p><strong>MCP2515 레벨시프터 적용 범위:</strong></p>
<table>
<thead>
<tr>
<th>SPI 신호</th>
<th>방향</th>
<th>레벨시프터 필요</th>
<th>이유</th>
</tr>
</thead>
<tbody><tr>
<td>MOSI</td>
<td>RPi(3.3V) → MCP2515</td>
<td>불필요</td>
<td>MCP2515가 3.3V 입력 허용</td>
</tr>
<tr>
<td>SCK</td>
<td>RPi(3.3V) → MCP2515</td>
<td>불필요</td>
<td>동일</td>
</tr>
<tr>
<td>CS</td>
<td>RPi(3.3V) → MCP2515</td>
<td>불필요</td>
<td>동일</td>
</tr>
<tr>
<td>MISO</td>
<td>MCP2515(5V) → RPi</td>
<td><strong>필수</strong></td>
<td>5V 출력이 RPi 3.3V 핀 손상 유발</td>
</tr>
<tr>
<td>INT</td>
<td>MCP2515(5V) → RPi</td>
<td><strong>필수</strong></td>
<td>동일</td>
</tr>
</tbody></table>
<p><strong><code>/boot/config.txt</code> 설정:</strong></p>
<pre><code class="language-bash">dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
# 적용 후
sudo ip link set can0 up type can bitrate 250000</code></pre>
<h3 id="7-2-상태머신-delivery_mqttcpp-최종">7-2. 상태머신 (delivery_mqtt.cpp 최종)</h3>
<pre><code>S_WAIT_CMD
└→ MQTT 출동 명령 수신 (destination + pin + order_id)
   → CAN 0x012: PIN + 목적지 → STM103
   → S_FOLLOW (출발, JUNC_START_DELAY 후 교차로 감지 활성)

S_FOLLOW  ← 라인트레이싱 + 교차로 감지 + ArUco 감지 (50ms 주기 CAN 0x010)
├→ 교차로 감지 (streak ≥ JUNC_STREAK) + junc_count &lt; max_junc
│   → S_JUNC_STOP (800~1000ms 정지)
│     → S_JUNC_LEFT / S_JUNC_RIGHT / S_JUNC_STRAIGHT (DUR_TURN_MS=3000ms)
│       → S_REACQUIRE (400ms 라인 재탐색)
│         → S_FOLLOW
│
└→ 목적지 ArUco ID 감지 (returning=false)
    → 즉시 정지
    → CAN 0x013: 도착 신호 → STM103
    → MQTT: arrived 보고
    → S_DELIVER_WAIT

S_DELIVER_WAIT
├← CAN 0x301=0x00 수신 (도어 닫힘) → g_door_closed = true → S_UTURN
└← CAN 0x302=0x02 수신 (오배달/미수령) → 즉시 S_UTURN

S_UTURN (DUR_UTURN_MS=1300ms U턴)
└→ S_REACQUIRE (직진, 라인 재탐색)
   └→ S_FOLLOW (returning=true, 귀환 교차로 행동 테이블)
      └→ ArUco ID=0 감지 (출발지)
         → S_FINISHED

S_FINISHED
└→ MQTT: completed → S_WAIT_CMD</code></pre><h3 id="7-3-vision-처리-파이프라인">7-3. Vision 처리 파이프라인</h3>
<pre><code>USB 카메라 1대 (/dev/video0, 320×240)
│
├── [라인트레이싱] 하단 35% ROI
│    GaussianBlur → OTSU 이진화 → 컨투어 → 무게중심 → 오차(err) 계산
│    err &gt; STRAIGHT_DEADBAND(50px) → LEFT / RIGHT
│    err ≤ STRAIGHT_DEADBAND      → FORWARD
│
├── [교차로 감지] 중간 22% ROI (H*0.40 ~ H*0.62)
│    이진화 → 좌/중/우 3분할 픽셀 비율 계산
│    L≥0.40 &amp;&amp; M≥0.40 &amp;&amp; R≥0.40  → J_PLUS (3방향)
│    L≥0.40 &amp;&amp; R≥0.40            → J_T (T자)
│    한쪽 ≥ HIGH_TH_ONE(0.65)     → J_T (단방향 강화)
│    연속 streak ≥ JUNC_STREAK(2) → 교차로 확정
│
└── [ArUco 마커] DICT_4X4_50
     ID 0: 출발지 (귀환 완료 판단)
     ID 1~4: 목적지 A~D</code></pre><h3 id="7-4-주행-파라미터">7-4. 주행 파라미터</h3>
<pre><code class="language-cpp">#define DEFAULT_RPM           60.0f   // 라인트레이싱 기본 속도
#define TURN_RPM              150.0f  // 회전 시 속도
#define STRAIGHT_DEADBAND     50      // 직진 판단 오차 허용 범위 (픽셀)

#define JUNC_STREAK           2       // 연속 감지 횟수 임계값
#define JUNC_START_DELAY      3000    // 출발 후 교차로 감지 시작 지연 (ms)
#define JUNC_COOLDOWN_MS      3500    // 교차로 처리 후 재감지 방지 시간 (ms)
#define HIGH_TH               0.40f   // 3방향 교차로 픽셀 비율 임계값
#define HIGH_TH_ONE           0.65f   // 단방향 강화 임계값
#define MID_TH                0.40f   // 중앙 픽셀 비율 임계값

#define DUR_JUNC_STOP_MS      1000    // 교차로 정지 시간 (ms)
#define DUR_STRAIGHT_MS       2000    // 교차로 직진 통과 시간 (ms)
#define DUR_TURN_MS           3000    // 좌/우회전 소요 시간 (ms) — 튜닝 필요
#define DUR_UTURN_MS          1300    // U턴 소요 시간 (ms)
#define DUR_REACQ_MS          400     // 라인 재탐색 시간 (ms)</code></pre>
<h3 id="7-5-can-수신-처리">7-5. CAN 수신 처리</h3>
<pre><code>0x301 = 0x00 → g_door_closed = true → S_UTURN 트리거
0x302 = 0x01 → MQTT alert(pin_success) 전송
0x302 = 0x02 → g_door_closed = true → 즉시 S_UTURN (오배달/미수령)
0x303 = 0x01 → MQTT alert(pin_locked) 전송 → RPi3 서버 로그</code></pre><h3 id="7-6-빌드-및-실행">7-6. 빌드 및 실행</h3>
<pre><code class="language-bash">g++ delivery_mqtt.cpp -o delivery \
    $(pkg-config --cflags --libs opencv4) \
    -lmosquittopp -lpthread

./delivery             # 기본 브로커 10.42.0.1
./delivery 10.42.0.1   # 브로커 IP 명시</code></pre>
<hr />
<h2 id="8-stm103-화물함-ecu-상세-설계">8. STM103 화물함 ECU 상세 설계</h2>
<h3 id="8-1-핀맵-최종-확정">8-1. 핀맵 (최종 확정)</h3>
<table>
<thead>
<tr>
<th>기능</th>
<th>핀</th>
<th>CubeMX 설정</th>
<th>연결 대상</th>
</tr>
</thead>
<tbody><tr>
<td>CAN1_RX</td>
<td>PB8</td>
<td>CAN1_RX</td>
<td>SN65HVD230 RXD (AFIO Remap2)</td>
</tr>
<tr>
<td>CAN1_TX</td>
<td>PB9</td>
<td>CAN1_TX</td>
<td>SN65HVD230 TXD (AFIO Remap2)</td>
</tr>
<tr>
<td>I2C2_SCL</td>
<td>PB10</td>
<td>I2C2_SCL</td>
<td>16×2 LCD (HD44780, I2C)</td>
</tr>
<tr>
<td>I2C2_SDA</td>
<td>PB11</td>
<td>I2C2_SDA</td>
<td>16×2 LCD</td>
</tr>
<tr>
<td>TIM3_CH1</td>
<td>PA6</td>
<td>PWM</td>
<td>서보 모터 (50Hz)</td>
</tr>
<tr>
<td>LED</td>
<td>PA5</td>
<td>GPIO_Output</td>
<td>상태 표시 LED</td>
</tr>
<tr>
<td>USART1_TX</td>
<td>PA9</td>
<td>USART1_TX</td>
<td>디버그 115200 bps</td>
</tr>
<tr>
<td>USART1_RX</td>
<td>PA10</td>
<td>USART1_RX</td>
<td>디버그</td>
</tr>
<tr>
<td>Keypad Row1~4</td>
<td>PC0~PC3</td>
<td>GPIO_Output</td>
<td>4×4 키패드 행</td>
</tr>
<tr>
<td>Keypad Col1~4</td>
<td>PB12~PB15</td>
<td>GPIO_Input Pull-Up</td>
<td>4×4 키패드 열</td>
</tr>
</tbody></table>
<h3 id="8-2-cubemx-설정">8-2. CubeMX 설정</h3>
<pre><code>CAN1:   PB8(RX)/PB9(TX), Prescaler=6, BS1=13TQ, BS2=2TQ → 250kbps
        AFIO Remap2 적용 필수: __HAL_AFIO_REMAP_CAN1_2()
I2C2:   PB10(SCL)/PB11(SDA), Standard Mode 100kHz
TIM3:   CH1(PA6), Prescaler=47, Period=19999 → 50Hz (서보 표준)
USART1: PA9(TX)/PA10(RX), 115200/8N1
GPIO:   PC0~PC3 Output / PB12~PB15 Input Pull-Up
Clock:  HSI 8MHz → PLL×12 → SYSCLK 48MHz
        APB1 /2 → PCLK1 24MHz (CAN/I2C2/TIM3)</code></pre><h3 id="8-3-서보-pwm-매크로">8-3. 서보 PWM 매크로</h3>
<pre><code class="language-c">#define SERVO_OPEN   2000   // 도어 열림 펄스폭 (μs)
#define SERVO_CLOSE  1000   // 도어 닫힘 펄스폭 (μs)</code></pre>
<h3 id="8-4-키패드-레이아웃">8-4. 키패드 레이아웃</h3>
<pre><code>        Col1(PB12) Col2(PB13) Col3(PB14) Col4(PB15)
Row1(PC0)   1          2          3          A
Row2(PC1)   4          5          6          B
Row3(PC2)   7          8          9          C
Row4(PC3)   *          0          #          D

* = 한 자리 삭제 (백스페이스)
# = 확인 (제출)
A~D = 목적지 입력</code></pre><h3 id="8-5-보안-상태머신">8-5. 보안 상태머신</h3>
<pre><code>STATE_IDLE
└→ CAN 0x012 수신 (PIN + 목적지)
   LCD: &quot;Destination: X / PIN received!&quot;
   → STATE_PKG_RECEIVED

STATE_PKG_RECEIVED
└→ CAN 0x013 수신 (도착 신호)
   LCD: &quot;Destination? / Enter: A B C D&quot;
   auth_timeout 카운트 시작
   → STATE_VERIFY_DEST

STATE_VERIFY_DEST
├→ 키패드 입력 (A/B/C/D) — 목적지 일치
│   LCD: &quot;Pkg arrived!! / PW: ____&quot;
│   → STATE_WAIT_FOR_PIN
└→ 키패드 입력 — 목적지 불일치
    LCD: &quot;Is dest X right? / 1:YES  2:NO&quot;
    → STATE_WRONG_DEST_CONFIRM

STATE_WRONG_DEST_CONFIRM
├→ '1'(YES) → CAN 0x302=0x02 → STATE_IDLE (오배달 귀환)
└→ '2'(NO)  → STATE_VERIFY_DEST (재입력)

STATE_WAIT_FOR_PIN
├→ PIN 성공 (#제출)
│   LED ON + 서보 열림 (5초 논블로킹 카운트다운)
│   CAN 0x302=0x01 (인증 성공)
│   CAN 0x301=0x00 (도어 닫힘 → RPi1 유턴 트리거)
│   → STATE_IDLE
├→ PIN 실패 (1~4회)
│   LED 점멸 + &quot;Wrong PIN! / N tries left&quot;
└→ PIN 실패 (5회)
    CAN 0x303=0x01 (잠금)
    → STATE_LOCKED (10초)

STATE_LOCKED
└→ 10초 후 → STATE_WAIT_FOR_PIN (fail_cnt 리셋)

미수령 타임아웃 (AUTH_TIMEOUT_MS=30000ms)
  VERIFY_DEST / WRONG_DEST_CONFIRM / WAIT_FOR_PIN 상태에서 30초 초과
  → CAN 0x302=0x02 → STATE_IDLE</code></pre><h3 id="8-6-lcd-표시-항목">8-6. LCD 표시 항목</h3>
<table>
<thead>
<tr>
<th>상태</th>
<th>1행</th>
<th>2행</th>
</tr>
</thead>
<tbody><tr>
<td>IDLE</td>
<td>&quot;  Cargo  ECU  &quot;</td>
<td>&quot;   Waiting...  &quot;</td>
</tr>
<tr>
<td>PKG_RECEIVED</td>
<td>&quot;Destination: X  &quot;</td>
<td>&quot;PIN received!   &quot;</td>
</tr>
<tr>
<td>VERIFY_DEST</td>
<td>&quot;Destination?    &quot;</td>
<td>&quot;Enter: A B C D  &quot;</td>
</tr>
<tr>
<td>WRONG_DEST_CONFIRM</td>
<td>&quot;Is dest X right?&quot;</td>
<td>&quot;1:YES  2:NO     &quot;</td>
</tr>
<tr>
<td>WAIT_FOR_PIN</td>
<td>&quot;Pkg arrived!!   &quot;</td>
<td>&quot;PW: ****        &quot;</td>
</tr>
<tr>
<td>성공</td>
<td>&quot;Delivery Done!  &quot;</td>
<td>&quot;Enjoy ur day! :D&quot;</td>
</tr>
<tr>
<td>LOCKED</td>
<td>&quot;!! LOCKED !!    &quot;</td>
<td>&quot;  Wait: Xs...   &quot;</td>
</tr>
<tr>
<td>오배달/미수령</td>
<td>&quot;Wrong delivery! &quot;</td>
<td>&quot;Returning home  &quot;</td>
</tr>
</tbody></table>
<hr />
<h2 id="9-rpi3-서버-상세-설계">9. RPi3 서버 상세 설계</h2>
<h3 id="9-1-핵심-원칙">9-1. 핵심 원칙</h3>
<p>실시간 제어에 절대 관여하지 않는다. 이벤트 기반 데이터 중계 및 저장.</p>
<h3 id="9-2-기능-구성">9-2. 기능 구성</h3>
<ul>
<li>Mosquitto MQTT 브로커 운용</li>
<li>RPi1 ↔ RPi3 ↔ RPi4 MQTT 메시지 중계</li>
<li>주문 정보 / PIN / 배달 상태 SQLite DB 저장</li>
<li>alert 토픽 구독 및 로그 처리</li>
<li>Qt 관제 UI (배달 상태 모니터링)</li>
</ul>
<h3 id="9-3-db-테이블-구조">9-3. DB 테이블 구조</h3>
<pre><code class="language-sql">delivery_table: id | vehicle_id | destination | receiver | start_time | end_time | status
password_table: vehicle_id | password | expire_time | used
event_log:      timestamp | vehicle_id | event_type | detail</code></pre>
<hr />
<h2 id="10-rpi4-클라이언트-상세-설계">10. RPi4 클라이언트 상세 설계</h2>
<p>Qt Widgets 기반 주문 UI (5인치 터치 디스플레이, XPT2046).
목적지(A~D) + PIN 4자리 설정 후 MQTT로 RPi3에 주문 전송.
배달 완료 알림 수신 및 표시.</p>
<hr />
<h2 id="11-하드웨어-구성">11. 하드웨어 구성</h2>
<h3 id="11-1-can-버스-배선">11-1. CAN 버스 배선</h3>
<blockquote>
<p><strong>직선(데이지체인) 버스 구조</strong> 필수. 별형(Star) 배선 금지.
<strong>모든 노드의 GND를 반드시 공통 연결.</strong></p>
</blockquote>
<pre><code>[STM32 주행 ECU]          [RPi1 + MCP2515]          [STM103 화물함 ECU]
  (버스 끝단)               (중간 노드)                (버스 끝단)
  SN65HVD230                TJA1050 내장               SN65HVD230
  종단저항 있음              J1 점퍼 제거               종단저항 있음
  220Ω || 220Ω = 110Ω      내장 120Ω 비활성화          220Ω || 220Ω = 110Ω
        │                        │                          │
        └────────── CANH ────────┴────────── CANH ──────────┘
        └────────── CANL ────────┴────────── CANL ──────────┘
        └────────── GND  ────────┴────────── GND  ──────────┘</code></pre><p><strong>SN65HVD230 연결 (STM32 / STM103 공통):</strong></p>
<pre><code>STM32/STM103 CAN_TX → SN65HVD230 TXD
SN65HVD230 RXD → STM32/STM103 CAN_RX
SN65HVD230 VCC = 3.3V  ← GND와 혼동 주의 (오결선으로 CAN 불통 경험)
SN65HVD230 GND = GND</code></pre><h3 id="11-2-stm32-실제-배선">11-2. STM32 실제 배선</h3>
<pre><code>STM32 → L298N:
  PA15 → ENA 직결 (3.3V PWM 직결, 레벨시프터 불필요)
  PA2  → ENB 직결
  PC2 → IN1 / PC3 → IN2 / PC4 → IN3 / PC5 → IN4

L298N → 모터:
  OUT1/OUT2 → 왼쪽 모터 2개 병렬
  OUT3/OUT4 → 오른쪽 모터 2개 병렬

엔코더 → 레벨시프터 → STM32:
  왼쪽 A/B → PA0/PA1 (TIM5)
  오른쪽 A/B → PA6/PA7 (TIM3)

전원:
  외부 12V → L298N VIN
  L298N 5V 출력 → 엔코더 VCC, 레벨시프터 HV
  STM32 3.3V → 레벨시프터 LV / 공통 GND 필수</code></pre><h3 id="11-3-타이머-사용-현황-stm32">11-3. 타이머 사용 현황 (STM32)</h3>
<table>
<thead>
<tr>
<th>타이머</th>
<th>용도</th>
<th>핀</th>
</tr>
</thead>
<tbody><tr>
<td>TIM2</td>
<td>PWM — ENA(CH1), ENB(CH3)</td>
<td>PA15, PA2</td>
</tr>
<tr>
<td>TIM3</td>
<td>Encoder Mode — 오른쪽</td>
<td>PA6, PA7</td>
</tr>
<tr>
<td>TIM5</td>
<td>Encoder Mode — 왼쪽</td>
<td>PA0, PA1</td>
</tr>
<tr>
<td>TIM6</td>
<td>PID 인터럽트 (10ms)</td>
<td>—</td>
</tr>
<tr>
<td>TIM7</td>
<td>HAL Timebase</td>
<td>—</td>
</tr>
<tr>
<td>IWDG</td>
<td>Watchdog 300ms</td>
<td>—</td>
</tr>
</tbody></table>
<h3 id="11-4-부품-리스트">11-4. 부품 리스트</h3>
<table>
<thead>
<tr>
<th>부품</th>
<th>수량</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td>JGB37-520 엔코더 모터</td>
<td>4개</td>
<td>좌우 대표 각 1개 사용</td>
</tr>
<tr>
<td>STM103 보드 (STM32F103)</td>
<td>2개</td>
<td>화물함 ECU 1개 + CAN 시뮬레이터 1개</td>
</tr>
<tr>
<td>RC카 섀시 키트</td>
<td>1개</td>
<td></td>
</tr>
<tr>
<td>L298N 모터 드라이버</td>
<td>1개</td>
<td></td>
</tr>
<tr>
<td>SN65HVD230 CAN 트랜시버</td>
<td>2개</td>
<td>STM32, STM103 각 1개</td>
</tr>
<tr>
<td>MCP2515 CAN 모듈 (5V)</td>
<td>2개</td>
<td>RPi1 전용 1개, 예비 1개</td>
</tr>
<tr>
<td>4채널 레벨시프터</td>
<td>2개</td>
<td>엔코더 4채널 + MCP2515 MISO/INT 2채널</td>
</tr>
<tr>
<td>220Ω 저항</td>
<td>4개</td>
<td>종단저항 (양 끝단 220Ω×2 병렬)</td>
</tr>
<tr>
<td>USB 카메라</td>
<td>1개</td>
<td>/dev/video0</td>
</tr>
<tr>
<td>소형 서보 모터</td>
<td>1개</td>
<td>화물함 도어</td>
</tr>
<tr>
<td>4×4 키패드</td>
<td>1개</td>
<td></td>
</tr>
<tr>
<td>LCD 1602 (I2C, HD44780)</td>
<td>1개</td>
<td></td>
</tr>
<tr>
<td>5인치 터치 디스플레이 (XPT2046)</td>
<td>1개</td>
<td>RPi4 클라이언트</td>
</tr>
<tr>
<td>배터리 + 홀더 (12V)</td>
<td>1세트</td>
<td></td>
</tr>
</tbody></table>
<hr />
<h2 id="12-fail-safe-설계">12. Fail-safe 설계</h2>
<table>
<thead>
<tr>
<th>상황</th>
<th>감지</th>
<th>대응</th>
</tr>
</thead>
<tbody><tr>
<td>STM32 Heartbeat 누락</td>
<td>RPi1: 300ms 이상 0x200 미수신</td>
<td>E-Stop(0x011) + MQTT 서버 보고</td>
</tr>
<tr>
<td>RPi1 다운</td>
<td>STM32 IWDG 300ms 만료</td>
<td>MCU 리셋 → 모터 즉시 정지</td>
</tr>
<tr>
<td>CAN 명령 타임아웃</td>
<td>STM32: 5초간 0x010 미수신</td>
<td>Motor_Stop() 자동 실행</td>
</tr>
<tr>
<td>PIN 5회 실패</td>
<td>STM103 카운트</td>
<td>10초 잠금 + 0x303 → MQTT 로그</td>
</tr>
<tr>
<td>오배달</td>
<td>STM103 목적지 불일치 확인</td>
<td>0x302=0x02 → RPi1 즉시 유턴</td>
</tr>
<tr>
<td>미수령 타임아웃</td>
<td>STM103: 도착 후 30초 초과</td>
<td>0x302=0x02 → RPi1 즉시 유턴</td>
</tr>
<tr>
<td>MQTT 연결 끊김</td>
<td>RPi1 연결 상태 감지</td>
<td>관제 UI 경고 표시</td>
</tr>
</tbody></table>
<hr />
<h2 id="13-기술-스택">13. 기술 스택</h2>
<table>
<thead>
<tr>
<th>영역</th>
<th>기술</th>
</tr>
</thead>
<tbody><tr>
<td>STM32 주행 ECU 펌웨어</td>
<td>C + STM32 HAL (CubeMX)</td>
</tr>
<tr>
<td>STM103 화물함 ECU 펌웨어</td>
<td>C + STM32 HAL (CubeMX)</td>
</tr>
<tr>
<td>서브 STM103 CAN 시뮬레이터</td>
<td>C + STM32 HAL (bxCAN)</td>
</tr>
<tr>
<td>라인트레이싱 / ArUco</td>
<td>C++ + OpenCV 4</td>
</tr>
<tr>
<td>미션 로직 (상태머신)</td>
<td>C++ + SocketCAN</td>
</tr>
<tr>
<td>MQTT 클라이언트</td>
<td>C++ + mosquittopp</td>
</tr>
<tr>
<td>MQTT 브로커</td>
<td>Mosquitto (Pi5_MQTT_AP)</td>
</tr>
<tr>
<td>주문 UI</td>
<td>C++ + Qt Widgets (RPi4, 5인치 터치)</td>
</tr>
<tr>
<td>관제 UI</td>
<td>C++ + Qt Widgets (RPi3)</td>
</tr>
<tr>
<td>서버 DB</td>
<td>SQLite (C++ API)</td>
</tr>
<tr>
<td>CAN 컨트롤러</td>
<td>MCP2515 (RPi1) / bxCAN 내장 (STM32, STM103)</td>
</tr>
<tr>
<td>CAN 트랜시버</td>
<td>SN65HVD230 (STM32, STM103) / TJA1050 내장 (MCP2515)</td>
</tr>
<tr>
<td>빌드</td>
<td>STM32CubeIDE / g++</td>
</tr>
</tbody></table>
<hr />
<h2 id="14-팀-구성-및-역할">14. 팀 구성 및 역할</h2>
<table>
<thead>
<tr>
<th>담당</th>
<th>역할</th>
<th>담당 영역</th>
</tr>
</thead>
<tbody><tr>
<td>구영모</td>
<td>FW-Drive + PM</td>
<td>STM32 주행 ECU (모터/엔코더/PID/CAN) + 전체 일정/문서</td>
</tr>
<tr>
<td>인수민</td>
<td>FW-Drive</td>
<td>STM32 주행 ECU 공동 담당</td>
</tr>
<tr>
<td>윤성진</td>
<td>Vision + System + 마일스톤</td>
<td>RPi1 카메라/라인트레이싱/ArUco/미션 상태머신/일정 관리</td>
</tr>
<tr>
<td>김민우</td>
<td>FW-Cargo</td>
<td>STM103 화물함 ECU (CAN/키패드/PIN/서보/LCD)</td>
</tr>
<tr>
<td>최지호</td>
<td>BE + Network</td>
<td>RPi3 서버 (Mosquitto/SQLite/MQTT/클라이언트 연동)</td>
</tr>
</tbody></table>
<hr />
<h2 id="15-github-브랜치-구조">15. GitHub 브랜치 구조</h2>
<pre><code>main                           ← 최종 통합 (직접 push 금지)
dev                            ← 통합 테스트
├── feature/stm32
│    ├── feature/stm32-youngmo
│    └── feature/stm32-insumin
├── feature/stm103
├── feature/stm103-sim
├── feature/rpi1
│    ├── feature/rpi1-vision
│    └── feature/rpi1-system
├── feature/rpi3
└── feature/rpi4</code></pre><p><strong>커밋 컨벤션:</strong></p>
<pre><code>[STM32] CAN RX 0x010 주행 명령 수신 구현
[STM103] CAN 0x013 도착신호 처리 구현
[RPi1] 교차로 상태머신 유턴 로직 수정
[RPi3] alert 토픽 구독 및 로그 처리
[docs] CAN ID 0x013 추가 반영</code></pre><hr />
<h2 id="16-can-통신-성공-판정-기준">16. CAN 통신 성공 판정 기준</h2>
<p><strong>Phase 1 — 내부 Loopback 테스트 (단일 노드)</strong></p>
<pre><code class="language-c">hcan1.Init.Mode = CAN_MODE_LOOPBACK;
// TX → RX 콜백 100% 수신, DLC/ID/Data 일치</code></pre>
<p><strong>Phase 2 — 2노드 Normal 통신 (STM32 ↔ 서브 STM103)</strong>
ACK 포함 HAL_OK, TEC/REC 증가 없음, BUS-OFF 없음</p>
<p><strong>Phase 3 — 3노드 통합 (STM32 + RPi1 + STM103)</strong>
0x010 주행 명령 50ms 주기 정상, 0x100 피드백 정상, 수신률 ≥ 99%</p>
<p><strong>오류 상태 모니터링:</strong></p>
<pre><code class="language-c">uint32_t esr = READ_REG(hcan1.Instance-&gt;ESR);
uint8_t tec  = (esr &gt;&gt; 16) &amp; 0xFF;   // 송신 에러 카운터
uint8_t rec  = (esr &gt;&gt; 24) &amp; 0xFF;   // 수신 에러 카운터
uint8_t lec  = (esr &gt;&gt; 4)  &amp; 0x07;   // 마지막 에러 코드
// LEC=3(Ack Error): 수신 노드 없음 or 종단저항 미연결</code></pre>
<hr />
<h2 id="17-주요-트러블슈팅-이력">17. 주요 트러블슈팅 이력</h2>
<table>
<thead>
<tr>
<th>날짜</th>
<th>문제</th>
<th>원인</th>
<th>해결</th>
</tr>
</thead>
<tbody><tr>
<td>03-03</td>
<td>UART 통신 안됨</td>
<td>ST-LINK VCP가 PB6/PB7에 내부 연결 (PA9/PA10 아님)</td>
<td>USART1 핀을 PB6(TX)/PB7(RX)로 변경</td>
</tr>
<tr>
<td>03-03</td>
<td>모터 동작 안됨</td>
<td>ENA/ENB 점퍼캡 미삽입 → L298N 출력 플로팅</td>
<td>점퍼캡 재삽입 확인</td>
</tr>
<tr>
<td>03-03</td>
<td>PWM 속도 제어 안됨</td>
<td>ENA/ENB 레벨시프터 신호 미도달</td>
<td>PA15/PA2 직결 (3.3V로 L298N 인식 확인)</td>
</tr>
<tr>
<td>03-05</td>
<td>RPM float 출력 안됨</td>
<td>newlib-nano float printf 기본 비활성화</td>
<td>링커 플래그 <code>-u _printf_float</code> 추가</td>
</tr>
<tr>
<td>03-05</td>
<td>엔코더 카운트 음수</td>
<td>A/B 채널 반대로 배선</td>
<td>배선 교체 (코드 수정 없음)</td>
</tr>
<tr>
<td>03-06</td>
<td>교차로 정지 후 미출발</td>
<td>S_JUNC_STOP → S_JUNC_STRAIGHT 전환 조건 누락</td>
<td>상태머신 전환 추가</td>
</tr>
<tr>
<td>03-06</td>
<td>유턴 미작동</td>
<td>도착 신호 CAN ID 0x010 충돌 → STM103 오수신</td>
<td>도착 신호 0x013으로 분리</td>
</tr>
<tr>
<td>03-07</td>
<td>DELIVER_WAIT 타임아웃 강제 유턴</td>
<td>도어 닫힘 전 타임아웃 발생</td>
<td>DELIVER_WAIT_MS 방식 유지, 도어닫힘(0x301=0x00)으로 유턴 트리거</td>
</tr>
<tr>
<td>03-08</td>
<td>STM103 CAN 불통</td>
<td>SN65HVD230 트랜시버 GND/VCC 오결선</td>
<td>배선 정정 (GND↔3.3V 핀 위치 확인)</td>
</tr>
<tr>
<td>03-08</td>
<td>STM103 플래시 실패</td>
<td>HardFault로 칩 잠금</td>
<td>STM32CubeProgrammer Under Reset + Full Erase → 재플래시</td>
</tr>
<tr>
<td>03-08</td>
<td>STM103 CAN Normal mode 진입 실패</td>
<td>PB8 pull-up 미적용, DBF 비트 미클리어</td>
<td>PB8 외부 pull-up 추가, 초기화 순서 정정</td>
</tr>
<tr>
<td>03-08</td>
<td>Pi5_MQTT_AP 재연결 안됨</td>
<td>RPi 재부팅 후 Wi-Fi 자동 연결 불가</td>
<td><code>sudo nmcli device wifi connect &quot;Pi5_MQTT_AP&quot;</code></td>
</tr>
<tr>
<td>03-08</td>
<td>STM32 모터 미작동 (CAN 수신은 됨)</td>
<td>CAN 타임아웃 카운터 STOP 조건 충족</td>
<td>CAN_CMD_TIMEOUT_MS=5000, RPi1에서 50ms 주기 명령 전송 유지</td>
</tr>
</tbody></table>
<hr />
<h2 id="18-미확정--튜닝-필요-항목">18. 미확정 / 튜닝 필요 항목</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>현황</th>
</tr>
</thead>
<tbody><tr>
<td>DUR_TURN_MS</td>
<td>현재 3000ms — 실제 90도 회전 시간 확인 필요</td>
</tr>
<tr>
<td>DUR_UTURN_MS</td>
<td>현재 1300ms — 실제 180도 회전 시간 확인 필요</td>
</tr>
<tr>
<td>DEFAULT_RPM</td>
<td>현재 60 — 교차로 인식 문제 시 30~40으로 낮추기</td>
</tr>
<tr>
<td>PID 게인 (Ki, Kd)</td>
<td>KP=0.5, KI=0.05 현재 적용 — Kd 추후 실험</td>
</tr>
<tr>
<td>SERVO_OPEN / SERVO_CLOSE</td>
<td>현재 2000/1000 — 실제 서보에 맞게 튜닝</td>
</tr>
<tr>
<td>Rpi1→STM103 PIN 전달</td>
<td>현재 CAN 0x012에 PIN 미포함 — delivery_mqtt.cpp에 PIN 파싱 및 전송 로직 추가 필요</td>
</tr>
</tbody></table>
<hr />
<hr />
<h1 id="부록-현재까지-진행-사항">부록. 현재까지 진행 사항</h1>
<h2 id="a-완료된-항목">A. 완료된 항목</h2>
<table>
<thead>
<tr>
<th>담당</th>
<th>항목</th>
</tr>
</thead>
<tbody><tr>
<td>구영모/인수민</td>
<td>STM32: UART, 모터 PWM, 엔코더 RPM, PID 속도 제어, CAN 0x010 수신/0x100 송신</td>
</tr>
<tr>
<td>구영모/인수민</td>
<td>U턴(DIR_UTURN=5) 추가, KI=0.05 적용, PULSE_PER_REV=5280 실측 확정</td>
</tr>
<tr>
<td>윤성진</td>
<td>ArUco + 라인트레이싱 단일 카메라 통합</td>
</tr>
<tr>
<td>윤성진</td>
<td>delivery_mqtt.cpp 상태머신 완성 (교차로 / 유턴 / 귀환)</td>
</tr>
<tr>
<td>윤성진</td>
<td>CAN + MQTT 통합, 브로커 Pi5_MQTT_AP 연동 확인</td>
</tr>
<tr>
<td>김민우</td>
<td>STM103 키패드 / LCD / 서보 기본 동작 확인</td>
</tr>
<tr>
<td>김민우</td>
<td>STM103 CAN 0x012/0x013 수신, 0x301/0x302/0x303 송신 구현 완료</td>
</tr>
<tr>
<td>김민우</td>
<td>인증 상태머신 (PIN 입력 / 목적지 검증 / 잠금 / 타임아웃) 완성</td>
</tr>
<tr>
<td>최지호</td>
<td>Mosquitto MQTT 브로커 구축, RPi1 ↔ RPi3 ↔ RPi4 통신 확인</td>
</tr>
<tr>
<td>최지호</td>
<td>RPi4→RPi3→RPi1 MQTT 경로로 목적지 + PIN 데이터 전달 및 주행 시작 확인</td>
</tr>
</tbody></table>
<h2 id="b-남은-항목">B. 남은 항목</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>내용</th>
</tr>
</thead>
<tbody><tr>
<td>RPi1 CAN 0x012 PIN 전달</td>
<td>delivery_mqtt.cpp에서 MQTT로 수신한 PIN을 CAN 0x012 페이로드에 포함시켜 STM103으로 전달하는 로직 추가</td>
</tr>
<tr>
<td>3노드 CAN 통합 테스트</td>
<td>STM32 ↔ RPi1 ↔ STM103 실차 CAN 3노드 동작 확인</td>
</tr>
<tr>
<td>교차로 / 유턴 타이밍 튜닝</td>
<td>DUR_TURN_MS, DUR_UTURN_MS 실측 조정</td>
</tr>
<tr>
<td>전체 배달 시나리오 E2E 테스트</td>
<td>RPi4 주문 → 자율주행 → 도착 → PIN 인증 → 귀환 전 구간</td>
</tr>
<tr>
<td>Fail-safe 검증</td>
<td>Heartbeat 누락 E-Stop, CAN 타임아웃 정지, PIN 잠금</td>
</tr>
<tr>
<td>데모 영상 촬영</td>
<td>최종 데모</td>
</tr>
</tbody></table>
<hr />
<p><em>문서 버전: v9.0 | 최종 업데이트: 2026-03-08</em></p>