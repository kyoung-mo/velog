<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a7aed161-898a-4d12-ac96-6f6abf0ac2d6/image.gif" /></p>
<h2 id="cvimshow-대신-qt에-카메라-영상-임베딩하기">cv::imshow() 대신 Qt에 카메라 영상 임베딩하기</h2>
<p><strong>핵심 개념:</strong> <code>cv::imshow()</code>는 OpenCV가 별도 OS 창을 띄우기 때문에 Qt UI 안에 넣을 수 없음.<br />대신 <code>cv::Mat → QImage → QPixmap → QLabel</code> 파이프라인으로 Qt 위젯 안에 직접 렌더링해야 함.</p>
<hr />
<h2 id="전체-흐름">전체 흐름</h2>
<h3 id="①-ui-준비-qt-designer">① UI 준비 (Qt Designer)</h3>
<ul>
<li><code>QVBoxLayout</code> 안에 <code>QLabel</code> 배치</li>
<li><code>QLabel</code> objectName을 <code>labelCamera</code>로 설정, 크기는 320x240</li>
</ul>
<h3 id="②-카메라-열기">② 카메라 열기</h3>
<p>GStreamer 파이프라인으로 <code>cv::VideoCapture</code>를 열고, 실패 시 레이블에 에러 텍스트 출력</p>
<h3 id="③-qtimer로-루프-구성">③ QTimer로 루프 구성</h3>
<p>33ms 주기(<code>≈30FPS</code>)로 <code>updateFrame()</code> 슬롯을 반복 호출</p>
<h3 id="④-updateframe-핵심-로직">④ updateFrame() 핵심 로직</h3>
<pre><code>GStreamer → cv::Mat (BGR)
    → cvtColor(BGR → RGB)       # 색상 채널 순서 맞추기
    → QImage(Format_RGB888)     # Qt 이미지 타입으로 변환
    → QPixmap::fromImage()      # 위젯에 표시 가능한 형태로
    → labelCamera-&gt;setPixmap()  # QLabel에 최종 렌더링</code></pre><hr />
<h2 id="주의사항-3가지">주의사항 3가지</h2>
<table>
<thead>
<tr>
<th>이슈</th>
<th>원인</th>
<th>해결</th>
</tr>
</thead>
<tbody><tr>
<td>스머프 현상(색 반전)</td>
<td>BGR을 RGB로 안 바꾸고 QImage에 넣음</td>
<td><code>cvtColor(BGR2RGB)</code> 필수</td>
</tr>
<tr>
<td>창 리사이즈 시 영상 안 늘어남</td>
<td>기본값은 고정 크기</td>
<td><code>setScaledContents(true)</code> 설정</td>
</tr>
<tr>
<td>메모리 누수 우려</td>
<td>QImage는 Mat 포인터를 참조만 함</td>
<td><code>fromImage()</code> 시점에 내부 복사 → 누수 없음</td>
</tr>
</tbody></table>
<hr />
<h2 id="핵심-멤버-변수-mainwindowh">핵심 멤버 변수 (mainwindow.h)</h2>
<pre><code class="language-cpp">cv::VideoCapture m_capture;  // GStreamer 파이프라인 캡처 객체
QTimer *m_timer;             // 주기적 프레임 갱신용 타이머</code></pre>
<blockquote>
<p><code>CMakeLists.txt</code>에는 <code>find_package(OpenCV REQUIRED)</code>와  
<code>target_link_libraries</code>에 <code>${OpenCV_LIBS}</code> 추가 필요.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2f2d25cd-5be1-424d-8600-e09d95531ffc/image.png" /></p>
<p><code>build/Deesktop-Debug</code> 위치에서 사진 저장 되는 것을 확인해볼 수 있다.</p>
<p><strong>1. CMakeLists.txt</strong></p>
<pre><code class="language-c">cmake_minimum_required(VERSION 3.16)
project(CameraFilterApp)

# 1. C++ 17 표준 지정 (Qt6 및 최신 OpenCV 권장)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 2. Qt 자동 빌드 시스템 활성화
set(CMAKE_AUTOMOC ON) # Q_OBJECT 매크로를 위한 메타 객체 자동 컴파일
set(CMAKE_AUTOUIC ON) # Qt Designer의 .ui 파일을 ui_*.h C++ 코드로 자동 변환
set(CMAKE_AUTORCC ON) # .qrc 리소스 파일 자동 변환

# 3. 필수 라이브러리 패키지 검색
# GUI 처리를 위한 Qt6와 영상 처리를 위한 OpenCV를 시스템에서 찾습니다.
find_package(Qt6 COMPONENTS Widgets Core Gui REQUIRED)
find_package(OpenCV REQUIRED)

# 4. 소스 파일 목록 정의 (실제 파일명에 맞게 수정 필수)
set(SOURCE_FILES
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
    # 카메라 캡처를 워커 스레드로 분리했다면 아래 주석을 해제하고 추가하세요
    # camerathread.cpp
    # camerathread.h
)

# 5. 실행 파일 타겟 생성
add_executable(${PROJECT_NAME} ${SOURCE_FILES})

# 6. 헤더 파일 경로 포함 및 의존성 라이브러리 링킹
target_include_directories(${PROJECT_NAME} PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Widgets
    Qt6::Core
    Qt6::Gui
    ${OpenCV_LIBS}
)</code></pre>
<p><strong>2. mainwindow.h</strong></p>
<pre><code class="language-c">#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include &lt;QMainWindow&gt;
#include &lt;QTimer&gt;
#include &lt;QLabel&gt;
#include &lt;QCheckBox&gt;
#include &lt;QPushButton&gt;
#include &lt;QVBoxLayout&gt;
#include &lt;QHBoxLayout&gt;
#include &lt;opencv2/opencv.hpp&gt;

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
private slots:
    void updateFrame();
    void saveImage();

private:
    // UI 요소
    // QLabel *lblCamera;
    // QCheckBox *chkBlur;
    // QCheckBox *chkSharpen;
    // QCheckBox *chkEdge;
    // QPushButton *btnSave;

    // 카메라 및 데이터
    QTimer *timer;
    cv::VideoCapture capture;
    cv::Mat currentProcessedFrame; // 저장을 위해 현재 프레임 유지

    // 3x3 필터 커널
    cv::Mat kernelBlur;
    cv::Mat kernelSharpen;
    cv::Mat kernelEdge;

    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H</code></pre>
<p><strong>3. mainwindow.cpp</strong></p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;./ui_mainwindow.h&quot;
#include &lt;QDateTime&gt;
#include &lt;QDebug&gt;
#include &lt;QMessageBox&gt;

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

    // 3. 시그널/슬롯 연결
    connect(ui-&gt;btnSave, &amp;QPushButton::clicked, this, &amp;MainWindow::saveImage);

    // 4. 카메라 및 타이머 시작 (USB 웹캠 0번)
    capture.open(0);
    timer = new QTimer(this);
    connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::updateFrame);
    if (capture.isOpened()) {
        timer-&gt;start(33); // 약 30FPS
    } else {
        ui-&gt;lblCamera-&gt;setText(&quot;카메라를 열 수 없습니다.&quot;);
    }
}

MainWindow::~MainWindow()
{
    if (timer-&gt;isActive()) timer-&gt;stop();
    if (capture.isOpened()) capture.release();
    delete ui;
}

void MainWindow::updateFrame()
{
    cv::Mat frame;
    capture &gt;&gt; frame;
    if (frame.empty()) return;

    // 복사본 생성하여 필터링 파이프라인 적용
    cv::Mat processed = frame.clone();

    // 체크박스 순서대로 필터 누적 적용 (filter2D)
    if (ui-&gt;chkBlur-&gt;isChecked()) {
        cv::filter2D(processed, processed, -1, kernelBlur);
    }
    if (ui-&gt;chkSharpen-&gt;isChecked()) {
        cv::filter2D(processed, processed, -1, kernelSharpen);
    }
    if (ui-&gt;chkEdge-&gt;isChecked()) {
        cv::filter2D(processed, processed, -1, kernelEdge);
    }

    // 파일 저장을 위해 클래스 멤버 변수에 최신 BGR 데이터 보관
    currentProcessedFrame = processed.clone();

    // OpenCV BGR -&gt; Qt RGB 변환
    cv::Mat rgbFrame;
    cv::cvtColor(processed, rgbFrame, cv::COLOR_BGR2RGB);

    // QImage 변환 및 화면 출력
    QImage qImg((const unsigned char*)rgbFrame.data,
                rgbFrame.cols, rgbFrame.rows, rgbFrame.step,
                QImage::Format_RGB888);

    ui-&gt;lblCamera-&gt;setPixmap(QPixmap::fromImage(qImg).scaled(
        ui-&gt;lblCamera-&gt;size(), Qt::KeepAspectRatio, Qt::FastTransformation));
}

void MainWindow::saveImage()
{
    if (currentProcessedFrame.empty()) {
        QMessageBox::warning(this, &quot;오류&quot;, &quot;저장할 이미지가 없습니다.&quot;);
        return;
    }

    // QDateTime을 이용하여 현재 시간을 지정된 포맷으로 문자열 변환
    QString currentTime = QDateTime::currentDateTime().toString(&quot;yyyyMMdd_HHmmss&quot;);
    QString fileName = currentTime + &quot;.png&quot;;

    // cv::imwrite를 사용하여 BGR 상태의 원본 그대로 무손실 PNG 저장
    if (cv::imwrite(fileName.toStdString(), currentProcessedFrame)) {
        QMessageBox::information(this, &quot;저장 완료&quot;, fileName + &quot; 파일이 저장되었습니다.&quot;);
    } else {
        QMessageBox::critical(this, &quot;저장 실패&quot;, &quot;파일 저장에 실패했습니다.&quot;);
    }
}</code></pre>