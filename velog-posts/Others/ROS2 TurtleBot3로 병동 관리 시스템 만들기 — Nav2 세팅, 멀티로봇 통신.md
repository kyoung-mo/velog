<h3 id="intel-ai-sw-academy-9기-2차-팀-프로젝트-20260416--20260427">Intel AI SW Academy 9기 2차 팀 프로젝트 (2026.04.16 ~ 2026.04.27)</h3>
<blockquote>
<p>본 글은 시리즈 1편입니다.
1편: 시스템 설계와 자율주행 세팅</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/61e72a1e-571f-4e48-a5a0-abd0d53a189a/image.png" /></p>
<hr />
<h2 id="요약">요약</h2>
<blockquote>
<p>같은 도메인에서 두 로봇을 제어하는 건, 생각처럼 되지 않았습니다.</p>
</blockquote>
<hr />
<h2 id="1-주제를-정하기까지">1. 주제를 정하기까지</h2>
<p>Intel AI SW Academy 9기 2차 프로젝트는 수업시간에 배운 ROS2를 활용한 로봇 시스템을 구현하는 것이었습니다.</p>
<p>팀이 꾸려지고 나서 주제 선정에 앞서 어떤 문제를 해결할 것인가를 먼저 이야기했습니다. 여러 아이디어가 나왔고, 그 중에서 실제 현장에서 의미 있는 문제를 다루고 싶었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0fe0fa57-8b73-46a7-a391-e6828984fd7a/image.png" /></p>
<p>코로나 펜데믹 기간 얘기가 나오면서 자연스럽게 감염병 환경에서의 의료진과 환자 간 불필요한 접촉을 줄여보자에서 주제 큰 틀을 정했습니다.
그리고, 야간 인력 부족으로 인한 낙상 감지 지연, 환자 호출에 대한 즉각적인 대응 어려움. 이렇게 두 가지를 자율주행 로봇으로 해결하는 방향으로 주제가 구체화됐습니다.</p>
<blockquote>
<p>로봇이 자율 순찰하며 낙상을 감지하고, 환자가 버튼 호출 및 음성으로 필요한 사항을 전달할 수 있는 비대면 케어 인프라를 구축한다.</p>
</blockquote>
<hr />
<h2 id="2-팀-구성과-역할-분담">2. 팀 구성과 역할 분담</h2>
<table>
<thead>
<tr>
<th>역할</th>
<th>담당</th>
</tr>
</thead>
<tbody><tr>
<td>PM + 음성·micro-ROS</td>
<td>구영모</td>
</tr>
<tr>
<td>PL + 자율주행 · Task Manager</td>
<td>안해성</td>
</tr>
<tr>
<td>비전 · 센서</td>
<td>인수민</td>
</tr>
<tr>
<td>GUI · 맵핑 · QA</td>
<td>곽종현</td>
</tr>
</tbody></table>
<p>4인 팀, 개발 기간 1주일이었습니다. 저는 이번 프로젝트에서 PM을 맡았습니다. 1차 CATNIP 프로젝트와 달리 이번에는 별도의 PL이 있었습니다. 발표 준비와 전체 일정 조율은 PL이 담당했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3ea72043-4f3b-4a78-8488-28638b8a3baa/image.png" /></p>
<p>저는 PM으로서 전체 프로젝트의 기술 설계와 주제 구체화를 이끌었습니다. 초반에 팀원들과 아이디어를 논의하며 시스템 방향을 잡았고, 진행 상황을 노션에 지속적으로 문서화했습니다. GitHub는 팀원별 브랜치 규칙을 정하고 코드 관리를 담당했습니다. 개발이 시작된 이후에는 각 파트 진행 상황을 확인하면서 막히는 부분이 생기면 직접 붙어서 함께 해결하는 방식으로 운영했습니다.</p>
<blockquote>
<p>각자 담당 파트가 있는 상황에서 PM이 할 수 있는 건 방향을 잡아주는 것이라고 생각했습니다. 초반에 구조와 규칙을 잡아두면, 개발 중반 이후에 충돌을 줄이고 방향을 유지하는 데 계속 도움이 됐습니다.</p>
</blockquote>
<hr />
<h2 id="3-시스템-구조">3. 시스템 구조</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f7762ac3-c488-45b1-b992-a0a73372ced1/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/daa01831-cff4-4ad3-ae5c-41042bf1c829/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6388b53f-50ac-48db-b97f-ece97508bc01/image.png" /></p>
<h3 id="물리적-환경">물리적 환경</h3>
<p>세트장은 병실 2개(각 65cm × 65cm), 복도, 스테이션 2개, 쓰레기 구역으로 구성했습니다.</p>
<pre><code>[관제 PC - Ubuntu 22.04, DOMAIN_ID=5]
   ├── Intel RealSense D435 (탑뷰, 낙상 의심 + 쓰레기 감지)
   ├── OpenCR1 × 2 (방 입구 버튼/LED/부저/LCD)
   ├── Nav2 / AMCL
   ├── HospitalTaskManager (C++)
   ├── YOLO11n-pose
   ├── Whisper STT / TTS
   └── Qt6 GUI

[세트장]
복도 ── 방1 ── 방2
         |       |
      [버튼]  [버튼]  ← OpenCR1 micro-ROS
      [RGB]   [RGB]
      [LCD]   [LCD]
      [부저]  [부저]</code></pre><h3 id="터틀봇-구성">터틀봇 구성</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>Robot1</th>
<th>Robot2</th>
</tr>
</thead>
<tbody><tr>
<td>ROS_DOMAIN_ID</td>
<td>5</td>
<td>7</td>
</tr>
<tr>
<td>스피커/마이크</td>
<td>✅</td>
<td>❌</td>
</tr>
<tr>
<td>주요 역할</td>
<td>순찰 + 음성 인터랙션</td>
<td>순찰</td>
</tr>
</tbody></table>
<p>두 로봇 모두 낙상 감지와 자율 순찰을 담당하지만, 음성 인터랙션은 Robot1에서만 동작합니다. MAX98357A 스피커와 USB 마이크가 Robot1에만 연결되어 있기 때문입니다.</p>
<hr />
<h2 id="4-맵핑">4. 맵핑</h2>
<p>자율주행의 기반이 되는 맵은 Cartographer SLAM으로 구성했습니다. 맵 구성 및 맵핑은 제가 직접 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9627ed88-f54c-4349-b498-8632e7dbffef/image.png" /></p>
<p>터틀봇을 텔레오퍼레이션으로 세트장 전체를 천천히 이동시키며 지도를 완성했습니다. 라이다 데이터가 쌓이면서 병실, 복도, 스테이션 구역이 점차 지도에 채워지는 과정이었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/404130cb-b130-4a22-9edd-d5939d60d023/image.png" /></p>
<p>다 완성된 모습입니다. 하지만 초반에 병실 문앞의 벽을 설정해둔게 저희가 볼때는 터틀봇이 충분히 지나갈만하다고 생각했으나, Nav2에서 주행 테스트를 해본결과 벽이 터틀봇이 지나가기 힘들어보여서 완전히 넓혀주었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/50b4335e-3070-407c-8145-6150c4cf26bb/image.png" /></p>
<p>맵이 완성되면 <code>map_saver_cli</code>로 저장하고, 이후 Nav2에서 불러와 AMCL 기반 위치 추정을 수행합니다.</p>
<pre><code class="language-bash">ros2 run nav2_map_server map_saver_cli -f ~/map/hospital_map</code></pre>
<hr />
<h2 id="5-costmap-inflation-조정">5. Costmap Inflation 조정</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6f6dc839-0c9d-4095-bfbb-a0a108e4aa2d/image.png" /></p>
<p>맵핑을 마치고 Nav2를 실행하자 예상치 못한 문제가 있었습니다.</p>
<p>RViz에서 보면 벽 주변으로 연보라색 영역(inflation layer)이 두껍게 생성되어 있었습니다. 문제는 세트장 자체가 작다 보니 이 영역이 통로 대부분을 덮어버렸습니다. 로봇 입장에서는 충돌 위험 구역으로 판단했고, 들어가는건 잘 들어갔으나 이후에 나오지를 못했습니다.</p>
<blockquote>
<p>사람 눈에는 충분히 넓어 보이는 통로가, 터틀봇 입장에서는 들어갈 수 없는 공간으로 인식되고 있었습니다.</p>
</blockquote>
<p>원인은 Nav2의 <code>inflation_radius</code> 기본값이 세트장 스케일에 비해 너무 컸기 때문입니다.</p>
<p><code>nav2_params.yaml</code>에서 <code>local_costmap</code>과 <code>global_costmap</code> 두 곳 모두 값을 조정했습니다.</p>
<pre><code class="language-yaml">local_costmap:
  local_costmap:
    ros__parameters:
      inflation_layer:
        inflation_radius: 0.15    # 기본값에서 줄임
        cost_scaling_factor: 5.0

global_costmap:
  global_costmap:
    ros__parameters:
      inflation_layer:
        inflation_radius: 0.15
        cost_scaling_factor: 5.0</code></pre>
<p>값을 줄이면서 통로에 흰색 공간이 확보되는 것을 RViz에서 확인했습니다. 다만 너무 줄이면 터틀봇이 실제 벽에 근접해서 주행하게 되므로, 터틀봇3 반지름(약 0.105m)을 고려해 안전 마진을 유지했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8af6931d-4aeb-4321-95f3-347e7b74de10/image.png" /></p>
<p>방안에 안전구역을 확보할만큼 경계 영역을 줄였으나, 벽을 너무 늦게 인식하여 벽을 우회하지 못하는 문제가 있었습니다. 그래서 파라미터 값을 적절하게 조절해주었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/06844c9f-3d49-40f3-98bb-1adb16dcacd7/image.png" /></p>
<hr />
<h2 id="6-경유지waypoint-설정">6. 경유지(Waypoint) 설정</h2>
<p>Inflation 문제를 해결했지만 또 다른 문제가 남아 있었습니다.</p>
<p>출발지와 목적지를 직선으로 이었을 때 경로 중간에 벽이 있으면, Nav2가 그 벽을 우회하지 못하는 경우가 있었습니다. 세트장이 작아 복도 폭이 좁다 보니 장애물 회피 경로 자체가 만들어지지 않는 구간이 생겼습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/25a1ca9c-76b2-4d0f-a4c6-473237b36d25/image.png" /></p>
<p>해결 방법은 직접 경유지 좌표를 심어두는 것이었습니다. 복도 중간, 방 입구 앞과 같이 병목이 생기는 지점에 경유지를 설정하였습니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/998537c6-289b-40d5-9a09-66a849221e7e/image.png" /></p>
<p><code>ros2 topic echo /clicked_point</code> 명령어를 통해 해당 절대 좌표를 확인하였고, 로봇이 해당 지점을 순서대로 거쳐가도록 task_manager에서 경로를 구성했습니다.</p>
<pre><code class="language-cpp">// Robot1 경유지
robot_wp_maps_[&quot;robot_1&quot;][&quot;CORRIDOR_MID&quot;] = {2.420,  0.510};
robot_wp_maps_[&quot;robot_1&quot;][&quot;CORRIDOR_L&quot;]   = {0.428,  0.467};
robot_wp_maps_[&quot;robot_1&quot;][&quot;waste_front&quot;]  = {4.827, -0.662};

// Robot2는 y축 기준 접근 방향이 달라 별도 좌표
robot_wp_maps_[&quot;robot_2&quot;][&quot;CORRIDOR_MID&quot;] = {2.420,  0.670};
robot_wp_maps_[&quot;robot_2&quot;][&quot;waste_front&quot;]  = {3.585,  0.531};</code></pre>
<p>두 로봇이 같은 방에 접근할 때 y축 기준 경로가 달라, 로봇별로 경유지 좌표를 분리해서 관리했습니다.</p>
<blockquote>
<p>좌표는 RViz의 <code>Publish Point</code> 기능으로 실측해서 하나씩 확정했습니다. 소수점 좌표를 수작업으로 맞추는 과정이 생각보다 시간이 걸렸습니다.</p>
</blockquote>
<hr />
<h2 id="7-domain-bridge--멀티로봇-통신">7. Domain Bridge — 멀티로봇 통신</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/30cb64c0-0a26-427a-b426-e157bea7a765/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f8178dca-d726-42c5-be76-702331fa12c5/image.png" /></p>
<p>두 로봇을 하나의 시스템에서 제어하려 할 때 예상치 못한 문제에 부딪혔습니다.</p>
<p>처음에는 두 로봇을 같은 <code>ROS_DOMAIN_ID=5</code>로 설정하고 네임스페이스로 구분하려 했습니다. 그런데 Nav2 스택 구조 특성상 같은 도메인에서 두 로봇을 독립적으로 제어하는 것이 생각만큼 깔끔하게 되지 않았습니다. 어느 명령이 어느 로봇에게 가는지 충돌이 생기는 상황이었습니다.</p>
<p>여러 방법을 찾아본 끝에 <code>domain_bridge</code> 패키지를 적용했습니다. Robot2를 <code>DOMAIN_ID=7</code>로 분리하고, 관제 PC(DOMAIN_ID=5)와 브릿지로 연결하는 구조입니다.</p>
<pre><code class="language-yaml"># bridge_config.yaml
name: turtlebot_test_bridge
from_domain: 7   # Robot2
to_domain: 5     # 관제 PC

topics:
  amcl_pose:
    type: geometry_msgs/msg/PoseWithCovarianceStamped
    remap: /robot2/amcl_pose
  robot2/goal_pose:
    type: geometry_msgs/msg/PoseStamped
    reversed: True
    remap: goal_pose</code></pre>
<p>브릿지 환경에서 한 가지 더 제약이 있었습니다. Nav2 Action(<code>/navigate_to_pose</code>)이 Domain Bridge를 통해서는 정상 동작하지 않았습니다. 결국 <code>/goal_pose</code> 토픽을 직접 발행하는 방식으로 우회했고, 도착 판정은 AMCL pose 기반으로 거리 35cm 이내 + 쿨다운 1.5초 조건으로 구현했습니다.</p>
<pre><code>관제 PC (domain5) ←→ [Domain Bridge] ←→ Robot2 (domain7)

robot2 → /amcl_pose         →  관제PC /robot2/amcl_pose
관제PC → /robot2/goal_pose  →  robot2 /goal_pose</code></pre><hr />
<h2 id="8-통합-테스트의-어려움">8. 통합 테스트의 어려움</h2>
<p>시스템이 어느 정도 갖춰지고 나서 전체 통합 테스트를 시작했습니다.</p>
<p>맵이 교실 복도 쪽에 구성되어 있었고, 개발은 자리에서 진행하다 보니 테스트를 할 때마다 장소를 이동해야 했습니다. 그리고 테스트 한 번을 위해 켜야 할 것들이 생각보다 많았습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/132bf7ed-ea5f-4486-9bdd-01d947c32f30/image.png" /></p>
<pre><code>관제 PC        : Nav2, AMCL, task_manager, YOLO ×2, Whisper, TTS, GUI, domain_bridge
               + micro_ros_agent ×2 (OpenCR 방1/방2)
Robot1 RPi4   : turtlebot3_bringup, camera_node, mic_node, tts_play_node
Robot2 RPi4   : turtlebot3_bringup, camera_node
OpenCR ×2     : micro-ROS 펌웨어</code></pre><p>각 환경마다 켜야 할 프로그램이 다르고, 하나라도 빠지거나 순서가 틀리면 원하는 동작이 나오지 않았습니다. 전체 테스트를 한 사이클 돌리는 데 걸리는 시간이 짧지 않았고, 그만큼 하루에 할 수 있는 테스트 횟수가 제한됐습니다.</p>
<blockquote>
<p>개별 노드 단위에서는 잘 됐던 것들이, 전체를 붙이는 순간 다른 양상으로 문제가 나타났습니다. 통합은 마지막에 붙이는 단계가 아니라, 그 자체로 별도의 개발 단계였습니다.</p>
</blockquote>
<hr />
<h2 id="9-전체-동작-흐름-정리">9. 전체 동작 흐름 정리</h2>
<p>이번 편에서 다룬 내용을 기반으로 한 전체 동작 흐름입니다.</p>
<pre><code>두 로봇 스테이션 대기
    → 10초 타이머 → 배터리 높은 로봇 선택 → 순찰 시작
        CORRIDOR_L → 101 → CORRIDOR_MID → 102 → waste_front → waste → S1/S2
    → 이벤트 발생 시 순찰 중단 → 이벤트 처리 → 스테이션 복귀</code></pre><p>버튼 호출, 음성 인터랙션, 낙상 감지 흐름은 2편에서 이어서 다루겠습니다.</p>
<hr />
<p><strong>🔗 GitHub</strong></p>
<p>전체 구현 코드는 GitHub에 정리해두었습니다.</p>
<p><a href="https://github.com/kyoung-mo/hospital-robot-ROS2"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&amp;logo=github" /></a></p>
<hr />
<blockquote>
<p>다음 편: <a href="https://api.velog.io/rss/@mommers">micro-ROS + 음성 인터랙션 구현기</a></p>
</blockquote>