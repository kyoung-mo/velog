<p><code>Qt Designer</code>를 사용하여 <code>mainwidget UI</code>를 단계적으로 구성하는 과정을 정리하였습니다. 위젯 배치부터 Signal/Slot 연결까지 순서대로 진행하겠습니다.</p>
<hr />
<h2 id="1-프로젝트-구조">1. 프로젝트 구조</h2>
<p>이번 글에서 구성하는 UI의 최종 구조는 다음과 같습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4ac095d8-f9c0-4dda-b158-2a8fad99074f/image.png" /></p>
<pre><code>MainWidget (QWidget)
└── Tab Widget
    ├── Tab 1 (pTab1) → Tab1DeviceControl 객체 배치 예정
    └── Tab 2 (pTab2)</code></pre><p><code>Tab1DeviceControl</code> 구현은 다음 글에서 진행합니다.
이번 글에서는 mainwidget의 기본 UI 구성과 Signal/Slot 연결에 집중합니다.</p>
<p><code>verticalLayout</code> 안에 가로 줄 4개(각각의 <code>horizontalLayout</code>)를 넣어주는 것이 큰 틀입니다.</p>
<pre><code>============================================
| 1 | PB(Start) | C(timervalue) | PB(Quit) |
| 2 |       DialLED    |     LCDNumber     |
| 3 |              progressBar             |
| 4 |       4*2 CB     |     LCDNumber     |
============================================</code></pre><ul>
<li>PB : <code>QPushButton</code></li>
<li>C : <code>QComboBox</code></li>
<li>CB : <code>QCheckBox</code></li>
</ul>
<hr />
<h2 id="2-위젯-배치">2. 위젯 배치</h2>
<h3 id="2-1-1번째-줄---상단-버튼-영역">2-1. 1번째 줄 - 상단 버튼 영역</h3>
<p><code>horizontalLayout</code>을 만들고 아래 위젯 3개를 배치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/40439f02-a7c7-4da3-9af6-de7228100888/image.png" /></p>
<table>
<thead>
<tr>
<th>위젯</th>
<th>objectName</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>QPushButton</td>
<td>pPBtimerStart</td>
<td>타이머 시작/정지</td>
</tr>
<tr>
<td>QComboBox</td>
<td>pCtimerValue</td>
<td>타이머 간격 선택</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBquit</td>
<td>앱 종료</td>
</tr>
</tbody></table>
<blockquote>
<p>objectName 앞에 <code>p</code>가 붙는 이유는 코드에서 포인터로 사용하기 때문입니다.</p>
</blockquote>
<p><code>horizontalLayout</code>의 <code>layoutStretch</code>를 <code>0,0,0</code> → <code>2,2,1</code>로 수정합니다.</p>
<h3 id="2-2-2번째-줄---dial--lcdnumber-영역">2-2. 2번째 줄 - Dial + LCDNumber 영역</h3>
<p><code>horizontalLayout_2</code>를 만들고 아래 위젯 2개를 배치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1f6e93e5-45e1-4d48-b3d4-5f34005e1316/image.png" /></p>
<table>
<thead>
<tr>
<th>위젯</th>
<th>objectName</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>QDial</td>
<td>pDialLed</td>
<td>다이얼 입력</td>
</tr>
<tr>
<td>QLCDNumber</td>
<td>pLcdNumberLed</td>
<td>다이얼 값 표시</td>
</tr>
</tbody></table>
<h3 id="2-3-3번째-줄---progressbar-영역">2-3. 3번째 줄 - ProgressBar 영역</h3>
<p><code>QProgressBar</code> 하나를 배치합니다.
나중에 크기 조정을 쉽게 하기 위해 <code>verticalLayout</code> 안에 넣어줍니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6d103510-cdc3-4e37-be78-a38989362e9f/image.png" /></p>
<table>
<thead>
<tr>
<th>위젯</th>
<th>objectName</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>QProgressBar</td>
<td>pProgressBar</td>
<td>다이얼 값 표시</td>
</tr>
</tbody></table>
<h3 id="2-4-전체-레이아웃-합치기">2-4. 전체 레이아웃 합치기</h3>
<p><code>verticalLayout_2</code>를 만들고 위에서 만든 레이아웃들을 순서대로 배치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bf995593-d64e-4484-9fa1-01837e6ae510/image.png" /></p>
<pre><code>verticalLayout_2
├── horizontalLayout   (1번째 줄)
├── horizontalLayout_2 (2번째 줄)
└── verticalLayout     (3번째 줄 - progressBar)</code></pre><p><code>verticalLayout_2</code>의 <code>layoutStretch</code>를 <code>0,0,0</code> → <code>1,8,1</code>로 설정합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/04f25386-49df-4c1f-9338-3e8ee86406e3/image.png" /></p>
<p>이후 MainWidget 우클릭 → <strong>Layout → Lay Out Vertically</strong> 를 선택하면 화면 비율이 전체 크기에 맞게 설정됩니다.</p>
<hr />
<h2 id="3-signalslot-연결-qt-designer">3. Signal/Slot 연결 (Qt Designer)</h2>
<p>Qt Designer의 <strong>Signals and Slots Editor</strong> 탭에서 코드 없이 위젯 간 Signal/Slot을 연결할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0f323a08-ca72-4b4c-b8db-3ef61cff6979/image.png" /></p>
<h3 id="dial-→-lcdnumber">Dial → LCDNumber</h3>
<table>
<thead>
<tr>
<th>Sender</th>
<th>Signal</th>
<th>Receiver</th>
<th>Slot</th>
</tr>
</thead>
<tbody><tr>
<td>pDialLed</td>
<td>valueChanged(int)</td>
<td>pLcdNumberLed</td>
<td>display(int)</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1b302dc7-9df2-49b7-9363-6b4556e77d4e/image.png" /></p>
<h3 id="dial-→-progressbar">Dial → ProgressBar</h3>
<table>
<thead>
<tr>
<th>Sender</th>
<th>Signal</th>
<th>Receiver</th>
<th>Slot</th>
</tr>
</thead>
<tbody><tr>
<td>pDialLed</td>
<td>valueChanged(int)</td>
<td>pProgressBar</td>
<td>setValue(int)</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/78340c77-cb4a-4a04-8d00-753a9837a431/image.png" /></p>
<p>설정을 완료하면 이렇게 구성됩니다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/ff93d729-3872-4748-b2bf-a59e1baebfb7/image.png" /></p>
<hr />
<h2 id="4-tab-widget-추가">4. Tab Widget 추가</h2>
<p><code>MainWidget</code>에 작성된 파일들을 <code>Tab1DeviceControl</code>로 옮기기 위해, <code>Qt Widgets Designer From Class</code> 로 선택하여 아래 사진과 같이 New File을 생성합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/85db23ee-61df-4e07-abd6-d10e81426ff8/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5b6892f6-4013-4bed-893e-78771de36e19/image.png" /></p>
<p>아래 사진은 오타입니다. <code>Tab1DeviceControl</code>로 class name을 작성하시면 됩니다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/830fbfe0-b826-49d9-ad5a-1e225825ff30/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1c5bf0ed-b994-457f-bdeb-29e75089f184/image.png" /></p>
<p>Widget Box에서 <strong>Tab Widget</strong>을 캔버스에 드래그합니다.
Tab 페이지의 objectName을 각각 <code>pTab1</code>, <code>pTab2</code>로 설정합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6e9f8e39-47ac-4e02-ad34-8b95c109842a/image.png" /></p>
<blockquote>
<p>Tab1에는 다음 글에서 Tab1DeviceControl 객체를 배치할 예정입니다.</p>
</blockquote>
<hr />
<h2 id="5-mainwidget-코드">5. mainwidget 코드</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<pre><code class="language-cpp">#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include &lt;QWidget&gt;
#include &quot;tab1devicecontrol.h&quot;

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
    Tab1DeviceControl *pTab1DeviceControl;
};
#endif // MAINWIDGET_H</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<pre><code class="language-cpp">#include &quot;mainwidget.h&quot;
#include &quot;ui_mainwidget.h&quot;
#include &lt;QVBoxLayout&gt;

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainWidget)
{
    ui-&gt;setupUi(this);
    pTab1DeviceControl = new Tab1DeviceControl(ui-&gt;pTab1);
    QVBoxLayout *layout = new QVBoxLayout(ui-&gt;pTab1);
    layout-&gt;addWidget(pTab1DeviceControl);
    ui-&gt;pTab1-&gt;setLayout(layout);
}

MainWidget::~MainWidget()
{
    delete ui;
}</code></pre>
<blockquote>
<p><code>Tab1DeviceControl</code> 객체를 생성하여 <code>pTab1</code> 위젯에 <code>QVBoxLayout</code>으로 배치합니다.</p>
</blockquote>