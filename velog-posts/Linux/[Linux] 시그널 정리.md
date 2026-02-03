<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ad5e1d86-ce66-4dd3-86cb-574ccac4a839/image.png" /></p>
<p>계속 중복되는 내용이 있지만.. 수업 진도에 따라 겹치는 부분이 있어도 한번 씩 더 정리중입니다.</p>
<hr />
<h3 id="시그널">시그널</h3>
<p>프로세스에게 보내는 <code>긴급 문자 메시지(비동기 알림)</code>으로, 받으면 하던 일을 멈추고 즉시 확인(처리)해야 합니다.</p>
<hr />
<h3 id="1-시그널-definition">1. 시그널 Definition</h3>
<ul>
<li><strong>비동기적(Asynchronous):</strong> 프로그램이 언제 받을지 예측할 수 없습니다. (예: 사용자가 갑자기 <code>Ctrl+C</code>를 누름).</li>
<li><strong>소프트웨어 인터럽트:</strong> 하드웨어 인터럽트(타이머, 키보드)를 흉내 낸 소프트웨어적 메커니즘입니다.</li>
<li><strong>IPC의 기본:</strong> 가장 원시적이지만 가장 빠른 프로세스 간 통신 수단입니다. (데이터를 담을 순 없고, &quot;사건 번호&quot;만 전달).</li>
</ul>
<h3 id="2-시그널-수명주기-lifecycle-3단계">2. 시그널 수명주기 (Lifecycle) 3단계</h3>
<ol>
<li><strong>발생 (Generation):</strong><ul>
<li>이벤트 발생 (예: <code>Ctrl+C</code>, <code>kill</code> 명령어, 0으로 나누기 연산 등).</li>
<li>송신자: 커널, 다른 프로세스, 또는 자기 자신.</li>
</ul>
</li>
<li><strong>대기 (Pending):</strong><ul>
<li>시그널이 생성되었으나 아직 프로세스에 전달되지 않은 상태.</li>
<li>프로세스가 해당 시그널을 <strong>블록(Block/Mask)</strong> 하고 있으면, 블록이 풀릴 때까지 커널 큐에 머무릅니다.</li>
</ul>
</li>
<li><strong>전달 및 처리 (Delivery):</strong><ul>
<li>커널이 프로세스를 깨우거나 실행 흐름을 가로채서 시그널을 넘겨줍니다.</li>
</ul>
</li>
</ol>
<h3 id="3-처리-방법-disposition">3. 처리 방법 (Disposition)</h3>
<p>개발자는 다음 3가지 중 하나를 선택하여 시그널에 대응합니다.</p>
<table>
<thead>
<tr>
<th><strong>처리 방식</strong></th>
<th><strong>매크로 / 함수</strong></th>
<th><strong>설명</strong></th>
<th><strong>비고</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>무시 (Ignore)</strong></td>
<td><code>SIG_IGN</code></td>
<td>&quot;그냥 무시해.&quot; 아무 일도 일어나지 않음.</td>
<td><strong>SIGKILL, SIGSTOP은 무시 불가.</strong> (관리자의 통제권 보장)</td>
</tr>
<tr>
<td><strong>기본 동작 (Default)</strong></td>
<td><code>SIG_DFL</code></td>
<td>커널이 정한 기본 행동 수행.</td>
<td>대부분 <strong>종료(Terminate)</strong> 또는 코어 덤프(Core Dump).</td>
</tr>
<tr>
<td><strong>포착 (Catch)</strong></td>
<td><code>handler_func</code></td>
<td>&quot;내가 처리할게.&quot; <strong>시그널 핸들러</strong> 함수 실행.</td>
<td>실행 중인 코드를 멈추고 핸들러로 점프 → 수행 후 복귀.</td>
</tr>
</tbody></table>
<h3 id="4-시그널-핸들러의-실행-흐름-context-jump">4. 시그널 핸들러의 실행 흐름 (Context Jump)</h3>
<p>일반 함수 호출과 다르게, 커널이 강제로 실행 흐름을 바꿉니다.</p>
<ol>
<li><strong>Main 코드 실행 중:</strong> <code>i = i + 1;</code> 수행 중.</li>
<li><strong>시그널 도착:</strong> 커널이 개입.</li>
<li><strong>Context 저장:</strong> 현재 레지스터와 스택 상태를 저장.</li>
<li><strong>Handler 실행:</strong> <code>signal_handler()</code> 함수로 강제 점프.</li>
<li><strong>Return:</strong> 핸들러가 끝나면(<code>return</code>), 저장해둔 위치(<code>i = i + 1</code> 다음)로 복귀하여 계속 실행.</li>
</ol>
<h3 id="5-주요-시그널-목록">5. 주요 시그널 목록</h3>
<table>
<thead>
<tr>
<th><strong>이름</strong></th>
<th><strong>번호</strong></th>
<th><strong>기본 동작</strong></th>
<th><strong>발생 상황</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>SIGINT</strong></td>
<td>2</td>
<td>종료</td>
<td>키보드 <code>Ctrl + C</code> 입력 시.</td>
</tr>
<tr>
<td><strong>SIGQUIT</strong></td>
<td>3</td>
<td>코어 덤프</td>
<td>키보드 <code>Ctrl + \</code> 입력 시.</td>
</tr>
<tr>
<td><strong>SIGKILL</strong></td>
<td>9</td>
<td><strong>강제 종료</strong></td>
<td><code>kill -9</code>. <strong>(포착, 무시, 블록 불가)</strong></td>
</tr>
<tr>
<td><strong>SIGSEGV</strong></td>
<td>11</td>
<td>코어 덤프</td>
<td>잘못된 메모리 접근 (Segmentation Fault).</td>
</tr>
<tr>
<td><strong>SIGTERM</strong></td>
<td>15</td>
<td>종료</td>
<td><code>kill</code> 명령의 기본값. (정상 종료 요청).</td>
</tr>
<tr>
<td><strong>SIGSTOP</strong></td>
<td>19</td>
<td>정지</td>
<td>실행 일시 정지. <strong>(포착, 무시, 블록 불가)</strong></td>
</tr>
<tr>
<td><strong>SIGCHLD</strong></td>
<td>17</td>
<td>무시</td>
<td>자식 프로세스가 종료되거나 멈춤.</td>
</tr>
</tbody></table>
<h3 id="6-코드-예제-signal-함수-사용">6. 코드 예제 (<code>signal</code> 함수 사용)</h3>
<p>C</p>
<pre><code class="language-cpp">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;
#include &lt;stdlib.h&gt;

// 시그널 핸들러 함수 (User defined)
void my_handler(int signo) {
    printf(&quot;\n[Signal] %d번 시그널을 받았습니다! 죽지 않아요.\n&quot;, signo);
    // 보통 여기서 자원 정리나 플래그 설정을 함
}

int main() {
    // 1. 핸들러 등록 (SIGINT 발생 시 my_handler 실행)
    if (signal(SIGINT, my_handler) == SIG_ERR) {
        perror(&quot;signal error&quot;);
        exit(1);
    }

    // 2. SIGQUIT는 무시하도록 설정 (Ctrl + \)
    signal(SIGQUIT, SIG_IGN);

    printf(&quot;Running... (Ctrl+C를 눌러보세요. Ctrl+\\는 무시됩니다.)\n&quot;);

    while (1) {
        printf(&quot;.&quot;);
        fflush(stdout);
        sleep(1);
    }
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f9940b78-9d56-4686-bc15-b63640987f2e/image.png" /></p>
<p>종료를 위해선 다른 터미널을 열어 아래 명령어 입력</p>
<pre><code class="language-bash">ps aux | grep signal_1
kill -9 [Process ID]</code></pre>
<hr />
<h3 id="팁-reentrancy-재진입성">팁: Reentrancy (재진입성)</h3>
<p>시그널 핸들러는 비동기적으로 호출되므로, 핸들러 내부에서 <strong><code>printf</code>, <code>malloc</code> 같은 일반 라이브러리 함수를 쓰는 것은 위험</strong>합니다. (이 함수들이 실행되는 도중에 시그널이 와서 또 호출하면 꼬일 수 있음).</p>
<hr />
<p>원칙적으로는, 핸들러 내부에서는 전역 변수(플래그)만 1로 세팅하고 최대한 빨리 빠져나오는 것이 정석입니다.</p>
<blockquote>
<p>핸들러는 <code>깃발(Flag)</code>만 올리고, 뒤처리는 <code>메인 루프</code>가 담당한다.</p>
</blockquote>
<p>시그널 핸들러 내부에서 <code>printf</code> 같은 무거운 함수를 제거하고, <code>volatile sig_atomic_t</code> 타입을 사용하여 <strong>비동기 신호 안전(Async-Signal-Safe)</strong> 원칙을 지키는 코드로 재작성된 코드입니다.</p>
<h3 id="✅-안전한-시그널-처리-패턴-코드">✅ 안전한 시그널 처리 패턴 코드</h3>
<pre><code class="language-cpp">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;
#include &lt;stdlib.h&gt;

/* * [핵심 1] volatile sig_atomic_t
 * - volatile: 컴파일러가 이 변수를 최적화(캐싱)하지 못하게 막음 (언제든 값이 변할 수 있음을 알림).
 * - sig_atomic_t: CPU가 한 번의 명령으로 읽고 쓸 수 있음을 보장하는 정수 타입 (쪼개지지 않음).
 */
volatile sig_atomic_t g_exit_flag = 0;

// 시그널 핸들러: 최대한 짧고 단순하게!
void my_handler(int signo) {
    // 여기서는 복잡한 작업(printf, malloc 등) 금지!
    // 오직 플래그 값만 변경하고 즉시 리턴함.
    g_exit_flag = 1;
}

int main() {
    // 핸들러 등록
    if (signal(SIGINT, my_handler) == SIG_ERR) {
        perror(&quot;signal error&quot;);
        exit(1);
    }

    printf(&quot;프로그램 실행 중... (Ctrl+C를 누르면 안전하게 종료합니다)\n&quot;);

    while (1) {
        // [핵심 2] 메인 루프에서 플래그 검사
        if (g_exit_flag == 1) {
            printf(&quot;\n[Main] 종료 플래그 감지! 자원을 정리하고 종료합니다.\n&quot;);
            break; // 루프 탈출
        }

        // 평소 작업 수행
        printf(&quot;.&quot;);
        fflush(stdout);

        // sleep 중에 시그널이 오면 sleep은 즉시 깨어나고(잔여 시간 반환), 
        // 핸들러 실행 후 다음 라인으로 넘어감.
        sleep(1); 
    }

    printf(&quot;Bye Bye!\n&quot;);
    return 0;
}</code></pre>
<hr />
<h3 id="1-printf-제거-이유-reentrancy">1. <code>printf</code> 제거 이유 (Reentrancy)</h3>
<ul>
<li><strong>상황:</strong> 메인 함수가 <code>printf</code>를 호출해서 내부적으로 락(Lock)을 걸고 있는데, 시그널이 발생해서 핸들러가 또 <code>printf</code>를 호출하면?</li>
<li><strong>결과:</strong> 핸들러는 메인의 락이 풀리길 기다리고, 메인은 핸들러가 끝나길 기다리는 <strong>교착 상태(Deadlock)</strong>에 빠질 수 있습니다.</li>
</ul>
<h3 id="2-volatile-키워드">2. <code>volatile</code> 키워드</h3>
<ul>
<li><strong>이유:</strong> 컴파일러는 <code>while(1)</code> 내부에서 <code>g_exit_flag</code>를 건드리는 코드가 없으면, 성능을 위해 이 값을 <strong>레지스터에 캐싱(저장)</strong>해버립니다.</li>
<li><strong>결과:</strong> 핸들러가 메모리상의 값을 <code>1</code>로 바꿔도, CPU는 레지스터의 <code>0</code>만 계속 보고 있어서 루프가 안 끝나는 버그가 발생합니다. <code>volatile</code>은 &quot;캐싱하지 말고 무조건 메모리에서 다시 읽어!&quot;라고 지시합니다.</li>
</ul>
<h3 id="3-sig_atomic_t-타입">3. <code>sig_atomic_t</code> 타입</h3>
<ul>
<li><strong>이유:</strong> <code>int</code>가 32비트인데 8비트 CPU에서 돌린다면? 값을 쓰는 도중(상위 16비트 쓰고 하위 16비트 쓰려는 찰나)에 읽어가면 엉뚱한 값이 될 수 있습니다.</li>
<li><strong>결과:</strong> 이 타입은 시스템에서 <strong>원자적(Atomic) 접근</strong>을 보장하는 가장 안전한 정수 타입입니다.</li>
</ul>
<hr />
<h3 id="deadlock-코드">Deadlock 코드</h3>
<p><strong>&quot;시그널 핸들러에서 <code>printf</code> 쓰면 위험하다&quot;</strong>는 것을 증명하는 <strong>교착 상태(Deadlock)</strong> 타이밍이 맞으면 프로그램이 그대로 멈춰버립니다.</p>
<h3 id="예제-시그널-핸들러-데드락-the-unsafe-printf-trap">예제: 시그널 핸들러 데드락 (The &quot;Unsafe printf&quot; Trap)</h3>
<p>이 코드는 <code>printf</code>가 내부적으로 사용하는 <strong>락(Lock)</strong> 때문에 죽습니다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;signal.h&gt;
#include &lt;unistd.h&gt;
#include &lt;pthread.h&gt; // 뮤텍스 사용

// 1. 자원을 보호하는 자물쇠 (Mutex)
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void handler(int signo) {
    printf(&quot;[Handler] 시그널 수신! 락 획득 시도 중...\n&quot;);

    // 3. 여기서 멈춤 (DEADLOCK)
    // Main이 이미 락을 가지고 있는데, Handler가 끝나야 Main이 락을 품.
    // 하지만 Handler는 락을 얻어야 끝남. -&gt; 무한 대기
    pthread_mutex_lock(&amp;lock); 

    printf(&quot;[Handler] 락 획득 성공! (이 메시지는 절대 안 보임)\n&quot;);
    pthread_mutex_unlock(&amp;lock);
}

int main() {
    signal(SIGINT, handler);

    printf(&quot;[Main] 시작: 락을 겁니다.\n&quot;);

    // 1. 메인이 락을 잠금
    pthread_mutex_lock(&amp;lock);

    printf(&quot;[Main] 락 획득함. 이제 시그널을 스스로 보냄 (자살골).\n&quot;);

    // 2. 락을 쥔 상태에서 시그널 발생 (Ctrl+C를 코드로 누름)
    // 이 순간 하던 일을 멈추고 handler로 점프함
    raise(SIGINT); 

    // 4. 핸들러가 끝나야 여기로 돌아오는데, 핸들러가 멈춰서 못 돌아옴.
    printf(&quot;[Main] 락 해제 (이 메시지도 절대 안 보임)\n&quot;);
    pthread_mutex_unlock(&amp;lock);

    return 0;
}</code></pre>
<hr />
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;signal.h&gt;
#include &lt;unistd.h&gt;

// 핸들러에서 메모리 할당 시도 (절대 금지 행위)
void handler(int signo) {
    // 여기서 malloc이 메인이 잡고 있는 '힙 락'을 기다리다 멈춤
    void *ptr = malloc(1024); 
    free(ptr);
}

int main() {
    signal(SIGINT, handler);

    printf(&quot;Running... (이 코드는 곧 멈춥니다)\n&quot;);

    // 자식 프로세스가 시그널 난사
    pid_t pid = getpid();
    if (fork() == 0) {
        while(1) {
            kill(pid, SIGINT);
            usleep(100); // 0.1ms 간격 폭격
        }
    }

    // 메인 루프: 쉴 새 없이 메모리 할당/해제 반복 (락을 계속 잡았다 풀었다 함)
    while(1) {
        void *p = malloc(1024);
        // [데드락 포인트] 
        // malloc이 내부 락을 잡고, 아직 리턴하기 전에 시그널이 오면 -&gt; 사망
        free(p);
    }
    return 0;
}</code></pre>
<p>위코드는 데드락에 안들어 갑니다. 확률적인 이유로 시그널 핸들러 안에서는 절대 뮤텍스(Lock)를 쓰거나, 락을 쓰는 함수(printf, malloc 등)를 호출하면 안 됩니다.</p>
<h3 id="해결책">해결책</h3>
<p>시그널 핸들러 안에서는 락을 쓰지 않는 <strong>Async-Signal-Safe</strong> 함수만 써야 합니다. <code>printf</code> 대신 <strong><code>write</code></strong>를 써야합니다.</p>
<pre><code class="language-c">// 안전한 버전
void handler(int signo) {
    char *msg = &quot;Handler: Safe Write!\n&quot;;
    write(STDOUT_FILENO, msg, strlen(msg)); // 락을 안 씀
}</code></pre>