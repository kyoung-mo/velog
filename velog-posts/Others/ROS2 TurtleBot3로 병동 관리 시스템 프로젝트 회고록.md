<h3 id="intel-ai-sw-academy-9기-2차-팀-프로젝트-20260416--20260427">Intel AI SW Academy 9기 2차 팀 프로젝트 (2026.04.16 ~ 2026.04.27)</h3>
<blockquote>
<p>본 글은 시리즈 3편입니다. (마지막)
1편: <a href="https://velog.io/@mommers/ROS2-PJ-1">ROS2 TurtleBot3로 병동 관리 시스템 만들기 — Nav2 세팅부터 멀티로봇 통신까지</a>
2편: <a href="https://velog.io/@mommers/ROS2-PJ-2">ROS2 TurtleBot3로 병동 관리 시스템 만들기 — micro-ROS와 음성 인터랙션 구현기</a>
3편: <a href="https://velog.io/@mommers/ROS2-PJ-3">ROS2 TurtleBot3로 병동 관리 시스템 프로젝트 회고록</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/610aa73c-45b6-4b60-8061-3c4b949630a8/image.png" /></p>
<hr />
<h2 id="요약">요약</h2>
<blockquote>
<p>원하지 않았던 주제였지만, 결국 그 안에서 할 수 있는 것들을 찾아갔습니다.</p>
</blockquote>
<hr />
<h2 id="1-원하지-않았던-주제">1. 원하지 않았던 주제</h2>
<p>솔직하게 말하면, 이번 프로젝트 주제는 원하던 방향이 아니었습니다. 저는 ROS보다 펌웨어 쪽 프로젝트를 하고 싶었습니다. 그래서 시간을 들여 따로 주제를 준비했습니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a4f8e9a3-6ae8-4412-8af9-1652cad3c030/image.png" /></p>
<p>터틀봇을 이용한 자동차 운전면허 시험장 프로젝트였습니다. teleop으로 터틀봇을 직접 조작하고, 팀원들끼리 경쟁하고 QT 대시보드에 결과를 띄워주는 구조였는데, 펌웨어 구현 비중을 최대한 높일 수 있는 방향으로 설계했습니다.</p>
<blockquote>
<p>하지만 교수님께서는 자율주행이 빠진다는 이유로 프로젝트 주제에 부합하지 않는다고 하셨습니다.</p>
</blockquote>
<p>주제가 막히고 나서, 팀에서는 AI로 아이디어를 검색하고 바로 병동 관리 시스템으로 방향을 잡았습니다. 준비한 주제가 막힌 것도 아쉬웠고, 충분히 고민을 거치지 않고 주제가 결정되는 느낌을 받아 처음에는 반대를 했습니다.</p>
<p>하지만 프로젝트를 주제 정하기까지 어느정도 시간이 남지도 않은 상황이였고, 저를 제외한 나머지 팀원들은 주제 괜찮다고 생각하여 고집을 버리고 프로젝트 주제에 대해 파악해보았습니다.</p>
<p>새로 정해진 주제에서 D435의 비중이 매우 높았습니다. D435를 통해 낙상 인지를 하고, 쓰레기통이 차있는지 비워져있는지를 판단에 따라 터틀봇이 움직이는것이였는데, 만약 D435가 잘 작동하지 않는다면 그 뒤에 작업은 진행될수가 없었습니다.</p>
<p>추가할만한 아이디어를 생각해봤고, 그 결과 micro-ROS로 방 입구 OpenCR을 제어하고, Whisper STT로 음성 인터랙션 파이프라인을 구성하는 과정이 프로젝트에 추가되었고, 터틀봇의 Picam에 Yolo 이용하여 사람을 감지하여 낙상 상태를 감지하는 등 주제를 구체화할 수 있었습니다.</p>
<hr />
<h2 id="2-pm-역할--이번엔-처음부터">2. PM 역할 — 이번엔 처음부터</h2>
<p>1차 CATNIP 프로젝트에서는 PM을 맡으면서도 초반에는 문서 작업에 집중하다가 개발 중반에 주행 ECU 쪽에 합류했습니다. 이때 처음부터 개발을 함께 진행하지 못한 아쉬움이 남아 있었습니다.</p>
<p>이번에는 PL이 따로 존재하기도 했고, PM이면서 처음부터 담당 파트를 맡아 개발과 문서 작업을 병행했습니다. <code>button_led_node</code>, <code>whisper_node</code>, <code>tts_node</code>, <code>mic_node</code>, <code>tts_play_node</code>까지 5개 노드를 처음부터 직접 구현했고, 노션 문서와 GitHub 관리도 함께 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7ef8cbe8-a7f4-40ed-93b6-5fa1738eb605/image.png" /></p>
<p>두 가지를 동시에 하는 게 쉽지 않을 거라 생각했는데, 오히려 전체 구조를 계속 문서로 정리하다 보니 다른 파트의 흐름도 자연스럽게 파악이 됐습니다. 제 파트가 먼저 마무리된 이후에는 <code>task_manager.cpp</code> 코드 수정과 Costmap 조정 작업 등 자율주행 파트에 붙어서 도와줄 수 있었던 것도 그 덕분이었습니다.</p>
<blockquote>
<p>이전 프로젝트에서 아쉬웠던 부분을 이번에 채운 느낌이었습니다.</p>
</blockquote>
<hr />
<h2 id="3-trouble-shooting">3. Trouble Shooting</h2>
<p><strong>멀티로봇 통신 구조를 찾기까지</strong></p>
<p>처음에는 두 로봇을 같은 <code>ROS_DOMAIN_ID</code>에서 네임스페이스로 구분해 제어하려 했습니다. 그런데 Nav2 스택 구조 특성상 같은 도메인에서 두 로봇이 충돌 없이 동작하게 만드는 것이 생각처럼 깔끔하지 않았습니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/40898b0c-d668-47f4-93a1-f2614aeb9fdf/image.png" /></p>
<p>여러 방법을 찾아본 끝에 <code>domain_bridge</code> 패키지를 적용해 Robot2를 별도 도메인으로 분리하는 방식으로 해결했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e6161279-2598-4b02-9783-7fbd6d7f8a2c/image.png" /></p>
<p><strong>YOLO 실시간 영상 딜레이</strong></p>
<p>통합 테스트 과정에서 YOLO 노드가 카메라 영상을 약 1fps 수준으로 수신하고 있었습니다. WiFi 환경에서 Raw 이미지를 그대로 전송하다 보니 데이터량이 너무 커서 제대로 전달되지 않았고, YOLO 추론 딜레이가 심각하게 발생했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/97ee0e51-4893-4f91-8ce6-537b68bacda2/image.png" /></p>
<p>CompressedImage 토픽으로 전환한 이후 수신 fps가 1fps에서 24fps로 대폭 증가했고, YOLO 딜레이도 함께 해소됐습니다.</p>
<table>
<thead>
<tr>
<th></th>
<th>Issue</th>
<th>Solution</th>
</tr>
</thead>
<tbody><tr>
<td>YOLO node</td>
<td>1fps</td>
<td>24fps</td>
</tr>
<tr>
<td>원인</td>
<td>Raw image 전송</td>
<td>CompressedImage 전환</td>
</tr>
</tbody></table>
<p><strong>Whisper STT 인식률 문제</strong></p>
<p>음성 인터랙션 파이프라인을 구성하고 나서 실제 발화 테스트를 진행했을 때, 처음 적용한 Whisper tiny 모델의 인식률이 생각보다 훨씬 낮았습니다. 카테고리별로 표본 테스트를 진행해 수치로 정리했고, 전체 인식률이 33%에 불과했습니다. Medicine 카테고리는 18%로 &quot;약 주세요&quot;라고 또렷하게 말해도 인식하지 못하는 경우가 대부분이었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cbf9124d-526b-4de2-b3b8-2434b6219d02/image.png" /></p>
<p>Whisper small 모델로 교체한 이후 전체 인식률이 87%로 올라갔습니다. tiny 대비 54%p 향상됐고, 평균 STT 처리 시간은 0.21초 → 0.26초로 소폭 증가에 그쳤습니다.</p>
<table>
<thead>
<tr>
<th></th>
<th>Whisper tiny</th>
<th>Whisper small</th>
</tr>
</thead>
<tbody><tr>
<td>전체 인식률</td>
<td>33%</td>
<td><strong>87%</strong></td>
</tr>
<tr>
<td>평균 STT 시간</td>
<td>0.21초</td>
<td>0.26초</td>
</tr>
</tbody></table>
<blockquote>
<p>모델 하나를 바꾸는 것만으로 인식률이 54%p 올라가는 걸 보면서, 무엇을 선택하느냐가 얼마나 큰 차이를 만드는지 실감했습니다.</p>
</blockquote>
<p><strong>좁은 맵과 자율주행의 타협</strong></p>
<p>세트장이 작다 보니 Nav2 기본 설정으로는 터틀봇이 방에 제대로 들어가지 못하는 문제가 있었습니다. 사람 눈에는 충분히 넓어 보이는 통로가, 터틀봇 입장에서는 Costmap inflation 때문에 진입하기 어려운 구역이 되어 있었습니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d88c86a2-831e-42d3-8caf-40dfd5fa7946/image.png" /></p>
<p><code>inflation_radius</code>를 줄여 통로를 확보했고, 직선 경로에 벽이 끼는 구간은 경유지 좌표를 하나씩 실측해서 심어뒀습니다.</p>
<p><strong>통합 테스트의 어려움</strong></p>
<p>맵이 교실 복도에 있어서 테스트를 할 때마다 장소를 이동해야 했습니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/df441aef-5cb8-40fd-8c68-4e522a5e676d/image.png" /></p>
<p>관제 PC, Robot1 RPi4, Robot2 RPi4, OpenCR 2개 — 각 환경마다 실행해야 할 노드가 달랐고, 하나라도 빠지면 원하는 동작이 나오지 않았습니다.</p>
<hr />
<h2 id="4-시나리오를-나누기로-한-결정">4. 시나리오를 나누기로 한 결정</h2>
<p>마감이 가까워지면서 전체 통합 테스트를 진행하는 과정에서 계속 문제가 발생했습니다. 관제 PC, Robot1 RPi4, Robot2 RPi4, OpenCR 2개 — 각 환경마다 실행해야 하는 노드의 개수가 18개나 되다보니 어떤 노드에서 문제가 발생하거나, 아니면 테스트를 진행할때 어떤 노드를 까먹고 실행했거나, 테스트를 반복하다보면 터틀봇의 배터리가 거의 다되서 충전해야하는 상황이 오거나..</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/286630f1-dc65-44cc-a565-55127a59b3cf/image.png" /></p>
<p>전체 시스템을 한 번에 붙여서 완벽하게 돌리는 것보다, 기능별로 검증된 시나리오를 나눠서 시연하는 것이 현실적인 판단이라고 생각했고, 두 가지 시나리오로 나눴습니다.</p>
<p><strong>시나리오 1 — 버튼 호출 + 음성 인터랙션 + 약 배달</strong></p>
<p>한 로봇이 순찰하는 동안 101호에서 버튼을 누르면, 로봇이 병실로 이동해 &quot;필요한 거 있으실까요?&quot;를 재생합니다. 환자가 약 관련 키워드를 말하면 간호사 스테이션으로 이동해 약을 수령하고, 환자 방으로 돌아와 전달한 뒤 스테이션으로 복귀합니다.</p>
<p><a href="https://www.youtube.com/watch?v=OJfixMXkzlU"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=flat-square&amp;logo=youtube&amp;logoColor=white" /></a></p>
<p><strong>시나리오 2 — D435 센서 기반 자동 감지</strong></p>
<p>D435 깊이 카메라를 중심으로 테스트를 진행합니다. 101호에서는 낙상 의심 토픽을 발행하면 로봇이 현장으로 파견돼 회전 탐색 후 스테이션으로 복귀합니다. 102호에서는 쓰레기 가득 참 토픽이 발행되면 로봇이 쓰레기를 수거해 쓰레기장으로 이동했다가 스테이션으로 복귀합니다.</p>
<p><a href="https://www.youtube.com/watch?v=NwL1haK7Blg"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=flat-square&amp;logo=youtube&amp;logoColor=white" /></a></p>
<blockquote>
<p>전체를 하나로 합치지 못한 건 아쉬웠지만, 두 시나리오 모두 완성도 있게 동작한다는 것을 증명하는 것이 그 시점에서 할 수 있는 최선이라고 판단했습니다.</p>
</blockquote>
<blockquote>
<p>깃허브에는 전체 통합 코드로 올려놨습니다.</p>
</blockquote>
<hr />
<h2 id="5-시나리오-12-성공">5. 시나리오 1,2 성공</h2>
<p>발표 전날 밤, 팀원들 모두 남아서 시나리오 1과 시나리오 2의 최종 시연 영상을 찍었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e57cdf47-6a48-4546-ae1e-0ef3dfb567ef/image.png" /></p>
<p>시나리오 1에서 로봇이 병실에 도착하고, 음성을 인식하고, 약을 수령해서 돌아오는 흐름이 끊기지 않고 한 번에 완료됐을 때, 그리고 시나리오 2에서 낙상 의심 신호를 받은 로봇이 현장으로 달려가 회전하고 복귀하는 것, 쓰레기 가득 참 신호에 다른 로봇이 수거하러 가는 것까지 한 번에 됐을 때 다들 오래 남아 고생한걸 알기 때문에 진짜 행복했습니다..</p>
<hr />
<h2 id="6-잘했다고-생각하는-것들">6. 잘했다고 생각하는 것들</h2>
<p><strong>원하지 않는 상황에서도 할 수 있는 것을 찾았다.</strong></p>
<p>처음에 원하지 않았던 주제였지만, 그 안에서 micro-ROS와 Whisper STT 파이프라인 등을 직접 제안하고 구현했습니다. 상황을 받아들이고 나서 나올 수 있는 최선을 찾아간 과정이었습니다.</p>
<p><strong>처음부터 구조를 잡았다.</strong></p>
<p>개발 시작 전에 전체 노드 구조, 토픽 흐름, 각 환경별 실행 노드를 문서로 정리했습니다. 설계가 바뀔 때마다 업데이트해 v6.4까지 버전이 올라갔고, 이 문서가 통합 단계에서 방향을 잡는 기준이 됐습니다.</p>
<p><strong>막히는 파트에 붙어서 같이 해결했다.</strong></p>
<p>제 파트를 마무리한 이후 Costmap 조정, 경유지 좌표 실측, task_manager 코드 수정까지 직접 참여했습니다. PM이 전체 흐름만 보고 있어서는 안 된다는 것을 CATNIP에서 배웠고, 이번에는 처음부터 개발과 병행하면서 더 자연스럽게 이어졌습니다.</p>
<p><strong>현실적인 판단을 했다.</strong></p>
<p>전체 통합이 어렵다고 판단한 시점에 시나리오를 분리하는 결정을 내렸습니다. 완성도를 높이는 방향 대신, 증명할 수 있는 것을 명확하게 보여줄 수 있는 방향을 선택했습니다. (사실 이것도 성공할 줄 몰랐다는 것..)</p>
<hr />
<h2 id="7-아쉬웠던-것들">7. 아쉬웠던 것들</h2>
<p><strong>처음부터 자율주행 환경에 대한 이해가 부족했다</strong></p>
<p>Costmap, Nav2 파라미터, Domain Bridge처럼 자율주행 환경에서 발생하는 문제들은 겪어보지 않으면 예측하기 어려운 것들이었습니다. 이 부분에 미리 시간을 쓸 수 있었다면 통합 테스트에 쓸 수 있는 시간이 더 늘어났을 것입니다.</p>
<p><strong>통합 코드가 아직 완성되지 않았다</strong></p>
<p>시나리오를 분리해서 시연에 성공했지만, 지금도 통합 코드에는 해결되지 않은 문제들이 남아 있습니다. 시연에서는 성공했지만 완전히 끝낸 것은 아니라는 것을 알고 있습니다.</p>
<p><strong>테스트 환경의 비효율</strong></p>
<p>launch 파일로 노드를 묶어두었다면 테스트 준비 시간을 상당히 줄일 수 있었을 것입니다. 매번 수동으로 실행하는 방식이 반복됐고, 그만큼 실제 테스트에 쓸 수 있는 시간이 줄었습니다.</p>
<hr />
<h2 id="8-배운-것들">8. 배운 것들</h2>
<p>원하지 않는 상황에서 어떻게 할 것인가에 대해 생각하게 된 프로젝트였습니다.</p>
<p>주제가 마음에 들지 않았을 때, 그 자리에서 고집을 부리는 것은 팀에도 저에게도 도움이 되지 않았습니다. 대신 결정된 방향 안에서 제가 하고 싶은 것을 직접 제안하고 추가하는 방식을 선택했고, 결과적으로 micro-ROS와 STT 파이프라인이 시스템의 핵심 기능이 됐습니다. 상황을 바꿀 수 없다면 그 안에서 의미를 찾는 것이 더 실용적이라는 것을 이번에 다시 확인했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f7168706-d827-41e3-97a1-3c76c6c6423a/image.png" /></p>
<p>CATNIP 이후 두 번째 팀 프로젝트였지만, 역할의 무게는 달랐습니다. 1차에서는 PM이면서 개발에 늦게 합류했는데, 이번에는 처음부터 개발을 담당하면서 문서까지 병행했습니다. 두 가지를 동시에 하는 것이 가능한지 확인하고 싶었고, 파트를 일찍 마무리한 덕에 다른 파트까지 기여할 수 있었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/558dafe9-0fb6-471a-9128-42318018a910/image.png" /></p>
<p>분산 시스템에서는 각 컴포넌트가 개별적으로 잘 동작하는 것과, 전체가 하나로 붙어서 잘 동작하는 것이 다른 문제라는 것을 이번에도 다시 체감했습니다. 통합 단계는 마지막에 붙이는 과정이 아니라, 그 자체로 별도의 개발 단계였습니다.</p>
<hr />
<blockquote>
<p>원하지 않는 방향이어도, 그 안에서 할 수 있는 것들을 찾아가면 결국 내 것이 됩니다.</p>
</blockquote>
<p><strong>읽어주셔서 감사합니다 😊</strong></p>
<hr />
<p><strong>🔗 GitHub</strong></p>
<p>전체 구현 코드는 GitHub에 정리해두었습니다.</p>
<p><a href="https://github.com/kyoung-mo/hospital-robot-ROS2"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&amp;logo=github" /></a></p>