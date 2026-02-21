<p>기존 opencv를 삭제해주는 명령어를 한 번 입력하고 진행했다.</p>
<pre><code class="language-bash">$ sudo apt-get purge libopencv* python-opencv
$ sudo apt-get autoremove</code></pre>
<p>그리고는 모든 설치 전 국룰 명령어 update , upgrade 2줄 바로 입력해주기 !</p>
<pre><code class="language-bash">$ sudo apt-get update
$ sudo apt-get upgrade</code></pre>
<p>② opencv 설치 전 종속성 패키지 설치
그리고 나면 패키지 설치 지옥이 시작되는데 .., 요고 장난아니다</p>
<pre><code class="language-bash"># 컴파일러 또는 tool 설치
$ sudo apt-get install build-essential cmake

# 설치 된 패키지 조회 및 확인
$ sudo apt-get install pkg-config

# 이미지 관련 패키지
$ sudo apt-get install libjpeg-dev libtiff5-dev libpng-dev

# 비디오 관련 패키지
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev

# 비디오 관련 패키지 (Linux)
$ sudo apt-get install libv4l-dev v4l-utils

# 비디오 스트리밍 관련 패키지 
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev 

# GUI 관련 패키지 -&gt; 나중에 이것 때문에 고생을 굉장히 했다고 한다
$ sudo apt-get install libgtk2.0-dev
$ sudo apt-get install mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev  

# OpenCV 최적화 패키지
$ sudo apt-get install libatlas-base-dev gfortran libeigen3-dev 

# Python 관련 패키지
$ sudo apt-get install python2.7-dev python3-dev python-numpy python3-numpy</code></pre>
<pre><code class="language-bash">03:09:19 pi@pi-mo opencv ±|master ✗|→ sudo apt-get install mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package libgtkgl2.0-dev
E: Couldn't find any package by glob 'libgtkgl2.0-dev'
E: Couldn't find any package by regex 'libgtkgl2.0-dev'
E: Unable to locate package libgtkglext1-dev
03:09:23 pi@pi-mo opencv ±|master ✗|→  sudo apt-get install libatlas-base-dev gfortran libeigen3-dev
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Package libatlas-base-dev is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source
E: Package 'libatlas-base-dev' has no installation candidate
03:09:30 pi@pi-mo opencv ±|master ✗|→</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9c94b565-0281-40c8-87dc-71a266cf4ca7/image.png" /></p>
<p>여기서 GUI 관련 패키지인 gtk, openGL 요 부분 때문에 무한 실패를 겪었다 ^^;
늘 느끼는 교훈이지만 라이브러리를 설치할 때는 너무 여러 개를 참고하기보다는
공식 doc이나 전체 프로세스가 잘 나와있는 하나의 블로그를 참고하자 🙏🏻
(나는 여기저기 기웃거리다가 버전을 섞어 설치해서 대참사가 일어났다 ㅎ)</p>
<p>③ opencv 소스코드 다운로드
opencv의 github에 들어가면 현재 릴리즈 되어있는 여러 버전의 코드를 다운받을 수 있다.</p>
<p><img alt="opencv github" src="https://github.com/opencv/" /></p>
<p>우선 소스코드를 다운로드 받을 폴더를 하나 만들어 준 후에, 사진 속 1번과 2번을 모두 다운로드 받아준다.
command로 진행하는 경우 아래 명령어로 파일을 다운로드 받아 사용하면 된다.</p>
<p>-&gt; 저는 git clone 후 버전이 같은지 확인하기 위해 cmake시 에러 안나게 하기 위해 버전 맞추는 과정 </p>
<pre><code class="language-bash">git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

cd opencv
git checkout 4.10.0
cd ../opencv_contrib
git checkout 4.10.0</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/caf7294c-f411-4490-a2c9-2b8ff73d79a2/image.png" /></p>
<p>④ 컴파일 설정 및 설치 ⭐️
여기서부터 진짜 대참사 .., 이것 때문에 opencv랑 강제로 2일동안 썸타기 .. 🫶🏻
우선 정상적으로 작동했던 설정을 알려주고 맨 내가 겪었던 오류들은 다음 글에서 😭</p>
<p>✔️ 컴파일 설정
아래 코드를 복사해서 바로 입력하는 것이 아니라 잠시 메모장에 옮겨서 아래 주의사항을 확인해보도록 한다.</p>
<pre><code class="language-bash">cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=/home/pi/project/opencv/opencv_contrib/modules \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D BUILD_opencv_python2=OFF \
      -D BUILD_opencv_python3=OFF \
      -D BUILD_EXAMPLES=OFF \
      -D BUILD_TESTS=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D BUILD_DOCS=OFF \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_LIBV4L=ON \
      -D WITH_GSTREAMER=ON \
      -D WITH_GTK=ON \
      -D WITH_EIGEN=ON \
      -D WITH_FFMPEG=ON \
      -D ENABLE_FAST_MATH=ON \
      ..</code></pre>
<ul>
<li>빌드 후</li>
</ul>
<pre><code class="language-c">-- General configuration for OpenCV 4.10.0 =====================================
--   Version control:               4.10.0
--
--   Extra modules:
--     Location (extra):            /home/pi/project/opencv/opencv_contrib/modules
--     Version control (extra):     4.10.0
--
--   Platform:
--     Timestamp:                   2026-02-20T06:25:05Z
--     Host:                        Linux 6.12.62+rpt-rpi-2712 aarch64
--     CMake:                       3.31.6
--     CMake generator:             Unix Makefiles
--     CMake build tool:            /usr/bin/gmake
--     Configuration:               RELEASE
--
--   CPU/HW features:
--     Baseline:                    NEON FP16
--     Dispatched code generation:  NEON_DOTPROD NEON_FP16 NEON_BF16
--       requested:                 NEON_FP16 NEON_BF16 NEON_DOTPROD
--       NEON_DOTPROD (1 files):    + NEON_DOTPROD
--       NEON_FP16 (2 files):       + NEON_FP16
--       NEON_BF16 (0 files):       + NEON_BF16
--
--   C/C++:
--     Built as dynamic libs?:      YES
--     C++ standard:                11
--     C++ Compiler:                /usr/bin/c++  (ver 14.2.0)
--     C++ flags (Release):         -fsigned-char -ffast-math -fno-finite-math-only -W -Wall -Wreturn-type -Wnon-virtual-dtor -Waddress -Wsequence-point -Wformat -Wformat-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections    -fvisibility=hidden -fvisibility-inlines-hidden -O3 -DNDEBUG  -DNDEBUG
--     C++ flags (Debug):           -fsigned-char -ffast-math -fno-finite-math-only -W -Wall -Wreturn-type -Wnon-virtual-dtor -Waddress -Wsequence-point -Wformat -Wformat-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections    -fvisibility=hidden -fvisibility-inlines-hidden -g  -O0 -DDEBUG -D_DEBUG
--     C Compiler:                  /usr/bin/cc
--     C flags (Release):           -fsigned-char -ffast-math -fno-finite-math-only -W -Wall -Wreturn-type -Waddress -Wsequence-point -Wformat -Wformat-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections    -fvisibility=hidden -O3 -DNDEBUG  -DNDEBUG
--     C flags (Debug):             -fsigned-char -ffast-math -fno-finite-math-only -W -Wall -Wreturn-type -Waddress -Wsequence-point -Wformat -Wformat-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections    -fvisibility=hidden -g  -O0 -DDEBUG -D_DEBUG
--     Linker flags (Release):      -Wl,--gc-sections -Wl,--as-needed -Wl,--no-undefined
--     Linker flags (Debug):        -Wl,--gc-sections -Wl,--as-needed -Wl,--no-undefined
--     ccache:                      NO
--     Precompiled headers:         NO
--     Extra dependencies:          dl m pthread rt
--     3rdparty dependencies:
--
--   OpenCV modules:
--     To be built:                 alphamat aruco bgsegm bioinspired calib3d ccalib core datasets dnn dnn_objdetect dnn_superres dpm face features2d flann freetype fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor mcc ml objdetect optflow phase_unwrapping photo plot quality rapid reg rgbd saliency shape signal stereo stitching structured_light superres surface_matching text tracking video videoio videostab wechat_qrcode xfeatures2d ximgproc xobjdetect xphoto
--     Disabled:                    python3 world
--     Disabled by dependency:      -
--     Unavailable:                 cannops cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv hdf java julia matlab ovis python2 sfm ts viz
--     Applications:                apps
--     Documentation:               NO
--     Non-free algorithms:         YES
--
--   GUI:                           GTK2
--     GTK+:                        YES (ver 2.24.33)
--       GThread :                  YES (ver 2.84.4)
--       GtkGlExt:                  NO
--     VTK support:                 NO
--
--   Media I/O:
--     ZLib:                        /usr/lib/aarch64-linux-gnu/libz.so (ver 1.3.1)
--     JPEG:                        /usr/lib/aarch64-linux-gnu/libjpeg.so (ver 62)
--     WEBP:                        /usr/lib/aarch64-linux-gnu/libwebp.so (ver encoder: 0x0210)
--     PNG:                         /usr/lib/aarch64-linux-gnu/libpng.so (ver 1.6.48)
--     TIFF:                        /usr/lib/aarch64-linux-gnu/libtiff.so (ver 42 / 4.7.0)
--     JPEG 2000:                   build (ver 2.5.0)
--     OpenEXR:                     build (ver 2.3.0)
--     HDR:                         YES
--     SUNRASTER:                   YES
--     PXM:                         YES
--     PFM:                         YES
--
--   Video I/O:
--     DC1394:                      NO
--     FFMPEG:                      YES
--       avcodec:                   YES (61.19.101)
--       avformat:                  YES (61.7.100)
--       avutil:                    YES (59.39.100)
--       swscale:                   YES (8.3.100)
--       avresample:                NO
--     GStreamer:                   YES (1.26.2)
--     v4l/v4l2:                    YES (linux/videodev2.h)
--
--   Parallel framework:            pthreads
--
--   Trace:                         YES (with Intel ITT)
--
--   Other third-party libraries:
--     Lapack:                      NO
--     Eigen:                       YES (ver 3.4.0)
--     Custom HAL:                  YES (carotene (ver 0.0.1, Auto detected))
--     Protobuf:                    build (3.19.1)
--     Flatbuffers:                 builtin/3rdparty (23.5.9)
--
--   OpenCL:                        YES (no extra features)
--     Include path:                /home/pi/project/opencv/opencv/3rdparty/include/opencl/1.2
--     Link libraries:              Dynamic load
--
--   Python (for build):            /usr/bin/python3
--
--   Java:
--     ant:                         /bin/ant (ver 1.10.15)
--     Java:                        NO
--     JNI:                         NO
--     Java wrappers:               NO
--     Java tests:                  NO
--
--   Install to:                    /usr/local
-- -----------------------------------------------------------------
--
-- Configuring done (37.9s)
-- Generating done (0.7s)
-- Build files have been written to: /home/pi/project/opencv/opencv/build</code></pre>
<p>이후 <code>make -j4</code>, <code>sudo make install</code> 을 해줘야한다는데 1-2시간 걸린다고 해서..</p>
<hr />
<p><code>sudo apt install libopencv-dev</code> 먼저 진행</p>
<p>설치 확인</p>
<pre><code class="language-bash">03:29:35 pi@pi-mo build ±|✔|→ pkg-config --modversion opencv4
4.10.0</code></pre>
<hr />
<p><strong>1. CMakeLists.txt</strong></p>
<pre><code class="language-c">cmake_minimum_required(VERSION 3.16)

project(camrea VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets Multimedia MultimediaWidgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets Multimedia MultimediaWidgets)
find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        mainwindow.h
        mainwindow.ui
)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(camrea
        MANUAL_FINALIZATION
        ${PROJECT_SOURCES}
    )
# Define target properties for Android with Qt 6 as:
#    set_property(TARGET camrea APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
#                 ${CMAKE_CURRENT_SOURCE_DIR}/android)
# For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation
else()
    if(ANDROID)
        add_library(camrea SHARED
            ${PROJECT_SOURCES}
        )
# Define properties for Android with Qt 5 after find_package() calls as:
#    set(ANDROID_PACKAGE_SOURCE_DIR &quot;${CMAKE_CURRENT_SOURCE_DIR}/android&quot;)
    else()
        add_executable(camrea
            ${PROJECT_SOURCES}
        )
    endif()
endif()

target_link_libraries(camrea PRIVATE
  Qt${QT_VERSION_MAJOR}::Widgets
  Qt${QT_VERSION_MAJOR}::Multimedia
  Qt${QT_VERSION_MAJOR}::MultimediaWidgets
  ${OpenCV_LIBS}
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
if(${QT_VERSION} VERSION_LESS 6.1.0)
  set(BUNDLE_ID_OPTION MACOSX_BUNDLE_GUI_IDENTIFIER com.example.camrea)
endif()
set_target_properties(camrea PROPERTIES
    ${BUNDLE_ID_OPTION}
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

include(GNUInstallDirs)
install(TARGETS camrea
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(camrea)
endif()</code></pre>
<p><strong>2.  mainwindow.h</strong></p>
<pre><code class="language-c">#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include &lt;QMainWindow&gt;
#include &lt;QCamera&gt;
#include &lt;QMediaCaptureSession&gt;
#include &lt;QVideoWidget&gt;
#include &lt;QCameraDevice&gt;
#include &lt;QVideoSink&gt;
#include &lt;QVideoFrame&gt;
#include &lt;QLabel&gt;

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
    void processFrame(const QVideoFrame &amp;frame);

private:
    Ui::MainWindow *ui;
    QCamera *camera;
    QMediaCaptureSession *captureSession;
    QVideoSink *videoSink;  // QVideoWidget 대신 QVideoSink 사용
};

#endif</code></pre>
<p><strong>3. mainwindow.cpp</strong></p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &lt;ui_mainwindow.h&gt;
#include &lt;QMediaDevices&gt;
#include &lt;QVBoxLayout&gt;
#include &lt;opencv2/opencv.hpp&gt;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui-&gt;setupUi(this);

    const QList&lt;QCameraDevice&gt; cameras = QMediaDevices::videoInputs();
    if (cameras.isEmpty()) {
        qDebug() &lt;&lt; &quot;연결된 USB 카메라를 찾을 수 없습니다.&quot;;
        return;
    }

    camera = new QCamera(cameras.first(), this);
    captureSession = new QMediaCaptureSession(this);
    videoSink = new QVideoSink(this);

    captureSession-&gt;setCamera(camera);
    captureSession-&gt;setVideoOutput(videoSink);

    // 프레임마다 processFrame 호출
    connect(videoSink, &amp;QVideoSink::videoFrameChanged,
            this, &amp;MainWindow::processFrame);

    camera-&gt;start();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::processFrame(const QVideoFrame &amp;frame)
{
    if (!frame.isValid())
        return;

    // QVideoFrame → QImage
    QImage img = frame.toImage().convertToFormat(QImage::Format_RGB888);
    if (img.isNull())
        return;

    // QImage → cv::Mat
    cv::Mat mat(img.height(), img.width(), CV_8UC3,
                (void*)img.bits(), img.bytesPerLine());

    // Gray 변환
    cv::Mat gray;
    cv::cvtColor(mat, gray, cv::COLOR_RGB2GRAY);

    // cv::Mat → QImage → QLabel에 표시
    QImage grayImg(gray.data, gray.cols, gray.rows,
                   gray.step, QImage::Format_Grayscale8);

    ui-&gt;cameraLabel-&gt;setPixmap(
        QPixmap::fromImage(grayImg).scaled(
            ui-&gt;cameraLabel-&gt;size(), Qt::KeepAspectRatio));
}</code></pre>