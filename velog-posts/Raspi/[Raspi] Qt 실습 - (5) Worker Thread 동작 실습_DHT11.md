<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/722d7111-56ae-42fd-9059-c9adfa0f9338/image.gif" /></p>
<hr />
<p>미세해서 안 보이지만.. 오른쪽에 있는 라벨에 2초마다 워커쓰레드에서 온습도 데이터를 업데이트 해주는 모습입니다.</p>
<p>메인 쓰레드를 사용하여 2초마다 sleep 시 다른 쓰레드 혹은 프로세스들도 동작하다가 2초 멈췄다가 반복하게 되는 문제가 있습니다.</p>
<p>Qt 실습 (4)에서 아래 두 코드가 메인 쓰레드에서 동작한다.</p>
<pre><code class="language-c">connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::on_btn_Read_clicked);
timer -&gt; start(2000);</code></pre>
<p>일단 수업 내용 정리하고, 관련 개념 따로 정리하겠습니다.</p>
<hr />
<h3 id="1-mainwindowui">1. mainwindow.ui</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3d9a97b0-b34f-45a8-ad09-846ffd868ea9/image.png" /></p>
<ul>
<li><code>QLable : labelHumi</code> -&gt; 이후에 워커 쓰레드 데이터 받아 바뀔 부분</li>
<li><code>QLable : labelTemp</code> -&gt; 이후에 워커 쓰레드 데이터 받아 바뀔 부분</li>
<li><code>QPushButton : btnRead</code></li>
<li><code>QTextBrowser : textBrowser</code></li>
<li><code>QMenuBar : menubar</code></li>
<li><code>QStatusBar : statusbar</code></li>
</ul>
<hr />
<h3 id="2-mainwindowh">2. mainwindow.h</h3>
<pre><code class="language-c">#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include &lt;QMainWindow&gt;
#include &lt;QThread&gt;
#include &quot;sensorWorker.h&quot;

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void updateUI(float temp,float hum1);

private slots:
    void on_btnRead_clicked();

private:
    Ui::MainWindow *ui;
    SensorWorker *m_worker = nullptr;
    QThread *m_thread = nullptr;
};

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

#endif // MAINWINDOW_H</code></pre>
<hr />
<h3 id="3-sensorworkerh-추가">3. sensorWorker.h (추가)</h3>
<pre><code class="language-c">#ifndef SENSORWORKER_H
#define SENSORWORKER_H

#include &lt;QObject&gt;
#include &lt;QFile&gt;
#include &lt;QThread&gt;

class SensorWorker : public QObject {
    Q_OBJECT

public slots:
    // 실제 센서를 읽는 루프
    void process() {
        while (m_running) {
            QString tempPath = &quot;/sys/bus/iio/devices/iio:device0/in_temp_input&quot;;
            QString humiPath = &quot;/sys/bus/iio/devices/iio:device0/in_humidityrelative_input&quot;;

            float temp = readValue(tempPath) / 1000.0f;
            float humi = readValue(humiPath) / 1000.0f;

            emit sensorDataReady(temp, humi); // 메인 스레드로 데이터 전송
            QThread::msleep(2000); // 2초 대기
        }
        emit finished();
    }

    void stop() { m_running = false; }

signals:
    void sensorDataReady(float temp, float humi);
    void finished();

private:
    bool m_running = true;

    float readValue(QString path) {
        QFile file(path);
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
            return 0.0f;
        QTextStream in(&amp;file);
        QString line = in.readLine();
        file.close();
        return line.toFloat();
    }
};

#endif // SENSORWORKER_H
</code></pre>
<hr />
<h3 id="4-maincpp">4. main.cpp</h3>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;

#include &lt;QApplication&gt;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}</code></pre>
<hr />
<h3 id="5-mainwindowcpp">5. mainwindow.cpp</h3>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;./ui_mainwindow.h&quot;
#include &lt;QFile&gt;
#include &lt;QTextStream&gt;
#include &lt;QDateTime&gt;
#include &lt;QDebug&gt;
#include &lt;QTimer&gt;
#include &quot;sensorWorker.h&quot;
#include &lt;QThread&gt;

float readDevice0Value(QString path){
    QFile file(path);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return -1.0f;

    QTextStream in(&amp;file);
    QString line = in.readLine();
    file.close();

    return line.toFloat() / 1000.0f;
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui-&gt;setupUi(this);

    //QTimer *timer = new QTimer(this);
    //connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::on_btnRead_clicked);
    //timer-&gt;start(2000);

    m_thread = new QThread(this);
    m_worker = new SensorWorker();
    m_worker -&gt; moveToThread(m_thread);

    connect(m_worker, &amp;SensorWorker::sensorDataReady, this, &amp;MainWindow::updateUI);
    connect(m_worker, &amp;SensorWorker::finished,m_thread, &amp;QThread::quit);
    connect(m_worker, &amp;SensorWorker::finished,m_worker, &amp;SensorWorker::deleteLater);
    connect(m_thread, &amp;QThread::finished,m_thread, &amp;QThread::deleteLater);
    connect(m_thread, &amp;QThread::started,m_worker, &amp;SensorWorker::process);
    m_thread-&gt;start();

}

MainWindow::~MainWindow()
{
    if(m_worker)
        m_worker-&gt;stop();
    if(m_thread &amp;&amp; m_thread-&gt;isRunning()){
        m_thread-&gt;quit();
        m_thread-&gt;wait();
    }
    delete ui;

}

void MainWindow::updateUI(float temp, float humi)
{
    ui-&gt;labelHumi-&gt;setText(QString::number(humi, 'f', 1) + &quot; 'C&quot;);
    ui-&gt;labelTemp-&gt;setText(QString::number(temp, 'f', 1) + &quot; %&quot;);

    // 이전에 만든 그래프 append 로직도 여기서 수행 가능
    // tempSeries-&gt;append(timeStep++, temp);
}

void MainWindow::on_btnRead_clicked()
{
    QString tempPath = &quot;/sys/bus/iio/devices/iio:device0/in_temp_input&quot;;
    QString humiPath = &quot;/sys/bus/iio/devices/iio:device0/in_humidityrelative_input&quot;;

    float temp = readDevice0Value(tempPath);
    float humi = readDevice0Value(humiPath);

    QString currentTime = QDateTime::currentDateTime().toString(&quot;hh:mm:ss&quot;);
    QString result = QString(&quot;[%1] Temp:%2°C | Humi: %3%&quot;)
                         .arg(currentTime)
                         .arg(temp, 0, 'f', 2)
                         .arg(humi, 0, 'f', 2);

    ui-&gt;textBrowser-&gt;append(result);
}</code></pre>
<hr />
<p>위와 같이 UI 구성, 코드를 작성했을 때 아래와 같이 동작합니다.</p>
<ul>
<li>버튼 누를 시 : <code>[hh:mm:ss] Temp xx.xx'C | Humi L xx.xx%</code> 로그 한줄 출력</li>
<li>2초마다 : 오른쪽 label 데이터 값 바뀜</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d9d4464c-64f2-4c3c-8f8f-65a018975ba6/image.gif" /></p>
<hr />
<h3 id="실습-정리">실습 정리</h3>
<p><strong>1. <code>MainWindow</code>는 메인 쓰레드에서 생성되고 동작한다.</strong>
<strong>2. 메인 쓰레드 vs 워커 쓰레드는 어느 쓰레드에서 코드가 실행되느냐? 의 차이이다.</strong></p>
<ol>
<li><p>실습(4)의 QTimer 방식이 메인 쓰레드 방식인 이유?
timer를 MainWindow 안에서 만듦 -&gt; 메인 쓰레드 소속
timeout 시그널로 인해 호출되는 <code>on_btnRead_clicked</code>가 호출될 때도 메인 쓰레드에서 실행</p>
</li>
<li><p>QThread 방식이 워커 쓰레드인 이유?</p>
<pre><code class="language-c">worker -&gt; moveToThread(thread); // 핵심 코드⭐
thread -&gt; start();</code></pre>
<p>첫 번째 줄의 코드가 핵심인데, 이 한줄로 worker 객체의 소속을 메인 thread에서 thread로 옮긴다. worker의 슬록들은 전부 thread에서 실행된다.
thread -&gt; start(); 시 thread가 실행되면서 started 시그널이 발생하는데, 이 때 worker -&gt; process()가 워커 쓰레드에서 호출된다.</p>
</li>
</ol>
<p><strong>즉, 메인 쓰레드는 영향을 받지 않는다.</strong></p>