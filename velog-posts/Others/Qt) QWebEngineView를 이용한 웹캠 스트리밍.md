<blockquote>
<p><a href="https://velog.io/@mommers/Qt-%EC%9B%B9%EC%BA%A0-%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D-Ubuntu-Rpi-%ED%99%98%EA%B2%BD-mjpg-streamer"> 이전 글  : Ubuntu | Rpi ) 웹캠 스트리밍 - mjpg-streamer </a></p>
</blockquote>
<p>이전 글에서 Windows에서 웹캠 동작을 확인하고, Ubuntu와 Raspberry Pi 환경에서 각각 mjpg-streamer를 빌드하여 브라우저에서 스트리밍을 테스트하였습니다.
이번 글에서는 Raspberry Pi에 웹캠을 연결하여 스트리밍을 실행하고, Ubuntu 환경의 Qt 애플리케이션에서 해당 스트림을 화면에 출력하는 과정을 정리하였습니다.</p>
<hr />
<h2 id="1-raspberry-pi에서-스트리밍-실행">1. Raspberry Pi에서 스트리밍 실행</h2>
<p>Raspberry Pi에 USB 웹캠을 연결한 후 mjpg-streamer를 실행합니다.</p>
<p>웹캠 장치 번호를 확인합니다.</p>
<pre><code class="language-bash">v4l2-ctl --list-devices</code></pre>
<p>스트리밍을 시작합니다.</p>
<pre><code class="language-bash">export LD_LIBRARY_PATH=.
./mjpg_streamer -o &quot;output_http.so -w ./www -l 0.0.0.0 -p 8080&quot; -i &quot;input_uvc.so -d /dev/video0&quot;</code></pre>
<p>Raspberry Pi의 IP를 확인합니다.</p>
<pre><code class="language-bash">ip addr | grep inet</code></pre>
<p>스트림 URL은 아래 형식으로 구성됩니다.</p>
<pre><code>http://라즈베리파이_IP:8080/?action=stream</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0891807d-5acd-4e27-b72e-ef027f4f3700/image.png" /></p>
<hr />
<h2 id="2-qt에서-스트리밍-화면-출력">2. Qt에서 스트리밍 화면 출력</h2>
<p>Ubuntu 환경에서 Qt 프로젝트를 생성하고 <code>QWebEngineView</code>를 사용하여 스트림을 출력합니다.</p>
<p><code>CMakeLists.txt</code>에 <code>WebEngineWidgets</code> 모듈을 추가합니다.</p>
<pre><code class="language-cmake">find_package(Qt6 6.5 REQUIRED COMPONENTS Core Widgets WebEngineWidgets)
target_link_libraries(프로젝트명 PRIVATE Qt6::Widgets Qt6::WebEngineWidgets)</code></pre>
<h3 id="2-1-url-연결-테스트-naver">2-1. URL 연결 테스트 (Naver)</h3>
<p>스트림 주소를 연결하기 전에 <code>QWebEngineView</code>가 정상적으로 동작하는지 네이버 URL로 먼저 테스트합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b792689d-8785-4600-9d1c-8330916641ac/image.png" /></p>
<p><strong>mainwidget.h</strong></p>
<pre><code class="language-cpp">#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include &lt;QWidget&gt;
#include &lt;QWebEngineView&gt;

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWidget;
}
QT_END_NAMESPACE

class MainWidget : public QWidget
{
    Q_OBJECT

public:
    explicit MainWidget(QWidget *parent = nullptr);
    ~MainWidget() override;

private:
    Ui::MainWidget *ui;
    QWebEngineView *pQWebEngineView;
};
#endif // MAINWIDGET_H</code></pre>
<p><strong>mainwidget.cpp</strong></p>
<pre><code class="language-cpp">#include &quot;mainwidget.h&quot;
#include &quot;ui_mainwidget.h&quot;

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
{
    ui-&gt;setupUi(this);
    pQWebEngineView = new QWebEngineView(this);
    pQWebEngineView-&gt;load(QUrl(&quot;http://www.naver.com&quot;));
    ui-&gt;verticalLayout_1-&gt;addWidget(pQWebEngineView);
}

MainWidget::~MainWidget()
{
    delete ui;
}</code></pre>
<p>Qt 위젯 안에 네이버 페이지가 정상적으로 로드되면 <code>QWebEngineView</code>가 올바르게 동작하는 것입니다.</p>
<hr />
<h2 id="3-웹캠-스트리밍-단일-화면">3. 웹캠 스트리밍 (단일 화면)</h2>
<p>네이버 URL 대신 Raspberry Pi의 mjpg-streamer 스트림 주소를 로드합니다.</p>
<p><img alt="업로드중.." src="blob:https://velog.io/789052d6-2f1d-407f-aa07-7abf354c18ba" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d8df3ec8-e979-4605-9c04-c0154f52fd69/image.png" /></p>
<p><strong>mainwidget.cpp</strong></p>
<pre><code class="language-cpp">#include &quot;mainwidget.h&quot;
#include &quot;ui_mainwidget.h&quot;

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
{
    ui-&gt;setupUi(this);
    pQWebEngineView = new QWebEngineView(this);
    pQWebEngineView-&gt;load(QUrl(&quot;http://10.10.16.65:8080/?action=stream&quot;));
    ui-&gt;verticalLayout_1-&gt;addWidget(pQWebEngineView);
}

MainWidget::~MainWidget()
{
    delete ui;
}</code></pre>
<hr />
<h2 id="4-웹캠-스트리밍-4분할-화면">4. 웹캠 스트리밍 (4분할 화면)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9a3c5074-b5c4-4f65-9e04-800332c88eb0/image.png" /></p>
<p>UI를 Qt Designer에서 4분할 레이아웃으로 구성한 후 <code>QWebEngineView</code>를 각 영역에 배치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a21a7432-cb0c-440a-8a80-8946dca3e2cc/image.png" /></p>
<blockquote>
<p>Qt Designer에서 <code>QVBoxLayout</code> 4개를 2x2 그리드로 배치합니다.
각 레이아웃의 이름을 <code>verticalLayout_1</code> ~ <code>verticalLayout_4</code> 로 지정합니다.</p>
</blockquote>
<p><strong>mainwidget.h</strong></p>
<pre><code class="language-cpp">private:
    Ui::MainWidget *ui;
    QWebEngineView *pQWebEngineView_1;
    QWebEngineView *pQWebEngineView_2;
    QWebEngineView *pQWebEngineView_3;
    QWebEngineView *pQWebEngineView_4;</code></pre>
<p><strong>mainwidget.cpp</strong></p>
<pre><code class="language-cpp">#include &quot;mainwidget.h&quot;
#include &quot;ui_mainwidget.h&quot;

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
{
    ui-&gt;setupUi(this);

    pQWebEngineView_1 = new QWebEngineView(this);
    pQWebEngineView_1-&gt;load(QUrl(&quot;http://10.10.16.65:8080/?action=stream&quot;));
    ui-&gt;verticalLayout_1-&gt;addWidget(pQWebEngineView_1);

    pQWebEngineView_2 = new QWebEngineView(this);
    pQWebEngineView_2-&gt;load(QUrl(&quot;http://10.10.16.65:8080/?action=stream&quot;));
    ui-&gt;verticalLayout_2-&gt;addWidget(pQWebEngineView_2);

    pQWebEngineView_3 = new QWebEngineView(this);
    pQWebEngineView_3-&gt;load(QUrl(&quot;http://10.10.16.65:8080/?action=stream&quot;));
    ui-&gt;verticalLayout_3-&gt;addWidget(pQWebEngineView_3);

    pQWebEngineView_4 = new QWebEngineView(this);
    pQWebEngineView_4-&gt;load(QUrl(&quot;http://10.10.16.65:8080/?action=stream&quot;));
    ui-&gt;verticalLayout_4-&gt;addWidget(pQWebEngineView_4);
}

MainWidget::~MainWidget()
{
    delete ui;
}</code></pre>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>Raspberry Pi에 웹캠 연결 → mjpg-streamer 실행
    ↓
Ubuntu Qt에서 QWebEngineView URL 테스트 (naver.com)
    ↓
스트림 주소로 변경하여 단일 화면 출력
    ↓
UI 4분할 레이아웃 구성 (Qt Designer)
    ↓
QWebEngineView 4개 생성 및 각 레이아웃에 배치
    ↓
4분할 화면 동시 스트리밍 확인</code></pre>