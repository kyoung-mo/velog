<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f42619b4-c581-49fa-878c-ede040f39525/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/ROS2-TurtleBot3-Bringup-SLAM-%EC%8B%A4%EC%8A%B5">TurtleBot3 Bringup과 SLAM 매핑</a></p>
</blockquote>
<p>이번 글에서는 ROS2의 기본 개념을 익히기 위해 TurtleSim을 활용한 Topic 통신 실습을 정리해보겠습니다.</p>
<p>TurtleSim은 ROS 학습을 위한 간단한 시뮬레이터로, 실제 로봇 없이도 Topic, Service, Action 등의 ROS2 통신 방식을 실습할 수 있습니다.</p>
<hr />
<h2 id="1-turtlesim-실행">1. TurtleSim 실행</h2>
<p>TurtleSim을 실행하려면 다음 명령어를 입력합니다.</p>
<pre><code class="language-bash">ros2 run turtlesim turtlesim_node</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4e026b3e-2ec3-4ab3-8506-b7f8b13089a5/image.png" /></p>
<p>파란 배경에 거북이가 하나 생성되는 것을 확인할 수 있습니다. 기본적으로 <code>turtle1</code>이라는 이름의 거북이가 중앙에 spawn됩니다.</p>
<h3 id="teleop으로-거북이-조종하기">teleop으로 거북이 조종하기</h3>
<p>새로운 터미널을 열어 teleop 노드를 실행합니다.</p>
<pre><code class="language-bash">ros2 run turtlesim turtle_teleop_key</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6745b4f2-ebbd-42bd-b834-1d1765ef6937/image.png" /></p>
<p>키보드 방향키를 사용해 거북이를 직접 움직일 수 있습니다. 거북이가 움직이면서 궤적이 그려지는 것을 확인할 수 있습니다.</p>
<hr />
<h2 id="2-ros2-node-개념">2. ROS2 Node 개념</h2>
<p>실행 파일 이름과 노드 이름은 다를 수 있습니다. 실행 중인 노드 목록을 확인하려면 다음 명령어를 사용합니다.</p>
<pre><code class="language-bash">ros2 node list</code></pre>
<p>TurtleSim과 teleop을 실행한 상태에서 확인하면 <code>/turtlesim</code>, <code>/teleop_turtle</code> 두 개의 노드가 실행 중인 것을 볼 수 있습니다.</p>
<h3 id="노드-정보-확인">노드 정보 확인</h3>
<p>특정 노드의 상세 정보를 보려면 <code>ros2 node info</code> 명령어를 사용합니다.</p>
<pre><code class="language-bash">ros2 node info /turtlesim</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7ddd63af-0f49-476f-a3a5-43f1b89fb7ae/image.png" /></p>
<p>이 명령어를 통해 해당 노드가 어떤 Topic을 Subscribe하고 Publish하는지, 어떤 Service와 Action을 제공하는지 확인할 수 있습니다.</p>
<p>마찬가지로 teleop 노드도 확인해봅니다.</p>
<pre><code class="language-bash">ros2 node info /teleop_turtle</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5e3452c2-edf6-40cb-bc2f-3e4e313e2527/image.png" /></p>
<p><code>/teleop_turtle</code> 노드는 <code>/turtle1/cmd_vel</code> 토픽으로 메시지를 발행하고, <code>/turtlesim</code> 노드는 이를 구독해서 거북이를 움직이는 구조입니다.</p>
<hr />
<h2 id="3-ros2-topic-개념">3. ROS2 Topic 개념</h2>
<h3 id="topic-통신의-특징">Topic 통신의 특징</h3>
<ul>
<li><strong>Publisher(발행자)</strong>와 <strong>Subscriber(구독자)</strong>로 구성됩니다.</li>
<li>Topic 이름이 동일해야 통신이 가능합니다.</li>
<li>메시지 타입도 일치해야 합니다.</li>
<li>1:1, 1:N, N:N 통신이 모두 가능합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9c91a9d1-0769-4ec5-a770-6f98d93d07b7/image.png" /></p>
<h3 id="topic-목록-확인">Topic 목록 확인</h3>
<p>현재 실행 중인 모든 Topic을 확인하려면:</p>
<pre><code class="language-bash">ros2 topic list</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2d354ecb-cbfe-4bc4-b51f-d779a0f1c92b/image.png" /></p>
<p><code>/turtle1/cmd_vel</code>, <code>/turtle1/pose</code>, <code>/turtle1/color_sensor</code> 등 TurtleSim 관련 Topic들이 보입니다.</p>
<hr />
<h2 id="4-topic-echo---실시간-데이터-확인">4. Topic Echo - 실시간 데이터 확인</h2>
<p>Topic으로 전송되는 메시지를 실시간으로 확인할 수 있습니다.</p>
<pre><code class="language-bash">ros2 topic echo /turtle1/cmd_vel</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a4db9447-9a82-4ec0-b23d-1333d359072f/image.png" /></p>
<p>teleop 창에서 방향키를 누르면 실시간으로 <code>linear</code>와 <code>angular</code> 값이 출력되는 것을 확인할 수 있습니다.</p>
<p>마찬가지로 거북이의 위치 정보도 확인할 수 있습니다.</p>
<pre><code class="language-bash">ros2 topic echo /turtle1/pose</code></pre>
<p>거북이가 움직일 때마다 <code>x</code>, <code>y</code>, <code>theta</code> 값이 실시간으로 업데이트됩니다.</p>
<hr />
<h2 id="5-topic-info---메시지-타입-확인">5. Topic Info - 메시지 타입 확인</h2>
<p>Topic의 메시지 타입을 확인하려면:</p>
<pre><code class="language-bash">ros2 topic info /turtle1/cmd_vel</code></pre>
<pre><code>Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 1</code></pre><p><code>geometry_msgs/msg/Twist</code> 타입이라는 것을 알 수 있습니다.</p>
<p>더 자세한 정보를 보려면 <code>--verbose</code> 옵션을 추가합니다.</p>
<pre><code class="language-bash">ros2 topic info /turtle1/cmd_vel --verbose</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/46dcd6bf-7413-44a0-baf0-b26310b284c1/image.png" /></p>
<p>QoS(Quality of Service) 설정, Publisher와 Subscriber의 노드 이름 등 상세한 정보를 확인할 수 있습니다.</p>
<hr />
<h2 id="6-interface-show---메시지-구조-확인">6. Interface Show - 메시지 구조 확인</h2>
<p><strong>메시지 타입을 알아야만 코드 작성이 가능합니다.</strong> 메시지 구조를 확인하려면:</p>
<pre><code class="language-bash">ros2 interface show geometry_msgs/msg/Twist</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9e47dc43-83e0-4b08-aac1-bd487f6b239b/image.png" /></p>
<pre><code>Vector3 linear
    float64 x
    float64 y
    float64 z
Vector3 angular
    float64 x
    float64 y
    float64 z</code></pre><p><code>Twist</code> 메시지는 <code>linear</code>(직진 속도)와 <code>angular</code>(회전 속도)로 구성되며, 각각 x, y, z 값을 가지는 것을 알 수 있습니다.</p>
<blockquote>
<p>참고: <code>float64</code>는 C/C++의 <code>double</code>형에 해당합니다.</p>
</blockquote>
<hr />
<h2 id="7-rqt---gui-도구-활용">7. rqt - GUI 도구 활용</h2>
<h3 id="rqt_graph---노드-간-통신-관계-시각화">rqt_graph - 노드 간 통신 관계 시각화</h3>
<pre><code class="language-bash">ros2 run rqt_graph rqt_graph</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1bc83a79-abf3-4ab4-89dd-0ca98eea5132/image.png" /></p>
<p><code>/teleop_turtle</code> 노드가 <code>/turtle1/cmd_vel</code> 토픽으로 메시지를 발행하고, <code>/turtlesim</code> 노드가 이를 구독하는 구조를 시각적으로 확인할 수 있습니다.</p>
<h3 id="rqt-topic-monitor---메시지-내용-확인">rqt Topic Monitor - 메시지 내용 확인</h3>
<p>GUI 기반 도구로 Topic 메시지를 확인할 수 있습니다.</p>
<pre><code class="language-bash">ros2 run rqt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2bca9313-c2d3-4307-b938-20f58bd80678/image.png" /></p>
<p>실행 후 <code>Plugins</code> → <code>Topics</code> → <code>Topic Monitor</code>를 선택합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/312387ef-55d4-46a0-ac57-4c989f3460fa/image.png" /></p>
<p>Topic을 체크하면 실시간으로 메시지 내용을 확인할 수 있으며, 트리 구조로 펼쳐볼 수 있어 메시지 구조를 파악하기 편리합니다.</p>
<p><strong>잘 모르겠으면 rqt에 들어가면 다 나옵니다.</strong> 메시지 타입, 구조, 실시간 값 모두 확인 가능합니다.</p>
<hr />
<h2 id="8-topic-pub---명령줄로-메시지-발행하기">8. Topic Pub - 명령줄로 메시지 발행하기</h2>
<p>직접 Topic으로 메시지를 발행할 수도 있습니다.</p>
<h3 id="원-그리기">원 그리기</h3>
<pre><code class="language-bash">ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist &quot;{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/693b6949-e36a-45e7-981e-e0a32e0f946b/image.png" /></p>
<p>이 명령어는 1Hz 주기로 계속 메시지를 발행합니다. 거북이가 원을 그리며 움직이는 것을 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6328dbb7-4af8-4c7f-af96-77473552b576/image.png" /></p>
<h3 id="한-번만-발행하기">한 번만 발행하기</h3>
<p>신호를 한 번만 주고 싶을 때는 <code>--once</code> 옵션을 사용합니다.</p>
<pre><code class="language-bash">ros2 topic pub --once -w 2 /turtle1/cmd_vel geometry_msgs/msg/Twist &quot;{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}&quot;</code></pre>
<p><code>-w 2</code> 옵션은 2초 동안 대기한 후 발행한다는 의미입니다.</p>
<hr />
<h2 id="9-터틀-2개-spawn하기">9. 터틀 2개 spawn하기</h2>
<p>TurtleSim에 거북이를 추가로 생성할 수 있습니다.</p>
<pre><code class="language-bash">ros2 service call /spawn turtlesim/srv/Spawn &quot;{x: 5.0, y: 8.0, theta: 3.14, name: 'turtle2'}&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/92ef898d-fda4-4a98-ba03-4e085314d9af/image.png" /></p>
<p><code>turtle2</code>라는 이름의 거북이가 지정한 좌표에 생성됩니다.</p>
<p>이제 <code>ros2 topic list</code>를 다시 확인하면 <code>/turtle2/cmd_vel</code>, <code>/turtle2/pose</code> 등 turtle2 관련 Topic들이 추가된 것을 볼 수 있습니다.</p>
<p>turtle2를 움직이려면:</p>
<pre><code class="language-bash">ros2 topic pub /turtle2/cmd_vel geometry_msgs/msg/Twist &quot;{linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}&quot;</code></pre>
<hr />
<h2 id="10-bashrc에-alias-등록하기">10. .bashrc에 alias 등록하기</h2>
<p>자주 사용하는 명령어를 짧게 만들어 편리하게 사용할 수 있습니다.</p>
<pre><code class="language-bash">vi ~/.bashrc</code></pre>
<p>파일 끝에 다음 내용을 추가합니다.</p>
<pre><code class="language-bash">alias rt='ros2 topic list'
alias re='ros2 topic echo'
alias rn='ros2 node list'</code></pre>
<p>저장 후 적용합니다.</p>
<pre><code class="language-bash">source ~/.bashrc</code></pre>
<p>이제 <code>rt</code>만 입력해도 <code>ros2 topic list</code>가 실행됩니다.</p>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 TurtleSim을 통해 ROS2의 Topic 통신 개념을 실습해보았습니다.</p>
<ul>
<li><strong>Node</strong>: 실행 단위</li>
<li><strong>Topic</strong>: Publisher와 Subscriber 간 비동기 통신</li>
<li><strong>메시지 타입</strong>: 통신 시 반드시 일치해야 함</li>
<li><strong>CLI 도구</strong>: <code>ros2 topic list/echo/info/pub</code>, <code>ros2 interface show</code></li>
<li><strong>GUI 도구</strong>: <code>rqt_graph</code>, <code>rqt Topic Monitor</code></li>
</ul>
<p>다음 글에서는 직접 C++ 코드로 Publisher와 Subscriber를 작성하는 방법을 정리하겠습니다.</p>