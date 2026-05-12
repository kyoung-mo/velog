<h3 id="intel-ai-sw-academy-9기-2차-팀-프로젝트-20260416--20260427">Intel AI SW Academy 9기 2차 팀 프로젝트 (2026.04.16 ~ 2026.04.27)</h3>
<blockquote>
<p>본 글은 시리즈 2편입니다.
1편: <a href="https://velog.io/@mommers/ROS2-PJ-1">ROS2 TurtleBot3로 병동 관리 시스템 만들기 — Nav2 세팅부터 멀티로봇 통신까지</a>
2편: ROS2 TurtleBot3로 병동 관리 시스템 만들기 — micro-ROS와 음성 인터랙션 구현</p>
</blockquote>
<hr />
<h2 id="요약">요약</h2>
<blockquote>
<p>환자가 버튼을 누르면 로봇이 와서, 환자가 말하면 상태에 따라서 로봇이 움직입니다.</p>
</blockquote>
<p>이번 편에서는 제가 직접 담당했던 <strong>방 입구 micro-ROS 노드</strong>와 <strong>음성 인터랙션 파이프라인</strong>을 다룹니다. 그리고 개발 중반 이후 task_manager 수정에 참여했던 내용도 함께 정리합니다.</p>
<hr />
<h2 id="1-담당-파트-구조">1. 담당 파트 구조</h2>
<p>제가 맡은 노드는 총 5개입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/63f71031-bd5c-42d7-9146-0f98ab7624e3/image.png" /></p>
<table>
<thead>
<tr>
<th>노드</th>
<th>언어</th>
<th>실행 위치</th>
</tr>
</thead>
<tbody><tr>
<td><code>button_led_node</code></td>
<td>Arduino C++</td>
<td>방 입구 OpenCR1 × 2</td>
</tr>
<tr>
<td><code>mic_node</code></td>
<td>C++</td>
<td>터틀봇1 RPi4</td>
</tr>
<tr>
<td><code>tts_play_node</code></td>
<td>C++</td>
<td>터틀봇1 RPi4</td>
</tr>
<tr>
<td><code>whisper_node</code></td>
<td>Python</td>
<td>관제 PC</td>
</tr>
<tr>
<td><code>tts_node</code></td>
<td>Python</td>
<td>관제 PC</td>
</tr>
</tbody></table>
<p>크게 두 가지 역할로 나뉩니다. 방 입구에서 환자와 물리적으로 상호작용하는 <strong>micro-ROS 노드</strong>, 그리고 로봇이 병실에 도착한 이후 음성으로 소통하는 <strong>음성 인터랙션 파이프라인</strong>입니다.</p>
<hr />
<h2 id="2-방-입구-micro-ros--button_led_node">2. 방 입구 micro-ROS — button_led_node</h2>
<blockquote>
<p>🔗 <a href="https://github.com/kyoung-mo/hospital-robot-ROS2/blob/main/turtlebot3/micro_ROS.ino">micro_ROS.ino</a></p>
</blockquote>
<p>병실 입구에는 OpenCR1 보드가 설치되어 있습니다. 환자가 누르는 버튼, 상태를 나타내는 RGB LED, 부저, 16×2 LCD가 모두 이 보드 하나에 연결되어 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c44f536b-691d-454b-8529-ebfe99f9695f/image.png" /></p>
<h3 id="핀맵">핀맵</h3>
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
<td>220Ω 저항</td>
</tr>
<tr>
<td>RGB G</td>
<td>D2</td>
<td>220Ω 저항</td>
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
<h3 id="상태-정의">상태 정의</h3>
<p>버튼 호출과 이벤트 상태에 따라 LED 색상, LCD 메시지, 부저 패턴이 달라집니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/17a19265-eccc-46de-8bd3-e952d12a5c00/image.png" /></p>
<table>
<thead>
<tr>
<th>상태</th>
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
<p>평상시에는 초록 LED가 켜져 있고, 환자가 버튼을 누르면 파랑으로 바뀌며 로봇 출동을 알립니다. 긴급 상황으로 판단되면 빨강으로 전환되고 부저가 3회 울립니다.</p>
<h3 id="micro-ros-통신-구조">micro-ROS 통신 구조</h3>
<p>OpenCR은 micro-ROS를 통해 관제 PC의 <code>micro_ros_agent</code>와 통신합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/770af240-3695-4ec1-8010-59c439519d11/image.png" /></p>
<pre><code>관제 PC
└── micro_ros_agent (USB 시리얼 /dev/ttyACM0, /dev/ttyACM1)
        ↕
    OpenCR1 (방1 입구) → 버튼 클릭 → /hospital/call/room1 발행
    OpenCR1 (방2 입구) → 버튼 클릭 → /hospital/call/room2 발행

관제 PC → /hospital/emergency_event/room1 → OpenCR1 (방1) LED/부저/LCD 제어
관제 PC → /hospital/emergency_event/room2 → OpenCR1 (방2) LED/부저/LCD 제어</code></pre><p>실행 명령어는 아래와 같습니다.</p>
<pre><code class="language-bash">ROS_DOMAIN_ID=5 ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 -b 115200
ROS_DOMAIN_ID=5 ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM1 -b 115200</code></pre>
<hr />
<h2 id="3-음성-인터랙션-파이프라인">3. 음성 인터랙션 파이프라인</h2>
<p>음성 인터랙션은 Robot1이 병실에 도착한 이후에만 동작합니다. 순찰 중에 Whisper가 계속 동작하면 불필요한 연산이 생기기 때문에, task_manager가 도착을 확인한 시점에 트리거를 발행하는 방식으로 설계했습니다.</p>
<h3 id="전체-흐름">전체 흐름</h3>
<pre><code>Robot1 병실 도착
    → task_manager: /hospital/tts_trigger 발행 (data: &quot;101&quot; or &quot;102&quot;)
    → tts_node: &quot;필요한 거 있으실까요?&quot; TTS 생성
    → /robot_1/tts_play 발행
    → tts_play_node (RPi4): MAX98357A 재생 (~2초)
    → tts_node: 3초 대기 후 /robot_1/mic_trigger 자동 발행
    → mic_node (RPi4): 트리거 수신 → 4초 녹음 → /robot_1/audio 발행
    → whisper_node (관제 PC): STT 변환 → 키워드 매칭 → 이벤트 발행</code></pre><p>마이크는 터틀봇1 RPi4에 연결되어 있고, 음성 데이터를 ROS2 토픽으로 관제 PC에 전달합니다. Whisper는 관제 PC에서 GPU를 활용해 STT를 수행합니다. RPi4에서 Whisper를 직접 돌리기엔 연산량이 부담스럽고, 관제 PC에 RTX 4060이 있어 GPU 추론이 가능했기 때문에 이 구조로 설계했습니다.</p>
<h3 id="mic_node-c-rpi4">mic_node (C++, RPi4)</h3>
<blockquote>
<p>🔗 <a href="https://github.com/kyoung-mo/hospital-robot-ROS2/blob/main/turtlebot3/mic_node.cpp">mic_node.cpp</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0e0c2b66-40b1-455b-b1d7-f069e9116156/image.png" /></p>
<p>mic_node는 <code>/robot_1/mic_trigger</code> 토픽을 수신하면 4초간 녹음을 시작하고, 완료된 오디오 데이터를 <code>/robot_1/audio</code> 토픽으로 발행합니다.</p>
<h3 id="tts_node--tts_play_node-python--c">tts_node + tts_play_node (Python / C++)</h3>
<blockquote>
<p>🔗 <a href="https://github.com/kyoung-mo/hospital-robot-ROS2/blob/main/src/hospital_voice/hospital_voice/tts_node.py">tts_node.py</a>
🔗 <a href="https://github.com/kyoung-mo/hospital-robot-ROS2/blob/main/turtlebot3/tts_play_node.cpp">tts_play_node.cpp</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e888179c-cd55-4628-8157-9feb6a0861e1/image.png" /></p>
<p>TTS는 gTTS로 음성 파일을 생성하고, 재생 명령을 <code>/robot_1/tts_play</code> 토픽으로 발행합니다. 터틀봇1 RPi4의 <code>tts_play_node</code>가 이를 수신해 MAX98357A 스피커로 출력합니다.</p>
<h3 id="whisper_node-키워드-매칭">whisper_node 키워드 매칭</h3>
<blockquote>
<p>🔗 <a href="https://github.com/kyoung-mo/hospital-robot-ROS2/blob/main/src/hospital_voice/hospital_voice/whisper_node.py">whisper_node.py</a></p>
</blockquote>
<p>Whisper STT 결과를 받아 키워드를 매칭하고, 해당 이벤트 토픽을 발행합니다.</p>
<pre><code class="language-python">KEYWORDS = {
    'medicine':  ['약', '약 주세요', '약주세요'],
    'emergency': ['간호사', '의사', '도와줘', '도와주세요', '살려줘'],
    'ok':        ['괜찮아', '괜찮아요', '됐어', '됐어요'],
    'trash':     ['쓰레기', '쓰레기통', '비워줘'],
}</code></pre>
<table>
<thead>
<tr>
<th>키워드</th>
<th>발행 토픽</th>
<th>이후 동작</th>
</tr>
</thead>
<tbody><tr>
<td>약</td>
<td><code>/hospital/medicine_request</code></td>
<td>phar 경유 → 방 복귀 → TTS → 스테이션</td>
</tr>
<tr>
<td>쓰레기</td>
<td><code>/hospital/trash_request</code></td>
<td>waste_front → waste → 스테이션</td>
</tr>
<tr>
<td>간호사/도와줘</td>
<td><code>/hospital/emergency_call</code></td>
<td>LED 빨강 / 부저 3회 / LCD EMERGENCY!</td>
</tr>
<tr>
<td>괜찮아/됐어</td>
<td>-</td>
<td>LED 초록 / 스테이션 복귀</td>
</tr>
</tbody></table>
<hr />
<h2 id="4-whisper-인식률-개선--tiny-→-small">4. Whisper 인식률 개선 — tiny → small</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7b0d9942-4385-4102-9588-c4f11f1a9035/image.png" /></p>
<p>노드 구현을 마치고 실제 음성을 발화하며 테스트를 진행했습니다. 그런데 처음 사용했던 Whisper tiny 모델의 인식률이 생각보다 많이 낮았습니다.</p>
<p>키워드별로 표본 테스트를 진행해서 수치로 정리했습니다.</p>
<h3 id="whisper-tiny-테스트-결과">Whisper tiny 테스트 결과</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/35d9f927-8378-49c7-bbf8-7492dbe49b6c/image.png" /></p>
<table>
<thead>
<tr>
<th>카테고리</th>
<th>테스트 수</th>
<th>인식 수</th>
<th>인식률</th>
<th>평균 STT 시간</th>
</tr>
</thead>
<tbody><tr>
<td>Medicine</td>
<td>11</td>
<td>2</td>
<td>18%</td>
<td>0.16초</td>
</tr>
<tr>
<td>Emergency</td>
<td>10</td>
<td>4</td>
<td>40%</td>
<td>0.20초</td>
</tr>
<tr>
<td>OK</td>
<td>8</td>
<td>2</td>
<td>25%</td>
<td>0.22초</td>
</tr>
<tr>
<td>Trash</td>
<td>13</td>
<td>6</td>
<td>46%</td>
<td>0.26초</td>
</tr>
<tr>
<td><strong>전체</strong></td>
<td><strong>42</strong></td>
<td><strong>14</strong></td>
<td><strong>33%</strong></td>
<td><strong>0.21초</strong></td>
</tr>
</tbody></table>
<p>전체 인식률 33%. Medicine 카테고리는 18%로 &quot;약 주세요&quot;라고 또렷하게 발화해도 &quot;야&quot;, &quot;숙orse&quot; 같은 결과가 나왔습니다.</p>
<blockquote>
<p>인식률 33%로는 실제 환자가 사용하는 시스템으로 의미가 없다고 판단했습니다. GPT API를 추가로 붙여 후처리하는 방법도 고려했지만, 모델 자체를 교체하는 것이 더 깔끔한 해결 방법이라고 생각했습니다.</p>
</blockquote>
<h3 id="whisper-small로-교체">Whisper small로 교체</h3>
<p>Whisper small 모델로 교체하고 동일한 방식으로 재테스트를 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0e36bbae-2c08-45f8-aab8-a229111f42d9/image.png" /></p>
<table>
<thead>
<tr>
<th>카테고리</th>
<th>테스트 수</th>
<th>인식 수</th>
<th>인식률</th>
<th>평균 STT 시간</th>
</tr>
</thead>
<tbody><tr>
<td>Medicine</td>
<td>10</td>
<td>7</td>
<td>70%</td>
<td>0.28초</td>
</tr>
<tr>
<td>Emergency</td>
<td>11</td>
<td>9</td>
<td>82%</td>
<td>0.42초</td>
</tr>
<tr>
<td>OK</td>
<td>8</td>
<td>8</td>
<td><strong>100%</strong></td>
<td>0.19초</td>
</tr>
<tr>
<td>Trash</td>
<td>9</td>
<td>9</td>
<td><strong>100%</strong></td>
<td>0.13초</td>
</tr>
<tr>
<td><strong>전체</strong></td>
<td><strong>38</strong></td>
<td><strong>33</strong></td>
<td><strong>87%</strong></td>
<td><strong>0.26초</strong></td>
</tr>
</tbody></table>
<p>전체 인식률 87%로, tiny 대비 <strong>54%p 향상</strong>됐습니다. STT 처리 시간은 평균 0.21초 → 0.26초로 소폭 증가했지만, 4초 녹음 후 처리하는 구조에서는 문제가 없는 수준이었습니다.</p>
<p>tiny에서 인식률이 낮았던 Medicine 카테고리도 18% → 70%로 크게 개선됐고, &quot;나 약 먹을 시간이야&quot;, &quot;약 좀 갖다줄래?&quot;처럼 키워드 리스트에 없는 자연스러운 발화도 인식하는 것을 확인했습니다.</p>
<p>최종적으로 <strong>Whisper small 모델을 채택</strong>했습니다.</p>
<hr />
<h2 id="5-약-요청-흐름">5. 약 요청 흐름</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3302998d-7dae-4307-8ee9-214e48356c01/image.png" /></p>
<p>음성으로 &quot;약 주세요&quot;를 인식하면 아래 흐름이 동작합니다.</p>
<pre><code>/hospital/medicine_request 수신
    → task_manager: 현재 Robot1 위치(r1_current_loc_) 기반 목적지 자동 설정
    → phar (간호사 스테이션) 출발
    → phar 도착 → 약 수령
    → CORRIDOR_MID 경유 → 환자 방으로 이동
    → 방 도착 → TTS &quot;약 도착했습니다&quot; 재생
    → 스테이션 복귀</code></pre><p>처음 설계에서는 whisper_node가 <code>/hospital/medicine_request</code>에 방 번호를 담아 발행하려 했습니다. 그런데 실제로는 &quot;medicine&quot; 문자열 그대로 발행되고 있었고, task_manager가 이를 목적지로 해석하려다 에러가 발생했습니다.</p>
<pre><code>❌ [R1] 알 수 없는 목적지: medicine</code></pre><p>Robot1은 이미 해당 방에 있는 상태이므로, 현재 위치(<code>r1_current_loc_</code>)를 기반으로 목적지를 자동 설정하는 방식으로 수정해 해결했습니다. 이 수정은 아래 섹션에서 다루는 task_manager 수정 작업의 일부였습니다.</p>
<hr />
<h2 id="6-task_manager-수정">6. task_manager 수정</h2>
<p>개발 중반 이후, task_manager를 담당하던 팀원이 개인파트 개발이 덜 끝난 상태여서, 저도 붙어서 <code>task_manager.cpp</code>를 수정했습니다.</p>
<h3 id="도착-감지-cascade-문제">도착 감지 cascade 문제</h3>
<p>통합 테스트 과정에서 Robot1이 목적지에 도착했을 때 Robot2의 도착 이벤트까지 연달아 트리거되는 cascade 문제가 발생했습니다.</p>
<p>원인은 포즈 구독 콜백에서 두 로봇의 도착 판정 로직이 명확하게 분리되지 않은 것이었습니다. <code>check_arrival</code> 함수에 <code>robot_id</code>를 파라미터로 추가해 각 로봇의 포즈 콜백에서 독립적으로 호출하는 구조로 수정했습니다.</p>
<pre><code class="language-cpp">// robot_id를 파라미터로 받아 독립적으로 판정
void HospitalTaskManager::check_arrival(const std::string&amp; robot_id,
                                         geometry_msgs::msg::Pose pose) { ... }

// R1/R2 포즈 콜백에서 각각 호출
r1_pose_sub_ = ... [this](...) {
    r1_pose_ = msg-&gt;pose.pose;
    if (fleet_[&quot;robot_1&quot;].is_busy) check_arrival(&quot;robot_1&quot;, r1_pose_);
};
r2_pose_sub_ = ... [this](...) {
    r2_pose_ = msg-&gt;pose.pose;
    if (fleet_[&quot;robot_2&quot;].is_busy) check_arrival(&quot;robot_2&quot;, r2_pose_);
};</code></pre>
<h3 id="도착-판정-기준-확정">도착 판정 기준 확정</h3>
<p>도착 임계값은 35cm로 설정했습니다. 좁은 세트장 특성상 너무 넓히면 방에 진입하기도 전에 도착으로 판정되는 경우가 있었고, 너무 좁히면 터틀봇이 목적지 바로 앞에서 멈추지 못하는 경우가 생겼습니다. 실측 테스트를 반복하면서 35cm로 확정했습니다.</p>
<h3 id="쿨다운-15초-추가">쿨다운 1.5초 추가</h3>
<p>도착 판정 직후 같은 목적지로의 연속 트리거를 방지하기 위해 1.5초 쿨다운을 추가했습니다. 이 값이 없으면 도착 판정이 한 번에 여러 번 발생해 이후 동작이 중복으로 실행되는 문제가 있었습니다.</p>
<blockquote>
<p>task_manager는 시스템 전체 흐름을 제어하는 핵심 노드입니다. 담당 팀원이 다른 부분을 수정하는 동안 저도 붙어서 수정을 진행했는데, 전체 구조를 이해하지 못했다면 쉽게 손댈 수 없었을 것 같습니다. 초반에 노션으로 전체 설계를 정리해뒀던 것이 이 시점에도 도움이 됐습니다.</p>
</blockquote>
<hr />
<h2 id="7-전체-음성-인터랙션-시나리오-요약">7. 전체 음성 인터랙션 시나리오 요약</h2>
<pre><code>환자가 버튼 1회 클릭
    → LCD: &quot;Calling...&quot; / RGB LED: 파랑 / 부저 1회
    → 로봇 출동
    → 병실 도착
    → TTS: &quot;필요한 거 있으실까요?&quot;
    → 4초 녹음
    → Whisper STT (small 모델) → 키워드 매칭
        ├── &quot;약 주세요&quot; → 약 배달
        ├── &quot;쓰레기&quot; → 쓰레기 수거
        ├── &quot;도와줘&quot; → 긴급 호출
        └── &quot;괜찮아&quot; → 스테이션 복귀</code></pre><hr />
<p><strong>🔗 GitHub</strong></p>
<p>전체 구현 코드는 GitHub에 정리해두었습니다.</p>
<p><a href="https://github.com/kyoung-mo/hospital-robot-ROS2"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&amp;logo=github" /></a></p>
<hr />
<p>다음편은 회고글로 프로젝트 정리를 마루리하겠습니다.</p>