<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f03a16d5-c535-4257-a9ad-063fa7ecba0d/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://api.velog.io/rss/%EB%A7%81%ED%81%AC">5편: TurtleBot3 Battery State 모니터링</a></p>
</blockquote>
<p>이번 글에서는 Qt6 GUI와 ROS2를 통합하여 TurtleBot3를 방향 버튼으로 조종하고, 전압·배터리·위치 정보를 실시간으로 표시하는 프로그램을 만든 과정을 정리해보겠습니다.</p>
<hr />
<h2 id="1-qt6--ros2-ament_cmake-패키지-생성">1. Qt6 + ROS2 ament_cmake 패키지 생성</h2>
<p>먼저 기존 <code>kccistc_ros2_pkg</code>와 별도로 Qt 전용 패키지를 생성합니다.</p>
<pre><code class="language-bash">ros2 pkg create kccistc_ros2_qt \
  --build-type ament_cmake \
  --dependencies rclcpp std_msgs \
  --license Apache-2.0</code></pre>
<p>Qt6는 시스템 패키지가 아닌 Qt 인스톨러로 설치된 버전을 사용하기 때문에, <code>.bashrc</code>에 PATH를 추가해야 합니다.</p>
<pre><code class="language-bash">export PATH=/home/ubuntu/Qt/6.8.3/gcc_64/bin:/home/ubuntu/Qt/Tools/Ninja:/home/ubuntu/Qt/Tools/QtCreator/bin:/home/ubuntu/Qt/Tools/CMake/bin:$PATH</code></pre>
<hr />
<h2 id="2-hello_qt--qt--ros2-첫-통합-테스트">2. hello_qt — Qt + ROS2 첫 통합 테스트</h2>
<p>본격적인 로봇 제어 프로그램에 앞서, Qt6와 ROS2가 정상적으로 연동되는지 확인하기 위해 <code>hello_qt</code> 예제를 먼저 작성합니다.</p>
<p><code>src/hello_qt/</code> 디렉토리를 생성하고, Qt 예제 파일(<code>main.cpp</code>, <code>mainwidget.cpp</code>, <code>mainwidget.h</code>, <code>mainwidget.ui</code>)을 복사한 뒤 <code>CMakeLists.txt</code>를 다음과 같이 구성합니다.</p>
<pre><code class="language-cmake">cmake_minimum_required(VERSION 3.8)
project(kccistc_ros2_qt)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(Qt6 REQUIRED COMPONENTS Widgets Core Gui)

# Qt 자동 처리 활성화
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# hello_qt 빌드
add_executable(hello_qt
  src/hello_qt/main.cpp
  src/hello_qt/mainwidget.cpp
  src/hello_qt/mainwidget.h
  src/hello_qt/mainwidget.ui
)
ament_target_dependencies(hello_qt rclcpp)
target_link_libraries(hello_qt Qt6::Widgets)

install(TARGETS hello_qt
  DESTINATION lib/${PROJECT_NAME})

ament_package()</code></pre>
<p>빌드 후 실행하면 &quot;Hello Qt&quot; 라벨이 담긴 윈도우가 출력됩니다.</p>
<pre><code class="language-bash">cd ~/robot_ws
colcon build --packages-select kccistc_ros2_qt
source ~/robot_ws/install/local_setup.bash
ros2 run kccistc_ros2_qt hello_qt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1788bcc7-a5c9-4679-acb7-c2820017e4ab/image.png" /></p>
<hr />
<h2 id="3-teleop_qt--방향-버튼으로-로봇-조종하기">3. teleop_qt — 방향 버튼으로 로봇 조종하기</h2>
<p><code>hello_qt</code>로 동작을 확인한 뒤, 실제 로봇 제어를 위한 <code>teleop_qt</code> 패키지를 작성합니다. Qt Creator에서 <strong>C++ Class</strong> 추가 메뉴로 <code>RosNode</code> 클래스를 생성하고, Base class를 <code>QWidget</code>으로 설정합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/627375a9-35c2-4d90-8280-762887e36df6/image.png" /></p>
<h3 id="3-1-rosnode-클래스-설계">3-1. RosNode 클래스 설계</h3>
<p><code>RosNode</code>는 ROS2 퍼블리셔와 Qt 타이머를 함께 관리하는 핵심 클래스입니다. <code>cmd_vel_pub.cpp</code>의 구조를 참고하여 헤더 파일(<code>rosnode.h</code>)을 작성합니다.</p>
<pre><code class="language-cpp">// rosnode.h
#ifndef ROSNODE_H
#define ROSNODE_H

#include &lt;QWidget&gt;
#include &lt;QTimer&gt;
#include &quot;rclcpp/rclcpp.hpp&quot;
#include &quot;geometry_msgs/msg/twist.hpp&quot;

class RosNode : public QWidget
{
    Q_OBJECT

private:
    geometry_msgs::msg::Twist msg_twist;
    rclcpp::Node::SharedPtr node_teleop;
    rclcpp::Publisher&lt;geometry_msgs::msg::Twist&gt;::SharedPtr pub_teleop;
    rclcpp::TimerBase::SharedPtr timer_teleop;

public:
    explicit RosNode(QWidget *parent = nullptr);
    void RunTeleopPublisher(double linearX, double angularZ);
    void AasNode();

private slots:
    void OnTimerCallbackFunc();
};

#endif // ROSNODE_H</code></pre>
<h3 id="3-2-rosnode-구현-rosnodecpp">3-2. RosNode 구현 (rosnode.cpp)</h3>
<p>생성자에서 노드, 퍼블리셔, Qt 타이머를 초기화합니다. <code>rclcpp::spin_some()</code>은 Qt 타이머가 주기적으로 호출하여 ROS2 콜백을 처리합니다.</p>
<pre><code class="language-cpp">// rosnode.cpp
#include &quot;rosnode.h&quot;

RosNode::RosNode(QWidget *parent)
    : QWidget{parent}
{
    msg_twist = geometry_msgs::msg::Twist();
    rclcpp::init(0, nullptr);

    auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(10));
    node_teleop = rclcpp::Node::make_shared(&quot;teleop_bat_qt&quot;);
    pub_teleop = node_teleop-&gt;create_publisher&lt;geometry_msgs::msg::Twist&gt;(
        &quot;cmd_vel&quot;, 10);

    QTimer *pQTimer = new QTimer(this);
    connect(pQTimer, SIGNAL(timeout()), this, SLOT(OnTimerCallbackFunc()));
    pQTimer-&gt;start(100);
}

void RosNode::OnTimerCallbackFunc()
{
    rclcpp::spin_some(node_teleop);
}

void RosNode::RunTeleopPublisher(double linearX, double angularZ)
{
    msg_twist.linear.x = linearX;
    msg_twist.angular.z = angularZ;
    pub_teleop-&gt;publish(msg_twist);
}

void RosNode::AasNode()
{
    rclcpp::shutdown();
}</code></pre>
<blockquote>
<p><code>rclcpp::spin_some()</code>을 직접 루프로 돌리는 대신 Qt 타이머에 연결하면, Qt 이벤트 루프와 ROS2 콜백이 충돌 없이 함께 동작할 수 있습니다.</p>
</blockquote>
<h3 id="3-3-mainwidget에서-버튼-이벤트-연결">3-3. MainWidget에서 버튼 이벤트 연결</h3>
<p><code>mainwidget.cpp</code>에서 방향 버튼의 클릭 이벤트가 발생하면 <code>RosNode::RunTeleopPublisher()</code>를 호출합니다. Linear, Angular 값은 슬라이더 퍼센트 값을 스케일링하여 전달합니다.</p>
<pre><code class="language-cpp">void MainWidget::SetVelocity()
{
    QString strLinear = QString(&quot;linearX : %1%&quot;).arg(linX * 10);
    ui-&gt;pLabelLinear-&gt;setText(strLinear);

    QString strAnguar = QString(&quot;angularZ : %1%&quot;).arg(angZ * 10);
    ui-&gt;pLabelAngular-&gt;setText(strAnguar);

    // Linear: 0~0.22 m/s, Angular: 0~2.84 rad/s
    pRosNode-&gt;RunTeleopPublisher(0.022 * linX, 0.284 * angZ);
}</code></pre>
<p>빌드 후 실행하면 방향 버튼으로 TurtleBot3를 조종할 수 있습니다.</p>
<pre><code class="language-bash">colcon build --packages-select kccistc_ros2_qt
source ~/robot_ws/install/local_setup.bash
ros2 run kccistc_ros2_qt teleop_qt</code></pre>
<hr />
<h2 id="4-teleop_bat_qt--전압과-위치-정보-추가">4. teleop_bat_qt — 전압과 위치 정보 추가</h2>
<p><code>teleop_qt</code>에 배터리(<code>/battery_state</code>)와 위치(<code>/odom</code>) 토픽 구독 기능을 추가합니다.</p>
<h3 id="4-1-구독할-토픽-확인">4-1. 구독할 토픽 확인</h3>
<p>rqt Topic Monitor에서 <code>/odom</code> 토픽 구조를 확인하면 아래와 같습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/874798bd-8339-4afe-b1eb-bc92d2a16aca/image.png" /></p>
<p>필요한 값은 다음 네 가지입니다.</p>
<ul>
<li><code>pose.pose.position.x</code> — 현재 x 좌표</li>
<li><code>pose.pose.position.y</code> — 현재 y 좌표</li>
<li><code>pose.pose.orientation.z</code> — 방향 (쿼터니언 z)</li>
<li><code>pose.pose.orientation.w</code> — 방향 (쿼터니언 w)</li>
</ul>
<p>방향값의 의미는 아래와 같습니다.</p>
<table>
<thead>
<tr>
<th>방향</th>
<th>z</th>
<th>w</th>
</tr>
</thead>
<tbody><tr>
<td>정면 (0°)</td>
<td>0.0</td>
<td>1.0</td>
</tr>
<tr>
<td>좌측 (90°)</td>
<td>0.707</td>
<td>0.707</td>
</tr>
<tr>
<td>뒤 (180°)</td>
<td>1.0</td>
<td>0.0</td>
</tr>
<tr>
<td>우측 (270°)</td>
<td>-0.707</td>
<td>0.707</td>
</tr>
</tbody></table>
<h3 id="4-2-rosnodeh-수정">4-2. rosnode.h 수정</h3>
<p><code>kym_battery_sub.cpp</code>를 참고하여 배터리 구독자와 위치 표시 시그널을 추가합니다.</p>
<pre><code class="language-cpp">// rosnode.h (teleop_bat_qt)
#ifndef ROSNODE_H
#define ROSNODE_H

#include &lt;chrono&gt;
#include &lt;functional&gt;
#include &lt;memory&gt;
#include &quot;rclcpp/rclcpp.hpp&quot;
#include &quot;geometry_msgs/msg/twist.hpp&quot;
#include &quot;sensor_msgs/msg/battery_state.hpp&quot;
#include &quot;nav_msgs/msg/odometry.hpp&quot;

using namespace std::chrono_literals;

class RosNode : public QWidget
{
    Q_OBJECT

private:
    geometry_msgs::msg::Twist msg_twist;
    rclcpp::Node::SharedPtr node_teleop;
    rclcpp::Publisher&lt;geometry_msgs::msg::Twist&gt;::SharedPtr pub_teleop;
    rclcpp::Subscription&lt;sensor_msgs::msg::BatteryState&gt;::SharedPtr sub_battery;
    rclcpp::Subscription&lt;nav_msgs::msg::Odometry&gt;::SharedPtr sub_odom;
    rclcpp::TimerBase::SharedPtr timer_teleop;
    QTimer *pQTimerSpin;

public:
    explicit RosNode(QWidget *parent = nullptr);
    void RunTeleopPublisher(double linearX, double angularZ);
    void AasNode();
    void OCheckss();

signals:
    void batteryLcdDisplaySig(double, double);
    void odomLcdDisplaySig(double, double, double, double);

private slots:
    void OnTimerCallbackFunc();
};

#endif // ROSNODE_H</code></pre>
<h3 id="4-3-odom-구독-콜백-추가-rosnodecpp">4-3. odom 구독 콜백 추가 (rosnode.cpp)</h3>
<p>배터리 콜백과 동일한 패턴으로 <code>/odom</code> 구독을 추가합니다. 값이 들어오면 시그널을 통해 GUI LCD에 전달합니다.</p>
<pre><code class="language-cpp">// 생성자 내 odom 구독 추가
sub_odom = node_teleop-&gt;create_subscription&lt;nav_msgs::msg::Odometry&gt;(
    &quot;odom&quot;, qos_profile,
    std::bind(&amp;RosNode::subscribe_odom_msg, this, _1));

// odom 콜백
void RosNode::subscribe_odom_msg(
    const nav_msgs::msg::Odometry::SharedPtr message) const
{
    double pos_x = message-&gt;pose.pose.position.x;
    double pos_y = message-&gt;pose.pose.position.y;
    double ori_z = message-&gt;pose.pose.orientation.z;
    double ori_w = message-&gt;pose.pose.orientation.w;

    emit odomLcdDisplaySig(pos_x, pos_y, ori_z, ori_w);
}</code></pre>
<blockquote>
<p>평상시에는 로봇이 정지해 있어 값이 0.0으로 유지됩니다. teleop으로 이동하면 실시간으로 값이 갱신되는 것을 확인할 수 있습니다.</p>
</blockquote>
<h3 id="4-4-mainwidget에서-lcd-연결">4-4. MainWidget에서 LCD 연결</h3>
<p><code>mainwidget.cpp</code> 생성자에서 시그널-슬롯을 연결합니다.</p>
<pre><code class="language-cpp">pRosNode = new RosNode(this);

connect(pRosNode, SIGNAL(batteryLcdDisplaySig(double, double)),
        this, SLOT(batteryLcdDisplaySig(double, double)));

connect(pRosNode, SIGNAL(odomLcdDisplaySig(double, double, double, double)),
        this, SLOT(odomLcdDisplaySig(double, double, double, double)));</code></pre>
<hr />
<h2 id="5-cmakeliststxt-최종-구성">5. CMakeLists.txt 최종 구성</h2>
<p><code>package.xml</code>에 <code>Qt6</code>, <code>geometry_msgs</code>, <code>sensor_msgs</code>, <code>nav_msgs</code> 의존성을 추가하고, <code>CMakeLists.txt</code>를 아래와 같이 정리합니다.</p>
<pre><code class="language-cmake">find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(Qt6 REQUIRED COMPONENTS Widgets Core Gui)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# hello_qt
add_executable(hello_qt
  src/hello_qt/main.cpp
  src/hello_qt/mainwidget.cpp
  src/hello_qt/mainwidget.h
  src/hello_qt/mainwidget.ui
)
ament_target_dependencies(hello_qt rclcpp)
target_link_libraries(hello_qt Qt6::Widgets)

# teleop_qt
add_executable(teleop_qt
  src/teleop_qt/main.cpp
  src/teleop_qt/mainwidget.cpp
  src/teleop_qt/mainwidget.h
  src/teleop_qt/mainwidget.ui
  src/teleop_qt/rosnode.cpp
  src/teleop_qt/rosnode.h
)
ament_target_dependencies(teleop_qt rclcpp geometry_msgs)
target_include_directories(teleop_qt PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_link_libraries(teleop_qt Qt6::Widgets)

# teleop_bat_qt
add_executable(teleop_bat_qt
  src/teleop_bat_qt/main.cpp
  src/teleop_bat_qt/mainwidget.cpp
  src/teleop_bat_qt/mainwidget.h
  src/teleop_bat_qt/mainwidget.ui
  src/teleop_bat_qt/rosnode.cpp
  src/teleop_bat_qt/rosnode.h
)
ament_target_dependencies(teleop_bat_qt rclcpp geometry_msgs sensor_msgs nav_msgs)
target_include_directories(teleop_bat_qt PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_link_libraries(teleop_bat_qt Qt6::Widgets)

install(TARGETS
  hello_qt
  teleop_qt
  teleop_bat_qt
  DESTINATION lib/${PROJECT_NAME})</code></pre>
<hr />
<h2 id="6-실행-결과">6. 실행 결과</h2>
<p>빌드 후 실행하면 아래와 같은 GUI를 확인할 수 있습니다.</p>
<pre><code class="language-bash">cd ~/robot_ws
colcon build --packages-select kccistc_ros2_qt
source ~/robot_ws/install/local_setup.bash
ros2 run kccistc_ros2_qt teleop_bat_qt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c279cf24-802c-4a00-b50f-c5b86926f711/image.png" /></p>
<ul>
<li><strong>Voltage / Percentage</strong>: <code>/battery_state</code> 토픽에서 실시간 수신</li>
<li><strong>pos.x / pos.y / ori.z / ori.w</strong>: <code>/odom</code> 토픽에서 실시간 수신, 로봇 이동 시 값 변경 확인</li>
<li><strong>방향 버튼</strong>: <code>/cmd_vel</code> 퍼블리시로 실제 로봇 제어</li>
</ul>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 Qt6와 ROS2를 ament_cmake 기반으로 통합하는 방법을 정리해보았습니다. 핵심 포인트는 <code>rclcpp::spin_some()</code>을 Qt 타이머에 연결하여 두 이벤트 루프가 충돌하지 않도록 구성하는 것이었습니다. <code>hello_qt</code>로 기초 연동을 확인하고, <code>teleop_qt</code>, <code>teleop_bat_qt</code> 순서로 기능을 점진적으로 추가하는 방식이 실습에 적합합니다.</p>
<p>다음 글에서는 Nav2를 활용한 자율 주행 목표 지점 설정을 정리하겠습니다.</p>