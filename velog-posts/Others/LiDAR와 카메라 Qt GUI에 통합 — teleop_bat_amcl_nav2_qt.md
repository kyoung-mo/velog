<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fcbd99ad-4cf2-4da8-b26a-bbf8bf2db339/image.png" /></p>
<blockquote>
<p>이전 글 : <a href="https://velog.io/@mommers/ROS2-Action%EA%B3%BC-Nav2-Qt-GUI%EB%A1%9C-%EC%9E%90%EC%9C%A8%EC%A3%BC%ED%96%89-%EB%AA%A9%ED%91%9C-%EC%A7%80%EC%A0%90-%EC%A0%9C%EC%96%B4">7편: ROS2 Action과 Nav2 — Qt GUI로 자율주행 목표 지점 제어하기</a></p>
</blockquote>
<p>이번 글에서는 LiDAR(<code>/scan</code>) 거리 데이터와 Raspberry Pi Camera Module 2 영상을 Qt GUI에 함께 표시하는 최종 통합 프로그램을 만든 과정을 정리해보겠습니다. OpenCV를 소스에서 직접 빌드하는 방법과 <code>image_transport</code>, <code>cv_bridge</code>를 이용한 카메라 영상 처리 방법도 함께 다루겠습니다.</p>
<hr />
<h2 id="1-최종-gui-구성">1. 최종 GUI 구성</h2>
<p>완성된 <code>teleop_bat_amcl_nav2_qt</code> 프로그램의 구성은 다음과 같습니다.</p>
<ul>
<li><strong>상단</strong>: Voltage / Percentage LCD, 방향별(0°/90°/180°/270°) LiDAR 거리 표시</li>
<li><strong>중단</strong>: pos.x / pos.y / ori.w / ori.z LCD (amcl_pose)</li>
<li><strong>버튼</strong>: Study / Front / Living / Bedroom 프리셋, 수동 좌표 입력 + goGoal</li>
<li><strong>방향 버튼</strong>: teleop 속도 제어 (체크박스로 활성화)</li>
<li><strong>하단</strong>: Raspberry Pi Camera 실시간 영상 프리뷰</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5082baac-f086-4180-af89-66c357d551ad/image.png" /></p>
<hr />
<h2 id="2-opencv-4120-소스-빌드">2. OpenCV 4.12.0 소스 빌드</h2>
<p>LiDAR 데이터 처리와 카메라 영상 변환에 OpenCV가 필요합니다. 시스템 패키지로 설치된 OpenCV는 ROS2 Humble 환경과 충돌이 발생할 수 있으므로 소스에서 직접 빌드합니다.</p>
<h3 id="2-1-기존-opencv-제거">2-1. 기존 OpenCV 제거</h3>
<pre><code class="language-bash">sudo apt-get purge libopencv* python-opencv
sudo apt-get autoremove
sudo find /usr/local -name &quot;*opencv*&quot; -exec rm -rf {} \;</code></pre>
<h3 id="2-2-의존성-설치">2-2. 의존성 설치</h3>
<pre><code class="language-bash">sudo apt update &amp;&amp; sudo apt upgrade
sudo apt install build-essential cmake git pkg-config \
  libjpeg-dev libtiff-dev libpng-dev libavcodec-dev \
  libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev \
  libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
  python3-dev python3-numpy</code></pre>
<h3 id="2-3-소스-다운로드-및-빌드">2-3. 소스 다운로드 및 빌드</h3>
<pre><code class="language-bash">mkdir openCV &amp;&amp; cd openCV
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.12.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.12.0.zip
unzip opencv.zip
unzip opencv_contrib.zip

cd opencv-4.12.0
mkdir build &amp;&amp; cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D WITH_TBB=OFF \
      -D WITH_IPP=OFF \
      -D BUILD_DOCS=OFF \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D BUILD_EXAMPLES=OFF \
      -D WITH_QT=OFF \
      -D WITH_GTK=ON \
      -D WITH_OPENGL=ON \
      -D BUILD_opencv_python3=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.12.0/modules \
      -D WITH_V4L=ON \
      -D WITH_FFMPEG=ON \
      -D WITH_XINE=ON \
      -D BUILD_NEW_PYTHON_SUPPORT=ON \
      -D OPENCV_SKIP_PYTHON_LOADER=ON \
      -D OPENCV_GENERATE_PKGCONFIG=ON ..

make -j4          # 약 35분 소요
sudo make install
sudo ldconfig
opencv_version    # 설치 확인</code></pre>
<blockquote>
<p><code>make -j4</code>는 코어 수에 따라 시간이 상당히 소요됩니다. 완료 후 <code>opencv_version</code> 명령으로 <code>4.12.0</code>이 출력되면 정상입니다.</p>
</blockquote>
<hr />
<h2 id="3-패키지-구조">3. 패키지 구조</h2>
<p><code>teleop_bat_amcl_nav2_qt</code>는 이전 패키지에서 <code>RosNodeLidarCam</code> 클래스를 추가한 구조입니다.</p>
<pre><code>src/teleop_bat_amcl_nav2_qt/
├── main.cpp
├── mainwidget.cpp / mainwidget.h / mainwidget.ui
├── rosnode.cpp / rosnode.h           ← teleop + battery + amcl_pose
├── rosnode_action.cpp / rosnode_action.h  ← Nav2 Action Client
└── rosnode_lidar_cam.cpp / rosnode_lidar_cam.h  ← LiDAR + 카메라 (신규)</code></pre><p><code>package.xml</code>에 추가된 의존성입니다.</p>
<pre><code class="language-xml">&lt;depend&gt;opencv&lt;/depend&gt;
&lt;depend&gt;cv_bridge&lt;/depend&gt;
&lt;depend&gt;image_transport&lt;/depend&gt;</code></pre>
<hr />
<h2 id="4-rosnodelidarcam-클래스-설계">4. RosNodeLidarCam 클래스 설계</h2>
<h3 id="4-1-헤더-파일-rosnode_lidar_camh">4-1. 헤더 파일 (rosnode_lidar_cam.h)</h3>
<p>LiDAR 구독자, 카메라 구독자, Qt <code>QLabel</code> 포인터를 멤버로 갖습니다.</p>
<pre><code class="language-cpp">#ifndef ROSNODE_LIDAR_CAM_H
#define ROSNODE_LIDAR_CAM_H

#include &lt;QWidget&gt;
#include &lt;QTimer&gt;
#include &lt;QLabel&gt;
#include &lt;chrono&gt;
#include &quot;rclcpp/rclcpp.hpp&quot;
#include &quot;sensor_msgs/msg/laser_scan.hpp&quot;
#include &lt;image_transport/image_transport.hpp&gt;
#include &lt;opencv2/highgui/highgui.hpp&gt;
#include &lt;cv_bridge/cv_bridge.h&gt;

class RosNodeLidarCam : public QWidget
{
    Q_OBJECT

private:
    rclcpp::Node::SharedPtr node_lidar_cam;
    rclcpp::Subscription&lt;sensor_msgs::msg::LaserScan&gt;::SharedPtr subscription_lidar;
    void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg);

    rclcpp::Subscription&lt;sensor_msgs::msg::Image&gt;::SharedPtr subscription_cam;
    void image_callback(const sensor_msgs::msg::Image::SharedPtr msg) const;

public:
    explicit RosNodeLidarCam(QWidget *parent = nullptr);
    ~RosNodeLidarCam();
    QLabel* pLcamView;
    rclcpp::Node::SharedPtr getNode();

signals:
    void ldsReceiveSig(float *);

private slots:
    void OnTimerCallbackFunc(void);
};

#endif // ROSNODE_LIDAR_CAM_H</code></pre>
<h3 id="4-2-구현-파일-rosnode_lidar_camcpp">4-2. 구현 파일 (rosnode_lidar_cam.cpp)</h3>
<p>생성자에서 LiDAR와 카메라 구독자를 모두 초기화합니다.</p>
<pre><code class="language-cpp">RosNodeLidarCam::RosNodeLidarCam(QWidget *parent)
    : QWidget{parent}
{
    auto sensor_qos = rclcpp::QoS(rclcpp::SensorDataQoS());
    node_lidar_cam = rclcpp::Node::make_shared(&quot;lidar_cam_qt&quot;);

    // LiDAR 구독
    subscription_lidar = node_lidar_cam-&gt;create_subscription&lt;sensor_msgs::msg::LaserScan&gt;(
        &quot;scan&quot;,
        sensor_qos,
        std::bind(&amp;RosNodeLidarCam::scan_callback, this, std::placeholders::_1));

    // 카메라 구독
    subscription_cam = node_lidar_cam-&gt;create_subscription&lt;sensor_msgs::msg::Image&gt;(
        &quot;/camera/image_raw&quot;,
        10,
        std::bind(&amp;RosNodeLidarCam::image_callback, this, std::placeholders::_1));

    RCLCPP_INFO(node_lidar_cam-&gt;get_logger(), &quot;LidarCam Node has started.&quot;);

    QTimer *pQTimer = new QTimer(this);
    connect(pQTimer, SIGNAL(timeout()), this, SLOT(OnTimerCallbackFunc()));
    pQTimer-&gt;start(100);
}</code></pre>
<hr />
<h2 id="5-lidar-거리-데이터-처리">5. LiDAR 거리 데이터 처리</h2>
<p><code>/scan</code> 토픽의 <code>ranges</code> 배열에서 4방향(0°/90°/180°/270°) 값을 추출합니다. 배열 인덱스와 실제 각도의 관계는 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th>방향</th>
<th>인덱스</th>
</tr>
</thead>
<tbody><tr>
<td>0° (정면)</td>
<td>0</td>
</tr>
<tr>
<td>90° (좌측)</td>
<td>90</td>
</tr>
<tr>
<td>180° (후방)</td>
<td>180</td>
</tr>
<tr>
<td>270° (우측)</td>
<td>270</td>
</tr>
</tbody></table>
<pre><code class="language-cpp">void RosNodeLidarCam::scan_callback(
    const sensor_msgs::msg::LaserScan::SharedPtr msg)
{
    float scanData[4];
    scanData[0] = msg-&gt;ranges[0];    // 0°
    scanData[1] = msg-&gt;ranges[90];   // 90°
    scanData[2] = msg-&gt;ranges[180];  // 180°
    scanData[3] = msg-&gt;ranges[270];  // 270°

    emit ldsReceiveSig(scanData);
}</code></pre>
<p><code>MainWidget</code>에서 시그널을 받아 LCD에 표시합니다.</p>
<pre><code class="language-cpp">void MainWidget::ldsReceiveSlot(float *pScanData)
{
    ui-&gt;pLNangle0-&gt;display(pScanData[0]);
    ui-&gt;pLNangle90-&gt;display(pScanData[1]);
    ui-&gt;pLNangle180-&gt;display(pScanData[2]);
    ui-&gt;pLNangle270-&gt;display(pScanData[3]);
}</code></pre>
<hr />
<h2 id="6-카메라-영상-처리--image_transport--cv_bridge">6. 카메라 영상 처리 — image_transport / cv_bridge</h2>
<p>Raspberry Pi Camera Module 2는 <code>/camera/image_raw</code> 토픽으로 영상을 퍼블리시합니다.</p>
<blockquote>
<p>로컬 웹캠(<code>v4l2_camera</code>)은 <code>/image_raw</code>로 퍼블리시하므로 토픽명이 다릅니다. 코드에서 <code>/camera/image_raw</code>를 구독하면 로봇의 picam이 켜져 있을 때만 정상 수신됩니다.</p>
</blockquote>
<pre><code class="language-cpp">void RosNodeLidarCam::image_callback(
    const sensor_msgs::msg::Image::SharedPtr msg) const
{
    cv::Mat frame;
    try {
        frame = cv_bridge::toCvShare(msg, &quot;bgr8&quot;)-&gt;image;
        imwrite(&quot;cap.jpg&quot;, frame);
    } catch (cv_bridge::Exception&amp; e) {
        RCLCPP_ERROR(node_lidar_cam-&gt;get_logger(),
                     &quot;Could not convert image: %s&quot;, e.what());
        return;
    }

    // 십자선 그리기
    cv::line(frame,
             cv::Point(frame.cols &gt;&gt; 1, 20),
             cv::Point(frame.cols &gt;&gt; 1, frame.rows - 20),
             cv::Scalar(0, 255, 0), 1);
    cv::line(frame,
             cv::Point(20, frame.rows &gt;&gt; 1),
             cv::Point(frame.cols - 20, frame.rows &gt;&gt; 1),
             cv::Scalar(0, 255, 0), 1);

    // Qt QLabel에 표시
    cvtColor(frame, frame, cv::COLOR_BGR2RGB);
    QImage* pImage = new QImage(
        frame.data, frame.cols, frame.rows, QImage::Format_RGB888);
    QImage repImage = pImage-&gt;scaled(
        pLcamView-&gt;height(), pLcamView-&gt;width(), Qt::KeepAspectRatio);
    pLcamView-&gt;setPixmap(QPixmap::fromImage(repImage));
}</code></pre>
<hr />
<h2 id="7-mainwidget에서-통합-연결">7. MainWidget에서 통합 연결</h2>
<p><code>mainwidget.cpp</code> 생성자에서 세 RosNode 객체를 생성하고 시그널-슬롯을 연결합니다.</p>
<pre><code class="language-cpp">MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
{
    ui-&gt;setupUi(this);
    pRosNode = new RosNode(this);
    pRosNodeAction = new RosNodeAction(this);
    pRosNodeLidarCam = new RosNodeLidarCam(this);
    pRosNodeLidarCam-&gt;pLcamView = ui-&gt;gridLayout;  // QLabel 연결

    connect(pRosNode, SIGNAL(batteryLcdDisplaySig(double, double)),
            this, SLOT(batteryLcdDisplaySlot(double, double)));

    connect(pRosNode, SIGNAL(amclposeLcdDisplaySig(
                const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr)),
            this, SLOT(amclposeLcdDisplaySlot(...)));

    connect(pRosNodeLidarCam, SIGNAL(ldsReceiveSig(float*)),
            this, SLOT(ldsReceiveSlot(float*)));
}</code></pre>
<hr />
<h2 id="8-cmakeliststxt-최종-구성">8. CMakeLists.txt 최종 구성</h2>
<pre><code class="language-cmake">find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(OpenCV REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(Qt6 REQUIRED COMPONENTS Widgets Core Gui)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

add_executable(teleop_bat_amcl_nav2_qt
    src/teleop_bat_amcl_nav2_qt/main.cpp
    src/teleop_bat_amcl_nav2_qt/mainwidget.cpp
    src/teleop_bat_amcl_nav2_qt/mainwidget.h
    src/teleop_bat_amcl_nav2_qt/mainwidget.ui
    src/teleop_bat_amcl_nav2_qt/rosnode.cpp
    src/teleop_bat_amcl_nav2_qt/rosnode.h
    src/teleop_bat_amcl_nav2_qt/rosnode_action.cpp
    src/teleop_bat_amcl_nav2_qt/rosnode_action.h
    src/teleop_bat_amcl_nav2_qt/rosnode_lidar_cam.cpp
    src/teleop_bat_amcl_nav2_qt/rosnode_lidar_cam.h
)
ament_target_dependencies(teleop_bat_amcl_nav2_qt
    rclcpp geometry_msgs sensor_msgs
    rclcpp_action nav2_msgs
    cv_bridge image_transport
)
target_include_directories(teleop_bat_amcl_nav2_qt PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${OpenCV_INCLUDE_DIRS}
)
target_link_libraries(teleop_bat_amcl_nav2_qt
    Qt6::Widgets
    ${OpenCV_LIBS}
)

install(TARGETS teleop_bat_amcl_nav2_qt
    DESTINATION lib/${PROJECT_NAME})</code></pre>
<hr />
<h2 id="9-빌드-및-실행">9. 빌드 및 실행</h2>
<pre><code class="language-bash"># OpenCV 라이브러리 경로 설정 (필요 시)
export LD_LIBRARY_PATH=/opt/ros/humble/lib:$LD_LIBRARY_PATH

cd ~/robot_ws
colcon build --packages-select kccistc_ros2_qt \
  --cmake-args -DOpenCV_DIR=/usr/local/lib/cmake/opencv4
source install/setup.bash
ros2 run kccistc_ros2_qt teleop_bat_amcl_nav2_qt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a6285d7c-6d8d-4022-b43e-a80f048eedf3/image.png" /></p>
<hr />
<h2 id="정리">정리</h2>
<p>이번 글에서는 OpenCV 소스 빌드부터 시작하여 LiDAR 4방향 거리 데이터와 Raspberry Pi Camera Module 2 영상을 Qt GUI에 통합하는 전 과정을 정리해보았습니다. <code>RosNodeLidarCam</code>을 독립 클래스로 분리하여 기존 <code>RosNode</code>, <code>RosNodeAction</code>과 함께 <code>MainWidget</code>에서 시그널-슬롯으로 연결하는 구조가 핵심이었습니다. 토픽명 불일치(<code>/image_raw</code> vs <code>/camera/image_raw</code>) 문제처럼 실제 하드웨어와 연동할 때 발생하는 디버깅 포인트도 기억해두면 도움이 될 것입니다.</p>