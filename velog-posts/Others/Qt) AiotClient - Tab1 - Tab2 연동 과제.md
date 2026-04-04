<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner4">이전 글 : Qt) Designer로 UI 구성하기(4) - Tab3ControlPannel</a></p>
</blockquote>
<p>이전 글까지 Tab1 ~ Tab3까지 구현해봤습니다. </p>
<p>이번 글에서는 Tab1과 Tab2 사이에서 교수님이 내주신 과제 2개를 정리하겠습니다. 과제를 구현하면서 Signal / Slot에 대해 확실히 이해하게 되어 함께 정리해보려 합니다.</p>
<hr />
<h2 id="1-과제-내용">1. 과제 내용</h2>
<h3 id="과제-1---다이얼-값-송신">과제 1 - 다이얼 값 송신</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/047f338f-adda-4d29-9cc6-fe6114f4b3b8/image.gif" /></p>
<p>Tab1에서 다이얼 값이 변화할 때마다 Tab2 소켓을 통해 <code>KYM_LIN</code> 클라이언트에게 아래 형식으로 메시지를 전송합니다.</p>
<pre><code>[KYM_LIN]DIAL@{0~255}</code></pre><h3 id="과제-2---체크박스-원격-제어">과제 2 - 체크박스 원격 제어</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9e6f4e36-4c10-4daa-a902-0ab490995a83/image.gif" /></p>
<p>서버에 접속한 상태에서 <code>KYM_QT</code>가 아래 형식의 메시지를 수신하면, Tab1의 해당 번호 체크박스를 ON 또는 OFF로 설정합니다.</p>
<pre><code>[KYM_QT]KEY@{1~8}@ON
[KYM_QT]KEY@{1~8}@OFF</code></pre><hr />
<h2 id="2-signal--slot-이란">2. Signal / Slot 이란?</h2>
<p>Signal / Slot은 <strong>어떠한 원하는 동작이 발생했을 때, Slot 함수를 실행시킨다</strong> 라고 생각하면 됩니다.</p>
<p>예를 들어 과제 1번에서, Tab1의 다이얼 값에 변화가 생겼다는 Signal이 발생했을 때 Tab2의 어떤 Slot 함수를 실행시킨다고 이해하면 됩니다.</p>
<p>Signal / Slot의 흐름은 아래와 같습니다.</p>
<pre><code>Tab1에서 emit 뒤에 Signal 내용 작성
    ↓
mainwidget에서 connect 함수 작성
    ↓
connect 함수에 맞는 Slot 함수를 Tab2에서 구현</code></pre><p>즉 Signal을 발생시키는 쪽(<code>emit</code>)과 이를 받아 처리하는 쪽(<code>Slot</code>)을 <code>mainwidget</code>의 <code>connect</code>로 연결하는 구조입니다.</p>
<hr />
<h2 id="3-과제-1-구현---다이얼-값-송신">3. 과제 1 구현 - 다이얼 값 송신</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7c22883f-cf5c-4ec8-a421-0e7eb73cf205/image.gif" /></p>
<h3 id="tab1devicecontrolh">tab1devicecontrol.h</h3>
<p>다이얼 값 변화 슬롯과 소켓 송신 시그널을 선언합니다.</p>
<pre><code class="language-cpp">private slots:
    void on_pDialLed_valueChanged(int value);

signals:
    void socketSendDataSig(QString);</code></pre>
<h3 id="tab1devicecontrolcpp">tab1devicecontrol.cpp</h3>
<p>다이얼 값이 변경될 때마다 <code>[KYM_LIN]DIAL@값</code> 형식으로 시그널을 emit합니다.</p>
<pre><code class="language-cpp">void Tab1DeviceControl::on_pDialLed_valueChanged(int value)
{
    QString strData = &quot;[KYM_LIN]DIAL@&quot; + QString::number(value);
    emit socketSendDataSig(strData);
}</code></pre>
<blockquote>
<p><code>on_pDialLed_valueChanged</code>는 Qt Designer에서 자동 연결되는 슬롯으로, 다이얼 값이 변할 때마다 호출됩니다.</p>
</blockquote>
<h3 id="mainwidgetcpp---connect-연결">mainwidget.cpp - connect 연결</h3>
<p>Tab1의 시그널을 Tab2의 소켓 송신 슬롯에 연결합니다.</p>
<pre><code class="language-cpp">connect(pTab1DeviceControl, SIGNAL(socketSendDataSig(QString)),
        pTab2SocketClient, SLOT(socketWriteDataSlot(QString)));</code></pre>
<hr />
<h2 id="4-과제-2-구현---체크박스-원격-제어">4. 과제 2 구현 - 체크박스 원격 제어</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9e6f4e36-4c10-4daa-a902-0ab490995a83/image.gif" /></p>
<h3 id="tab2socketclientcpp---수신-메시지-파싱">tab2socketclient.cpp - 수신 메시지 파싱</h3>
<p>Tab2의 <code>updateRecvDataSlot</code>에서 수신된 문자열을 파싱하여 Tab1으로 전달합니다.</p>
<pre><code class="language-cpp">strRecvData.replace(&quot;[&quot;, &quot;@&quot;);
strRecvData.replace(&quot;]&quot;, &quot;@&quot;);
QStringList strList = strRecvData.split(&quot;@&quot;);
// strList[0] = &quot;&quot;
// strList[1] = &quot;KYM_QT&quot;
// strList[2] = &quot;KEY&quot;
// strList[3] = &quot;1&quot;     ← 체크박스 번호
// strList[4] = &quot;ON&quot;    ← ON / OFF

if(strList[2] == &quot;KEY&quot;)
    emit tab1RecvDataSig(strList);</code></pre>
<h3 id="tab2socketclienth---시그널-선언">tab2socketclient.h - 시그널 선언</h3>
<pre><code class="language-cpp">signals:
    void tab1RecvDataSig(QStringList&amp;);</code></pre>
<h3 id="tab1devicecontrolh---슬롯-선언">tab1devicecontrol.h - 슬롯 선언</h3>
<pre><code class="language-cpp">public slots:
    void tab1RecvDataSlot(QStringList&amp;);</code></pre>
<h3 id="tab1devicecontrolcpp---체크박스-제어">tab1devicecontrol.cpp - 체크박스 제어</h3>
<p>파싱된 <code>QStringList</code>에서 체크박스 번호와 ON/OFF 상태를 추출하여 해당 체크박스를 설정합니다.</p>
<pre><code class="language-cpp">void Tab1DeviceControl::tab1RecvDataSlot(QStringList&amp; strList)
{
    bool keyFlag;
    int keyNumber = strList[3].toInt();

    if(keyNumber &lt; 1 || 8 &lt; keyNumber)
        return;
    else
        keyNumber--;

    if(strList[4] == &quot;ON&quot;)
        keyFlag = true;
    else
        keyFlag = false;

    pQCheckBox[keyNumber]-&gt;setChecked(keyFlag);
    updateCheckBoxSlot(++keyNumber);
}</code></pre>
<h3 id="mainwidgetcpp---connect-연결-1">mainwidget.cpp - connect 연결</h3>
<p>Tab2의 시그널을 Tab1의 슬롯에 연결합니다.</p>
<pre><code class="language-cpp">connect(pTab2SocketClient, SIGNAL(tab1RecvDataSig(QStringList&amp;)),
        pTab1DeviceControl, SLOT(tab1RecvDataSlot(QStringList&amp;)));</code></pre>
<hr />
<h2 id="5-전체-signal--slot-흐름-요약">5. 전체 Signal / Slot 흐름 요약</h2>
<h3 id="과제-1-흐름">과제 1 흐름</h3>
<pre><code>[Tab1] 다이얼 값 변화
    ↓ on_pDialLed_valueChanged(int value)
    ↓ emit socketSendDataSig(&quot;[KYM_LIN]DIAL@값&quot;)
    ↓ mainwidget connect
[Tab2] socketWriteDataSlot(QString)
    ↓ 소켓 송신</code></pre><h3 id="과제-2-흐름">과제 2 흐름</h3>
<pre><code>소켓 수신
    ↓ [Tab2] updateRecvDataSlot(QString)
    ↓ 문자열 파싱 → QStringList
    ↓ emit tab1RecvDataSig(strList)
    ↓ mainwidget connect
[Tab1] tab1RecvDataSlot(QStringList&amp;)
    ↓ 체크박스 번호 추출 및 ON/OFF 설정</code></pre>