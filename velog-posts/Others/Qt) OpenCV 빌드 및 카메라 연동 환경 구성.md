<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner5">이전 글 : Qt) AiotClient - Tab1 / Tab2 연동 과제</a></p>
</blockquote>
<p>이전 글에서 Tab1과 Tab2의 소켓 연동 과제를 구현해봤습니다.</p>
<p>이번 글에서는 Tab7, Tab6 카메라 탭 구현에 앞서 ubuntu05 환경에 OpenCV 4.12.0을 소스 빌드하고, Qt + OpenCV 연동 예제인 <code>CamViewerThread</code>를 실행해 카메라 영상 출력을 확인하는 과정을 정리합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3f8c2673-4713-4cee-8922-87c87e5776e7/image.png" /></p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fd2919cd-081a-424e-ae40-b15dfa0f84fa/image.png" /></p>
<h2 id="1-opencv-4120-소스-빌드">1. OpenCV 4.12.0 소스 빌드</h2>
<h3 id="1-1-기존-버전-확인-및-제거">1-1. 기존 버전 확인 및 제거</h3>
<p>빌드에 앞서 기존에 설치된 OpenCV가 있다면 제거합니다.</p>
<pre><code class="language-bash">opencv_version

sudo apt-get purge libopencv* python-opencv
sudo apt-get autoremove
sudo find /usr/local/ -name &quot;*opencv*&quot; -exec rm -rf {} \;</code></pre>
<blockquote>
<p><code>sudo find</code> 명령은 직접 소스 빌드로 설치한 경우에만 실행합니다.</p>
</blockquote>
<hr />
<h3 id="1-2-의존성-패키지-설치">1-2. 의존성 패키지 설치</h3>
<pre><code class="language-bash">sudo apt update
sudo apt upgrade
sudo apt install build-essential cmake git pkg-config \
  libjpeg-dev libtiff-dev libpng-dev \
  libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
  v4l-utils libxvidcore-dev libx264-dev libgtk-3-dev \
  libatlas-base-dev gfortran python3-dev opencl-headers \
  ffmpeg libxine2-dev libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev mesa-utils \
  libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev \
  libeigen3-dev python3-numpy</code></pre>
<hr />
<h3 id="1-3-소스-다운로드-및-빌드-디렉토리-생성">1-3. 소스 다운로드 및 빌드 디렉토리 생성</h3>
<p>opencv와 opencv_contrib를 함께 다운로드합니다.
<code>contrib</code> 모듈은 SIFT, SURF 등 추가 알고리즘을 포함합니다.</p>
<pre><code class="language-bash">mkdir openCV &amp;&amp; cd openCV
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.12.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.12.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
cd opencv-4.12.0
mkdir build &amp;&amp; cd build</code></pre>
<hr />
<h3 id="1-4-cmake-옵션-설정">1-4. cmake 옵션 설정</h3>
<pre><code class="language-bash">cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D WITH_TBB=OFF \
      -D WITH_IPP=OFF \
      -D WITH_1394=OFF \
      -D BUILD_WITH_DEBUG_INFO=OFF \
      -D BUILD_DOCS=OFF \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D BUILD_EXAMPLES=OFF \
      -D BUILD_PACKAGE=OFF \
      -D BUILD_TESTS=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D WITH_QT=OFF \
      -D WITH_GTK=ON \
      -D WITH_OPENGL=ON \
      -D BUILD_opencv_python3=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.12.0/modules \
      -D WITH_V4L=ON \
      -D WITH_FFMPEG=ON \
      -D WITH_XINE=ON \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D BUILD_NEW_PYTHON_SUPPORT=ON \
      -D OPENCV_SKIP_PYTHON_LOADER=ON \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      ../</code></pre>
<blockquote>
<p><code>OPENCV_GENERATE_PKGCONFIG=ON</code> 옵션을 설정해야 이후 <code>pkg-config opencv4 --cflags --libs</code> 명령으로 경로를 확인할 수 있습니다.</p>
</blockquote>
<hr />
<h3 id="1-5-빌드-및-설치">1-5. 빌드 및 설치</h3>
<pre><code class="language-bash">make -j4          # 약 35분 소요
sudo make install
sudo ldconfig</code></pre>
<p>설치 완료 후 버전 및 경로를 확인합니다.</p>
<pre><code class="language-bash">opencv_version
pkg-config opencv4 --cflags --libs</code></pre>
<hr />
<h2 id="2-opencv-설치-확인---firstcpp">2. OpenCV 설치 확인 - first.cpp</h2>
<p>설치가 정상적으로 완료됐는지 간단한 예제로 확인합니다.
<code>first.cpp</code>는 지정한 크기의 단색 이미지를 화면에 출력하는 예제입니다.</p>
<pre><code class="language-cpp">#include &lt;opencv2/highgui.hpp&gt;
using namespace::cv;
int main(void)
{
    Mat image(300, 400, CV_8UC1, Scalar(128));
    imshow(&quot;영상보기&quot;, image);
    waitKey(0);
    return 0;
}</code></pre>
<p><code>Scalar(128)</code> 값을 수정해 이미지 밝기가 바뀌는 것을 확인하며 OpenCV가 정상적으로 동작함을 확인했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/775983b2-02cb-48ac-9078-69f9d68cfe35/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e29a85cc-8568-4215-a241-371bac6870c9/image.png" /></p>
<blockquote>
<p>위 캡쳐에서 밝은 회색 → 어두운 회색으로 변경되는 것을 확인할 수 있습니다.</p>
</blockquote>
<hr />
<h2 id="3-camviewerthread---qt--opencv-카메라-연동">3. CamViewerThread - Qt + OpenCV 카메라 연동</h2>
<p>OpenCV 설치를 확인한 후, Qt와 OpenCV를 연동해 카메라 영상을 Qt 화면에 출력하는 예제 프로젝트를 진행했습니다.</p>
<h3 id="3-1-프로젝트-구조">3-1. 프로젝트 구조</h3>
<table>
<thead>
<tr>
<th>파일</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td><code>mainwidget.h/cpp</code></td>
<td>메인 위젯, 버튼 이벤트 처리</td>
</tr>
<tr>
<td><code>webcamthread.h/cpp</code></td>
<td><code>QThread</code> 상속, OpenCV 카메라 루프</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-2-pro-파일-opencv-경로-설정">3-2. .pro 파일 OpenCV 경로 설정</h3>
<p>Qt 프로젝트에서 OpenCV 헤더를 사용하려면 <code>.pro</code> 파일에 경로를 추가해야 합니다.
ubuntu05는 소스 빌드 설치이므로 경로가 <code>/usr/local</code> 하위에 위치합니다.</p>
<pre><code>INCLUDEPATH += /usr/local/include/opencv4
LIBS += `pkg-config opencv4 --cflags --libs`</code></pre><hr />
<h3 id="3-3-webcamthreadh">3-3. webcamthread.h</h3>
<p>카메라 루프는 UI 스레드와 분리하기 위해 <code>QThread</code>를 상속한 <code>WebCamThread</code> 클래스로 구현합니다.</p>
<pre><code class="language-cpp">#ifndef WEBCAMTHREAD_H
#define WEBCAMTHREAD_H

#include &lt;QThread&gt;
#include &lt;QLabel&gt;
#include &lt;opencv2/opencv.hpp&gt;
using namespace cv;
using namespace std;

class WebCamThread : public QThread
{
    Q_OBJECT
    void run();
    int cnt;
    string fname;
    Mat frame;
    void put_string(Mat &amp;frame, string text, Point pt, int value);

public:
    WebCamThread(QObject *parent = nullptr);
    bool camViewFlag;
    QLabel *pCamView;
    void snapShot();
};

#endif // WEBCAMTHREAD_H</code></pre>
<hr />
<h3 id="3-4-webcamthreadcpp">3-4. webcamthread.cpp</h3>
<p><code>run()</code> 안에서 <code>VideoCapture</code>로 카메라를 열고, 프레임을 읽어 <code>QLabel</code>에 표시합니다.
<code>cv::Mat</code> 데이터를 <code>QImage</code>로 변환한 뒤 <code>QPixmap</code>으로 설정하는 방식입니다.</p>
<pre><code class="language-cpp">#include &quot;webcamthread.h&quot;

WebCamThread::WebCamThread(QObject *parent)
    : QThread(parent)
{
    cnt = 0;
    camViewFlag = false;
}

void WebCamThread::run()
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
        put_string(frame, &quot;Count: &quot;, Point(10, 40), cnt);
        fname = &quot;cam_&quot; + to_string(cnt++);
        fname += &quot;.jpg&quot;;
        QImage qImage(frame.data, frame.cols, frame.rows, QImage::Format_BGR888);
        pCamView-&gt;setPixmap(QPixmap::fromImage(qImage));
    }
    capture.release();
    pCamView-&gt;setPixmap(QPixmap(&quot;initDisplay.png&quot;));
}

void WebCamThread::put_string(Mat &amp;frame, string text, Point pt, int value)
{
    text += to_string(value);
    Point shade = pt + Point(2, 2);
    int font = FONT_HERSHEY_SIMPLEX;
    putText(frame, text, shade, font, 0.7, Scalar(0, 0, 0), 2);
    putText(frame, text, pt, font, 0.7, Scalar(120, 200, 90), 2);
}

void WebCamThread::snapShot()
{
    imwrite(fname, frame);
}</code></pre>
<blockquote>
<p><code>QImage::Format_BGR888</code>을 사용하면 OpenCV의 BGR 포맷을 별도 변환 없이 바로 Qt에서 표시할 수 있습니다. 이후 Tab7에서는 <code>cvtColor</code>로 RGB 변환 후 <code>Format_RGB888</code>을 사용하는 방식으로 변경됩니다.</p>
</blockquote>
<hr />
<h3 id="3-5-mainwidgeth">3-5. mainwidget.h</h3>
<pre><code class="language-cpp">#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include &lt;QWidget&gt;
#include &lt;QDebug&gt;
#include &quot;webcamthread.h&quot;

namespace Ui {
class MainWidget;
}

class MainWidget : public QWidget
{
    Q_OBJECT

public:
    explicit MainWidget(QWidget *parent = nullptr);
    ~MainWidget();

private slots:
    void on_pPBcamStart_clicked(bool checked);
    void on_pPBsnapShot_clicked();

private:
    Ui::MainWidget *ui;
    WebCamThread *pWebCamThread;
};

#endif // MAINWIDGET_H</code></pre>
<hr />
<h3 id="3-6-mainwidgetcpp">3-6. mainwidget.cpp</h3>
<p>생성자에서 <code>WebCamThread</code>를 생성하고 <code>pCamView</code>에 <code>QLabel</code> 포인터를 전달합니다.
<code>CamStart</code> 버튼은 checkable 버튼으로, 클릭 시 <code>bool</code> 값을 받아 스레드를 시작/정지합니다.</p>
<pre><code class="language-cpp">#include &quot;mainwidget.h&quot;
#include &quot;ui_mainwidget.h&quot;

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
{
    ui-&gt;setupUi(this);
    setWindowTitle(&quot;CamViewer&quot;);
    ui-&gt;pPBsnapShot-&gt;setEnabled(false);
    pWebCamThread = new WebCamThread(this);
    pWebCamThread-&gt;pCamView = ui-&gt;plabelCamView;
}

MainWidget::~MainWidget()
{
    delete ui;
}

void MainWidget::on_pPBcamStart_clicked(bool checked)
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
}

void MainWidget::on_pPBsnapShot_clicked()
{
    pWebCamThread-&gt;snapShot();
}</code></pre>
<hr />
<h3 id="3-7-실행-결과">3-7. 실행 결과</h3>
<p>빌드 후 실행하면 카메라 영상이 Qt 위젯에 실시간으로 출력됩니다. 좌측 상단에 프레임 카운트가 함께 표시되며, <code>SnapShot</code> 버튼을 클릭하면 <code>cam_[count번호].jpg</code>로 사진이 저장됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b46261aa-1b97-4542-af6a-9e9baac2ec43/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f8131df1-54ac-4dfd-b84c-58594aa94163/image.png" /></p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>OpenCV 4.12.0 소스 빌드 (의존성 설치 → cmake → make -j4 → make install → ldconfig)
    ↓
first.cpp로 설치 확인 (단색 이미지 출력, Scalar 값 변경으로 동작 검증)
    ↓
.pro 파일에 OpenCV 경로 추가 (INCLUDEPATH, LIBS)
    ↓
CamViewerThread 프로젝트 구현
    ↓
WebCamThread (QThread) - VideoCapture → Mat → QImage → QPixmap → QLabel
    ↓
CamStart/CamStop 토글 버튼으로 스레드 제어, Snapshot 저장 확인</code></pre>