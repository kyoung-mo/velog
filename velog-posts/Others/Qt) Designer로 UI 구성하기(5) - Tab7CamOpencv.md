<blockquote>
<p><a href="https://velog.io/@mommers/QtOpenCV6">이전 글 : Qt) OpenCV 빌드 및 카메라 연동 환경 구성</a></p>
</blockquote>
<p>이전 글에서 OpenCV 4.12.0을 빌드하고 <code>CamViewerThread</code> 예제로 Qt + OpenCV 카메라 연동을 확인했습니다.</p>
<p>이번 글에서는 <code>CamViewerThread</code>를 기반으로 AiotClient에 <code>Tab7CamOpencv</code> 탭을 추가하는 과정을 정리합니다.
HSV 색상 분류 기능과 소켓 송신 연동을 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7f0fa84c-aac5-431a-a8e9-612da32e0dfb/image.gif" /></p>
<hr />
<h2 id="1-aiotclient-pro-파일에-opencv-경로-추가">1. AiotClient .pro 파일에 OpenCV 경로 추가</h2>
<p>Tab7에서 <code>#include &lt;opencv2/opencv.hpp&gt;</code>를 사용하기 위해 <code>.pro</code> 파일에 OpenCV 경로를 추가합니다.
ubuntu05는 소스 빌드 설치이므로 <code>/usr/local</code> 하위 경로를 사용합니다.</p>
<pre><code>INCLUDEPATH += /usr/local/include/opencv4
LIBS += `pkg-config opencv4 --cflags --libs`</code></pre><blockquote>
<p>echo 명령으로 추가하는 과정에서 중복 줄이 생길 수 있습니다. vi로 열어서 위 두 줄만 남기고 중복 줄을 제거합니다.</p>
</blockquote>
<hr />
<h2 id="2-이미지-리소스-준비">2. 이미지 리소스 준비</h2>
<p>Tab7의 초기 화면과 카메라 정지 시 표시할 이미지를 준비합니다.
사용하는 이미지는 아래 GitHub에서 받을 수 있습니다.</p>
<p><a href="https://github.com/kyoung-mo/qt-study/tree/main/AiotClient_tab7/Images">github : kyoung-mo / images source</a></p>
<h3 id="2-1-gimp로-이미지-리사이즈">2-1. GIMP로 이미지 리사이즈</h3>
<p><code>background.jpg</code>의 원본 크기가 위젯 크기(400x300)보다 커서 화면에서 이미지가 잘렸습니다.
GIMP를 설치하고 이미지를 리사이즈합니다.</p>
<pre><code class="language-bash">sudo apt install gimp</code></pre>
<p>GIMP에서 <code>background.jpg</code>를 열고 <strong>이미지 → 크기 조정</strong>으로 크기를 줄인 뒤,
<strong>파일 → 내보내기</strong>로 <code>background_resize.png</code>로 저장합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c0b85914-29ab-4b13-99ea-a807d32c3cd6/image.png" /></p>
<h3 id="2-2-프로젝트-리소스-등록">2-2. 프로젝트 리소스 등록</h3>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Resource File</strong></p>
<p>리소스 파일에 <code>Images</code> 프리픽스를 추가하고 아래 이미지를 등록합니다.</p>
<table>
<thead>
<tr>
<th>파일</th>
<th>용도</th>
</tr>
</thead>
<tbody><tr>
<td>background_resize.png</td>
<td>카메라 정지 시 표시 이미지</td>
</tr>
<tr>
<td>initDisplay_1.png</td>
<td>Tab7 초기 표시 이미지</td>
</tr>
</tbody></table>
<hr />
<h2 id="3-tab7camopencv-클래스-생성">3. Tab7CamOpencv 클래스 생성</h2>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p>Class name을 <code>Tab7CamOpencv</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab7camopencv.h</code></li>
<li><code>tab7camopencv.cpp</code></li>
<li><code>tab7camopencv.ui</code></li>
</ul>
<hr />
<h2 id="4-tab7camopencv-ui-구성">4. Tab7CamOpencv UI 구성</h2>
<p><code>tab7camopencv.ui</code>를 Qt Designer에서 열고 아래와 같이 위젯을 배치합니다.</p>
<pre><code>======================================
|                                    |
|          plabelCamView             |
|         (초기 이미지 표시)           |
|                                    |
|------------------------------------|
| pPBcamStart | pCBrgb | pPBsnapShot |
======================================</code></pre><p>레이아웃 비율은 카메라 뷰 9 : 버튼 영역 1로 설정합니다.</p>
<h3 id="주요-위젯-objectname">주요 위젯 objectName</h3>
<table>
<thead>
<tr>
<th>위젯</th>
<th>objectName</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>QLabel</td>
<td>plabelCamView</td>
<td>카메라 프레임 표시</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBcamStart</td>
<td>카메라 시작/정지 (Checkable)</td>
</tr>
<tr>
<td>QCheckBox</td>
<td>pCBrgb</td>
<td>RGB 분류 ON/OFF</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBsnapShot</td>
<td>스냅샷 저장</td>
</tr>
</tbody></table>
<blockquote>
<p><code>plabelCamView</code>의 Property Editor에서 <code>pixmap</code>에 <code>initDisplay_1.png</code>를 지정하면 초기 화면 이미지가 표시됩니다.</p>
</blockquote>
<blockquote>
<p><code>pPBcamStart</code>는 Property Editor에서 <code>checkable</code>을 체크해야 토글 버튼으로 동작합니다.</p>
</blockquote>
<hr />
<h2 id="5-webcamthread-구현">5. WebCamThread 구현</h2>
<p><code>CamViewerThread</code> 예제의 <code>WebCamThread</code>를 AiotClient용으로 확장합니다.
추가된 주요 항목은 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th>항목</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>QTimer</code></td>
<td>RGB 분류 주기 제어 (1초 간격)</td>
</tr>
<tr>
<td><code>rgbClassifyFlag</code></td>
<td>타이머 tick마다 색상 분류 실행 여부</td>
</tr>
<tr>
<td><code>strColor</code>, <code>strColorPre</code></td>
<td>현재/이전 색상 문자열 (중복 송신 방지)</td>
</tr>
<tr>
<td><code>frameQt</code></td>
<td>BGR→RGB 변환된 표시용 프레임</td>
</tr>
<tr>
<td><code>qImage</code></td>
<td>스냅샷 저장용 멤버 변수</td>
</tr>
<tr>
<td><code>socketSendDataSig</code></td>
<td>색상 변경 시 소켓 메시지 송신 시그널</td>
</tr>
</tbody></table>
<h3 id="5-1-webcamthreadh">5-1. webcamthread.h</h3>
<pre><code class="language-cpp">#ifndef WEBCAMTHREAD_H
#define WEBCAMTHREAD_H

#include &lt;QThread&gt;
#include &lt;QLabel&gt;
#include &lt;QTimer&gt;
#include &lt;opencv2/opencv.hpp&gt;
using namespace cv;
using namespace std;

class WebCamThread : public QThread
{
    Q_OBJECT
    void run();
    int cnt;
    string fname;
    QString strColor, strColorPre;
    Mat frame, frameQt;
    QImage qImage;
    QTimer *pQTimer;
    bool rgbClassifyFlag;
    void put_string(Mat &amp;frame, string text, Point pt, int value = -1);

public:
    WebCamThread(QObject *parent = nullptr);
    bool camViewFlag;
    QLabel *pCamView;
    void snapShot();
    void rgbTimerStart();
    void rgbTimerStop();

private slots:
    void rgbClassifySlot();

signals:
    void socketSendDataSig(QString);
};

#endif // WEBCAMTHREAD_H</code></pre>
<hr />
<h3 id="5-2-webcamthreadcpp---생성자">5-2. webcamthread.cpp - 생성자</h3>
<pre><code class="language-cpp">WebCamThread::WebCamThread(QObject *parent)
    : QThread(parent)
{
    cnt = 0;
    strColor = &quot;NONE&quot;;
    strColorPre = &quot;&quot;;
    camViewFlag = false;
    rgbClassifyFlag = false;
    pQTimer = new QTimer(this);
    connect(pQTimer, SIGNAL(timeout()), this, SLOT(rgbClassifySlot()));
}</code></pre>
<hr />
<h3 id="5-3-webcamthreadcpp---run">5-3. webcamthread.cpp - run()</h3>
<p><code>CamViewerThread</code>와의 주요 차이점은 두 가지입니다.</p>
<p>첫째, <code>cvtColor</code>로 BGR → RGB 변환 후 <code>QImage::Format_RGB888</code>을 사용합니다.
HSV 색상 분류는 원본 <code>frame</code>(BGR) 기준으로 동작하기 때문에 표시용 프레임을 <code>frameQt</code>로 분리합니다.</p>
<p>둘째, 화면 중앙에 십자선과 사각형을 오버레이하여 색상 분류 영역을 시각적으로 표시합니다.</p>
<pre><code class="language-cpp">void WebCamThread::run()
{
    VideoCapture capture(0);
    if (!capture.isOpened())
    {
        cout &lt;&lt; &quot;카메라가 연결되지 않았습니다.&quot; &lt;&lt; endl;
        exit(1);
    }
    while(camViewFlag)
    {
        capture.read(frame);
        fname = &quot;cam_&quot; + to_string(cnt++);
        fname += &quot;.jpg&quot;;

        cvtColor(frame, frameQt, COLOR_BGR2RGB);

        int x = frameQt.cols / 2;
        int y = frameQt.rows / 2;

        if(rgbClassifyFlag)
        {
            Scalar meanHsv;
            Mat frameRoi, hsvImage;
            frameRoi = frame(Rect((x-32), (y-32), 64, 64));
            cvtColor(frameRoi, hsvImage, COLOR_BGR2HSV);
            meanHsv = mean(hsvImage);

            if(170 &lt;= meanHsv[0] || meanHsv[0] &lt; 10)
                strColor = &quot;RED&quot;;
            else if(50 &lt;= meanHsv[0] &amp;&amp; meanHsv[0] &lt; 70)
                strColor = &quot;GREEN&quot;;
            else if(110 &lt;= meanHsv[0] &amp;&amp; meanHsv[0] &lt; 130)
                strColor = &quot;BLUE&quot;;
            else
                strColor = &quot;NONE&quot;;

            rgbClassifyFlag = false;

            // 색상이 변경된 경우에만 소켓 메시지 송신
            if(strColor != strColorPre)
            {
                emit socketSendDataSig(&quot;[KYM_LIN]COLOR@&quot; + strColor);
                strColorPre = strColor;
            }
        }

        put_string(frameQt, strColor.toStdString(), Point(10, 40));
        line(frameQt, Point((x-32), y), Point((x+32), y), Scalar(255, 0, 0), 1);
        line(frameQt, Point(x, y-32), Point(x, y+32), Scalar(255, 0, 0), 1);
        rectangle(frameQt, Point((x-32), (y-32)), Point((x+32), (y+32)), Scalar(0, 255, 0), 2);

        qImage = QImage(frameQt.data, frameQt.cols, frameQt.rows, QImage::Format_RGB888);
        pCamView-&gt;setPixmap(QPixmap::fromImage(qImage));
    }
    capture.release();
    pCamView-&gt;setPixmap(QPixmap(&quot;:/Images/Images/initDisplay.png&quot;));
}</code></pre>
<blockquote>
<p>HSV 색상 범위는 OpenCV 기준 H: 0~179입니다. RED는 색상환의 양 끝(170° 이상 또는 10° 미만)에 걸쳐있어 조건이 두 개로 나뉩니다.</p>
</blockquote>
<hr />
<h3 id="5-4-webcamthreadcpp---나머지-함수">5-4. webcamthread.cpp - 나머지 함수</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/44503020-6cdc-4966-9494-b6eeb95f8f88/image.png" /></p>
<p><strong>put_string</strong> : 색상 이름에 따라 텍스트 색상을 다르게 표시합니다.</p>
<pre><code class="language-cpp">void WebCamThread::put_string(Mat &amp;frame, string text, Point pt, int value)
{
    Scalar colorScalar;
    if(value != -1)
        text += to_string(value);
    if(text == &quot;RED&quot;)         colorScalar = {255, 0, 0};
    else if(text == &quot;GREEN&quot;)  colorScalar = {0, 255, 0};
    else if(text == &quot;BLUE&quot;)   colorScalar = {0, 0, 255};
    else                      colorScalar = {128, 128, 128};
    Point shade = pt + Point(2, 2);
    int font = FONT_HERSHEY_SIMPLEX;
    putText(frame, text, shade, font, 0.7, Scalar(0, 0, 0), 2);
    putText(frame, text, pt, font, 0.7, colorScalar, 2);
}</code></pre>
<p><strong>snapShot</strong> : <code>imwrite</code> 대신 <code>qImage.save()</code>를 사용하여 RGB 변환된 상태로 저장합니다.</p>
<pre><code class="language-cpp">void WebCamThread::snapShot()
{
    qImage.save(QString::fromStdString(fname), &quot;JPG&quot;, 80);
}</code></pre>
<p><strong>RGB 타이머 제어</strong> : 1초 간격으로 <code>rgbClassifyFlag</code>를 <code>true</code>로 설정합니다.
<code>run()</code> 루프는 이 플래그를 확인하여 해당 프레임에서만 색상 분류를 수행합니다.</p>
<pre><code class="language-cpp">void WebCamThread::rgbTimerStart() { pQTimer-&gt;start(1000); }
void WebCamThread::rgbTimerStop()  { if(pQTimer-&gt;isActive()) pQTimer-&gt;stop(); }
void WebCamThread::rgbClassifySlot() { rgbClassifyFlag = true; }</code></pre>
<hr />
<h2 id="6-tab7camopencvh--cpp">6. tab7camopencv.h / cpp</h2>
<h3 id="tab7camopencvh">tab7camopencv.h</h3>
<pre><code class="language-cpp">#ifndef TAB7CAMOPENCV_H
#define TAB7CAMOPENCV_H

#include &lt;QWidget&gt;
#include &lt;webcamthread.h&gt;

namespace Ui {
class Tab7CamOpencv;
}

class Tab7CamOpencv : public QWidget
{
    Q_OBJECT

public:
    explicit Tab7CamOpencv(QWidget *parent = nullptr);
    ~Tab7CamOpencv();
    WebCamThread* getpWebCamThread();

private slots:
    void on_pPBsnapShot_clicked();
    void on_pPBcamStart_clicked(bool checked);
    void on_pCBrgb_clicked(bool checked);

private:
    Ui::Tab7CamOpencv *ui;
    WebCamThread *pWebCamThread;
};

#endif // TAB7CAMOPENCV_H</code></pre>
<h3 id="tab7camopencvcpp---생성자">tab7camopencv.cpp - 생성자</h3>
<p>초기 상태에서 <code>pPBsnapShot</code>과 <code>pCBrgb</code>는 비활성화합니다.
카메라가 시작된 이후에만 사용할 수 있도록 버튼 활성화를 <code>on_pPBcamStart_clicked</code>에서 제어합니다.</p>
<pre><code class="language-cpp">Tab7CamOpencv::Tab7CamOpencv(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Tab7CamOpencv)
{
    ui-&gt;setupUi(this);
    ui-&gt;pPBsnapShot-&gt;setEnabled(false);
    ui-&gt;pCBrgb-&gt;setEnabled(false);
    pWebCamThread = new WebCamThread(this);
    pWebCamThread-&gt;pCamView = ui-&gt;plabelCamView;
}</code></pre>
<h3 id="tab7camopencvcpp---버튼-슬롯">tab7camopencv.cpp - 버튼 슬롯</h3>
<pre><code class="language-cpp">void Tab7CamOpencv::on_pPBcamStart_clicked(bool checked)
{
    if(checked)
    {
        pWebCamThread-&gt;camViewFlag = true;
        if(!pWebCamThread-&gt;isRunning())
        {
            pWebCamThread-&gt;start();
            ui-&gt;pPBcamStart-&gt;setText(&quot;CamStop&quot;);
            ui-&gt;pPBsnapShot-&gt;setEnabled(true);
        }
    }
    else
    {
        pWebCamThread-&gt;camViewFlag = false;
        ui-&gt;pPBcamStart-&gt;setText(&quot;CamStart&quot;);
        ui-&gt;pPBsnapShot-&gt;setEnabled(false);
    }
    ui-&gt;pCBrgb-&gt;setEnabled(checked);
}

void Tab7CamOpencv::on_pPBsnapShot_clicked()
{
    pWebCamThread-&gt;snapShot();
}

void Tab7CamOpencv::on_pCBrgb_clicked(bool checked)
{
    if(checked)
        pWebCamThread-&gt;rgbTimerStart();
    else
        pWebCamThread-&gt;rgbTimerStop();
}

WebCamThread* Tab7CamOpencv::getpWebCamThread()
{
    return pWebCamThread;
}</code></pre>
<hr />
<h2 id="7-mainwidget에-tab7-추가-및-소켓-연동">7. mainwidget에 Tab7 추가 및 소켓 연동</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<pre><code class="language-cpp">#include &lt;tab7camopencv.h&gt;

Tab7CamOpencv *pTab7CamOpencv;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<p><code>Tab7CamOpencv</code> 객체를 생성하여 <code>pTab7</code>에 배치하고, <code>WebCamThread</code>의 소켓 시그널을 Tab2와 연결합니다.</p>
<pre><code class="language-cpp">pTab7CamOpencv = new Tab7CamOpencv(ui-&gt;pTab7);
ui-&gt;pTab7-&gt;setLayout(pTab7CamOpencv-&gt;layout());

connect(pTab7CamOpencv-&gt;getpWebCamThread(), SIGNAL(socketSendDataSig(QString)),
        pTab2SocketClient, SLOT(socketWriteDataSlot(QString)));</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ac6436c5-796b-4ad7-8df5-7affe06df198/image.png" /></p>
<p>Tab2에서 서버에 접속한 상태에서 RGB Classify를 활성화하면, 색상이 변경될 때마다 아래 형식의 메시지가 서버로 전송됩니다.</p>
<pre><code>[KYM_LIN]COLOR@RED
[KYM_LIN]COLOR@GREEN
[KYM_LIN]COLOR@BLUE</code></pre><blockquote>
<p><code>WebCamThread</code> 내부에서 직접 소켓을 다루지 않고 시그널만 emit합니다. 실제 송신은 Tab2의 <code>socketWriteDataSlot</code>이 담당하므로, Tab2가 서버에 연결된 상태여야 메시지가 전달됩니다.</p>
</blockquote>
<hr />
<h2 id="8-실행-결과">8. 실행 결과</h2>
<p>RGB Classify 체크박스를 활성화하면 1초 간격으로 중앙 영역의 색상을 분석합니다.
인식된 색상은 화면 좌측 상단에 해당 색상으로 표시되고, 색상이 변경될 때만 서버로 메시지를 송신합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/53610960-55a9-4079-a84d-49cb18b0b160/image.gif" /></p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>AiotClient .pro에 OpenCV 경로 추가 (INCLUDEPATH, LIBS)
    ↓
background 이미지 GIMP로 리사이즈 → 프로젝트 리소스 등록
    ↓
Tab7CamOpencv 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
UI 구성 (QLabel + QPushButton(Checkable) + QCheckBox + QPushButton)
    ↓
WebCamThread 확장
    ↓
run() : VideoCapture → BGR→RGB 변환 → 오버레이 → QLabel 표시
    ↓
RGB 분류 : QTimer(1초) → HSV 변환 → 색상 판별 → socketSendDataSig emit
    ↓
tab7camopencv.cpp : 버튼 슬롯 구현, getpWebCamThread() 제공
    ↓
mainwidget에 Tab7 추가 및 WebCamThread 소켓 시그널 연결
    ↓
Tab2 서버 연결 상태에서 색상 변경 시 서버로 메시지 송신</code></pre>