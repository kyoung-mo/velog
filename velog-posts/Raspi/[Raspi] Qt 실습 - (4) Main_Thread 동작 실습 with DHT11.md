<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/01d3d87e-cfa0-4e4f-8047-f588aba938d1/image.gif" /></p>
<hr />
<p>위 사진은 2초마다 메인쓰레드에서 온습도 데이터를 업데이트 해주는 모습입니다.</p>
<p>아래 두 코드가 메인 쓰레드에서 동작하게 합니다.</p>
<pre><code class="language-c">connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::on_btn_Read_clicked);
timer -&gt; start(2000);</code></pre>
<hr />
<h3 id="1-mainwindowui">1. mainwindow.ui</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3d9a97b0-b34f-45a8-ad09-846ffd868ea9/image.png" /></p>
<p>아래 두개는 워커 스레드에 필요</p>
<ul>
<li><code>QLable : labelHumi</code> -&gt; 현재는 필요x</li>
<li><code>QLable : labelTemp</code> -&gt; 현재는 필요x</li>
</ul>
<p>메인 쓰레드 사용 시 필요한 것</p>
<ul>
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

private slots:
    void on_btnRead_clicked();

private:
    Ui::MainWindow *ui;
};

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

#endif // MAINWINDOW_H</code></pre>
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

    QTimer *timer = new QTimer(this);
    connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::on_btnRead_clicked);
    timer-&gt;start(2000);

}

MainWindow::~MainWindow()
{
    delete ui;

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
<li>2초마다 : <code>[hh:mm:ss] Temp xx.xx'C | Humi L xx.xx%</code> 로그 한줄 출력</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3d19cd5f-ac7d-4886-b83d-56e5088dab4f/image.gif" /></p>
<hr />
<h3 id="실습-정리">실습 정리</h3>
<p><strong><code>MainWindow</code>는 메인 쓰레드에서 생성되고 동작한다.</strong></p>
<p><strong>QTimer 방식이 메인 쓰레드 방식인 이유?</strong>
timer를 MainWindow 안에서 만듦 -&gt; 메인 쓰레드 소속
timeout 시그널로 인해 호출되는 <code>on_btnRead_clicked</code>가 호출될 때도 메인 쓰레드에서 실행</p>