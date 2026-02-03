<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7c4423b7-3c69-47ec-97ed-62eee84e4317/image.png" /></p>
<hr />
<h3 id="파일과-디렉토리-정보">파일과 디렉토리 정보</h3>
<h3 id="1-파일-io-방식-비교-system-call-vs-standard-library">1. 파일 I/O 방식 비교: System Call vs Standard Library</h3>
<p>리눅스에서 파일을 다루는 방법은 크게 커널을 직접 호출(<code>System Call</code>)하거나, C 표준 라이브러리(<code>Wrapper</code>)를 사용하는 것으로 나뉩니다.</p>
<table>
<thead>
<tr>
<th><strong>구분</strong></th>
<th><strong>System Call (저수준)</strong></th>
<th><strong>Standard Library (고수준)</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>함수</strong></td>
<td><code>open</code>, <code>read</code>, <code>write</code>, <code>close</code></td>
<td><code>fopen</code>, <code>fread</code>, <code>fwrite</code>, <code>fclose</code></td>
</tr>
<tr>
<td><strong>식별자</strong></td>
<td><strong>File Descriptor (int fd)</strong></td>
<td><em>*File Stream (FILE fp)</em></td>
</tr>
<tr>
<td><strong>버퍼링</strong></td>
<td>없음 (Unbuffered, 직접 커널 요청)</td>
<td>있음 (Buffered, 성능 최적화)</td>
</tr>
<tr>
<td><strong>이식성</strong></td>
<td>리눅스/유닉스 계열 종속</td>
<td>모든 C 언어 지원 OS 호환</td>
</tr>
<tr>
<td><strong>헤더</strong></td>
<td><code>&lt;fcntl.h&gt;</code>, <code>&lt;unistd.h&gt;</code></td>
<td><code>&lt;stdio.h&gt;</code></td>
</tr>
</tbody></table>
<hr />
<h3 id="2-주요-system-call-및-플래그-open">2. 주요 System Call 및 플래그 (<code>open</code>)</h3>
<ul>
<li><code>&lt;fcntl.h&gt;</code>, <code>&lt;unistd.h&gt;</code> 추가 해야함<h4 id="함수-원형">함수 원형</h4>
</li>
</ul>
<pre><code class="language-c">int open(const char *pathname, int flags, mode_t mode);
ssize_t write(int fd, const void *buf, size_t count);
ssize_t read(int fd, void *buf, size_t count);</code></pre>
<hr />
<h4 id="주요-flags---fcntlh-에-포함">주요 Flags -&gt; fcntl.h 에 포함</h4>
<p><code>O_RDONLY</code> (읽기), <code>O_WRONLY</code> (쓰기), <code>O_RDWR</code> (읽기/쓰기)</p>
<ul>
<li><code>O_CREAT</code>: 파일 없으면 생성 (생성 시 <code>mode</code> 권한 필수).</li>
<li><code>O_EXCL</code>: <code>O_CREAT</code>와 함께 사용. 파일이 이미 있으면 에러(덮어쓰기 방지).</li>
<li><code>O_TRUNC</code>: 파일이 이미 있으면 내용을 싹 지우고 크기를 0으로 만듦.</li>
<li><code>O_APPEND</code>: 파일 끝에 내용 추가.</li>
</ul>
<hr />
<h4 id="권한-설정-permission--umask">권한 설정 (Permission) &amp; umask</h4>
<p><code>0664</code>: User(RW), Group(RW), Other(R).
코드에서 <code>0664</code>를 줘도, 실제 파일 권한은 <code>0664 &amp; ~umask</code>로 결정됨.</p>
<ul>
<li>일반 유저 <code>umask</code>: 보통 <code>0002</code> → 결과 <code>0664</code></li>
<li>Root(<code>sudo</code>) <code>umask</code>: 보통 <code>0022</code> → 결과 <code>0644</code>. (예제에서 <code>sudo</code> 실행 시 권한이 달라진 이유)</li>
</ul>
<pre><code>| **Umask** | **의미** | **최종 권한 (파일/디렉터리)** | **사용처** |
| --- | --- | --- | --- |
| **0000** | 아무것도 안 뺌 (완전 개방) | 666 / 777 | 개발/테스트용 (위험) |
| **0002** | Other의 쓰기만 뺌 | 664 / 775 | **일반 사용자 기본값** (같은 그룹끼리 협업 용이) |
| **0022** | Group, Other의 쓰기 뺌 | 644 / 755 | **Root / 서버 기본값** (나만 수정 가능) |
| **0077** | 나 빼고 전부 차단 | 600 / 700 | 개인 키, 보안 설정 파일 (`.ssh` 등) |</code></pre><hr />
<h3 id="3-코드-예제-struct--binary-io">3. 코드 예제 (Struct &amp; Binary I/O)</h3>
<p>로깅, 프로세스 잠금, 논블로킹, 리다이렉션을 통해 <code>open</code> 플래그와 주요 시스템 콜 활용법을 정리했습니다.</p>
<hr />
<h3 id="1-로그-파일-기록-atomic-append">1. 로그 파일 기록 (Atomic Append)</h3>
<p>서버나 데몬에서 로그를 남길 때, 여러 프로세스가 동시에 써도 <strong>내용이 덮어쓰기되거나 꼬이지 않게</strong> 하는 것이 핵심입니다.</p>
<p><code>O_APPEND</code> : 커널 레벨에서 쓰기 직전, 파일 포인터를 무조건 <strong>파일의 끝</strong>으로 이동시킴 (Atomic Operation). 경쟁 상태(Race Condition) 방지.</p>
<pre><code class="language-c">#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;stdio.h&gt;

void write_log(const char *msg) {
    // O_APPEND: 쓰기 시 무조건 파일 끝에 붙임 (동시성 보장)
    // 0644: 소유자 RW, 그룹/기타 R
    int fd = open(&quot;system.log&quot;, O_WRONLY | O_CREAT | O_APPEND, 0644);
    if (fd == -1) {
        perror(&quot;log open fail&quot;);
        return;
    }

    // 실제로는 timestamp 등을 붙여서 write함
    write(fd, msg, strlen(msg));
    write(fd, &quot;\n&quot;, 1);

    close(fd);
}

int main() {
    write_log(&quot;[INFO] System Started&quot;);
    write_log(&quot;[WARN] Memory usage high&quot;);
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0bdfcb7e-3439-485e-b38e-add60c78a1fd/image.png" /></p>
<blockquote>
<p><code>file_log.c</code>에 대한 로그 <code>system.log</code>가 생성된 것을 확인할 수 있고, <code>ls -al</code> 명령어를 통해 <code>system.log</code>가775 -&gt; 644 로 권한이 바뀐 것을 확인할 수 있다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/95eed805-178a-4590-a8d4-6a17c4e37aad/image.png" /></p>
</blockquote>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/20167f84-83f0-48ef-b516-749e1a180d64/image.png" /></p>
<p>위(Raspi), 아래(wsl) 환경에서 file file_log, file file_log_wsl을 비교해보면</p>
<pre><code class="language-bash">// 라즈베리파이5
pi@pi-222:~/project/linux_system $ file file_log
file_log: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, BuildID[sha1]=1753207b9ae31e16b7b3de9a38ad1135a42b880f, for GNU/Linux 3.7.0, with debug_info, not stripped

// wsl
mo@DESKTOP-HMRIDMH:~/project/linux_system$ file file_log_wsl 
file_log_wsl: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b116cbfe4854e154f043b34b8980028414f406df, for GNU/Linux 3.2.0, not stripped</code></pre>
<hr />
<h4 id="timestamp-붙여서-write함">timestamp 붙여서 write함</h4>
<p><code>write()</code> 시스템 콜은 <code>printf</code>처럼 포맷팅(<code>%d</code>, <code>%s</code>) 기능이 없습니다. 오직 <strong>&quot;바이트 배열&quot;</strong>만 처리합니다.</p>
<p>따라서, <strong><code>sprintf</code></strong> 계열 함수를 사용하여 <strong>[시간 + 메시지]</strong>를 하나의 문자열 버퍼로 합친 뒤, 그 버퍼를 <code>write()</code> 해야 합니다.</p>
<h4 id="방법-1-snprintf--write-표준적인-방식">방법 1: <code>snprintf</code> + <code>write</code> (표준적인 방식)</h4>
<p>메모리 버퍼에 내용을 미리 완성한 뒤 파일에 씁니다. 가장 일반적입니다.</p>
<pre><code class="language-c">#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;stdio.h&gt;
#include &lt;time.h&gt;   // 시간 관련 헤더

void write_log_with_time(const char *msg) {
    int fd = open(&quot;system.log&quot;, O_WRONLY | O_CREAT | O_APPEND, 0644);
    if (fd == -1) return;

    // 1. 현재 시간 구하기
    time_t now = time(NULL);
    struct tm t;
    localtime_r(&amp;now, &amp;t); // Thread-safe한 버전 사용 권장

    // 2. 시간 포맷팅 (예: 2026-01-31 14:00:00)
    char time_str[64];
    strftime(time_str, sizeof(time_str), &quot;%Y-%m-%d %H:%M:%S&quot;, &amp;t);

    // 3. 최종 로그 문자열 만들기 (시간 + 메시지 + 개행)
    char log_buf[1024];
    // snprintf: 버퍼 오버플로우 방지 (안전함)
    int len = snprintf(log_buf, sizeof(log_buf), &quot;[%s] %s\n&quot;, time_str, msg);

    // 4. 한번에 쓰기 (Atomic write 효과)
    if (len &gt; 0) {
        write(fd, log_buf, len);
    }

    close(fd);
}</code></pre>
<h4 id="방법-2-dprintf-사용-linuxposix-전용-꿀팁">방법 2: <code>dprintf</code> 사용 (Linux/POSIX 전용 꿀팁)</h4>
<p>리눅스 시스템 프로그래밍에서는 <code>dprintf</code> (Descriptor printf)를 지원합니다. <code>fd</code>에 직접 <code>printf</code> 포맷을 쏠 수 있어 코드가 훨씬 간결해집니다.</p>
<pre><code class="language-c">#define _POSIX_C_SOURCE 200809L // dprintf 사용을 위한 매크로
#include &lt;stdio.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;time.h&gt;

void write_log_simple(const char *msg) {
    int fd = open(&quot;system.log&quot;, O_WRONLY | O_CREAT | O_APPEND, 0644);
    if (fd == -1) return;

    time_t now = time(NULL);
    struct tm t;
    localtime_r(&amp;now, &amp;t);

    char time_str[64];
    strftime(time_str, sizeof(time_str), &quot;%Y-%m-%d %H:%M:%S&quot;, &amp;t);

    // ★ 핵심: write() 대신 printf처럼 사용 가능
    dprintf(fd, &quot;[%s] %s\n&quot;, time_str, msg);

    close(fd);
}</code></pre>
<h4 id="핵심-함수-요약">핵심 함수 요약</h4>
<ul>
<li><strong><code>time()</code></strong>: 현재 유닉스 타임스탬프(초 단위) 가져오기.</li>
<li><strong><code>localtime_r()</code></strong>: 타임스탬프를 년/월/일 구조체(<code>struct tm</code>)로 변환. (<code>_r</code>이 붙어야 멀티스레드에서 안전).</li>
<li><strong><code>strftime()</code></strong>: 구조체를 예쁜 문자열(<code>&quot;2026-01-31&quot;</code>)로 변환.</li>
<li><strong><code>dprintf()</code></strong>: <code>fd</code>에 포맷팅 문자열을 바로 쏘는 함수.</li>
</ul>
<hr />
<h3 id="2-단일-인스턴스-실행-보장-pid-lock-file">2. 단일 인스턴스 실행 보장 (PID Lock File)</h3>
<p>프로그램이 중복 실행되는 것을 막기 위해 <strong>PID 파일</strong>을 생성합니다. 파일 존재 여부 확인과 생성이 <strong>동시에(Atomic)</strong> 이루어져야 합니다.</p>
<ul>
<li><strong>핵심 플래그:</strong> <code>O_EXCL</code><ul>
<li><code>O_CREAT</code>와 함께 사용 시, <strong>&quot;파일이 없으면 만들고, 있으면 즉시 에러(EEXIST) 리턴&quot;</strong>함.</li>
<li><code>if (access) { open }</code> 방식의 경쟁 상태(TOCTOU) 보안 취약점을 해결.</li>
</ul>
</li>
</ul>
<pre><code class="language-c">#include &lt;fcntl.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;errno.h&gt;
#include &lt;string.h&gt; // dprintf 사용시 필요할 수 있음

#define PID_FILE &quot;/var/run/myapp.pid&quot;

int main() {
    // 1. PID 파일 열기 (O_EXCL: 이미 있으면 실패)
    int fd = open(PID_FILE, O_WRONLY | O_CREAT | O_EXCL, 0644);

    if (fd == -1) {
        if (errno == EEXIST) {
            fprintf(stderr, &quot;[Error] 프로그램이 이미 실행 중입니다! (PID 파일 존재)\\n&quot;);
            exit(1);
        }
        perror(&quot;open failed&quot;); // 권한 문제 등 다른 에러
        exit(1);
    }

    // 2. 내 PID 기록
    dprintf(fd, &quot;%d\\n&quot;, getpid());

    // 3. 실행 상태 유지 (테스트를 위해 무한 대기)
    printf(&quot;프로그램 시작됨. (PID: %d)\\n&quot;, getpid());
    printf(&quot;종료하려면 'kill %d' 또는 Ctrl+C를 누르세요.\\n&quot;, getpid());

    while(1) {
        sleep(10);
    }

    // (참고) 강제 종료 시 이 부분은 실행 안 됨 -&gt; 파일이 남음 (단점)
    close(fd);
    return 0;
}</code></pre>
<hr />
<h3 id="테스트-시나리오-터미널-2개-사용">테스트 시나리오 (터미널 2개 사용)</h3>
<pre><code class="language-cpp">gcc single_proc.c -o single_proc</code></pre>
<h4 id="①-첫-번째-실행-성공-케이스">① 첫 번째 실행 (성공 케이스)</h4>
<p><code>/var/run</code>에 파일을 써야 하므로 <strong><code>sudo</code></strong>가 필수입니다.</p>
<p>Bash</p>
<pre><code class="language-cpp"># 터미널 A
sudo ./single_proc</code></pre>
<pre><code class="language-cpp">결과:프로그램 시작됨. (PID: 1234) 가 뜨고 멈춰있음.</code></pre>
<h4 id="②-두-번째-실행-중복-방지-확인">② 두 번째 실행 (중복 방지 확인)</h4>
<p>새 터미널을 열거나, 기존 터미널에서 백그라운드로 실행 후 재시도합니다.</p>
<p>Bash</p>
<pre><code class="language-cpp"># 터미널 B (또는 새 창)
sudo ./single_proc</code></pre>
<blockquote>
<p>결과:[Error] 프로그램이 이미 실행 중입니다! (PID 파일 존재) 라고 뜨고 즉시 종료됨.</p>
</blockquote>
<h4 id="정리-및-파일-확인">정리 및 파일 확인</h4>
<p>이 방식의 단점(파일이 남는 문제)을 확인해 봅니다.</p>
<ol>
<li>실행 중인 프로세스 강제 종료 (Ctrl+C).</li>
<li>다시 실행 시도:Bash</li>
</ol>
<pre><code class="language-cpp">sudo ./single_proc</code></pre>
<blockquote>
<p>결과: 프로세스가 없는데도 [Error] ... 가 뜨며 실행이 안 됨. (좀비 파일 문제)</p>
</blockquote>
<ol start="3">
<li><strong>수동 해결:</strong>Bash</li>
</ol>
<p><code>sudo rm /var/run/myapp.pid</code>
지워줘야 다시 실행됩니다. (그래서 <code>flock</code> 방식을 더 추천함).</p>
<hr />
<h3 id="flock함수">flock()함수</h3>
<p><strong>&quot;잠금 파일(Lock File)을 만들고 <code>flock()</code> 함수로 침(Flag)을 발라라.&quot;</strong></p>
<p>가장 확실하고 안전한 방법은 <strong>파일 잠금(File Locking)</strong> 기능을 사용하는 것입니다.</p>
<h4 id="추천-방법-flock-사용">추천 방법: <code>flock()</code> 사용</h4>
<p>운영체제 차원에서 파일에 &quot;사용 중&quot; 표시를 남기는 방식입니다.
가장 큰 장점은 <strong>프로그램이 비정상 종료(Crash, Kill)되어도 OS가 자동으로 잠금을 해제</strong>해줍니다. (좀비 잠금 파일이 남지 않음).</p>
<h4 id="코드-구현-clinux">코드 구현 (C/Linux)</h4>
<p>C</p>
<pre><code class="language-cpp">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;sys/file.h&gt; // flock을 위해 필요
#include &lt;errno.h&gt;

#define LOCK_FILE &quot;/var/run/myapp.lock&quot; // 보통 /var/run 또는 /tmp 사용

int main() {
    // 1. 잠금 파일 열기 (없으면 생성)
    int fd = open(LOCK_FILE, O_RDWR | O_CREAT, 0666);
    if (fd &lt; 0) {
        perror(&quot;Open lock file failed&quot;);
        exit(1);
    }

    // 2. 잠금 시도 (핵심!)
    // LOCK_EX: 배타적 잠금 (나만 쓸 거야)
    // LOCK_NB: Non-Blocking (이미 잠겨있으면 기다리지 말고 바로 에러 리턴해)
    if (flock(fd, LOCK_EX | LOCK_NB) == -1) {
        if (errno == EWOULDBLOCK) {
            fprintf(stderr, &quot;&gt;&gt;&gt; 프로그램이 이미 실행 중입니다! &lt;&lt;&lt;\n&quot;);
            exit(1); // 중복 실행이므로 종료
        } else {
            perror(&quot;Lock failed&quot;);
            exit(1);
        }
    }

    // 3. 성공 시: 이후 정상 로직 수행
    printf(&quot;프로그램 시작... (PID: %d)\n&quot;, getpid());

    // 프로그램이 도는 동안 fd를 닫으면 안 됨!
    while(1) {
        sleep(10); 
    }

    return 0;
}</code></pre>
<h4 id="동작-원리">동작 원리</h4>
<ol>
<li><strong>첫 번째 실행:</strong> <code>flock</code>이 성공하고 파일을 붙잡음.</li>
<li><strong>두 번째 실행:</strong> <code>flock</code>을 시도했으나, 이미 첫 번째 놈이 잡고 있어서 <code>EWOULDBLOCK</code> 에러 발생 → <strong>즉시 종료</strong>.</li>
<li><strong>종료 시:</strong> 프로세스가 죽으면 OS가 <code>fd</code>를 회수하면서 잠금도 자동으로 풀림.</li>
</ol>
<hr />
<h4 id="비추천-방법-예전-방식">비추천 방법 (예전 방식)</h4>
<ul>
<li><strong>PID 파일 존재 여부 체크 (<code>O_EXCL</code>):</strong><ul>
<li>파일이 있으면 실행 불가로 판단.</li>
<li><strong>치명적 단점:</strong> 프로그램이 버그로 뻗어버리면 파일이 그대로 남아서, <strong>재부팅 전까지 다시 실행 못하는 상황</strong> 발생 (수동으로 지워줘야 함).</li>
</ul>
</li>
</ul>
<hr />
<h3 id="3-논블로킹-읽기-non-blocking-io">3. 논블로킹 읽기 (Non-blocking I/O)</h3>
<p>키보드 입력, 파이프, 소켓 등에서 <strong>데이터가 없으면 기다리지 않고 다른 일을 하러 가야 할 때</strong> 사용합니다. (이벤트 루프 방식).</p>
<ul>
<li><strong>핵심 플래그:</strong> <code>O_NONBLOCK</code><ul>
<li><code>read</code> 호출 시 데이터가 없으면 대기(Block)하지 않고 즉시 <code>1</code> 리턴하며 <code>errno</code>를 <code>EAGAIN</code>으로 설정.</li>
</ul>
</li>
</ul>
<pre><code class="language-c">#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;
#include &lt;errno.h&gt;

int main() {
    char buf[128];
    // 표준 입력(0)을 논블로킹 모드로 다시 열기 (또는 fcntl 사용 가능)
    // 예제 편의상 FIFO나 디바이스 파일이라 가정
    int fd = open(&quot;/dev/tty&quot;, O_RDONLY | O_NONBLOCK); 

    while (1) {
        ssize_t ret = read(fd, buf, sizeof(buf));

        if (ret &gt; 0) {
            printf(&quot;Read data: %.*s\n&quot;, (int)ret, buf);
        } else if (ret == -1) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // 데이터가 없음. 에러가 아님.
                printf(&quot;No data... doing other tasks...\n&quot;);
                sleep(1); // 다른 작업 시뮬레이션
                continue;
            }
            perror(&quot;read error&quot;);
            break;
        }
    }
    close(fd);
    return 0;
}</code></pre>
<hr />
<h3 id="devtty">/dev/tty</h3>
<p>정확히 말하면 <strong>&quot;키보드 그 자체(H/W)&quot;는 아니지만, &quot;프로세스와 연결된 터미널 창(S/W)&quot;</strong>을 의미합니다.
하지만 결과적으로 <strong>&quot;키보드 입력을 받아오는 통로&quot;</strong> 역할을 합니다.</p>
<h4 id="1-devtty의-정체-마법의-거울-alias">1. <code>/dev/tty</code>의 정체: &quot;마법의 거울 (Alias)&quot;</h4>
<ul>
<li><strong>정의:</strong> 현재 프로세스를 제어하고 있는 <strong>터미널(Controlling Terminal)</strong>을 가리키는 <strong>특수 파일(Alias)</strong>입니다.</li>
<li><strong>동작:</strong><ul>
<li>내가 <strong>터미널 1</strong>(<code>pts/0</code>)에서 실행하면 → <code>/dev/tty</code>는 <code>/dev/pts/0</code>을 가리킵니다.</li>
<li>내가 <strong>터미널 2</strong>(<code>pts/1</code>)에서 실행하면 → <code>/dev/tty</code>는 <code>/dev/pts/1</code>을 가리킵니다.</li>
</ul>
</li>
<li><strong>결과:</strong> 어느 창에서 실행하든 상관없이 <strong>&quot;지금 사용자가 보고 있는 그 화면과 키보드&quot;</strong>에 연결해 줍니다.</li>
</ul>
<h4 id="2-데이터-흐름-키보드-→-devtty">2. 데이터 흐름 (키보드 → <code>/dev/tty</code>)</h4>
<p>물리적 키보드가 <code>/dev/tty</code>까지 도달하는 과정입니다.</p>
<ol>
<li><strong>Hardware:</strong> 키보드 누름.</li>
<li><strong>Kernel Driver:</strong> <code>/dev/input/eventX</code> (Raw 데이터 처리).</li>
<li><strong>Terminal Emulator:</strong> (예: Putty, VSCode 터미널) 입력을 받아 텍스트로 변환.</li>
<li><strong>TTY Driver:</strong> 입력된 문자를 버퍼에 담음.</li>
<li><strong><code>/dev/tty</code>:</strong> 애플리케이션이 여기서 <code>read()</code>를 하면 버퍼에 담긴 키보드 글자를 가져옴.</li>
</ol>
<h4 id="3-왜-stdin0번-대신-devtty를-썼나요">3. 왜 <code>stdin</code>(0번) 대신 <code>/dev/tty</code>를 썼나요?</h4>
<p>보통 <code>stdin</code>도 키보드와 연결되어 있지만, <strong>리다이렉션</strong>될 경우 키보드가 아니게 됩니다.</p>
<ul>
<li><strong><code>scanf</code> / <code>read(0)</code>:</strong><ul>
<li>명령어: <code>./app &lt; input.txt</code></li>
<li>결과: 키보드가 아니라 <strong>파일(<code>input.txt</code>)</strong> 내용을 읽어버립니다.</li>
</ul>
</li>
<li><strong><code>open(&quot;/dev/tty&quot;)</code>:</strong><ul>
<li>명령어: <code>./app &lt; input.txt</code></li>
<li>결과: 표준 입력은 파일로 바뀌었어도, <code>/dev/tty</code>는 여전히 <strong>사용자의 키보드/터미널</strong>을 가리킵니다.</li>
<li><strong>용도:</strong> &quot;비밀번호 입력&quot;이나 &quot;계속하시겠습니까?(Y/n)&quot; 처럼 <strong>반드시 사람의 직접 입력</strong>을 받아야 할 때 사용합니다.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="4-표준-출력-리다이렉션-daemon-log">4. 표준 출력 리다이렉션 (Daemon Log)</h3>
<p><code>printf</code>로 찍는 모든 내용을 터미널이 아닌 <strong>특정 파일</strong>로 돌릴 때 사용합니다. (데몬 프로세스 만들 때 필수).</p>
<ul>
<li><strong>핵심 시스템 콜:</strong> <code>dup2(old_fd, new_fd)</code><ul>
<li><code>new_fd</code>(예: 1번 stdout)를 닫고, <code>old_fd</code>(로그 파일)를 복제하여 덮어씌움.</li>
</ul>
</li>
</ul>
<pre><code class="language-c">#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;

int main() {
    int fd = open(&quot;daemon.out&quot;, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror(&quot;open&quot;);
        return 1;
    }

    // 화면(1)으로 나갈 출력을 파일(fd)로 바꿔치기
    // 이제 1번 fd는 파일(fd)을 가리킴
    if (dup2(fd, STDOUT_FILENO) == -1) {
        perror(&quot;dup2&quot;);
        return 1;
    }

    // 원본 fd는 필요 없으니 닫음 (복제본이 1번에 살아있음)
    close(fd);

    // printf는 stdout(1번)에 쓰지만, 실제로는 파일에 저장됨
    printf(&quot;This message goes to the file, not the screen.\n&quot;);
    printf(&quot;Redirect success!\n&quot;);

    return 0;
}</code></pre>
<hr />
<h3 id="dup2old_fd-new_fd했을-떄-원본-fd를-닫아도-되는-이유">dup2(old_fd, new_fd)했을 떄 원본 fd를 닫아도 되는 이유?</h3>
<p><strong>&quot;커널 내부의 '실제 파일 객체'는 공유되고, '참조 카운트(Reference Count)'가 0이 될 때까지 사라지지 않기 때문입니다.&quot;</strong></p>
<p><code>dup2</code>는 파일 내용을 복사하는 것이 아니라, <strong>&quot;같은 파일을 가리키는 화살표(포인터) 하나를 더 만드는 것&quot;</strong>입니다.</p>
<h4 id="1-동작-원리-reference-counting">1. 동작 원리 (Reference Counting)</h4>
<p>리눅스 커널은 열린 파일을 관리할 때 <strong>참조 카운트(Reference Count)</strong> 방식을 사용합니다.</p>
<ol>
<li><strong><code>open()</code> 실행 시:</strong><ul>
<li>커널에 <code>struct file</code> 객체가 생성됩니다.</li>
<li><code>old_fd</code>가 이 객체를 가리킵니다.</li>
<li><strong>참조 카운트 = 1</strong></li>
</ul>
</li>
<li><strong><code>dup2(old_fd, new_fd)</code> 실행 시:</strong><ul>
<li><code>new_fd</code>도 <code>old_fd</code>가 가리키던 <strong>그 객체</strong>를 똑같이 가리키게 됩니다.</li>
<li>커널은 &quot;이 파일을 보는 녀석이 둘이네?&quot; 하고 카운트를 올립니다.</li>
<li><strong>참조 카운트 = 2</strong></li>
</ul>
</li>
<li><strong><code>close(old_fd)</code> 실행 시:</strong><ul>
<li><code>old_fd</code>와 파일 객체의 연결을 끊습니다.</li>
<li>참조 카운트를 1 내립니다.</li>
<li><strong>참조 카운트 = 1</strong></li>
<li><strong>결과:</strong> 카운트가 0이 아니므로 <strong>파일 객체는 소멸되지 않고 살아있습니다.</strong> <code>new_fd</code>를 통해 여전히 접근 가능합니다.</li>
</ul>
</li>
</ol>
<h4 id="2-비유-tv-리모컨">2. 비유: TV 리모컨</h4>
<ul>
<li><strong>파일:</strong> 거실에 있는 <strong>TV</strong>.</li>
<li><strong>old_fd:</strong> 원래 가지고 있던 <strong>리모컨 A</strong>.</li>
<li><strong>dup2:</strong> 리모컨 A를 복제해서 <strong>리모컨 B(new_fd)</strong>를 만듦.</li>
<li><strong>close(old_fd):</strong> <strong>리모컨 A를 버림.</strong></li>
<li><strong>결과:</strong> 리모컨 A를 버렸다고 해서 <strong>TV가 꺼지거나 리모컨 B가 작동을 안 하는 것은 아닙니다.</strong></li>
</ul>
<h4 id="3-왜-굳이-닫나요-리소스-관리">3. 왜 굳이 닫나요? (리소스 관리)</h4>
<p>안 닫아도 동작은 하지만, 닫는 것이 <strong>좋은 습관</strong>입니다.</p>
<ul>
<li><strong>낭비 방지:</strong> 프로세스가 가질 수 있는 fd의 개수(기본 1024개)는 제한되어 있습니다.</li>
<li><strong>깔끔함:</strong> <code>dup2</code>를 통해 <code>stdout(1번)</code>으로 복제했다면, 원본인 <code>fd(3번)</code>는 더 이상 필요 없으므로 닫아서 번호를 반환하는 것이 시스템 리소스 관리에 유리합니다.</li>
</ul>
<hr />
<h4 id="1-inode--dup2-">1. inode == dup2 ?</h4>
<p>관계가 있긴 하지만 <code>dup2</code>는 Inode보다 한 단계 위인 '오픈 파일 테이블'을 공유하게 만듦</p>
<p>엄밀히 말하면 <code>dup2</code>는 <strong>Inode를 직접 건드리는 것이 아니라, 중간 다리 역할인 'Open File Description(파일 구조체)'을 공유</strong>합니다. 물론 결과적으로는 <strong>같은 Inode</strong>를 가리키게 됩니다.
이 관계를 <strong>3단계 구조</strong>로 이해하는 것이 핵심입니다.</p>
<table>
<thead>
<tr>
<th><strong>단계</strong></th>
<th><strong>명칭</strong></th>
<th><strong>역할</strong></th>
<th><strong>dup2 시 동작</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>Level 1</strong></td>
<td><strong>FD Table</strong> (프로세스 전용)</td>
<td>사용자가 쓰는 번호표 (<code>int fd</code>)</td>
<td><strong>새 번호표 발급</strong> (예: 1번이 3번 복제)</td>
</tr>
<tr>
<td><strong>Level 2</strong></td>
<td><strong>Open File Table</strong> (커널 전역)</td>
<td><strong>현재 읽는 위치(Offset)</strong>, 모드(R/W), <strong>참조 카운트</strong></td>
<td><strong>기존 것을 공유함</strong> (새로 안 만듦!)</td>
</tr>
<tr>
<td><strong>Level 3</strong></td>
<td><strong>Inode Table</strong> (파일 시스템)</td>
<td>실제 파일 메타데이터, 데이터 블록 위치</td>
<td><strong>같은 놈을 가리킴</strong></td>
</tr>
</tbody></table>
<h4 id="2-dup2의-비밀-level-2를-공유한다">2. <code>dup2</code>의 비밀: &quot;Level 2를 공유한다&quot;</h4>
<p><code>dup2(old_fd, new_fd)</code>를 실행하면 다음과 같은 일이 벌어집니다.</p>
<ol>
<li><strong>Level 1 (FD):</strong> 서로 다른 번호 (<code>old_fd: 3</code>, <code>new_fd: 4</code>)를 가집니다.</li>
<li><strong>Level 2 (Open File):</strong> 두 FD가 <strong>하나의 구조체(<code>struct file</code>)</strong>를 동시에 가리킵니다.<ul>
<li><strong>중요:</strong> 따라서 <strong>파일 오프셋(Offset)도 공유</strong>됩니다.</li>
<li><code>fd 3</code>으로 읽어서 오프셋이 이동하면, <code>fd 4</code>도 이동된 위치부터 읽습니다.</li>
</ul>
</li>
<li><strong>Level 3 (Inode):</strong> 당연히 같은 Inode를 봅니다.</li>
</ol>
<h4 id="3-비교-open을-두-번-한-경우-vs-dup2">3. 비교: <code>open()</code>을 두 번 한 경우 vs <code>dup2()</code></h4>
<p>가장 많이 혼동하는 부분입니다.</p>
<ul>
<li><strong>Case A: <code>dup2</code> (복제)</strong><ul>
<li><strong>상황:</strong> <code>fd1 = open(...)</code>, <code>fd2 = dup(fd1)</code></li>
<li><strong>관계:</strong> FD는 다르지만 <strong>Level 2(오프셋)를 공유</strong>.</li>
<li><strong>Inode:</strong> 같음.</li>
<li><strong>특징:</strong> <code>fd1</code>에서 읽으면 <code>fd2</code>의 읽기 위치도 바뀜.</li>
</ul>
</li>
<li><strong>Case B: <code>open</code> (독립적 열기)</strong><ul>
<li><strong>상황:</strong> <code>fd1 = open(...)</code>, <code>fd2 = open(...)</code> (같은 파일)</li>
<li><strong>관계:</strong> FD 다르고, <strong>Level 2(오프셋)도 서로 다름 (독립적)</strong>.</li>
<li><strong>Inode:</strong> 같음 (물리적 파일은 하나니까).</li>
<li><strong>특징:</strong> <code>fd1</code>이 파일을 읽든 말든, <code>fd2</code>는 자기만의 위치(0)에서 시작함.</li>
</ul>
</li>
</ul>
<h4 id="4-결론">4. 결론</h4>
<p>&quot;원본 FD를 닫아도 되는 이유&quot;를 Inode 관점에서 다시 설명하면:</p>
<blockquote>
<p>dup2로 인해 Level 2 객체를 붙잡고 있는 녀석(참조 카운트)이 2명이 되었기 때문에,
원본 FD가 close 되어 하나가 떠나도, 복제된 FD가 Level 2 객체(와 그 아래 연결된 Inode)를 꽉 잡고 있어서 안전한 것입니다.</p>
</blockquote>