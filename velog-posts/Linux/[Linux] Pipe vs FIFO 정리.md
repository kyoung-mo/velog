<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bdd16faa-f5d1-4573-9053-1dd1e0ea7fcb/image.gif" /></p>
<hr />
<h3 id="pipe-정리">Pipe 정리</h3>
<h3 id="1-pipe-vs-fifo">1. Pipe vs FIFO</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>Pipe (Unnamed)</th>
<th>FIFO (Named)</th>
</tr>
</thead>
<tbody><tr>
<td>식별자</td>
<td>이름 없음 (파일 디스크립터로 접근)</td>
<td>파일 시스템 내 경로명 (이름 있음)</td>
</tr>
<tr>
<td>통신 범위</td>
<td>부모-자식 등 혈연 관계 프로세스 간</td>
<td>관계없는 독립적인 프로세스 간</td>
</tr>
<tr>
<td>생성 방식</td>
<td><code>pipe()</code> 시스템 콜</td>
<td><code>mkfifo()</code> 시스템 콜 또는 명령</td>
</tr>
<tr>
<td>지속성</td>
<td>프로세스 종료 시 소멸</td>
<td>명시적으로 삭제(<code>unlink</code>) 전까지 유지</td>
</tr>
<tr>
<td>통신 방향</td>
<td>반이중(Half-Duplex)</td>
<td>반이중(Half-Duplex)</td>
</tr>
</tbody></table>
<hr />
<h3 id="2-pipe-unnamed-pipe-상세">2. Pipe (Unnamed Pipe) 상세</h3>
<ul>
<li>커널 메모리에 유지되는 한정된 용량의 버퍼(기본 4KB)입니다.</li>
<li>읽을 데이터가 없으면 <code>read()</code>는 블록(Block)됩니다. 쓰기 측이 파이프를 닫으면 EOF(0)를 수신합니다.</li>
<li>단방향이 기본이므로, 전이중 통신을 위해서는 두 개의 파이프가 필요합니다.</li>
<li><code>dup2()</code>를 이용해 표준 출력(1)을 파이프의 쓰기 종단으로, 표준 입력(0)을 파이프의 읽기 종단으로 연결하여 <code>exec</code> 계열 함수와 함께 자주 사용됩니다.</li>
</ul>
<hr />
<h3 id="21-unnamed-pipe-통신-예제-c언어">2.1) Unnamed Pipe 통신 예제 (C언어)</h3>
<p>이 코드는 자식 프로세스가 <code>ls -l</code>과 같은 명령을 실행하고, 부모 프로세스가 그 결과를 파이프를 통해 읽어와서 출력하는 &quot;입출력 리다이렉션&quot; 메커니즘을 시뮬레이션합니다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;sys/wait.h&gt;

#define BUF_SIZE 1024

int main() {
    int pipe_fds[2]; // [0]: Read end, [1]: Write end
    pid_t pid;
    char buffer[BUF_SIZE];

    // 1. 파이프 생성
    if (pipe(pipe_fds) == -1) {
        perror(&quot;pipe failed&quot;);
        return 1;
    }

    // 2. 자식 프로세스 생성
    pid = fork();

    if (pid &lt; 0) {
        perror(&quot;fork failed&quot;);
        return 1;
    }

    if (pid == 0) {
        /*** 자식 프로세스: 송신자(Writer) ***/

        // 사용하지 않는 읽기용 FD는 즉시 닫음 (매우 중요)
        close(pipe_fds[0]);

        const char *msg = &quot;Hello from Child process via Pipe!&quot;;
        printf(&quot;[Child] Sending data to parent...\n&quot;);

        // 커널 버퍼에 데이터 쓰기
        write(pipe_fds[1], msg, strlen(msg) + 1);

        // 쓰기 완료 후 FD 닫기 (부모 측에 EOF 전달)
        close(pipe_fds[1]);
        exit(0);

    } else {
        /*** 부모 프로세스: 수신자(Reader) ***/

        // 사용하지 않는 쓰기용 FD는 즉시 닫음
        close(pipe_fds[1]);

        printf(&quot;[Parent] Waiting for data...\n&quot;);

        // 파이프에서 데이터 읽기 (데이터가 올 때까지 Blocking)
        ssize_t nbytes = read(pipe_fds[0], buffer, sizeof(buffer));

        if (nbytes &gt; 0) {
            printf(&quot;[Parent] Received message: %s\n&quot;, buffer);
        }

        // 읽기 완료 후 FD 닫기
        close(pipe_fds[0]);

        // 자식 프로세스 종료 대기 (Zombie 방지)
        wait(NULL);
        printf(&quot;[Parent] Child finished. Exiting.\n&quot;);
    }

    return 0;
}</code></pre>
<h3 id="22-핵심-체크포인트">2.2) 핵심 체크포인트</h3>
<ul>
<li><strong>FD 관리 (Unused Close)</strong>:<ul>
<li><code>fork()</code> 직후 각 프로세스에서 사용하지 않는 방향의 파일 디스크립터를 즉시 닫아야 합니다.</li>
<li>특히 <strong>쓰기 종단(<code>pipe_fds[1]</code>)</strong>이 모든 프로세스에서 닫히지 않으면, 읽기 측 프로세스의 <code>read()</code> 함수는 EOF를 감지하지 못하고 무한 대기(Hang) 상태에 빠질 수 있습니다.</li>
</ul>
</li>
<li><strong>Atomic Write</strong>:<ul>
<li><code>PIPE_BUF</code> 크기(일반적으로 4KB) 이하의 데이터 쓰기는 원자성(Atomicity)이 보장됩니다. 여러 프로세스가 동시에 쓸 때 데이터 섞임을 방지하려면 이 크기를 고려해야 합니다.</li>
</ul>
</li>
<li><strong>Blocking I/O</strong>:<ul>
<li>파이프는 기본적으로 동기적입니다. 데이터가 없으면 <code>read</code>는 블록되고, 파이프 버퍼가 가득 차면 <code>write</code>가 블록됩니다. 비동기 처리가 필요하다면 <code>fcntl</code>을 통해 <code>O_NONBLOCK</code> 설정을 고려해야 합니다.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="3-fifo-named-pipe-상세">3. FIFO (Named Pipe) 상세</h3>
<ul>
<li>특징: &quot;이름이 있는 파이프&quot;로, 파일 시스템에 특수 파일 형태로 존재합니다.</li>
<li>접근성: 파일 경로만 안다면 서로 모르는 프로세스(예: Client-Server)끼리도 <code>open()</code>을 통해 통신할 수 있습니다.</li>
<li>생성:<ul>
<li>C 코드: <code>mkfifo(&quot;/tmp/myfifo&quot;, 0666);</code></li>
<li>Shell: <code>$ mkfifo myfifo</code></li>
</ul>
</li>
</ul>
<hr />
<h3 id="3-1-예제--fifonamed-pipe는-서로-관계가-없는-독립적인-프로세스-간의-통신">3-1) 예제 -FIFO(Named Pipe)는 서로 관계가 없는 독립적인 프로세스 간의 통신</h3>
<p>파일 시스템에 실제 경로를 가진 <strong>Special File</strong>을 생성합니다.</p>
<p>통신을 확인하기 위해 <strong>Writer(송신)</strong>와 <strong>Reader(수신)</strong> 두 개의 독립적인 프로그램을 작성해야 합니다.</p>
<hr />
<h3 id="3-2-fifo-reader-수신측-fifo_readerc">3-2) FIFO Reader (수신측: <code>fifo_reader.c</code>)</h3>
<p>이 프로그램은 FIFO 파일을 생성하고, 데이터가 들어올 때까지 대기(Blocking)합니다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;

#define FIFO_NAME &quot;/tmp/my_test_fifo&quot;
#define BUF_SIZE 1024

int main() {
    int fd;
    char buffer[BUF_SIZE];

    // 1. FIFO 파일 생성 (이미 존재하면 건너뜀)
    // 권한: 0666 (rw-rw-rw-)
    if (mkfifo(FIFO_NAME, 0666) == -1) {
        // 이미 존재하는 경우는 에러가 아니므로 체크
    }

    printf(&quot;[Reader] Waiting for a writer...\n&quot;);

    // 2. FIFO 오픈 (송신측이 열 때까지 여기서 블록됨)
    fd = open(FIFO_NAME, O_RDONLY);
    if (fd == -1) {
        perror(&quot;open&quot;);
        return 1;
    }

    printf(&quot;[Reader] Writer connected. Reading data...\n&quot;);

    // 3. 데이터 읽기
    while (1) {
        ssize_t n = read(fd, buffer, BUF_SIZE);
        if (n &lt;= 0) break; // EOF (Writer가 닫음)

        printf(&quot;[Reader] Received: %s&quot;, buffer);
        memset(buffer, 0, BUF_SIZE);
    }

    close(fd);
    unlink(FIFO_NAME); // 통신 종료 후 FIFO 파일 삭제
    printf(&quot;[Reader] Finished.\n&quot;);

    return 0;
}</code></pre>
<hr />
<h3 id="3-3-fifo-writer-송신측-fifo_writerc">3-3) FIFO Writer (송신측: <code>fifo_writer.c</code>)</h3>
<p>이 프로그램은 이미 생성된 FIFO 파일에 데이터를 씁니다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;

#define FIFO_NAME &quot;/tmp/my_test_fifo&quot;

int main() {
    int fd;
    char *msg1 = &quot;Hello from Writer!\n&quot;;
    char *msg2 = &quot;Named Pipe (FIFO) test success.\n&quot;;

    printf(&quot;[Writer] Attempting to open FIFO...\n&quot;);

    // 1. FIFO 오픈 (수신측이 열려 있어야 오픈 성공)
    fd = open(FIFO_NAME, O_WRONLY);
    if (fd == -1) {
        perror(&quot;open (Is reader running?)&quot;);
        return 1;
    }

    // 2. 데이터 전송
    printf(&quot;[Writer] Sending data...\n&quot;);
    write(fd, msg1, strlen(msg1) + 1);
    sleep(1);
    write(fd, msg2, strlen(msg2) + 1);

    close(fd);
    printf(&quot;[Writer] Finished.\n&quot;);

    return 0;
}</code></pre>
<hr />
<h3 id="34-실행-및-테스트-방법">3.4) 실행 및 테스트 방법</h3>
<p>두 프로그램을 각각 컴파일한 후, <strong>두 개의 터미널</strong>에서 실행하세요.</p>
<h4 id="1-terminal-1-reader-실행bash">1. <strong>Terminal 1 (Reader 실행)</strong>:Bash</h4>
<pre><code class="language-bash">gcc fifo_reader.c -o reader
./reader</code></pre>
<p><em>결과: <code>Waiting for a writer...</code> 메시지와 함께 대기 상태가 됩니다.</em></p>
<h4 id="2-terminal-2-writer-실행bash">2. <strong>Terminal 2 (Writer 실행)</strong>:Bash</h4>
<pre><code>```bash
gcc fifo_writer.c -o writer
./writer
```

*결과: Writer가 실행되는 즉시 Reader 터미널에 메시지가 출력됩니다.*</code></pre><hr />
<h3 id="35-핵심-요약">3.5) 핵심 요약</h3>
<ul>
<li><strong>Synchronization (Rendezvous)</strong>: FIFO는 <code>open()</code> 시점에 동기화가 발생합니다. <code>O_RDONLY</code>로 여는 프로세스는 다른 프로세스가 <code>O_WRONLY</code>로 열 때까지 블록됩니다 (반대도 마찬가지).</li>
<li><strong>Persistent Node</strong>: FIFO 파일은 <code>pipe()</code>와 달리 파일 시스템 상에 노드로 남습니다. 따라서 사용 후 <code>unlink()</code>를 통해 명시적으로 제거해주는 것이 깔끔합니다.</li>
<li><strong>Blocking Behavior</strong>: <code>read()</code> 시 파이프가 비어있으면 데이터가 들어올 때까지 대기하며, <code>write()</code> 시 파이프 버퍼가 가득 차면 빈 공간이 생길 때까지 대기합니다.</li>
<li><strong>Non-blocking</strong>: 비동기 처리가 필요할 경우 <code>open(FIFO_NAME, O_RDONLY | O_NONBLOCK)</code>으로 설정하여 즉시 리턴받도록 구현할 수 있습니다.</li>
</ul>
<hr />
<h3 id="36-예제--g_count를-pipe를-이용">3.6) 예제 : g_count를 pipe를 이용</h3>
<p>2개의 자식 프로세스를 만들어 각각 100,000더한후 부모 프로세스에서 파이프로 받아서 합산하여 출력.</p>
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
<hr />
<h3 id="4-쉘-명령어-pipe--vs-tee">4. 쉘 명령어: Pipe (<code>|</code>) vs <code>tee</code></h3>
<p>프로세스 간 데이터 흐름을 제어할 때 쉘에서 자주 사용하는 도구입니다.</p>
<ul>
<li>Pipe (<code>|</code>): 단순히 앞 명령어의 출력을 다음 명령어의 입력으로 수직 전달합니다. (중간 확인 불가)</li>
<li>tee: 입력을 받아서 표준 출력(화면)과 파일에 동시에 기록합니다.<ul>
<li>사용 예: <code>ls | tee list.txt | grep &quot;test&quot;</code> (파일로 저장하면서 동시에 다음 필터로 전달)</li>
</ul>
</li>
</ul>
<hr />
<h3 id="41-pipe-code-예제--1--pipe---부모와-자식-프로세스간-데이터-전송--반이중">4.1) Pipe code 예제 – 1 : pipe() - 부모와 자식 프로세스간 데이터 전송 -반이중</h3>
<ul>
<li>Pipe (unnamed pipe)<pre><code>  - 프로세스간 통신을 위한 단방향 데이터 전송 채널
  - Pipe는 바이트 스트림 통신
  - PIPE_BUF(4096 bytes) 까지 쓰기가 보장 (limit.h)
  - Pipe는 커널 메모리에 유지되는 단순한 버퍼 - 최대 용량이 제한
  - 데이터가 있는 파이프를 읽고자 하는 경우 파이프에 적어도 1바이트가 pipe에 쓰여질 때까지 블럭됨
  - 파이프에 쓰는 측에서 파이프를 닫으면 읽는 측에서는 EOF을 의미하는 0을 수신
  - 파이프는 구조가 간단하여 사용하기가 쉽고, 반 이중(Half-Duplex) 통신만 제공함
  - 하나의 프로세스는 단지 데이터의 송신만 가능하고 다른 프로세스는 데이터의 수신만 가능함
  - 파이프를 이용하여 전 이중(Full-Duplex) 통신을 하려면 두 개의 파이프를 사용 해야 함 파일
  - 사용 시의 보안 문제 해결</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3d5a8693-b362-4836-bdf7-c20eb099082b/image.png" /></p>
<ul>
<li>pipe() 함수 원형</li>
</ul>
<pre><code class="language-c">#include &lt;unistd.h&gt; 
int pipe(int pipefd[2]);</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fb3e047d-7e12-4f39-bfb7-13787c2aa61e/image.png" /></p>
<h3 id="42-pipe-code-예제1">4.2) Pipe code 예제1</h3>
<p>05.ipc/01.mypipe1.c</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;time.h&gt;

int main(void) {
    int pd[2], read_fd, write_fd;
    pid_t pid;
    time_t timer1, timer2;
    char tx_buf[100], rx_buf[100];

    if ( pipe(pd) == -1 ) {
        perror(&quot;pipe&quot;);
        exit(1);
    }

    read_fd = pd[0];
    write_fd = pd[1];

    switch(pid=fork()) {
        case 0: //child
            close(read_fd);
            for(int i=0; i&lt;11; i++){
                sprintf(tx_buf, &quot;\e[31mHello Parent. I am child ---%d\n&quot;, i);
                write(write_fd, tx_buf, strlen(tx_buf)+1);
                for(timer1=time(NULL); time(NULL)&lt;timer1 + 1;)
                    continue;
            }
            exit(0);
        default: //parent
#if 1
            close(write_fd);
            for(int i=0; i&lt;10; i++){
                read(read_fd, rx_buf, sizeof(rx_buf));
                printf(&quot;\e[00mPARENT: %s\n&quot;, rx_buf);
            }
#else
            for(int i=0; i&lt;10; i++){
                for(timer2=time(NULL); time(NULL)&lt;timer2 + 2;)
                    continue;
                strcpy(tx_buf, &quot;\e[00mHello Child. I am Parent&quot;);
                write(write_fd, tx_buf, strlen(tx_buf)+1);
                read(read_fd, rx_buf, sizeof(rx_buf));
                printf(&quot;\e[00mPARENT: %s\n&quot;, rx_buf);
            }
#endif
            exit(0);
    }
}</code></pre>
<pre><code class="language-c">$ gcc 01.mypipe1.c -o 01.mypipe1

$ ./01.mypipe1
PARENT: Hello Parent. I am child ---0

PARENT: Hello Parent. I am child ---1

PARENT: Hello Parent. I am child ---2

PARENT: Hello Parent. I am child ---3

PARENT: Hello Parent. I am child ---4

PARENT: Hello Parent. I am child ---5

PARENT: Hello Parent. I am child ---6

PARENT: Hello Parent. I am child ---7

PARENT: Hello Parent. I am child ---8

PARENT: Hello Parent. I am child ---9</code></pre>
<h3 id="43-pipe-code-예제2">4.3) Pipe code 예제2</h3>
<p>pipe() - 부모와 자식 프로세스간 데이터 전송 - 전이중</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a8006a14-327b-485a-a9b6-0ad680602c42/image.png" /></p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;time.h&gt;

int main(void) {
    int pd[2], read_fd, write_fd;
    pid_t pid;
    time_t timer1, timer2;
    char tx_buf[100], rx_buf[100];

    if ( pipe(pd) == -1 ) {
        perror(&quot;pipe&quot;);
        exit(1);
    }

    read_fd = pd[0];
    write_fd = pd[1];

    switch(pid=fork()) {
        case 0: //child
            close(read_fd);
            for(int i=0; i&lt;11; i++){
                sprintf(tx_buf, &quot;\e[31mHello Parent. I am child ---%d\n&quot;, i);
                write(write_fd, tx_buf, strlen(tx_buf)+1);
                for(timer1=time(NULL); time(NULL)&lt;timer1 + 1;)
                    continue;
            }
            exit(0);
        default: //parent
            close(write_fd);
            for(int i=0; i&lt;10; i++){
                read(read_fd, rx_buf, sizeof(rx_buf));
                printf(&quot;\e[00mPARENT: %s\n&quot;, rx_buf);
            }
            exit(0);
    }
}</code></pre>
<pre><code class="language-c">$ gcc 01.mypipe1.c -o 01.mypipe1

$ ./01.mypipe1
PARENT: Hello Parent. I am child ---0

PARENT: Hello Parent. I am child ---1

PARENT: Hello Parent. I am child ---2

PARENT: Hello Parent. I am child ---3

PARENT: Hello Parent. I am child ---4

PARENT: Hello Parent. I am child ---5

PARENT: Hello Parent. I am child ---6

PARENT: Hello Parent. I am child ---7

PARENT: Hello Parent. I am child ---8

PARENT: Hello Parent. I am child ---9</code></pre>
<hr />
<h3 id="5-fifonamed-pipe">5. FIFO(Named Pipe)</h3>
<ul>
<li>FIFO는 파일 시스템 내에 이름을 갖고, 일반 파일과 동일한 방법으로 open 한다.</li>
<li>즉, FIFO = 이름이 부여된 PIPE</li>
<li>관련이 없는 프로세스간 통신에 사용 (Client &lt;-&gt; Server)</li>
<li>(익명을 사용하는) PIPE는 관련이 있는 프로세스간 통신에 사용</li>
</ul>
<pre><code class="language-c">#include &lt;sys/types.h&gt; 
#include &lt;sys/stat.h&gt; 

int mkfifo(const char *pathname, mode_t mode); 

$ mkfifo [ -m mode ] pathname </code></pre>
<ul>
<li>FIFO가 생성된 후에는 어느 프로세스도 파일을 열 수 있고 사용할 수 있음</li>
<li>I/O는 PIPE와 동일</li>
<li>FIFO와 tee 사용</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ca4e0de4-74e8-40f2-ae7b-13c55b59af35/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ea923ecf-a164-40e8-acc4-d78909243577/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2e294b69-267f-462e-87f1-a580fb032d0b/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e69df333-f5e0-4c34-aa7f-252160234ac7/image.png" /></p>
<p>리눅스 쉘에서 <strong>pipe(|)</strong>와 tee 명령어는 모두 명령어의 출력을 다루지만, 목적과 동작 방식에 차이가 있습니다.</p>
<h3 id="51-fifo-code-예제-1">5.1) FIFO code 예제 1</h3>
<ul>
<li>myfifo_recv.c</li>
</ul>
<pre><code class="language-c">#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;

int main(){
    int fd;
    char buf[128];
    int count = 0;

    if((access (&quot;/tmp/myfifo&quot;, F_OK)) != 0){
        if(mkfifo(&quot;/tmp/myfifo&quot;, S_IRUSR | S_IWUSR) == -1){
            perror(&quot;mkfifo&quot;);
            exit(1);
        }
    }

    if((fd = open(&quot;/tmp/myfifo&quot;, O_RDONLY)) == -1){
        perror(&quot;open&quot;);
        exit(1);
    }

    while(1){
        memset(buf, 0, sizeof(buf));
        read(fd, buf, sizeof(buf));
        printf(&quot;Rx - %s\n&quot;, buf);
        if(strstr(buf, &quot;end&quot;)){
            break;
        }
    }
    close(fd);
    unlink(&quot;/tmp/myfifo&quot;);
    return 0;
}</code></pre>
<pre><code class="language-c">$ gcc 03.myfifo_recv.c  -o recv

$ ./recv
Rx - Hello(0)
Rx - Hello(1)
Rx - Hello(2)
Rx - Hello(3)
Rx - Hello(4)
Rx - end</code></pre>
<h3 id="52-fifo-code-예제-2">5.2) FIFO code 예제 2</h3>
<p>myfifo_send.c</p>
<pre><code class="language-c">#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;

int main(){
    int fd, i;
    char buf[128];
    time_t timer1;

    if((fd = open(&quot;/tmp/myfifo&quot;, O_WRONLY)) == -1){
        perror(&quot;open&quot;);
        exit(2);
    }

    for(i=0; i&lt;5; i++){
        memset(buf, 0, sizeof(buf));
        sprintf(&amp;buf[0], &quot;Hello(%d)&quot;, i);
        write(fd, &amp;buf[0], strlen(buf)+1);
        printf(&quot;Tx: %s\n&quot;, buf);
        for(timer1=time(NULL); time(NULL)&lt;timer1 + 2;)
            continue;
    }
    memset(buf, 0, sizeof(buf));
    sprintf(buf, &quot;end&quot;);
    write(fd, buf, strlen(buf)+1);
    close(fd);
    /* unlink(&quot;/tmp/mkfifo&quot;); */
    return 0;
}</code></pre>
<pre><code class="language-c">$ gcc 04.myfifo_send.c  -o  send

$ ./send
Tx: Hello(0)
Tx: Hello(1)
Tx: Hello(2)
Tx: Hello(3)
Tx: Hello(4)</code></pre>
<hr />
<h3 id="6-unnamed-파이프를-이용한-프로세스간-통신">6. unnamed 파이프를 이용한 프로세스간 통신</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/45096034-9f2c-4502-8c62-5c7851ea4bfd/image.png" /></p>
<h3 id="61-unmaned-pipe-예제-1">6.1) unmaned-pipe 예제 1</h3>
<ul>
<li>child.c</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;

#define MSGSIZE    64

int main(){

    time_t timer1;
    char sbuf[MSGSIZE];
    int i;

    for(i=0; i&lt;5; i++){
        sprintf(&amp;sbuf[0], &quot;Hello, Parent --- I am child -- %d&quot;, i);
        write(1, sbuf, strlen(sbuf));
        for(timer1=time(NULL); time(NULL)&lt;timer1 + 1;)
            continue;
    }
    return 0;
}</code></pre>
<hr />
<h3 id="62-unmaned-pipe-예제-2">6.2) unmaned-pipe 예제 2</h3>
<ul>
<li>parent.c</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;

#define MSGSIZE    1024

int main(){

    time_t timer1;
    char rbuf[MSGSIZE];
    int i, len;

    for(i=0; ; i++){
        memset(&amp;rbuf[0], 0, MSGSIZE);
        len = read(0, rbuf, MSGSIZE);
        if(len == 0){
            break;
        }
        printf(&quot;%s\n&quot;, rbuf);
    }
    exit(0);
}

</code></pre>
<hr />
<h3 id="63-unmaned-pipe-예제-3">6.3) unmaned-pipe 예제 3</h3>
<ul>
<li>unnamed.c</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/wait.h&gt;

#define MSGSIZE    64

int main(void){
    int status;
    time_t timer1;
    int fd;
    int pd[2];

    pipe(pd);

    switch(fork()){
        case 0:                    //child
            close(pd[0]);
            dup2(pd[1], 1);
            if((execl(&quot;./child&quot;, &quot;child&quot;, (char *) 0)) == -1)
                perror(&quot;execl-child&quot;);
        default:                //parent
            switch(fork()){
                case 0:
                    close(pd[1]);
                    dup2(pd[0],0);
                    if((execl(&quot;./parent&quot;, &quot;parent&quot;,  (char *) 0)) == -1)
                        perror(&quot;execl-parent&quot;);
                default:
                    wait(&amp;status);
            }
    }
    close(pd[0]);
    close(pd[1]);
    return 0;
}</code></pre>
<p>child.c 소스 코드를 컴파일하여 child 실행 파일을 만들고, parent.c 소스 파일을 컴파일 해서 parent 실행 파일을 생성한 후 03.unamed 를 실행</p>
<pre><code class="language-c">$ gcc 03.unnamed.c  -o 03.unnamed

$ gcc child.c  -o child

$ gcc parent.c  -o parent

$ ./03.unnamed
Hello, Parent --- I am child -- 0
Hello, Parent --- I am child -- 1
Hello, Parent --- I am child -- 2
Hello, Parent --- I am child -- 3
Hello, Parent --- I am child -- 4</code></pre>