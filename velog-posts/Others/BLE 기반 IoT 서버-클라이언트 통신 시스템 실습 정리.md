<h1 id="bluetooth-iot-서버-클라이언트-통신-시스템-실습-정리">BLUETOOTH) IoT 서버-클라이언트 통신 시스템 실습 정리</h1>
<blockquote>
<p>WiFi 모듈 대신 HC-06 블루투스 모듈로 교체 — 동일한 iot_server/iot_client 구조를 재사용하면서 블루투스 브릿지 클라이언트를 추가한 실습</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2d3173a5-7cc8-4dae-bcac-15f8fb07510f/image.gif" /></p>
<h2 id="목차">목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-%EC%8B%A4%EC%8A%B5-%EA%B0%9C%EC%9A%94-%EB%B0%8F-3%EB%8B%A8%EA%B3%84-%ED%9D%90%EB%A6%84">실습 개요 및 3단계 흐름</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-hc-06-%EB%B8%94%EB%A3%A8%ED%88%AC%EC%8A%A4-%EB%AA%A8%EB%93%88-%ED%8A%B9%EC%A7%95">HC-06 블루투스 모듈 특징</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-1%EB%8B%A8%EA%B3%84-arduino--rpi--%EC%84%9C%EB%B2%84-%EC%97%B0%EB%8F%99">1단계: Arduino + RPi + 서버 연동</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-2%EB%8B%A8%EA%B3%84-%EA%B0%80%EB%B3%80%EC%A0%80%ED%95%AD%EC%9C%BC%EB%A1%9C-%EC%A7%9D%EA%BF%8D-%EB%AA%A8%ED%84%B0-%EC%A0%9C%EC%96%B4">2단계: 가변저항으로 짝꿍 모터 제어</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-3%EB%8B%A8%EA%B3%84-stm32--bt--dht11-%EC%A7%81%EB%A0%AC-%EC%B6%9C%EB%A0%A5">3단계: STM32 + BT + DHT11 직렬 출력</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-iot_client_bluetoothc-%EB%B6%84%EC%84%9D">iot_client_bluetooth.c 분석</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-arduino-%EC%BD%94%EB%93%9C-%EB%B6%84%EC%84%9D">Arduino 코드 분석</a></li>
<li><a href="https://api.velog.io/rss/@mommers#8-%EB%B9%8C%EB%93%9C-%EB%B0%8F-%EC%8B%A4%ED%96%89">빌드 및 실행</a></li>
</ol>
<hr />
<h2 id="1-실습-개요-및-3단계-흐름">1. 실습 개요 및 3단계 흐름</h2>
<p>WiFi 세션과 달리 Arduino에 HC-06 블루투스 모듈을 달고, Raspberry Pi가 RFCOMM으로 HC-06에 접속한다. RPi에서 실행하는 <code>iot_client_bluetooth</code>가 <strong>BT ↔ TCP 브릿지</strong> 역할을 하면서 기존 서버 구조를 그대로 재활용한다.</p>
<pre><code>[Arduino Uno + HC-06]                [Ubuntu Linux]
  SoftwareSerial(10,11) ↔ HC-06        iot_server (port 5000)
  DHT11, CDS, MOTOR, LED                    ▲
  버튼, 가변저항, I2C LCD                    │ TCP
        │                                   │
        │ RFCOMM (Bluetooth)    [Raspberry Pi]
        └──────────────────→  iot_client_bluetooth
                                  (BT ↔ TCP 브릿지)</code></pre><h3 id="3단계-진행-순서">3단계 진행 순서</h3>
<table>
<thead>
<tr>
<th>단계</th>
<th>구성</th>
<th>핵심 내용</th>
</tr>
</thead>
<tbody><tr>
<td>1단계</td>
<td>Arduino + RPi + Ubuntu 서버</td>
<td>HC-06 ↔ RPi RFCOMM ↔ TCP 서버 연동, LED/LAMP/센서 제어</td>
</tr>
<tr>
<td>2단계</td>
<td>본인 + 짝꿍 아두이노 연동</td>
<td>내 가변저항 → 짝꿍 모터 제어, 서버 ID 통합</td>
</tr>
<tr>
<td>3단계</td>
<td>Arduino + STM32F411RE + RPi</td>
<td>BT를 STM32에 연결, Arduino → STM32 시리얼로 DHT11 데이터 전달</td>
</tr>
</tbody></table>
<hr />
<h2 id="2-hc-06-블루투스-모듈-특징">2. HC-06 블루투스 모듈 특징</h2>
<ul>
<li><strong>근거리 통신</strong> (약 10m 내외)</li>
<li>WiFi 대비 소비전력이 낮고, 노이즈에 강한 편</li>
<li>Arduino에는 하드웨어 시리얼이 하나뿐 → SoftwareSerial로 연결<ul>
<li>디버깅(Serial 모니터)과 BT 통신을 동시에 쓸 수 없음</li>
<li>업로드 중에는 BT 모듈을 분리해야 함</li>
</ul>
</li>
<li>통신 속도: 실습에서 9600 bps 사용 (38400이 SoftwareSerial 최대치지만 HC-06 기본값이 9600)</li>
<li>접속 방식: <code>RFCOMM</code> 프로토콜 (Bluetooth SPP — Serial Port Profile)</li>
</ul>
<h3 id="hc-06-핀-연결-arduino">HC-06 핀 연결 (Arduino)</h3>
<table>
<thead>
<tr>
<th>HC-06 핀</th>
<th>Arduino 핀</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td>TXD</td>
<td>D10 (SoftSerial RX)</td>
<td>HC-06 송신 → Arduino 수신</td>
</tr>
<tr>
<td>RXD</td>
<td>D11 (SoftSerial TX)</td>
<td>Arduino 송신 → HC-06 수신</td>
</tr>
<tr>
<td>VCC</td>
<td>5V</td>
<td></td>
</tr>
<tr>
<td>GND</td>
<td>GND</td>
<td></td>
</tr>
</tbody></table>
<pre><code class="language-c">SoftwareSerial BTSerial(10, 11); // RX=10, TX=11
BTSerial.begin(9600);</code></pre>
<hr />
<h2 id="3-1단계-arduino--rpi--서버-연동">3. 1단계: Arduino + RPi + 서버 연동</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a7648f54-73c7-4097-8e29-062cc4c41499/image.jpg" /></p>
<h3 id="전체-데이터-흐름">전체 데이터 흐름</h3>
<pre><code>Linux 클라이언트 터미널
  → [KYM_ARD]LAMP@ON 입력
  → iot_server 가 KYM_ARD 로 라우팅
  → iot_client_bluetooth 의 recv_msg 수신
  → btfd 로 write → HC-06 → Arduino
  → bluetoothEvent() 에서 LAMP@ON 처리
  → LED 켜짐 + [KYM_SQL]SETDB@LAMP@ON@KYM_LIN BT로 송신
  → iot_client_bluetooth 의 send_msg 수신
  → sockfd 로 write → 서버 → KYM_SQL 클라이언트 → DB 업데이트</code></pre><h3 id="rpi에서-블루투스-연결">RPi에서 블루투스 연결</h3>
<pre><code class="language-bash"># libbluetooth 설치
sudo apt-get install libbluetooth-dev

# HC-06 MAC 주소 확인 (스캔)
hcitool scan

# 페어링 (HC-06 기본 PIN: 1234)
bluetoothctl
  &gt; pair 98:DA:60:09:9B:BC
  &gt; trust 98:DA:60:09:9B:BC</code></pre>
<p><code>iot_client_bluetooth.c</code> 내부에 HC-06 MAC 주소가 하드코딩되어 있다.</p>
<pre><code class="language-c">char dest[18] = &quot;98:DA:60:09:9B:BC&quot;;  // HC-06 MAC</code></pre>
<pre><code>pi@pi00:~$ hcitool scan
Scanning ...
    98:DA:60:09:9B:C8       iot10
        74:42:18:A7:91:02       n/a
        98:DA:60:09:6E:F4       iot07
        98:DA:60:02:B8:F7       iot01
        98:DA:60:08:1C:0F       iot12
        98:DA:60:0D:AE:D4       iot06.
        98:DA:60:07:9F:17       iot08
        98:DA:60:09:9B:BC       iot22
        98:DA:60:08:0C:D9       iot13
        98:DA:60:02:85:43       iot18
        98:DA:60:07:D5:29       iot11
        98:DA:60:09:E5:62       iot03
        98:DA:60:07:F6:5B       iot14
        98:DA:60:0B:32:A6       iot02
        98:DA:60:02:B7:30       iot16
        98:DA:60:02:B6:AE       iot04
        98:DA:60:0D:A1:AC       iot00
        98:D3:31:FB:B1:B1       n/a

pi@pi00:~$ bluetoothctl
Agent registered
[bluetoothctl]&gt; 
[bluetoothctl]&gt; help        
[bluetoothctl]&gt; default-agent
[bluetoothctl]&gt; scan on

[bluetoothctl]&gt; pair 98:DA:60:0D:A1:AC        
Attempting to pair with 98:DA:60:0D:A1:AC
[CHG] Device 98:DA:60:0D:A1:AC Connected: yes
Request PIN code
[agent] Enter PIN code: 1234
Pairing successful

[bluetoothctl]&gt;scan off
Discovery stopped

[bluetoothctl]&gt; devices Paired
Device 98:DA:60:0D:A1:AC iot00

[bluetoothctl]&gt;exit

pi@pi00:~$</code></pre><h3 id="실행">실행</h3>
<pre><code class="language-bash">./iot_client_bluetooth 10.10.16.35 5000 KYM_ARD</code></pre>
<hr />
<h2 id="4-2단계-가변저항으로-짝꿍-모터-제어">4. 2단계: 가변저항으로 짝꿍 모터 제어</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/de6f641f-704c-46b9-b2ba-59d9a3609932/image.gif" /></p>
<h3 id="개요">개요</h3>
<ul>
<li>내 빵판의 가변저항(A1) 값을 읽어 짝꿍의 Arduino 모터로 전송</li>
<li>서버에 짝꿍 ID를 추가하고, 두 아두이노 코드를 수정해서 ID를 구분</li>
</ul>
<h3 id="가변저항-→-모터-전송-arduino-코드">가변저항 → 모터 전송 (Arduino 코드)</h3>
<pre><code class="language-c">// A1 가변저항 읽기 → 0~100으로 정규화
varValue = analogRead(A1);
varValue = map(varValue, 0, 1023, 0, 100);

// 3 이상 변화 시에만 전송 (노이즈 제거)
if (abs(varValue - varValueold) &gt; 3) {
    varValueold = varValue;
    sprintf(sendBuf, &quot;[%s]MOTOR@%d\n&quot;, &quot;KYM_ARD&quot;, varValue);
    // &quot;KYM_ARD&quot; 자리에 짝꿍 ID 입력
    BTSerial.write(sendBuf);
}</code></pre>
<p>서버에서는 <code>[짝꿍_ID]MOTOR@{값}</code> 형태로 라우팅되어 짝꿍의 BT 클라이언트를 거쳐 Arduino PWM 핀으로 전달된다.</p>
<pre><code class="language-c">// 수신 측 Arduino
else if (!strcmp(pArray[1], &quot;MOTOR&quot;)) {
    int speed = atoi(pArray[2]);
    speed = map(speed, 0, 100, 0, 255);  // 0~100 → 0~255 (PWM)
    analogWrite(MOTOR_PIN, speed);
}</code></pre>
<hr />
<h2 id="5-3단계-stm32--bt--dht11-직렬-출력">5. 3단계: STM32 + BT + DHT11 직렬 출력</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c9e97511-438f-43ff-a27d-6c0bfcabcccb/image.jpg" /></p>
<h3 id="구성-변경">구성 변경</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>변경 전 (1단계)</th>
<th>변경 후 (3단계)</th>
</tr>
</thead>
<tbody><tr>
<td>BT 모듈 연결 대상</td>
<td>Arduino Uno</td>
<td>STM32F411RE Nucleo</td>
</tr>
<tr>
<td>RPi 블루투스 접속</td>
<td>Arduino HC-06</td>
<td>STM32 HC-06</td>
</tr>
<tr>
<td>DHT11 데이터 목적지</td>
<td>DB 저장</td>
<td>STM32 시리얼 모니터로 출력</td>
</tr>
</tbody></table>
<h3 id="흐름">흐름</h3>
<pre><code>Arduino (DHT11 측정)
  → SENSOR 메시지를 BT로 전송
  → iot_client_bluetooth 가 서버로 중계
  → [STM32_ID] 로 라우팅
  → STM32의 UART → 시리얼 모니터에 온습도 값 출력

동시에)
RPi → 서버 → Arduino 로 LED 제어 명령 전달 가능</code></pre><p>STM32 측은 UART로 수신한 메시지를 시리얼 모니터(<code>printf</code> 또는 <code>HAL_UART_Transmit</code>)로 그대로 출력하는 구조.</p>
<h3 id="결과시리얼">결과(시리얼)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/35994417-0cfa-48ae-a45f-387f4bf24d54/image.png" /></p>
<hr />
<h2 id="6-iot_client_bluetoothc-분석">6. iot_client_bluetooth.c 분석</h2>
<blockquote>
<p>📁 참고: WiFi 세션의 <code>iot_client.c</code> 구조를 기반으로, Bluetooth fd를 추가한 버전</p>
</blockquote>
<h3 id="핵심-자료구조">핵심 자료구조</h3>
<pre><code class="language-c">typedef struct {
    int sockfd;           // TCP 서버 소켓 fd
    int btfd;             // Bluetooth RFCOMM 소켓 fd
    char sendid[NAME_SIZE];
} DEV_FD;</code></pre>
<p>두 개의 fd를 묶어서 스레드에 전달한다.</p>
<h3 id="bluetooth-rfcomm-소켓-연결">Bluetooth RFCOMM 소켓 연결</h3>
<pre><code class="language-c">dev_fd.btfd = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);

struct sockaddr_rc addr = { 0 };
addr.rc_family  = AF_BLUETOOTH;
addr.rc_channel = (uint8_t)1;         // RFCOMM 채널 1
str2ba(dest, &amp;addr.rc_bdaddr);        // MAC 문자열 → bt_addr 변환

connect(dev_fd.btfd, (struct sockaddr *)&amp;addr, sizeof(addr));</code></pre>
<h3 id="send_msg-스레드-bt-→-서버">send_msg 스레드 (BT → 서버)</h3>
<p><code>select()</code> 로 <code>btfd</code>를 감시하다가 Arduino에서 데이터가 오면 TCP 서버로 relay.</p>
<pre><code class="language-c">// btfd 와 sockfd 모두 select 감시
FD_SET(dev_fd-&gt;sockfd, &amp;initset);
FD_SET(dev_fd-&gt;btfd, &amp;initset);

// btfd에 데이터가 오면
if (FD_ISSET(dev_fd-&gt;btfd, &amp;newset)) {
    ret = read(dev_fd-&gt;btfd, msg + total, BUF_SIZE - total);
    total += ret;

    if (msg[total - 1] == '\n') {   // '\n' 확인 후 완성된 메시지 전송
        msg[total] = 0;
        total = 0;
    } else
        continue;                   // 아직 미완성이면 더 읽기

    write(dev_fd-&gt;sockfd, msg, strlen(msg));  // 서버로 전달
}</code></pre>
<blockquote>
<p><strong>포인트:</strong> <code>'\n'</code>이 올 때까지 부분 수신을 누적한다. Bluetooth는 TCP처럼 스트림이라 한 번에 전체가 안 올 수도 있기 때문.</p>
</blockquote>
<h3 id="recv_msg-스레드-서버-→-bt">recv_msg 스레드 (서버 → BT)</h3>
<p>서버에서 오는 메시지를 그대로 btfd로 write → HC-06 → Arduino.</p>
<pre><code class="language-c">str_len = read(dev_fd-&gt;sockfd, name_msg, NAME_SIZE + BUF_SIZE);
write(dev_fd-&gt;btfd, name_msg, strlen(name_msg));</code></pre>
<hr />
<h2 id="7-arduino-코드-분석">7. Arduino 코드 분석</h2>
<h3 id="하드웨어-핀맵">하드웨어 핀맵</h3>
<table>
<thead>
<tr>
<th>핀</th>
<th>연결</th>
</tr>
</thead>
<tbody><tr>
<td>A0</td>
<td>CDS 조도 센서</td>
</tr>
<tr>
<td>A1</td>
<td>가변저항 (2단계 짝꿍 모터 제어용)</td>
</tr>
<tr>
<td>D2</td>
<td>버튼 (GAS ON/OFF 이벤트)</td>
</tr>
<tr>
<td>D4</td>
<td>DHT11 Signal</td>
</tr>
<tr>
<td>D6</td>
<td>DC Motor (PWM)</td>
</tr>
<tr>
<td>D10</td>
<td>SoftwareSerial RX (← HC-06 TX)</td>
</tr>
<tr>
<td>D11</td>
<td>SoftwareSerial TX (→ HC-06 RX)</td>
</tr>
<tr>
<td>D13</td>
<td>LED (내장)</td>
</tr>
<tr>
<td>I2C</td>
<td>LCD (0x27, 16x2)</td>
</tr>
</tbody></table>
<h3 id="사용-라이브러리">사용 라이브러리</h3>
<ul>
<li><code>SoftwareSerial</code> — HC-06 UART 통신</li>
<li><code>DHT</code> — DHT11 온습도</li>
<li><code>MsTimer2</code> — 1초 타이머 인터럽트</li>
<li><code>LiquidCrystal_I2C</code> — I2C LCD 제어</li>
</ul>
<h3 id="타이머-기반-비블로킹-구조">타이머 기반 비블로킹 구조</h3>
<p>WiFi 버전과 동일하게 <code>delay()</code> 없이 타이머 인터럽트 + 플래그로 처리한다.</p>
<pre><code class="language-c">void timerIsr() {
    timerIsrFlag = true;
    secCount++;
}

void loop() {
    if (BTSerial.available())
        bluetoothEvent();      // BT 수신 즉시 처리

    // 가변저항 변화 감지 (폴링)
    varValue = map(analogRead(A1), 0, 1023, 0, 100);
    if (abs(varValue - varValueold) &gt; 3) { ... }

    if (timerIsrFlag) {        // 1초마다
        timerIsrFlag = false;
        // 센서 읽기, LCD 업데이트, SENSOR 전송, CDS 이벤트 감지
    }

    // 버튼 디바운싱 처리
    currentButton = debounce(lastButton);
    if (lastButton == HIGH &amp;&amp; currentButton == LOW) {
        // 버튼 눌림 → GAS 이벤트 전송
    }
}</code></pre>
<h3 id="bluetoothevent-처리-커맨드">bluetoothEvent() 처리 커맨드</h3>
<table>
<thead>
<tr>
<th>수신 커맨드</th>
<th>동작</th>
<th>응답</th>
</tr>
</thead>
<tbody><tr>
<td><code>LAMP@ON/OFF</code></td>
<td>LED_BUILTIN 제어</td>
<td><code>[KYM_SQL]SETDB@LAMP@ON/OFF@{발신ID}</code></td>
</tr>
<tr>
<td><code>MOTOR@{0~100}</code></td>
<td><code>map → PWM</code> 출력</td>
<td>(없음, 즉시 return)</td>
</tr>
<tr>
<td><code>GETSENSOR@{N}</code></td>
<td>N초 주기 센서 전송 설정</td>
<td>현재 센서값 1회 즉시 응답</td>
</tr>
<tr>
<td><code>New…</code> / <code>Alr…</code></td>
<td>서버 접속 알림</td>
<td>return (무시)</td>
</tr>
</tbody></table>
<h3 id="cds-이벤트-감지">CDS 이벤트 감지</h3>
<p>임계값 50을 기준으로 <strong>상태가 바뀔 때만</strong> 1회 전송 (매 초 전송 X).</p>
<pre><code class="language-c">if ((cds &gt;= 50) &amp;&amp; cdsFlag) {       // 밝아졌을 때
    cdsFlag = false;
    sprintf(sendBuf, &quot;[%s]CDS@%d\n&quot;, recvId, cds);
    BTSerial.write(sendBuf, strlen(sendBuf));
}
else if ((cds &lt; 50) &amp;&amp; !cdsFlag) {  // 어두워졌을 때
    cdsFlag = true;
    sprintf(sendBuf, &quot;[%s]CDS@%d\n&quot;, recvId, cds);
    BTSerial.write(sendBuf, strlen(sendBuf));
}</code></pre>
<h3 id="버튼-디바운싱">버튼 디바운싱</h3>
<pre><code class="language-c">boolean debounce(boolean last) {
    boolean current = digitalRead(BUTTON_PIN);
    if (last != current) {
        delay(5);                         // 5ms 대기 후 재확인
        current = digitalRead(BUTTON_PIN);
    }
    return current;
}</code></pre>
<hr />
<h2 id="8-빌드-및-실행">8. 빌드 및 실행</h2>
<h3 id="rpi에서-빌드">RPi에서 빌드</h3>
<pre><code class="language-bash"># libbluetooth 설치 (최초 1회)
sudo apt-get install libbluetooth-dev

# 빌드
gcc iot_client_bluetooth.c -o iot_client_bluetooth -lbluetooth -pthread</code></pre>
<h3 id="실행-1">실행</h3>
<pre><code class="language-bash"># 서버 실행 (Ubuntu)
./iot_server 5000

# BT 브릿지 클라이언트 실행 (Raspberry Pi)
./iot_client_bluetooth 10.10.16.35 5000 KYM_ARD

# 제어용 콘솔 클라이언트 (Ubuntu 또는 RPi)
./iot_client 10.10.16.35 5000 KYM_LIN</code></pre>
<h3 id="제어-명령-예시">제어 명령 예시</h3>
<pre><code>[KYM_ARD]LAMP@ON         → Arduino LED 켜기
[KYM_ARD]LAMP@OFF        → Arduino LED 끄기
[KYM_ARD]GETSENSOR@5     → 5초마다 센서 데이터 전송 요청
[KYM_ARD]MOTOR@70        → 모터 70% 출력</code></pre><hr />
<h2 id="wifi-세션과의-비교">WiFi 세션과의 비교</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>WiFi (ESP8266)</th>
<th>Bluetooth (HC-06)</th>
</tr>
</thead>
<tbody><tr>
<td>통신 거리</td>
<td>~수십 m</td>
<td>~10 m</td>
</tr>
<tr>
<td>소비전력</td>
<td>높음</td>
<td>낮음</td>
</tr>
<tr>
<td>노이즈 내성</td>
<td>보통</td>
<td>강한 편</td>
</tr>
<tr>
<td>Arduino 연결</td>
<td>SoftwareSerial (D6/D7)</td>
<td>SoftwareSerial (D10/D11)</td>
</tr>
<tr>
<td>RPi 역할</td>
<td>클라이언트 (직접 TCP)</td>
<td>BT↔TCP 브릿지</td>
</tr>
<tr>
<td>서버 변경 여부</td>
<td>없음 (ID만 추가)</td>
<td>없음 (ID만 추가)</td>
</tr>
<tr>
<td>브릿지 클라이언트</td>
<td>불필요</td>
<td><code>iot_client_bluetooth.c</code> 필요</td>
</tr>
<tr>
<td>인증 포맷</td>
<td><code>[ID:PASSWD]</code></td>
<td>동일</td>
</tr>
</tbody></table>
<blockquote>
<p><strong>핵심 포인트:</strong> iot_server 코드는 전혀 바뀌지 않는다. 통신 방식이 바뀌어도 <code>[ID]커맨드@파라미터</code> 프로토콜과 서버 라우팅 구조는 그대로 재사용된다.</p>
</blockquote>