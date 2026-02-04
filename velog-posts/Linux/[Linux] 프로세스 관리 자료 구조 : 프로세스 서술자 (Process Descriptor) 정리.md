<h3 id="프로세스-서술자-process-descriptor">프로세스 서술자 (Process Descriptor)</h3>
<p>리눅스 커널의 가장 중요한 객체로, 프로세스의 '주민등록등본'이자 '의료 기록 차트' 같은 느낌 (<code>PCB</code>)</p>
<p>리눅스 커널 소스(<code>&lt;linux/sched.h&gt;</code>)에 정의된 <code>struct task_struct</code>는 프로세스 제어 블록(PCB)의 리눅스 구조체입니다. 아래는 간략화된 실제 구조입니다.</p>
<pre><code class="language-c">struct task_struct {
    // 프로세스 상태
    volatile long state;        // 실행중? 대기중? 종료?

    // 프로세스 ID
    pid_t pid;                  // 프로세스 ID
    pid_t tgid;                 // 스레드 그룹 ID

    // 스케줄링 정보
    int prio;                   // 우선순위
    unsigned int policy;        // 스케줄링 정책

    // 메모리 관리
    struct mm_struct *mm;       // 메모리 주소 공간

    // 파일 시스템 정보
    struct files_struct *files; // 열린 파일들

    // CPU 레지스터 상태 (컨텍스트)
    struct thread_struct thread;

    // 부모-자식 프로세스 관계
    struct task_struct *parent;
    struct list_head children;

    // ... 훨씬 더 많은 필드들
};</code></pre>
<hr />
<h3 id="1-task_struct의-핵심-구성-요소">1. <code>task_struct</code>의 핵심 구성 요소</h3>
<p>커널은 이 구조체 하나로 프로세스의 모든 부분을 관리합니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>주요 필드 (변수명)</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>신원 (ID)</td>
<td><code>pid</code>, <code>tgid</code></td>
<td>프로세스 ID, 스레드 그룹 ID.</td>
</tr>
<tr>
<td>상태 (State)</td>
<td><code>state</code> (or <code>__state</code>)</td>
<td>실행 중(<code>TASK_RUNNING</code>), 대기 중, 좀비 등 현재 상태.</td>
</tr>
<tr>
<td>스케줄링</td>
<td><code>prio</code>, <code>policy</code>, <code>sched_class</code></td>
<td>우선순위, 스케줄링 정책(FIFO, RR, CFS).</td>
</tr>
<tr>
<td>메모리</td>
<td><code>struct mm_struct *mm</code></td>
<td>코드, 데이터, 힙, 스택이 있는 가상 메모리 정보.</td>
</tr>
<tr>
<td>파일 시스템</td>
<td><code>struct files_struct *files</code></td>
<td>현재 열려 있는 파일 디스크립터(fd) 테이블.</td>
</tr>
<tr>
<td>가계도</td>
<td><code>parent</code>, <code>children</code>, <code>sibling</code></td>
<td>부모, 자식, 형제 프로세스를 연결하는 이중 연결 리스트.</td>
</tr>
<tr>
<td>시그널</td>
<td><code>signal</code>, <code>sighand</code></td>
<td>대기 중인 시그널, 시그널 핸들러 정보.</td>
</tr>
</tbody></table>
<hr />
<h3 id="2-관리-구조-이중-연결-리스트-task-list">2. 관리 구조: 이중 연결 리스트 (Task List)</h3>
<p>모든 프로세스(테스크)는 원형 이중 연결 리스트로 묶여 있습니다.</p>
<ul>
<li>장점: 커널은 <code>for_each_process()</code> 매크로를 통해 시스템의 모든 프로세스를 빠르게 탐색할 수 있습니다.</li>
<li>구조: <code>init</code> 프로세스를 조상으로 하여 트리 형태로도 연결됩니다.</li>
</ul>
<hr />
<h3 id="3-핵심-매크로-current">3. 핵심 매크로: <code>current</code></h3>
<p>커널 코드에서 가장 많이 보이는 매크로 중 하나로, 현재 CPU에서 실행 중인 프로세스의 <code>task_struct</code> 주소를 즉시 반환합니다.</p>
<pre><code class="language-cpp">// 현재 프로세스의 PID를 알고 싶을 때
printk(KERN_INFO &quot;Current PID: %d\n&quot;, current-&gt;pid);</code></pre>
<hr />
<h3 id="4-참고-스레드와-task_struct">4. 참고: 스레드와 task_struct</h3>
<p>리눅스에서는 스레드도 <code>task_struct</code>로 관리됩니다. (Light Weight Process).</p>
<ul>
<li>프로세스: <code>mm</code>(메모리)과 <code>files</code>(파일) 구조체를 독점</li>
<li>스레드: 같은 프로세스 내 스레드끼리 <code>mm</code>과 <code>files</code> 포인터를 공유</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dae0087f-4cbc-45f6-a6ca-d150314120d8/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/41e511ff-236d-4b30-b1e9-dbf14da26f7a/image.png" /></p>
<hr />
<h3 id="실습">실습</h3>
<p>사용자 영역(User Space)에서는 <code>task_struct</code>에 직접 접근할 수 없으므로, <code>/proc</code> 파일시스템을 파싱(parsing)하여 구조체 내용을 확인하는 코드를 작성합니다.</p>
<p><code>task_struct</code>는 커널 메모리에 존재하므로 일반 C 프로그램에서는 접근이 불가능합니다. 대신 커널이 해당 구조체의 정보를 보여주는 <code>/proc/[PID]/stat</code> 파일을 읽어, <code>task_struct</code>와 유사한 구조체에 담아보는 실습이 가장 효과적입니다.</p>
<blockquote>
<p><em>파싱(parsing) : 분석하여 필요한 정보를 추출한다.</em></p>
</blockquote>
<h3 id="1-사용자-영역-시뮬레이션-코드-task_struct_viewc">1. 사용자 영역 시뮬레이션 코드 (<code>task_struct_view.c</code>)</h3>
<p>리눅스 커널의 <code>task_struct</code>에서 핵심 필드 몇 가지를 뽑아 구조체로 정의하고, 내 프로세스의 정보를 읽어 채우는 예제입니다.</p>
<pre><code class="language-cpp">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;

// 커널의 task_struct를 흉내 낸 사용자 정의 구조체
typedef struct _MyTaskStruct {
    pid_t pid;              // 프로세스 ID
    char comm[16];          // 프로세스 이름 (Command)
    char state;             // 프로세스 상태 (R:Running, S:Sleeping...)
    pid_t ppid;             // 부모 프로세스 ID
    int priority;           // 우선순위
    unsigned long vsize;    // 가상 메모리 크기
    long rss;               // 실제 메모리 사용량 (Page 단위)
} MyTaskStruct;

void get_process_info(MyTaskStruct *task) {
    FILE *fp;
    char path[256];

    // 내 프로세스(/proc/self)의 상태 정보를 여는 경로
    // 이 파일의 내용은 커널이 task_struct 값을 읽어서 생성해줌
    sprintf(path, &quot;/proc/%d/stat&quot;, getpid());

    fp = fopen(path, &quot;r&quot;);
    if (fp == NULL) {
        perror(&quot;fopen&quot;);
        exit(1);
    }

    // /proc/[pid]/stat 파일 포맷 파싱
    // (pid) (comm) (state) (ppid) ... 순서
    fscanf(fp, &quot;%d %s %c %d %*d %*d %*d %*d %*d %*d %*d %*d %*d %*d %*d %d %*d %*d %*d %*d %*d %*d %lu %ld&quot;,
           &amp;task-&gt;pid,
           task-&gt;comm,
           &amp;task-&gt;state,
           &amp;task-&gt;ppid,
           &amp;task-&gt;priority,  // 18번째 필드 근처 (정확한 위치는 man proc 참조 필요)
           &amp;task-&gt;vsize,
           &amp;task-&gt;rss);

    fclose(fp);

    // comm(이름)에 붙은 괄호() 제거
    size_t len = strlen(task-&gt;comm);
    if (len &gt; 2) {
        task-&gt;comm[len-1] = '\0'; // 닫는 괄호 제거
        memmove(task-&gt;comm, task-&gt;comm+1, len-1); // 여는 괄호 제거
    }
}

int main() {
    MyTaskStruct my_task;

    printf(&quot;=== Pseudo task_struct Viewer ===\n&quot;);
    printf(&quot;내 PID: %d\n&quot;, getpid());

    // 정보 가져오기
    get_process_info(&amp;my_task);

    // 구조체 내용 출력
    printf(&quot;\n[Process Descriptor Info]\n&quot;);
    printf(&quot;PID      : %d\n&quot;, my_task.pid);
    printf(&quot;Name     : %s\n&quot;, my_task.comm);
    printf(&quot;State    : %c (R=Running, S=Sleep)\n&quot;, my_task.state);
    printf(&quot;Parent   : %d\n&quot;, my_task.ppid);
    printf(&quot;Priority : %d\n&quot;, my_task.priority);
    printf(&quot;Virt Mem : %lu bytes\n&quot;, my_task.vsize);
    printf(&quot;RSS Mem  : %ld pages\n&quot;, my_task.rss);

    return 0;
}</code></pre>
<h3 id="실행-결과">실행 결과</h3>
<pre><code class="language-cpp">=== Pseudo task_struct Viewer ===
내 PID: 717130

[Process Descriptor Info]
PID      : 717130
Name     : practice1
State    : R (R=Running, S=Sleep)
Parent   : 717121
Priority : 0
Virt Mem : 2424832 bytes
RSS Mem  : 33 pages
[1] + Done                       &quot;/usr/bin/gdb&quot; --interpreter=mi --tty=${DbgTerm} 0&lt;&quot;/tmp/Microsoft-MIEngine-In-pvj3ybuu.2xa&quot; 1&gt;&quot;/tmp/Microsoft-MIEngine-Out-onspekwl.xh0&quot;</code></pre>
<hr />
<h3 id="2-현재-프로세스의-부모-프로세스를-계속-찾아가-1이-나올-떄까지-모두-보여주기">2. 현재 프로세스의 부모 프로세스를 계속 찾아가 1이 나올 떄까지 모두 보여주기</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;

// 커널의 task_struct를 흉내 낸 사용자 정의 구조체
typedef struct _MyTaskStruct {
    pid_t pid;              // 프로세스 ID
    char comm[16];          // 프로세스 이름 (Command)
    char state;             // 프로세스 상태 (R:Running, S:Sleeping...)
    pid_t ppid;             // 부모 프로세스 ID
    int priority;           // 우선순위
    unsigned long vsize;    // 가상 메모리 크기
    long rss;               // 실제 메모리 사용량 (Page 단위)
} MyTaskStruct;

void get_process_info(MyTaskStruct *task, pid_t pid) {
    FILE *fp;
    char path[256];

    // 내 프로세스(/proc/self)의 상태 정보를 여는 경로
    // 이 파일의 내용은 커널이 task_struct 값을 읽어서 생성해줌
    sprintf(path, &quot;/proc/%d/stat&quot;, pid);

    fp = fopen(path, &quot;r&quot;);
    if (fp == NULL) {
        perror(&quot;fopen&quot;);
        exit(1);
    }

    // /proc/[pid]/stat 파일 포맷 파싱
    // (pid) (comm) (state) (ppid) ... 순서
    fscanf(fp, &quot;%d %s %c %d %*d %*d %*d %*d %*d %*d %*d %*d %*d %*d %*d %d %*d %*d %*d %*d %*d %*d %lu %ld&quot;,
           &amp;task-&gt;pid,
           task-&gt;comm,
           &amp;task-&gt;state,
           &amp;task-&gt;ppid,
           &amp;task-&gt;priority,  // 18번째 필드 근처 (정확한 위치는 man proc 참조 필요)
           &amp;task-&gt;vsize,
           &amp;task-&gt;rss);

    fclose(fp);

    // comm(이름)에 붙은 괄호() 제거
    size_t len = strlen(task-&gt;comm);
    if (len &gt; 2) {
        task-&gt;comm[len-1] = '\0'; // 닫는 괄호 제거
        memmove(task-&gt;comm, task-&gt;comm+1, len-1); // 여는 괄호 제거
    }
}

        // 구조체 내용 출력
void print_task(MyTaskStruct task){
        printf(&quot;\n[Process Descriptor Info]\n&quot;);
        printf(&quot;PID      : %d\n&quot;, task.pid);
        printf(&quot;Name     : %s\n&quot;, task.comm);
        printf(&quot;State    : %c (R=Running, S=Sleep)\n&quot;, task.state);
        printf(&quot;Parent   : %d\n&quot;, task.ppid);
        printf(&quot;Priority : %d\n&quot;, task.priority);
        printf(&quot;Virt Mem : %lu bytes\n&quot;, task.vsize);
        printf(&quot;RSS Mem  : %ld pages\n&quot;, task.rss);
}

void go_parant(MyTaskStruct task, pid_t my_pid){
    pid_t cur_pid = my_pid;
     while (cur_pid &gt; 1)
     {
           // 정보 가져오기
        get_process_info(&amp;task, cur_pid);
        print_task(task);
        cur_pid = task.ppid;
     }
        // 정보 가져오기
        get_process_info(&amp;task, cur_pid);
        print_task(task);
}


int main() {
    MyTaskStruct my_task;
    pid_t my_pid = getpid();
    printf(&quot;=== Pseudo task_struct Viewer ===\n&quot;);
    printf(&quot;내 PID: %d\n&quot;, my_pid);

    go_parant(my_task, my_pid);

    return 0;
}</code></pre>
<h3 id="실행-결과-1">실행 결과</h3>
<pre><code class="language-c">
=== Pseudo task_struct Viewer ===
내 PID: 721512

[Process Descriptor Info]
PID      : 721512
Name     : parents_process
State    :  (R=Running, S=Sleep)
Parent   : 721501
Priority : 0
Virt Mem : 2424832 bytes
RSS Mem  : 33 pages

[Process Descriptor Info]
PID      : 721501
Name     : gdb
State    : S (R=Running, S=Sleep)
Parent   : 721499
Priority : 0
Virt Mem : 373604352 bytes
RSS Mem  : 2395 pages

[Process Descriptor Info]
PID      : 721499
Name     : sh
State    : S (R=Running, S=Sleep)
Parent   : 721179
Priority : 0
Virt Mem : 2539520 bytes
RSS Mem  : 67 pages

[Process Descriptor Info]
PID      : 721179
Name     : bash
State    : S (R=Running, S=Sleep)
Parent   : 716293
Priority : 21
Virt Mem : 9207808 bytes
RSS Mem  : 325 pages

[Process Descriptor Info]
PID      : 716293
Name     : node
State    : S (R=Running, S=Sleep)
Parent   : 716249
Priority : 48
Virt Mem : 1113718784 bytes
RSS Mem  : 5397 pages

[Process Descriptor Info]
PID      : 716249
Name     : node
State    : S (R=Running, S=Sleep)
Parent   : 716245
Priority : 546
Virt Mem : 11844747264 bytes
RSS Mem  : 7455 pages

[Process Descriptor Info]
PID      : 716245
Name     : sh
State    : S (R=Running, S=Sleep)
Parent   : 1
Priority : 0
Virt Mem : 2539520 bytes
RSS Mem  : 67 pages

[Process Descriptor Info]
PID      : 1
Name     : systemd
State    : S (R=Running, S=Sleep)
Parent   : 0
Priority : 144324
Virt Mem : 26542080 bytes
RSS Mem  : 915 pages
[1] + Done                       &quot;/usr/bin/gdb&quot; --interpreter=mi --tty=${DbgTerm} 0&lt;&quot;/tmp/Microsoft-MIEngine-In-gt2gj1va.wc3&quot; 1&gt;&quot;/tmp/Microsoft-MIEngine-Out-4emzzton.0sl&quot;</code></pre>
<hr />
<h3 id="실제-커널-모듈-코드-참고">실제 커널 모듈 코드 (참고)</h3>
<p>만약 진짜 <code>task_struct</code>에 접근하려면 커널 모듈(LKM)을 작성해야 합니다.</p>
<pre><code class="language-cpp">/* kernel_task_check.c */
#include &lt;linux/module.h&gt;
#include &lt;linux/kernel.h&gt;
#include &lt;linux/sched.h&gt; // 실제 task_struct 정의 헤더

int init_module(void) {
    // 'current' 매크로는 현재 실행 중인 프로세스(이 모듈을 로드한 insmod)의
    // task_struct 포인터를 반환함.
    struct task_struct *task = current;

    printk(KERN_INFO &quot;[Kernel] PID: %d\n&quot;, task-&gt;pid);
    printk(KERN_INFO &quot;[Kernel] Comm: %s\n&quot;, task-&gt;comm);
    printk(KERN_INFO &quot;[Kernel] Parent PID: %d\n&quot;, task-&gt;parent-&gt;pid);

    return 0;
}

void cleanup_module(void) {
    printk(KERN_INFO &quot;[Kernel] Module removed.\n&quot;);
}

MODULE_LICENSE(&quot;GPL&quot;);</code></pre>
<hr />
<ul>
<li>User Space: <code>/proc</code> 파일 시스템을 통해 <code>task_struct</code> 정보를 간접적으로 확인 (안전, 실무적).</li>
<li>Kernel Space: <code>current</code> 매크로를 통해 <code>task_struct</code>에 직접 접근 (드라이버 개발 시 사용).</li>
</ul>
<p><a href="https://www.notion.so/2fac59623e6180e684fcfb6809f10f41?pvs=21">커널 컴파일</a></p>