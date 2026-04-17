<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c9f3cbe4-2bc4-4dfe-a351-56547747b33d/image.gif" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/ros2-%EA%B0%9C%EB%B0%9C-%ED%99%98%EA%B2%BD-%EC%84%B8%ED%8C%85-raspberryPi4">ros2 개발 환경 세팅 (RPi4, Ubuntu)</a></p>
</blockquote>
<p>이번 글에서는 TurtleBot3 Bringup부터 SLAM을 이용한 매핑까지의 과정을 정리해보겠습니다.</p>
<blockquote>
<p>주로 참고한 사이트는 아래 두 링크입니다.
🔗 <a href="https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/">ROBOTIS e-Manual : TurtleBot3</a>
🔗 <a href="https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html">ROS 2 Documentation : Humble - Configuring environment</a></p>
</blockquote>
<hr />
<p>수업을 시작할때 오래걸리는 작업인 OpenCV 4.12 빌드를 먼저 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ab629864-7dce-4851-b652-0168d0bfe195/image.png" /></p>
<p>같은 네트워크에서 19명이 동시에 빌드를 진행하다 보니 속도가 굉장히 느렸고, 빌드 완료까지 상당한 시간이 소요되었습니다. </p>
<p>OpenCV 빌드를 돌려두고 수업을 진행했으나 저는 100%에서 오류가 나서 수업 끝나고 다시 돌렸습니다..</p>
<hr />
<h2 id="1-turtlebot3-bringup">1. TurtleBot3 Bringup</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/119e1d02-7f1b-4531-a061-7bb1901b8632/image.png" /></p>
<p>터틀봇을 직접 작동시키기 위해서는 먼저 SBC(라즈베리파이4)에서 Bringup을 실행해야 합니다.</p>
<p>Bringup은 터틀봇의 센서, 모터 등 하드웨어와 ROS2 노드를 연결해주는 역할을 합니다.</p>
<p>bring-up은 아래 명령어로 실행이 가능합니다.</p>
<blockquote>
<p><code>ros2 launch turtlebot3_bringup robot.launch.py</code></p>
</blockquote>
<p>bringup 실행 전에 <code>.bashrc</code>에 아래 환경 변수들을 작성해주고, 적용해주었습니다.</p>
<pre><code class="language-bash">vi ~/.bashrc
---------------
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=5  #TURTLEBOT3
export TURTLEBOT3_MODEL=burger
---------------

source ~/.bashrc // 바뀐 내용 적용</code></pre>
<p>환경 변수 설정이 확인되었으면 SBC에서 Bringup을 실행합니다.</p>
<pre><code class="language-bash"># [TurtleBot3 SBC]
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_bringup robot.launch.py</code></pre>
<hr />
<h2 id="2-topic--service-list-확인">2. Topic / Service List 확인</h2>
<p>Bringup이 정상적으로 실행되면 Remote PC에서 <code>topic</code>과 <code>service</code> 목록을 확인할 수 있습니다.</p>
<blockquote>
<p><code>ros2 topic list</code></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a8218964-445d-4896-a0ee-28ee90bb9b03/image.png" /></p>
<p><code>ros2 topic list</code> 결과로 <code>/battery_state</code>, <code>/cmd_vel</code>, <code>/imu</code>, <code>/odom</code>, <code>/scan</code> 등 터틀봇 관련 토픽들이 출력되는 것을 확인했습니다.</p>
<p>Bringup 전에는 <code>/parameter_events</code>, <code>/rosout</code> 두 개만 출력되었던 것과 비교하면, Bringup 이후 터틀봇 관련 토픽들이 정상적으로 등록된 것을 알 수 있었습니다.</p>
<blockquote>
<p><code>ros2 service list</code></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/69161cb1-2626-447a-a3b6-92ae9536534e/image.png" /></p>
<p><code>ros2 service list</code>에서는 <code>/diff_drive_controller</code>, <code>/ld08_driver</code>, <code>/motor_power</code>, <code>/reset_odometry</code> 등 터틀봇 하드웨어 제어 관련 서비스들을 확인했습니다.</p>
<hr />
<h2 id="3-teleop으로-직접-조종">3. Teleop으로 직접 조종</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4ae09439-6b03-4610-9486-571dfe30359f/image.png" /></p>
<p>토픽과 서비스 확인 후, 키보드로 터틀봇을 직접 조종해보았습니다.</p>
<pre><code class="language-bash"># [Remote PC]
export TURTLEBOT3_MODEL=burger
ros2 run turtlebot3_teleop teleop_keyboard</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/45fd8841-737f-4d15-9dea-505caa35626a/image.gif" /></p>
<p>실행하면 아래와 같은 조종 안내가 출력됩니다.</p>
<pre><code>Control Your TurtleBot3!
---------------------------
Moving around:
       w
  a    s    d
       x

w/x : increase/decrease linear velocity
a/d : increase/decrease angular velocity
space key, s : force stop

CTRL-C to quit</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/af7b97cd-2cb8-44f1-8f58-b4d525d48c05/image.png" /></p>
<p><code>w/x</code> 키로 전진·후진 속도를, <code>a/d</code> 키로 회전 속도를 조절하며 실제 터틀봇을 이동시켜보았습니다. <code>s</code>를 통해 정지할 수 있습니다.</p>
<hr />
<h2 id="4-slam-cartographer">4. SLAM (Cartographer)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7c7d93fd-8c2f-4d8e-b8aa-c3caba871729/image.png" /></p>
<p>Teleop으로 조종이 확인된 후, SLAM을 이용한 매핑을 진행했습니다.</p>
<p>사실 이번 교육과정에서 SLAM 공부 동아리에 들어갔다가 수학 관련된 식과, 개념들이 너무 어려워서.,. 굉장히 쫄아있었는데, 오늘 해보고 이렇게 쉽게 된다고? 라는 생각이 들었습니다. </p>
<p>터틀봇만 있어도 기존에 있는 프로그램들을 통해 환경 설정만 해주면 빠르게 가능하고, 터틀봇이 없다고 해도 gazebo라는 프로그램을 이용해서 가상환경에서 돌릴 수 있었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1f822901-f902-445a-9a10-f492327fcca4/image.png" /></p>
<p>혹시 궁금하신분은 아래 링크 참고하시면 좋을 것 같고, 간단하게 gazebo에서 SLAM을 진행한 과정도 <code>Chap 5</code>에 정리해두었습니다.</p>
<blockquote>
<p>🔗 <a href="https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation">ROBOTIZ : gazebo Simulation</a></p>
</blockquote>
<p>SLAM(Simultaneous Localization and Mapping)은 로봇이 미지의 환경을 탐색하면서 동시에 지도를 생성하는 기술입니다. 수업에서는 ROS2의 기본 SLAM 방식인 <strong>Cartographer</strong>를 사용했습니다.</p>
<pre><code class="language-bash"># [Remote PC]
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_cartographer cartographer.launch.py</code></pre>
<p>실행하면 RViz가 실행되면서 LiDAR 센서 데이터를 기반으로 지도가 실시간으로 그려지는 것을 확인할 수 있었습니다. 돌리고 초반부에 캡쳐한거라 아직 데이터 수집이 덜 되어있는 상태입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9ee1aa20-102e-42f2-9051-575814ecd2a2/image.png" /></p>
<p>제 교실을 한바퀴 돌리면서 전체적으로 데이터를 수집해보았습니다.</p>
<p>아직 운전이 익숙하지가 않았어서 회전을 많이하다보니 Map이 조금 어긋나있는 부분이 있었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cc80271e-932a-4848-890d-eb21ba971822/image.png" /></p>
<p>Teleop을 함께 실행하여 터틀봇을 직접 조종하며 공간 전체를 스캔했습니다. 매핑 시 급격한 속도 변화는 지도 품질에 영향을 주기 때문에 천천히 이동하며 구석구석 스캔하는 것이 좋습니다.</p>
<hr />
<h2 id="5-스크립트-등록-cartosh--navish">5. 스크립트 등록 (carto.sh / navi.sh)</h2>
<p>매번 긴 명령어를 입력하는 번거로움을 줄이기 위해 자주 사용하는 명령어를 쉘 스크립트로 만들어 <code>~/bin</code>에 등록해두었습니다. 우분투에는 <code>carto.sh</code>를 등록해놨고, 터틀봇에는 <code>bringup.sh</code> 를 등록해놨습니다.</p>
<p><strong>Ubuntu</strong></p>
<pre><code class="language-bash"># ~/bin/carto.sh
ros2 launch turtlebot3_cartographer cartographer.launch.py</code></pre>
<p><strong>turtlebot</strong></p>
<pre><code class="language-bash"># ~/bin/bringup.sh
ros2 launch turtlebot3_bringup robot.launch.py</code></pre>
<p><code>~/bin</code> 디렉토리는 PATH에 자동으로 포함되어 있어, 터미널 어디서든 <code>carto.sh</code>, <code>bringup.sh</code> 명령어만으로 바로 실행할 수 있습니다.</p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f93cd094-217d-48c6-ad7e-84abc8b0ad22/image.png" /></p>
<p>사람들 좀 집가니까 그나마 빨리 되더라구요.. 앞으로는 빌드할거 있으면 다른 사람들 시작하기 전에 미리 끝내야겠습니다.</p>
<p>이날은 빌드하고 다운로드 받을게 많았어서 진도를 많이 못 나갔습니다~!
<code>sudo apt update</code> 명령어 진행하는데 30분 걸리더라구요 ㅎㅎ</p>
<p>다음부터는 내용이 점점 많아져서 어떻게 쪼개야할지 모르겠지만.. 정리해보겠습니다.</p>