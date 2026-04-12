<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner9">이전 글 : Qt) Designer로 UI 구성하기(7) - Tab4SensorChart</a></p>
</blockquote>
<p>이전 글에서 소켓으로 수신한 센서 데이터를 실시간 그래프로 표시하는 Tab4를 구현했습니다.</p>
<p>이번 글에서는 SQLite 데이터베이스를 활용해 센서 데이터를 저장하고, 저장된 데이터를 조회하여 테이블과 그래프로 표시하는 <code>Tab5SensorDatabase</code>를 구현하는 과정을 정리합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5893e448-e285-4634-9fb2-7ead7c00b712/image.png" /></p>
<hr />
<h2 id="1-pro-파일에-sql-모듈-추가">1. .pro 파일에 sql 모듈 추가</h2>
<p><code>QSqlDatabase</code>, <code>QSqlQuery</code> 등 데이터베이스 관련 클래스를 사용하기 위해 <code>.pro</code> 파일에 <code>sql</code> 모듈을 추가합니다.</p>
<pre><code>QT += widgets network charts sql</code></pre><hr />
<h2 id="2-tab5sensordatabase-클래스-생성">2. Tab5SensorDatabase 클래스 생성</h2>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p>Class name을 <code>Tab5SensorDatabase</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab5sensordatabase.h</code></li>
<li><code>tab5sensordatabase.cpp</code></li>
<li><code>tab5sensordatabase.ui</code></li>
</ul>
<hr />
<h2 id="3-tab5sensordatabase-ui-구성">3. Tab5SensorDatabase UI 구성</h2>
<p><code>tab5sensordatabase.ui</code>를 Qt Designer에서 열고 아래와 같이 위젯을 배치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/681352bc-68fe-4e29-8dde-85c7da1297b0/image.png" /></p>
<pre><code>=================================================================
| pDateTimeEditFrom  |  pDateTimeEditTo  | [조회] | [삭제]      |
|-----------------------------------------------------------------|
|                            |                                   |
|     pTBsensor              |     pChartViewLayout              |
|  (ID/날짜/조도/온도/습도)    |      (차트 표시 영역)             |
|                            |                                   |
=================================================================</code></pre><h3 id="주요-위젯-objectname">주요 위젯 objectName</h3>
<table>
<thead>
<tr>
<th>위젯</th>
<th>objectName</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>QDateTimeEdit</td>
<td>pDateTimeEditFrom</td>
<td>조회 시작 시각</td>
</tr>
<tr>
<td>QDateTimeEdit</td>
<td>pDateTimeEditTo</td>
<td>조회 종료 시각</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBDbSearch</td>
<td>DB 조회</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBDbDelete</td>
<td>테이블/차트 초기화</td>
</tr>
<tr>
<td>QTableWidget</td>
<td>pTBsensor</td>
<td>조회 결과 테이블 표시</td>
</tr>
<tr>
<td>QWidget</td>
<td>pChartViewLayout</td>
<td>차트 뷰를 추가할 레이아웃 영역</td>
</tr>
</tbody></table>
<hr />
<h2 id="4-tab5sensordatabaseh">4. tab5sensordatabase.h</h2>
<p>Tab4와 차트 관련 멤버 변수는 동일하며, 데이터베이스 관련 멤버로 <code>QSqlDatabase</code>가 추가됩니다.</p>
<pre><code class="language-cpp">#ifndef TAB5SENSORDATABASE_H
#define TAB5SENSORDATABASE_H

#include &lt;QWidget&gt;
#include &lt;QChartView&gt;
#include &lt;QSqlDatabase&gt;
#include &lt;QSqlQuery&gt;
#include &lt;qsqlerror.h&gt;
#include &lt;QLineSeries&gt;
#include &lt;QDateTimeAxis&gt;
#include &lt;QDate&gt;
#include &lt;QTime&gt;

namespace Ui {
class Tab5SensorDatabase;
}

class Tab5SensorDatabase : public QWidget
{
    Q_OBJECT

public:
    explicit Tab5SensorDatabase(QWidget *parent = nullptr);
    ~Tab5SensorDatabase();
    void updateLastDateTimeSql(bool);

private slots:
    void tab5RecvDataSlot(QStringList&amp;);
    void on_pPBDbDelete_clicked();
    void on_pPBDbSearch_clicked();

private:
    Ui::Tab5SensorDatabase *ui;
    QSqlDatabase qSqlDatabase;
    QLineSeries *illuLine;
    QLineSeries *humiLine;
    QLineSeries *tempLine;
    QChart *pQChart;
    QChartView *pQChartView;
    QDateTimeAxis *pQDateTimeAxis;
    QDateTime firstDateTime;
    QDateTime lastDateTime;
};

#endif // TAB5SENSORDATABASE_H</code></pre>
<hr />
<h2 id="5-tab5sensordatabasecpp">5. tab5sensordatabase.cpp</h2>
<h3 id="5-1-생성자---db-연결-및-테이블-생성">5-1. 생성자 - DB 연결 및 테이블 생성</h3>
<p>생성자에서 SQLite DB를 열고 <code>sensor_tb</code> 테이블을 생성합니다.
테이블이 이미 존재하면 <code>create table</code> 쿼리는 실패하지만 이후 동작에는 영향이 없습니다.</p>
<pre><code class="language-cpp">Tab5SensorDatabase::Tab5SensorDatabase(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Tab5SensorDatabase)
{
    ui-&gt;setupUi(this);

    // SQLite DB 연결
    qSqlDatabase = QSqlDatabase::addDatabase(&quot;QSQLITE&quot;);
    qSqlDatabase.setDatabaseName(&quot;aiot.db&quot;);
    if(qSqlDatabase.open())
        qDebug() &lt;&lt; &quot;success open sqlDatabse&quot;;
    else
        qDebug() &lt;&lt; &quot;failed to open sqlDatabse&quot;;

    // 테이블 생성
    QString strQuery = &quot;create table sensor_tb (&quot;
                       &quot;name varchar(10),&quot;
                       &quot;date DATETIME primary key,&quot;
                       &quot;illu varchar(10),&quot;
                       &quot;temp varchar(10),&quot;
                       &quot;humi varchar(10))&quot;;
    QSqlQuery QSqlQuery;
    if(QSqlQuery.exec(strQuery))
        qDebug() &lt;&lt; &quot;Create Table&quot;;

    // 차트 초기화 (Tab4와 동일)
    illuLine = new QLineSeries(this);
    illuLine-&gt;setName(&quot;조도&quot;);
    // ... (Tab4와 동일한 QPen 설정 생략)

    pQChart = new QChart();
    pQChart-&gt;addSeries(illuLine);
    pQChart-&gt;addSeries(humiLine);
    pQChart-&gt;addSeries(tempLine);
    pQChart-&gt;createDefaultAxes();
    pQChart-&gt;axes(Qt::Vertical).constFirst()-&gt;setRange(0, 100);

    pQChartView = new QChartView(pQChart);
    pQDateTimeAxis = new QDateTimeAxis;
    pQDateTimeAxis-&gt;setFormat(&quot;hh:mm&quot;);

    updateLastDateTimeSql(false);

    ui-&gt;pChartViewLayout-&gt;layout()-&gt;addWidget(pQChartView);
    pQChartView-&gt;chart()-&gt;setAxisX(pQDateTimeAxis, illuLine);
    pQChartView-&gt;chart()-&gt;setAxisX(pQDateTimeAxis, humiLine);
    pQChartView-&gt;chart()-&gt;setAxisX(pQDateTimeAxis, tempLine);
}</code></pre>
<blockquote>
<p><code>aiot.db</code> 파일은 앱 실행 시 자동으로 생성됩니다.</p>
</blockquote>
<hr />
<h3 id="5-2-updatelastdatetimesql---x축-시간-범위-업데이트">5-2. updateLastDateTimeSql - X축 시간 범위 업데이트</h3>
<p>Tab4의 <code>updateLastDateTime</code>과 달리, Tab5에서는 UI의 <code>pDateTimeEditFrom</code>, <code>pDateTimeEditTo</code> 값을 기준으로 X축 범위를 설정합니다.</p>
<pre><code class="language-cpp">void Tab5SensorDatabase::updateLastDateTimeSql(bool bFlag)
{
    QDateTime firstDateTime;
    QDateTime lastDateTime;
    QDateTime fromDateTime = ui-&gt;pDateTimeEditFrom-&gt;dateTime();
    QDateTime toDateTime = ui-&gt;pDateTimeEditTo-&gt;dateTime();

    if(!bFlag)
    {
        firstDateTime = fromDateTime;
        lastDateTime = toDateTime;
    }
    else
    {
        firstDateTime = ui-&gt;pDateTimeEditFrom-&gt;dateTime();
        lastDateTime = QDateTime::currentDateTime().addSecs(60);
    }
    pQDateTimeAxis-&gt;setRange(firstDateTime, lastDateTime);
}</code></pre>
<hr />
<h3 id="5-3-tab5recvdataslot---수신-데이터-db-저장-및-차트-추가">5-3. tab5RecvDataSlot - 수신 데이터 DB 저장 및 차트 추가</h3>
<p>소켓으로 데이터를 수신하면 DB에 INSERT하고 차트에도 실시간으로 추가합니다.
INSERT 성공 시 <code>pDateTimeEditTo</code>를 현재 시각으로 업데이트합니다.</p>
<pre><code class="language-cpp">void Tab5SensorDatabase::tab5RecvDataSlot(QStringList&amp; strList)
{
    QDateTime dateTime = QDateTime::currentDateTime();
    QString name = strList[1];
    QString strIllu = strList[3];
    QString strTemp = strList[4];
    QString strHumi = strList[5];

    if(lastDateTime.toSecsSinceEpoch() &lt; dateTime.toSecsSinceEpoch())
        updateLastDateTimeSql(true);

    // DB INSERT
    QString strQuery = &quot;insert into sensor_tb(name, date, illu, temp, humi) values('&quot;
                     + name + &quot;' , '&quot;
                     + dateTime.toString(&quot;yyyy/MM/dd hh:mm:ss&quot;) + &quot;' , '&quot;
                     + strIllu + &quot;' , '&quot;
                     + strTemp + &quot;' , '&quot;
                     + strHumi + &quot;' ) &quot;;
    QSqlQuery qSqlQuery;
    if(qSqlQuery.exec(strQuery))
    {
        qDebug() &lt;&lt; &quot;Insert Query OK&quot;;
        ui-&gt;pDateTimeEditTo-&gt;setDateTime(dateTime);
        pQDateTimeAxis-&gt;setMax(dateTime);
    }

    // 차트에 실시간 추가
    illuLine-&gt;append(dateTime.toMSecsSinceEpoch(), strIllu.toInt());
    humiLine-&gt;append(dateTime.toMSecsSinceEpoch(), strTemp.toDouble());
    tempLine-&gt;append(dateTime.toMSecsSinceEpoch(), strHumi.toDouble());
}</code></pre>
<hr />
<h3 id="5-4-조회-버튼---db-select-및-테이블차트-갱신">5-4. 조회 버튼 - DB SELECT 및 테이블/차트 갱신</h3>
<p>조회 버튼을 누르면 DB에서 <code>pDateTimeEditFrom</code> ~ <code>pDateTimeEditTo</code> 범위의 데이터를 SELECT하여 <code>pTBsensor</code>에 표시하고 차트도 갱신합니다.</p>
<pre><code class="language-cpp">void Tab5SensorDatabase::on_pPBDbSearch_clicked()
{
    // DB에서 가장 오래된 데이터 시각을 찾아 From에 설정
    QSqlQuery minQuery;
    if(minQuery.exec(&quot;select min(date) from sensor_tb&quot;) &amp;&amp; minQuery.next())
    {
        QString strMinDate = minQuery.value(0).toString();
        QDateTime minDateTime = QDateTime::fromString(strMinDate, &quot;yyyy/MM/dd hh:mm:ss&quot;);
        if(minDateTime.isValid())
        {
            ui-&gt;pDateTimeEditFrom-&gt;setDateTime(minDateTime);
            ui-&gt;pDateTimeEditTo-&gt;setDateTime(QDateTime::currentDateTime());
        }
    }

    illuLine-&gt;clear();
    humiLine-&gt;clear();
    tempLine-&gt;clear();
    updateLastDateTimeSql(false);

    // 범위 조건으로 SELECT
    QString strFromDateTime = ui-&gt;pDateTimeEditFrom-&gt;dateTime().toString(&quot;yyyy/MM/dd hh:mm:ss&quot;);
    QString strToDateTime = ui-&gt;pDateTimeEditTo-&gt;dateTime().toString(&quot;yyyy/MM/dd hh:mm:ss&quot;);
    QString strQuery = &quot;select * from sensor_tb where '&quot;
                     + strFromDateTime + &quot;' &lt;= date AND date &lt; '&quot;
                     + strToDateTime + &quot;' &quot;;

    int rowCount = 0;
    QSqlQuery qSqlQuery;
    if(qSqlQuery.exec(strQuery))
    {
        qDebug() &lt;&lt; &quot;Select Query Ok&quot;;
        while(qSqlQuery.next())
        {
            rowCount++;
            ui-&gt;pTBsensor-&gt;setRowCount(rowCount);

            QTableWidgetItem *pId   = new QTableWidgetItem();
            QTableWidgetItem *pDate = new QTableWidgetItem();
            QTableWidgetItem *pIllu = new QTableWidgetItem();
            QTableWidgetItem *pTemp = new QTableWidgetItem();
            QTableWidgetItem *pHumi = new QTableWidgetItem();

            pId-&gt;setText(qSqlQuery.value(&quot;name&quot;).toString());
            pDate-&gt;setText(qSqlQuery.value(&quot;date&quot;).toString());
            pIllu-&gt;setText(qSqlQuery.value(&quot;illu&quot;).toString());
            pTemp-&gt;setText(qSqlQuery.value(&quot;temp&quot;).toString());
            pHumi-&gt;setText(qSqlQuery.value(&quot;humi&quot;).toString());

            ui-&gt;pTBsensor-&gt;setItem(rowCount-1, 0, pId);
            ui-&gt;pTBsensor-&gt;setItem(rowCount-1, 1, pDate);
            ui-&gt;pTBsensor-&gt;setItem(rowCount-1, 2, pIllu);
            ui-&gt;pTBsensor-&gt;setItem(rowCount-1, 3, pTemp);
            ui-&gt;pTBsensor-&gt;setItem(rowCount-1, 4, pHumi);

            QDateTime xValue = QDateTime::fromString(pDate-&gt;text(), &quot;yyyy/MM/dd hh:mm:ss&quot;);
            illuLine-&gt;append(xValue.toMSecsSinceEpoch(), pIllu-&gt;text().toInt());
            humiLine-&gt;append(xValue.toMSecsSinceEpoch(), pHumi-&gt;text().toDouble());
            tempLine-&gt;append(xValue.toMSecsSinceEpoch(), pTemp-&gt;text().toDouble());
        }

        ui-&gt;pTBsensor-&gt;resizeColumnToContents(0);
        ui-&gt;pTBsensor-&gt;resizeColumnToContents(1);
        ui-&gt;pTBsensor-&gt;resizeColumnToContents(2);
        ui-&gt;pTBsensor-&gt;resizeColumnToContents(3);
        ui-&gt;pTBsensor-&gt;resizeColumnToContents(4);
    }
}</code></pre>
<hr />
<h3 id="5-5-삭제-버튼---테이블차트-초기화">5-5. 삭제 버튼 - 테이블/차트 초기화</h3>
<pre><code class="language-cpp">void Tab5SensorDatabase::on_pPBDbDelete_clicked()
{
    ui-&gt;pTBsensor-&gt;clearContents();
    illuLine-&gt;clear();
    humiLine-&gt;clear();
    tempLine-&gt;clear();
}</code></pre>
<blockquote>
<p>삭제 버튼은 화면에 표시된 테이블과 차트만 초기화합니다. DB에 저장된 데이터는 유지됩니다.</p>
</blockquote>
<hr />
<h2 id="6-mainwidget에-tab5-추가-및-소켓-연동">6. mainwidget에 Tab5 추가 및 소켓 연동</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<pre><code class="language-cpp">#include &lt;tab5sensordatabase.h&gt;

Tab5SensorDatabase *pTab5SensorDatabase;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<pre><code class="language-cpp">pTab5SensorDatabase = new Tab5SensorDatabase(ui-&gt;pTab5);
ui-&gt;pTab5-&gt;setLayout(pTab5SensorDatabase-&gt;layout());

connect(pTab2SocketClient, SIGNAL(tab5RecvDataSig(QStringList&amp;)),
        pTab5SensorDatabase, SLOT(tab5RecvDataSlot(QStringList&amp;)));</code></pre>
<hr />
<h2 id="7-tab4-vs-tab5-비교">7. Tab4 vs Tab5 비교</h2>
<table>
<thead>
<tr>
<th></th>
<th>Tab4</th>
<th>Tab5</th>
</tr>
</thead>
<tbody><tr>
<td>데이터 저장</td>
<td>없음 (메모리)</td>
<td>SQLite DB 저장</td>
</tr>
<tr>
<td>X축 기준</td>
<td>현재 시각 자동</td>
<td>DateTimeEdit 기준</td>
</tr>
<tr>
<td>조회 기능</td>
<td>없음</td>
<td>DB SELECT + 테이블 표시</td>
</tr>
<tr>
<td>초기화</td>
<td>차트만</td>
<td>테이블 + 차트</td>
</tr>
</tbody></table>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>.pro에 sql 모듈 추가 (QT += sql)
    ↓
Tab5SensorDatabase 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
UI 구성 (DateTimeEdit x2 + 조회/삭제 버튼 + QTableWidget + 차트 영역)
    ↓
생성자 : SQLite DB 연결 → sensor_tb 테이블 생성 → 차트 초기화
    ↓
tab5RecvDataSlot : 수신 데이터 DB INSERT → 차트 실시간 추가
    ↓
조회 버튼 : DB SELECT → QTableWidget 표시 → 차트 갱신
    ↓
삭제 버튼 : 화면 테이블/차트 초기화 (DB 데이터 유지)
    ↓
mainwidget에 Tab5 추가 및 Tab2 수신 시그널 연결</code></pre>