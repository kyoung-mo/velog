<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/eb4f78f6-72f5-441e-8f52-32cb5b700c42/image.png" /></p>
<p>Qt6에서 센서 데이터를 그래프로 시각화하기 위해 <strong>Qt Charts</strong> 모듈을 사용해보는 실습을 진행하겠습니다. <code>QLineSeries</code>를 이용해 실시간으로 변하는 온도와 습도 데이터를 선 그래프로 표현해보겠습니다.</p>
<p>아래 명령어를 통해 charts 패키지를 설치해줍니다.</p>
<pre><code class="language-bash">sudo apt install libqt6charts6-dev # 둘 중 하나
sudo apt install qt6-charts-dev</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d50b516c-2279-477a-8ffb-0fdaebe8408b/image.png" /></p>
<p>설치후 Qt6다시 시작해줍니다.</p>
<hr />
<h3 id="1-cmakeliststxt">1. CMakeLists.txt</h3>
<p>Qt Charts 모듈을 프로젝트에 포함해야 하기 때문에, 아래 내용을 <code>CMakeLists.txt</code> 에 추가해줍니다.</p>
<ul>
<li><code>find_package()</code> 수정
<img alt="" src="https://velog.velcdn.com/images/mommers/post/4139b838-d341-4691-8c9f-7d5b85e3ec1c/image.png" /></li>
<li><code>target_link_libraries()</code> 수정
<img alt="" src="https://velog.velcdn.com/images/mommers/post/c0682451-c2cb-47df-b632-f3a1f9a64366/image.png" /></li>
</ul>
<pre><code class="language-c">find_package(Qt6 REQUIRED COMPONENTS Widgets Charts)

target_link_libraries(sensor_project PRIVATE 
    Qt6::Widgets 
    Qt6::Charts
)</code></pre>
<p>mainwindow.ui</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0a99c673-0851-437e-b55f-0c0e4ace6a2f/image.png" /></p>
<p><code>mainwindow.ui</code>에서 그래프가 표시될 영역을 만듭니다.</p>
<ol>
<li><strong>Vertical Layout</strong> 또는 <strong>Widget</strong>을 하나 배치합니다 (객체 이름: <code>chartLayout</code> 또는 <code>chartWidget</code>).</li>
<li>코드로 <code>QChartView</code>를 생성하여 이 레이아웃에 추가할 것입니다.</li>
</ol>
<hr />
<h3 id="코드">코드</h3>
<p>** 1. <code>CMakeList.txt</code>**</p>
<pre><code class="language-c">cmake_minimum_required(VERSION 3.16)

project(sensor_chart VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets Charts)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets Charts)

set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        mainwindow.h
        mainwindow.ui
)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(sensor_chart
        MANUAL_FINALIZATION
        ${PROJECT_SOURCES}
    )
# Define target properties for Android with Qt 6 as:
#    set_property(TARGET sensor_chart APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
#                 ${CMAKE_CURRENT_SOURCE_DIR}/android)
# For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation
else()
    if(ANDROID)
        add_library(sensor_chart SHARED
            ${PROJECT_SOURCES}
        )
# Define properties for Android with Qt 5 after find_package() calls as:
#    set(ANDROID_PACKAGE_SOURCE_DIR &quot;${CMAKE_CURRENT_SOURCE_DIR}/android&quot;)
    else()
        add_executable(sensor_chart
            ${PROJECT_SOURCES}
        )
    endif()
endif()

target_link_libraries(sensor_chart PRIVATE
  Qt${QT_VERSION_MAJOR}::Widgets
  Qt${QT_VERSION_MAJOR}::Charts
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
if(${QT_VERSION} VERSION_LESS 6.1.0)
  set(BUNDLE_ID_OPTION MACOSX_BUNDLE_GUI_IDENTIFIER com.example.sensor_chart)
endif()
set_target_properties(sensor_chart PROPERTIES
    ${BUNDLE_ID_OPTION}
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

include(GNUInstallDirs)
install(TARGETS sensor_chart
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(sensor_chart)
endif()</code></pre>
<p>** 2. <code>MainWindow.h</code>**</p>
<pre><code class="language-c">#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include &lt;QMainWindow&gt;
#include &lt;QtCharts/QChartView&gt;
#include &lt;QtCharts/QLineSeries&gt;
#include &lt;QtCharts/QValueAxis&gt;
#include &lt;QTimer&gt;

namespace Ui { class MainWindow; }

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
private slots:
    void updateSensorData();
private:
    Ui::MainWindow *ui;
    QLineSeries *tempSeries;
    QLineSeries *humiSeries;
    QChart *chart;
    QTimer *timer;
    int timeStep = 0;
};

#endif // MAINWINDOW_H
</code></pre>
<p>** 3. <code>MainWindow.cpp</code>**</p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;./ui_mainwindow.h&quot;
#include &lt;QFile&gt;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui-&gt;setupUi(this);

    // 1. 시리즈 및 차트 초기화
    tempSeries = new QLineSeries();
    tempSeries-&gt;setName(&quot;온도 (°C)&quot;);
    humiSeries = new QLineSeries();
    humiSeries-&gt;setName(&quot;습도 (%)&quot;);

    chart = new QChart();
    chart-&gt;addSeries(tempSeries);
    chart-&gt;addSeries(humiSeries);
    chart-&gt;createDefaultAxes();
    chart-&gt;axes(Qt::Vertical).first()-&gt;setRange(0, 100); // Y축 범위 설정

    // 2. 차트 뷰를 UI 레이아웃에 추가
    QChartView *chartView = new QChartView(chart);
    chartView-&gt;setRenderHint(QPainter::Antialiasing);
    ui-&gt;chartLayout-&gt;addWidget(chartView);

    // 3. 타이머 설정 (1초마다 업데이트)
    timer = new QTimer(this);
    connect(timer, &amp;QTimer::timeout, this, &amp;MainWindow::updateSensorData);
    timer-&gt;start(1000);


}

void MainWindow::updateSensorData() {
    auto readVal = [](QString path) {
        QFile file(path);
        if (!file.open(QIODevice::ReadOnly)) return 0.0f;
        return file.readAll().trimmed().toFloat() / 1000.0f;
    };

    float t = readVal(&quot;/sys/bus/iio/devices/iio:device0/in_temp_input&quot;);
    float h = readVal(&quot;/sys/bus/iio/devices/iio:device0/in_humidityrelative_input&quot;);

    // 데이터 추가
    tempSeries-&gt;append(timeStep, t);
    humiSeries-&gt;append(timeStep, h);
    timeStep++;

    // X축 범위 동적 업데이트 (최신 20개 데이터만 보이게)
    if (timeStep &gt; 20) {
        chart-&gt;axes(Qt::Horizontal).first()-&gt;setRange(timeStep - 20, timeStep);
    } else {
        chart-&gt;axes(Qt::Horizontal).first()-&gt;setRange(0, 20);
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}
</code></pre>
<hr />
<p>시스템 파일의 값은 $milli$ 단위이므로 </p>
<p>$Value_{actual} = \frac{Value_{sys}}{1000}$ 연산을 수행합니다.</p>
<pre><code class="language-c">axis-&gt;setRange() // 실시간 그래프 갱신
QPainter::Antialiasing // 안티 엘리어싱 적용</code></pre>
<p><code>timeStep</code>이 늘어남에 따라 <code>axis-&gt;setRange()</code>를 호출하여 그래프가 왼쪽으로 흐르는 효과를 줄 수 있습니다. MobaXterm 원격 화면에서도 선이 부드럽게 보이게 하기 위해 <code>QPainter::Antialiasing</code>를 통해 안티 엘리어싱 설정을 해주었습니다.</p>
<p>X11 포워딩 환경에서 그래프 갱신이 너무 빠르면 버벅일 수 있기 때문에 타이머 주기를 <code>2000</code> (2초) 이상으로 설정해주었습니다.</p>