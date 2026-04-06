<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner7">이전 글 : Qt) Designer로 UI 구성하기(5) - Tab7CamOpencv</a></p>
</blockquote>
<p>이전 글에서 OpenCV와 QThread를 활용해 Tab7 카메라 탭을 구현했습니다.</p>
<p>이번 글에서는 <code>mjpg-streamer</code>를 Qt 앱 내에서 직접 실행하고, <code>QWebEngineView</code>로 스트림을 표시하는 <code>Tab6WebCamera</code>를 구현하는 과정을 정리합니다.</p>
<p>mjpg-streamer 설치 및 브라우저에서의 스트리밍 확인은 이전 글들을 참고 부탁드립니다!</p>
<blockquote>
<p><a href="https://velog.io/@mommers/Qt-%EC%9B%B9%EC%BA%A0-%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D-Ubuntu-Rpi-%ED%99%98%EA%B2%BD-mjpg-streamer">Ubuntu | Rpi ) 웹캠 스트리밍 - mjpg-streamer</a></p>
</blockquote>
<blockquote>
<p><a href="https://velog.io/@mommers/Qt-QWebEngineView%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9B%B9%EC%BA%A0-%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D">Qt) QWebEngineView를 이용한 웹캠 스트리밍</a></p>
</blockquote>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/681d10e7-bfa9-4333-af18-7f8915d1ae74/image.png" /></p>
<h2 id="1-mjpg-streamer-masterzip-압축-해제-및-빌드">1. mjpg-streamer-master.zip 압축 해제 및 빌드</h2>
<p>교수님이 제공하신 <code>mjpg-streamer-master.zip</code>을 홈 디렉토리에서 압축 해제합니다. 관련 github 링크도 첨부해둘테니 여기서 가져오셔도 됩니다.</p>
<p><a href="https://github.com/jacksonliam/mjpg-streamer">https://github.com/jacksonliam/mjpg-streamer</a></p>
<pre><code class="language-bash">cd ~
unzip mjpg-streamer-master.zip
cd mjpg-streamer-master
make
sudo make install</code></pre>
<p>빌드 완료 후 디렉토리 구조를 확인합니다.</p>
<pre><code class="language-bash">ls ~/mjpg-streamer-master</code></pre>
<pre><code>mjpg_streamer  input_uvc.so  output_http.so  www/  start.sh  ...</code></pre><p><code>mjpg_streamer</code> 실행 파일과 <code>input_uvc.so</code>, <code>output_http.so</code>, <code>www/</code> 가 모두 같은 디렉토리에 위치합니다.</p>
<blockquote>
<p><code>start.sh</code>에서 <code>export LD_LIBRARY_PATH=&quot;$(pwd)&quot;</code>를 설정하는 이유도 <code>.so</code> 플러그인 파일들이 시스템 경로가 아닌 같은 디렉토리에 있기 때문입니다.</p>
</blockquote>
<p>터미널에서 직접 실행해 정상 동작을 확인합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/22b2ff1e-53ec-46c9-aad1-0216754fa6b1/image.png" /></p>
<pre><code class="language-bash">cd ~/mjpg-streamer-master
vi start.sh  # 필요 시 인증 옵션 확인
bash start.sh
# start.sh 실행 시 아래 명령어가 자동으로 실행됩니다
# export LD_LIBRARY_PATH=&quot;$(pwd)&quot;
# ./mjpg_streamer -i &quot;./input_uvc.so&quot; -o &quot;./output_http.so -w ./www&quot;</code></pre>
<p>브라우저에서 <code>http://10.10.16.35:8080</code>에 접속해 스트리밍이 출력되면 정상입니다.</p>
<hr />
<h2 id="2-tab6webcamera-클래스-생성">2. Tab6WebCamera 클래스 생성</h2>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p>Class name을 <code>Tab6WebCamera</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab6webcamera.h</code></li>
<li><code>tab6webcamera.cpp</code></li>
<li><code>tab6webcamera.ui</code></li>
</ul>
<hr />
<h2 id="3-tab6webcamera-ui-구성">3. Tab6WebCamera UI 구성</h2>
<p><code>tab6webcamera.ui</code>를 Qt Designer에서 열고 아래와 같이 위젯을 배치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b29076e3-ff6b-4d45-adeb-d8a0d9f5eaa5/image.png" /></p>
<pre><code>=====================================
|                                   |
|           pGPView                 |
|      (QGraphicsView)              |
|                                   |
|-----------------------------------|
|    pPBCamStart   |  pPBsnapShot   |
=====================================</code></pre><p>레이아웃 비율은 카메라 뷰 9 : 버튼 영역 1로 설정합니다.</p>
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
<td>QGraphicsView</td>
<td>pGPView</td>
<td>초기 이미지 및 스트림 영역</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBCamStart</td>
<td>카메라 시작/정지 (Checkable)</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBsnapShot</td>
<td>스냅샷 저장</td>
</tr>
</tbody></table>
<blockquote>
<p><code>pPBCamStart</code>는 Property Editor에서 <code>checkable</code>을 체크해야 토글 버튼으로 동작합니다.</p>
</blockquote>
<hr />
<h2 id="4-tab6webcamerah">4. tab6webcamera.h</h2>
<p>Tab6는 <code>QWebEngineView</code>와 <code>QProcess</code>를 멤버로 가집니다.
<code>QWebEngineView</code>는 생성자에서 동적으로 생성하고, CamStart 버튼 클릭 시 <code>pGPView</code> 위에 올립니다.</p>
<pre><code class="language-cpp">#ifndef TAB6WEBCAMERA_H
#define TAB6WEBCAMERA_H

#include &lt;QWidget&gt;
#include &lt;QWebEngineView&gt;
#include &lt;QProcess&gt;
#include &lt;QGraphicsPixmapItem&gt;
#include &lt;QThread&gt;
#include &lt;QGraphicsScene&gt;

namespace Ui {
class Tab6WebCamera;
}

class Tab6WebCamera : public QWidget
{
    Q_OBJECT

public:
    explicit Tab6WebCamera(QWidget *parent = nullptr);
    ~Tab6WebCamera();

private:
    Ui::Tab6WebCamera *ui;
    QWebEngineView *pQWebEngineView;
    QProcess *pQProcess;
    QUrl webcamUrl;
    QGraphicsScene initDisplayScene;

private slots:
    void camStartSlot(bool);
    void on_pPBsnapShot_clicked();
};

#endif // TAB6WEBCAMERA_H</code></pre>
<hr />
<h2 id="5-tab6webcameracpp">5. tab6webcamera.cpp</h2>
<h3 id="5-1-생성자">5-1. 생성자</h3>
<p>생성자에서 스트림 URL을 설정하고, <code>QProcess</code>와 <code>QWebEngineView</code>를 생성합니다.
초기 화면은 <code>QGraphicsScene</code>에 <code>initDisplay_2.png</code>를 추가해 <code>pGPView</code>에 표시합니다.</p>
<pre><code class="language-cpp">Tab6WebCamera::Tab6WebCamera(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Tab6WebCamera)
{
    ui-&gt;setupUi(this);

    webcamUrl = QUrl(&quot;http://10.10.16.35:8080/?action=stream&quot;);
    webcamUrl.setUserName(&quot;user&quot;);
    webcamUrl.setPassword(&quot;1234&quot;);

    pQProcess = new QProcess(this);
    pQWebEngineView = new QWebEngineView(this);

    QPixmap pixMap(&quot;:/Images/Images/initDisplay_2.png&quot;);
    QGraphicsScene* scene = new QGraphicsScene(ui-&gt;pGPView);
    scene-&gt;addPixmap(pixMap);
    ui-&gt;pGPView-&gt;setScene(scene);

    connect(ui-&gt;pPBCamStart, SIGNAL(clicked(bool)), this, SLOT(camStartSlot(bool)));
}</code></pre>
<blockquote>
<p>스트림 URL에 <code>setUserName</code>, <code>setPassword</code>를 설정하면 mjpg-streamer의 <code>-c user:1234</code> 인증을 자동으로 처리합니다.</p>
</blockquote>
<hr />
<h3 id="5-2-camstartslot---mjpg-streamer-실행-및-스트림-연결">5-2. camStartSlot - mjpg-streamer 실행 및 스트림 연결</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d9e964d8-4c9e-4df2-a861-2762b6e6b8ec/image.gif" /></p>
<p>Tab6의 동작 원리는 다음과 같습니다.</p>
<p><strong>CamStart</strong> 시 <code>QProcess</code>가 ubuntu05 로컬에서 <code>mjpg-streamer</code>를 실행합니다. mjpg-streamer는 포트 8080을 열고 HTTP 서버 역할을 시작하고, <code>QWebEngineView</code>가 해당 주소에 접속해 스트림을 표시합니다.</p>
<p><strong>CamStop</strong> 시 <code>pQProcess-&gt;kill()</code>로 mjpg-streamer 프로세스를 강제 종료합니다. 포트 8080을 열고 있던 프로세스가 종료되면 서버 자체가 사라지므로 스트리밍이 중단됩니다.</p>
<pre><code>CamStart → QProcess로 mjpg-streamer 실행 → 포트 8080 오픈 → QWebEngineView로 스트림 접속
CamStop  → QProcess kill → mjpg-streamer 종료 → 포트 8080 닫힘</code></pre><p>실행 파일과 <code>.so</code> 플러그인이 모두 같은 디렉토리에 있기 때문에 경로를 절대경로로 지정합니다.
프로세스가 정상적으로 시작되면 200ms 대기 후 <code>QWebEngineView</code>에 스트림 URL을 로드하고, <code>pGPView</code>의 자식 위젯으로 올린 뒤 기존 <code>QGraphicsScene</code>을 제거합니다.</p>
<pre><code class="language-cpp">void Tab6WebCamera::camStartSlot(bool bCheck)
{
    QString webcamProgrm = &quot;/home/ubuntu/mjpg-streamer-master/mjpg_streamer&quot;;
    QStringList webcamArg = {
        &quot;-i&quot;, &quot;/home/ubuntu/mjpg-streamer-master/input_uvc.so&quot;,
        &quot;-o&quot;, &quot;/home/ubuntu/mjpg-streamer-master/output_http.so &quot;
              &quot;-w /home/ubuntu/mjpg-streamer-master/www -c user:1234&quot;
    };

    if(bCheck)
    {
        pQProcess-&gt;start(webcamProgrm, webcamArg);
        if(pQProcess-&gt;waitForStarted())
        {
            QThread::msleep(200);
            pQWebEngineView-&gt;load(webcamUrl);
            pQWebEngineView-&gt;saveGeometry();
            ui-&gt;pPBCamStart-&gt;setText(&quot;CamStop&quot;);

            pQWebEngineView-&gt;setParent(ui-&gt;pGPView);
            pQWebEngineView-&gt;setGeometry(ui-&gt;pGPView-&gt;rect());
            pQWebEngineView-&gt;show();

            if(ui-&gt;pGPView-&gt;scene())
                ui-&gt;pGPView-&gt;setScene(nullptr);
        }
    }
    else
    {
        pQProcess-&gt;kill();
        pQWebEngineView-&gt;stop();
        pQWebEngineView-&gt;hide();
        ui-&gt;pPBCamStart-&gt;setText(&quot;CamStart&quot;);

        QGraphicsScene* oldScene = ui-&gt;pGPView-&gt;scene();
        if(oldScene)
        {
            ui-&gt;pGPView-&gt;setScene(nullptr);
            delete oldScene;
        }
        QPixmap pixMap(&quot;:/Images/Images/initDisplay_2.png&quot;);
        QGraphicsScene* scene = new QGraphicsScene(ui-&gt;pGPView);
        scene-&gt;addPixmap(pixMap);
        ui-&gt;pGPView-&gt;setScene(scene);
    }
}</code></pre>
<blockquote>
<p><code>setGeometry(ui-&gt;pGPView-&gt;rect())</code>로 <code>QWebEngineView</code> 크기를 <code>pGPView</code> 영역에 맞게 설정합니다.</p>
</blockquote>
<hr />
<h3 id="5-3-snapshot">5-3. Snapshot</h3>
<p>현재 Snapshot 기능은 미구현 상태입니다.
mjpg-streamer의 snapshot URL(<code>?action=snapshot</code>)을 <code>wget</code>으로 저장하는 방식으로 추후 구현할 예정입니다.</p>
<pre><code class="language-cpp">void Tab6WebCamera::on_pPBsnapShot_clicked()
{
    //wget -O a.jpg http://10.10.16.35:8080/?action=snapshot
}</code></pre>
<hr />
<h2 id="6-mainwidget에-tab6-추가">6. mainwidget에 Tab6 추가</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<pre><code class="language-cpp">#include &lt;tab6webcamera.h&gt;

Tab6WebCamera *pTab6WebCamera;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<pre><code class="language-cpp">pTab6WebCamera = new Tab6WebCamera(ui-&gt;pTab6);
ui-&gt;pTab6-&gt;setLayout(pTab6WebCamera-&gt;layout());</code></pre>
<p>Tab6는 Tab7과 달리 소켓 연동이 없으므로 별도 Signal/Slot 연결이 필요하지 않습니다.</p>
<hr />
<h2 id="7-tab6-vs-tab7-비교">7. Tab6 vs Tab7 비교</h2>
<table>
<thead>
<tr>
<th></th>
<th>Tab6</th>
<th>Tab7</th>
</tr>
</thead>
<tbody><tr>
<td>카메라 처리</td>
<td>mjpg-streamer (QProcess로 외부 실행)</td>
<td>OpenCV VideoCapture (직접)</td>
</tr>
<tr>
<td>화면 표시</td>
<td>QWebEngineView (HTTP 스트림)</td>
<td>QLabel + QPixmap</td>
</tr>
<tr>
<td>스레드</td>
<td>없음</td>
<td>QThread</td>
</tr>
<tr>
<td>RGB 분류</td>
<td>없음</td>
<td>HSV 기반 색상 분류</td>
</tr>
<tr>
<td>소켓 연동</td>
<td>없음</td>
<td>있음</td>
</tr>
</tbody></table>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>mjpg-streamer-master.zip 압축 해제 → make → sudo make install
    ↓
터미널에서 직접 실행 후 브라우저 스트리밍 확인
    ↓
Tab6WebCamera 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
UI 구성 (QGraphicsView + QPushButton x2)
    ↓
생성자 : 스트림 URL 설정, QProcess/QWebEngineView 생성, 초기 이미지 표시
    ↓
CamStart ON : QProcess로 mjpg-streamer 실행 → 포트 8080 오픈 → QWebEngineView로 스트림 접속
    ↓
QWebEngineView를 pGPView 위에 자식 위젯으로 올리기
    ↓
CamStop : QProcess kill → mjpg-streamer 종료 → QWebEngineView hide → 초기 이미지 복원
    ↓
mainwidget에 Tab6 추가</code></pre>