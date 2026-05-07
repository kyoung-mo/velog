<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ddc1ac18-9490-4538-aa4c-219f543ab237/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/ROS2-%EA%B8%B0%EC%B4%88-TurtldSim%EA%B3%BC-Topic-%ED%86%B5%EC%8B%A0-%EC%8B%A4%EC%8A%B5">ROS2 기초 - TurtleSim과 Topic 통신 실습</a></p>
</blockquote>
<p>이번 글에서는 직접 C++ 코드로 ROS2 패키지를 만들고, Publisher와 Subscriber 노드를 구현하는 과정을 정리하겠습니다.</p>
<p>이전 글에서는 <code>ros2 topic pub</code> 명령어로 메시지를 발행했지만, 실제 로봇 개발에서는 C++ 또는 Python으로 노드를 작성해야 합니다.</p>
<hr />
<h2 id="1-패키지-생성">1. 패키지 생성</h2>
<p>ROS2 패키지는 관련된 노드, 라이브러리, 설정 파일 등을 묶어놓은 단위입니다.</p>
<p>작업 공간으로 이동한 후 패키지를 생성합니다.</p>
<pre><code class="language-bash">cd ~/robot_ws/src
ros2 pkg create my_first_ros_rclcpp_pkg --build-type ament_cmake --dependencies rclcpp std_msgs</code></pre>
<ul>
<li><code>--build-type ament_cmake</code>: C++ 패키지 (Python은 <code>ament_python</code>)</li>
<li><code>--dependencies rclcpp std_msgs</code>: 의존성 패키지 자동 추가</li>
</ul>
<p>생성된 패키지 구조를 확인해봅니다.</p>
<pre><code class="language-bash">cd my_first_ros_rclcpp_pkg
tree</code></pre>
<pre><code>.
├── CMakeLists.txt
├── include
│   └── my_first_ros_rclcpp_pkg
├── package.xml
└── src</code></pre><p>기본적으로 <code>src</code> 폴더에 소스 코드를 작성하고, <code>CMakeLists.txt</code>에서 빌드 설정을 합니다.</p>
<hr />
<h2 id="2-gazebo로-작업-환경-준비">2. Gazebo로 작업 환경 준비</h2>
<p>실제 TurtleBot3을 켜기 전에 Gazebo 시뮬레이터에서 먼저 테스트해봅니다.</p>
<h3 id="gazebo-실행">Gazebo 실행</h3>
<pre><code class="language-bash">ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py</code></pre>
<h3 id="navigation-실행">Navigation 실행</h3>
<pre><code class="language-bash">ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=true map:=$HOME/map.yaml</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4a203891-2640-4c72-8ea5-8c14b43566dd/image.png" /></p>
<p>RViz에서 <code>2D Pose Estimate</code>를 클릭해 로봇의 초기 위치를 설정해줍니다.</p>
<p>이제 <code>/cmd_vel</code> 토픽으로 메시지를 보내면 로봇이 움직이는 것을 확인할 수 있습니다.</p>
<hr />
<h2 id="3-cmd_vel_pubcpp-작성">3. cmd_vel_pub.cpp 작성</h2>
<p>Publisher 노드를 작성해봅니다. 이 노드는 주기적으로 <code>/cmd_vel</code> 토픽으로 속도 명령을 발행합니다.</p>
<pre><code class="language-bash">cd ~/robot_ws/src/kccistc_ros2_pkg/src
vi cmd_vel_pub.cpp</code></pre>
<h3 id="코드-작성">코드 작성</h3>
<pre><code class="language-cpp">#include &lt;chrono&gt;
#include &lt;memory&gt;

#include &quot;rclcpp/rclcpp.hpp&quot;
#include &quot;geometry_msgs/msg/twist.hpp&quot;

using namespace std::chrono_literals;

class CmdVelPublisher : public rclcpp::Node
{
public:
  CmdVelPublisher()
  : Node(&quot;cmd_vel_publisher&quot;)
  {
    publisher_ = this-&gt;create_publisher&lt;geometry_msgs::msg::Twist&gt;(&quot;cmd_vel&quot;, 10);
    timer_ = this-&gt;create_wall_timer(
      500ms, std::bind(&amp;CmdVelPublisher::publish_velocity, this));
  }

private:
  void publish_velocity()
  {
    auto message = geometry_msgs::msg::Twist();
    message.linear.x = 0.1;  // 전진 속도
    message.angular.z = 0.0; // 회전 속도

    RCLCPP_INFO(this-&gt;get_logger(), &quot;Publishing: linear=%.2f, angular=%.2f&quot;, 
                message.linear.x, message.angular.z);
    publisher_-&gt;publish(message);
  }

  rclcpp::Publisher&lt;geometry_msgs::msg::Twist&gt;::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared&lt;CmdVelPublisher&gt;());
  rclcpp::shutdown();
  return 0;
}</code></pre>
<h3 id="코드-설명">코드 설명</h3>
<ol>
<li><p><strong>헤더 파일</strong></p>
<ul>
<li><code>rclcpp/rclcpp.hpp</code>: ROS2 C++ 라이브러리</li>
<li><code>geometry_msgs/msg/twist.hpp</code>: Twist 메시지 타입</li>
</ul>
</li>
<li><p><strong>클래스 구조</strong></p>
<ul>
<li><code>rclcpp::Node</code>를 상속받아 노드를 구현합니다.</li>
<li>생성자에서 Publisher와 Timer를 초기화합니다.</li>
</ul>
</li>
<li><p><strong>Publisher 생성</strong></p>
<ul>
<li><code>create_publisher&lt;메시지타입&gt;(&quot;토픽명&quot;, QoS크기)</code></li>
<li>QoS 10은 최근 10개 메시지를 버퍼에 보관한다는 의미입니다.</li>
</ul>
</li>
<li><p><strong>Timer 설정</strong></p>
<ul>
<li><code>create_wall_timer</code>로 주기적으로 함수를 호출합니다.</li>
<li><code>500ms</code>마다 <code>publish_velocity</code> 함수가 실행됩니다.</li>
</ul>
</li>
<li><p><strong>메시지 발행</strong></p>
<ul>
<li><code>Twist</code> 메시지를 생성하고 값을 설정합니다.</li>
<li><code>publisher_-&gt;publish(message)</code>로 발행합니다.</li>
</ul>
</li>
</ol>
<hr />
<h2 id="4-cmd_vel_subcpp-작성">4. cmd_vel_sub.cpp 작성</h2>
<p>이번에는 Subscriber 노드를 작성합니다. <code>/cmd_vel</code> 토픽을 구독해서 값을 출력합니다.</p>
<pre><code class="language-bash">vi cmd_vel_sub.cpp</code></pre>
<h3 id="코드-작성-1">코드 작성</h3>
<pre><code class="language-cpp">#include &lt;memory&gt;

#include &quot;rclcpp/rclcpp.hpp&quot;
#include &quot;geometry_msgs/msg/twist.hpp&quot;

using std::placeholders::_1;

class CmdVelSubscriber : public rclcpp::Node
{
public:
  CmdVelSubscriber()
  : Node(&quot;cmd_vel_subscriber&quot;)
  {
    subscription_ = this-&gt;create_subscription&lt;geometry_msgs::msg::Twist&gt;(
      &quot;cmd_vel&quot;, 10, std::bind(&amp;CmdVelSubscriber::topic_callback, this, _1));
  }

private:
  void topic_callback(const geometry_msgs::msg::Twist::SharedPtr msg) const
  {
    RCLCPP_INFO(this-&gt;get_logger(), &quot;Received: linear=%.2f, angular=%.2f&quot;,
                msg-&gt;linear.x, msg-&gt;angular.z);
  }

  rclcpp::Subscription&lt;geometry_msgs::msg::Twist&gt;::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared&lt;CmdVelSubscriber&gt;());
  rclcpp::shutdown();
  return 0;
}</code></pre>
<h3 id="코드-설명-1">코드 설명</h3>
<ol>
<li><p><strong>Subscriber 생성</strong></p>
<ul>
<li><code>create_subscription&lt;메시지타입&gt;(&quot;토픽명&quot;, QoS크기, 콜백함수)</code></li>
<li><code>std::bind</code>로 멤버 함수를 콜백으로 등록합니다.</li>
</ul>
</li>
<li><p><strong>콜백 함수</strong></p>
<ul>
<li>메시지가 들어올 때마다 자동으로 호출됩니다.</li>
<li><code>SharedPtr</code>로 메시지를 받습니다.</li>
</ul>
</li>
<li><p><strong>메시지 접근</strong></p>
<ul>
<li><code>msg-&gt;linear.x</code>, <code>msg-&gt;angular.z</code>로 값을 읽습니다.</li>
</ul>
</li>
</ol>
<hr />
<h2 id="5-cmakeliststxt-수정">5. CMakeLists.txt 수정</h2>
<p>작성한 코드를 빌드하려면 <code>CMakeLists.txt</code>에 등록해야 합니다.</p>
<pre><code class="language-bash">cd ~/robot_ws/src/kccistc_ros2_pkg
vi CMakeLists.txt</code></pre>
<h3 id="의존성-추가">의존성 추가</h3>
<pre><code class="language-cmake">find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)</code></pre>
<p><code>geometry_msgs</code> 패키지를 추가합니다.</p>
<h3 id="실행-파일-빌드">실행 파일 빌드</h3>
<pre><code class="language-cmake"># Publisher
add_executable(cmd_vel_pub src/cmd_vel_pub.cpp)
ament_target_dependencies(cmd_vel_pub rclcpp std_msgs geometry_msgs)

# Subscriber
add_executable(cmd_vel_sub src/cmd_vel_sub.cpp)
ament_target_dependencies(cmd_vel_sub rclcpp std_msgs geometry_msgs)</code></pre>
<h3 id="설치-설정">설치 설정</h3>
<pre><code class="language-cmake">install(TARGETS
  cmd_vel_pub
  cmd_vel_sub
  DESTINATION lib/${PROJECT_NAME})</code></pre>
<p><code>install</code> 디렉터리로 복사되어 <code>ros2 run</code> 명령어로 실행할 수 있게 됩니다.</p>
<hr />
<h2 id="6-빌드-및-실행">6. 빌드 및 실행</h2>
<h3 id="패키지-빌드">패키지 빌드</h3>
<pre><code class="language-bash">cd ~/robot_ws
colcon build --packages-select kccistc_ros2_pkg</code></pre>
<p>빌드가 완료되면 다음과 같이 출력됩니다.</p>
<pre><code>Summary: 1 package finished [시간]</code></pre><h3 id="환경-설정-적용">환경 설정 적용</h3>
<p>빌드 후에는 반드시 새로운 <code>setup.bash</code>를 source해야 합니다.</p>
<pre><code class="language-bash">source ~/robot_ws/install/local_setup.bash</code></pre>
<blockquote>
<p><strong>중요</strong>: 매번 새 터미널을 열 때마다 source를 해줘야 하므로, <code>.bashrc</code>에 등록하는 것을 권장합니다.</p>
</blockquote>
<pre><code class="language-bash">echo &quot;source ~/robot_ws/install/local_setup.bash&quot; &gt;&gt; ~/.bashrc</code></pre>
<h3 id="publisher-실행">Publisher 실행</h3>
<pre><code class="language-bash">ros2 run kccistc_ros2_pkg cmd_vel_pub</code></pre>
<p>로봇이 전진하는 것을 확인할 수 있습니다.</p>
<h3 id="subscriber-실행">Subscriber 실행</h3>
<p>새 터미널에서:</p>
<pre><code class="language-bash">source ~/robot_ws/install/local_setup.bash
ros2 run kccistc_ros2_pkg cmd_vel_sub</code></pre>
<p>Publisher가 발행하는 메시지를 실시간으로 받아서 출력합니다.</p>
<hr />
<h2 id="7-rqt_graph로-확인">7. rqt_graph로 확인</h2>
<p>노드 간 통신 관계를 시각적으로 확인해봅니다.</p>
<pre><code class="language-bash">ros2 run rqt_graph rqt_graph</code></pre>
<p><code>cmd_vel_publisher</code> → <code>/cmd_vel</code> → <code>cmd_vel_subscriber</code> 연결이 보입니다.</p>
<hr />
<h2 id="8-실제-turtlebot3에-적용하기">8. 실제 TurtleBot3에 적용하기</h2>
<h3 id="gazebo-종료">Gazebo 종료</h3>
<p>실제 로봇을 사용할 때는 Gazebo를 종료해야 합니다.</p>
<pre><code class="language-bash">ros2 node list</code></pre>
<p>모든 노드가 종료되었는지 확인합니다.</p>
<h3 id="turtlebot3-bringup">TurtleBot3 Bringup</h3>
<p>라즈베리파이(SBC)에서:</p>
<pre><code class="language-bash">ros2 launch turtlebot3_bringup robot.launch.py</code></pre>
<h3 id="publisher-실행-1">Publisher 실행</h3>
<p>Ubuntu PC에서:</p>
<pre><code class="language-bash">source ~/robot_ws/install/local_setup.bash
ros2 run kccistc_ros2_pkg cmd_vel_pub</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/82e5d623-f3e5-4b8a-b441-1e3e20ebd214/image.png" /></p>
<p>실제 TurtleBot3이 움직이는 것을 확인할 수 있습니다!</p>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 ROS2 커스텀 패키지를 만들고 Publisher/Subscriber를 직접 구현해보았습니다.</p>
<p><strong>주요 학습 내용:</strong></p>
<ul>
<li>ROS2 패키지 생성 (<code>ros2 pkg create</code>)</li>
<li>C++ Publisher/Subscriber 코드 작성</li>
<li><code>CMakeLists.txt</code> 빌드 설정</li>
<li><code>colcon build</code>로 패키지 빌드</li>
<li>Gazebo 시뮬레이터와 실제 로봇에서 테스트</li>
</ul>
<p><strong>핵심 포인트:</strong></p>
<ol>
<li>메시지 타입 확인: <code>ros2 interface show</code></li>
<li>헤더 파일 include: <code>geometry_msgs/msg/twist.hpp</code></li>
<li>CMakeLists.txt에 의존성 추가: <code>geometry_msgs</code></li>
<li>빌드 후 source 적용: <code>source install/local_setup.bash</code></li>
</ol>
<p>다음 글에서는 실제 TurtleBot3의 배터리 상태를 모니터링하는 노드를 작성하는 과정을 정리하겠습니다.</p>