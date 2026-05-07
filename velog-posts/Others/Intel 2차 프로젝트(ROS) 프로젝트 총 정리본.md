<p>ROS2 기반으로 2차 프로젝트를 진행했습니다. 총 정리본 먼저 올리고 천천히 정리해야지 . .</p>
<hr />
<h3 id="🏥-자율주행-기반-스마트-병동-관리-시스템">🏥 자율주행 기반 스마트 병동 관리 시스템</h3>
<h4 id="project-summary-v63">Project Summary v6.3</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/17cf9e96-867f-46a2-9a03-6ac9260220ce/image.png" /></p>
<hr />
<h2 id="프로젝트-개요">프로젝트 개요</h2>
<p>감염병 확산 환경에서 의료진과 환자 간 불필요한 접촉을 최소화하는 동시에, 거동이 불편한 입원 환자의 안전과 편의를 24시간 보장하기 위해 자율주행 로봇을 도입한다.</p>
<p>기존 병원 시스템에서는 낙상 사고 발견 지연, 야간 인력 부족, 환자 호출에 대한 즉각적인 대응 어려움 등의 문제가 존재한다.</p>
<p>이를 해결하기 위해 로봇이 자율 순찰하며 낙상을 감지하고, 환자가 버튼 호출 및 음성으로 필요한 사항을 전달할 수 있는 비대면 케어 인프라를 구축한다.</p>
<ul>
<li><strong>개발 기간:</strong> 1주일</li>
<li><strong>팀 인원:</strong> 4명</li>
<li><strong>주요 하드웨어:</strong> TurtleBot3 × 2, Intel RealSense D435 × 1, OpenCR1 × 2 (방 입구), USB 마이크 × 1, MAX98357A × 1</li>
</ul>
<hr />
<h2 id="v62-→-v63-변경-사항">v6.2 → v6.3 변경 사항</h2>
<ul>
<li><strong>토픽명 변경 (101/102 → room1/room2)</strong><ul>
<li><code>/hospital/call/101</code> → <code>/hospital/call/room1</code></li>
<li><code>/hospital/call/102</code> → <code>/hospital/call/room2</code></li>
<li><code>/hospital/emergency_event/101</code> → <code>/hospital/emergency_event/room1</code></li>
<li><code>/hospital/emergency_event/102</code> → <code>/hospital/emergency_event/room2</code></li>
</ul>
</li>
<li><strong>약 수령 위치 변경</strong><ul>
<li>기존: S1 스테이션으로 이동 후 약 수령</li>
<li>변경: START 좌표(맵 원점, 간호사 스테이션 위치)로 이동 후 약 수령 → 환자 방 → 본인 스테이션 복귀</li>
</ul>
</li>
<li><strong>이동 명령 방식 명시</strong><ul>
<li>Domain Bridge 환경에서 Nav2 Action 미지원 확인</li>
<li><code>/navigate_to_pose</code> Action → <code>/goal_pose</code> Topic 방식으로 전환 (현재 코드 반영)</li>
</ul>
</li>
<li><strong>CORRIDOR_MID 좌표 확정</strong><ul>
<li><code>{2.030, 0.528, 1.0}</code> (publish_point 실측, map 프레임 절대좌표)</li>
</ul>
</li>
</ul>
<hr />
<h2 id="물리적-환경-구성">물리적 환경 구성</h2>
<pre><code>[관제 PC - Ubuntu, DOMAIN_ID=5]
   ├── D435 (USB 연결, 탑뷰 설치 / 높이 약 0.8~1.0m) ✅
   ├── OpenCR1 (USB 시리얼 /dev/ttyACM0) ← 방1 버튼/LED/부저/LCD ✅
   ├── OpenCR1 (USB 시리얼 /dev/ttyACM1) ← 방2 버튼/LED/부저/LCD ✅
   ├── Nav2 / AMCL ✅
   ├── HospitalTaskManager ✏️
   ├── YOLO (카메라 토픽 구독 → PC에서 추론) ✅
   ├── Whisper STT ✅
   └── Qt6 GUI (순찰 경로 설정 포함) ✅

[세트장 구성]
Station1(S1) / Station2(S2) ✏️
   ↓
복도 ── 방1 ── 방2
         |       |
      [버튼]  [버튼]  ← OpenCR1 micro-ROS (방 입구)
      [RGB]   [RGB]   ← 초록:정상 / 파랑:출동중 / 빨강:긴급
      [LCD]   [LCD]
      [부저]  [부저]

쓰레기 구역 (별도)</code></pre><ul>
<li>병실 2개 (각 65cm × 65cm) + 복도 + 스테이션 + 쓰레기 구역</li>
<li>D435는 방1/방2 경계 위 탑뷰 설치 → 두 방 동시 커버</li>
<li>D435 커버 영역: 방1 침대, 방1 쓰레기통, 방2 침대, 방2 쓰레기통 (ROI 4구역)</li>
<li>OpenCR1은 미사용 터틀봇에서 분리하여 사용</li>
</ul>
<hr />
<h2 id="터틀봇-구성">터틀봇 구성</h2>
<table>
<thead>
<tr>
<th>장치</th>
<th>터틀봇1 (Robot1)</th>
<th>터틀봇2 (Robot2)</th>
</tr>
</thead>
<tbody><tr>
<td>ROS_DOMAIN_ID</td>
<td>5</td>
<td>7</td>
</tr>
<tr>
<td>복귀 스테이션</td>
<td>S1</td>
<td>S2</td>
</tr>
<tr>
<td>라이다</td>
<td>✅</td>
<td>✅</td>
</tr>
<tr>
<td>카메라 모듈2</td>
<td>✅</td>
<td>✅</td>
</tr>
<tr>
<td>MAX98357A 스피커</td>
<td>✅</td>
<td>❌</td>
</tr>
<tr>
<td>USB 마이크</td>
<td>✅</td>
<td>❌</td>
</tr>
<tr>
<td>내장 OpenCR 부저/버튼</td>
<td>✅</td>
<td>✅</td>
</tr>
<tr>
<td>역할</td>
<td>순찰 + 낙상 감지 + 음성 인터랙션</td>
<td>순찰 + 낙상 감지</td>
</tr>
</tbody></table>
<hr />
<h2 id="domain-bridge-구성">Domain Bridge 구성</h2>
<pre><code class="language-yaml"># bridge_config.yaml
name: turtlebot_test_bridge
from_domain: 7   # Robot2 (TurtleBot2)
to_domain: 5     # 관제 PC

topics:
  amcl_pose:
    type: geometry_msgs/msg/PoseWithCovarianceStamped
    remap: /robot2/amcl_pose

  battery_state:
    type: sensor_msgs/msg/BatteryState
    remap: /robot2/battery_state

  robot2/goal_pose:
    type: geometry_msgs/msg/PoseStamped
    reversed: True
    remap: goal_pose</code></pre>
<pre><code>관제 PC (domain5) ←→ [Domain Bridge] ←→ Robot2 (domain7)

robot2 → /amcl_pose         bridge→  관제PC /robot2/amcl_pose
robot2 → /battery_state     bridge→  관제PC /robot2/battery_state
관제PC → /robot2/goal_pose  bridge→  robot2 /goal_pose</code></pre><hr />
<h2 id="노드-전체-구조">노드 전체 구조</h2>
<h3 id="관제-pc에서-실행되는-노드">관제 PC에서 실행되는 노드</h3>
<pre><code>[기존 패키지 - 갖다 쓰면 됨]
├── nav2_bringup           ← 자율주행 스택
├── amcl                   ← 위치 추정
├── map_server             ← 맵 로딩
├── domain_bridge          ← Robot2 통신 브릿지
└── micro_ros_agent × 2   ← 방 입구 OpenCR1 통신

[커스텀 노드 - 직접 구현]
├── hospital_task_manager  (C++)    ← 이벤트 판단 + 이동 명령 ✏️
├── yolo_node              (Python) ← 카메라 영상 → YOLO 추론 ✅
├── d435_node              (Python) ← D435 깊이값 → 감지 ✅
├── whisper_node           (Python) ← 오디오 → STT → 키워드 ✅
├── tts_node               (Python) ← TTS 음성 생성 → 재생 명령 ✅
└── gui_node               (C++)    ← Qt6 관제 대시보드 + 순찰 경로 설정 ✅</code></pre><h3 id="터틀봇1-rpi4에서-실행되는-노드">터틀봇1 RPi4에서 실행되는 노드</h3>
<pre><code>├── turtlebot3_bringup     ← 라이다, 모터 (기존 패키지) ✅
├── camera_node            ← 카메라 영상 발행 (기존 패키지) ✅
├── mic_node        (C++)  ← 마이크 녹음 → 오디오 토픽 발행 ✅
└── tts_play_node   (C++)  ← TTS 재생 명령 수신 → MAX98357A 출력 ✅</code></pre><h3 id="터틀봇2-rpi4에서-실행되는-노드">터틀봇2 RPi4에서 실행되는 노드</h3>
<pre><code>├── turtlebot3_bringup     ← 라이다, 모터 (기존 패키지) ✅
└── camera_node            ← 카메라 영상 발행 (기존 패키지) ✅</code></pre><h3 id="방-입구-opencr1에서-실행되는-노드">방 입구 OpenCR1에서 실행되는 노드</h3>
<pre><code>[OpenCR1 - 방1 입구]
└── button_led_node  (Arduino C++) ← 버튼 + RGB LED + 부저 + LCD ✅

[OpenCR1 - 방2 입구]
└── button_led_node  (Arduino C++) ← 버튼 + RGB LED + 부저 + LCD ✅</code></pre><hr />
<h2 id="패키지-구조">패키지 구조</h2>
<pre><code>hospital_robot_ws/  (관제 PC)
├── hospital_control/          ← C++ 패키지 (hospital_task_manager) ✏️
│   └── config/
│       └── bridge_config.yaml ← Domain Bridge 설정 ✅
├── hospital_vision/           ← Python 패키지 (yolo_node, d435_node) ✅
├── hospital_voice/            ← Python 패키지 (whisper_node, tts_node) ✅
├── hospital_interface/        ← Arduino C++ (button_led_node) ✅
└── hospital_gui/              ← C++ 패키지 (Qt6 gui_node) ✏️

hospital_robot_ws/  (터틀봇1 RPi4)
└── hospital_voice/            ← C++ 패키지 (mic_node, tts_play_node) ✅</code></pre><hr />
<h2 id="순찰-경로">순찰 경로</h2>
<pre><code>배터리 높은 로봇 선택
    ↓
CORRIDOR_L (왼쪽 복도)
    ↓
101 (방1)
    ↓
CORRIDOR_MID (중간 복도)
    ↓
102 (방2)
    ↓
CORRIDOR_MID (중간 복도)
    ↓
waste front (오른쪽 복도)
    ↓
waste (쓰레기 보관함)
    ↓
waste front (오른쪽 복도)
    ↓
S1 or S2 (스테이션 복귀)</code></pre><ul>
<li>이벤트 발생 시 순찰 중단 → 이벤트 처리 → 스테이션 복귀 → 10초 후 재순찰 (처음부터)</li>
<li>Robot1은 항상 S1으로, Robot2는 항상 S2로 복귀</li>
</ul>
<hr />
<h2 id="전체-동작-흐름">전체 동작 흐름</h2>
<h3 id="평상시-순찰">평상시 순찰</h3>
<pre><code>두 로봇 스테이션 대기
    → patrol_scheduler (10초 타이머)
    → 배터리 높은 로봇 선택
    → 순찰 경로 순서대로 자율주행
        ├── CORRIDOR_L → 101 → CORRIDOR_MID → 102 → CORRIDOR_MID → waste → S1/S2
    → yolo_node: 카메라 토픽 구독 → YOLO11n-pose 추론
        ├── 정상 자세 → 계속 순찰
        └── 낙상 감지 → 낙상 감지 흐름으로 전환</code></pre><h3 id="낙상-감지-흐름-핵심-변경">낙상 감지 흐름 (핵심 변경)</h3>
<pre><code>터틀봇 카메라 → yolo_node → 낙상 감지
    → /hospital/emergency_call 발행
    → task_manager 수신
    → 해당 로봇 그 자리 정지
    → 내장 OpenCR 부저 울림 시작
    → 의료진 현장 도착
    → 터틀봇 내장 버튼 누름 (/sensor_state.button 수신)
    → 부저 정지
    → 해당 로봇 스테이션 복귀 (Robot1→S1, Robot2→S2)
    → 10초 후 재순찰</code></pre><h3 id="d435-낙상-의심-흐름">D435 낙상 의심 흐름</h3>
<pre><code>D435 → 낙상 의심 → /hospital/fall_suspected 발행
    → 가까운 로봇 파견 (순찰 중단)
    → 로봇 현장 도착 → yolo_node 현장 확인
        ├── 낙상 맞으면 → 그 자리 정지 + 부저 → 버튼 누르면 복귀
        └── 오탐지면 → 스테이션 복귀 → 재순찰</code></pre><h3 id="버튼-호출-→-음성-인터랙션-흐름">버튼 호출 → 음성 인터랙션 흐름</h3>
<blockquote>
<p><strong>Whisper는 터틀봇1이 병실에 도착한 후에만 동작</strong>
평소 순찰 중에는 마이크 녹음 및 STT 비활성</p>
</blockquote>
<pre><code>환자가 버튼 1회 클릭
    → /hospital/call/101 (또는 /hospital/call/102) 발행
    → LCD: &quot;Calling...&quot; / RGB LED: 파랑 / 부저 1회
    → task_manager: 놀고 있는 로봇 우선, 둘 다 바쁘면 가까운 쪽 파견
    → /hospital/emergency_event/101 → &quot;dispatching&quot; 발행
    → 터틀봇 병실 도착
    → task_manager: /hospital/tts_trigger 발행 (data: &quot;101&quot; or &quot;102&quot;)
    → tts_node: &quot;필요한 거 있으실까요?&quot; TTS 생성 → /robot_1/tts_play 발행
    → tts_play_node: MAX98357A 재생 (~2초)
    → tts_node: 3초 대기 후 /robot_1/mic_trigger 자동 발행
    → mic_node: 트리거 수신 → 4초 녹음 → /robot_1/audio 발행
    → whisper_node: STT 변환 → 키워드 매칭
        ├── &quot;약&quot; / &quot;약 주세요&quot;
        │    → /hospital/medicine_request 발행
        │    → 스테이션 경유 → 방 복귀 → &quot;약 도착했습니다&quot; TTS 재생
        │
        ├── &quot;쓰레기&quot; / &quot;쓰레기통&quot; / &quot;비워줘&quot;
        │    → /hospital/trash_request 발행
        │    → 방 → 쓰레기 수거장 → 스테이션 복귀
        │
        ├── &quot;간호사&quot; / &quot;의사&quot; / &quot;도와줘&quot; / &quot;살려줘&quot;
        │    → /hospital/emergency_call 발행
        │    → RGB LED: 빨강 / 부저 3회 / LCD: &quot;EMERGENCY!&quot;
        │
        └── &quot;괜찮아&quot; / &quot;됐어&quot; / 미인식
             → RGB LED: 초록 / LCD: &quot;Normal&quot;
             → 스테이션 복귀 → 재순찰</code></pre><h3 id="약-요청-흐름">약 요청 흐름</h3>
<pre><code>/hospital/medicine_request 수신 (data: 방 번호)
    → next_goal = 방 번호 저장
    → START 좌표로 먼저 출발 (간호사 스테이션, 약 수령)
    → START 도착 → 약 수령 완료
    → 환자 방으로 이동
    → 방 도착 → &quot;약 도착했습니다&quot; TTS 재생
    → 본인 스테이션 복귀 (Robot1→S1, Robot2→S2)</code></pre><h3 id="쓰레기-수거-흐름">쓰레기 수거 흐름</h3>
<p><strong>음성 요청 (환자가 직접 요청)</strong></p>
<pre><code>/hospital/trash_request 수신
    → 현재 그 방에 있는 로봇 찾기
    → 해당 로봇 → waste로 즉시 출발
    → waste 도착 → 스테이션 복귀</code></pre><p><strong>D435 자동 감지</strong></p>
<pre><code>/hospital/facility_status 수신
    → next_goal = &quot;waste&quot; 예약
    → 로봇을 방으로 파견
    → 방 도착 → waste로 이동
    → waste 도착 → 스테이션 복귀</code></pre><hr />
<h2 id="이벤트-처리-구조">이벤트 처리 구조</h2>
<table>
<thead>
<tr>
<th>이벤트</th>
<th>감지 방법</th>
<th>토픽</th>
<th>우선순위</th>
<th>로봇 동작</th>
</tr>
</thead>
<tbody><tr>
<td><strong>낙상 감지</strong></td>
<td>YOLO keypoint</td>
<td><code>/hospital/emergency_call</code></td>
<td>🔴 즉시 정지</td>
<td>그 자리 정지 → 내장 부저 → 버튼 누르면 복귀</td>
</tr>
<tr>
<td><strong>낙상 의심</strong></td>
<td>D435 깊이값</td>
<td><code>/hospital/fall_suspected</code></td>
<td>🔴 즉시 파견</td>
<td>가까운 로봇 파견 → YOLO 확인</td>
</tr>
<tr>
<td><strong>버튼 호출</strong></td>
<td>방 입구 버튼 1회</td>
<td><code>/hospital/call/101(102)</code></td>
<td>🟡 하던 일 후</td>
<td>놀고 있는 로봇 파견 → 음성 인터랙션</td>
</tr>
<tr>
<td><strong>긴급 음성</strong></td>
<td>Whisper &quot;도와줘/살려줘&quot;</td>
<td><code>/hospital/emergency_call</code></td>
<td>🔴 즉시 처리</td>
<td>방 입구 LED/부저/LCD 긴급</td>
</tr>
<tr>
<td><strong>약 요청</strong></td>
<td>Whisper &quot;약 주세요&quot;</td>
<td><code>/hospital/medicine_request</code></td>
<td>🟡 하던 일 후</td>
<td>START 경유(약 수령) → 방 복귀 → TTS → 스테이션 복귀</td>
</tr>
<tr>
<td><strong>쓰레기 수거</strong></td>
<td>Whisper &quot;쓰레기&quot;</td>
<td><code>/hospital/trash_request</code></td>
<td>🟡 하던 일 후</td>
<td>방 → 수거장 → 스테이션 복귀</td>
</tr>
<tr>
<td><strong>쓰레기 가득</strong></td>
<td>D435 깊이값</td>
<td><code>/hospital/facility_status</code></td>
<td>🟡 하던 일 후</td>
<td>방으로 이동 → 수거장 → 스테이션 복귀</td>
</tr>
</tbody></table>
<hr />
<h2 id="핵심-ros2-토픽-구조">핵심 ROS2 토픽 구조</h2>
<pre><code>[이벤트 토픽]
/hospital/emergency_call          ← 낙상 감지 or 긴급 음성
/hospital/fall_suspected          ← D435 낙상 의심
/hospital/call/101              ← 방1 버튼 호출
/hospital/call/102              ← 방2 버튼 호출
/hospital/medicine_request        ← Whisper &quot;약 주세요&quot;
/hospital/trash_request           ← Whisper &quot;쓰레기&quot;
/hospital/facility_status         ← D435 쓰레기 가득 참
/hospital/emergency_event/101   ← 방1 RGB LED/부저/LCD 제어
/hospital/emergency_event/102   ← 방2 RGB LED/부저/LCD 제어
/hospital/tts_trigger             ← task_manager → tts_node 재생 트리거

[Robot1 토픽 - domain5 직접]
/amcl_pose                        ← Robot1 현재 위치
/battery_state                    ← Robot1 배터리
/goal_pose                        ← Robot1 이동 목표
/sensor_state                     ← Robot1 내장 버튼/부저 상태
/robot_1/audio                    ← 마이크 녹음
/robot_1/mic_trigger              ← tts_node → mic_node 녹음 트리거
/robot_1/tts_play                 ← tts_node → tts_play_node 재생 명령
/robot_1/camera/image_raw         ← Robot1 카메라 영상

[Robot2 토픽 - domain bridge 경유]
/robot2/amcl_pose                 ← Robot2 현재 위치 (bridge)
/robot2/battery_state             ← Robot2 배터리 (bridge)
/robot2/goal_pose                 ← Robot2 이동 목표 (bridge, reversed)
/robot_2/camera/image_raw         ← Robot2 카메라 영상</code></pre><hr />
<h2 id="로봇-선정-로직">로봇 선정 로직</h2>
<pre><code>긴급 상황 (is_emergency=true)
    → 두 로봇 중 거리 가까운 쪽 무조건 선택

일반 상황 (is_emergency=false)
    → 한쪽만 바쁘면 → 놀고 있는 쪽 선택
    → 둘 다 바쁘거나 둘 다 한가하면 → 거리 가까운 쪽 선택</code></pre><hr />
<h2 id="파트-구성-4명">파트 구성 (4명)</h2>
<h3 id="팀원-a---자율주행-system-integrator">팀원 A - 자율주행 (System Integrator)</h3>
<p><strong>담당 노드</strong></p>
<table>
<thead>
<tr>
<th>노드</th>
<th>언어</th>
<th>실행 위치</th>
</tr>
</thead>
<tbody><tr>
<td><code>hospital_task_manager</code></td>
<td>C++</td>
<td>관제 PC</td>
</tr>
<tr>
<td>Nav2 / AMCL / map_server</td>
<td>기존 패키지</td>
<td>관제 PC</td>
</tr>
<tr>
<td>domain_bridge</td>
<td>기존 패키지</td>
<td>관제 PC</td>
</tr>
</tbody></table>
<p><strong>통신 구조</strong></p>
<pre><code>[hospital_task_manager]

구독하는 토픽:
├── /hospital/emergency_call       ← B(yolo_node), C(whisper_node)
├── /hospital/fall_suspected       ← B(d435_node)
├── /hospital/call/101           ← C(button_led_node 방1)
├── /hospital/call/102           ← C(button_led_node 방2)
├── /hospital/medicine_request     ← C(whisper_node)
├── /hospital/trash_request        ← C(whisper_node)
├── /hospital/facility_status      ← B(d435_node)
├── /amcl_pose                     ← Robot1 위치
├── /robot2/amcl_pose              ← Robot2 위치 (bridge)
├── /battery_state                 ← Robot1 배터리
├── /robot2/battery_state          ← Robot2 배터리 (bridge)
└── /sensor_state                  ← Robot1/2 내장 버튼 상태

발행하는 토픽:
├── /goal_pose                     → Robot1 이동 목표
├── /robot2/goal_pose              → Robot2 이동 목표 (bridge)
├── /hospital/emergency_event/101 → C(button_led_node 방1)
├── /hospital/emergency_event/102 → C(button_led_node 방2)
└── /hospital/tts_trigger          → C(tts_node)</code></pre><p><strong>이동 명령 방식</strong></p>
<p>Domain Bridge 환경에서 Nav2 Action(<code>/navigate_to_pose</code>)이 지원되지 않으므로 <code>/goal_pose</code> Topic으로 목표 좌표를 직접 발행하는 방식을 사용한다. 도착 판정은 AMCL pose를 구독해 목표 좌표와의 거리가 35cm 이내가 되면 도착으로 처리한다.</p>
<pre><code class="language-cpp">// 이동 명령 (Topic 방식)
r1_goal_pub_-&gt;publish(goal_msg);  // Robot1: /goal_pose
r2_goal_pub_-&gt;publish(goal_msg);  // Robot2: /robot2/goal_pose (bridge 경유)

// 도착 판정
if (dist &lt; 0.35) { process_arrival_logic(robot_id, target); }</code></pre>
<p><strong>room_map 좌표</strong></p>
<pre><code class="language-cpp">room_map_[&quot;START&quot;]        = {0.01,   0.01,  1.0};  // 간호사 스테이션 (약 수령 위치)
room_map_[&quot;CORRIDOR_L&quot;]   = {미확정};               // 왼쪽 복도
room_map_[&quot;101&quot;]          = {1.686, -0.663, 1.0};
room_map_[&quot;CORRIDOR_MID&quot;] = {2.030,  0.528, 1.0};  // 확정 (publish_point 실측)
room_map_[&quot;102&quot;]          = {2.450, -0.546, 1.0};
room_map_[&quot;waste&quot;]        = {5.379,  1.027, 1.0};
room_map_[&quot;S1&quot;]           = {4.437, -0.969, 1.0};
room_map_[&quot;S2&quot;]           = {5.134, -0.996, 1.0};</code></pre>
<p><strong>코드 수정 완료 사항 (v6.3)</strong></p>
<ul>
<li>✅ 토픽명: <code>/hospital/call/room1</code>, <code>/hospital/call/room2</code> 분리</li>
<li>✅ 토픽명: <code>/hospital/emergency_event/room1</code>, <code>/hospital/emergency_event/room2</code> 분리</li>
<li>✅ <code>waste_full_sub_</code> 구독자 연결</li>
<li>✅ 순찰 경로 웨이포인트 배열 구현 (waste_front 포함)</li>
<li>✅ Robot 복귀 스테이션 robot_id 기준 분기 (Robot1→S1, Robot2→S2)</li>
<li>✅ <code>last_patrol_time</code> 갱신 위치 → S1/S2 복귀 완료 시점</li>
<li>✅ 약 수령 위치 → <code>phar</code> 경유</li>
<li>✅ <code>go_to_with_routing()</code>: 경유지 자동 라우팅</li>
<li>✅ <code>send_nav_sequence()</code> + <code>waypoint_queues_</code>: 웨이포인트 큐 이동</li>
<li>✅ <code>is_high_priority_active()</code>: 우선순위 체계</li>
<li>✅ <code>suspected_callback</code>: busy 무관 강제 파견</li>
<li>✅ <code>start/stop_scan_rotation()</code>: 낙상 의심 20초 회전 탐색</li>
<li>✅ <code>waste_front</code> 좌표 추가 및 경유 적용</li>
</ul>
<hr />
<h3 id="팀원-b---비전--센서-vision--embedded">팀원 B - 비전 &amp; 센서 (Vision &amp; Embedded)</h3>
<p><strong>담당 노드</strong></p>
<table>
<thead>
<tr>
<th>노드</th>
<th>언어</th>
<th>실행 위치</th>
</tr>
</thead>
<tbody><tr>
<td><code>yolo_node</code></td>
<td>Python</td>
<td>관제 PC</td>
</tr>
<tr>
<td><code>d435_node</code></td>
<td>Python</td>
<td>관제 PC</td>
</tr>
</tbody></table>
<p><strong>통신 구조</strong></p>
<pre><code>[yolo_node]
구독: /robot_1/camera/image_raw, /robot_2/camera/image_raw
발행: /hospital/emergency_call
동작: YOLO11n-pose keypoint → 낙상 판단

[d435_node]
발행: /hospital/fall_suspected, /hospital/facility_status
동작: ROI 4구역 깊이값 분석</code></pre><hr />
<h3 id="팀원-c---음성--micro-ros-field-interface">팀원 C - 음성 &amp; micro-ROS (Field Interface)</h3>
<p><strong>담당 노드</strong></p>
<table>
<thead>
<tr>
<th>노드</th>
<th>언어</th>
<th>실행 위치</th>
<th>상태</th>
</tr>
</thead>
<tbody><tr>
<td><code>whisper_node</code></td>
<td>Python</td>
<td>관제 PC</td>
<td>✅</td>
</tr>
<tr>
<td><code>tts_node</code></td>
<td>Python</td>
<td>관제 PC</td>
<td>✅</td>
</tr>
<tr>
<td><code>button_led_node</code></td>
<td>Arduino C++</td>
<td>방 입구 OpenCR1 × 2</td>
<td>✅</td>
</tr>
<tr>
<td><code>mic_node</code></td>
<td>C++</td>
<td>터틀봇1 RPi4</td>
<td>✅</td>
</tr>
<tr>
<td><code>tts_play_node</code></td>
<td>C++</td>
<td>터틀봇1 RPi4</td>
<td>✅</td>
</tr>
</tbody></table>
<p><strong>Whisper 키워드</strong></p>
<pre><code class="language-python">KEYWORDS = {
    'medicine':  ['약', '약 주세요', '약주세요'],
    'emergency': ['간호사', '의사', '도와줘', '도와주세요', '살려줘'],
    'ok':        ['괜찮아', '괜찮아요', '됐어', '됐어요'],
    'trash':     ['쓰레기', '쓰레기통', '비워줘'],
}</code></pre>
<p><strong>button_led_node 핀맵 (방 입구 OpenCR1)</strong></p>
<table>
<thead>
<tr>
<th>부품</th>
<th>핀</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td>버튼</td>
<td>D7</td>
<td>INPUT_PULLUP</td>
</tr>
<tr>
<td>RGB R</td>
<td>D4</td>
<td></td>
</tr>
<tr>
<td>RGB G</td>
<td>D2</td>
<td></td>
</tr>
<tr>
<td>RGB B</td>
<td>D3</td>
<td>220Ω 저항</td>
</tr>
<tr>
<td>부저(+)</td>
<td>D5</td>
<td></td>
</tr>
<tr>
<td>LCD VCC</td>
<td>5V</td>
<td>I2C 0x27</td>
</tr>
<tr>
<td>LCD SDA</td>
<td>SDA</td>
<td></td>
</tr>
<tr>
<td>LCD SCL</td>
<td>SCL</td>
<td></td>
</tr>
</tbody></table>
<p><strong>RGB LED / LCD 상태</strong></p>
<table>
<thead>
<tr>
<th>data 값</th>
<th>RGB LED</th>
<th>LCD</th>
<th>부저</th>
</tr>
</thead>
<tbody><tr>
<td><code>idle</code></td>
<td>🟢 초록</td>
<td>Normal</td>
<td>-</td>
</tr>
<tr>
<td><code>dispatching</code></td>
<td>🔵 파랑</td>
<td>Calling...</td>
<td>1회</td>
</tr>
<tr>
<td><code>emergency</code></td>
<td>🔴 빨강</td>
<td>EMERGENCY!</td>
<td>3회</td>
</tr>
</tbody></table>
<hr />
<h3 id="팀원-d---gui--맵핑--qa-environment-director">팀원 D - GUI &amp; 맵핑 &amp; QA (Environment Director)</h3>
<p><strong>담당 노드</strong></p>
<table>
<thead>
<tr>
<th>노드</th>
<th>언어</th>
<th>실행 위치</th>
</tr>
</thead>
<tbody><tr>
<td><code>gui_node</code></td>
<td>C++ (Qt6)</td>
<td>관제 PC</td>
</tr>
</tbody></table>
<p><strong>통신 구조</strong></p>
<pre><code>[gui_node]

구독:
├── /amcl_pose              ← Robot1 실시간 위치
├── /robot2/amcl_pose       ← Robot2 실시간 위치
├── /battery_state          ← Robot1 배터리
├── /robot2/battery_state   ← Robot2 배터리
├── /hospital/emergency_call
├── /hospital/fall_suspected
├── /hospital/call/101(2)
├── /hospital/medicine_request
├── /hospital/trash_request
└── /hospital/facility_status

발행:
└── /hospital/patrol_waypoints → task_manager 순찰 경로 전달</code></pre><hr />
<h2 id="하드웨어-역할-요약">하드웨어 역할 요약</h2>
<table>
<thead>
<tr>
<th>장치</th>
<th>수량</th>
<th>실행 위치</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td><strong>터틀봇3 (RPi4 내장)</strong></td>
<td>2</td>
<td>터틀봇1/2</td>
<td>라이다, 모터, 카메라 영상 발행</td>
</tr>
<tr>
<td><strong>내장 OpenCR (터틀봇)</strong></td>
<td>2</td>
<td>터틀봇1/2</td>
<td>낙상 감지 시 부저 + 버튼으로 해제</td>
</tr>
<tr>
<td><strong>D435</strong></td>
<td>1</td>
<td>관제 PC (USB)</td>
<td>탑뷰 낙상 의심 + 쓰레기통 깊이 감지</td>
</tr>
<tr>
<td><strong>MAX98357A</strong></td>
<td>1</td>
<td>터틀봇1</td>
<td>음성 안내 재생</td>
</tr>
<tr>
<td><strong>USB 마이크</strong></td>
<td>1</td>
<td>터틀봇1</td>
<td>환자 음성 녹음</td>
</tr>
<tr>
<td><strong>OpenCR1 (방 입구)</strong></td>
<td>2</td>
<td>방1/2 입구</td>
<td>버튼 + RGB LED + 부저 + 16×2 LCD</td>
</tr>
<tr>
<td><strong>관제 PC (Ubuntu)</strong></td>
<td>1</td>
<td>PC</td>
<td>Nav2, AMCL, YOLO, Whisper, D435, Qt GUI</td>
</tr>
</tbody></table>
<hr />
<h2 id="개발-환경-버전">개발 환경 버전</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>관제 PC</th>
<th>터틀봇1 RPi4</th>
<th>터틀봇2 RPi4</th>
</tr>
</thead>
<tbody><tr>
<td>OS</td>
<td>Ubuntu 22.04.5 LTS</td>
<td>Ubuntu 22.04 (ARM64)</td>
<td>Ubuntu 22.04 (ARM64)</td>
</tr>
<tr>
<td>ROS2</td>
<td>Humble</td>
<td>Humble</td>
<td>Humble</td>
</tr>
<tr>
<td>ROS_DOMAIN_ID</td>
<td>5</td>
<td>5</td>
<td>7</td>
</tr>
<tr>
<td>Python</td>
<td>3.10.12</td>
<td>3.10</td>
<td>-</td>
</tr>
<tr>
<td>openai-whisper</td>
<td>20240930</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>torch</td>
<td>2.5.1+cu121 (GPU)</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>gTTS</td>
<td>2.5.4</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>micro-ROS</td>
<td>v2.0.8-humble</td>
<td>-</td>
<td>-</td>
</tr>
</tbody></table>
<hr />
<h2 id="실행-명령어">실행 명령어</h2>
<pre><code class="language-bash"># Domain Bridge 실행
ros2 run domain_bridge domain_bridge --config bridge_config.yaml

# micro-ROS agent (방 입구 OpenCR)
ROS_DOMAIN_ID=5 ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 -b 115200
ROS_DOMAIN_ID=5 ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM1 -b 115200

# 관제 PC 노드
ros2 run hospital_control hospital_task_manager
ros2 run hospital_voice whisper_node
ros2 run hospital_voice tts_node

# 터틀봇1 RPi4
ROS_DOMAIN_ID=5 ros2 run hospital_voice mic_node --ros-args -p robot_id:=1 -p card_id:=2
ROS_DOMAIN_ID=5 ros2 run hospital_voice tts_play_node --ros-args -p robot_id:=1</code></pre>
<hr />
<p><em>v6.3 | 토픽명 room1/room2 확정(숫자 시작 불가), 메시지 data 101/102 통일, task_manager 경유지 라우팅·우선순위·낙상탐색 회전 추가, waste_front 좌표 확정, Qt GUI 맵 배경·실시간 위치 개선</em></p>