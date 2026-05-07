<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/faec5d0b-1c5d-42b5-b480-e1908bf5adc4/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/ROS2-%EC%BB%A4%EC%8A%A4%ED%85%80-%ED%8C%A8%ED%82%A4%EC%A7%80-%EA%B0%9C%EB%B0%9C-Publisher-Subscriber-%EA%B5%AC%ED%98%84">ROS2 커스텀 패키지 개발 - Publisher &amp; Subscriber 구현</a></p>
</blockquote>
<p>이번 글에서는 실제 TurtleBot3의 배터리 상태를 실시간으로 모니터링하는 Subscriber 노드를 작성하는 과정을 정리하겠습니다. 현재 터틀봇을 프로젝트 끝나고 센터에 제출해둔상태라 필기했던 내용 기반으로 하다보니 캡쳐본이 많이 없습니다..</p>
<p>이전 글에서는 <code>geometry_msgs/msg/Twist</code> 타입을 사용했지만, 이번에는 <code>sensor_msgs/msg/BatteryState</code> 타입을 다루게 됩니다.</p>
<hr />
<h2 id="1-battery_state-토픽-확인">1. /battery_state 토픽 확인</h2>
<p>TurtleBot3을 Bringup하면 배터리 관련 토픽이 자동으로 생성됩니다.</p>
<h3 id="turtlebot3-bringup">TurtleBot3 Bringup</h3>
<p>라즈베리파이(SBC)에서:</p>
<pre><code class="language-bash">ros2 launch turtlebot3_bringup robot.launch.py</code></pre>
<h3 id="토픽-목록-확인">토픽 목록 확인</h3>
<p>Ubuntu PC에서:</p>
<pre><code class="language-bash">ros2 topic list</code></pre>
<p><code>/battery_state</code> 토픽이 보이는 것을 확인할 수 있습니다.</p>
<hr />
<h2 id="2-메시지-타입-분석">2. 메시지 타입 분석</h2>
<h3 id="토픽-정보-확인">토픽 정보 확인</h3>
<pre><code class="language-bash">ros2 topic info /battery_state</code></pre>
<pre><code>Type: sensor_msgs/msg/BatteryState
Publisher count: 1
Subscription count: 0</code></pre><p><code>sensor_msgs/msg/BatteryState</code> 타입인 것을 확인했습니다.</p>
<h3 id="메시지-구조-확인">메시지 구조 확인</h3>
<pre><code class="language-bash">ros2 interface show sensor_msgs/msg/BatteryState</code></pre>
<p>메시지 구조가 복잡하지만, 우리가 사용할 필드는:</p>
<ul>
<li><code>voltage</code> (float32): 배터리 전압</li>
<li><code>percentage</code> (float32): 배터리 잔량 퍼센트</li>
</ul>
<h3 id="실시간-데이터-확인">실시간 데이터 확인</h3>
<pre><code class="language-bash">ros2 topic echo /battery_state</code></pre>
<p>실제로 배터리 값이 실시간으로 출력되는 것을 확인할 수 있습니다.</p>
<hr />
<h2 id="3-rqt로-메시지-확인">3. rqt로 메시지 확인</h2>
<p>GUI 도구로도 확인해봅니다.</p>
<pre><code class="language-bash">ros2 run rqt</code></pre>
<p><code>Plugins</code> → <code>Topics</code> → <code>Topic Monitor</code>를 선택한 후 <code>/battery_state</code>를 체크합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/41b450d8-df62-4866-963c-2cfb4feaebe3/image.png" /></p>
<p>트리 구조로 펼쳐보면 <code>voltage</code>와 <code>percentage</code> 필드를 쉽게 찾을 수 있습니다.</p>
<p><strong>rqt에 들어가면 모든 Topic을 확인 가능합니다.</strong></p>
<hr />
<h2 id="4-kym_battery_subcpp-작성">4. kym_battery_sub.cpp 작성</h2>
<p>이제 배터리 상태를 구독하는 노드를 작성합니다.</p>
<pre><code class="language-bash">cd ~/robot_ws/src/kccistc_ros2_pkg/src
vi kym_battery_sub.cpp</code></pre>
<h3 id="전체-코드">전체 코드</h3>
<pre><code class="language-cpp">#include &lt;chrono&gt;
#include &lt;functional&gt;
#include &lt;memory&gt;
#include &lt;string&gt;

#include &quot;rclcpp/rclcpp.hpp&quot;
#include &quot;sensor_msgs/msg/battery_state.hpp&quot;

using std::placeholders::_1;

class BatterySub : public rclcpp::Node
{
public:
  BatterySub()
  : Node(&quot;battery_sub&quot;)
  {
    auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(10));
    subscriber_battery = this-&gt;create_subscription&lt;sensor_msgs::msg::BatteryState&gt;(
      &quot;battery_state&quot;,
      qos_profile,
      std::bind(&amp;BatterySub::subscribe_topic_message, this, _1));
  }

private:
  void subscribe_topic_message(const sensor_msgs::msg::BatteryState::SharedPtr msg) const
  {
    RCLCPP_INFO(this-&gt;get_logger(), &quot;Received Battery: '%.2f', Voltage %.2f&quot;, 
                msg-&gt;percentage, msg-&gt;voltage);
  }

  rclcpp::Subscription&lt;sensor_msgs::msg::BatteryState&gt;::SharedPtr subscriber_battery;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared&lt;BatterySub&gt;();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}</code></pre>
<h3 id="코드-설명">코드 설명</h3>
<ol>
<li><p><strong>헤더 파일</strong></p>
<ul>
<li><code>sensor_msgs/msg/battery_state.hpp</code>: BatteryState 메시지 타입</li>
</ul>
</li>
<li><p><strong>QoS 설정</strong></p>
<ul>
<li><code>rclcpp::QoS(rclcpp::KeepLast(10))</code>: 최근 10개 메시지 보관</li>
<li>TurtleBot3의 QoS 설정과 일치시켜야 통신이 원활합니다.</li>
</ul>
</li>
<li><p><strong>Subscriber 생성</strong></p>
<ul>
<li>토픽명: <code>battery_state</code></li>
<li>메시지 타입: <code>sensor_msgs::msg::BatteryState</code></li>
<li>콜백 함수: <code>subscribe_topic_message</code></li>
</ul>
</li>
<li><p><strong>콜백 함수</strong></p>
<ul>
<li><code>msg-&gt;percentage</code>: 배터리 잔량 (%)</li>
<li><code>msg-&gt;voltage</code>: 배터리 전압 (V)</li>
<li><code>RCLCPP_INFO</code>로 로그 출력</li>
</ul>
</li>
</ol>
<hr />
<h2 id="5-cmakeliststxt-수정">5. CMakeLists.txt 수정</h2>
<p>빌드 설정에 새로운 노드를 추가합니다.</p>
<pre><code class="language-bash">cd ~/robot_ws/src/kccistc_ros2_pkg
vi CMakeLists.txt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f200e5ca-e1d8-4563-bfb5-27ef9671ff16/image.png" /></p>
<h3 id="의존성-추가">의존성 추가</h3>
<pre><code class="language-cmake">find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)</code></pre>
<p><code>sensor_msgs</code> 패키지를 추가합니다.</p>
<h3 id="실행-파일-빌드">실행 파일 빌드</h3>
<pre><code class="language-cmake">add_executable(cmd_vel_pub src/cmd_vel_pub.cpp)
ament_target_dependencies(cmd_vel_pub rclcpp std_msgs geometry_msgs)

add_executable(cmd_vel_sub src/cmd_vel_sub.cpp)
ament_target_dependencies(cmd_vel_sub rclcpp std_msgs geometry_msgs)

add_executable(kym_battery_sub src/kym_battery_sub.cpp)
ament_target_dependencies(kym_battery_sub rclcpp std_msgs sensor_msgs)</code></pre>
<p><code>kym_battery_sub</code> 실행 파일을 추가하고, <code>sensor_msgs</code> 의존성을 명시합니다.</p>
<h3 id="설치-설정">설치 설정</h3>
<pre><code class="language-cmake">install(TARGETS
  cmd_vel_pub
  cmd_vel_sub
  kym_battery_sub
  DESTINATION lib/${PROJECT_NAME})</code></pre>
<hr />
<h2 id="6-빌드-및-실행">6. 빌드 및 실행</h2>
<h3 id="패키지-빌드">패키지 빌드</h3>
<pre><code class="language-bash">cd ~/robot_ws
colcon build --packages-select kccistc_ros2_pkg</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/55d21e2e-7786-4ac7-abbc-26e90e8e77b2/image.png" /></p>
<h3 id="환경-설정-적용">환경 설정 적용</h3>
<pre><code class="language-bash">source ~/robot_ws/install/local_setup.bash</code></pre>
<h3 id="노드-실행">노드 실행</h3>
<pre><code class="language-bash">ros2 run kccistc_ros2_pkg kym_battery_sub</code></pre>
<p>실시간으로 배터리 상태가 출력되는 것을 확인할 수 있습니다.</p>
<pre><code>[INFO] [battery_sub]: Received Battery: '95.23', Voltage 12.34
[INFO] [battery_sub]: Received Battery: '95.20', Voltage 12.33
[INFO] [battery_sub]: Received Battery: '95.18', Voltage 12.32</code></pre><hr />
<h2 id="7-다양한-메시지-타입-다루기">7. 다양한 메시지 타입 다루기</h2>
<h3 id="geometry_msgs-vs-sensor_msgs">geometry_msgs vs sensor_msgs</h3>
<p>이번 실습에서 사용한 메시지 타입들:</p>
<table>
<thead>
<tr>
<th>메시지 타입</th>
<th>패키지</th>
<th>용도</th>
</tr>
</thead>
<tbody><tr>
<td><code>Twist</code></td>
<td><code>geometry_msgs</code></td>
<td>속도 제어 (linear, angular)</td>
</tr>
<tr>
<td><code>BatteryState</code></td>
<td><code>sensor_msgs</code></td>
<td>배터리 상태 (voltage, percentage)</td>
</tr>
</tbody></table>
<h3 id="헤더-파일-경로">헤더 파일 경로</h3>
<p>ROS2 메시지 타입의 헤더 파일은 다음 경로에 있습니다.</p>
<pre><code class="language-bash">ls /opt/ros/humble/include/geometry_msgs/geometry_msgs/msg/
ls /opt/ros/humble/include/sensor_msgs/sensor_msgs/msg/</code></pre>
<p><img alt="" src="https://api.velog.io/rss/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_%ED%97%A4%EB%8D%94_%EA%B2%BD%EB%A1%9C.png" /></p>
<p>필요한 메시지 타입이 있다면 이 경로에서 <code>.hpp</code> 파일을 확인할 수 있습니다.</p>
<h3 id="메시지-타입-찾는-방법">메시지 타입 찾는 방법</h3>
<ol>
<li><code>ros2 topic list</code>로 토픽 확인</li>
<li><code>ros2 topic info /토픽명</code>으로 메시지 타입 확인</li>
<li><code>ros2 interface show 메시지타입</code>으로 구조 확인</li>
<li>또는 <strong>rqt Topic Monitor</strong>로 모든 정보 한 번에 확인</li>
</ol>
<hr />
<h2 id="8-실전-활용-예시">8. 실전 활용 예시</h2>
<h3 id="배터리-잔량에-따른-동작-변경">배터리 잔량에 따른 동작 변경</h3>
<pre><code class="language-cpp">void subscribe_topic_message(const sensor_msgs::msg::BatteryState::SharedPtr msg) const
{
  if (msg-&gt;percentage &lt; 20.0) {
    RCLCPP_WARN(this-&gt;get_logger(), &quot;Low Battery! %.2f%%&quot;, msg-&gt;percentage);
  } else {
    RCLCPP_INFO(this-&gt;get_logger(), &quot;Battery: %.2f%%, Voltage: %.2fV&quot;, 
                msg-&gt;percentage, msg-&gt;voltage);
  }
}</code></pre>
<p>배터리가 20% 이하로 떨어지면 경고 메시지를 출력할 수 있습니다.</p>
<h3 id="publisher와-결합">Publisher와 결합</h3>
<p>배터리가 부족하면 자동으로 충전 스테이션으로 이동하는 로직을 만들 수도 있습니다.</p>
<pre><code class="language-cpp">if (msg-&gt;percentage &lt; 15.0) {
  // cmd_vel_pub를 호출해서 충전 스테이션으로 이동
  auto cmd = geometry_msgs::msg::Twist();
  cmd.linear.x = -0.1;  // 후진
  cmd_vel_publisher_-&gt;publish(cmd);
}</code></pre>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 실제 TurtleBot3의 센서 데이터를 구독하는 노드를 작성해보았습니다.</p>
<p><strong>주요 학습 내용:</strong></p>
<ul>
<li><code>/battery_state</code> 토픽 분석</li>
<li><code>sensor_msgs/msg/BatteryState</code> 메시지 타입 사용</li>
<li>QoS 설정 (<code>rclcpp::QoS</code>)</li>
<li>CMakeLists.txt에 <code>sensor_msgs</code> 의존성 추가</li>
<li>실시간 배터리 모니터링 구현</li>
</ul>
<p><strong>핵심 포인트:</strong></p>
<ol>
<li>새로운 메시지 타입 사용 시 <code>find_package</code>와 <code>ament_target_dependencies</code>에 추가</li>
<li>헤더 파일은 <code>/opt/ros/humble/include/</code> 경로에서 확인 가능</li>
<li>메시지 구조는 <code>ros2 interface show</code> 또는 rqt로 확인</li>
<li>실제 하드웨어는 Bringup 후에만 토픽이 생성됨</li>
</ol>
<p>지금까지 3개의 글을 통해 ROS2의 Topic 통신, 커스텀 패키지 개발, 실전 센서 데이터 활용까지 다뤄보았습니다.</p>
<p>다음 글에서는 Service 통신과 Action 통신에 대해 정리하겠습니다.</p>