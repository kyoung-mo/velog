<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/633e5b5c-cb72-4f30-a919-0a4b0818eb84/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/LiDAR%EC%99%80-%EC%B9%B4%EB%A9%94%EB%9D%BC-Qt-GUI%EC%97%90-%ED%86%B5%ED%95%A9-teleopbatamclnav2qt">LiDAR와 카메라 Qt GUI에 통합</a></p>
</blockquote>
<p>이번 글에서는 micro-ROS의 개념과 OpenCR 보드에서 ROS2와 통신하는 방법을 정리해보겠습니다.<br />환경 설정부터 시작해서 Publisher와 Subscriber 예제를 OpenCR에서 직접 실행해보는 것까지 다루겠습니다.</p>
<hr />
<h2 id="1-micro-ros란">1. micro-ROS란?</h2>
<p>지금까지 다뤄온 ROS2는 Ubuntu가 설치된 PC나 Raspberry Pi처럼 Linux 환경 위에서 동작하는 미들웨어입니다.<br />그런데 실제 로봇 시스템에는 STM32, OpenCR 같은 마이크로컨트롤러(MCU)가 포함되어 있는 경우가 많습니다.<br />이런 MCU는 OS 없이 동작하거나 RTOS(Real-Time OS) 위에서만 동작하기 때문에, 일반적인 ROS2 노드를 그대로 올릴 수 없습니다.</p>
<p><strong>micro-ROS</strong>는 이 문제를 해결하기 위해 등장한 프레임워크입니다.<br />MCU에서 ROS2 통신(토픽, 서비스, 액션)을 가능하게 해주며, <strong>micro-ROS Agent</strong>가 MCU와 ROS2 네트워크 사이를 중계해주는 역할을 합니다.</p>
<pre><code>[OpenCR (MCU)] ──시리얼(USB)──&gt; [micro-ROS Agent (Ubuntu)] ──DDS──&gt; [ROS2 네트워크]</code></pre><p>TurtleBot3에 탑재된 <strong>OpenCR</strong>은 STM32F7 기반 컨트롤러로, micro-ROS 실행 대상으로 적합합니다.<br />Arduino IDE를 통해 코드를 작성하고 업로드하는 방식으로 개발합니다.</p>
<hr />
<h2 id="2-opencr-보드-소개">2. OpenCR 보드 소개</h2>
<p>OpenCR(Open-source Control module for ROS)은 ROBOTIS에서 만든 STM32 기반 보드입니다.<br />TurtleBot3에 기본 탑재되어 있으며, Dynamixel 모터 제어, IMU, 각종 GPIO를 지원합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d236d2b4-f7c2-47f5-a4cd-07f8b7c23df3/image.png" /></p>
<p>공식 문서는 아래에서 확인할 수 있습니다.</p>
<blockquote>
<p><a href="https://emanual.robotis.com/docs/en/parts/controller/opencr10/">https://emanual.robotis.com/docs/en/parts/controller/opencr10/</a></p>
</blockquote>
<p>주요 특징은 다음과 같습니다.</p>
<ul>
<li>MCU: STM32F746ZGT6 (ARM Cortex-M7, 216MHz)</li>
<li>입력 전압: 12V</li>
<li>USB-C 포트를 통해 PC와 시리얼 통신 (micro-ROS Agent 연결)</li>
<li>Arduino IDE로 펌웨어 개발 가능</li>
<li>ROS2 환경에서는 <strong>ROSSERIAL</strong> 대신 <strong>micro-ROS</strong>가 표준</li>
</ul>
<blockquote>
<p>참고: ROSSERIAL은 ROS1용이므로 ROS2 환경에서는 사용하지 않습니다.</p>
</blockquote>
<hr />
<h2 id="3-arduino-ide-설치-및-opencr-보드-설정-linux">3. Arduino IDE 설치 및 OpenCR 보드 설정 (Linux)</h2>
<p>micro-ROS 코드를 OpenCR에 업로드하려면 Arduino IDE와 OpenCR 보드 패키지가 필요합니다.<br />Ubuntu 환경 기준으로 설치 과정을 정리하겠습니다.</p>
<p>공식 설치 가이드는 아래 링크를 참고합니다.</p>
<blockquote>
<p><a href="https://emanual.robotis.com/docs/en/parts/controller/opencr10/#arduino-ide">https://emanual.robotis.com/docs/en/parts/controller/opencr10/#arduino-ide</a></p>
</blockquote>
<h3 id="31-arduino-ide-다운로드">3.1 Arduino IDE 다운로드</h3>
<p>아래 링크에서 <strong>Linux Zip file (64-bit X86-64)</strong> 버전을 다운로드합니다.</p>
<blockquote>
<p><a href="https://www.arduino.cc/en/software/">https://www.arduino.cc/en/software/</a></p>
</blockquote>
<p>압축 해제 후, <code>~/.bashrc</code>에 PATH를 추가합니다.</p>
<pre><code class="language-bash">export PATH=/home/ubuntu/arduino-ide_2.3.8_Linux_64bit:$PATH</code></pre>
<pre><code class="language-bash">source ~/.bashrc</code></pre>
<h3 id="32-opencr-보드-패키지-설치">3.2 OpenCR 보드 패키지 설치</h3>
<p>Arduino IDE를 실행한 뒤, <strong>File → Preferences</strong>에서 Additional Boards Manager URLs에 아래 주소를 추가합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/716eb6b5-aea6-4fb5-855e-2c2a82f29c7c/image.png" /></p>
<pre><code>https://raw.githubusercontent.com/ROBOTIS-GIT/OpenCR/master/arduino/opencr_release/package_opencr_index.json</code></pre><p>이후 <strong>Tools → Board → Boards Manager</strong>에서 <code>OpenCR</code>을 검색해 <strong>1.5.3 버전</strong>을 설치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f43375d1-8f18-4224-b7d0-e4ba14d1c5e5/image.png" /></p>
<p>설치가 완료되면 <strong>Tools → Board</strong>에 <code>OpenCR</code>이 나타납니다.</p>
<h3 id="33-업로드-권한-설정">3.3 업로드 권한 설정</h3>
<p>처음 업로드 시 아래와 같이 Permission Denied 오류가 발생할 수 있습니다.</p>
<pre><code>Fail to open port 1 : /dev/ttyACM0
ser_open: unable to open port: Permission denied</code></pre><p>아래 명령어로 시리얼 포트 접근 권한을 부여합니다.</p>
<pre><code class="language-bash">sudo usermod -aG dialout $USER</code></pre>
<p>이후 로그아웃 후 재로그인하면 적용됩니다.</p>
<p>또한, 리눅스의 modemmanager 패키지가 OpenCR 연결 직후 AT 명령을 보내 간섭할 수 있으므로 제거합니다.</p>
<pre><code class="language-bash">sudo apt-get purge modemmanager</code></pre>
<p>그리고 64bit PC에서 OpenCR 라이브러리가 32bit로 빌드되어 있어 아래 패키지도 설치해줍니다.</p>
<pre><code class="language-bash">sudo apt-get install libncurses5-dev:i386</code></pre>
<h3 id="34-동작-확인-led-blink">3.4 동작 확인 (LED Blink)</h3>
<p><strong>Examples → OpenCR → Basics → b.Blink_LED.ino</strong> 예제를 열어 업로드합니다.<br />LED가 점멸하면 환경 설정이 정상적으로 완료된 것입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/966a761e-817a-4bdc-85b6-66778f14edc5/image.gif" /></p>
<blockquote>
<p>Arduino 13번 핀은 <code>LED_BUILTIN</code>에 해당합니다.</p>
</blockquote>
<hr />
<h2 id="4-micro-ros-설치-및-agent-실행">4. micro-ROS 설치 및 Agent 실행</h2>
<p>micro-ROS 통신은 <strong>OpenCR(클라이언트)</strong> 와 <strong>Ubuntu PC(Agent)</strong> 가 시리얼로 연결되어 동작합니다.<br />Agent를 Ubuntu에 설치하고 실행하는 과정을 정리합니다.</p>
<h3 id="41-micro-ros-워크스페이스-생성-및-빌드">4.1 micro-ROS 워크스페이스 생성 및 빌드</h3>
<pre><code class="language-bash">mkdir -p ~/microRos_ws/src
cd ~/microRos_ws</code></pre>
<p>micro-ROS setup 패키지를 받아 빌드합니다.</p>
<pre><code class="language-bash"># micro-ROS setup 패키지 설치
sudo apt install ros-humble-micro-ros-setup

source /opt/ros/humble/setup.bash

# Agent 워크스페이스 생성
ros2 run micro_ros_setup create_agent_ws.sh

# Agent 빌드
ros2 run micro_ros_setup build_agent.sh

colcon build
source install/local_setup.bash</code></pre>
<h3 id="42-micro-ros-agent-실행">4.2 micro-ROS Agent 실행</h3>
<p>OpenCR을 USB로 연결한 뒤, 아래 명령으로 Agent를 실행합니다.</p>
<pre><code class="language-bash">source /opt/ros/humble/setup.bash
source ~/microRos_ws/install/local_setup.bash

ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0</code></pre>
<p>OpenCR이 연결되지 않은 상태라면 아래처럼 대기 메시지가 반복됩니다.</p>
<pre><code>[info] | TermiosAgentLinux.cpp | Serial port not found. | device: /dev/ttyACM0, error 2, waiting for connection...</code></pre><p>OpenCR에 micro-ROS 펌웨어가 올라가 있고 USB가 연결되면 아래처럼 세션이 수립됩니다.</p>
<pre><code>[info] | running... | fd: 3
[info] | Root.cpp | create_client | client_key: 0x5D0B1AEB, session_id: 0x81
[info] | SessionManager.hpp | establish_session | session established
[info] | ProxyClient.cpp | create_participant | participant created
[info] | ProxyClient.cpp | create_topic | topic created
[info] | ProxyClient.cpp | create_publisher | publisher created</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bfcdcd6c-0499-46c5-a5bb-e7387cf12c42/image.png" /></p>
<hr />
<h2 id="5-publisher-구현--opencr-→-ubuntu">5. Publisher 구현 — OpenCR → Ubuntu</h2>
<p>OpenCR이 1초마다 정수를 증가시켜 토픽으로 퍼블리시하는 예제입니다.</p>
<h3 id="51-코드-micro-ros_publisherino">5.1 코드 (micro-ros_Publisher.ino)</h3>
<pre><code class="language-cpp">#include &lt;micro_ros_arduino.h&gt;
#include &lt;stdio.h&gt;
#include &lt;rcl/rcl.h&gt;
#include &lt;rcl/error_handling.h&gt;
#include &lt;rclc/rclc.h&gt;
#include &lt;rclc/executor.h&gt;
#include &lt;std_msgs/msg/int32.h&gt;

rcl_publisher_t publisher;
std_msgs__msg__Int32 msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

#define LED_PIN 13
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void error_loop() {
  while(1) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time) {
  RCLC_UNUSED(last_call_time);
  if (timer != NULL) {
    RCSOFTCHECK(rcl_publish(&amp;publisher, &amp;msg, NULL));
    msg.data++;
  }
}

void setup() {
  set_microros_transports();
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  delay(2000);

  allocator = rcl_get_default_allocator();

  // ROS_DOMAIN_ID=5 설정
  rcl_init_options_t init_options = rcl_get_zero_initialized_init_options();
  RCCHECK(rcl_init_options_init(&amp;init_options, allocator));
  RCCHECK(rcl_init_options_set_domain_id(&amp;init_options, 5));
  RCCHECK(rclc_support_init_with_options(&amp;support, 0, NULL, &amp;init_options, &amp;allocator));

  // 노드 생성
  RCCHECK(rclc_node_init_default(&amp;node, &quot;micro_ros_arduino_node&quot;, &quot;&quot;, &amp;support));

  // Publisher 생성
  RCCHECK(rclc_publisher_init_default(
    &amp;publisher,
    &amp;node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    &quot;micro_ros_arduino_node_publisher_kym&quot;));

  // 타이머 생성 (1000ms)
  const unsigned int timer_timeout = 1000;
  RCCHECK(rclc_timer_init_default(&amp;timer, &amp;support, RCL_MS_TO_NS(timer_timeout), timer_callback));

  // Executor 생성 및 타이머 등록
  RCCHECK(rclc_executor_init(&amp;executor, &amp;support.context, 1, &amp;allocator));
  RCCHECK(rclc_executor_add_timer(&amp;executor, &amp;timer));

  msg.data = 0;
}

void loop() {
  delay(100);
  RCSOFTCHECK(rclc_executor_spin_some(&amp;executor, RCL_MS_TO_NS(100)));
}</code></pre>
<h3 id="52-코드-설명">5.2 코드 설명</h3>
<p>일반 ROS2 C++ 노드와 구조는 유사하지만, micro-ROS에서는 몇 가지 다른 점이 있습니다.</p>
<ul>
<li><code>set_microros_transports()</code>: 시리얼 통신 초기화 (Agent와의 연결)</li>
<li><code>rcl_init_options_set_domain_id(&amp;init_options, 5)</code>: ROS_DOMAIN_ID를 5로 설정 (ubuntu05와 맞춤)</li>
<li><code>rclc_support_init_with_options</code>: 도메인 ID 옵션을 포함해 support 초기화</li>
<li><code>RCCHECK</code> / <code>RCSOFTCHECK</code>: 오류 처리 매크로. <code>RCCHECK</code>는 실패 시 <code>error_loop()</code>로 진입하고, <code>RCSOFTCHECK</code>는 오류를 무시합니다.</li>
<li><code>loop()</code>에서 <code>rclc_executor_spin_some()</code>을 100ms마다 호출해 콜백을 처리합니다.</li>
</ul>
<h3 id="53-실행-결과-확인">5.3 실행 결과 확인</h3>
<p>코드를 업로드하고 Agent를 실행한 뒤, 다른 터미널에서 토픽을 확인합니다.</p>
<pre><code class="language-bash">ros2 topic list</code></pre>
<pre><code>/micro_ros_arduino_node_publisher_kym
/parameter_events
/rosout</code></pre><pre><code class="language-bash">ros2 topic echo /micro_ros_arduino_node_publisher_kym</code></pre>
<pre><code>data: 0
---
data: 1
---
data: 2
---</code></pre><p>1초마다 값이 증가하는 것을 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d37b97c7-32a1-4ec5-b3f9-5837ee22e926/image.png" /></p>
<hr />
<h2 id="6-subscriber-구현--ubuntu-→-opencr">6. Subscriber 구현 — Ubuntu → OpenCR</h2>
<p>Ubuntu에서 퍼블리시한 <code>Int32</code> 값을 OpenCR이 구독해, 값에 따라 LED를 제어하는 예제입니다.<br /><code>data == 0</code>이면 LED OFF, 그 외에는 LED ON으로 동작합니다.</p>
<h3 id="61-코드-micro-ros_subscriberino">6.1 코드 (micro-ros_Subscriber.ino)</h3>
<pre><code class="language-cpp">#include &lt;micro_ros_arduino.h&gt;
#include &lt;stdio.h&gt;
#include &lt;rcl/rcl.h&gt;
#include &lt;rcl/error_handling.h&gt;
#include &lt;rclc/rclc.h&gt;
#include &lt;rclc/executor.h&gt;
#include &lt;std_msgs/msg/int32.h&gt;

rcl_subscription_t subscriber;
std_msgs__msg__Int32 msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

#define LED_PIN 13
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void error_loop() {
  while(1) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void subscription_callback(const void * msgin) {
  const std_msgs__msg__Int32 * msg = (const std_msgs__msg__Int32 *)msgin;
  digitalWrite(LED_PIN, (msg-&gt;data == 0) ? LOW : HIGH);
}

void setup() {
  set_microros_transports();
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  delay(2000);

  allocator = rcl_get_default_allocator();

  rcl_init_options_t init_options = rcl_get_zero_initialized_init_options();
  RCCHECK(rcl_init_options_init(&amp;init_options, allocator));
  RCCHECK(rcl_init_options_set_domain_id(&amp;init_options, 5));
  RCCHECK(rclc_support_init_with_options(&amp;support, 0, NULL, &amp;init_options, &amp;allocator));

  RCCHECK(rclc_node_init_default(&amp;node, &quot;micro_ros_arduino_node&quot;, &quot;&quot;, &amp;support));

  // Subscriber 생성
  RCCHECK(rclc_subscription_init_default(
    &amp;subscriber,
    &amp;node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    &quot;micro_ros_arduino_subscriber_kym&quot;));

  RCCHECK(rclc_executor_init(&amp;executor, &amp;support.context, 1, &amp;allocator));
  RCCHECK(rclc_executor_add_subscription(
    &amp;executor, &amp;subscriber, &amp;msg, &amp;subscription_callback, ON_NEW_DATA));
}

void loop() {
  delay(100);
  RCCHECK(rclc_executor_spin_some(&amp;executor, RCL_MS_TO_NS(100)));
}</code></pre>
<h3 id="62-ubuntu에서-퍼블리시-테스트">6.2 Ubuntu에서 퍼블리시 테스트</h3>
<pre><code class="language-bash"># LED ON
ros2 topic pub /micro_ros_arduino_subscriber_kym std_msgs/msg/Int32 &quot;{data: 1}&quot;

# LED OFF
ros2 topic pub /micro_ros_arduino_subscriber_kym std_msgs/msg/Int32 &quot;{data: 0}&quot;</code></pre>
<p>Ubuntu에서 퍼블리시한 값에 따라 OpenCR의 LED 13번이 켜지고 꺼지는 것을 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/49873813-a6be-4476-a275-4a002b3b32d5/image.png" /></p>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 micro-ROS의 개념과 OpenCR 환경 설정, Agent 설치, Publisher/Subscriber 구현까지 다뤄보았습니다.</p>
<p>핵심 내용을 정리하면 다음과 같습니다.</p>
<ul>
<li>micro-ROS는 MCU에서 ROS2 통신을 가능하게 해주는 프레임워크입니다.</li>
<li>OpenCR과 Ubuntu는 USB 시리얼로 연결되며, micro-ROS Agent가 중계 역할을 합니다.</li>
<li><code>ROS_DOMAIN_ID</code>는 코드 내에서 <code>rcl_init_options_set_domain_id()</code>로 설정합니다.</li>
<li>Publisher는 타이머 콜백에서 주기적으로 데이터를 퍼블리시합니다.</li>
<li>Subscriber는 구독 콜백에서 수신 데이터를 처리합니다.</li>
</ul>
<p>다음 글에서는 Service 통신을 이용해 Ubuntu에서 OpenCR의 LED를 제어하는 방법을 정리하겠습니다.</p>