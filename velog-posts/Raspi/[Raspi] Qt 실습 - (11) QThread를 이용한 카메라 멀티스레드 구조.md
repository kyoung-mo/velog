<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bc1b23c3-c28b-478a-a4d9-9a8b381adac8/image.gif" />
(10) 실습하고 비교 시 UI 속도가 상대적으로 빠른 것을 확인할 수 있다.</p>
<hr />
<p><strong>핵심 개념:</strong> QTimer 방식은 GUI 스레드에서 영상 처리까지 다 하기 때문에 무거운 필터 연산 시 화면이 멈춤(Freezing).<br />워커 스레드(<code>CameraThread</code>)에서 캡처 + 필터링 + QImage 변환을 전담하고, 완성된 이미지만 시그널로 GUI에 전달하는 구조가 표준.</p>
<hr />
<h2 id="전체-구조">전체 구조</h2>
<pre><code>[CameraThread - 워커 스레드]               [MainWindow - GUI 스레드]
  cap &gt;&gt; frame                                 
  → 필터 적용 (blur/sharpen/edge)              
  → BGR → RGB 변환                            
  → QImage 변환                               
  → emit frameReady(qImg.copy())  ─시그널→  updateUI() → QLabel에 렌더링</code></pre><hr />
<h2 id="파일-구조-3개">파일 구조 3개</h2>
<h3 id="①-camerathreadh-워커-스레드-헤더">① camerathread.h (워커 스레드 헤더)</h3>
<ul>
<li><code>QThread</code>를 상속받아 <code>run()</code> 오버라이드</li>
<li>스레드 간 공유 변수는 <code>std::atomic&lt;bool&gt;</code>로 선언 → 레이스 컨디션 방지</li>
<li><code>frameReady(const QImage &amp;image)</code> 시그널로 GUI에 프레임 전달<pre><code class="language-cpp">std::atomic m_running;   // 스레드 실행 제어
std::atomic m_blur;      // 필터 상태 (GUI에서 체크박스로 제어)
std::atomic m_sharpen;
std::atomic m_edge;</code></pre>
</li>
</ul>
<h3 id="②-camerathreadcpp-워커-스레드-구현">② camerathread.cpp (워커 스레드 구현)</h3>
<p><strong>run() 내부 흐름:</strong></p>
<pre><code>GStreamer 파이프라인으로 카메라 열기
  → while(m_running) 무한 루프
      → cap &gt;&gt; frame  (프레임 획득)
      → 체크박스 상태에 따라 filter2D() 적용
      → cvtColor(BGR → RGB)
      → QImage 변환
      → emit frameReady(qImg.copy())   ← 반드시 copy() !!
  → cap.release()</code></pre><p><strong>3x3 필터 커널:</strong></p>
<table>
<thead>
<tr>
<th>필터</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td><code>kernelBlur</code></td>
<td>평균 블러 (모든 값 1/9)</td>
</tr>
<tr>
<td><code>kernelSharpen</code></td>
<td>샤프닝 (중앙값 5, 주변 -1)</td>
</tr>
<tr>
<td><code>kernelEdge</code></td>
<td>라플라시안 엣지 검출</td>
</tr>
</tbody></table>
<h3 id="③-mainwindowcpp-gui-스레드">③ mainwindow.cpp (GUI 스레드)</h3>
<ul>
<li>생성자에서 <code>CameraThread</code> 생성 후 <code>start()</code></li>
<li>시그널-슬롯 연결 3가지:<ul>
<li><code>frameReady</code> → <code>updateUI()</code> : 프레임 화면 갱신</li>
<li><code>chkBlur/chkSharpen/chkEdge toggled</code> → <code>updateFilters()</code> : 필터 상태 스레드에 전달</li>
<li><code>btnSave clicked</code> → <code>saveImage()</code> : 현재 프레임 PNG 저장<pre><code class="language-cpp">// 소멸자에서 반드시 이 순서로 정리
m_thread-&gt;stop();   // m_running = false → 루프 탈출 유도
m_thread-&gt;wait();   // 스레드가 완전히 종료될 때까지 대기</code></pre>
</li>
</ul>
</li>
</ul>
<hr />
<h3 id="전체-코드">전체 코드</h3>
<p><strong>1. CMakeLists.txt</strong></p>
<pre><code class="language-c">cmake_minimum_required(VERSION 3.16)

project(CameraFilterApp VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)
find_package(Qt6 COMPONENTS Widgets Core Gui REQUIRED)
find_package(OpenCV REQUIRED)

set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        mainwindow.h
        mainwindow.ui
)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(CameraFilterApp
        MANUAL_FINALIZATION
        ${PROJECT_SOURCES}
        camerathread.h
        camerathread.cpp
        camerathread.cpp
        camerathread.cpp
    )
# Define target properties for Android with Qt 6 as:
#    set_property(TARGET CameraFilterApp APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
#                 ${CMAKE_CURRENT_SOURCE_DIR}/android)
# For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation
else()
    if(ANDROID)
        add_library(CameraFilterApp SHARED
            ${PROJECT_SOURCES}
        )
# Define properties for Android with Qt 5 after find_package() calls as:
#    set(ANDROID_PACKAGE_SOURCE_DIR &quot;${CMAKE_CURRENT_SOURCE_DIR}/android&quot;)
    else()
        add_executable(CameraFilterApp
            ${PROJECT_SOURCES}
        )
    endif()
endif()

# 6. 헤더 파일 경로 포함 및 의존성 라이브러리 링킹
target_include_directories(${PROJECT_NAME} PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Widgets
    Qt6::Core
    Qt6::Gui
    ${OpenCV_LIBS}
)
target_link_libraries(CameraFilterApp PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
if(${QT_VERSION} VERSION_LESS 6.1.0)
  set(BUNDLE_ID_OPTION MACOSX_BUNDLE_GUI_IDENTIFIER com.example.CameraFilterApp)
endif()
set_target_properties(CameraFilterApp PROPERTIES
    ${BUNDLE_ID_OPTION}
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

include(GNUInstallDirs)
install(TARGETS CameraFilterApp
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(CameraFilterApp)
endif()</code></pre>
<p><strong>2. camerathread.h</strong></p>
<pre><code class="language-c">#ifndef CAMERATHREAD_H
#define CAMERATHREAD_H

#include &lt;QThread&gt;
#include &lt;QImage&gt;
#include &lt;opencv2/opencv.hpp&gt;
#include &lt;atomic&gt;

class CameraThread : public QThread
{
    Q_OBJECT

public:
    explicit CameraThread(QObject *parent = nullptr);
    ~CameraThread();

    void run() override; // 실제 스레드가 도는 무한 루프
    void stop();         // 스레드 안전 종료

    // GUI에서 체크박스 상태를 전달받을 함수
    void setFilters(bool blur, bool sharpen, bool edge);

signals:
    // 처리가 완료된 프레임을 Main UI로 쏘아보내는 시그널
    void frameReady(const QImage &amp;image);

private:
    std::atomic&lt;bool&gt; m_running;
    std::atomic&lt;bool&gt; m_blur;
    std::atomic&lt;bool&gt; m_sharpen;
    std::atomic&lt;bool&gt; m_edge;
};

#endif // CAMERATHREAD_H</code></pre>
<p><strong>3. mainwindow.h</strong></p>
<pre><code class="language-c">#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include &lt;QMainWindow&gt;
#include &lt;QImage&gt;
#include &lt;QMainWindow&gt;
#include &lt;QTimer&gt;
#include &lt;QLabel&gt;
#include &lt;QCheckBox&gt;
#include &lt;QPushButton&gt;
#include &lt;QVBoxLayout&gt;
#include &lt;QHBoxLayout&gt;
#include &lt;opencv2/opencv.hpp&gt;
#include &quot;camerathread.h&quot;

// 1. 전방 선언 (Forward Declarations)
// 헤더 파일 간의 꼬임을 방지하고 컴파일 속도를 높이기 위해 사용함
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class CameraThread; // 워커 스레드 클래스가 존재함을 컴파일러에 알림

// 2. 메인 윈도우 클래스
class MainWindow : public QMainWindow
{
    Q_OBJECT // Qt의 시그널-슬롯 메커니즘을 사용하기 위한 필수 매크로

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    // 워커 스레드의 frameReady 시그널을 받아 화면을 갱신하는 슬롯
    void updateUI(const QImage &amp;image);

    // 체크박스(Blur, Sharpen, Edge) 클릭 시 상태를 스레드에 전달하는 슬롯
    void updateFilters();

    // 저장 버튼 클릭 시 현재 프레임을 파일로 저장하는 슬롯
    void saveImage();

private:
    Ui::MainWindow *ui;         // Qt Designer UI 위젯 접근용 포인터
    CameraThread *m_thread;     // 카메라 캡처 및 처리를 전담할 워커 스레드
    QImage m_currentImage;      // 현재 화면에 표시된 이미지를 저장하기 위한 백업 변수
};

#endif // MAINWINDOW_H</code></pre>
<p><strong>4. camerathread.cpp</strong></p>
<pre><code class="language-c">#include &quot;camerathread.h&quot;

CameraThread::CameraThread(QObject *parent)
    : QThread(parent), m_running(false), m_blur(false), m_sharpen(false), m_edge(false) {}

CameraThread::~CameraThread() {
    stop();
    wait(); // 스레드가 완전히 죽을 때까지 대기
}

void CameraThread::stop() {
    m_running = false;
}

void CameraThread::setFilters(bool blur, bool sharpen, bool edge) {
    m_blur = blur;
    m_sharpen = sharpen;
    m_edge = edge;
}

void CameraThread::run() {
    m_running = true;

    std::string pipeline = &quot;v4l2src device=/dev/video0 ! &quot;
                           &quot;video/x-raw, width=320, height=240, framerate=30/1 ! &quot;
                           &quot;videoconvert ! video/x-raw, format=BGR ! &quot;
                           &quot;appsink drop=true max-buffers=1&quot;;

    cv::VideoCapture cap(pipeline, cv::CAP_GSTREAMER);
    if (!cap.isOpened()) return;

    // 3x3 필터 커널
    cv::Mat kernelBlur;
    cv::Mat kernelSharpen;
    cv::Mat kernelEdge;
    // 2. 3x3 필터 커널 (행렬식) 초기화
    // 평균 블러 필터
    kernelBlur = (cv::Mat_&lt;float&gt;(3, 3) &lt;&lt;
                      1/9.f, 1/9.f, 1/9.f,
                  1/9.f, 1/9.f, 1/9.f,
                  1/9.f, 1/9.f, 1/9.f);

    // 샤프닝 필터
    kernelSharpen = (cv::Mat_&lt;float&gt;(3, 3) &lt;&lt;
                         0.f, -1.f,  0.f,
                     -1.f,  5.f, -1.f,
                     0.f, -1.f,  0.f);

    // 라플라시안 엣지 검출 필터
    kernelEdge = (cv::Mat_&lt;float&gt;(3, 3) &lt;&lt;
                      0.f,  1.f,  0.f,
                  1.f, -4.f,  1.f,
                  0.f,  1.f,  0.f);

    cv::Mat frame, processed;
    while (m_running) {
        cap &gt;&gt; frame;
        if (frame.empty()) continue;

        processed = frame.clone();

        // 1. 알고리즘 연산 (체크박스 상태에 따라 필터 적용)
        if (m_blur) {
            cv::filter2D(processed, processed, -1, kernelBlur);
            //cv::GaussianBlur(processed, processed, cv::Size(7, 7), 0);
        }
        if (m_sharpen) {
            cv::filter2D(processed, processed, -1, kernelSharpen);
            //cv::Mat kernel = (cv::Mat_&lt;float&gt;(3,3) &lt;&lt; 0, -1, 0, -1, 5, -1, 0, -1, 0);
            //cv::filter2D(processed, processed, processed.depth(), kernel);
        }
        if (m_edge) {
            cv::filter2D(processed, processed, -1, kernelEdge);
            //cv::Canny(processed, processed, 50, 150);
            //cv::cvtColor(processed, processed, cv::COLOR_GRAY2BGR); // QImage 변환을 위해 채널 복구
        }

        // 2. QImage 변환 (BGR -&gt; RGB)
        cv::Mat rgb;
        cv::cvtColor(processed, rgb, cv::COLOR_BGR2RGB);
        QImage qImg(rgb.data, rgb.cols, rgb.rows, rgb.step, QImage::Format_RGB888);

        // 3. 시그널 전송 (반드시 copy()를 호출하여 Deep Copy로 넘겨야 메모리 충돌 안 남 🔥)
        emit frameReady(qImg.copy());
    }
    cap.release();
}</code></pre>
<p><strong>5. mainwindow.cpp</strong></p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;./ui_mainwindow.h&quot;
#include &lt;QDateTime&gt;
#include &lt;QDebug&gt;
#include &lt;QMessageBox&gt;
#include &quot;camerathread.h&quot;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui-&gt;setupUi(this);

    // 1. 동적 UI 생성 및 배치
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    ui-&gt;lblCamera = new QLabel(&quot;카메라 대기중...&quot;, this);
    ui-&gt;lblCamera-&gt;setMinimumSize(320, 240);
    ui-&gt;lblCamera-&gt;setAlignment(Qt::AlignCenter);

    ui-&gt;chkBlur = new QCheckBox(&quot;1. 흐림 (Blur 3x3)&quot;, this);
    ui-&gt;chkSharpen = new QCheckBox(&quot;2. 선명하게 (Sharpen 3x3)&quot;, this);
    ui-&gt;chkEdge = new QCheckBox(&quot;3. 윤곽선 (Edge 3x3)&quot;, this);
    ui-&gt;btnSave = new QPushButton(&quot;현재 이미지 저장 (.png)&quot;, this);

    QVBoxLayout *ctrlLayout = new QVBoxLayout();
    ctrlLayout-&gt;addWidget(ui-&gt;chkBlur);
    ctrlLayout-&gt;addWidget(ui-&gt;chkSharpen);
    ctrlLayout-&gt;addWidget(ui-&gt;chkEdge);
    ctrlLayout-&gt;addStretch();
    ctrlLayout-&gt;addWidget(ui-&gt;btnSave);

    QHBoxLayout *mainLayout = new QHBoxLayout(centralWidget);
    mainLayout-&gt;addWidget(ui-&gt;lblCamera, 1);
    mainLayout-&gt;addLayout(ctrlLayout);

    // 스레드 객체 생성 및 시그널-슬롯 연결
    m_thread = new CameraThread(this);
    connect(m_thread, &amp;CameraThread::frameReady, this, &amp;MainWindow::updateUI);

    // 체크박스 상태 변경 시 스레드로 상태 전달
    connect(ui-&gt;chkBlur, &amp;QCheckBox::toggled, this, &amp;MainWindow::updateFilters);
    connect(ui-&gt;chkSharpen, &amp;QCheckBox::toggled, this, &amp;MainWindow::updateFilters);
    connect(ui-&gt;chkEdge, &amp;QCheckBox::toggled, this, &amp;MainWindow::updateFilters);

    // 저장 버튼 클릭 이벤트
    connect(ui-&gt;btnSave, &amp;QPushButton::clicked, this, &amp;MainWindow::saveImage);

    // 워커 스레드 시작
    m_thread-&gt;start();



}

MainWindow::~MainWindow()
{
    m_thread-&gt;stop();
    m_thread-&gt;wait();

    delete ui;
}
// 스레드에서 온 이미지를 QLabel에 그리기
void MainWindow::updateUI(const QImage &amp;image) {
    m_currentImage = image; // 저장을 위해 멤버 변수에 백업
    ui-&gt;lblCamera-&gt;setPixmap(QPixmap::fromImage(image));
}

// 체크박스 상태를 읽어서 스레드의 원자적 변수 갱신
void MainWindow::updateFilters() {
    m_thread-&gt;setFilters(
        ui-&gt;chkBlur-&gt;isChecked(),
        ui-&gt;chkSharpen-&gt;isChecked(),
        ui-&gt;chkEdge-&gt;isChecked()
        );
}

// 현재 시간으로 파일 저장
void MainWindow::saveImage() {
    if (m_currentImage.isNull()) return;

    QString fileName = QDateTime::currentDateTime().toString(&quot;yyyyMMdd_HHmmss&quot;) + &quot;.png&quot;;
    m_currentImage.save(fileName, &quot;PNG&quot;);
    // ui-&gt;statusbar-&gt;showMessage(fileName + &quot; 저장 완료!&quot;, 3000); // 상태 표시줄 알림
}</code></pre>
<h2 id="핵심-주의사항">핵심 주의사항</h2>
<table>
<thead>
<tr>
<th>포인트</th>
<th>이유</th>
</tr>
</thead>
<tbody><tr>
<td><code>emit frameReady(qImg.copy())</code></td>
<td>QImage는 cv::Mat 메모리를 참조만 함. 루프가 돌면 덮어씌워져 화면 깨짐 → Deep Copy 필수</td>
</tr>
<tr>
<td><code>wait()</code> 호출</td>
<td>종료 시 워커 스레드가 루프를 다 빠져나오기 전에 메모리 해제되면 Segmentation Fault 발생</td>
</tr>
<tr>
<td><code>atomic&lt;bool&gt;</code> 사용</td>
<td>두 스레드가 동시에 같은 변수를 읽고 쓸 때 레이스 컨디션 방지</td>
</tr>
<tr>
<td><code>m_currentImage</code> 백업</td>
<td><code>saveImage()</code>에서 현재 프레임을 파일로 저장하기 위해 GUI 스레드에 복사본 유지</td>
</tr>
</tbody></table>