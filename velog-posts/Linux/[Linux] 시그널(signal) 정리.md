<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ad5e1d86-ce66-4dd3-86cb-574ccac4a839/image.png" /></p>
<p>계속 중복되는 내용이 있지만.. 수업 진도에 따라 겹치는 부분이 있어도 한번 씩 더 정리중입니다.</p>
<hr />
<h3 id="시그널">시그널</h3>
<p>프로세스에게 보내는 <code>긴급 문자 메시지(비동기 알림)</code>으로, 받으면 하던 일을 멈추고 즉시 확인(처리)해야 합니다.</p>
<hr />
<h3 id="1-시그널-definition">1. 시그널 Definition</h3>
<ul>
<li>비동기적(Asynchronous): 프로그램이 언제 받을지 예측할 수 없습니다. (예: 사용자가 갑자기 <code>Ctrl+C</code>를 누름).</li>
<li>소프트웨어 인터럽트: 하드웨어 인터럽트(타이머, 키보드)를 흉내 낸 소프트웨어적 메커니즘입니다.</li>
<li>IPC의 기본: 가장 원시적이지만 가장 빠른 프로세스 간 통신 수단입니다. (데이터를 담을 순 없고, &quot;사건 번호&quot;만 전달).</li>
</ul>
<h3 id="2-시그널-수명주기-lifecycle-3단계">2. 시그널 수명주기 (Lifecycle) 3단계</h3>
<ol>
<li>발생 (Generation):<ul>
<li>이벤트 발생 (예: <code>Ctrl+C</code>, <code>kill</code> 명령어, 0으로 나누기 연산 등).</li>
<li>송신자: 커널, 다른 프로세스, 또는 자기 자신.</li>
</ul>
</li>
<li>대기 (Pending):<ul>
<li>시그널이 생성되었으나 아직 프로세스에 전달되지 않은 상태.</li>
<li>프로세스가 해당 시그널을 블록(Block/Mask) 하고 있으면, 블록이 풀릴 때까지 커널 큐에 머무릅니다.</li>
</ul>
</li>
<li>전달 및 처리 (Delivery):<ul>
<li>커널이 프로세스를 깨우거나 실행 흐름을 가로채서 시그널을 넘겨줍니다.</li>
</ul>
</li>
</ol>
<h3 id="3-처리-방법-disposition">3. 처리 방법 (Disposition)</h3>
<p>개발자는 다음 3가지 중 하나를 선택하여 시그널에 대응합니다.</p>
<table>
<thead>
<tr>
<th>처리 방식</th>
<th>매크로 / 함수</th>
<th>설명</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td>무시 (Ignore)</td>
<td><code>SIG_IGN</code></td>
<td>&quot;그냥 무시해.&quot; 아무 일도 일어나지 않음.</td>
<td>SIGKILL, SIGSTOP은 무시 불가. (관리자의 통제권 보장)</td>
</tr>
<tr>
<td>기본 동작 (Default)</td>
<td><code>SIG_DFL</code></td>
<td>커널이 정한 기본 행동 수행.</td>
<td>대부분 종료(Terminate) 또는 코어 덤프(Core Dump).</td>
</tr>
<tr>
<td>포착 (Catch)</td>
<td><code>handler_func</code></td>
<td>&quot;내가 처리할게.&quot; 시그널 핸들러 함수 실행.</td>
<td>실행 중인 코드를 멈추고 핸들러로 점프 → 수행 후 복귀.</td>
</tr>
</tbody></table>
<h3 id="4-시그널-핸들러의-실행-흐름-context-jump">4. 시그널 핸들러의 실행 흐름 (Context Jump)</h3>
<p>일반 함수 호출과 다르게, 커널이 강제로 실행 흐름을 바꿉니다.</p>
<ol>
<li>Main 코드 실행 중: <code>i = i + 1;</code> 수행 중.</li>
<li>시그널 도착: 커널이 개입.</li>
<li>Context 저장: 현재 레지스터와 스택 상태를 저장.</li>
<li>Handler 실행: <code>signal_handler()</code> 함수로 강제 점프.</li>
<li>Return: 핸들러가 끝나면(<code>return</code>), 저장해둔 위치(<code>i = i + 1</code> 다음)로 복귀하여 계속 실행.</li>
</ol>
<h3 id="5-주요-시그널-목록">5. 주요 시그널 목록</h3>
<table>
<thead>
<tr>
<th>이름</th>
<th>번호</th>
<th>기본 동작</th>
<th>발생 상황</th>
</tr>
</thead>
<tbody><tr>
<td>SIGINT</td>
<td>2</td>
<td>종료</td>
<td>키보드 <code>Ctrl + C</code> 입력 시.</td>
</tr>
<tr>
<td>SIGQUIT</td>
<td>3</td>
<td>코어 덤프</td>
<td>키보드 <code>Ctrl + \</code> 입력 시.</td>
</tr>
<tr>
<td>SIGKILL</td>
<td>9</td>
<td>강제 종료</td>
<td><code>kill -9</code>. (포착, 무시, 블록 불가)</td>
</tr>
<tr>
<td>SIGSEGV</td>
<td>11</td>
<td>코어 덤프</td>
<td>잘못된 메모리 접근 (Segmentation Fault).</td>
</tr>
<tr>
<td>SIGTERM</td>
<td>15</td>
<td>종료</td>
<td><code>kill</code> 명령의 기본값. (정상 종료 요청).</td>
</tr>
<tr>
<td>SIGSTOP</td>
<td>19</td>
<td>정지</td>
<td>실행 일시 정지. (포착, 무시, 블록 불가)</td>
</tr>
<tr>
<td>SIGCHLD</td>
<td>17</td>
<td>무시</td>
<td>자식 프로세스가 종료되거나 멈춤.</td>
</tr>
</tbody></table>
<hr />
<p><code>+ 추가)</code></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6cfaeea9-2177-4309-a757-3bb648663b8b/image.png" /></p>
<h3 id="6-코드-예제-signal-함수-사용">6. 코드 예제 (<code>signal</code> 함수 사용)</h3>
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
<p>시그널 핸들러는 비동기적으로 호출되므로, 핸들러 내부에서 <code>printf</code>, <code>malloc</code> 같은 일반 라이브러리 함수를 쓰는 것은 위험합니다. (이 함수들이 실행되는 도중에 시그널이 와서 또 호출하면 꼬일 수 있음).</p>
<hr />
<p>원칙적으로는, 핸들러 내부에서는 전역 변수(플래그)만 1로 세팅하고 최대한 빨리 빠져나오는 것이 정석입니다.</p>
<blockquote>
<p>핸들러는 <code>깃발(Flag)</code>만 올리고, 뒤처리는 <code>메인 루프</code>가 담당한다.</p>
</blockquote>
<p>시그널 핸들러 내부에서 <code>printf</code> 같은 무거운 함수를 제거하고, <code>volatile sig_atomic_t</code> 타입을 사용하여 비동기 신호 안전(Async-Signal-Safe) 원칙을 지키는 코드로 재작성된 코드입니다.</p>
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
<li>상황: 메인 함수가 <code>printf</code>를 호출해서 내부적으로 락(Lock)을 걸고 있는데, 시그널이 발생해서 핸들러가 또 <code>printf</code>를 호출하면?</li>
<li>결과: 핸들러는 메인의 락이 풀리길 기다리고, 메인은 핸들러가 끝나길 기다리는 교착 상태(Deadlock)에 빠질 수 있습니다.</li>
</ul>
<h3 id="2-volatile-키워드">2. <code>volatile</code> 키워드</h3>
<ul>
<li>이유: 컴파일러는 <code>while(1)</code> 내부에서 <code>g_exit_flag</code>를 건드리는 코드가 없으면, 성능을 위해 이 값을 레지스터에 캐싱(저장)해버립니다.</li>
<li>결과: 핸들러가 메모리상의 값을 <code>1</code>로 바꿔도, CPU는 레지스터의 <code>0</code>만 계속 보고 있어서 루프가 안 끝나는 버그가 발생합니다. <code>volatile</code>은 &quot;캐싱하지 말고 무조건 메모리에서 다시 읽어!&quot;라고 지시합니다.</li>
</ul>
<h3 id="3-sig_atomic_t-타입">3. <code>sig_atomic_t</code> 타입</h3>
<ul>
<li>이유: <code>int</code>가 32비트인데 8비트 CPU에서 돌린다면? 값을 쓰는 도중(상위 16비트 쓰고 하위 16비트 쓰려는 찰나)에 읽어가면 엉뚱한 값이 될 수 있습니다.</li>
<li>결과: 이 타입은 시스템에서 원자적(Atomic) 접근을 보장하는 가장 안전한 정수 타입입니다.</li>
</ul>
<hr />
<h3 id="deadlock-코드">Deadlock 코드</h3>
<p>&quot;시그널 핸들러에서 <code>printf</code> 쓰면 위험하다&quot;는 것을 증명하는 교착 상태(Deadlock) 타이밍이 맞으면 프로그램이 그대로 멈춰버립니다.</p>
<h3 id="예제-시그널-핸들러-데드락-the-unsafe-printf-trap">예제: 시그널 핸들러 데드락 (The &quot;Unsafe printf&quot; Trap)</h3>
<p>이 코드는 <code>printf</code>가 내부적으로 사용하는 락(Lock) 때문에 죽습니다.</p>
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
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/87d57a8f-d53c-4c46-9dce-478629c992bd/image.png" /></p>
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
<p>시그널 핸들러 안에서는 락을 쓰지 않는 Async-Signal-Safe 함수만 써야 합니다. <code>printf</code> 대신 <code>write</code>를 써야합니다.</p>
<pre><code class="language-c">// 안전한 버전
void handler(int signo) {
    char *msg = &quot;Handler: Safe Write!\n&quot;;
    write(STDOUT_FILENO, msg, strlen(msg)); // 락을 안 씀
}</code></pre>
<hr />
<h3 id="시그널집합signalset과-집합-제어">시그널집합(Signalset)과 집합 제어</h3>
<p>&quot;여러 시그널을 비트 마스크(<code>sigset_t</code>)로 묶어, 특정 구간에서 수신을 잠시 막거나(Block) 푸는(Unblock) 기술.</p>
<hr />
<h3 id="1-시그널-집합-sigset_t">1. 시그널 집합 (<code>sigset_t</code>)</h3>
<p>리눅스는 64개의 시그널을 다루기 위해 <code>unsigned long</code> 배열 비트 마스크인 <code>sigset_t</code> 타입을 사용합니다. 직접 비트 연산을 하지 않고 전용 매크로 함수를 사용합니다.</p>
<h3 id="주요-조작-함수">주요 조작 함수</h3>
<ul>
<li><code>sigemptyset(sigset_t *set)</code>: 집합 비우기 (모든 비트 0).</li>
<li><code>sigfillset(sigset_t *set)</code>: 모든 시그널 포함 (모든 비트 1).</li>
<li><code>sigaddset(sigset_t *set, int signum)</code>: 특정 시그널 추가.</li>
<li><code>sigdelset(sigset_t *set, int signum)</code>: 특정 시그널 제거.</li>
<li><code>sigismember(sigset_t *set, int signum)</code>: 포함 여부 확인 (True/False).</li>
</ul>
<hr />
<h3 id="2-시그널-제어-maskingblocking">2. 시그널 제어 (Masking/Blocking)</h3>
<p>시그널 집합을 커널에 등록하여 &quot;이 구간에서는 이 시그널들을 잠시 보류해줘&quot;라고 요청하는 것입니다.</p>
<h4 id="시스템-콜-sigprocmask-사용-시">시스템 콜 sigprocmask 사용 시</h4>
<pre><code class="language-cpp">#include &lt;signal.h&gt;
int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);</code></pre>
<hr />
<table>
<thead>
<tr>
<th>how 옵션</th>
<th>동작 설명</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td><code>SIG_BLOCK</code></td>
<td>현재 마스크 + <code>set</code> (합집합)</td>
<td>기존 차단 목록에 추가</td>
</tr>
<tr>
<td><code>SIG_UNBLOCK</code></td>
<td>현재 마스크 - <code>set</code> (차집합)</td>
<td>차단 목록에서 해제</td>
</tr>
<tr>
<td><code>SIG_SETMASK</code></td>
<td>현재 마스크 = <code>set</code> (대입)</td>
<td>아예 새 목록으로 덮어쓰기</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-예제-critical-section-보호">3. 예제: Critical Section 보호</h3>
<p>중요한 데이터를 쓰고 있을 때 <code>SIGINT(Ctrl+C)</code>가 들어와도 즉시 종료되지 않고, 작업이 끝난 후에 처리되도록 합니다.</p>
<pre><code class="language-cpp">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;

int main() {
    sigset_t new_set, old_set;

    // 1. 집합 초기화 및 SIGINT(2번) 추가
    sigemptyset(&amp;new_set);
    sigaddset(&amp;new_set, SIGINT);

    printf(&quot;[Start] 중요 작업 시작 전 (Ctrl+C 가능)\n&quot;);
    sleep(3);

    // 2. 블록 설정 (이제부터 SIGINT는 Pending 큐에 쌓이고 전달 안 됨)
    // old_set에 이전 상태를 백업해둠
    sigprocmask(SIG_BLOCK, &amp;new_set, &amp;old_set);

    printf(&quot;\n[Critical Section] 중요 데이터 기록 중... (Ctrl+C 눌러도 안 죽음)\n&quot;);
    for(int i=0; i&lt;5; i++) {
        printf(&quot;Writing data... %d/5\n&quot;, i+1);
        sleep(1); 
    }
    printf(&quot;[Critical Section] 완료.\n&quot;);

    // 3. 블록 해제 (백업해둔 상태로 복구)
    // 이 시점에 아까 눌렀던 Ctrl+C가 있다면 즉시 배달되어 프로세스 종료됨
    sigprocmask(SIG_SETMASK, &amp;old_set, NULL);

    printf(&quot;\n[End] 작업 끝. (여기까지 출력되면 Ctrl+C 안 누른 것)\n&quot;);
    sleep(3);

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/34629665-5f66-4fe6-abb7-672f3280f9d6/image.png" /></p>
<h3 id="실행-시나리오">실행 시나리오</h3>
<ol>
<li>&quot;중요 데이터 기록 중...&quot; 일 때 <code>Ctrl+C</code>를 누름.</li>
<li>프로세스가 종료되지 않고 <code>Writing data...</code>를 끝까지 출력함.</li>
<li>블록이 해제되는 순간(<code>sigprocmask</code> 복구 직후), 아까 참았던 <code>SIGINT</code>가 도착하여 즉시 종료됨. (마지막 <code>[End]</code> 메시지는 출력 안 됨).</li>
</ol>
<hr />
<h3 id="개별-시그널-확인-방법">개별 시그널 확인 방법</h3>
<p>시그널이 64 기존 sig  8bit 구분해서  프린트하게, 왼쪽이 낮은 비트</p>
<p>예) 00000000 00100000 00000000 00000000  00000000 00000000 00000000 00000000</p>
<pre><code class="language-c">#define _POSIX_C_SOURCE 200809L //IntelliSense (코드 분석기)의 오탐으로 인해 추가
#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;


void printf_SIG(sigset_t sig){
    int count=1;
    for (int i = 1; i &lt;= 64; i++)
    {
        if(sigismember(&amp;sig, i)==1){
            printf(&quot;1&quot;);
        }else printf(&quot;0&quot;);
        if((count%8)==0)printf(&quot; &quot;);
        count++;
    }
    printf(&quot;\n&quot;);

}


int main() {
    sigset_t new_set, old_set;

    // 1. 집합 초기화 및 SIGINT(2번) 추가
    printf_SIG(old_set);

    sigemptyset(&amp;new_set);    
    sigaddset(&amp;new_set, SIGINT);
    printf_SIG(new_set);

    printf(&quot;[Start] 중요 작업 시작 전 (Ctrl+C 가능)\n&quot;);
    sleep(3);

    printf(&quot;[Start] 마스킹처리됨 (Ctrl+C 안됨)\n&quot;);
    sigprocmask(0, NULL,&amp;old_set);
    printf_SIG(old_set);

    // 2. 블록 설정 (이제부터 SIGINT는 Pending 큐에 쌓이고 전달 안 됨)
    // old_set에 이전 상태를 백업해둠
    sigprocmask(SIG_BLOCK, &amp;new_set, &amp;old_set); //old_set =&gt; 0

    printf_SIG(old_set);

    sigprocmask(0, NULL,&amp;old_set); //=&gt; 1

    printf_SIG(old_set);

    printf(&quot;\n[Critical Section] 중요 데이터 기록 중... (Ctrl+C 눌러도 안 죽음)\n&quot;);
    for(int i=0; i&lt;5; i++) {
        printf(&quot;Writing data... %d/5\n&quot;, i+1);
        sleep(1); 
    }
    printf(&quot;[Critical Section] 완료.\n&quot;);

    // 3. 블록 해제 (백업해둔 상태로 복구)
    // 이 시점에 아까 눌렀던 Ctrl+C가 있다면 즉시 배달되어 프로세스 종료됨
    sigprocmask(SIG_SETMASK, &amp;old_set, NULL);
    printf_SIG(old_set);
    printf(&quot;\n[End] 작업 끝. (여기까지 출력되면 Ctrl+C 안 누른 것)\n&quot;);
    sleep(3);

    return 0;
}</code></pre>
<p>위 코드 한번 더 정리할 것</p>
<hr />
<h3 id="시그널을-보낸-pid를-통해서-어느-사용자uid가-왜-보내었는지-확인-하는-프로그램">시그널을 보낸 pid를 통해서 어느 사용자(UID)가 왜? 보내었는지 확인 하는 프로그램</h3>
<pre><code class="language-c">#define _POSIX_C_SOURCE 200809L //IntelliSense (코드 분석기)의 오탐으로 인해 추가
#include &lt;stdio.h&gt;      // printf()
#include &lt;stdlib.h&gt;     // exit()
#include &lt;unistd.h&gt;     // sleep(), getpid()
#include &lt;signal.h&gt;    // sigaction, siginfo_t, SI_USER, SI_KERNEL
#include &lt;string.h&gt;

void detailed_handler(int sig, siginfo_t *info, void *ucontext) {
    printf(&quot;\n[Signal Received] 번호: %d\n&quot;, sig);

    // 1. 누가 보냈는가?
    printf(&quot; - 보낸 프로세스 PID: %d\n&quot;, info-&gt;si_pid);
    printf(&quot; - 보낸 사용자 UID: %u\n&quot;, info-&gt;si_uid);

    // 2. 왜 보냈는가? (si_code 분석)
    printf(&quot; - 발생 원인 코드: %d &quot;, info-&gt;si_code);

    if (info-&gt;si_code == SI_USER) {
        printf(&quot;(사용자가 kill이나 raise로 직접 전송)\n&quot;);
    } else if (info-&gt;si_code == SI_KERNEL) {
        printf(&quot;(커널에서 전송)\n&quot;);
    } else {
        printf(&quot;(기타 사유)\n&quot;);
    }
}

int main() {
    struct sigaction sa;

    // 구조체 초기화
    sa.sa_sigaction = detailed_handler; // 상세 정보를 받는 핸들러 연결
    sigemptyset(&amp;sa.sa_mask);           // 핸들러 실행 중 블록할 시그널 없음
    sa.sa_flags = SA_SIGINFO;           // 상세 정보 사용 플래그 설정

    // SIGINT(Ctrl+C)에 대해 sigaction 설정
    if (sigaction(SIGINT, &amp;sa, NULL) == -1) {
        perror(&quot;sigaction&quot;);
        exit(1);
    }

    printf(&quot;현재 프로세스 PID: %d\n&quot;, getpid());
    printf(&quot;Ctrl+C를 누르거나, 다른 터미널에서 'kill -2 %d'를 입력하세요.\n&quot;, getpid());

    // 시그널 대기
    while (1) {
        sleep(1);
    }

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/704bea5c-5197-4764-801a-1493a976e42b/image.png" /></p>
<hr />
<blockquote>
<p>_ 썸넬 reference_  : <a href="https://blockdmask.tistory.com/23">https://blockdmask.tistory.com/23</a></p>
</blockquote>