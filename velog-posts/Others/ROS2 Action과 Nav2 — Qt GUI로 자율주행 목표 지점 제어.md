<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d3d04aeb-63b8-41f6-b79f-99f249fbf4d3/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/ROS2-QT-%EB%A1%9C%EB%B4%87-%EC%A1%B0%EC%A2%85-GUI-%EB%A7%8C%EB%93%A4%EA%B8%B0">6편: Qt GUI로 TurtleBot3 조종하기</a></p>
</blockquote>
<p>이번 글에서는 ROS2 Action의 개념을 정리하고, Nav2의 <code>/navigate_to_pose</code> 액션을 활용하여 Qt GUI에서 자율주행 목표 지점을 전송하는 프로그램을 만든 과정을 정리해보겠습니다. 아울러 <code>/amcl_pose</code> 구독을 통해 로봇의 현재 위치를 실시간으로 표시하고, teleop 모드와 자율주행 모드를 안전하게 전환하는 기능도 함께 다루겠습니다.</p>
<hr />
<h2 id="1-ros2-통신-방식-비교--topic--service--action">1. ROS2 통신 방식 비교 — Topic / Service / Action</h2>
<p>본격적인 구현에 앞서 세 가지 통신 방식의 차이를 정리해두겠습니다.</p>
<p><strong>Topic</strong>은 퍼블리셔가 구독자에게 지속적으로 데이터를 전송하는 1:다 구조입니다. 실시간성이 좋지만 누가 수신하는지 알 수 없어 보안상 단점이 있습니다.</p>
<p><strong>Service</strong>는 클라이언트가 요청하면 서버가 한 번 응답하는 1:1 구조입니다. 요청이 있을 때만 데이터를 주고받기 때문에 Topic에 비해 보안상 유리합니다. 다만 응답이 오기 전까지 결과를 알 수 없습니다.</p>
<p><strong>Action</strong>은 Service를 기반으로 하되, 목표를 보낸 뒤 완료까지 주기적인 Feedback을 지속적으로 받을 수 있는 구조입니다. 목표(Goal), 피드백(Feedback), 결과(Result)의 세 부분으로 구성됩니다. 장시간 실행되는 태스크에 적합하며, 진행 중에 취소도 가능합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6a6e690e-cedd-494d-8272-0a4f14026b73/image.png" /></p>
<p>Nav2의 자율주행이 Action을 사용하는 이유가 여기에 있습니다. 목표 지점까지 이동하는 데 수십 초가 걸릴 수 있고, 그 동안 남은 거리를 Feedback으로 계속 받아야 하기 때문입니다.</p>
<hr />
<h2 id="2-turtlesim으로-action-실습">2. turtlesim으로 Action 실습</h2>
<p>개념을 확인하기 위해 turtlesim의 <code>/turtle1/rotate_absolute</code> 액션을 먼저 실습합니다.</p>
<pre><code class="language-bash">ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key</code></pre>
<p><code>turtle_teleop_key</code>에서 방향키는 Topic(<code>/turtle1/cmd_vel</code>)으로 동작하지만, <code>G|B|V|C|D|E|R|T</code> 키는 절대 각도 회전 액션으로 동작합니다.</p>
<p>노드 정보를 확인하면 turtlesim은 Action Server, teleop_turtle은 Action Client로 구성되어 있음을 확인할 수 있습니다.</p>
<pre><code class="language-bash">ros2 node info /turtlesim
# Action Servers:
#   /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute

ros2 node info /teleop_turtle
# Action Clients:
#   /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute</code></pre>
<p>액션 인터페이스 구조는 <code>---</code>로 Goal / Result / Feedback 세 영역이 구분됩니다.</p>
<pre><code class="language-bash">ros2 interface show turtlesim/action/RotateAbsolute
# float32 theta        ← Goal: 목표 각도 (rad)
# ---
# float32 delta        ← Result: 실제 회전량
# ---
# float32 remaining    ← Feedback: 남은 회전량</code></pre>
<p>목표를 전송하고 Feedback을 확인합니다.</p>
<pre><code class="language-bash">ros2 action send_goal /turtle1/rotate_absolute \
  turtlesim/action/RotateAbsolute &quot;{theta: 1.57}&quot; --feedback</code></pre>
<p>Feedback으로 <code>remaining</code> 값이 점점 줄어들다가 완료되면 <code>Goal finished with status: SUCCEEDED</code>가 출력됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/940a1114-ef9d-42ca-a288-893bb0b2dde7/image.png" /></p>
<hr />
<h2 id="3-nav2-action-확인">3. Nav2 Action 확인</h2>
<p>Nav2가 실행된 상태에서 액션 목록을 확인하면 다양한 네비게이션 액션이 등록되어 있습니다.</p>
<pre><code class="language-bash">ros2 action list -t
# /navigate_to_pose [nav2_msgs/action/NavigateToPose]
# /follow_waypoints [nav2_msgs/action/FollowWaypoints]
# ...</code></pre>
<p>우리가 사용할 것은 <code>/navigate_to_pose</code>입니다. Nav2 실행 시 주의할 점은 navi 실행 중에는 teleop을 절대 함께 실행하면 안 된다는 점입니다. 두 노드가 동시에 <code>/cmd_vel</code>을 퍼블리시하면 충돌이 발생합니다.</p>
<hr />
<h2 id="4-nav_to_pose_clientcpp--action-client-구현">4. nav_to_pose_client.cpp — Action Client 구현</h2>
<p><code>kccistc_ros2_pkg</code>에 Nav2 Action Client 노드를 작성합니다. <code>CMakeLists.txt</code>에 <code>rclcpp_action</code>과 <code>nav2_msgs</code>를 추가합니다.</p>
<pre><code class="language-cmake">find_package(rclcpp_action REQUIRED)
find_package(nav2_msgs REQUIRED)

add_executable(nav_to_pose_client src/nav_to_pose_client.cpp)
ament_target_dependencies(nav_to_pose_client
  rclcpp rclcpp_action std_msgs nav2_msgs)</code></pre>
<p>핵심 구현 내용입니다. <code>flagPoint</code>를 이용해 첫 번째 목표 도착 후 두 번째 목표(복귀)를 자동 전송하는 방식입니다.</p>
<pre><code class="language-cpp">// nav_to_pose_client.cpp 핵심 구조
class Nav2Client : public rclcpp::Node {
public:
  int flagPoint = 0;
  using NavigateToPose = nav2_msgs::action::NavigateToPose;
  using GoalHandleNav = rclcpp_action::ClientGoalHandle&lt;NavigateToPose&gt;;

  void send_goal(float x, float y) {
    auto goal_msg = NavigateToPose::Goal();
    goal_msg.pose.header.frame_id = &quot;map&quot;;
    goal_msg.pose.pose.position.x = x;
    goal_msg.pose.pose.position.y = y;
    goal_msg.pose.pose.orientation.w = 1.0;

    // 피드백: 남은 거리 출력
    send_goal_options.feedback_callback = [this](...) {
      RCLCPP_INFO(..., &quot;Distance remaining: %f&quot;, feedback-&gt;distance_remaining);
    };

    // 결과: 도착 시 flagPoint 증가
    send_goal_options.result_callback = [&amp;](...) {
      if (result.code == rclcpp_action::ResultCode::SUCCEEDED)
        flagPoint++;
    };

    client_ptr_-&gt;async_send_goal(goal_msg, send_goal_options);
  }
};

// main: flagPoint 값에 따라 순차 목표 전송
while (rclcpp::ok()) {
  rclcpp::spin_some(node);
  rate.sleep();
  if ((node-&gt;flagPoint == 1) &amp;&amp; check) {
    node-&gt;send_goal(0, 0);  // 원점 복귀
    check = 0;
  }
  if (node-&gt;flagPoint == 2) break;  // 완료 후 종료
}</code></pre>
<hr />
<h2 id="5-teleop_bat_amcl_qt--qt-gui에-nav2-통합">5. teleop_bat_amcl_qt — Qt GUI에 Nav2 통합</h2>
<p>이전 <code>teleop_bat_qt</code>를 기반으로 <code>/amcl_pose</code> 구독과 Nav2 Action Client를 추가한 <code>teleop_bat_amcl_qt</code> 패키지를 작성합니다.</p>
<h3 id="5-1-amcl_pose-구독">5-1. /amcl_pose 구독</h3>
<p><code>/amcl_pose</code> 토픽의 타입은 <code>geometry_msgs/msg/PoseWithCovarianceStamped</code>입니다.</p>
<pre><code class="language-bash">ros2 interface show geometry_msgs/msg/PoseWithCovarianceStamped
# PoseWithCovariance pose
#   Pose pose
#     Point position
#       float64 x
#       float64 y
#     Quaternion orientation
#       float64 z
#       float64 w</code></pre>
<p><code>rosnode.h</code>에 구독자와 시그널을 추가합니다.</p>
<pre><code class="language-cpp">// rosnode.h
#include &quot;geometry_msgs/msg/pose_with_covariance_stamped.hpp&quot;

private:
  rclcpp::Subscription&lt;geometry_msgs::msg::PoseWithCovarianceStamped&gt;::SharedPtr sub_amcl_pose;
  void subscribe_amcl_pose_msg(
    const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr message);

signals:
  void amclposeLcdDisplaySig(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr);</code></pre>
<p>콜백에서 position.x/y, orientation.z/w를 추출해 시그널로 전달합니다.</p>
<pre><code class="language-cpp">void RosNode::subscribe_amcl_pose_msg(
    const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg)
{
  double px = msg-&gt;pose.pose.position.x;
  double py = msg-&gt;pose.pose.position.y;
  double oz = msg-&gt;pose.pose.orientation.z;
  double ow = msg-&gt;pose.pose.orientation.w;
  emit poseLcdDisplaySig(px, py, oz, ow);
}</code></pre>
<blockquote>
<p>평상시에는 로봇이 정지해 있어 값이 0.0으로 유지됩니다. Nav2로 이동을 시작하면 실시간으로 값이 갱신됩니다.</p>
</blockquote>
<h3 id="5-2-rosnodeaction-클래스--nav2-action-client">5-2. RosNodeAction 클래스 — Nav2 Action Client</h3>
<p>Action Client는 별도 클래스 <code>RosNodeAction</code>으로 분리합니다. <code>rosnode_action.h</code>와 <code>rosnode_action.cpp</code>를 추가합니다.</p>
<pre><code class="language-cpp">// rosnode_action.h
#include &quot;rclcpp_action/rclcpp_action.hpp&quot;
#include &quot;nav2_msgs/action/navigate_to_pose.hpp&quot;

class RosNodeAction : public QWidget {
  Q_OBJECT
public:
  using NavigateToPose = nav2_msgs::action::NavigateToPose;
  void send_goal(double spinBoxArray[4]);  // x, y, oz, ow
  // ...
};</code></pre>
<p><code>send_goal()</code>은 <code>spinBoxArray[4]</code> 배열로 x, y, orientation.z, orientation.w를 받아 Nav2에 전송합니다.</p>
<h3 id="5-3-프리셋-버튼과-수동-좌표-입력">5-3. 프리셋 버튼과 수동 좌표 입력</h3>
<p><code>mainwidget.cpp</code>에서 Study / Front / Living / Bedroom 버튼 클릭 시 미리 정해둔 좌표 배열을 전달합니다.</p>
<pre><code class="language-cpp">void MainWidget::on_pPBBedroom_clicked()
{
    double spinBoxArray[4] = {2.0, 1.0, -0.784, 0.704};
    pRosNodeAction-&gt;send_goal(spinBoxArray);
}</code></pre>
<p>수동 입력은 UI의 SpinBox에서 pos.x, pos.y, ori.z, ori.w 값을 직접 입력한 뒤 goGoal 버튼을 누르는 방식입니다.</p>
<h3 id="5-4-teleop-안전-잠금">5-4. teleop 안전 잠금</h3>
<p>Nav2 실행 중 teleop이 동시에 동작하면 안 되므로, teleop 체크박스 상태에 따라 퍼블리시를 차단합니다.</p>
<pre><code class="language-cpp">void RosNode::setTeleopEnabled(bool enabled)
{
    m_teleopEnabled = enabled;
    if (!enabled) {
        msg_twist.linear.x = 0;
        msg_twist.angular.z = 0;
        pub_teleop-&gt;publish(msg_twist);  // 즉시 정지
    }
}

void RosNode::RunTeleopPublisher(double linearX, double angularZ)
{
    if (!m_teleopEnabled) return;  // 체크 해제 시 무시
    msg_twist.linear.x += linearX;
    msg_twist.angular.z += angularZ;
    pub_teleop-&gt;publish(msg_twist);
}</code></pre>
<hr />
<h2 id="6-mapyaml-설정">6. map.yaml 설정</h2>
<p>Nav2 실행 시 맵 파일을 지정합니다. <code>~/map/map.yaml</code>의 주요 항목은 다음과 같습니다.</p>
<pre><code class="language-yaml">image: map_603.pgm
mode: trinary
resolution: 0.05
origin: [-2.27, -7.02, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25</code></pre>
<p>Nav2 실행 편의를 위해 <code>~/bin/navi.sh</code> 스크립트를 작성해두면 매번 긴 명령어를 입력하지 않아도 됩니다.</p>
<pre><code class="language-bash"># ~/bin/navi.sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=$HOME/map/map.yaml</code></pre>
<hr />
<h2 id="7-빌드-및-실행">7. 빌드 및 실행</h2>
<pre><code class="language-bash">cd ~/robot_ws
colcon build --packages-select kccistc_ros2_qt
source install/local_setup.bash
ros2 run kccistc_ros2_qt teleop_bat_amcl_qt</code></pre>
<blockquote>
<p><code>local_setup.bash</code> 대신 <code>setup.bash</code>를 사용해야 <code>ros2 run</code>에서 패키지를 정상적으로 탐색할 수 있습니다. 빌드 후 <code>ils</code>(source install/setup.bash 별칭) 실행을 잊지 않도록 주의합니다.</p>
</blockquote>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 ROS2 Action의 구조를 turtlesim 실습으로 확인하고, Nav2의 <code>/navigate_to_pose</code> 액션을 Qt GUI에 통합하는 과정을 정리해보았습니다. 핵심 포인트는 Action Client를 별도 클래스로 분리하고, teleop 체크박스로 수동·자율 모드를 안전하게 전환하는 설계였습니다.</p>
<p>다음 글에서는 LiDAR 거리 데이터와 Raspberry Pi Camera Module 2 영상을 Qt GUI에 함께 표시하는 과정을 정리하겠습니다.</p>