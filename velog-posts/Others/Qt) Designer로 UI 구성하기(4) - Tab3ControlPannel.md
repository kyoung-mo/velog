<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner3">이전 글 : Qt) Designer로 UI 구성하기(3) - Tab2SocketClient</a></p>
</blockquote>
<p>이전 글에서 Tab2SocketClient 클래스를 구현하였습니다.</p>
<p>이번 글에서는 이미지 리소스를 활용한 <code>Tab3ControlPannel</code> 클래스를 구현하는 과정을 정리하겠습니다.
배경 이미지와 아이콘 이미지를 위젯에 적용하고, <code>QPalette</code>로 버튼 색상을 제어하며, 소켓 메시지를 통해 원격으로 lamp/plug 상태를 제어합니다.</p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5997f0da-4d48-4ef2-a285-2853e55fdf26/image.gif" /></p>
<h2 id="1-tab3controlpannel-클래스-생성">1. Tab3ControlPannel 클래스 생성</h2>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p>Class name을 <code>Tab3ControlPannel</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab3controlpannel.h</code></li>
<li><code>tab3controlpannel.cpp</code></li>
<li><code>tab3controlpannel.ui</code></li>
</ul>
<hr />
<h2 id="2-이미지-리소스-추가">2. 이미지 리소스 추가</h2>
<p>UI에 사용할 이미지 파일을 프로젝트 리소스로 등록합니다.
사용하는 이미지는 아래와 같습니다.</p>
<p>이미지는 깃허브에 올려놓겠습니다.
<a href="https://github.com/kyoung-mo/qt-study/tree/main/AiotClient_tab7/Images">github : kyoungmo / images source</a></p>
<table>
<thead>
<tr>
<th>이미지 파일</th>
<th>용도</th>
</tr>
</thead>
<tbody><tr>
<td>room1.png</td>
<td>배경 이미지</td>
</tr>
<tr>
<td>light_off.png</td>
<td>전등 버튼 기본 상태 아이콘</td>
</tr>
<tr>
<td>light_on.png</td>
<td>전등 버튼 ON 상태 아이콘</td>
</tr>
<tr>
<td>plug_off.png</td>
<td>플러그 버튼 기본 상태 아이콘</td>
</tr>
<tr>
<td>plug_on.png</td>
<td>플러그 버튼 ON 상태 아이콘</td>
</tr>
</tbody></table>
<hr />
<h2 id="3-tab3controlpannel-ui-구성-designer">3. Tab3ControlPannel UI 구성 (Designer)</h2>
<p><code>tab3controlpannel.ui</code>를 Qt Designer에서 열고 위젯을 배치합니다.</p>
<h3 id="3-1-qlabel---배경-이미지-설정">3-1. QLabel - 배경 이미지 설정</h3>
<p><code>QLabel</code>을 캔버스에 배치하고 Property Editor에서 <code>pixmap</code>에 <code>room1.png</code>를 지정합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0f56ed76-eab2-4642-9a54-41439873348a/image.png" /></p>
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
<td>label</td>
<td>배경 이미지 표시</td>
</tr>
</tbody></table>
<h3 id="3-2-qpushbutton---전등-버튼-아이콘-설정">3-2. QPushButton - 전등 버튼 아이콘 설정</h3>
<p><code>QPushButton</code>을 배치하고 Property Editor에서 <code>icon</code>에 이미지를 지정합니다.</p>
<ul>
<li><strong>Normal Off</strong> : <code>light_off.png</code></li>
<li><strong>Normal On</strong> : <code>light_on.png</code></li>
<li><code>iconSize</code> : 70 x 70</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3f2918da-5e79-4a25-a129-6d068e7d7261/image.png" /></p>
<blockquote>
<p><code>checkable</code>을 체크하면 Normal Off / Normal On 상태에 따라 아이콘이 자동으로 전환됩니다.</p>
</blockquote>
<h3 id="3-3-qpushbutton---플러그-버튼-아이콘-설정">3-3. QPushButton - 플러그 버튼 아이콘 설정</h3>
<p>전등 버튼과 동일한 방식으로 플러그 버튼을 설정합니다.</p>
<ul>
<li><strong>Normal Off</strong> : <code>plug_off.png</code></li>
<li><strong>Normal On</strong> : <code>plug_on.png</code></li>
<li><code>iconSize</code> : 70 x 70</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b322c57d-e0bb-416a-bcdb-7a55626535af/image.png" /></p>
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
<td>label</td>
<td>배경 이미지</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBlamp</td>
<td>전등 ON/OFF (Checkable)</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBplug</td>
<td>플러그 ON/OFF (Checkable)</td>
</tr>
</tbody></table>
<h3 id="3-4-qscrollarea로-감싸기">3-4. QScrollArea로 감싸기</h3>
<p>위젯 전체를 <code>QScrollArea</code>로 감싸서 화면 크기에 따라 스크롤이 가능하도록 합니다.</p>
<p>Widget Box에서 <strong>Scroll Area</strong>를 검색하여 캔버스에 추가한 뒤, 기존 위젯들을 내부로 이동합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fbe4e13c-a1ac-4085-9156-63dd36c9dcbc/image.png" /></p>
<p>Object Inspector에서 최종 구조를 확인합니다.</p>
<pre><code>Tab3ControlPannel (QWidget)
└── scrollArea (QScrollArea)
    └── scrollAreaWidgetContents (QWidget)
        ├── label (QLabel)
        ├── pPBlamp (QPushButton)
        └── pPBplug (QPushButton)</code></pre><hr />
<h2 id="4-tab3controlpannel-코드">4. Tab3ControlPannel 코드</h2>
<h3 id="tab3controlpannelh">tab3controlpannel.h</h3>
<p><code>QPalette</code>를 멤버 변수로 선언하여 버튼 색상 ON/OFF 상태를 관리합니다.
버튼 클릭 시 소켓으로 메시지를 보내기 위한 <code>socketSendDataSig</code> 시그널과,
수신 메시지를 처리할 <code>tab3RecvDataSlot</code>을 선언합니다.</p>
<pre><code class="language-cpp">signals:
    void socketSendDataSig(QString);

public slots:
    void tab3RecvDataSlot(QStringList&amp;);

private:
    QPalette paletteOn;
    QPalette paletteOff;</code></pre>
<h3 id="생성자---qpalette-초기화">생성자 - QPalette 초기화</h3>
<p>생성자에서 ON/OFF 상태의 팔레트 색상을 미리 설정합니다.</p>
<pre><code class="language-cpp">paletteOn.setColor(ui-&gt;pPBlamp-&gt;backgroundRole(), QColor(255, 0, 0));  // 빨강
paletteOff.setColor(ui-&gt;pPBlamp-&gt;backgroundRole(), QColor(0, 0, 255)); // 파랑
ui-&gt;pPBlamp-&gt;setPalette(paletteOff);
ui-&gt;pPBplug-&gt;setPalette(paletteOff);</code></pre>
<p>초기 상태에서 두 버튼 모두 <code>paletteOff</code>(파란색)으로 설정됩니다.</p>
<h3 id="버튼-클릭-슬롯---소켓-메시지-송신">버튼 클릭 슬롯 - 소켓 메시지 송신</h3>
<p>버튼 클릭 시 <code>socketSendDataSig</code> 시그널로 소켓 메시지를 emit합니다.
<code>checked</code> 상태에 따라 ON/OFF 메시지를 구분하여 전송합니다.</p>
<pre><code class="language-cpp">void Tab3ControlPannel::on_pPBlamp_clicked(bool checked)
{
    if(checked)
    {
        ui-&gt;pPBlamp-&gt;setChecked(true);
        emit socketSendDataSig(&quot;[KYM_LIN]LAMPON&quot;);
        ui-&gt;pPBlamp-&gt;setPalette(paletteOn);
    }
    else
    {
        ui-&gt;pPBlamp-&gt;setChecked(false);
        emit socketSendDataSig(&quot;[KYM_LIN]LAMPOFF&quot;);
        ui-&gt;pPBlamp-&gt;setPalette(paletteOff);
    }
}

void Tab3ControlPannel::on_pPBplug_clicked(bool checked)
{
    if(checked)
    {
        ui-&gt;pPBplug-&gt;setChecked(true);
        emit socketSendDataSig(&quot;[KYM_LIN]PLUGON&quot;);

        ui-&gt;pPBplug-&gt;setPalette(paletteOn);
    }
    else
    {
        ui-&gt;pPBplug-&gt;setChecked(false);
        emit socketSendDataSig(&quot;[KYM_LIN]PLUGOFF&quot;);
        ui-&gt;pPBplug-&gt;setPalette(paletteOff);
    }
}</code></pre>
<blockquote>
<p>Tab2에서 파싱된 <code>QStringList</code>를 참조 타입으로 전달받아 버튼 상태와 팔레트를 업데이트합니다.</p>
</blockquote>
<hr />
<h2 id="5-mainwidget에-tab3-추가">5. mainwidget에 Tab3 추가</h2>
<h3 id="tab-페이지-추가">Tab 페이지 추가</h3>
<p><code>mainwidget.ui</code>를 열고 Tab Widget에 Tab3 페이지를 추가합니다.</p>
<p><strong>Tab Widget 우클릭 → Insert Page → After Current Page</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/723b29d5-9f62-42b3-9a48-74c786968c5d/image.png" /></p>
<p>추가된 Tab 페이지의 objectName을 <code>pTab3</code>으로 설정합니다.</p>
<h3 id="mainwidgeth">mainwidget.h</h3>
<p><code>tab3controlpannel.h</code>를 include하고 <code>Tab3ControlPannel</code> 포인터를 선언합니다.</p>
<pre><code class="language-cpp">#include &lt;tab3controlpannel.h&gt;

Tab3ControlPannel *pTab3ControlPannel;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<p><code>Tab3ControlPannel</code> 객체를 생성하여 <code>pTab3</code>에 배치하고, Tab2와 Signal/Slot을 연결합니다.</p>
<pre><code class="language-cpp">pTab3ControlPannel = new Tab3ControlPannel(ui-&gt;pTab3);
ui-&gt;pTab3-&gt;setLayout(pTab3ControlPannel-&gt;layout());

connect(pTab3ControlPannel, SIGNAL(socketSendDataSig(QString)),
        pTab2SocketClient, SLOT(socketWriteDataSlot(QString)));
connect(pTab2SocketClient, SIGNAL(tab3RecvDataSig(QStringList&amp;)),
        pTab3ControlPannel, SLOT(tab3RecvDataSlot(QStringList&amp;)));</code></pre>
<p>Tab3의 버튼 클릭 → Tab2를 통해 소켓 송신, Tab2에서 수신한 메시지 → Tab3 버튼 상태 업데이트로 연결됩니다.</p>
<h3 id="tab2socketclientcpp---수신-메시지-파싱-및-라우팅">tab2socketclient.cpp - 수신 메시지 파싱 및 라우팅</h3>
<p>Tab2의 <code>updateRecvDataSlot</code>에서 수신된 문자열을 파싱하여 Tab3로 전달합니다.</p>
<pre><code class="language-cpp">void Tab2SocketClient::updateRecvDataSlot(QString strRecvData)
{
    strRecvData.chop(1);    // '\n' 제거
    QTime time = QTime::currentTime();
    QString strTime = time.toString() + &quot; &quot; + strRecvData;
    ui-&gt;pTErecvData-&gt;append(strTime);

    // [KYM_LIN]LAMPON → &quot;@KYM_LIN@LAMPON@&quot;으로 변환 후 split
    strRecvData.replace(&quot;[&quot;, &quot;@&quot;);
    strRecvData.replace(&quot;]&quot;, &quot;@&quot;);
    QStringList strList = strRecvData.split(&quot;@&quot;);
    // strList[0] = &quot;&quot;
    // strList[1] = &quot;KYM_LIN&quot;
    // strList[2] = &quot;LAMPON&quot;

    if((strList[2].indexOf(&quot;LAMP&quot;) == 0) || (strList[2].indexOf(&quot;PLUG&quot;) == 0))
        emit tab3RecvDataSig(strList);
}</code></pre>
<p><code>LAMP</code> 또는 <code>PLUG</code>로 시작하는 메시지는 <code>tab3RecvDataSig</code>로 emit하여 Tab3로 전달합니다.</p>
<hr />
<h2 id="6-실행-결과">6. 실행 결과</h2>
<p>빌드 후 실행하면 Tab3에 배경 이미지와 아이콘 버튼이 정상적으로 표시됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8d6a0cff-d256-4183-a80f-5ee4d969fc83/image.gif" /></p>
<p>버튼 클릭 시 소켓 메시지가 전송되고, 서버로부터 응답이 돌아오면 아이콘과 배경색이 전환됩니다.</p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>Tab3ControlPannel 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
이미지 리소스 추가 (배경, 아이콘)
    ↓
QLabel에 room1.png 배경 이미지 설정
    ↓
QPushButton에 아이콘 이미지 설정 (Normal Off / Normal On)
    ↓
QScrollArea로 전체 위젯 감싸기
    ↓
생성자에서 QPalette 초기화
    ↓
버튼 클릭 슬롯에서 socketSendDataSig emit
    ↓
tab3RecvDataSlot에서 수신 메시지 파싱 및 버튼 상태 변경
    ↓
mainwidget.ui에서 Tab3 페이지 추가
    ↓
mainwidget에서 Tab3ControlPannel 객체 생성 및 Tab2와 Signal/Slot 연결</code></pre>