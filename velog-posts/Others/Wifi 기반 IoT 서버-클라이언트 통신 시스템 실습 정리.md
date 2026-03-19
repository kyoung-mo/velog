<p> 이번에는 멀티 쓰레딩 기반으로 Ubuntu + Arduino + RaspberryPi5 를 이용해 IOT 실습을 진행했습니다. intel 국비지원 과정에서 교수님의 소스 코드를 수정해서 진행했습니다.</p>
<hr />
<h1 id="wifi-iot-서버-클라이언트-통신-시스템-실습-정리">Wifi) IoT 서버-클라이언트 통신 시스템 실습 정리</h1>
<blockquote>
<p>Arduino + ESP8266 + Linux TCP Server + MariaDB + PHP 웹 시각화까지 연결하는 IoT 풀스택 실습</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6fcba6a5-270c-41ae-b1a8-244e0d16c529/image.gif" /></p>
<h2 id="목차">목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B0%9C%EC%9A%94">프로젝트 개요</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-%EC%A0%84%EC%B2%B4-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98">전체 아키텍처</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-%ED%86%B5%EC%8B%A0-%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C">통신 프로토콜</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-iot-%EC%84%9C%EB%B2%84-iot_serverc">IoT 서버 (iot_server.c)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-linux-%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8">Linux 클라이언트</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-arduino--esp8266-wifi-%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8">Arduino + ESP8266 (WiFi 클라이언트)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-mariadb-%EA%B5%AC%EC%84%B1-raspberry-pi">MariaDB 구성 (Raspberry Pi)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#8-%EC%9B%B9-%EC%8B%9C%EA%B0%81%ED%99%94-apache2--php">웹 시각화 (Apache2 + PHP)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#9-github-%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C">GitHub 소스코드</a></li>
</ol>
<hr />
<h2 id="1-프로젝트-개요">1. 프로젝트 개요</h2>
<p>Arduino Uno에 ESP8266 WiFi 모듈을 붙여 Linux TCP 서버에 접속하고, 온습도(DHT11) · 조도(CDS) 센서 데이터를 MariaDB에 저장한 뒤 PHP + Google Charts로 웹 시각화하는 IoT 시스템이다.</p>
<p>디바이스 제어(LED · LAMP · MOTOR) 역시 서버를 통해 양방향으로 가능하다.</p>
<hr />
<h2 id="2-전체-아키텍처">2. 전체 아키텍처</h2>
<pre><code>[Arduino Uno + ESP8266]
  DHT11(온습도), CDS(조도)
  LED, LAMP, MOTOR 제어
        │
        │ WiFi TCP (port 5000)
        ▼
[Ubuntu Linux - iot_server.c]   ← 멀티스레드 TCP 서버, ID/PW 인증, 메시지 라우팅
        │
        │ TCP (같은 서버에 클라이언트로 접속)
        ▼
[iot_client_sensor_device.c]    ← SENSOR 수신 → MariaDB INSERT
        │                          GETDB/SETDB → device 테이블 읽기/쓰기
        ▼
[Raspberry Pi - MariaDB (iotdb)]
        │
        ▼
[Apache2 + PHP]
  sensorTable.php  → DB 조회 결과를 HTML 테이블로 출력
  sensorGraph.php  → Google Charts 라인 그래프
  index.html       → 두 페이지를 frameset으로 분할 출력</code></pre><hr />
<h2 id="3-통신-프로토콜">3. 통신 프로토콜</h2>
<p>서버와 클라이언트 간 메시지는 아래 포맷을 공유한다.</p>
<pre><code>[수신ID]커맨드@파라미터1@파라미터2\n</code></pre><h3 id="주요-커맨드-예시">주요 커맨드 예시</h3>
<table>
<thead>
<tr>
<th>방향</th>
<th>예시 메시지</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>서버 → Arduino</td>
<td><code>[KYM_ARD]LED@ON</code></td>
<td>LED 켜기</td>
</tr>
<tr>
<td>서버 → Arduino</td>
<td><code>[KYM_ARD]LAMP@OFF</code></td>
<td>LAMP 끄기</td>
</tr>
<tr>
<td>서버 → Arduino</td>
<td><code>[KYM_ARD]MOTOR@50</code></td>
<td>모터 50% 출력</td>
</tr>
<tr>
<td>서버 → Arduino</td>
<td><code>[KYM_ARD]GETSENSOR@10</code></td>
<td>10초마다 센서 전송 요청</td>
</tr>
<tr>
<td>Arduino → 서버</td>
<td><code>[KYM_SQL]SENSOR@88@22.4@6.0</code></td>
<td>조도@온도@습도 전송</td>
</tr>
<tr>
<td>클라이언트 → 서버</td>
<td><code>[KYM_ARD]GETSTATE@DEV</code></td>
<td>현재 LED/LAMP 상태 요청</td>
</tr>
<tr>
<td>SQL클라이언트 → 서버</td>
<td><code>[KYM_ARD]SETDB@LAMP@ON@KYM_LIN</code></td>
<td>DB device 테이블 업데이트 후 전달</td>
</tr>
</tbody></table>
<h3 id="strtok-파싱-구조">strtok 파싱 구조</h3>
<p>수신된 메시지는 <code>[</code>, <code>]</code>, <code>@</code>, <code>:</code> 을 구분자로 <code>strtok</code>으로 파싱한다.</p>
<pre><code class="language-c">// 예: &quot;[KYM_ARD]LED@ON\n&quot;
// pArray[0] = &quot;KYM_ARD&quot;
// pArray[1] = &quot;LED&quot;
// pArray[2] = &quot;ON&quot;

pToken = strtok(recvBuf, &quot;[@]&quot;);
while (pToken != NULL) {
    pArray[i++] = pToken;
    pToken = strtok(NULL, &quot;[@]&quot;);
}</code></pre>
<hr />
<h2 id="4-iot-서버-iot_serverc">4. IoT 서버 (iot_server.c)</h2>
<blockquote>
<p>📁 <a href="https://github.com/kyoung-mo/linuxC/tree/main/iot_socket.d">iot_socket.d</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/99200af4-32c6-434a-a50d-34e52a6ba4f2/image.png" /></p>
<h3 id="주요-특징">주요 특징</h3>
<ul>
<li>최대 32개 클라이언트 동시 접속 (pthread 기반)</li>
<li>접속 시 ID/PW 인증 → 통과 시 전용 스레드 생성</li>
<li>메시지 라우팅: <code>ALLMSG</code>(전체 브로드캐스트) / <code>IDLIST</code>(접속자 목록) / 특정 ID(1:1 전달)</li>
<li><code>SO_REUSEADDR</code> 설정으로 서버 재시작 시 포트 즉시 재사용</li>
</ul>
<h3 id="등록된-클라이언트-id-일부">등록된 클라이언트 ID (일부)</h3>
<pre><code class="language-c">// 서버 코드 내 고정 등록
{0,-1,&quot;&quot;,&quot;KYM_STM&quot;,&quot;PASSWD&quot;},  // STM32 보드
{0,-1,&quot;&quot;,&quot;KYM_LDP&quot;,&quot;PASSWD&quot;},  // 랩탑
{0,-1,&quot;&quot;,&quot;KYM_LIN&quot;,&quot;PASSWD&quot;},  // Linux 클라이언트
{0,-1,&quot;&quot;,&quot;KYM_ARD&quot;,&quot;PASSWD&quot;},  // Arduino
{0,-1,&quot;&quot;,&quot;KYM_SQL&quot;,&quot;PASSWD&quot;},  // DB 클라이언트</code></pre>
<h3 id="실행-방법">실행 방법</h3>
<pre><code class="language-bash">gcc -o iot_server iot_server.c -lpthread
./iot_server 5000</code></pre>
<h3 id="메시지-라우팅-흐름">메시지 라우팅 흐름</h3>
<pre><code>클라이언트 A가 &quot;[KYM_ARD]LED@ON\n&quot; 전송
    → 서버가 수신 후 to = &quot;KYM_ARD&quot; 파싱
    → client_info 배열에서 id == &quot;KYM_ARD&quot; 찾아서 write()
    → Arduino 수신 후 LED ON 처리</code></pre><hr />
<h2 id="5-linux-클라이언트">5. Linux 클라이언트</h2>
<h3 id="5-1-iot_clientc-기본-콘솔-클라이언트">5-1. iot_client.c (기본 콘솔 클라이언트)</h3>
<blockquote>
<p>📁 <a href="https://github.com/kyoung-mo/linuxC/tree/main/iot_socket.d">iot_socket.d</a></p>
</blockquote>
<p>터미널에서 직접 메시지를 입력해 다른 클라이언트로 전송하거나 서버를 테스트하는 용도.</p>
<ul>
<li><code>send_msg</code> / <code>recv_msg</code> 스레드로 분리</li>
<li><code>select()</code> 를 사용해 stdin을 <strong>비블로킹</strong>으로 처리 (1초 타임아웃)</li>
<li><code>quit</code> 입력 시 종료</li>
</ul>
<pre><code class="language-bash">gcc -o iot_client iot_client.c -lpthread
./iot_client 10.10.16.35 5000 KYM_LIN</code></pre>
<h3 id="5-2-iot_client_sensor_devicec-db-연동-클라이언트">5-2. iot_client_sensor_device.c (DB 연동 클라이언트)</h3>
<blockquote>
<p>📁 <a href="https://github.com/kyoung-mo/linuxC/tree/main/sql_client">sql_client</a></p>
</blockquote>
<p>Arduino에서 전송된 센서 데이터를 받아 MariaDB에 자동 저장하고, <code>device</code> 테이블 읽기/쓰기를 처리하는 클라이언트.</p>
<pre><code class="language-bash"># 빌드 (Raspberry Pi 환경)
make

# 실행
./iot_client_sql 127.0.0.1 5000 KYM_SQL</code></pre>
<h4 id="sensor-수신-→-db-insert">SENSOR 수신 → DB INSERT</h4>
<pre><code class="language-c">// 수신: &quot;[KYM_ARD]SENSOR@88@22.4@6.0&quot;
if (!strcmp(pArray[1], &quot;SENSOR&quot;) &amp;&amp; (i == 5)) {
    illu = atoi(pArray[2]);
    temp = atof(pArray[3]);
    humi = atof(pArray[4]);
    sprintf(sql_cmd,
        &quot;insert into sensor(name,date,time,illu,temp,humi) &quot;
        &quot;values('%s',now(),now(),%d,%f,%f)&quot;,
        pArray[0], illu, temp, humi);
    mysql_query(conn, sql_cmd);
}</code></pre>
<h4 id="setdb-→-device-테이블-업데이트">SETDB → device 테이블 업데이트</h4>
<pre><code class="language-c">// 수신: &quot;[KYM_SQL]SETDB@LAMP@ON@KYM_LIN&quot;
// → device 테이블에서 LAMP 값을 ON으로 update
// → &quot;[KYM_LIN]LAMP@ON\n&quot; 을 해당 클라이언트로 전달
sprintf(sql_cmd,
    &quot;update device set value='%s', date=now(), time=now() where name='%s'&quot;,
    pArray[3], pArray[2]);</code></pre>
<hr />
<h2 id="6-arduino--esp8266-wifi-클라이언트">6. Arduino + ESP8266 (WiFi 클라이언트)</h2>
<blockquote>
<p>📁 <a href="https://github.com/kyoung-mo/linuxC/tree/main/Arduino">Arduino</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/afd66b12-98f7-4e01-b3a5-bf5a790beb25/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f4578e7a-ec22-4026-b35b-fdda9b0e6bc9/image.png" /></p>
<h3 id="하드웨어-구성">하드웨어 구성</h3>
<table>
<thead>
<tr>
<th>핀</th>
<th>연결</th>
</tr>
</thead>
<tbody><tr>
<td>D4</td>
<td>DHT11 Signal</td>
</tr>
<tr>
<td>D6</td>
<td>SoftwareSerial RX (← ESP8266 TX)</td>
</tr>
<tr>
<td>D7</td>
<td>SoftwareSerial TX (→ ESP8266 RX)</td>
</tr>
<tr>
<td>D11</td>
<td>DC Motor (PWM)</td>
</tr>
<tr>
<td>D12</td>
<td>LAMP (LED)</td>
</tr>
<tr>
<td>D13</td>
<td>LED (내장)</td>
</tr>
<tr>
<td>A0</td>
<td>CDS 조도센서</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/67872e73-f919-4455-9618-4c2f1bc0a8eb/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c6d41633-181e-42df-a6b7-fc06ddea775f/image.png" /></p>
<h3 id="사용-라이브러리">사용 라이브러리</h3>
<ul>
<li><code>WiFiEsp</code> 2.2.2 — ESP8266 WiFi 통신</li>
<li><code>SoftwareSerial</code> — D6/D7 소프트웨어 UART</li>
<li><code>TimerOne</code> — 1초 하드웨어 타이머 인터럽트</li>
<li><code>DHT</code> (KXN) — DHT11 온습도 센서</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fa841e1c-b047-4b37-a6d0-55384c877611/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0d757ff2-61f5-4eec-a374-2ec2fec7e745/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/21b7b0da-0b51-4ab3-9087-ec8be309df17/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e848da3e-3523-4c90-9df8-c4642a6f7503/image.png" /></p>
<h3 id="핵심-동작-구조">핵심 동작 구조</h3>
<pre><code class="language-c">void loop() {
    if (client.available())   // 서버에서 데이터 오면
        socketEvent();         // 명령 파싱 및 처리

    if (timerIsrFlag) {        // 1초마다
        timerIsrFlag = false;
        if (!(secCount % 5)) { // 5초마다
            // 서버 연결 확인 + 센서값 읽기
        }
        if (sensorTime != 0 &amp;&amp; !(secCount % sensorTime)) {
            // GETSENSOR로 설정된 주기마다 센서 데이터 전송
        }
    }
}</code></pre>
<blockquote>
<p><strong>포인트:</strong> <code>delay()</code> 를 쓰지 않고 TimerOne 인터럽트 + 플래그 방식으로 루프를 막지 않는다. <code>loop()</code> 에서 <code>socketEvent()</code> 를 폴링하기 때문에 블로킹이 생기면 서버 명령을 놓친다.</p>
</blockquote>
<h3 id="socketevent-처리-명령">socketEvent() 처리 명령</h3>
<table>
<thead>
<tr>
<th>수신 커맨드</th>
<th>동작</th>
</tr>
</thead>
<tbody><tr>
<td><code>LED@ON/OFF</code></td>
<td>D13 LED 제어 → <code>SETDB</code> 응답 전송</td>
</tr>
<tr>
<td><code>LAMP@ON/OFF</code></td>
<td>D12 LAMP 제어 → <code>SETDB</code> 응답 전송</td>
</tr>
<tr>
<td><code>MOTOR@{0~100}</code></td>
<td><code>map(0~100 → 0~255)</code> 후 PWM 출력</td>
</tr>
<tr>
<td><code>GETSENSOR@{N}</code></td>
<td>N초 주기로 센서 전송 설정</td>
</tr>
<tr>
<td><code>GETSTATE@DEV</code></td>
<td>현재 LED/LAMP 상태 응답</td>
</tr>
</tbody></table>
<h3 id="센서-전송-포맷">센서 전송 포맷</h3>
<pre><code class="language-c">// 조도는 analogRead(A0) → map(0,1023,0,100) 변환
// 온습도는 dtostrf()로 소수점 포맷 맞춤
sprintf(sendBuf, &quot;[%s]SENSOR@%d@%s@%s\n&quot;, recvId, cds, tempStr, humiStr);
// 예: &quot;[KYM_SQL]SENSOR@88@22.4@ 6.0\n&quot;</code></pre>
<hr />
<h2 id="7-mariadb-구성-raspberry-pi">7. MariaDB 구성 (Raspberry Pi)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8a34b26c-0126-4cfa-bbb3-f1d601bf7719/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d2147096-1ec3-47c3-afcf-4c3741539a36/image.png" /></p>
<h3 id="설치">설치</h3>
<pre><code class="language-bash">sudo apt install mariadb-server mariadb-client -y
sudo mysql</code></pre>
<h3 id="db--테이블-생성">DB / 테이블 생성</h3>
<pre><code class="language-sql">CREATE DATABASE iotdb CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON iotdb.* TO iot@localhost IDENTIFIED BY 'pwiot';

USE iotdb;

-- 센서 시계열 로그 테이블
CREATE TABLE sensor (
    id   INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20),
    date DATE,
    time TIME,
    illu INT,
    temp FLOAT,
    humi FLOAT,
    PRIMARY KEY (id)
) DEFAULT CHARSET=utf8;

-- 디바이스 상태 테이블
CREATE TABLE device (
    id    INT NOT NULL,
    name  VARCHAR(20),
    date  DATE,
    time  TIME,
    value VARCHAR(20),
    info  VARCHAR(20),
    PRIMARY KEY (id)
) DEFAULT CHARSET=utf8;

-- 초기 데이터
INSERT INTO device (id, name, date, time, value, info)
VALUES (1, 'LAMP', now(), now(), 'OFF', 'room1 lamp1');
INSERT INTO device (id, name, date, time, value, info)
VALUES (2, 'PLUG', now(), now(), 'OFF', 'room1 plug1');</code></pre>
<h3 id="외부-접속-허용-서버에서-rpi-db-연결-시">외부 접속 허용 (서버에서 RPi DB 연결 시)</h3>
<pre><code class="language-bash">sudo vi /etc/mysql/mariadb.conf.d/50-server.cnf
# bind-address = 127.0.0.1  ← 주석 처리
sudo service mysql restart</code></pre>
<pre><code class="language-sql">CREATE USER 'iot'@'%' IDENTIFIED BY 'pwiot';
GRANT ALL PRIVILEGES ON iotdb.* TO 'iot'@'%';
FLUSH PRIVILEGES;</code></pre>
<hr />
<h2 id="8-웹-시각화-apache2--php">8. 웹 시각화 (Apache2 + PHP)</h2>
<blockquote>
<p>📁 <a href="https://github.com/kyoung-mo/linuxC/tree/main/html">html</a></p>
</blockquote>
<p>핵심은 웹으로 DB를 직접 조회해서 표와 그래프를 띄울 수 있다는 것. 상세 구현보다는 이런 흐름이 가능하다는 것을 파악하는 용도.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/53221892-7792-44f7-9ede-898e9e0a3b46/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/312bed8f-3bda-4109-9de5-d40ac4416567/image.png" /></p>
<h3 id="설치-1">설치</h3>
<pre><code class="language-bash">sudo apt install apache2 -y
sudo apt install php php-gd php-mysql -y
sudo apt install phpmyadmin -y   # 웹 GUI DB 관리</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/141141c8-2d00-4008-8aac-4854a0941648/image.png" /></p>
<h3 id="파일-구성">파일 구성</h3>
<pre><code>/var/www/html/
├── index.html         # frameset으로 좌우 분할
├── sensorTable.php    # sensor 테이블 → HTML 테이블
└── sensorGraph.php    # sensor 테이블 → Google Charts 라인 그래프</code></pre><h3 id="indexhtml">index.html</h3>
<pre><code class="language-html">&lt;frameset cols=&quot;50%,*&quot;&gt;
  &lt;frame src=&quot;http://10.10.16.90/sensorTable.php&quot;&gt;
  &lt;frame src=&quot;http://10.10.16.90/sensorGraph.php&quot;&gt;
&lt;/frameset&gt;</code></pre>
<h3 id="sensortablephp-핵심-로직">sensorTable.php (핵심 로직)</h3>
<pre><code class="language-php">$conn = mysqli_connect(&quot;localhost&quot;, &quot;iot&quot;, &quot;pwiot&quot;);
mysqli_select_db($conn, &quot;iotdb&quot;);
$result = mysqli_query($conn, &quot;select * from sensor&quot;);
while ($row = mysqli_fetch_array($result)) {
    echo &quot;&lt;tr&gt;&quot;;
    echo &quot;&lt;td&gt;{$row['id']}&lt;/td&gt;&lt;td&gt;{$row['name']}&lt;/td&gt;&quot;;
    echo &quot;&lt;td&gt;{$row['date']}&lt;/td&gt;&lt;td&gt;{$row['time']}&lt;/td&gt;&quot;;
    echo &quot;&lt;td&gt;{$row['illu']}&lt;/td&gt;&lt;td&gt;{$row['temp']}&lt;/td&gt;&lt;td&gt;{$row['humi']}&lt;/td&gt;&quot;;
    echo &quot;&lt;/tr&gt;&quot;;
}</code></pre>
<p><code>&lt;meta http-equiv=&quot;refresh&quot; content=&quot;30&quot;&gt;</code> 으로 30초마다 자동 갱신된다.</p>
<h3 id="sensorgraphphp-핵심-로직">sensorGraph.php (핵심 로직)</h3>
<pre><code class="language-php">// DB에서 데이터 읽어서 PHP 배열로 만든 뒤
$data = array(array('time','illu','temp','humi'));
while ($row = mysqli_fetch_array($result)) {
    array_push($data, array(
        $row['date'].&quot;\n&quot;.$row['time'],
        intval($row['illu']),
        intval($row['temp']),
        intval($row['humi'])
    ));
}</code></pre>
<pre><code class="language-javascript">// json_encode()로 JS에 넘겨서 Google Charts로 그림
var data = &lt;?= json_encode($data) ?&gt;;
google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(function() {
    var chart = new google.visualization.LineChart(
        document.querySelector('#chart_div')
    );
    chart.draw(google.visualization.arrayToDataTable(data), options);
});</code></pre>
<p>결과적으로 <code>http://10.10.16.90</code> 에 접속하면 좌측에 센서 DB 테이블, 우측에 illu · temp · humi 라인 그래프가 출력된다.</p>
<hr />
<h2 id="9-github-소스코드">9. GitHub 소스코드</h2>
<table>
<thead>
<tr>
<th>디렉토리</th>
<th>내용</th>
</tr>
</thead>
<tbody><tr>
<td><a href="https://github.com/kyoung-mo/linuxC/tree/main/iot_socket.d">iot_socket.d</a></td>
<td>iot_server.c, iot_client.c</td>
</tr>
<tr>
<td><a href="https://github.com/kyoung-mo/linuxC/tree/main/sql_client">sql_client</a></td>
<td>iot_client_sensor_device.c (MariaDB 연동)</td>
</tr>
<tr>
<td><a href="https://github.com/kyoung-mo/linuxC/tree/main/Arduino">Arduino</a></td>
<td>wifi_client_v1_idpass.ino, wifi_client_v2_led.ino</td>
</tr>
<tr>
<td><a href="https://github.com/kyoung-mo/linuxC/tree/main/html">html</a></td>
<td>sensorTable.php, sensorGraph.php, index.html</td>
</tr>
</tbody></table>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>1. Arduino + ESP8266 → WiFi로 서버(port 5000) 접속 (ID: KYM_ARD)
2. iot_client_sql    → 서버에 접속 (ID: KYM_SQL)
3. Linux 터미널      → [KYM_ARD]GETSENSOR@5 전송
4. 서버가 Arduino로 라우팅
5. Arduino가 5초마다 [KYM_SQL]SENSOR@88@22.4@6.0 전송
6. 서버가 KYM_SQL 클라이언트로 라우팅
7. iot_client_sql이 수신 → MariaDB sensor 테이블 INSERT
8. 웹브라우저에서 http://RPi_IP 접속 → 표 + 그래프 확인</code></pre>