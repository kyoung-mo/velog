<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner10">이전 글 : Qt) Designer로 UI 구성하기(8) - Tab5SensorDatabase</a></p>
</blockquote>
<p>이전 글까지 AiotClient의 Tab1~Tab7을 구현하는 과정을 정리했습니다.</p>
<p>이번 글에서는 수업에서 배운 내용을 바탕으로 진행한 간단한 시험 내용에 대해 정리해보려합니다.
기존 AiotClient의 소켓 클라이언트(Tab2)와 센서 차트(Tab4), SQLite DB(Tab5) 기능을 새 프로젝트에 Tab1, Tab2, Tab3으로 재구성하는 내용입니다.
시험때 캡쳐해둔 내용도 없고, 교수님 서버가 지금은 꺼져있어서, 내용으로만 정리해보겠습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2a370882-1e8a-4b06-95c0-c9480a119c16/image.png" /></p>
<hr />
<h2 id="트러블슈팅---charts-모듈-추가-오류">트러블슈팅 - charts 모듈 추가 오류</h2>
<p>과제를 진행하면서 Ubuntu(VirtualBox) 환경에서 문제가 발생했습니다.</p>
<p>새 프로젝트를 생성하고 Tab1, Tab2, Tab3 클래스를 추가한 뒤 <code>.pro</code> 파일에 모듈을 추가하는 과정에서 문제가 생겼습니다.</p>
<pre><code>QT += widgets network charts sql</code></pre><p>기존에 작업하던 위젯 파일들은 정상적으로 동작했지만, 새로 추가한 파일들에서 <code>charts</code> 모듈을 추가하면 계속 빌드 오류가 발생했습니다.</p>
<p>교수님께 말씀드렸고, 교수님 컴퓨터에서 새 파일에 <code>charts</code>만 추가해서 정상 동작하는 것을 확인한 후 파일을 보내주셨습니다. 하지만 해당 파일을 제 Ubuntu 환경에서 실행하면 동일한 오류가 발생했습니다.</p>
<p>원인을 파악하지 못한 채로, 교수님 지시에 따라 <strong>Windows 환경의 Qt Creator</strong>로 과제를 진행했습니다.</p>
<hr />
<h2 id="1-프로젝트-구조">1. 프로젝트 구조</h2>
<p>AiotClient와 비교하면 아래와 같이 탭 구성이 변경됐습니다.</p>
<table>
<thead>
<tr>
<th>AiotClient</th>
<th>SensorManKYM</th>
<th>기능</th>
</tr>
</thead>
<tbody><tr>
<td>Tab2SocketClient</td>
<td>Tab1Socket</td>
<td>소켓 연결/수신/송신</td>
</tr>
<tr>
<td>Tab4SensorChart</td>
<td>Tab2Sensor</td>
<td>실시간 센서 차트</td>
</tr>
<tr>
<td>Tab5SensorDatabase</td>
<td>Tab3Sqlite</td>
<td>SQLite DB 저장/조회</td>
</tr>
</tbody></table>
<p>AiotClient에서는 Tab2가 메시지를 파싱한 뒤 mainwidget을 통해 각 탭으로 라우팅하는 구조였습니다.
이번 과제에서는 <strong>Tab1이 직접 파싱하여 Tab2, Tab3으로 동시에 emit</strong>하는 구조로 단순화했습니다.</p>
<pre><code>수신 메시지 : [HM_CON]SENSOR@71@26.6@51.2
                  ↓
            Tab1에서 파싱
                  ↓
    tab2RecvDataSig + tab3RecvDataSig 동시 emit
           ↓               ↓
       Tab2Sensor      Tab3Sqlite</code></pre><hr />
<h2 id="2-pro-파일-모듈-설정">2. .pro 파일 모듈 설정</h2>
<pre><code>QT += widgets network charts sql</code></pre><hr />
<h2 id="3-tab1socket">3. Tab1Socket</h2>
<h3 id="ui-구성">UI 구성</h3>
<pre><code>==============================================
|  [서버연결(Checkable)]                     |
|----------------------------------------------|
|         수신 데이터 표시 (읽기전용)          |
|----------------------------------------------|
|  수신ID입력창  |  송신데이터입력창  | [Send] |
|----------------------------------------------|
|                              [수신Clear]     |
==============================================</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4ed65b3b-981f-4b90-9b87-714f1cff09db/image.png" /></p>
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
<td>pPBserverConnect</td>
<td>서버 연결/해제 (Checkable)</td>
</tr>
<tr>
<td>QTextEdit</td>
<td>pTErecvData</td>
<td>수신 데이터 표시 (읽기전용)</td>
</tr>
<tr>
<td>QLineEdit</td>
<td>pLErecvId</td>
<td>수신 ID 입력</td>
</tr>
<tr>
<td>QLineEdit</td>
<td>pLEsendData</td>
<td>송신 데이터 입력</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBsend</td>
<td>송신 (초기 비활성화)</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBrecvClear</td>
<td>수신 창 초기화</td>
</tr>
</tbody></table>
<p>AiotClient의 Tab2SocketClient와 비교해 <strong>수신 창 Clear 버튼</strong>(<code>pPBrecvClear</code>)이 추가됐습니다.</p>
<h3 id="tab1socketh">tab1socket.h</h3>
<pre><code class="language-cpp">#ifndef TAB1SOCKET_H
#define TAB1SOCKET_H

#include &lt;QWidget&gt;
#include &lt;QTime&gt;
#include &quot;socketclient.h&quot;

namespace Ui {
class Tab1Socket;
}

class Tab1Socket : public QWidget
{
    Q_OBJECT

public:
    explicit Tab1Socket(QWidget *parent = nullptr);
    ~Tab1Socket();

private slots:
    void updateRecvDataSlot(QString);
    void on_pPBserverConnect_clicked(bool checked);
    void on_pPBsend_clicked();
    void on_pPBrecvClear_clicked();

public slots:
    void socketWriteDataSlot(QString);

private:
    Ui::Tab1Socket *ui;
    SocketClient *pSocketClient;

signals:
    void tab2RecvDataSig(QStringList&amp;);
    void tab3RecvDataSig(QStringList&amp;);
};

#endif // TAB1SOCKET_H</code></pre>
<h3 id="tab1socketcpp">tab1socket.cpp</h3>
<p>생성자에서 <code>SocketClient</code>를 생성하고 수신 시그널을 연결합니다.</p>
<pre><code class="language-cpp">Tab1Socket::Tab1Socket(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Tab1Socket)
{
    ui-&gt;setupUi(this);
    pSocketClient = new SocketClient(this);
    ui-&gt;pPBsend-&gt;setEnabled(false);
    connect(pSocketClient, SIGNAL(socketRecvDataSig(QString)), this, SLOT(updateRecvDataSlot(QString)));
}</code></pre>
<p>수신 데이터를 파싱하여 메시지 종류가 <code>SENSOR</code>이면 Tab2와 Tab3으로 동시에 emit합니다.</p>
<pre><code class="language-cpp">void Tab1Socket::updateRecvDataSlot(QString strRecvData)
{
    strRecvData.chop(1);
    QTime time = QTime::currentTime();
    QString strTime = time.toString() + &quot; &quot; + strRecvData;
    ui-&gt;pTErecvData-&gt;append(strTime);

    strRecvData.replace(&quot;[&quot;, &quot;@&quot;);
    strRecvData.replace(&quot;]&quot;, &quot;@&quot;);
    QStringList strList = strRecvData.split(&quot;@&quot;);

    if(strList[2] == &quot;SENSOR&quot;)
    {
        emit tab2RecvDataSig(strList);
        emit tab3RecvDataSig(strList);
    }
}</code></pre>
<p>서버 연결/해제, 송신, 수신 Clear 버튼 슬롯입니다.</p>
<pre><code class="language-cpp">void Tab1Socket::on_pPBserverConnect_clicked(bool checked)
{
    bool bFlag;
    if(checked)
    {
        pSocketClient-&gt;connectToServerSlot(bFlag);
        if(bFlag)
        {
            ui-&gt;pPBserverConnect-&gt;setText(&quot;서버해제&quot;);
            ui-&gt;pPBsend-&gt;setEnabled(true);
        }
        else
            ui-&gt;pPBserverConnect-&gt;setChecked(false);
    }
    else
    {
        pSocketClient-&gt;socketClosedServerSlot();
        ui-&gt;pPBserverConnect-&gt;setText(&quot;서버연결&quot;);
        ui-&gt;pPBsend-&gt;setEnabled(false);
    }
}

void Tab1Socket::on_pPBsend_clicked()
{
    QString strRecvId = ui-&gt;pLErecvId-&gt;text();
    QString strSendData = ui-&gt;pLEsendData-&gt;text();
    if(strSendData.isEmpty())
        return;
    if(strRecvId.isEmpty())
        strSendData = &quot;[ALLMSG]&quot; + strSendData;
    else
        strSendData = &quot;[&quot; + strRecvId + &quot;]&quot; + strSendData;
    pSocketClient-&gt;socketWriteDataSlot(strSendData);
    ui-&gt;pLEsendData-&gt;clear();
}

void Tab1Socket::on_pPBrecvClear_clicked()
{
    ui-&gt;pTErecvData-&gt;clear();
}</code></pre>
<hr />
<h2 id="4-tab2sensor">4. Tab2Sensor</h2>
<p>AiotClient의 Tab4SensorChart와 동일한 구조입니다.
자세한 구현 내용은 아래 글을 참고해 주세요.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/241f83f4-3baa-4a13-aea2-62b6806f3f38/image.png" /></p>
<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner9">Qt) Designer로 UI 구성하기(7) - Tab4SensorChart</a></p>
</blockquote>
<p>슬롯 이름만 <code>tab4RecvDataSlot</code> → <code>tab2RecvDataSlot</code>으로 변경됐습니다.</p>
<hr />
<h2 id="5-tab3sqlite">5. Tab3Sqlite</h2>
<p>AiotClient의 Tab5SensorDatabase와 대부분 동일하며, 삭제 버튼 동작에 차이가 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bb697f5a-adc0-446a-8bff-054c99416ac8/image.png" /></p>
<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner10">Qt) Designer로 UI 구성하기(8) - Tab5SensorDatabase</a></p>
</blockquote>
<p><strong>Tab5SensorDatabase와의 차이점:</strong></p>
<p>Tab5의 삭제 버튼은 화면(테이블, 차트)만 초기화했지만, Tab3Sqlite에서는 <strong>DB에서도 실제로 DELETE 쿼리를 실행</strong>합니다.</p>
<pre><code class="language-cpp">void Tab3Sqlite::on_pPBDbDelete_clicked()
{
    QString strFromDateTime = ui-&gt;pDateTimeEditFrom-&gt;dateTime().toString(&quot;yyyy/MM/dd hh:mm:ss&quot;);
    QString strToDateTime = ui-&gt;pDateTimeEditTo-&gt;dateTime().toString(&quot;yyyy/MM/dd hh:mm:ss&quot;);

    QString strQuery = &quot;delete from sensor_tb where '&quot;
                     + strFromDateTime + &quot;' &lt;= date AND date &lt; '&quot;
                     + strToDateTime + &quot;' &quot;;
    QSqlQuery qSqlQuery;
    if(qSqlQuery.exec(strQuery))
        qDebug() &lt;&lt; &quot;delete query ok&quot;;

    ui-&gt;pTBsensor-&gt;clearContents();
    illuLine-&gt;clear();
    humiLine-&gt;clear();
    tempLine-&gt;clear();
}</code></pre>
<hr />
<h2 id="6-mainwidget-연결">6. mainwidget 연결</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<pre><code class="language-cpp">#include &lt;tab1socket.h&gt;
#include &lt;tab2sensor.h&gt;
#include &lt;tab3sqlite.h&gt;

Tab1Socket *pTab1Socket;
Tab2Sensor *pTab2Sensor;
Tab3Sqlite *pTab3Sqlite;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<p>Tab1이 파싱과 라우팅을 담당하므로 mainwidget에서의 connect 구조가 단순해졌습니다.</p>
<pre><code class="language-cpp">pTab1Socket = new Tab1Socket(ui-&gt;pTab1);
ui-&gt;pTab1-&gt;setLayout(pTab1Socket-&gt;layout());

pTab2Sensor = new Tab2Sensor(ui-&gt;pTab2);
ui-&gt;pTab2-&gt;setLayout(pTab2Sensor-&gt;layout());

pTab3Sqlite = new Tab3Sqlite(ui-&gt;pTab3);
ui-&gt;pTab3-&gt;setLayout(pTab3Sqlite-&gt;layout());

ui-&gt;tabWidget-&gt;setCurrentIndex(0);

connect(pTab1Socket, SIGNAL(tab2RecvDataSig(QStringList&amp;)),
        pTab2Sensor, SLOT(tab2RecvDataSlot(QStringList&amp;)));
connect(pTab1Socket, SIGNAL(tab3RecvDataSig(QStringList&amp;)),
        pTab3Sqlite, SLOT(tab3RecvDataSlot(QStringList&amp;)));</code></pre>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>새 프로젝트 생성 (SensorManKYM, qmake)
    ↓
.pro에 모듈 추가 (widgets network charts sql)
    ↓
Ubuntu 환경 charts 오류 발생 → Windows Qt Creator로 환경 전환
    ↓
Tab1Socket 구현 (소켓 연결/수신/송신/파싱/라우팅)
    ↓
Tab2Sensor 구현 (실시간 센서 차트)
    ↓
Tab3Sqlite 구현 (SQLite DB 저장/조회/삭제)
    ↓
mainwidget에 Tab1~3 추가 및 Signal/Slot 연결
    ↓
Tab1 수신 → SENSOR 메시지 파싱 → Tab2, Tab3 동시 emit</code></pre><hr />
<p>이제 다음 시간부터는 터틀봇을 제공받고, ROS2 수업에 대해 정리할 예정입니다...</p>