<blockquote>
<p><a href="https://velog.io/@mommers/Qt-Designer%EB%A1%9C-UI-%EA%B5%AC%EC%84%B1%ED%95%98%EA%B8%B0-mainwidget-Windows-%ED%99%98%EA%B2%BD-8kyg7m8a">이전 글 : Qt) Designer로 UI 구성하기(1) - mainwidget (Windows 환경)</a></p>
</blockquote>
<p>이전 글에서 mainwidget UI를 구성하고 Tab Widget을 추가해봤습니다.</p>
<p>이번 글에서는 Tab1에 배치할 <code>Tab1DeviceControl</code> 클래스를 생성하고 QTimer, QButtonGroup을 구현하는 과정을 정리할 예정입니다.</p>
<p>수업 진도 따라가기 바빠서 중간 과정을 캡쳐를 못해뒀기 때문에 최종 Tab1 결과물에 대해 설명하는 방향으로 정리해보겠습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/03c6bd8c-9776-4503-92e7-b0cc54d0a4c1/image.gif" /></p>
<hr />
<h2 id="1-tab1devicecontrol-클래스-생성">1. Tab1DeviceControl 클래스 생성</h2>
<p>QtCreator에서 새 파일을 추가합니다.</p>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e2dabb34-0b54-4fc9-a6a5-ff83df6142be/image.png" /></p>
<p>Class name을 <code>Tab1DeviceControl</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab1devicecontrol.h</code></li>
<li><code>tab1devicecontrol.cpp</code></li>
<li><code>tab1devicecontrol.ui</code></li>
</ul>
<hr />
<h2 id="2-tab1devicecontrol-ui-구성">2. Tab1DeviceControl UI 구성</h2>
<p><code>tab1devicecontrol.ui</code>를 Qt Designer에서 열고 아래와 같이 위젯을 배치합니다.</p>
<pre><code>=====================================================
| 1 | PB(Start) | C(timervalue) | PB(Quit)          |
| 2 |       DialLED    |     LCDNumber              |
| 3 |              progressBar                      |
| 4 |   4x2 CheckBox Grid   |     LCDNumber(Key)    |
=====================================================</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3a187029-5a35-460c-93a5-81a5c964e780/image.png" /></p>
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
<td>QPushButton</td>
<td>pPBtimerStart</td>
<td>타이머 시작/정지 (Checkable)</td>
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
<tr>
<td>QDial</td>
<td>pDialLed</td>
<td>다이얼 입력</td>
</tr>
<tr>
<td>QLCDNumber</td>
<td>pLcdNumberLed</td>
<td>다이얼 값 표시</td>
</tr>
<tr>
<td>QProgressBar</td>
<td>pProgressBar</td>
<td>다이얼 값 표시</td>
</tr>
<tr>
<td>QGridLayout</td>
<td>gridLayout</td>
<td>체크박스 4x2 배치</td>
</tr>
<tr>
<td>QLCDNumber</td>
<td>pLcdNumberKey</td>
<td>체크박스 상태 표시</td>
</tr>
</tbody></table>
<blockquote>
<p><code>pPBtimerStart</code>는 Property Editor에서 <code>checkable</code>을 체크해야 토글 버튼으로 동작합니다.</p>
</blockquote>
<hr />
<h2 id="3-signalslot-연결-qt-designer">3. Signal/Slot 연결 (Qt Designer)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7b462002-3fe7-4537-ba18-af9ac3514d38/image.png" /></p>
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
<tr>
<td>pDialLed</td>
<td>valueChanged(int)</td>
<td>pProgressBar</td>
<td>setValue(int)</td>
</tr>
</tbody></table>
<hr />
<h2 id="4-tab1devicecontrolh">4. tab1devicecontrol.h</h2>
<pre><code class="language-cpp">#ifndef TAB1DEVICECONTROL_H
#define TAB1DEVICECONTROL_H

#include &lt;QWidget&gt;
#include &lt;QTimer&gt;
#include &lt;QDial&gt;
#include &lt;QComboBox&gt;
#include &lt;QLCDNumber&gt;
#include &lt;QProgressBar&gt;
#include &lt;QCheckBox&gt;
#include &lt;QButtonGroup&gt;
#include &lt;QDebug&gt;

namespace Ui {
class Tab1DeviceControl;
}

class Tab1DeviceControl : public QWidget
{
    Q_OBJECT

public:
    explicit Tab1DeviceControl(QWidget *parent = nullptr);
    ~Tab1DeviceControl();

private slots:
    void on_pPBquit_clicked();
    void timerStartSlot(bool);
    void updateDialValueSlot();
    void updateComboSlot(QString strValue);
    void updateCheckBoxSlot(int);

private:
    Ui::Tab1DeviceControl *ui;
    QTimer *pQTimer;
    QCheckBox *pQCheckBox[8];
    QButtonGroup *pQButtonGroup;
    unsigned char lcdDataKey;
};

#endif // TAB1DEVICECONTROL_H</code></pre>
<hr />
<h2 id="5-tab1devicecontrolcpp">5. tab1devicecontrol.cpp</h2>
<h3 id="5-1-생성자---초기화-및-signalslot-연결">5-1. 생성자 - 초기화 및 Signal/Slot 연결</h3>
<pre><code class="language-cpp">#include &quot;tab1devicecontrol.h&quot;
#include &quot;ui_tab1devicecontrol.h&quot;
#include &lt;QTimer&gt;
#include &lt;QButtonGroup&gt;

Tab1DeviceControl::Tab1DeviceControl(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Tab1DeviceControl)
{
    ui-&gt;setupUi(this);

    // gridLayout의 체크박스를 배열에 저장
    int keyCount = ui-&gt;gridLayout-&gt;rowCount() * ui-&gt;gridLayout-&gt;columnCount();
    for(int i = 0; i &lt; ui-&gt;gridLayout-&gt;rowCount(); i++)
    {
        for(int j = 0; j &lt; ui-&gt;gridLayout-&gt;columnCount(); j++)
        {
            pQCheckBox[--keyCount] = dynamic_cast&lt;QCheckBox*&gt;(
                ui-&gt;gridLayout-&gt;itemAtPosition(i, j)-&gt;widget());
        }
    }

    // QTimer 생성
    pQTimer = new QTimer(this);

    // QButtonGroup 생성 및 체크박스 등록
    pQButtonGroup = new QButtonGroup(this);
    pQButtonGroup-&gt;setExclusive(false);

    keyCount = ui-&gt;gridLayout-&gt;rowCount() * ui-&gt;gridLayout-&gt;columnCount();
    for(int i = 0; i &lt; keyCount; i++)
    {
        pQButtonGroup-&gt;addButton(pQCheckBox[i], i + 1);
    }

    // Signal/Slot 연결
    connect(pQButtonGroup, SIGNAL(idClicked(int)), this, SLOT(updateCheckBoxSlot(int)));
    connect(pQTimer, SIGNAL(timeout()), this, SLOT(updateDialValueSlot()));
    connect(ui-&gt;pCtimerValue, SIGNAL(currentTextChanged(QString)), this, SLOT(updateComboSlot(QString)));
    connect(ui-&gt;pPBtimerStart, SIGNAL(clicked(bool)), this, SLOT(timerStartSlot(bool)));
}

Tab1DeviceControl::~Tab1DeviceControl()
{
    delete ui;
}</code></pre>
<h3 id="5-2-quit-버튼">5-2. Quit 버튼</h3>
<pre><code class="language-cpp">void Tab1DeviceControl::on_pPBquit_clicked()
{
    qApp-&gt;exit();
}</code></pre>
<h3 id="5-3-타이머-시작정지">5-3. 타이머 시작/정지</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/392b5954-2241-49de-ae8b-70539b0e3441/image.gif" /></p>
<p><code>pPBtimerStart</code>는 checkable 버튼으로, 클릭 시 <code>bool</code> 값을 전달합니다.</p>
<pre><code class="language-cpp">void Tab1DeviceControl::timerStartSlot(bool bFlag)
{
    if(bFlag)
    {
        QString strValue = ui-&gt;pCtimerValue-&gt;currentText();
        pQTimer-&gt;start(strValue.toInt());
        ui-&gt;pPBtimerStart-&gt;setText(&quot;TimerStop&quot;);
    }
    else
    {
        pQTimer-&gt;stop();
        ui-&gt;pPBtimerStart-&gt;setText(&quot;TimerStart&quot;);
    }
}</code></pre>
<h3 id="5-4-타이머-timeout---dial-값-자동-증가">5-4. 타이머 timeout - Dial 값 자동 증가</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2de9372e-1c11-4cb8-bfdd-b9cdbc0edf10/image.gif" /></p>
<p>타이머가 동작하는 동안 Dial 값을 1씩 증가시킵니다.
최댓값을 초과하면 0으로 초기화합니다.</p>
<pre><code class="language-cpp">void Tab1DeviceControl::updateDialValueSlot()
{
    int dialValue = ui-&gt;pDialLed-&gt;value();
    dialValue++;
    if(dialValue &gt; ui-&gt;pDialLed-&gt;maximum())
    {
        dialValue = 0;
    }
    ui-&gt;pDialLed-&gt;setValue(dialValue);
}</code></pre>
<h3 id="5-5-combobox-값-변경---타이머-간격-업데이트">5-5. ComboBox 값 변경 - 타이머 간격 업데이트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aeb69473-2096-4d09-83d5-e5e15796d22b/image.gif" /></p>
<p>타이머가 동작 중일 때 ComboBox 값이 변경되면 타이머 간격을 즉시 업데이트합니다.</p>
<pre><code class="language-cpp">void Tab1DeviceControl::updateComboSlot(QString strValue)
{
    if(pQTimer-&gt;isActive())
    {
        pQTimer-&gt;stop();
        pQTimer-&gt;start(strValue.toInt());
    }
}</code></pre>
<h3 id="5-6-checkbox-상태---lcd-표시">5-6. CheckBox 상태 - LCD 표시</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/14ee3572-1cfc-480f-b506-ca5727147890/image.gif" /></p>
<p>체크박스를 클릭하면 해당 비트를 XOR 연산으로 토글하여 LCD에 표시합니다.</p>
<pre><code class="language-cpp">void Tab1DeviceControl::updateCheckBoxSlot(int keyNum)
{
    qDebug() &lt;&lt; keyNum;
    lcdDataKey = lcdDataKey ^ (0x01 &lt;&lt; keyNum - 1);
    ui-&gt;pLcdNumberKey-&gt;display(lcdDataKey);
}</code></pre>
<blockquote>
<p>체크박스 8개가 각각 1~8번 ID로 등록되어 있으며, 클릭 시 해당 비트가 토글됩니다.</p>
</blockquote>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>Tab1DeviceControl 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
tab1devicecontrol.ui에서 위젯 배치
    ↓
Qt Designer에서 Dial → LCD, Dial → ProgressBar Signal/Slot 연결
    ↓
생성자에서 QTimer, QButtonGroup 초기화
    ↓
체크박스 배열 등록 (gridLayout에서 동적 추출)
    ↓
Signal/Slot 연결 (타이머, 콤보박스, 체크박스)
    ↓
각 Slot 구현 (타이머 시작/정지, Dial 자동 증가, 체크박스 LCD 표시)</code></pre>