<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner2">이전 글 : Qt) Designer로 UI 구성하기(2) - Tab1DeviceControl</a></p>
</blockquote>
<p>이전 글에서 Tab1DeviceControl 클래스를 구현하였습니다.</p>
<p>이번 글에서는 TCP 소켓 통신을 담당하는 <code>SocketClient</code> 클래스와, 이를 UI로 감싸는 <code>Tab2SocketClient</code> 클래스를 구현하는 과정을 정리하겠습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b4a7437f-eea2-4574-be8c-fde1f43a356d/image.png" /></p>
<hr />
<h2 id="1-서버에-kym_qt-id-등록-확인">1. 서버에 KYM_QT ID 등록 확인</h2>
<p><code>iot_server</code>는 클라이언트 접속 시 ID/PW를 검증합니다.
서버 코드의 <code>CLIENT_INFO</code> 배열에서 <code>KYM_QT</code>가 등록되어 있는지 먼저 확인합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1c3edd22-95fa-4037-ba6e-cb9a909337a7/image.png" /></p>
<p><code>KYM_QT</code>로 등록이 확인되었으므로, 클라이언트에서 <code>[KYM_QT:PASSWD]</code> 형식으로 접속하면 됩니다.</p>
<hr />
<h2 id="2-socketclient-클래스-파일-추가">2. SocketClient 클래스 파일 추가</h2>
<p>Qt의 소켓 통신 예제를 참고합니다.
Qt Creator 상단 메뉴에서 Examples를 열고 <code>socket</code>으로 검색하면 관련 샘플을 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f31f27c0-0f24-491a-b535-5be1b2e2d321/image.png" /></p>
<p>샘플 코드를 재구성한 예제</p>
<p><code>SocketClient</code> 클래스는 <code>QTcpSocket</code>을 래핑하여 소켓 통신만 전담합니다.
<code>Tab2SocketClient</code>는 UI만 담당하고, 실제 소켓 동작은 <code>SocketClient</code>에 위임하는 구조입니다.</p>
<p>프로젝트에 일반 C++ 클래스로 파일을 추가합니다.</p>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → C++ → C++ Class</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5b889ae6-a903-4e8e-af16-615d824600f0/image.png" /></p>
<ul>
<li><code>socketclient.h</code></li>
<li><code>socketclient.cpp</code></li>
</ul>
<hr />
<h2 id="3-socketclient-클래스-구현">3. SocketClient 클래스 구현</h2>
<h3 id="접속-정보-정의">접속 정보 정의</h3>
<p><code>socketclient.h</code>에 서버 IP, 포트, 로그인 정보를 멤버 변수로 정의합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f93c4fee-0585-425a-94d8-fff9121112d6/image.png" /></p>
<pre><code class="language-cpp">QString SERVERIP = &quot;10.10.16.35&quot;;
int SERVERPORT = 5000;
QString LOGID = &quot;KYM_QT&quot;;
QString LOGPW = &quot;PASSWD&quot;;</code></pre>
<h3 id="signalslot-구성">Signal/Slot 구성</h3>
<p><code>QTcpSocket</code>의 시그널을 <code>SocketClient</code>의 슬롯으로 연결합니다.</p>
<pre><code class="language-cpp">connect(pQTcpSocket, SIGNAL(connected()), this, SLOT(socketConnectServerSlot()));
connect(pQTcpSocket, SIGNAL(disconnected()), this, SLOT(socketClosedServerSlot()));
connect(pQTcpSocket, SIGNAL(readyRead()), this, SLOT(socketReadDataSlot()));</code></pre>
<blockquote>
<p>Qt 버전에 따라 에러 시그널 이름이 다릅니다. <code>#if QT_VERSION</code> 전처리기로 분기 처리합니다.</p>
<ul>
<li>Qt6 : <code>errorOccurred(QAbstractSocket::SocketError)</code></li>
<li>Qt5 : <code>error(QAbstractSocket::SocketError)</code></li>
</ul>
</blockquote>
<h3 id="주요-슬롯-구현">주요 슬롯 구현</h3>
<p>연결이 완료되면 <code>[KYM_QT:PASSWD]</code> 형식으로 서버에 로그인 메시지를 전송합니다.</p>
<p>![]<img alt="" src="https://velog.velcdn.com/images/mommers/post/91ba2040-143b-4b06-80c5-70e5db10e399/image.png" /></p>
<p>데이터 수신 시 <code>socketRecvDataSig</code> 시그널로 상위 클래스에 전달합니다.
데이터 송신 시 문자열 끝에 <code>\n</code>을 추가하여 전송합니다.</p>
<hr />
<h2 id="4-tab2socketclient-클래스-생성">4. Tab2SocketClient 클래스 생성</h2>
<p>Tab2에 배치할 위젯 클래스를 생성합니다.</p>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p>Class name을 <code>Tab2SocketClient</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab2socketclient.h</code></li>
<li><code>tab2socketclient.cpp</code></li>
<li><code>tab2socketclient.ui</code></li>
</ul>
<hr />
<h2 id="5-tab2socketclient-ui-구성-designer">5. Tab2SocketClient UI 구성 (Designer)</h2>
<p><code>tab2socketclient.ui</code>를 Qt Designer에서 열고 위젯을 배치합니다.</p>
<pre><code>=============================================
| 수신 데이터 | pPBrecvClear | pPBserverConnect |
|                                           |
|              pTErecvData                  |
|                                           |
| pLErecvid  |   pLEsendData   |  pPBsend   |
=============================================</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/011dc839-f9a1-40d1-b92a-3cdd948523b4/image.png" /></p>
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
<td>&quot;수신 데이터&quot; 텍스트</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBrecvClear</td>
<td>수신창 초기화</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBserverConnect</td>
<td>서버 연결/해제 (Checkable)</td>
</tr>
<tr>
<td>QTextEdit</td>
<td>pTErecvData</td>
<td>수신 메시지 표시</td>
</tr>
<tr>
<td>QLineEdit</td>
<td>pLErecvid</td>
<td>수신 대상 ID 입력</td>
</tr>
<tr>
<td>QLineEdit</td>
<td>pLEsendData</td>
<td>송신 메시지 입력</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBsend</td>
<td>메시지 송신</td>
</tr>
</tbody></table>
<blockquote>
<p><code>pPBserverConnect</code>는 Property Editor에서 <code>checkable</code>을 체크해야 토글 버튼으로 동작합니다.</p>
</blockquote>
<hr />
<h2 id="6-signalslot-연결-qt-designer---수신-삭제">6. Signal/Slot 연결 (Qt Designer) - 수신 삭제</h2>
<p>Qt Designer의 <strong>Signals and Slots Editor</strong>에서 수신 삭제 버튼을 연결합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d56e2e38-9cc5-45fc-b157-3cc36895af78/image.png" /></p>
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
<td>pPBrecvClear</td>
<td>clicked()</td>
<td>pTErecvData</td>
<td>clear()</td>
</tr>
</tbody></table>
<hr />
<h2 id="7-tab2socketclient-코드">7. Tab2SocketClient 코드</h2>
<h3 id="tab2socketclienth">tab2socketclient.h</h3>
<p><code>SocketClient</code> 포인터를 멤버 변수로 선언하고, 서버 연결 버튼 슬롯과 수신 슬롯을 정의합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/68ebb73a-0e48-4988-9603-4bed0cd8339a/image.png" /></p>
<h3 id="생성자---socketclient-생성-및-signalslot-연결">생성자 - SocketClient 생성 및 Signal/Slot 연결</h3>
<p><code>SocketClient</code> 객체를 생성하고, 수신 시그널을 슬롯에 연결합니다.</p>
<pre><code class="language-cpp">pSocketClient = new SocketClient(this);
connect(pSocketClient, SIGNAL(socketRecvDataSig(QString)), this, SLOT(updateRecvDataSlot(QString)));</code></pre>
<h3 id="서버-연결해제">서버 연결/해제</h3>
<p><code>pPBserverConnect</code>는 checkable 버튼으로, 연결/해제 상태를 토글합니다.
연결 성공 시 버튼 텍스트를 &quot;서버 종료&quot;로 변경합니다.</p>
<h3 id="수신-데이터-표시">수신 데이터 표시</h3>
<p>수신된 문자열 끝의 <code>\n</code>을 제거하고 현재 시각과 함께 <code>pTErecvData</code>에 추가합니다.</p>
<pre><code class="language-cpp">strRecvData.chop(1);    // '\n' 제거
QTime time = QTime::currentTime();
QString strTime = time.toString() + &quot; &quot; + strRecvData;
ui-&gt;pTErecvData-&gt;append(strTime);</code></pre>
<hr />
<h2 id="8-mainwidget에-tab2-추가">8. mainwidget에 Tab2 추가</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<p><code>tab2socketclient.h</code>를 include하고 <code>Tab2SocketClient</code> 포인터를 선언합니다.</p>
<pre><code class="language-cpp">Tab2SocketClient *pTab2SocketClient;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<p><code>Tab2SocketClient</code> 객체를 생성하여 <code>pTab2</code>에 배치합니다.</p>
<pre><code class="language-cpp">pTab2SocketClient = new Tab2SocketClient(ui-&gt;pTab2);
ui-&gt;pTab2-&gt;setLayout(pTab2SocketClient-&gt;layout());</code></pre>
<p>빌드 후 실행하면 Tab2 UI가 정상적으로 나타납니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/edec3524-80dc-4b36-896e-ea60e0968a28/image.png" /></p>
<hr />
<h2 id="9-서버-연결-테스트">9. 서버 연결 테스트</h2>
<p>서버 연결 버튼을 클릭하면 <code>QInputDialog</code>에서 IP를 입력받습니다.
입력 없이 확인하면 기본 IP(<code>10.10.16.35</code>)로 접속합니다.</p>
<p>연결 성공 시 수신창에 서버 메시지가 표시됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fcf3f2e1-5c19-418c-a68d-f25516562f18/image.png" /></p>
<pre><code>[KYM_QT] New connected!
(ip:10.10.16.35,fd:7,sockcnt:2)</code></pre><hr />
<h2 id="10-송신-기능-추가-및-테스트">10. 송신 기능 추가 및 테스트</h2>
<h3 id="signalslot-연결-qt-designer---엔터→송신">Signal/Slot 연결 (Qt Designer) - 엔터→송신</h3>
<p><code>pLEsendData</code>에서 엔터 입력 시 송신 버튼 클릭과 동일하게 동작하도록 연결합니다.</p>
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
<td>pLEsendData</td>
<td>returnPressed()</td>
<td>pPBsend</td>
<td>click()</td>
</tr>
</tbody></table>
<h3 id="송신-메시지-포맷">송신 메시지 포맷</h3>
<p>수신 ID 입력 여부에 따라 메시지 형식이 달라집니다.</p>
<ul>
<li>ID 입력 없음 → <code>[ALLMSG]메시지</code></li>
<li>ID 입력 있음 → <code>[입력 아이디]메시지</code></li>
</ul>
<h3 id="동작-확인">동작 확인</h3>
<p>메시지를 입력하고 송신하면 수신창에 에코 메시지가 표시됩니다.</p>
<p><img alt="image.png" src="attachment:a188ae15-ec61-4b1c-8ab7-44ad495e3dda:image.png" /></p>
<p>서버 측에서도 메시지 수신을 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/17cf5609-e8d1-495e-8f68-a9689cbdec2a/image.png" /></p>
<p><code>KYM_LIN</code> 클라이언트가 접속한 경우, 해당 클라이언트가 보낸 메시지도 수신창에 표시됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1666bfec-b14c-4f76-8e0f-37f3418d397d/image.png" /></p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>서버에 KYM_QT ID 등록 확인
    ↓
SocketClient 클래스 파일 추가 (QTcpSocket 래핑)
    ↓
Tab2SocketClient 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
tab2socketclient.ui에서 위젯 배치
    ↓
Qt Designer에서 Signal/Slot 연결 (수신 삭제, 엔터→송신)
    ↓
생성자에서 SocketClient 생성 및 Signal/Slot 연결
    ↓
서버 연결/해제, 수신 표시, 메시지 송신 Slot 구현
    ↓
mainwidget에서 Tab2SocketClient 객체 생성 및 pTab2에 배치
    ↓
서버 연결 및 송수신 동작 확인</code></pre>