<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/166de269-bff2-45c2-82a2-64e4e803f681/image.gif" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/micro-ROS-OpenCR%EC%97%90%EC%84%9C-ROS2%EC%99%80-%ED%86%B5%EC%8B%A0">micro-ROS — OpenCR에서 ROS2와 통신하기</a></p>
</blockquote>
<p>이번 글에서는 micro-ROS의 Service 통신을 활용해 Ubuntu PC에서 OpenCR의 LED를 제어하는 방법을 정리해보겠습니다.<br />커스텀 인터페이스를 시도하는 과정에서 발생한 문제와 우회 방법, 그리고 최종 구현까지 다루겠습니다.</p>
<hr />
<h2 id="1-이번-글의-목표">1. 이번 글의 목표</h2>
<ul>
<li>OpenCR에 micro-ROS Service 서버를 구현합니다.</li>
<li>Ubuntu에서 Service 클라이언트를 실행해 LED를 켜고 끕니다.</li>
<li>커스텀 인터페이스 사용 시 발생하는 문제와 우회 방법을 이해합니다.</li>
</ul>
<p>최종 구성은 다음과 같습니다.</p>
<pre><code>[Ubuntu 클라이언트] ──서비스 요청(led_reg_kym)──&gt; [micro-ROS Agent] ──&gt; [OpenCR 서버]
                                                                          └── LED ON/OFF</code></pre><hr />
<h2 id="2-ros2-service-복습">2. ROS2 Service 복습</h2>
<p>Service는 토픽과 달리 <strong>요청-응답(call-response)</strong> 방식으로 동작합니다.<br />퍼블리시/서브스크라이브처럼 지속적으로 데이터를 주고받는 것이 아니라, 클라이언트가 요청을 보낼 때만 서버가 응답합니다.</p>
<pre><code>[클라이언트] ── Request ──&gt; [서버]
[클라이언트] &lt;── Response── [서버]</code></pre><p>서버는 하나만 존재하며, 한 번에 하나의 클라이언트와 1:1 통신합니다.</p>
<p>서비스 타입을 확인하는 명령어는 아래와 같습니다.</p>
<pre><code class="language-bash">ros2 service list -t
ros2 interface show example_interfaces/srv/AddTwoInts</code></pre>
<p><code>AddTwoInts</code> 타입의 구조는 다음과 같습니다.</p>
<pre><code>int64 a
int64 b
---
int64 sum</code></pre><p><code>---</code> 위쪽이 Request, 아래쪽이 Response에 해당합니다.</p>
<hr />
<h2 id="3-커스텀-인터페이스-시도--leddevicesrv">3. 커스텀 인터페이스 시도 — LedDevice.srv</h2>
<p>처음에는 LED 제어를 위한 커스텀 서비스 타입을 직접 만들려 했습니다.<br /><code>tutorial_interfaces</code> 패키지에 아래와 같이 <code>LedDevice.srv</code>를 정의했습니다.</p>
<pre><code>uint8 req
---
uint8 res</code></pre><p>Ubuntu 측에서는 <code>colcon build</code>로 정상적으로 빌드되었습니다.</p>
<h3 id="31-문제-발생--micro_ros_arduino-링크-오류">3.1 문제 발생 — micro_ros_arduino 링크 오류</h3>
<p>OpenCR 코드에서 이 커스텀 타입을 사용하려면 생성된 헤더 파일을 Arduino 라이브러리 경로에 추가해야 합니다.<br />그러나 <code>micro_ros_arduino</code>는 <strong>precompiled 라이브러리</strong> 형태로 배포되어 있어, 새로운 커스텀 타입을 추가하면 <strong>rosidl_typesupport 링크 오류</strong>가 발생합니다.</p>
<pre><code>rosidl_typesupport 링크 오류 발생
→ 헤더 파일만 추가해서는 안 됨</code></pre><p>커스텀 타입을 완전히 지원하려면 micro_ros_arduino를 소스에서 직접 빌드해야 합니다.<br />이번 수업 범위에서는 이 방법 대신 기존에 제공되는 타입을 재활용하는 방식으로 우회했습니다.</p>
<blockquote>
<p>소스 빌드를 통한 커스텀 인터페이스 통합은 추후 과제로 남겨두었습니다.</p>
</blockquote>
<hr />
<h2 id="4-우회-방법--addtwoints-타입-재활용">4. 우회 방법 — AddTwoInts 타입 재활용</h2>
<p><code>micro_ros_arduino</code>에 이미 포함되어 있는 <code>example_interfaces/srv/AddTwoInts</code> 타입을 재활용해 LED 제어를 구현했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/be71dbe6-543b-4cd6-8956-ef68a0436676/image.png" /></p>
<p>필드 매핑은 다음과 같이 약속합니다.</p>
<table>
<thead>
<tr>
<th>필드</th>
<th>역할</th>
<th>값</th>
</tr>
</thead>
<tbody><tr>
<td><code>req.a</code></td>
<td>LED 제어 신호</td>
<td>13 = LED ON, 0 = LED OFF</td>
</tr>
<tr>
<td><code>req.b</code></td>
<td>미사용</td>
<td>-</td>
</tr>
<tr>
<td><code>res.sum</code></td>
<td>응답 (고정값)</td>
<td>항상 0 반환</td>
</tr>
</tbody></table>
<p>서비스 이름은 <code>led_reg_kym</code>으로 통일합니다.</p>
<hr />
<h2 id="5-opencr-service-서버-구현">5. OpenCR Service 서버 구현</h2>
<h3 id="51-기본-구조--addtwointsino">5.1 기본 구조 — addtwoints.ino</h3>
<p>먼저 두 정수를 받아 합산하는 기본 Service 서버 예제입니다.</p>
<pre><code class="language-cpp">#include &lt;micro_ros_arduino.h&gt;
#include &lt;example_interfaces/srv/add_two_ints.h&gt;
#include &lt;stdio.h&gt;
#include &lt;rcl/error_handling.h&gt;
#include &lt;rclc/rclc.h&gt;
#include &lt;rclc/executor.h&gt;
#include &lt;std_msgs/msg/int64.h&gt;

rcl_node_t node;
rclc_support_t support;
rcl_allocator_t allocator;
rclc_executor_t executor;
rcl_service_t service;
rcl_wait_set_t wait_set;

example_interfaces__srv__AddTwoInts_Response res;
example_interfaces__srv__AddTwoInts_Request req;

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){while(1){};}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void service_callback(const void * req, void * res) {
  example_interfaces__srv__AddTwoInts_Request * req_in =
    (example_interfaces__srv__AddTwoInts_Request *) req;
  example_interfaces__srv__AddTwoInts_Response * res_in =
    (example_interfaces__srv__AddTwoInts_Response *) res;

  res_in-&gt;sum = req_in-&gt;a + req_in-&gt;b;
}

void setup() {
  set_microros_transports();
  delay(1000);

  allocator = rcl_get_default_allocator();
  RCCHECK(rclc_support_init(&amp;support, 0, NULL, &amp;allocator));

  RCCHECK(rclc_node_init_default(&amp;node, &quot;add_twoints_client_rclc&quot;, &quot;&quot;, &amp;support));

  RCCHECK(rclc_service_init_default(
    &amp;service, &amp;node,
    ROSIDL_GET_SRV_TYPE_SUPPORT(example_interfaces, srv, AddTwoInts),
    &quot;/addtwoints_kym&quot;));

  RCCHECK(rclc_executor_init(&amp;executor, &amp;support.context, 1, &amp;allocator));
  RCCHECK(rclc_executor_add_service(&amp;executor, &amp;service, &amp;req, &amp;res, service_callback));
}

void loop() {
  delay(100);
  RCSOFTCHECK(rclc_executor_spin_some(&amp;executor, RCL_MS_TO_NS(100)));
}</code></pre>
<h3 id="52-코드-설명">5.2 코드 설명</h3>
<p>Publisher/Subscriber와 비교했을 때 Service 서버의 차이점은 다음과 같습니다.</p>
<ul>
<li><code>rcl_service_t</code>: 서비스 핸들을 선언합니다.</li>
<li><code>rclc_service_init_default()</code>: 서비스 이름과 타입을 등록합니다.</li>
<li><code>rclc_executor_add_service()</code>: Executor에 서비스 콜백을 등록합니다.</li>
<li><code>service_callback()</code>: 요청(req)을 받아 응답(res)을 채워주는 함수입니다.</li>
</ul>
<p><code>loop()</code>에서는 Publisher/Subscriber와 동일하게 <code>rclc_executor_spin_some()</code>으로 수신 데이터를 확인합니다.</p>
<hr />
<h2 id="6-led-제어-최종-구현">6. LED 제어 최종 구현</h2>
<p>AddTwoInts 타입을 재활용해 LED를 제어하는 최종 코드입니다.</p>
<h3 id="61-opencr-서버-코드-led_regino">6.1 OpenCR 서버 코드 (LED_REG.ino)</h3>
<pre><code class="language-cpp">#include &lt;micro_ros_arduino.h&gt;
#include &lt;example_interfaces/srv/add_two_ints.h&gt;  // LedReg 대신 재활용
#include &lt;rcl/error_handling.h&gt;
#include &lt;rclc/rclc.h&gt;
#include &lt;rclc/executor.h&gt;

rcl_node_t node;
rclc_support_t support;
rcl_allocator_t allocator;
rclc_executor_t executor;
rcl_service_t service;
rcl_wait_set_t wait_set;

example_interfaces__srv__AddTwoInts_Response res;
example_interfaces__srv__AddTwoInts_Request req;

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){while(1){};}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void service_callback(const void * req, void * res) {
  example_interfaces__srv__AddTwoInts_Request * req_in =
    (example_interfaces__srv__AddTwoInts_Request *) req;
  example_interfaces__srv__AddTwoInts_Response * res_in =
    (example_interfaces__srv__AddTwoInts_Response *) res;

  if (req_in-&gt;a == 13) {
    digitalWrite(13, HIGH);   // LED ON
  } else if (req_in-&gt;a == 0) {
    digitalWrite(13, LOW);    // LED OFF
  }

  res_in-&gt;sum = 0;  // 항상 0 반환
}

void setup() {
  set_microros_transports();
  pinMode(13, OUTPUT);
  delay(1000);

  allocator = rcl_get_default_allocator();

  // ROS_DOMAIN_ID=5 설정
  rcl_init_options_t init_options = rcl_get_zero_initialized_init_options();
  RCCHECK(rcl_init_options_init(&amp;init_options, allocator));
  RCCHECK(rcl_init_options_set_domain_id(&amp;init_options, 5));
  RCCHECK(rclc_support_init_with_options(&amp;support, 0, NULL, &amp;init_options, &amp;allocator));

  RCCHECK(rclc_node_init_default(&amp;node, &quot;led_reg_server&quot;, &quot;&quot;, &amp;support));

  RCCHECK(rclc_service_init_default(
    &amp;service, &amp;node,
    ROSIDL_GET_SRV_TYPE_SUPPORT(example_interfaces, srv, AddTwoInts),
    &quot;led_reg_kym&quot;));

  RCCHECK(rclc_executor_init(&amp;executor, &amp;support.context, 1, &amp;allocator));
  RCCHECK(rclc_executor_add_service(&amp;executor, &amp;service, &amp;req, &amp;res, service_callback));
}

void loop() {
  delay(100);
  RCSOFTCHECK(rclc_executor_spin_some(&amp;executor, RCL_MS_TO_NS(100)));
}</code></pre>
<h3 id="62-ubuntu-클라이언트-실행">6.2 Ubuntu 클라이언트 실행</h3>
<p>Ubuntu 측에서는 기존에 작성한 <code>cpp_srvcli</code> 패키지의 클라이언트를 사용합니다.</p>
<pre><code class="language-bash"># micro-ROS Agent 실행 (터미널 1)
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0

# LED ON (터미널 2)
ros2 run cpp_srvcli led_reg_client 13

# LED OFF
ros2 run cpp_srvcli led_reg_client 0</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/55990947-d679-4e38-8980-7a794d55d557/image.png" /></p>
<hr />
<h2 id="7-트러블슈팅">7. 트러블슈팅</h2>
<h3 id="71-서비스-이름-불일치">7.1 서비스 이름 불일치</h3>
<p><strong>증상</strong>: 클라이언트가 요청을 보냈으나 서버에서 응답이 없음.</p>
<p><strong>원인</strong>: OpenCR 서버의 서비스 이름과 Ubuntu 클라이언트의 서비스 이름이 달랐습니다.</p>
<pre><code>OpenCR 서버:      /addtwoints_kym
Ubuntu 클라이언트: /add_two_ints  ← 기본값</code></pre><p><strong>해결</strong>: 서비스 이름을 <code>led_reg_kym</code>으로 양쪽에서 통일했습니다.</p>
<pre><code class="language-cpp">// OpenCR 서버 (LED_REG.ino)
RCCHECK(rclc_service_init_default(..., &quot;led_reg_kym&quot;));</code></pre>
<pre><code class="language-cpp">// Ubuntu 클라이언트
// 클라이언트 초기화 시 서비스 이름 동일하게 지정</code></pre>
<h3 id="72-커스텀-헤더-링크-오류">7.2 커스텀 헤더 링크 오류</h3>
<p><strong>증상</strong>: Ubuntu에서 <code>colcon build</code>로 생성한 커스텀 <code>.h</code> 파일을 Arduino 라이브러리 경로에 추가했으나, 업로드 시 링크 오류 발생.</p>
<p><strong>원인</strong>: <code>micro_ros_arduino</code>는 precompiled 라이브러리이기 때문에, 커스텀 타입에 대한 <code>rosidl_typesupport</code> 심볼이 포함되어 있지 않습니다. 헤더만 추가하는 것으로는 링크가 되지 않습니다.</p>
<p><strong>해결</strong>: <code>AddTwoInts</code> 타입을 재활용하는 방식으로 우회했습니다.<br />완전한 해결책은 <code>micro_ros_arduino</code>를 소스에서 빌드하는 것이나, 이는 별도 작업이 필요합니다.</p>
<h3 id="73-usb-연결-후-agent-세션-미수립">7.3 USB 연결 후 Agent 세션 미수립</h3>
<p><strong>증상</strong>: OpenCR을 USB로 연결했으나 Agent 로그에 &quot;waiting for connection...&quot; 메시지가 계속 출력됨.</p>
<p><strong>확인 사항</strong>:</p>
<ul>
<li>OpenCR에 micro-ROS 펌웨어가 정상적으로 업로드되었는지 확인합니다.</li>
<li><code>/dev/ttyACM0</code> 장치가 정상 인식되는지 확인합니다.</li>
</ul>
<pre><code class="language-bash">ls /dev/ttyACM*</code></pre>
<ul>
<li>modemmanager가 포트를 점유하고 있는 경우 제거합니다.</li>
</ul>
<pre><code class="language-bash">sudo apt-get purge modemmanager</code></pre>
<hr />
<h2 id="8-최종-구성-정리">8. 최종 구성 정리</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>OpenCR (서버)</th>
<th>Ubuntu (클라이언트)</th>
</tr>
</thead>
<tbody><tr>
<td>메시지 타입</td>
<td><code>AddTwoInts</code> 재활용</td>
<td><code>AddTwoInts</code> 재활용</td>
</tr>
<tr>
<td>서비스 이름</td>
<td><code>led_reg_kym</code></td>
<td><code>led_reg_kym</code></td>
</tr>
<tr>
<td>ROS_DOMAIN_ID</td>
<td>5</td>
<td>5</td>
</tr>
<tr>
<td><code>req.a</code> 의미</td>
<td>13=LED ON, 0=LED OFF</td>
<td>인자로 전달</td>
</tr>
<tr>
<td><code>res.sum</code> 의미</td>
<td>항상 0 반환</td>
<td>응답 출력</td>
</tr>
</tbody></table>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 micro-ROS Service 통신을 이용해 Ubuntu에서 OpenCR의 LED를 제어하는 방법을 다뤄보았습니다.</p>
<p>핵심 내용을 정리하면 다음과 같습니다.</p>
<ul>
<li>micro-ROS에서도 ROS2 Service와 동일한 요청-응답 구조를 사용합니다.</li>
<li><code>micro_ros_arduino</code>는 precompiled 라이브러리이므로 커스텀 타입 추가 시 소스 빌드가 필요합니다.</li>
<li>이번에는 기존 <code>AddTwoInts</code> 타입을 재활용하는 방식으로 우회해 LED 제어를 구현했습니다.</li>
<li>서비스 이름은 서버와 클라이언트 양쪽에서 반드시 동일하게 맞춰야 합니다.</li>
</ul>
<p>다음 글에서는 Dynamixel SDK를 이용한 모터 제어를 정리하겠습니다.</p>