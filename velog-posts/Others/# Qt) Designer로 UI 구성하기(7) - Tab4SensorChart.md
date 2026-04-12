<p>ROS 수업을 새로 들어가고부터 수업 진도 따라가고 백준 코테문제 집중해서 푸느라 블로그 정리가 밀렸네요.. 기억나는 순서대로 천천히 정리해보겠습니다.</p>
<hr />
<blockquote>
<p><a href="https://velog.io/@mommers/QtDesigner8">이전 글 : Qt) Designer로 UI 구성하기(6) - Tab6WebCamera</a></p>
</blockquote>
<p>이전 글에서 mjpg-streamer와 QWebEngineView를 활용해 Tab6 웹캠 탭을 구현했습니다.</p>
<p>이번 글에서는 소켓으로 수신한 센서 데이터를 실시간 그래프로 표시하는 <code>Tab4SensorChart</code>를 구현하는 과정을 정리해보겠습니다. 수업에서는 조도 데이터만으로 그래프를 그려보았고, 이후 시험에서 온도와 습도 데이터를 추가하는 방향으로 진행됐습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0665bea9-e279-4288-b23a-561db3829e51/image.png" /></p>
<hr />
<h2 id="1-pro-파일에-charts-모듈-추가">1. .pro 파일에 charts 모듈 추가</h2>
<p><code>QLineSeries</code>, <code>QChart</code>, <code>QChartView</code> 등 차트 관련 클래스를 사용하기 위해 <code>.pro</code> 파일에 <code>charts</code> 모듈을 추가합니다.</p>
<pre><code>QT += widgets network charts</code></pre><hr />
<h2 id="2-tab4sensorchart-클래스-생성">2. Tab4SensorChart 클래스 생성</h2>
<p><strong>AiotClient 프로젝트 우클릭 → Add New → Qt → Qt Widgets Designer Form Class → Widget 선택</strong></p>
<p>Class name을 <code>Tab4SensorChart</code>로 입력하면 아래 파일이 자동 생성됩니다.</p>
<ul>
<li><code>tab4sensorchart.h</code></li>
<li><code>tab4sensorchart.cpp</code></li>
<li><code>tab4sensorchart.ui</code></li>
</ul>
<hr />
<h2 id="3-tab4sensorchart-ui-구성">3. Tab4SensorChart UI 구성</h2>
<p><code>tab4sensorchart.ui</code>를 Qt Designer에서 열고 아래와 같이 위젯을 배치합니다.</p>
<pre><code>=====================================
|                         [Clear]   |
|                                   |
|       pChartViewLayout            |
|        (차트 표시 영역)             |
|                                   |
=====================================</code></pre><h3 id="주요-위젯-objectname">주요 위젯 objectName</h3>
<table>
<thead>
<tr>
<th>위젯</th>
<th>objectName</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>QWidget</td>
<td>pChartViewLayout</td>
<td>차트 뷰를 추가할 레이아웃 영역</td>
</tr>
<tr>
<td>QPushButton</td>
<td>pPBchartClear</td>
<td>차트 데이터 초기화</td>
</tr>
</tbody></table>
<blockquote>
<p><code>pChartViewLayout</code>은 <code>QWidget</code>을 배치하고 레이아웃을 설정한 후, 생성자에서 <code>QChartView</code>를 동적으로 추가하는 방식을 사용합니다.</p>
</blockquote>
<hr />
<h2 id="4-tab4sensorcharth">4. tab4sensorchart.h</h2>
<p>차트 관련 멤버 변수로 <code>QLineSeries</code>, <code>QChart</code>, <code>QChartView</code>, <code>QDateTimeAxis</code>를 선언합니다.
X축을 시간 기반으로 표시하기 위해 <code>QDateTimeAxis</code>를 사용합니다.</p>
<pre><code class="language-cpp">#ifndef TAB4SENSORCHART_H
#define TAB4SENSORCHART_H

#include &lt;QWidget&gt;
#include &lt;QChartView&gt;
#include &lt;QLineSeries&gt;
#include &lt;QDateTimeAxis&gt;
#include &lt;QDate&gt;
#include &lt;QTime&gt;

namespace Ui {
class Tab4SensorChart;
}

class Tab4SensorChart : public QWidget
{
    Q_OBJECT

public:
    explicit Tab4SensorChart(QWidget *parent = nullptr);
    ~Tab4SensorChart();
    void updateLastDateTime(bool bFlag);

private slots:
    void tab4RecvDataSlot(QStringList&amp;);
    void on_pPBchartClear_clicked();

private:
    Ui::Tab4SensorChart *ui;
    QLineSeries *illuLine;
    QLineSeries *humiLine;
    QLineSeries *tempLine;
    QChart *pQChart;
    QChartView *pQChartView;
    QDateTimeAxis *pQDateTimeAxis;
    QDateTime firstDateTime;
    QDateTime lastDateTime;
};

#endif // TAB4SENSORCHART_H</code></pre>
<hr />
<h2 id="5-tab4sensorchartcpp">5. tab4sensorchart.cpp</h2>
<h3 id="5-1-생성자---차트-초기화">5-1. 생성자 - 차트 초기화</h3>
<p>조도, 온도, 습도 각각 <code>QLineSeries</code>를 생성하고 색상을 지정합니다.
<code>QPen</code>으로 선 굵기와 색상을 설정합니다.</p>
<pre><code class="language-cpp">Tab4SensorChart::Tab4SensorChart(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Tab4SensorChart)
{
    ui-&gt;setupUi(this);

    // 조도 - 빨간색
    illuLine = new QLineSeries(this);
    illuLine-&gt;setName(&quot;조도&quot;);
    QPen pen_r;
    pen_r.setWidth(2);
    pen_r.setBrush(Qt::red);
    pen_r.setCapStyle(Qt::FlatCap);
    pen_r.setJoinStyle(Qt::MiterJoin);
    illuLine-&gt;setPen(pen_r);

    // 습도 - 초록색
    humiLine = new QLineSeries(this);
    humiLine-&gt;setName(&quot;습도&quot;);
    QPen pen_g;
    pen_g.setWidth(2);
    pen_g.setBrush(Qt::green);
    humiLine-&gt;setPen(pen_g);

    // 온도 - 파란색
    tempLine = new QLineSeries(this);
    tempLine-&gt;setName(&quot;온도&quot;);
    QPen pen_b;
    pen_b.setWidth(2);
    pen_b.setBrush(Qt::blue);
    tempLine-&gt;setPen(pen_b);

    // QChart 생성 및 시리즈 추가
    pQChart = new QChart();
    pQChart-&gt;addSeries(illuLine);
    pQChart-&gt;addSeries(humiLine);
    pQChart-&gt;addSeries(tempLine);

    // Y축 범위 0~100 설정
    pQChart-&gt;createDefaultAxes();
    pQChart-&gt;axes(Qt::Vertical).constFirst()-&gt;setRange(0, 100);

    // QChartView 생성
    pQChartView = new QChartView(pQChart);

    // X축 시간 축 설정
    pQDateTimeAxis = new QDateTimeAxis;
    pQDateTimeAxis-&gt;setFormat(&quot;hh:mm&quot;);

    updateLastDateTime(false);

    // pChartViewLayout에 QChartView 추가
    ui-&gt;pChartViewLayout-&gt;layout()-&gt;addWidget(pQChartView);
    pQChartView-&gt;chart()-&gt;setAxisX(pQDateTimeAxis, illuLine);
    pQChartView-&gt;chart()-&gt;setAxisX(pQDateTimeAxis, humiLine);
    pQChartView-&gt;chart()-&gt;setAxisX(pQDateTimeAxis, tempLine);
}</code></pre>
<blockquote>
<p><code>QChartView</code>를 Designer에서 직접 배치하지 않고 생성자에서 동적으로 생성하여 <code>pChartViewLayout</code>에 추가하는 방식을 사용했습니다.</p>
</blockquote>
<hr />
<h3 id="5-2-updatelastdatetime---x축-시간-범위-업데이트">5-2. updateLastDateTime - X축 시간 범위 업데이트</h3>
<p><code>bFlag</code>가 <code>false</code>이면 현재 시각을 시작 시각으로 설정하고, <code>true</code>이면 현재 시각으로 끝 시각만 연장합니다.</p>
<pre><code class="language-cpp">void Tab4SensorChart::updateLastDateTime(bool bFlag)
{
    QDate date = QDate::currentDate();
    QTime time = QTime::currentTime();
    if(!bFlag)
    {
        firstDateTime.setDate(date);
        firstDateTime.setTime(time);
    }
    lastDateTime.setDate(date);
    lastDateTime.setTime(time.addSecs(60 * 1));
    pQDateTimeAxis-&gt;setRange(firstDateTime, lastDateTime);
}</code></pre>
<blockquote>
<p>처음 실행 시(<code>false</code>) 현재 시각을 기준으로 X축을 1분 범위로 초기화합니다.
데이터가 들어오면서 시간이 범위를 초과하면(<code>true</code>) X축 끝 시각을 현재 시각으로 연장합니다.</p>
</blockquote>
<hr />
<h3 id="5-3-tab4recvdataslot---수신-데이터-차트에-추가">5-3. tab4RecvDataSlot - 수신 데이터 차트에 추가</h3>
<p>Tab2에서 파싱된 <code>QStringList</code>를 받아 각 센서 값을 차트에 추가합니다.
X축 값은 현재 시각을 밀리초 단위로 변환하여 사용합니다.</p>
<pre><code class="language-cpp">void Tab4SensorChart::tab4RecvDataSlot(QStringList&amp; strList)
{
    QDateTime dateTime = QDateTime::currentDateTime();

    QString strIllu = strList[3];
    QString strTemp = strList[4];
    QString strHumi = strList[5];

    if(lastDateTime.toSecsSinceEpoch() &lt; dateTime.toSecsSinceEpoch())
    {
        updateLastDateTime(true);
    }

    illuLine-&gt;append(dateTime.toMSecsSinceEpoch(), strIllu.toInt());
    humiLine-&gt;append(dateTime.toMSecsSinceEpoch(), strTemp.toDouble());
    tempLine-&gt;append(dateTime.toMSecsSinceEpoch(), strHumi.toDouble());
}</code></pre>
<hr />
<h3 id="5-4-clear-버튼---차트-초기화">5-4. Clear 버튼 - 차트 초기화</h3>
<pre><code class="language-cpp">void Tab4SensorChart::on_pPBchartClear_clicked()
{
    illuLine-&gt;clear();
    humiLine-&gt;clear();
    tempLine-&gt;clear();
    updateLastDateTime(false);
}</code></pre>
<hr />
<h2 id="6-mainwidget에-tab4-추가-및-소켓-연동">6. mainwidget에 Tab4 추가 및 소켓 연동</h2>
<h3 id="mainwidgeth">mainwidget.h</h3>
<pre><code class="language-cpp">#include &lt;tab4sensorchart.h&gt;

Tab4SensorChart *pTab4SensorChart;</code></pre>
<h3 id="mainwidgetcpp">mainwidget.cpp</h3>
<pre><code class="language-cpp">pTab4SensorChart = new Tab4SensorChart(ui-&gt;pTab4);
ui-&gt;pTab4-&gt;setLayout(pTab4SensorChart-&gt;layout());

connect(pTab2SocketClient, SIGNAL(tab4RecvDataSig(QStringList&amp;)),
        pTab4SensorChart, SLOT(tab4RecvDataSlot(QStringList&amp;)));</code></pre>
<p>Tab2의 <code>updateRecvDataSlot</code>에서 센서 데이터(<code>HUM</code> 등)를 파싱하여 <code>tab4RecvDataSig</code>로 emit하면 Tab4에서 수신하여 차트에 추가합니다.</p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>.pro에 charts 모듈 추가 (QT += charts)
    ↓
Tab4SensorChart 클래스 생성 (Qt Widgets Designer Form Class)
    ↓
UI 구성 (pChartViewLayout + Clear 버튼)
    ↓
생성자 : QLineSeries 3개 생성 및 색상 설정 (조도-빨강, 습도-초록, 온도-파랑)
    ↓
QChart에 시리즈 추가 → QChartView 생성 → pChartViewLayout에 추가
    ↓
QDateTimeAxis로 X축 시간 범위 설정
    ↓
tab4RecvDataSlot : 수신 데이터 파싱 → 각 시리즈에 append
    ↓
mainwidget에 Tab4 추가 및 Tab2 수신 시그널 연결</code></pre>