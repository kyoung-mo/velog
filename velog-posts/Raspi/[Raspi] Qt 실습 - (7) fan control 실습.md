<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/87977b04-8b42-42d2-a8b2-3a087f206c1e/image.gif" /></p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f81ddf64-ee70-4854-8b76-9fcf144a4094/image.png" /></p>
<p><code>/boot/firmware/config.txt</code> 에서 기존에 팬 관련 설정 부분을 주석처리해주었다.</p>
<p>C언어로 라즈베리 파이 5의 펜 속도를 제어하려면 시스템 파일인 <code>/sys/class/thermal/cooling_device0/cur_state</code>에 정수 값을 쓰는 방식을 사용한다고 한다.</p>
<hr />
<p><strong>구현 시 주의사항 (권한 문제)</strong></p>
<p><code>/sys/class/thermal/cooling_device0/cur_state</code> 파일은 기본적으로 <strong>root(sudo)</strong> 권한이 필요합니다. C 프로그램이나 Qt 앱을 일반 사용자로 실행하면 파일 열기에 실패할 수 있습니다.</p>
<p><strong>udev 규칙 설정:</strong> 부팅 시 해당 파일의 쓰기 권한을 일반 사용자에게 부여하도록 <code>udev</code> 규칙을 추가할 수 있습니다. (추천 방식)</p>
<ul>
<li><code>/etc/udev/rules.d/99-fan.rules</code> 파일을 만들고 아래 내용 추가</li>
</ul>
<pre><code class="language-c">SUBSYSTEM==&quot;thermal&quot;, KERNEL==&quot;cooling_device*&quot;, ACTION==&quot;add&quot;, RUN+=&quot;/bin/chmod 666 /sys/class/thermal/%k/cur_state&quot;</code></pre>
<pre><code class="language-c">sudo reboot</code></pre>
<hr />
<p><strong>제어 단계(State) 설명</strong></p>
<table>
<thead>
<tr>
<th><strong>State 값</strong></th>
<th><strong>온도</strong></th>
<th><strong>동작</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>0</strong></td>
<td>Off</td>
<td>펜이 완전히 멈춤</td>
</tr>
<tr>
<td><strong>1</strong></td>
<td>40'C 이상</td>
<td>낮은 소음으로 가동 시작</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td>45'C 이상</td>
<td>일반적인 부하 상태</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td>55'C 이상</td>
<td>고온 상태 대응</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td>65'C 이상</td>
<td>최대 풍량 (소음 발생)</td>
</tr>
</tbody></table>
<hr />
<p><strong>UI 설정</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/df139594-f817-437b-ae0b-9fd8fd140fbb/image.png" /></p>
<h3 id="코드">코드</h3>
<p>** 1.  <code>MainWindow.h</code>**</p>
<pre><code class="language-c">#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include &lt;QMainWindow&gt;
#include &lt;QTimer&gt;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void updateStatus();           // 1초마다 온도 읽기 + 자동제어
    void onSliderChanged(int value); // 슬라이더 수동 제어
    void onAutoModeToggled(bool checked); // 자동/수동 모드 전환

private:
    Ui::MainWindow *ui;
    QTimer *timer;

    float readTemperature();       // 온도 읽기
    int   readFanState();          // 현재 팬 상태 읽기
    void  setFanState(int state);  // 팬 상태 쓰기
    int   autoFanControl(float temp); // 온도 → 팬 단계 계산
};

#endif</code></pre>
<p>** 2. <code>MainWindow.cpp</code>**</p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;ui_mainwindow.h&quot;
#include &lt;QFile&gt;
#include &lt;QTextStream&gt;
#include &lt;QDebug&gt;

#define TEMP_PATH  &quot;/sys/class/thermal/thermal_zone0/temp&quot;
#define FAN_PATH   &quot;/sys/class/thermal/cooling_device0/cur_state&quot;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui-&gt;setupUi(this);

    // 슬라이더 범위 설정
    ui-&gt;fanSlider-&gt;setRange(0, 4);
    ui-&gt;fanSlider-&gt;setValue(0);

    // 시그널 연결
    connect(ui-&gt;fanSlider,   &amp;QSlider::valueChanged,
            this,            &amp;MainWindow::onSliderChanged);
    connect(ui-&gt;autoCheckBox, &amp;QCheckBox::toggled,
            this,             &amp;MainWindow::onAutoModeToggled);

    // 타이머 1초마다 updateStatus 호출
    timer = new QTimer(this);
    connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::updateStatus);
    timer-&gt;start(1000);

    // 초기 상태
    ui-&gt;autoCheckBox-&gt;setChecked(true);
    ui-&gt;fanSlider-&gt;setEnabled(false);
}

MainWindow::~MainWindow()
{
    setFanState(0); // 종료 시 팬 끄기
    delete ui;
}

// ── 온도 읽기 ──────────────────────────────────────
float MainWindow::readTemperature()
{
    QFile file(TEMP_PATH);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return -1.0f;

    QTextStream in(&amp;file);
    int raw = in.readLine().trimmed().toInt();
    file.close();
    return raw / 1000.0f; // 마이크로도 → 섭씨
}

// ── 팬 상태 읽기 ───────────────────────────────────
int MainWindow::readFanState()
{
    QFile file(FAN_PATH);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return -1;

    QTextStream in(&amp;file);
    int state = in.readLine().trimmed().toInt();
    file.close();
    return state;
}

// ── 팬 상태 쓰기 ───────────────────────────────────
void MainWindow::setFanState(int state)
{
    QFile file(FAN_PATH);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qDebug() &lt;&lt; &quot;팬 파일 열기 실패 (권한 확인)&quot;;
        return;
    }
    QTextStream out(&amp;file);
    out &lt;&lt; state;
    file.close();
}

// ── 온도 → 팬 단계 자동 계산 ──────────────────────
int MainWindow::autoFanControl(float temp)
{
    if      (temp &gt;= 65.0f) return 4;
    else if (temp &gt;= 55.0f) return 3;
    else if (temp &gt;= 45.0f) return 2;
    else if (temp &gt;= 40.0f) return 1;
    else                    return 0;
}

// ── 1초마다 호출 ───────────────────────────────────
void MainWindow::updateStatus()
{
    float temp = readTemperature();
    int   fan  = readFanState();

    // UI 업데이트
    ui-&gt;tempLabel-&gt;setText(QString(&quot;온도: %1 °C&quot;).arg(temp, 0, 'f', 1));
    ui-&gt;fanLabel -&gt;setText(QString(&quot;팬 상태: %1 / 4&quot;).arg(fan));
    ui-&gt;fanSlider-&gt;blockSignals(true);
    ui-&gt;fanSlider-&gt;setValue(fan);
    ui-&gt;fanSlider-&gt;blockSignals(false);

    // 자동 모드일 때만 팬 제어
    if (ui-&gt;autoCheckBox-&gt;isChecked()) {
        int target = autoFanControl(temp);
        if (target != fan)
            setFanState(target);
    }
}

// ── 슬라이더 변경 (수동 모드) ──────────────────────
void MainWindow::onSliderChanged(int value)
{
    if (!ui-&gt;autoCheckBox-&gt;isChecked())
        setFanState(value);
}

// ── 자동/수동 모드 전환 ────────────────────────────
void MainWindow::onAutoModeToggled(bool checked)
{
    ui-&gt;fanSlider-&gt;setEnabled(!checked);
    if (checked) {
        qDebug() &lt;&lt; &quot;자동 모드 ON&quot;;
    } else {
        qDebug() &lt;&lt; &quot;수동 모드 ON&quot;;
    }
}
---
</code></pre>