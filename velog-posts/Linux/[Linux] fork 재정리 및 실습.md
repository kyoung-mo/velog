<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f5850036-401b-4890-a259-fafee7c35edd/image.png" /></p>
<hr />
<h3 id="1-fork란-무엇인가">1. fork()란 무엇인가?</h3>
<blockquote>
<p><code>fork()</code> : 프로세스 생성 시 사용하는 함수이다.</p>
</blockquote>
<p>기존 프로세스(부모)를 복제하여 새로운 프로세스(자식)를 만듭니다. fork 사용을 위해서는 <code>&lt;unistd.h&gt;</code> 를 include 해야 합니다. fork 함수는 <code>unistd.h</code> 파일에 system call로 정의되어 있습니다. 그리고 fork 함수 호출 이후 코드부터 각자의 메모리를 사용하여 실행됩니다.</p>
<hr />
<h4 id="1-1-메모리-복제">1-1) 메모리 복제</h4>
<ul>
<li>코드 영역(text): 읽기 전용이므로 실제로는 공유 (복사 X)</li>
<li>데이터 영역(data, bss), 힙(heap), 스택(stack): COW(Copy On Write) 기법 사용</li>
</ul>
<p>처음에는 페이지를 공유하다가, 수정이 발생할 때 실제로 복사합니다.</p>
<h4 id="1-2-반환값">1-2) 반환값</h4>
<ul>
<li>부모 프로세스: 자식의 PID 반환</li>
<li>자식 프로세스: 0 반환</li>
</ul>
<h4 id="1-3-파일-디스크립터">1-3) 파일 디스크립터</h4>
<ul>
<li>파일 디스크립터 번호가 복사됨</li>
<li>부모/자식 모두 같은 파일 테이블 엔트리를 가리킴</li>
</ul>
<p>따라서 파일 오프셋(lseek 위치), 파일 상태 플래그 등을 공유</p>
<h4 id="1-4-자식이-상속받는-것">1-4) 자식이 상속받는 것</h4>
<ul>
<li>프로세스 그룹 ID, 세션 ID</li>
<li>Signal handler 설정</li>
<li>umask, nice 값, 리소스 제한</li>
<li>현재 작업 디렉토리, 루트 디렉토리</li>
<li>환경 변수</li>
</ul>
<h4 id="1-5-자식이-상속받지-않는-것">1-5) 자식이 상속받지 않는 것</h4>
<ul>
<li>Pending Signal</li>
<li>File Lock (fcntl)</li>
<li>타이머 (alarm, setitimer)</li>
<li>비동기 I/O 컨텍스트</li>
<li>디렉토리 스트림 위치 (opendir)</li>
<li>mmap으로 생성한 메모리 lock</li>
</ul>
<h4 id="1-6-주의사항">1-6) 주의사항</h4>
<ul>
<li>멀티스레드 프로세스를 fork하면, 자식은 단일 스레드가 됨 (fork를 호출한 스레드만 복제)</li>
</ul>
<hr />
<h3 id="2-fork-예제">2. fork() 예제</h3>
<h3 id="2-1-병렬-작업-처리-parallel-processing">2-1) 병렬 작업 처리 (Parallel Processing)</h3>
<p><strong>목적:</strong> 하나의 작업을 둘로 나누어 동시에 처리 (속도 향상).
<strong>시나리오:</strong> 부모는 데이터를 수집하고, 자식은 수집된 데이터를 DB에 기록함.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // [Child] 무거운 연산 담당
        printf(&quot;[Child] 데이터 분석 중... (PID: %d)\n&quot;, getpid());
        sleep(2); // 연산 시뮬레이션
        printf(&quot;[Child] 분석 완료!\n&quot;);
    } else if (pid &gt; 0) {
        // [Parent] 사용자 입력 대기 또는 UI 갱신
        printf(&quot;[Parent] 다른 작업 수행 중... (PID: %d)\n&quot;, getpid());
    }
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/18dc7cd7-b726-42ad-ade6-47726bff3338/image.png" /></p>
<hr />
<h3 id="2-2-외부-프로그램-실행-shell-pattern">2-2) 외부 프로그램 실행 (Shell Pattern)</h3>
<p><strong>목적:</strong> 현재 프로세스를 유지하면서 다른 바이너리(<code>ls</code>, <code>grep</code> 등)를 실행.
<strong>시나리오:</strong> 쉘(Shell)이 명령어를 입력받아 실행하는 방식 (<code>fork</code> + <code>exec</code>).</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/wait.h&gt;

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // [Child] 현재 메모리를 비우고 'ls' 명령어로 덮어씀
        printf(&quot;[Child] 'ls -l' 실행\n&quot;);
        execl(&quot;/bin/ls&quot;, &quot;ls&quot;, &quot;-l&quot;, NULL);
        perror(&quot;execl failed&quot;); // 실패 시만 실행됨
    } else {
        // [Parent] 자식이 끝날 때까지 대기
        wait(NULL);
        printf(&quot;[Parent] 자식 프로세스(명령어) 종료 확인 완료.\n&quot;);
    }
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/94753c0e-3672-46a6-aa6c-488905d93ad9/image.png" /></p>
<hr />
<h3 id="2-3-다중-접속-서버-concurrent-server">2-3. 다중 접속 서버 (Concurrent Server)</h3>
<p><strong>목적:</strong> 여러 클라이언트의 요청을 동시에 처리.
<strong>시나리오:</strong> 웹 서버(Apache 등)가 클라이언트가 접속(<code>accept</code>)할 때마다 전담 자식 프로세스를 생성.</p>
<pre><code class="language-c">// (의사 코드 - 핵심 로직 위주)
int server_fd = socket(...);
bind(server_fd, ...);
listen(server_fd, 5);

while(1) {
    // 1. 클라이언트 연결 수락 (Blocking)
    int client_fd = accept(server_fd, ...);

    // 2. 연결 들어오면 즉시 fork
    if (fork() == 0) {
        // [Child] 이 클라이언트만 전담 처리
        close(server_fd); // 자식은 듣기 소켓 필요 없음
        process_request(client_fd);
        close(client_fd);
        exit(0); // 처리 후 자식 소멸
    } else {
        // [Parent] 즉시 다시 listen 모드로 복귀 (다른 클라이언트 받으러 감)
        close(client_fd); // 부모는 핸들링 안 하므로 닫음
    }
}</code></pre>
<hr />
<h3 id="3-실습-과제">3. 실습 과제</h3>
<ul>
<li>전역변수 int g_count=0;을 만들고, fork()를 이용 하여 2개의 프로세스가  전역변수를 같이 1씩 증가 시키려면?</li>
<li>MAX_COUNT=100,000;   </li>
<li>예상 결과값 : 100,000 ~200,000</li>
</ul>
<hr />
<h3 id="31-풀이-1-semaphore-세마포어-방식">3.1) 풀이 1: Semaphore (세마포어) 방식</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;sys/mman.h&gt;
#include &lt;sys/wait.h&gt;
#include &lt;semaphore.h&gt;

#define MAX_COUNT 100000


int main() {
    int * g_count = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, 
                            MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    sem_t * locker = mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE, 
                            MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *g_count = 0;
    sem_init(locker, 1, 1);
    printf(&quot;=== [Start] count를 시작합니다 (PID: %d) ===\n&quot;, getpid());

    // 1. 여기서 프로세스가 복제됨 (세포 분열)
    pid_t pid = fork();

    // 2. 분기 처리 (복제된 직후)
    if (pid &lt; 0) {
        perror(&quot;Fork 실패&quot;);
        return 1;
    }

    if (pid == 0) {
        for (int i = 0; i &lt; MAX_COUNT; i++) {
            sem_wait(locker);
            (*g_count)++;
            sem_post(locker);
        }
        printf(&quot;자식 실행 종료\n&quot;);
        exit(0);
    } else {
        for (int i = 0; i &lt; MAX_COUNT; i++) {
            sem_wait(locker);
            (*g_count)++;
            sem_post(locker);
    }
    printf(&quot;자식이 끝날때까지 대기\n&quot;);
    waitpid(pid, NULL, 0);
    printf(&quot;자식 종료 확인\n&quot;);
    printf(&quot;%d\n&quot;,*g_count);
    munmap(g_count, sizeof(int));
    munmap(locker, sizeof(sem_t));
    }
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a286c502-d3ce-47ee-bcf1-8d7444eaa6b8/image.png" /></p>
<hr />
<h3 id="3-2-풀이-2-atomic-연산-방식">3-2) 풀이 2: Atomic 연산 방식</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;sys/mman.h&gt;
#include &lt;sys/wait.h&gt;
#include &lt;stdatomic.h&gt;

#define MAX_COUNT 100000000

//spin lock방식으로 메모리 접근 제한
void lock(int* locker){
    //lock이 1이면 무한 반복
    while(*locker == 1){
    }
    //빠져나오면 자신이 lock을 검
    *locker = 1;
}

void freelock(int* locker){
    *locker = 0;
}

int main() {
    atomic_int  *g_count = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, 
                            MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    int * locker = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, 
                            MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *g_count = 0;
    *locker = 0;
    printf(&quot;=== [Start] count를 시작합니다 (PID: %d) ===\n&quot;, getpid());

    // 1. 여기서 프로세스가 복제됨 (세포 분열)
    pid_t pid = fork();

    // 2. 분기 처리 (복제된 직후)
    if (pid &lt; 0) {
        perror(&quot;Fork 실패&quot;);
        return 1;
    }

    if (pid == 0) {
        for (int i = 0; i &lt; MAX_COUNT; i++) {

            (*g_count)++;

        }
        printf(&quot;자식 실행 종료\n&quot;);
        exit(0);
    } else {
        for (int i = 0; i &lt; MAX_COUNT; i++) {

            (*g_count)++;

    }
    printf(&quot;자식이 끝날때까지 대기\n&quot;);
    waitpid(pid, NULL, 0);
    printf(&quot;자식 종료 확인\n&quot;);
    printf(&quot;%d\n&quot;,*g_count);
    munmap(g_count, sizeof(int));
    munmap(locker, sizeof(int));
    }
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e1edf488-b751-4bbc-ae29-bc9182eede5e/image.png" /></p>
<hr />
<h3 id="3-3-풀이-3-pipe-통신-방식">3-3) 풀이 3: Pipe 통신 방식</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/wait.h&gt;
#include &lt;sys/mman.h&gt;
#define MAX_COUNT 100000
/*
Q. 전역변수 int g_count=0;을 만들고, fork()를 이용 하여 2개의 프로세스가  전역변수를 같이 1씩 증가 시키려면?
- MAX_COUNT=100,000; 
- 예상 결과값 : 100,000 ~200,000
*/
int g_count=0;

int main() {

    int pipefd[2];
    pipe(pipefd);

    pid_t pid1= fork();
    pid_t pid2= fork();

    if (pid1 == 0 &amp;&amp; pid2&gt;0) 
    {
        // [Child] 무거운 연산 담당
        printf(&quot;[Child1] g_count++ 중... (PID: %d)\n&quot;, getpid());
        while(1){
            g_count++;
            if(g_count&gt;=MAX_COUNT) break;
        }
        printf(&quot;child1 &gt;  g_count=%d\n&quot;,g_count);
        printf(&quot;[Child1] 완료!\n&quot;);

        int my_count=g_count;
        write(pipefd[1], &amp;my_count, sizeof(int));
    } 
    else if(pid1 &gt;0 &amp;&amp; pid2==0)
    {
        printf(&quot;[Child2] g_count++ 중... (PID: %d)\n&quot;, getpid());
        while(1){
            g_count++;
            if(g_count&gt;=MAX_COUNT) break;
        }
        printf(&quot;child2 &gt; g_count=%d\n&quot;,g_count);
        printf(&quot;[Child2] 완료!\n&quot;);

        int my_count=g_count;
        write(pipefd[1], &amp;my_count, sizeof(int));
    }
    else if(pid1 &gt;0 &amp;&amp; pid2 &gt;0)
    {
        // [Parent] 사용자 입력 대기 또는 UI 갱신
        wait(NULL);
        wait(NULL);

        int child1_count, child2_count;
        read(pipefd[0], &amp;child1_count, sizeof(int));  
        read(pipefd[0], &amp;child2_count, sizeof(int));  
        g_count = child1_count + child2_count;
        printf(&quot;[Parent] 자식 프로세스 대기중 (PID: %d)\n&quot;, getpid()); 
        printf(&quot;\n==========&lt; 최종 parent &gt; g_count=%d &gt;============\n&quot;,g_count);
    }

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a9b67fb1-a878-4e6c-a091-11ea440f0967/image.png" /></p>
<hr />
<h3 id="3-4-풀이-3-수정-pipe-통신-방식-fork-순서-개선">3-4) 풀이 3 수정: Pipe 통신 방식 (fork 순서 개선)</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/wait.h&gt;
#include &lt;sys/mman.h&gt;
#define MAX_COUNT 100000
/*
Q. 전역변수 int g_count=0;을 만들고, fork()를 이용 하여 2개의 프로세스가  전역변수를 같이 1씩 증가 시키려면?
- MAX_COUNT=100,000;
- 예상 결과값 : 100,000 ~200,000
*/
int g_count = 0;

int main()
{

    int pipefd[2];
    pipe(pipefd);

    pid_t pid1 = fork();

    if (pid1 == 0)
    {
        // [Child] 무거운 연산 담당
        printf(&quot;[Child1] g_count++ 중... (PID: %d)\n&quot;, getpid());
        while (1)
        {
            g_count++;
            if (g_count &gt;= MAX_COUNT)
                break;
        }
        printf(&quot;child1 &gt;  g_count=%d\n&quot;, g_count);
        printf(&quot;[Child1] 완료!\n&quot;);

        int my_count = g_count;
        write(pipefd[1], &amp;my_count, sizeof(int));
    }
    else if (pid1 &gt; 0)
    {
        pid_t pid2 = fork();
        if (pid2 == 0)
        {
            printf(&quot;[Child2] g_count++ 중... (PID: %d)\n&quot;, getpid());
            while (1)
            {
                g_count++;
                if (g_count &gt;= MAX_COUNT)
                    break;
            }
            printf(&quot;child2 &gt; g_count=%d\n&quot;, g_count);
            printf(&quot;[Child2] 완료!\n&quot;);

            int my_count = g_count;
            write(pipefd[1], &amp;my_count, sizeof(int));
        }
        else
        {
            // [Parent] 사용자 입력 대기 또는 UI 갱신
            wait(NULL);
            wait(NULL);

            int child1_count, child2_count;
            read(pipefd[0], &amp;child1_count, sizeof(int));
            read(pipefd[0], &amp;child2_count, sizeof(int));
            g_count = child1_count + child2_count;
            printf(&quot;[Parent] 자식 프로세스 대기중 (PID: %d)\n&quot;, getpid());
            printf(&quot;\n==========&lt; 최종 parent &gt; g_count=%d &gt;============\n&quot;, g_count);
        }
    }

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b10da49e-823b-4c8e-988d-45f2aaab706e/image.png" /></p>
<hr />
<p>풀이 3 방법이 내가 풀었던 방법인데,</p>
<pre><code class="language-c">pid_t pid1= fork();
pid_t pid2= fork();</code></pre>
<p>을 했을때, 프로세스가 4개 생성된다는 것을 이해를 못했다. 프로그램의 부모 pid까지 출력하고, <code>sleep(500)</code>을 건 다음, <code>ps --ppid [부모 프로세스 pid]</code> 를 통해 자식 프로세스를 확인해보았다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a46ef8d4-1376-494c-8d16-14f6ca5ed70d/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d05a60cd-9c24-42cd-9707-c22edfc0f9b3/image.png" /></p>
<p>확인해보니 프로세스가 4개 나와야 하지만 어떻게 설정하든 2개밖에 안 나와서 부모 프로세스 1개 + 자식 프로세스 2개 = 총 3개의 프로세스 이렇게 생성되는건가 헷갈렸으나,</p>
<p>처음에는 프로세스가 총 4개인게 맞고, 만들어진 프로세스 중에 조건에 해당되지 않는 프로세스는 코드 상에서 할 일이 없으니 빠르게 return 0;을 통해 종료되어 <code>ps --ppid</code> 명령어에 안 보인것이라고 한다.</p>
<p>기존 코드는 아래 과정을 통해 4개 생성</p>
<pre><code class="language-c">pid_t pid1 = fork();  // A → A, B (2개)
pid_t pid2 = fork();  // A, B 둘 다 fork → A, B, C, D (4개)</code></pre>
<p>프로세스를 총 3개 만들기 위해서는 </p>
<pre><code class="language-c">pid_t pid1 = fork();       // A → A, B (2개)
if (pid1 == 0) { 
    // 자식1(B)은 여기서 끝
}
else {
    pid_t pid2 = fork();   // 부모(A)만 fork → A, B, C (3개)
}</code></pre>
<p>이렇게 <code>if-else</code> 구조를 통해 자식1이 두 번째 <code>fork()</code>를 실행하지 않고, 부모만 자식2를 생성하므로 총 3개 프로세스만 생성된다.</p>