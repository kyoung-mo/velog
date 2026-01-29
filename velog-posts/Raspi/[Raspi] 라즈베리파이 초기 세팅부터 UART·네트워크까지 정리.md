<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/abc46826-5ca5-403b-a54f-a74ff424f6e6/image.png" /></p>
<hr />
<p>SD카드에 이미저를 구워주자.
microSD카드를 USB 젠더를 이용해 컴퓨터랑 연결해주고, 라즈베리파이 이미저를 다운 받기 위해 아래 사이트에서 다운 받는다.</p>
<ul>
<li><a href="https://www.raspberrypi.com/software/">Raspberry Pi Imager 다운로드 공식 홈페이지</a></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/79724372-bb2f-45bf-b0cd-f4ed6a2166c6/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a006059b-981c-449b-82d9-ecb103d5ced3/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2652024e-ff8f-4103-b7ad-0a17fd3993ba/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d5dc21e5-25fa-42d0-8c5d-ef24e643cb59/image.png" /></p>
<p>공용으로 사용하기 때문에 내 IP와 관련해서 지었다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1057b730-2082-4520-ad2b-27e3ab81c918/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ab7ef39c-7069-4273-aab1-021ff37988e5/image.png" /></p>
<blockquote>
<p>ID : pi
PW : 1234</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a4f591da-0179-4793-a204-4aa7465b6774/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/20fccd0d-74fc-4940-8af4-e65c919284cc/image.png" /></p>
<p>아래 과정은 수업에는 안 쓰지만 개인 라즈베리파이로 간단하게 정리..
(라즈베리파이 켜두기만 하면 저 사이트에서
원격 조정하는 느낌이라 유용한 편)</p>
<p>================================</p>
<ul>
<li><a href="https://connect.raspberrypi.com/devices">Rasp_Connect 사이트</a></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4358e961-bca1-482b-93b7-d730751f1efc/image.png" /></p>
<p>토큰을 공식 Connect 사이트 들어가서 따온다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fa6b8f0b-0ae4-4540-8157-556d767d4531/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/163ef009-e991-4860-b0ff-3a74fbc20d05/image.png" /></p>
<p>두 가지 모드가 있다. </p>
<ul>
<li><code>Connect_via</code></li>
</ul>
<p>1) Screen Sharing</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/84c39927-7486-481b-b5fb-3dc03a13007c/image.png" /></p>
<p>2) Remote shell</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0babeb31-244e-48ed-9505-d3c0f462cd8e/image.png" /></p>
<p>이런식으로 윈도우 창이 열리면서, 원격으로 접속이 가능하다.</p>
<p>=================================
다시 돌아와서)
<img alt="" src="https://velog.velcdn.com/images/mommers/post/434c1fa4-6810-4d29-8dec-9a6dc3e2dcad/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f732b355-2b4f-4de9-9805-576fd9c4d47f/image.png" /></p>
<p>SD 카드에 이미지 굽기는 끝났다.</p>
<p>이제 라즈베리파이 이미저의 설정 메뉴에는 SSH 켜기는 있으나, UART(시리얼 포트) 켜기 버튼이 따로 없기 때문에, SD카드를 PC에 연결해서 설정을 해주어야 한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bd13995b-ad29-44f3-b95e-121a799250c7/image.png" /></p>
<ul>
<li><code>config.txt</code> -&gt; 맨 아래 <code>[all]</code> 부분에 추가</li>
<li><blockquote>
<p><code>enable_uart=1</code></p>
</blockquote>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/62e8c3df-968a-4cc7-9a82-32a3a96fec3f/image.png" /></p>
<ul>
<li><code>cmdline.txt</code> -&gt; 아래 내용 복붙<pre><code class="language-javascript">console=serial0,115200 console=tty1 root=PARTUUID=efab4ffe-02 rootfstype=ext4 fsck.repair=yes rootwait resize splash plymouth.ignore-serial-consoles cfg80211.ieee80211_regdom=KR</code></pre>
</li>
</ul>
<hr />
<h3 id="하드웨어-연결">하드웨어 연결</h3>
<p>라즈베리파이에서는 시리얼 연결을 두 가지 방식으로 한다.</p>
<h4 id="1-uart-connector-사용권장">1. UART CONNECTOR 사용(권장)</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d8388bbc-5430-4f46-ae46-6a4dd038490c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/69426843-c9f4-47ac-a119-dadf884e0270/image.png" /></p>
<p>위 빨간색 232 모듈에서 선 3개만 사용해서 시리얼 모니터에 띄워볼 예정</p>
<ul>
<li>GND &lt;-&gt; GND</li>
<li>TX &lt;-&gt; RX</li>
<li>RX &lt;-&gt; TX</li>
</ul>
<p>배선을 한 이후, PC에 USB-Serial 장치를 연결하고 터미널 프로그램(Putty, TeraTerm, Minicom,Mobaxterm 등)을 연다.</p>
<ul>
<li>처음 부팅하면 10초정도 기다려야 한다. 
⇒ 한번 리부팅이 일어난다.</li>
<li>와이파이 연결되어 있으면 바로 사용가능</li>
<li><strong>Port:</strong> 장치 관리자에서 확인한 포트<br />(예: COM3, /dev/ttyUSB0)</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/95f6f295-bb14-42fc-95f1-d00cc4c9185a/image.png" /></p>
<ul>
<li>MobaXterm-Session 에서 아래와 같이 설정!!<ul>
<li><strong>Baud Rate (속도):</strong> <strong>115200</strong> (가장 중요)</li>
<li><strong>Data bits:</strong> 8</li>
<li><strong>Stop bits:</strong> 1</li>
<li><strong>Parity:</strong> None</li>
<li><strong>Flow Control:</strong> None (XON/XOFF 아님)</li>
</ul>
</li>
</ul>
<p>설정해주면, 성공!</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3a0d40bc-d4a8-4f3e-9f8a-7bd93158c630/image.png" /></p>
<h4 id="2-gpio-헤더-사용기존-방식">2. GPIO 헤더 사용(기존 방식)</h4>
<ul>
<li>설명 스킵</li>
</ul>
<hr />
<h3 id="시리얼-콘솔-상에서-무선-와이파이-접속">시리얼 콘솔 상에서 무선 와이파이 접속</h3>
<ol>
<li><code>nmcli dev wifi list</code> 명령어 : 현재 와이파이 목록 확인</li>
</ol>
<pre><code class="language-javascript">pi@pi-222:~$ nmcli dev wifi list
IN-USE  BSSID  SSID  MODE  CHAN  RATE  SIGNAL  BARS  SECURITY
// 사용 가능한 무선 와이파이 없음</code></pre>
<ol start="2">
<li><code>sudo nmtui</code> 명령어 입력 : GUI로 설정 가능</li>
</ol>
<p>![]
(<a href="https://velog.velcdn.com/images/mommers/post/e4a17477-2f08-4e67-9fb4-b4eee0ac9e85/image.png">https://velog.velcdn.com/images/mommers/post/e4a17477-2f08-4e67-9fb4-b4eee0ac9e85/image.png</a>)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0658bec3-5430-4bfb-8c3b-2580a9561631/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cd7a4e2c-ee0d-4a74-9d50-fe0e3f06feb9/image.png" /></p>
<p>수업에서 다른 사람들과 겹치지 않도록, </p>
<ul>
<li><code>IPv4 CONFIGURATION</code> -&gt; 
Address : 10.10.16.xxx + 50으로 설정 </li>
<li><code>GateWay</code>는 교수님과 동일하게 설정</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4afcf0ce-cf4e-43e9-812d-c5aeef80263d/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b0e23189-e43c-4b43-b253-270038519d0d/image.png" /></p>
<pre><code class="language-javascript">2: eth0: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 2c:cf:67:12:90:ea brd ff:ff:ff:ff:ff:ff
    inet 10.10.16.222/8 brd 10.255.255.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::2ecf:67ff:fe12:90ea/64 scope link noprefixroute
       valid_lft forever preferred_lft forever</code></pre>
<p><code>10.10.16.222</code> 로 잘 설정된 것을 확인할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f2ef6c7e-3e08-429d-9814-37afebeab432/image.png" /></p>
<p><code>ping 8.8.8.8</code> : 인터넷 연결도 잘 되는것을 확인하였다.</p>
<hr />
<h2 id="apt-list---installed">apt list --installed</h2>
<ul>
<li>현재 apt로 깔려있는 명령어 확인.. 까먹었다</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8ce85235-1324-4a3f-bf3b-301366cefc05/image.png" /></p>
<ul>
<li><code>apt list --installed</code> &gt; 깔려있는 패키지 목록 확인만 하는 것이기 때문에 sudo 필요하지 않다. 주로 sudo는 새로운 패키지를 설치하거나, 지우는 경우 사용</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/64584e2c-8ce9-4cf4-b9bb-9c7d53e5b645/image.png" /></p>
<hr />