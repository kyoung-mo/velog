<h3 id="intel-ai-sw-academy-9기-1차-팀-프로젝트-20260224--20260309">Intel AI SW Academy 9기 1차 팀 프로젝트 (2026.02.24 ~ 2026.03.09)</h3>
<blockquote>
<p>STM32 × 2 + Raspberry Pi × 3, 분산 ECU 아키텍처 기반 자율주행 무인 배달 RC카</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1c7a5ce4-0c55-4465-a189-bae90aa0faed/image.png" /></p>
<hr />
<h2 id="한-줄-요약">한 줄 요약</h2>
<blockquote>
<p>Raspberry Pi 기반의 고수준 제어와 STM32 기반의 실시간 제어를 CAN으로 연결한 분산 ECU 자율주행 무인 배달 시스템입니다.</p>
</blockquote>
<blockquote>
<p>본 글에서는 전체 시스템 설계와 아키텍처 구조를 중심으로 설명합니다.
이후 글에서는 직접 담당한 주행 ECU 구현과 CAN 통신 검증 과정을 상세히 다룹니다.</p>
</blockquote>
<hr />
<h2 id="🧠-핵심-아키텍처-요약">🧠 핵심 아키텍처 요약</h2>
<blockquote>
<p>STM32는 실시간 제어만 담당하고,
Raspberry Pi는 모든 판단과 네트워크를 담당하는
<strong>분산 ECU 구조 기반 시스템</strong></p>
</blockquote>
<hr />
<h2 id="1-문제-정의--왜-무인-배달-프로젝트인가">1. 문제 정의 — 왜 무인 배달 프로젝트인가?</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/09e50b23-da25-418c-8f09-9955458cc370/image.png" /></p>
<p>이번 프로젝트는 단순한 아이디어에서 시작된 것이 아니라,
<strong>팀원 각각이 원하는 기술 분야와 사회적 문제를 연결하면서 만들어진 결과</strong>입니다.</p>
<p>저희 팀은 총 5명으로 구성되어 있으며,
각자 관심 있는 분야를 하나씩 가져와 이를 하나의 시스템으로 통합하는 방향으로 프로젝트를 기획했습니다.</p>
<ul>
<li>저는 <strong>CAN 통신을 직접 구현해보고 싶었고</strong>,</li>
<li>한 팀원은 <strong>Vision(OpenCV)</strong>,</li>
<li>다른 팀원은 <strong>MQTT 기반 통신</strong>을 경험하고 싶어 했습니다.</li>
</ul>
<p>이렇게 기술적인 관심사를 모으다 보니,
자연스럽게 이를 적용할 수 있는 주제로 <strong>무인 배달 시스템</strong>을 떠올리게 되었고 프로젝트가 시작되었습니다.</p>
<hr />
<p>프로젝트 초기에는 비교적 단순하게 접근했습니다.</p>
<blockquote>
<p>&quot;RC카에 카메라 달고, 라인 따라가고,
목적지에서 상자 열어주면 되는 거 아닌가?&quot;</p>
</blockquote>
<p>하지만 실제로 구현을 시작하면서 생각보다 많은 문제가 드러났습니다.</p>
<p>카메라 기반 OpenCV 연산과 모터 PWM 제어를 하나의 보드에서 동시에 처리하자,
영상 처리 지연이 발생할 때마다 모터 제어 타이밍이 흔들리는 문제가 발생했습니다.</p>
<p>여기에 더해 다음 기능들까지 하나의 보드에 집중되면서 구조는 더욱 복잡해졌습니다.</p>
<ul>
<li>PIN 인증 처리</li>
<li>MQTT 통신</li>
<li>ArUco 마커 인식</li>
</ul>
<p>결과적으로,
<strong>문제가 발생했을 때 원인을 특정하기 어려운 구조</strong>가 되어버렸습니다.</p>
<hr />
<p>이 경험을 통해 단순한 RC카 구현을 넘어,
<strong>실제 차량처럼 역할을 분리한 분산 ECU 구조가 필요하다는 결론</strong>에 도달했습니다.</p>
<p>단일 보드 구조의 한계를 정리하면 다음과 같습니다.</p>
<ul>
<li><p><strong>실시간성 보장 불가</strong>
→ 모터 PWM 제어와 같은 정밀 제어가 OpenCV 연산에 의해 쉽게 영향을 받음</p>
</li>
<li><p><strong>기능 확장의 어려움</strong>
→ 하나의 노드에 기능이 집중될수록 유지보수와 디버깅이 어려워짐</p>
</li>
<li><p><strong>보안 영역 분리 불가</strong>
→ 화물함 PIN 인증과 같은 기능을 주행 시스템과 독립적으로 구성할 수 없음</p>
</li>
</ul>
<hr />
<p>결국 이 프로젝트는 단순한 기능 구현이 아니라,</p>
<blockquote>
<p><strong>&quot;실제 차량 구조처럼 역할을 나누고, 각 ECU가 협업하는 시스템을 만들어보자&quot;</strong></p>
</blockquote>
<p>라는 방향으로 설계가 전환되었습니다.</p>
<hr />
<h2 id="2-프로젝트-목표">2. 프로젝트 목표</h2>
<p>본 프로젝트의 핵심 기능은 다음과 같습니다.</p>
<ul>
<li><strong>자율 주행</strong>: 라인트레이싱 + 교차로 감지 + 목적지별 분기</li>
<li><strong>목적지 인식</strong>: ArUco 마커 ID 기반 도착 판단</li>
<li><strong>화물함 보안 수령</strong>: PIN 인증 기반 서보 제어, 오배달·미수령 자동 귀환</li>
<li><strong>원격 주문 및 관제</strong>: Qt 클라이언트 → MQTT → 서버 → 차량 출동 명령</li>
<li><strong>분산 ECU 협업</strong>: CAN 버스 단일 선로로 3개 노드 실시간 통신</li>
</ul>
<hr />
<h2 id="3-전체-시스템-구성">3. 전체 시스템 구성</h2>
<p><img alt="HW Architecture" src="https://velog.velcdn.com/images/mommers/post/3da9df0b-513b-41b4-94ca-af751899f031/image.png" /></p>
<p>시스템은 차량 탑재(온보드) 3개 노드와 오프보드 2개 노드로 구성됩니다.</p>
<table>
<thead>
<tr>
<th>노드</th>
<th>보드</th>
<th>위치</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>STM32</td>
<td>B-L475E-IOT01A (STM32L4)</td>
<td>온보드</td>
<td>주행 ECU — 모터 PWM / 엔코더 / 속도 PID</td>
</tr>
<tr>
<td>RPi1</td>
<td>Raspberry Pi 5</td>
<td>온보드</td>
<td>미션 ECU — 라인트레이싱 / ArUco / 미션 상태머신 / MQTT 게이트웨이</td>
</tr>
<tr>
<td>STM103</td>
<td>STM32F103 (MangoM32)</td>
<td>온보드</td>
<td>화물함 ECU — PIN 인증 / 서보 / LCD / 키패드</td>
</tr>
<tr>
<td>RPi3</td>
<td>Raspberry Pi 5</td>
<td>오프보드</td>
<td>MQTT 브로커 / 주문 중계 / SQLite DB</td>
</tr>
<tr>
<td>RPi4</td>
<td>Raspberry Pi 5</td>
<td>오프보드</td>
<td>Qt 주문 클라이언트 / 5인치 터치 디스플레이</td>
</tr>
</tbody></table>
<h3 id="역할-분리-원칙">역할 분리 원칙</h3>
<p>각 노드의 역할 경계를 명확하게 정의하는 것이 설계의 핵심이었습니다.</p>
<ul>
<li><strong>STM32 주행 ECU</strong>: 판단하지 않습니다. CAN으로 받은 명령을 수행하고 센서 데이터를 피드백할 뿐입니다.</li>
<li><strong>RPi1 미션 ECU</strong>: 모든 판단은 여기서 합니다. 카메라 영상 분석, 교차로 판단, 목적지 결정, 서버 통신을 전담합니다.</li>
<li><strong>STM103 화물함 ECU</strong>: 주행 시스템과 완전히 독립된 보안 영역입니다. 외부 네트워크에 직접 연결하지 않으며, CAN만 사용합니다.</li>
<li><strong>RPi3 서버</strong>: 실시간 제어에 관여하지 않습니다. 이벤트 기반 데이터 중계와 저장만 담당합니다.</li>
</ul>
<hr />
<h2 id="4-데이터-흐름--주문부터-완료까지">4. 데이터 흐름 — 주문부터 완료까지</h2>
<p><img alt="Flowchart" src="https://velog.velcdn.com/images/mommers/post/d705133f-19c9-4295-bd9b-47bf9f6d7c18/image.png" /></p>
<pre><code>① 주문 생성
   RPi4 Qt UI → 목적지(A~D) + PIN 4자리 입력
   → MQTT → RPi3 DB 저장

② 차량 출동
   RPi3 → MQTT → RPi1 출동 명령 (destination + pin + order_id)
   RPi1 → CAN 0x012 → STM103: PIN + 목적지 전달
   RPi1: S_WAIT_CMD → S_FOLLOW (자율 주행 시작)

③ 자율 주행
   RPi1 카메라 → 라인 ROI 이진화 → 방향 결정
   → CAN 0x010 (50ms) → STM32 PID 모터 제어
   교차로 감지 시 목적지별 행동 테이블에 따라 좌/우/직진 분기

④ 목적지 도착
   RPi1: ArUco 마커 ID(1~4) 감지 → 즉시 정지
   → CAN 0x013 → STM103 도착 신호
   → MQTT → RPi3 arrived 보고

⑤ 화물함 인증 및 수령
   STM103: LCD 안내 → 키패드 목적지 확인 → PIN 4자리 입력
   성공 → 서보 열림(5초) → 닫힘 → CAN 0x301=0x00 → RPi1 유턴 트리거
   실패 5회 → 10초 잠금 / 오배달·미수령 30초 → 즉시 유턴

⑥ 귀환 및 완료
   RPi1: U턴 → 라인 재탐색 → 귀환 교차로 테이블 추종
   ArUco ID=0(출발지) 감지 → S_FINISHED
   → MQTT → RPi3 completed 보고</code></pre><h3 id="🎬-시연-영상">🎬 시연 영상</h3>
<p><a href="https://www.youtube.com/watch?v=Z4IQcvlYzos"><img alt="Demo Video" src="https://img.youtube.com/vi/Z4IQcvlYzos/0.jpg" /></a></p>
<hr />
<h2 id="5-통신-구조--can과-mqtt를-함께-쓴-이유">5. 통신 구조 — CAN과 MQTT를 함께 쓴 이유</h2>
<p>차량 내부 통신으로 CAN을 선택한 것은 처음부터 의도된 결정이었습니다. CAN 통신은 제가 이번 프로젝트에서 경험하고 싶었던 기술이기도 했고, 기술적으로도 차량 내부 실시간 제어에 가장 적합한 선택이었습니다.</p>
<p>MQTT는 브로커를 거치는 구조라 지연이 불규칙합니다.
RPi1에서 STM32로 모터 명령을 50ms마다 보내야 하는 상황에서 비결정적인 TCP 기반 통신은 맞지 않습니다.</p>
<p>반면 CAN은 결정론적 동작이 보장되고 ACK 기반 오류 감지까지 됩니다.</p>
<blockquote>
<p>결과적으로 <strong>차량 내부는 CAN, 외부 통신은 MQTT</strong>로 역할을 분리했습니다.</p>
</blockquote>
<h3 id="can-250-kbps--차량-내부-실시간-통신">CAN (250 kbps) — 차량 내부 실시간 통신</h3>
<p><img alt="can_connection" src="https://velog.velcdn.com/images/mommers/post/6dcaf5d3-4f1a-4215-85fa-0fd3337a2963/image.png" /></p>
<p><img alt="can_table" src="https://velog.velcdn.com/images/mommers/post/5082975b-b0f5-43cd-93e5-5d2555721235/image.png" /></p>
<pre><code>  STM32 ────────────── RPi1 ─────────────── STM103
(주행 ECU)          (미션 ECU)           (화물함 ECU)

  ← CAN 0x010 주행 명령 (50ms)
  ← CAN 0x011 E-Stop
    CAN 0x100 속도 피드백 (50ms) →
    CAN 0x200 Heartbeat (100ms) →
                     CAN 0x012 배달정보 →
                     CAN 0x013 도착 신호 →
                   ← CAN 0x301 도어 상태
                   ← CAN 0x302 인증 결과
                     CAN 0x303 PIN 실패(잠금) →</code></pre><ul>
<li><strong>실시간성</strong>: 50ms 주기 명령 전송, 버스 점유율 1% 미만</li>
<li><strong>신뢰성</strong>: ACK 기반 오류 감지, BUS-OFF 자동 복구</li>
<li><strong>확장성</strong>: 노드 추가 시 버스에 연결만 하면 됩니다</li>
<li><strong>MCU 내장 컨트롤러</strong>: STM32는 bxCAN 내장으로 외부 IC 불필요</li>
</ul>
<h3 id="mqtt--차량-외부-원격-통신">MQTT — 차량 외부 원격 통신</h3>
<p><img alt="mqtt_table" src="https://velog.velcdn.com/images/mommers/post/d522f5c0-10a7-4354-9ab4-d2a9e8137e8c/image.png" /></p>
<pre><code>RPi1 (차량) ── Wi-Fi ── RPi3 (브로커/서버) ── RPi4 (클라이언트)</code></pre><ul>
<li><strong>확장성</strong>: 차량이 늘어도 브로커 연결 하나로 통합 관리 가능</li>
<li><strong>비동기 이벤트 처리</strong>: 주문, 도착, 완료 이벤트를 발행/구독 구조로 처리</li>
<li><strong>단일 연결 유지</strong>: 차량당 RPi1 하나만 브로커에 연결</li>
</ul>
<h3 id="역할-구분-요약">역할 구분 요약</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>CAN</th>
<th>MQTT</th>
</tr>
</thead>
<tbody><tr>
<td>범위</td>
<td>차량 내부</td>
<td>차량 ↔ 서버 ↔ 클라이언트</td>
</tr>
<tr>
<td>특성</td>
<td>실시간, 결정론적</td>
<td>비동기, 이벤트 기반</td>
</tr>
<tr>
<td>목적</td>
<td>모터 제어 / 센서 피드백 / 인증</td>
<td>주문 수신 / 상태 보고 / 관제</td>
</tr>
</tbody></table>
<hr />
<h2 id="6-설계-철학">6. 설계 철학</h2>
<p>이 프로젝트를 설계하면서 가장 많이 고민한 부분은 <strong>&quot;어디까지를 STM32가 하고, 어디부터를 RPi가 해야 하는가&quot;</strong>였습니다.</p>
<p>처음에는 경계가 명확하지 않았습니다. RPi에서 PWM도 직접 제어해보려 했고, STM32에서 CAN 메시지를 보고 스스로 판단하는 로직을 넣어보려 했던 시도도 있었습니다. 하지만 그렇게 하면 어느 쪽도 제 역할을 제대로 못 하는 구조가 됩니다.</p>
<p>결국 <strong>Separation of Concerns(관심사의 분리)</strong> 원칙으로 정리했습니다.</p>
<ul>
<li><strong>Real-time Control</strong>: STM32가 전담합니다. 판단 없이 명령만 수행합니다.</li>
<li><strong>High-level Decision</strong>: RPi1이 전담합니다. 모든 판단과 외부 통신을 담당합니다.</li>
<li><strong>Security Domain</strong>: STM103이 전담합니다. 주행 시스템과 물리적으로 분리된 독립 보안 영역입니다.</li>
</ul>
<p>이 구조 덕분에 RPi1이 잠깐 처리 지연이 발생해도 STM32는 마지막 명령을 유지하며 주행을 계속할 수 있었습니다. 그리고 RPi1이 완전히 다운되는 최악의 상황에서는 STM32의 IWDG Watchdog(300ms)이 MCU를 리셋하여 모터를 즉시 정지시킵니다.</p>
<p>단순히 &quot;기능을 나눈&quot; 것이 아니라, <strong>고장 상황에서도 안전하게 멈출 수 있는 구조</strong>를 만든 것이 이 설계의 핵심입니다.</p>
<hr />
<h2 id="📌-이-구조의-핵심-장점">📌 이 구조의 핵심 장점</h2>
<ul>
<li><strong>실시간 제어와 비실시간 처리를 완전히 분리</strong> — 타이밍 충돌 없음</li>
<li><strong>문제 발생 시 원인 추적이 쉬움</strong> — ECU 단위로 독립 디버깅 가능</li>
<li><strong>ECU 단위 확장 가능</strong> — 노드 추가 시 CAN 버스에 연결만 하면 됨</li>
<li><strong>안전성 확보</strong> — IWDG Watchdog 기반 Fail-safe, CAN 타임아웃 자동 정지</li>
</ul>
<hr />
<h2 id="마치며">마치며</h2>
<p>다음 글에서는 직접 담당한 <strong>STM32L4 주행 ECU 설계 및 CAN 통신 구현</strong> 과정을 다룹니다. B-L475E 보드의 핀 충돌 이슈부터 모터 PWM, 엔코더 RPM 측정, 속도 PID, 그리고 MangoM32를 활용한 CAN 통신 단계별 검증까지 정리할 예정입니다.</p>
<p><strong>🔗 GitHub</strong>
전체 코드와 상세 구현은 아래에서 확인할 수 있습니다.</p>
<p><a href="https://github.com/kyoung-mo/can-based-autonomous-delivery-car"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&amp;logo=github" /></a></p>