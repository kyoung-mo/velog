<h3 id="raspi-config">raspi-config</h3>
<p><code>raspi-config</code>는 라즈베리파이 운영체제의 기본 설정을 간편하게 관리할수 있는 터미널 기반 설정 도구이다.
CLI 환경에서도 GUI 환경 비슷하게 설정을 바꿀 수 있다는 점이 메리트가 있다!</p>
<p>라즈베리파이만 지원되고, STM32, OrangePi 등등의 보드에서는 지원이 안되는 기능이다.</p>
<pre><code class="language-c">sudo raspi-config // 라즈베리파이 전용 설정 GUI</code></pre>
<p>명령어를 통해 접속할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/941a220e-4ff6-4a15-ac18-5ee6623a70b8/image.png" /></p>
<hr />
<h2 id="기능-별-정리">기능 별 정리</h2>
<h3 id="1-system-options-기본-설정">1. System Options (기본 설정)</h3>
<ul>
<li><strong>S1 Wireless LAN (와이파이)</strong><ul>
<li>와이파이 이름(SSID)과 비밀번호 입력 및 연결 설정.</li>
</ul>
</li>
<li><strong>S2 Audio (오디오)</strong><ul>
<li>소리 출력 장치 선택 (HDMI 또는 3.5mm 잭).</li>
</ul>
</li>
<li><strong>S3 Password (비밀번호)</strong><ul>
<li>현재 사용자(<code>pi</code>)의 로그인 비밀번호 변경.</li>
</ul>
</li>
<li><strong>S4 Hostname (호스트 이름)</strong><ul>
<li>네트워크상에서 표시될 기기 이름 설정.</li>
</ul>
</li>
<li><strong>S5 Boot (부팅 모드)</strong><ul>
<li>부팅 시 진입 환경 선택 (데스크톱 GUI 또는 콘솔 CLI).</li>
</ul>
</li>
<li><strong>S6 Auto Login (자동 로그인)</strong><ul>
<li>부팅 시 아이디/비번 입력 없이 자동 접속 설정.</li>
</ul>
</li>
<li><strong>S7 Splash Screen (부팅 화면)</strong><ul>
<li>부팅 시 그래픽 로고를 띄울지, 텍스트 로그를 띄울지 선택.</li>
</ul>
</li>
<li><strong>S8 Power LED (전원 LED)</strong><ul>
<li>전원 표시등(빨간불)의 켜짐/꺼짐 동작 방식 제어.</li>
</ul>
</li>
<li><strong>S9 Browser (브라우저)</strong><ul>
<li>기본으로 사용할 웹 브라우저 선택 (Chromium/Firefox 등).</li>
</ul>
</li>
</ul>
<h3 id="2-display-options-화면-설정">2. Display Options (화면 설정)</h3>
<ul>
<li><strong>D2 Screen Blanking (화면 절전)</strong><ul>
<li>일정 시간 미사용 시 화면 자동 꺼짐 설정.</li>
<li><strong>Enable:</strong> 절전 모드 켜기 (일반 사용).</li>
<li><strong>Disable:</strong> 화면 항상 켜기 (키오스크/전광판용).</li>
</ul>
</li>
<li><strong>D4 Composite (아날로그 TV 출력)</strong><ul>
<li>이어폰 잭을 통한 구형 TV(노란색 단자) 연결 기능.</li>
<li><strong>Disable:</strong> HDMI 모니터 사용 시 <strong>필수</strong> (성능 저하 방지).</li>
<li><strong>Enable:</strong> 브라운관 TV 연결 시에만 사용.</li>
</ul>
</li>
<li><strong>D6 Onscreen Keyboard (가상 키보드)</strong><ul>
<li>화면에 터치용 소프트웨어 키보드 표시.</li>
<li>키보드 없이 마우스/터치스크린만 사용할 때 활성화.</li>
</ul>
</li>
<li><strong>D7 Keyboard Output (키보드 위치)</strong><ul>
<li>듀얼 모니터 사용 시 가상 키보드를 띄울 화면 지정.</li>
<li>모니터 1개 사용 시 설정 불필요.</li>
</ul>
</li>
</ul>
<h3 id="3-interface-options-하드웨어통신">3. Interface Options (하드웨어/통신)</h3>
<ul>
<li><strong>I1 SSH (원격 터미널)</strong><ul>
<li>PC에서 명령어(CLI)로 원격 접속 허용. (필수 권장)</li>
</ul>
</li>
<li><strong>I2 RPi Connect (웹 원격 접속)</strong><ul>
<li>포트 포워딩 없이 웹 브라우저로 원격 제어하는 라즈베리 파이 공식 클라우드 서비스 활성화.</li>
</ul>
</li>
<li><strong>I3 VNC (원격 데스크톱)</strong><ul>
<li>PC에서 화면(GUI)을 보며 원격 제어 허용.</li>
</ul>
</li>
<li><strong>I4 SPI (SPI 통신)</strong><ul>
<li>고속 직렬 통신 인터페이스 활성화 (소형 LCD, 통신 모듈 등).</li>
</ul>
</li>
<li><strong>I5 I2C (I2C 통신)</strong><ul>
<li>저속 근거리 통신 인터페이스 활성화 (대부분의 센서, RTC 모듈 등).</li>
</ul>
</li>
<li><strong>I6 Serial Port (시리얼 포트)</strong><ul>
<li>UART 통신 활성화.</li>
<li>TX/RX 핀으로 데이터 통신을 하거나, 시리얼 케이블로 콘솔 로그인 시 사용.</li>
</ul>
</li>
<li><strong>I7 1-Wire (1-Wire 통신)</strong><ul>
<li>선 하나로 통신하는 저속 인터페이스 활성화 (주로 DS18B20 온도 센서용).</li>
</ul>
</li>
</ul>
<h3 id="4-performance-options-성능-제어">4. Performance Options (성능 제어)</h3>
<ul>
<li><strong>P2 Overlay File System (오버레이 파일 시스템)</strong><ul>
<li><strong>[보호 모드]</strong> 파일 시스템을 '읽기 전용'으로 전환.</li>
<li>재부팅 시 모든 변경 사항이 초기화됨 (키오스크/전광판용, SD카드 수명 연장).</li>
</ul>
</li>
<li><strong>P4 USB Current (USB 전류)</strong><ul>
<li>USB 포트로 공급하는 전력 제한을 높임.</li>
<li>외장 하드디스크(HDD/SSD) 등 전력을 많이 소모하는 장치 연결 시 활성화.</li>
</ul>
</li>
</ul>
<h3 id="5-localisation-options-지역언어">5. Localisation Options (지역/언어)</h3>
<ul>
<li><strong>L1 Locale:</strong> 언어셋 변경 (한글: <code>ko_KR.UTF-8</code>).</li>
<li><strong>L2 Timezone:</strong> 표준시 변경 (서울: Asia -&gt; Seoul).</li>
<li><strong>L3 Keyboard:</strong> 키보드 레이아웃 변경 (Generic 105 -&gt; Korean).</li>
<li><strong>L4 WLAN Country:</strong> 와이파이 국가 코드 (5GHz 사용 시 <code>KR</code> 필수).</li>
</ul>
<h3 id="6-advanced-options-고급-설정">6. Advanced Options (고급 설정)</h3>
<ul>
<li><strong>A1 Expand Filesystem (파일 시스템 확장)</strong><ul>
<li>SD카드의 남은 공간을 모두 사용할 수 있도록 파티션 크기 확장.</li>
</ul>
</li>
<li><strong>A2 Network Interface Names (네트워크 인터페이스 이름)</strong><ul>
<li>네트워크 장치명 규칙 설정.</li>
<li>활성화 시 <code>enx...</code> (고유값), 비활성화 시 <code>eth0</code> (기존 방식) 사용.</li>
</ul>
</li>
<li><strong>A3 Network Proxy Settings (프록시 설정)</strong><ul>
<li>사내망 등 인터넷 제한 환경에서 프록시 서버 주소 설정.</li>
</ul>
</li>
<li><strong>A4 Boot Order (부팅 순서)</strong><ul>
<li>부팅 우선순위 장치 변경 (SD카드, NVMe SSD, USB, 네트워크 부팅 등).</li>
</ul>
</li>
<li><strong>A5 Bootloader Version (부트로더 버전)</strong><ul>
<li>부트로더(EEPROM) 펌웨어 선택 (최신 버전 vs 공장 초기 버전).</li>
</ul>
</li>
<li><strong>A6 Beta Access (베타 접근)</strong><ul>
<li>소프트웨어 업데이트 저장소 변경 (안정적인 정식 버전 vs 테스트용 베타 버전).</li>
</ul>
</li>
<li><strong>A7 Wayland (웨일랜드 전환)</strong><ul>
<li>윈도우 그래픽 시스템 전환.</li>
<li><strong>Wayland:</strong> 신형 (기본값, 성능 우수).</li>
<li><strong>X11:</strong> 구형 (원격 제어 등 호환성 필요시 사용).</li>
</ul>
</li>
<li><strong>A8 PCIe Speed (PCIe 속도)</strong><ul>
<li><strong>[RPi 5 전용]</strong> PCIe 포트 대역폭 설정.</li>
<li><strong>Gen 2:</strong> 기본값 (안정적).</li>
<li><strong>Gen 3:</strong> 2배 빠름 (NVMe SSD 사용 시 권장).</li>
</ul>
</li>
<li><strong>A9 Network Install UI (네트워크 설치 화면)</strong><ul>
<li>부팅 장치가 없을 때 나타나는 '네트워크 OS 설치' 화면 표시 여부 설정.</li>
</ul>
</li>
<li><strong>A10 Libliftoff (하드웨어 오버레이)</strong><ul>
<li>그래픽 처리를 돕는 KMS 평면 할당 라이브러리 활성화 (그래픽 성능 최적화).</li>
</ul>
</li>
<li><strong>A11 Shutdown Behaviour (종료 동작)</strong><ul>
<li>시스템 종료(Shutdown) 시 전원 상태 설정 (전력 소모 최소화 모드 등).</li>
</ul>
</li>
</ul>
<h3 id="8-update">8. Update</h3>
<ul>
<li><strong>Update:</strong> <code>raspi-config</code> 툴 자체 업데이트.</li>
</ul>
<h3 id="9-about-raspi-config">9. About raspi-config</h3>
<pre><code class="language-c">This tool provides a straightforward way of doing initial
configuration of the Raspberry Pi. Although it can be run   
at any time, some of the options may have difficulties if 
you have heavily customised your installation.

Version: 20251202</code></pre>