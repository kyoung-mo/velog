<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ddc02e27-94e0-4d47-aafe-d1fe5bea7255/image.png" /></p>
<h3 id="데몬-프로세스-생성-daemon">데몬 프로세스 생성 (Daemon)</h3>
<h3 id="1-데몬daemon이란">1. 데몬(Daemon)이란?</h3>
<p>백그라운드에서 실행되며 특정 서비스를 제공하는 장기 실행 프로세스 (예: <code>httpd</code>, <code>sshd</code>).</p>
<ul>
<li>제어 터미널(Controlling Terminal)이 없음: 사용자의 입력을 직접 받지 않습니다.</li>
<li>부모 프로세스: 과거에는 <code>init</code>(PID 1), 최신 리눅스에서는 <code>systemd</code>가 관리합니다.</li>
<li>로그: 표준 입출력이 없으므로 <code>syslog</code>나 <code>journald</code>를 통해 로그를 남깁니다.</li>
</ul>
<hr />
<h3 id="2-데몬-생성-방식-비교sysv-vs-systemd">2. 데몬 생성 방식 비교(SysV vs systemd)</h3>
<p>가장 중요한 차이점은 프로그래머가 얼마나 많은 코드를 직접 짜야 하는지에 대한 것 입니다.</p>
<table>
<thead>
<tr>
<th>비교 항목</th>
<th>고전 방식 (SysV / Old School)</th>
<th>현대 방식 (systemd / New School)</th>
</tr>
</thead>
<tbody><tr>
<td>구현 난이도</td>
<td>복잡함 (직접 코딩 필요)</td>
<td>매우 간단 (설정 파일 위임)</td>
</tr>
<tr>
<td>프로세스 생성</td>
<td><code>fork()</code> 2번 (Double Fork)</td>
<td><code>systemd</code>가 직접 실행 (<code>Type=simple</code>)</td>
</tr>
<tr>
<td>터미널 제어</td>
<td><code>setsid()</code>, <code>close(fd)</code> 직접 호출</td>
<td><code>systemd</code>가 알아서 처리</td>
</tr>
<tr>
<td>로그 처리</td>
<td>파일 <code>open</code> 후 직접 기록</td>
<td><code>printf</code>만 하면 <code>journald</code>가 수집</td>
</tr>
<tr>
<td>관리</td>
<td>PID 파일 직접 생성/삭제</td>
<td><code>systemd</code>가 PID 추적 및 관리</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-고전적-데몬-생성-coding-the-hard-way">3. 고전적 데몬 생성 (Coding the Hard Way)</h3>
<ol>
<li><code>fork()</code>: 부모를 종료시켜 쉘이 &quot;끝났다&quot;고 착각하게 만듦 (백그라운드 진입).</li>
<li><code>setsid()</code>: 새로운 세션을 만들어 터미널 제어권 박탈 (필수).</li>
<li><code>chdir(&quot;/&quot;)</code>: 작업 디렉토리를 루트로 이동 (USB 등을 마운트 해제 못 하는 문제 방지).</li>
<li><code>umask(0)</code>: 파일 생성 권한 제약을 없앰.</li>
<li><code>close(fd)</code> &amp; <code>dup2</code>: 표준 입출력(0,1,2)을 닫거나 <code>/dev/null</code>로 돌림.</li>
</ol>
<hr />
<h3 id="31-고전적-데몬-예제1">3.1 고전적 데몬 예제1</h3>
<p>SysV는 <code>Double Fork</code>를 통해 부모와 연결을 끊고, 터미널 제어권을 완전히 박탈합니다.</p>
<ul>
<li><code>classic_daemon.c</code></li>
</ul>
<p>이 코드는 Double Fork 기법을 사용하여 터미널 제어권을 완벽하게 제거하고, <code>/dev/null</code>로 표준 입출력을 돌린 뒤, syslog를 통해 로그를 남깁니다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;syslog.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;string.h&gt;
#include &lt;errno.h&gt;

// 실제 서비스 로직 (5초마다 로그 기록)
void main_service_loop() {
    int count = 0;
    while (1) {
        // 터미널이 없으므로 printf 대신 syslog 사용
        syslog(LOG_INFO, &quot;My Classic Daemon is alive! Count: %d&quot;, count++);
        sleep(5);
    }
}

// 데몬화 함수 (핵심)
static void skeleton_daemon() {
    pid_t pid;

    // 1. First Fork: 부모 프로세스 종료 (백그라운드 전환)
    pid = fork();
    if (pid &lt; 0) exit(EXIT_FAILURE);
    if (pid &gt; 0) exit(EXIT_SUCCESS);

    // 2. 새로운 세션 생성 (터미널 제어권 박탈)
    if (setsid() &lt; 0) exit(EXIT_FAILURE);

    // 3. 시그널 처리 (SIGHUP 무시)
    signal(SIGCHLD, SIG_IGN);
    signal(SIGHUP, SIG_IGN);

    // 4. Second Fork: 세션 리더가 아님을 보장 (터미널 재할당 방지)
    pid = fork();
    if (pid &lt; 0) exit(EXIT_FAILURE);
    if (pid &gt; 0) exit(EXIT_SUCCESS);

    // 5. 파일 모드 마스크 초기화 (권한 문제 방지)
    umask(0);

    // 6. 작업 디렉토리 변경 (마운트된 파일시스템 잠금 방지)
    if (chdir(&quot;/&quot;) &lt; 0) {
        syslog(LOG_ERR, &quot;Could not change working directory to /&quot;);
        exit(EXIT_FAILURE);
    }

    // 7. 표준 입출력 닫기 및 /dev/null 리다이렉션
    // (printf 등이 에러 없이 동작하도록 구멍으로 연결)
    int x;
    for (x = sysconf(_SC_OPEN_MAX); x &gt;= 0; x--) {
        close(x);
    }

    // fd 0, 1, 2를 /dev/null로 연결
    int fd0 = open(&quot;/dev/null&quot;, O_RDWR); // stdin
    int fd1 = dup(0);                    // stdout
    int fd2 = dup(0);                    // stderr

    // syslog 초기화
    openlog(&quot;classic_daemon&quot;, LOG_PID, LOG_DAEMON);
}

int main() {
    // 데몬 만들기 시작
    skeleton_daemon();

    // 여기까지 오면 완벽한 데몬 상태임
    syslog(LOG_NOTICE, &quot;Daemon started successfully.&quot;);

    // 실제 서비스 시작
    main_service_loop();

    // 종료 (실제로는 도달하지 않음)
    closelog();
    return EXIT_SUCCESS;
}</code></pre>
<hr />
<h3 id="3-2-실행-및-확인-방법">3-2) 실행 및 확인 방법</h3>
<h4 id="①-컴파일">① 컴파일</h4>
<pre><code class="language-bash">gcc classic_daemon.c -o classic_daemon</code></pre>
<h4 id="②-실행">② 실행</h4>
<pre><code class="language-bash">./classic_daemon
# (아무런 메시지 없이 쉘 프롬프트가 바로 떨어져야 정상)</code></pre>
<h4 id="③-동작-확인-ps-확인">③ 동작 확인 (PS 확인)</h4>
<p>터미널(<code>TTY</code>)이 <code>?</code>로 표시되어야 하며, <code>PPID</code>가 <code>1</code>(systemd/init)이어야 합니다.</p>
<pre><code class="language-bash">ps -efj | grep classic_daemon
# 출력 예시:
# andrew   12345     1  12344 ?        00:00:00 ./classic_daemon</code></pre>
<ul>
<li>TTY = <code>?</code>: 터미널 없음 (성공).</li>
<li>PPID = <code>1</code>: 부모가 init/systemd (성공).</li>
</ul>
<h4 id="④-로그-확인-syslog">④ 로그 확인 (Syslog)</h4>
<p><code>printf</code> 내용이 화면에 안 나오고 시스템 로그에 기록됩니다.</p>
<pre><code class="language-bash"># Ubuntu/Debian 계열
tail -f /var/log/syslog | grep classic_daemon

# 출력 예시:
# Feb  1 16:30:00 hostname classic_daemon[12345]: Daemon started successfully.
# Feb  1 16:30:00 hostname classic_daemon[12345]: My Classic Daemon is alive! Count: 0
# Feb  1 16:30:05 hostname classic_daemon[12345]: My Classic Daemon is alive! Count: 1</code></pre>
<h3 id="⑤-종료-방법">⑤ 종료 방법</h3>
<p>데몬은 스스로 죽지 않으므로 <code>kill</code> 명령어로 종료해야 합니다.</p>
<pre><code class="language-bash">killall classic_daemon
# 또는
kill &lt;PID&gt;</code></pre>
<hr />
<h3 id="3-3-핵심-코드">3-3) 핵심 코드</h3>
<ol>
<li><code>setsid()</code>: 이 호출이 없으면 데몬이 터미널을 붙잡고 있어서, 터미널을 닫으면 데몬도 같이 죽습니다. 필수 과정입니다.</li>
<li><code>/dev/null</code> 리다이렉션: 데몬 내부에서 실수로 <code>printf</code>를 써도 프로그램이 죽지 않도록, 표준 출력을 &quot;블랙홀&quot;로 연결해두는 안전 장치입니다.</li>
<li><code>chdir(&quot;/&quot;)</code>: 데몬이 <code>/home/user/test</code> 폴더에서 실행된 채로 있으면, 관리자가 <code>/home</code> 파티션을 언마운트 할 수 없게 됩니다. 그래서 루트로 이동시킵니다.</li>
</ol>
<hr />
<h3 id="4-systemd-기반-데몬-configuring-the-easy-way">4. systemd 기반 데몬 (Configuring the Easy Way)</h3>
<p><code>10.newdaemon.c</code> 처럼 코드가 매우 단순해집니다. <code>fork</code>도, <code>setsid</code>도 필요 없습니다. Unit 파일(.service)이 모든 귀찮은 일을 대신합니다.</p>
<h4 id="핵심-unit-파일-설정-service">핵심 Unit 파일 설정 (<code>.service</code>)</h4>
<pre><code class="language-bash">[Service]
ExecStart=/home/pi/bin/10.newdaemon  # 실행할 파일 경로
Type=simple                          # fork 안 하고 바로 실행함 (기본값)
Restart=on-failure                   # 죽으면 자동으로 다시 살려냄 (데몬의 영생)</code></pre>
<h4 id="로깅의-혁신-journald">로깅의 혁신 (<code>journald</code>)</h4>
<ul>
<li>바이너리 저장: 텍스트가 아닌 바이너리로 저장되어 검색 속도가 빠르고 위변조가 어렵습니다.</li>
<li>자동 수집: 프로그램에서 <code>printf(&quot;Hello&quot;);</code> 만 해도 <code>journalctl</code>에 예쁘게 기록됩니다.</li>
<li>명령어:<ul>
<li><code>journalctl -u [서비스명]</code>: 해당 서비스 로그만 보기.</li>
<li><code>journalctl -f</code>: 실시간 로그 확인 (tail -f 유사).</li>
</ul>
</li>
</ul>
<hr />
<h3 id="5-트러블슈팅-unit-is-masked-에러">5. 트러블슈팅: &quot;Unit is masked&quot; 에러</h3>
<p><code>masked</code> 상태는 서비스가 &quot;/dev/null&quot;로 링크되어 실행이 원천 봉쇄된 상태입니다.</p>
<ul>
<li><code>sudo systemctl start mydaemon</code> 실패 → <code>Unit is masked.</code></li>
<li>의도적인 차단 혹은 잘못된 심볼릭 링크 때문</li>
<li>해결 순서:<ol>
<li>해제 : <code>sudo systemctl unmask [서비스명]</code></li>
<li>확인 : <code>/etc/systemd/system/</code> 아래에 서비스 파일이 진짜 있는지 확인 (<code>ls -l</code>).</li>
<li>갱신 : <code>sudo systemctl daemon-reload</code> (설정 변경 사항 반영).</li>
<li>시작 : <code>sudo systemctl start [서비스명]</code></li>
</ol>
</li>
</ul>
<hr />
<h3 id="정리">정리</h3>
<ul>
<li><p>새로운 데몬을 개발한다면 <code>systemd</code> 방식(<code>Type=simple</code>)을 권장하는 편이라고 합니다. 코드가 간결해지고, 로그 관리와 프로세스 감시(Watchdog)를 OS에 맡길 수 있어 훨씬 안정적입니다.</p>
</li>
<li><p>만약 데몬이 죽었을 때 이메일을 보내거나, 특정 시간(타이머)에만 실행되게 하려면 <code>systemd</code>의 Timer Unit을 확인해보면 좋습니다.</p>
</li>
</ul>