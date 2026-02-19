<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5a679de9-4868-4f51-9214-d9233d49085e/image.png" /></p>
<h3 id="ui-구조-핵심">UI 구조 핵심</h3>
<p>리눅스 GUI는 아래 구조로 동작한다.</p>
<p>Application (Qt 앱) → Qt Framework → Display Server (Wayland 또는 X11) →
Kernel / GPU Driver → Hardware</p>
<p>즉, Qt는 GUI를 만드는 프레임워크이고<br />Wayland는 화면에 출력하는 디스플레이 서버다.</p>
<hr />
<h3 id="x11-vs-wayland-핵심-차이">X11 vs Wayland 핵심 차이</h3>
<p>X11 구조:</p>
<p>Application → X Server → Kernel → Hardware</p>
<p>Wayland 구조:</p>
<p>Application → Wayland Compositor → Kernel → Hardware</p>
<p>차이점:</p>
<ul>
<li>Wayland는 구조가 단순해서 성능이 더 좋음</li>
<li>입력 지연(input latency)이 낮음</li>
<li>보안이 더 좋음</li>
<li>최신 Linux는 기본적으로 Wayland 사용</li>
</ul>
<p>Raspberry Pi OS Bookworm 이상은 기본이 Wayland다.</p>
<hr />
<h3 id="qt란-무엇인가">Qt란 무엇인가</h3>
<p>Qt는 GUI 애플리케이션을 만들기 위한 C++ 프레임워크다.</p>
<p>사용 가능한 기능:</p>
<ul>
<li>GUI (버튼, 창, 레이아웃)</li>
<li>OpenGL 그래픽</li>
<li>파일 입출력</li>
<li>네트워크</li>
<li>멀티스레드</li>
<li>임베디드 Linux 지원</li>
</ul>
<p>즉, Linux에서 GUI 프로그램 만들 때 가장 많이 사용하는 프레임워크 중
하나다.</p>
<hr />
<h3 id="qt-주요-모듈">Qt 주요 모듈</h3>
<p>QtCore<br />→ 자료구조, 파일, 스레드, 이벤트 루프</p>
<p>QtGui<br />→ 그래픽, 이미지, OpenGL</p>
<p>QtWidgets<br />→ 버튼, 창, 레이아웃</p>
<p>QtNetwork<br />→ TCP, UDP 통신</p>
<p>QtMultimedia<br />→ 카메라, 오디오, 비디오</p>
<hr />
<h3 id="raspberry-pi-5에서-qt6-사용하는-이유">Raspberry Pi 5에서 Qt6 사용하는 이유</h3>
<p>RPi5는 GPU 성능이 충분해서 Qt6 사용이 적합하다.</p>
<p>Qt6 장점:</p>
<ul>
<li>Wayland 완전 지원</li>
<li>GPU 가속 지원</li>
<li>성능 향상</li>
<li>최신 Linux 환경에 최적화</li>
</ul>
<p>Qt5는 레거시이고 신규 프로젝트는 Qt6 사용하는 것이 좋다.</p>
<p>추천 조합:</p>
<p>Raspberry Pi OS (64bit)\</p>
<ul>
<li>Wayland\</li>
<li>Qt 6.8 LTS</li>
</ul>
<hr />
<h3 id="qt6-설치-방법-rpi5">Qt6 설치 방법 (RPi5)</h3>
<p>패키지 설치:</p>
<p>sudo apt update sudo apt install qtcreator qt6-base-dev qt6-wayland</p>
<p>설치 확인:</p>
<p>qmake6 -v</p>
<p>또는</p>
<p>qtcreator --version</p>
<hr />
<h3 id="qt-creator-실행">Qt Creator 실행</h3>
<p>Wayland 환경:</p>
<p>qtcreator</p>
<p>X11 환경:</p>
<p>export DISPLAY=:0 qtcreator</p>
<hr />
<h3 id="x11-forwarding으로-실행-선택">X11 Forwarding으로 실행 (선택)</h3>
<p>Windows에서 실행:</p>
<p>qtcreator &amp;</p>
<p>또는</p>
<p>export DISPLAY=:0 qtcreator &amp;</p>
<p>Wayland 환경에서는 VNC 사용하는 것이 더 빠르다.</p>
<hr />
<h3 id="정리">정리</h3>
<pre><code class="language-c">// 1. Qt
→ GUI 만드는 프레임워크

// 2. Wayland
→ 화면 출력 담당

// 3. RPi5 권장 환경:
Wayland + Qt6

// 4. 설치
sudo apt install qtcreator qt6-base-dev qt6-wayland
</code></pre>
<p>이 조합이 가장 안정적이고 성능이 좋다.</p>