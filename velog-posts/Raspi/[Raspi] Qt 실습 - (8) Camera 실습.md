<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4fed6967-61c5-465d-94c6-e57dc744aced/image.gif" /></p>
<p>라즈베리 파이 5(RPi5)에서 카메라 영상을 Qt6 GUI 창에 띄우고 이를 윈도우에서 확인하려면, Qt Multimedia 모듈을 사용하여 <code>QVideoWidget</code>에 카메라 스트림을 연결해야 합니다.</p>
<p>일단 아래 패키지를 먼저 설치해줍니다.</p>
<pre><code class="language-bash">sudo apt update
sudo apt install qt6-multimedia-dev libqt6multimedia6 libqt6multimediawidgets6 -y</code></pre>
<p>라즈베리파이와 camera를 USB를 통해 연결해주고, CMakeLists.txt에 <code>Multimedia</code>와 <code>MultimediaWidgets</code> 모듈을 추가합니다.</p>
<p><strong>CMakeLists.txt</strong></p>
<pre><code class="language-c">find_package(Qt6 REQUIRED COMPONENTS Widgets Multimedia MultimediaWidgets)

target_link_libraries(camera_app PRIVATE 
    Qt6::Widgets 
    Qt6::Multimedia 
    Qt6::MultimediaWidgets
)</code></pre>
<p><strong>MainWindow.h</strong></p>
<pre><code class="language-c">#include &lt;QCamera&gt;
#include &lt;QMediaCaptureSession&gt;
#include &lt;QVideoWidget&gt;
#include &lt;QMainWindow&gt;
#include &lt;QMediaDevices&gt;


class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget *parent = nullptr);
private:
    QCamera *camera;
    QMediaCaptureSession *captureSession;
    QVideoWidget *videoWidget;
};</code></pre>
<h3 id="mainwindowcpp"><code>MainWindow.cpp</code></h3>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &lt;QVBoxLayout&gt;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    // 1. 카메라 및 세션 초기화
            camera = new QCamera(QMediaDevices::defaultVideoInput(), this);
    captureSession = new QMediaCaptureSession(this);
    videoWidget = new QVideoWidget(this);

    // 2. 카메라 출력을 비디오 위젯으로 설정
    captureSession-&gt;setCamera(camera);
    captureSession-&gt;setVideoOutput(videoWidget);

    // 3. 레이아웃 설정
    setCentralWidget(videoWidget);
    resize(640, 480);

    // 4. 카메라 시작
    camera-&gt;start();
}</code></pre>
<hr />
<p><strong>WayVNC</strong>는 카메라의 하드웨어 가속 영상을 비교적 잘 전달합니다.화면이 검게 나온다면 RPi5 모니터 출력 설정이 활성화되어 있어야 합니다.</p>
<ul>
<li><strong>성능 저하:</strong> X11 포워딩은 매 프레임을 네트워크로 전송하므로 매우 느리거나 화면이 깨질 수 있습니다.</li>
<li><strong>환경 변수:</strong> 실행 전 터미널에 아래 설정을 입력하여 소프트웨어 렌더링을 유도하면 화면이 뜰 확률이 높아집니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a0612638-05c9-44f3-93cc-35bce2b397c4/image.png" /></p>
<p>RPi5는 <code>/dev/video0</code> 형식이 아닌 <code>libcamera</code>를 기본으로 합니다. Qt6는 이를 지원하지만, <code>libcamerav4l2</code> 어댑터가 필요할 수도 있습니다.</p>
<hr />
<p>트러블슈팅: 화면이 검은색으로만 나올 때</p>
<ol>
<li>카메라 권한: <code>sudo usermod -aG video $USER</code> 후 재부팅</li>
<li>백엔드 강제: <code>export QT_MEDIA_BACKEND=ffmpeg</code> 또는 <code>gstreamer</code>를 입력하여 Qt가 사용하는 멀티미디어 엔진을 바꿔보기</li>
</ol>
<hr />
<h3 id="전체-화면이-아닌-위젯-크기-설정해준만큼-동작">전체 화면이 아닌, 위젯 크기 설정해준만큼 동작</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/18c6774d-9775-4713-b8b0-cba8496aa67b/image.png" /></p>
<p>카메라가 들어갈 위치에 <code>Widget</code>을 하나 배치하고, 객체 이름은 <code>videoContainer</code>으로 설정해주고, 그 위젯 안에 <code>Vertical Layout</code>을 하나 넣어주고, 객체 이름은 <code>videoLayout</code>으로 설정해줍니다.</p>
<p><strong>MainWindow.cpp 수정</strong></p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;ui_mainwindow.h&quot; // UI 파일을 사용한다면 필수
#include &lt;QMediaDevices&gt;
#include &lt;QVBoxLayout&gt;

MainWindow::MainWindow(QWidget *parent) 
    : QMainWindow(parent)
    , ui(new Ui::MainWindow) // UI 초기화
{
    ui-&gt;setupUi(this);

    // 1. 사용 가능한 비디오 입력 장치 확인
     const QList&lt;QCameraDevice&gt; cameras = QMediaDevices::videoInputs();

     if (cameras.isEmpty()) {
         qDebug() &lt;&lt; &quot;연결된 USB 카메라를 찾을 수 없습니다.&quot;;
         return;
     }

     // 2. 첫 번째 USB 카메라 선택 (보통 인덱스 0)
     camera = new QCamera(cameras.first(), this);
     captureSession = new QMediaCaptureSession(this);
     videoWidget = new QVideoWidget(this);

     // 3. 세션 연결
     captureSession-&gt;setCamera(camera);
     captureSession-&gt;setVideoOutput(videoWidget);

     //setCentralWidget(videoWidget);

     // 4. 레이아웃에 카메라 위젯 추가 (핵심)
     // ui-&gt;videoLayout은 Designer에서 미리 만들어둔 레이아웃입니다.
     ui-&gt;videoLayout-&gt;addWidget(videoWidget);

     // 5. 해상도 및 포맷 설정 (선택 사항)
     // USB 카메라의 성능에 맞춰 자동 설정되지만, 명시적으로 지정 가능합니다.

     camera-&gt;start();
}</code></pre>