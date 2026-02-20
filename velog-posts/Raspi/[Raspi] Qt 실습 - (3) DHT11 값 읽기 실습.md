<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/89b83594-1a6f-4936-a29e-71ac0edd232e/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5dcbd120-081e-498c-9105-4654a5554943/image.png" /></p>
<p>위 두 사진을 참고해서, GPIO핀에 DATA를 연결하고, 간단하게 dtoverlay 명령어를 통해 값을 읽어봅시다.</p>
<pre><code class="language-bash">sudo dtoverlay dht11,gpiopin=4</code></pre>
<p>위 명령어를 통해 gpio 4번 핀에 dht11을 쓰겠다고 설정을 해줍니다.</p>
<pre><code class="language-bash"># 1. 장치 확인 (iio:device0 같은 게 있어야 함)
ls /sys/bus/iio/devices/

# 2. 온도 읽기 (단위: 1000분의 1도, 즉 25000 = 25.0도)
cat /sys/bus/iio/devices/iio:device0/in_temp_input

# 3. 습도 읽기 (단위: 1000분의 1%, 즉 40000 = 40.0%)
cat /sys/bus/iio/devices/iio:device0/in_humidityrelative_input</code></pre>
<p>위 명령어를 통해 장치가 연결됐는지 확인하고, 온도 및 습도를 읽어올 수 있습니다.</p>
<hr />
<h3 id="trouble-shooting">Trouble Shooting)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fc100685-5645-4c7f-ae34-6d5facb0177e/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7e013aed-ed5a-4a4b-a85f-3ae97084222d/image.png" /></p>
<p>gpio 4번 핀을 설정해주고, <code>ls /sys/bus/iio/devices/</code> 명령어를 입력했음에도 아무것도 뜨지 않았습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/327a50e3-ece1-40b4-9fd8-ae9346d415e4/image.png" /></p>
<p>아까 UART, I2C, 1W 통신  등을 전부 설정해놨더니, 4번 핀이 이미 1 Wire 통신으로 잡혀있던것이 이유였습니다.</p>
<p><code>pinctrl</code> 명령어를 통해 gpio 핀의 점유 상태를 확인하고, 나는 17번 핀이 none이라 17번 핀으로 설정해주었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/64ab3f79-1e5d-4b20-be1a-9c8baad44237/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fe2a1221-e536-42b3-9385-99057a3106f3/image.png" /></p>
<p>이후 값이 잘 뜨는 것을 확인하였습니다.</p>
<hr />
<p>다시 Qt로 돌아와서,</p>
<h3 id="1-mainwindowui">1. mainwindow.ui</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f5e846c9-509d-4dc5-9620-4f8adf848bf1/image.png" /></p>
<ul>
<li>pressButton 의 객체 이름 <code>btnRead</code> 로 생성 or 설정</li>
<li>textBrowser 생성</li>
</ul>
<h3 id="2-mainwindowh">2. mainwindow.h</h3>
<p>원본에서 QT_BEGIN_NAMESPACE ~ QT_END_NAMESPACE 블록이 맨 위에 있었는데, 아래로 내려서 #endif 바로 위에 위치하도록 변경했습니다.</p>
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
<h3 id="3-maincpp---그대로">3. main.cpp -&gt; 그대로</h3>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;

#include &lt;QApplication&gt;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}</code></pre>
<h3 id="4-mainwindowcpp">4. mainwindow.cpp</h3>
<p>① include 추가
기존에 <code>&lt;QMessageBox&gt;</code>, <code>&lt;QMainWindow&gt;</code>, <code>&lt;QString&gt;</code> 이 있었는데, 실제로 필요한 것들로 정리했습니다.</p>
<pre><code class="language-bash">제거 : &lt;QMessageBox&gt;, &lt;QMainWindow&gt;, &lt;QString&gt;
추가 : &lt;QDateTime&gt;, &lt;QDebug&gt;</code></pre>
<p>② readDevice0Value 함수 구현
기존에는 return 0.0f 만 있던 빈 함수였는데, 실제로 파일을 열어서 값을 읽고 / 1000.0f 해서 반환하는 코드로 바꿨습니다.</p>
<p>③ on_btnRead_clicked 완성
기존에는 result 문자열 생성까지만 있었는데, 
<code>ui-&gt;textBrowser-&gt;append(result)</code> 로 실제로 화면에 출력하는 코드를 추가했습니다.</p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;./ui_mainwindow.h&quot;
#include &lt;QFile&gt;
#include &lt;QTextStream&gt;
#include &lt;QDateTime&gt;
#include &lt;QDebug&gt;

float readDevice0Value(QString path){
    QFile file(path);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return 0.0f;

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
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f262c3c7-4319-49d0-b4e0-3730ee199335/image.png" /></p>
<p>센서 값을 잘 읽어오는 것을 확인할 수 있습니다.</p>