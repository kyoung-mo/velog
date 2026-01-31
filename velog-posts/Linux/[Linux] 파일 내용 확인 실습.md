<h3 id="파일-내용-확인-1-cat-tac-nl">파일 내용 확인 1. cat, tac, nl</h3>
<ul>
<li><strong>학습:</strong> 짧은 파일 출력. 파일 합치기.</li>
<li><strong>실습:</strong><ul>
<li><code>cat &gt; file.txt</code>로 키보드 입력 내용을 파일로 저장.</li>
</ul>
</li>
</ul>
<pre><code class="language-bash">pi@pi-222:~/project/0130 $ cat &gt; file.txt
file check
EOF
^C
pi@pi-222:~/project/0130 $ ls
file.txt
pi@pi-222:~/project/0130 $ nano file.txt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/819d9615-bf25-4e0c-a860-e975631694d4/image.png" /></p>
<ul>
<li><code>cat file1 file2 &gt; file3</code> 리다이렉션으로 파일 병합.<pre><code class="language-bash">pi@pi-222:~/project/0130 $ nano file1.txt
pi@pi-222:~/project/0130 $ nano file2.txt
pi@pi-222:~/project/0130 $ cat file1 file2 &gt; file3
cat: file1: No such file or directory
cat: file2: No such file or directory
pi@pi-222:~/project/0130 $ ls
file1.txt  file2.txt  file3  file.txt
pi@pi-222:~/project/0130 $ cat file1.txt file2.txt &gt; file3.txt
pi@pi-222:~/project/0130 $ ls
file1.txt  file2.txt  file3  file3.txt  file.txt
pi@pi-222:~/project/0130 $ nano file3.txt</code></pre>
<img alt="" src="https://velog.velcdn.com/images/mommers/post/ff4c65ad-e678-4b0c-9b46-1c01d9b33a15/image.png" /></li>
</ul>
<ul>
<li><code>nl</code> 명령어로 소스 코드 파일에 줄 번호 붙여서 출력해보기.</li>
</ul>
<pre><code class="language-bash">pi@pi-222:~/project/0130 $ nl file1.txt file2.txt &gt; file4.txt
pi@pi-222:~/project/0130 $ ls
file1.txt  file2.txt  file3  file3.txt  file4.txt  file.txt
pi@pi-222:~/project/0130 $ nano file4.txt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ae8ac9d1-b4aa-4ad0-af2e-ddf6ab57021a/image.png" /></p>
<ul>
<li><code>tac</code>으로 로그 파일 역순(최신 내용부터) 출력해보기.</li>
</ul>
<pre><code class="language-bash">pi@pi-222:~/project/0130 $ tac file3.txt
file2.txt
file1.txt</code></pre>
<hr />
<h2 id="파일-내용-확인-2-head-tail-less"><strong>파일 내용 확인 2. head, tail, less</strong></h2>
<h3 id="1syslog-생성하기">1.syslog 생성하기</h3>
<hr />
<p><strong>Ubuntu 24.04</strong> (그리고 최신 라즈베리파이 OS)부터는 <code>/var/log/syslog</code> 파일을 만드는 <strong><code>rsyslog</code> 패키지가 기본 설치되지 않습니다.</strong></p>
<p>대신 <strong><code>systemd-journald</code></strong> 가 로그를 관리하며, 텍스트 파일이 아닌 <strong>바이너리(DB) 형태</strong>로 저장합니다.</p>
<h4 id="방법-1-요즘-방식-추천-journalctl-사용">방법 1. 요즘 방식 (추천: journalctl 사용)</h4>
<p>파일을 열지 않고 전용 명령어로 확인합니다. 기능은 똑같습니다.</p>
<ul>
<li><p><strong>실시간 로그 확인 (<code>tail -f</code> 대체):</strong>Bash</p>
<pre><code class="language-bash">  journalctl -f</code></pre>
</li>
<li><p><strong>전체 로그 보기 (<code>cat</code> 대체):</strong>Bash</p>
<pre><code class="language-bash">  journalctl</code></pre>
</li>
<li><p><strong>부팅 후 로그만 보기:</strong>Bash</p>
<pre><code class="language-bash">  journalctl -b</code></pre>
</li>
</ul>
<h4 id="방법-2-옛날-방식-syslog-파일-부활시키기">방법 2. 옛날 방식 (syslog 파일 부활시키기)</h4>
<p> <code>/var/log/syslog</code>  패키지를 설치하면 바로 생성됩니다.</p>
<ol>
<li><p><strong>설치:</strong>Bash</p>
<pre><code class="language-bash"> sudo apt update
 sudo apt install -y rsyslog</code></pre>
</li>
<li><p><strong>확인:</strong>
설치 직후부터 <code>/var/log/syslog</code> 파일이 생성되고 로그가 쌓이기 시작합니다.</p>
</li>
</ol>
<p><strong>결론:</strong> 그냥 <strong><code>journalctl -f</code></strong> 명령어를 쓰는 습관을 들이는 것이 좋습니다. (더 보기 편함)</p>
<hr />
<h3 id="2-syslog-이벤트-발생하기">2. syslog 이벤트 발생하기</h3>
<hr />
<p>실습을 위해 <strong>터미널을 2개</strong> 띄우고 진행하세요.</p>
<h4 id="1단계-감시하기-터미널-1">1단계: 감시하기 (터미널 1)</h4>
<p>먼저 로그가 들어오는지 실시간으로 지켜봅니다.</p>
<p>Bash</p>
<pre><code class="language-bash">journalctl -f</code></pre>
<p><em>(커서가 깜빡거리며 대기 상태가 됩니다.)</em></p>
<h3 id="2단계-로그-발생시키기-터미널-2">2단계: 로그 발생시키기 (터미널 2)</h3>
<h4 id="방법-1-텍스트-보내기-logger---가장-추천">방법 1. 텍스트 보내기 (<code>logger</code>) - <strong>가장 추천</strong></h4>
<p>터미널 2에서 아래 명령어를 치면, 터미널 1에 즉시 뜹니다.</p>
<p>Bash</p>
<pre><code class="language-bash">logger &quot;안녕하세요, 로그 테스트 중입니다.&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aae4a7d3-514a-49c8-ba07-a64130a36254/image.png" /></p>
<ul>
<li><strong>결과:</strong> <code>Jan 29 21:00:00 ubuntu user: 안녕하세요, 로그 테스트 중입니다.</code></li>
</ul>
<h4 id="방법-2-에러처럼-꾸며서-보내기">방법 2. 에러처럼 꾸며서 보내기</h4>
<p>빨간색이나 강조된 로그를 보고 싶다면 <code>-p</code> (priority) 옵션을 씁니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/82897dd1-c7ac-41c3-972e-06bdfec5f93c/image.png" /></p>
<p>Bash</p>
<pre><code class="language-bash">logger -p user.err &quot;심각한 에러 발생! (테스트임)&quot;</code></pre>
<h4 id="방법-3-시스템-행동-유발하기-sudo">방법 3. 시스템 행동 유발하기 (<code>sudo</code>)</h4>
<p><code>sudo</code> 명령어를 쓸 때마다 보안 로그가 남습니다.</p>
<p>Bash</p>
<pre><code class="language-bash">sudo ls</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f4d998a8-1407-45cc-a5d3-f8a75acb090b/image.png" /></p>
<ul>
<li><strong>결과:</strong> <code>sudo: ubuntu : TTY=pts/1 ; PWD=... ; USER=root ; COMMAND=/usr/bin/ls</code></li>
</ul>
<h4 id="방법-4-하드웨어-이벤트-usb">방법 4. 하드웨어 이벤트 (USB)</h4>
<p>라즈베리파이 USB 포트에 <strong>마우스나 키보드, USB 메모리를 꽂았다 빼보세요.</strong>
커널(<code>kernel</code>)이 하드웨어를 인식하는 과정이 주루룩 올라옵니다.</p>
<p>⇒ 라즈베리파이에 USB-TTL을 꼽습니다. </p>
<hr />
<h3 id="3-syslog-레벨">3. syslog 레벨</h3>
<hr />
<p>Syslog도 커널(<code>printk</code>)과 동일한 <strong>표준 8단계 레벨(0~7)</strong>을 사용합니다.</p>
<p>사실 <code>printk</code>의 레벨 시스템 자체가 Syslog 표준을 따온 것입니다.</p>
<h4 id="1-syslog-8단계-레벨표-severity">1. Syslog 8단계 레벨표 (Severity)</h4>
<p>숫자가 <strong>낮을수록 심각</strong>하고, <strong>높을수록 단순 정보</strong>입니다.</p>
<table>
<thead>
<tr>
<th><strong>번호</strong></th>
<th><strong>이름 (Keyword)</strong></th>
<th><strong>설명</strong></th>
<th><strong>비고</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>0</strong></td>
<td><strong>emerg</strong></td>
<td>Emergency</td>
<td>시스템이 완전히 멈춤 (사용 불가)</td>
</tr>
<tr>
<td><strong>1</strong></td>
<td><strong>alert</strong></td>
<td>Alert</td>
<td>즉시 조치 필요 (DB 손상 등)</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td><strong>crit</strong></td>
<td>Critical</td>
<td>치명적 오류 (하드웨어 에러)</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td><strong>err</strong></td>
<td>Error</td>
<td>일반적 기능 오류 (가장 흔함)</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td><strong>warning</strong></td>
<td>Warning</td>
<td>경고 (문제 될 소지 있음)</td>
</tr>
<tr>
<td><strong>5</strong></td>
<td><strong>notice</strong></td>
<td>Notice</td>
<td>정상이지만 중요한 알림</td>
</tr>
<tr>
<td><strong>6</strong></td>
<td><strong>info</strong></td>
<td>Info</td>
<td>일반적인 정보 (로그인, 시작 등)</td>
</tr>
<tr>
<td><strong>7</strong></td>
<td><strong>debug</strong></td>
<td>Debug</td>
<td>개발용 디버깅 정보</td>
</tr>
</tbody></table>
<pre><code class="language-bash">sudo systemd-analyze set-log-level debug

# 원상복구: 
sudo systemd-analyze set-log-level info

# 확인
systemctl show -p LogLevel
</code></pre>
<ul>
<li>LogLevel 확인 가능!<pre><code class="language-bash">pi@pi-222:~ $ sudo systemd-analyze set-log-level debug
pi@pi-222:~ $ systemctl show -p LogLevel
LogLevel=debug
pi@pi-222:~ $ sudo systemd-analyze set-log-level info
pi@pi-222:~ $ systemctl show -p LogLevel
LogLevel=info</code></pre>
</li>
</ul>
<hr />
<h4 id="2-syslog만의-특징-카테고리가-있다">2. Syslog만의 특징: &quot;카테고리&quot;가 있다</h4>
<p>Syslog는 레벨(Severity) 외에 <strong>&quot;누가 보냈냐(Facility)&quot;</strong>라는 꼬리표가 하나 더 붙습니다.</p>
<p>이 둘을 합쳐서 <strong><code>카테고리.레벨</code></strong> 형식으로 사용합니다.</p>
<ul>
<li><strong>형식:</strong> <code>facility.level</code></li>
<li><strong>예시:</strong><ul>
<li><code>kern.err</code>: <strong>커널</strong>에서 발생한 <strong>에러</strong></li>
<li><code>auth.notice</code>: <strong>보안/인증</strong> 관련 <strong>알림</strong></li>
<li><code>cron.info</code>: <strong>예약 작업</strong> 관련 <strong>정보</strong></li>
<li><code>user.debug</code>: <strong>일반 사용자</strong> 프로그램의 <strong>디버그</strong></li>
</ul>
</li>
</ul>
<hr />
<h4 id="3-실습-레벨-지정해서-로그-보내보기">3. 실습: 레벨 지정해서 로그 보내보기</h4>
<p><code>logger</code> 명령어에 <strong><code>-p</code> (priority)</strong> 옵션을 쓰면 레벨을 골라서 보낼 수 있습니다.</p>
<p><strong>터미널 1 (감시):</strong></p>
<p>Bash</p>
<pre><code class="language-bash">journalctl -f</code></pre>
<p><strong>터미널 2 (발송):</strong></p>
<p>Bash</p>
<pre><code class="language-bash"># 1. 에러 레벨로 보내기 (빨간색으로 표시될 수 있음)
logger -p user.err &quot;이것은 에러입니다!&quot;

# 2. 경고 레벨로 보내기
logger -p user.warning &quot;이것은 경고입니다.&quot;

# 3. 디버그 레벨로 보내기 (설정에 따라 안 보일 수 있음)
logger -p user.debug &quot;이것은 개발용 잡담입니다.&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/98944a03-9a62-4277-8ed9-cb5c0f1bd8b9/image.png" /></p>
<h4 id="4-설정-파일에서의-활용-etcrsyslogconf">4. 설정 파일에서의 활용 (/etc/rsyslog.conf)</h4>
<p>리눅스 내부 설정 파일에서는 이 레벨을 이용해 <strong>&quot;어떤 로그를 저장할지&quot;</strong> 결정합니다.</p>
<p>Plaintext</p>
<pre><code class="language-bash"># 예시: /etc/rsyslog.conf 내용 중

# 1. 모든 카테고리의 info 레벨 이상(*)만 저장해라 (debug는 버림)
*.info;mail.none;authpriv.none      /var/log/syslog

# 2. 에러(err) 레벨 이상인 것만 따로 모아라
*.err                               /var/log/error.log</code></pre>
<p><strong>핵심:</strong> 여기서도 <code>*.info</code>라고 쓰면, <strong>Info(6)보다 숫자가 낮은(0~5, 더 중요한)</strong> 로그들은 자동으로 다 포함됩니다. (부등호 법칙 적용)</p>
<hr />
<h3 id="커널-로그-드라이버-개발-시-printk">커널 로그 (드라이버 개발 시 <code>printk</code>)</h3>
<p>드라이버 개발 중 사용하는 <code>printk</code> 메시지는 <strong>이미 시리얼로 나가고 있을 것입니다.</strong>
만약 안 나온다면, 로그 레벨이 너무 높게 잡혀 있어서 중요한 것만 나오는 상태입니다.</p>
<p><strong>해결책 (모든 잡다한 커널 로그 다 뱉어내게 하기):</strong>
터미널에서 아래 명령어를 입력하세요.</p>
<p>Bash</p>
<pre><code class="language-bash"># 콘솔 로그 레벨을 최고(8)로 높임
sudo sh -c &quot;echo 8 &gt; /proc/sys/kernel/printk&quot;</code></pre>
<p>이제 <code>printk</code>로 찍는 모든 내용이 시리얼 모니터에 실시간으로 뜹니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/18c57928-665b-4069-b1c5-6a328171225d/image.png" /></p>
<p>usb메모리등을 라즈베리파이의 usb에 꼽았다 빼면 커널로그가 보이기 시작함.</p>
<hr />
<h3 id="사용자-로그-syslog-logger-일반-앱">사용자 로그 (<code>syslog</code>, <code>logger</code>, 일반 앱)</h3>
<p>아까 <code>logger &quot;hello&quot;</code>로 보낸 메시지나, 파이썬/C++ 앱에서 <code>printf</code>로 찍은 것은 시리얼 콘솔로 <strong>자동으로 가지 않습니다.</strong> (이건 저널에만 기록됩니다.)</p>
<hr />
<p>평상시(기본값)는 <strong><code>4</code></strong> 로 설정하는 것이 표준입니다.</p>
<p>리눅스 커널의 로그 레벨은 숫자가 <strong>낮을수록 심각한 문제</strong>이고, <strong>높을수록 사소한 정보</strong>입니다.</p>
<p>보통 <strong>&quot;경고(Warning, 4)&quot;</strong> 단계까지만 화면에 보여주고, 잡다한 정보는 숨기는 것이 기본 설정입니다.</p>
<h3 id="1-원래대로-되돌리는-명령어-복구">1. 원래대로 되돌리는 명령어 (복구)</h3>
<p>Bash</p>
<pre><code class="language-bash">sudo sh -c &quot;echo 4 &gt; /proc/sys/kernel/printk&quot;

cat /proc/sys/kernel/printk</code></pre>
<hr />
<h3 id="2-왜-4-인가요-레벨-가이드">2. 왜 '4' 인가요? (레벨 가이드)</h3>
<p>커널 로그 레벨은 총 8단계(0~7)가 있습니다. 설정한 숫자보다 <strong>작은(더 심각한)</strong> 레벨만 화면에 출력됩니다.</p>
<table>
<thead>
<tr>
<th><strong>레벨</strong></th>
<th><strong>이름</strong></th>
<th><strong>설명</strong></th>
<th><strong>출력 여부 (설정값 4일 때)</strong></th>
</tr>
</thead>
<tbody><tr>
<td>0</td>
<td><strong>Emergency</strong></td>
<td>시스템 멈춤 (최악)</td>
<td>✅ 출력됨</td>
</tr>
<tr>
<td>1</td>
<td><strong>Alert</strong></td>
<td>즉각 조치 필요</td>
<td>✅ 출력됨</td>
</tr>
<tr>
<td>2</td>
<td><strong>Critical</strong></td>
<td>치명적 에러</td>
<td>✅ 출력됨</td>
</tr>
<tr>
<td>3</td>
<td><strong>Error</strong></td>
<td>일반 에러</td>
<td>✅ 출력됨</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td><strong>Warning</strong></td>
<td><strong>경고 (주의 요망)</strong></td>
<td>❌ <strong>여기서부터 차단</strong> (화면엔 안 나옴)</td>
</tr>
<tr>
<td>5</td>
<td><strong>Notice</strong></td>
<td>알림 (정상이지만 중요함)</td>
<td>❌ 차단</td>
</tr>
<tr>
<td>6</td>
<td><strong>Info</strong></td>
<td>일반 정보 (드라이버 로딩 등)</td>
<td>❌ 차단</td>
</tr>
<tr>
<td>7</td>
<td><strong>Debug</strong></td>
<td>디버깅용 잡다한 정보</td>
<td>❌ 차단</td>
</tr>
<tr>
<td>- <strong>설정 8 (Debug 모드):</strong> 모든 잡담(<code>pr_info</code>, <code>pr_debug</code>)까지 다 보여줌. 드라이버 개발할 때만 사용.</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>- <strong>설정 4 (Quiet 모드):</strong> 에러나 경고가 떴을 때만 알려줌. 평상시 사용.</td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody></table>
<hr />
<h3 id="3-계속-8로-두면-안-되나요">3. 계속 8로 두면 안 되나요?</h3>
<p>두 가지 문제가 생깁니다.</p>
<ol>
<li><strong>성능 저하:</strong> 시리얼 포트(UART)는 속도가 느립니다. 커널이 모든 동작마다 로그를 뱉어내면, CPU가 로그 출력하느라 실제 작업을 못해서 시스템이 버벅거립니다.</li>
<li><strong>중요한 정보 놓침:</strong> 쓸데없는 정보(<code>Info</code>)가 너무 빨리 스크롤 되어 지나가버려서, 진짜 중요한 에러(<code>Error</code>)를 못 보고 지나칠 수 있습니다.</li>
</ol>
<p><strong>결론:</strong> 개발 끝나면 꼭 <strong>4</strong>로 돌려놓으세요!</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/71e9671d-e520-400b-b65c-657b8858ba1f/image.png" /></p>
<ul>
<li><code>/var/log/syslog</code> 파일을 <code>less</code>로 열고 검색(<code>/</code>), 이동(<code>G</code>, <code>g</code>) 연습.</li>
<li><code>head -n 20</code> vs <code>tail -n 20</code> 비교.</li>
<li><strong>핵심:</strong> <code>tail -f</code> 옵션 켜두고, 다른 터미널에서 시스템 변화(USB 꽂기 등) 실시간 모니터링.</li>
<li>다른 쉘에서 로그인 정보를 실시간으로 확인하기</li>
</ul>