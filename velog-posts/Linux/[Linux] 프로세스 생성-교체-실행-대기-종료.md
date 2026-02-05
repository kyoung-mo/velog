<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/05e178da-050b-437a-b353-9c52ead8e2ca/image.png" /></p>
<hr />
<h3 id="프로세스-생성교체종료-대기종료">프로세스 생성/교체/종료 대기/종료</h3>
<h3 id="1-프로세스-생성-fork">1. 프로세스 생성 (<code>fork</code>)</h3>
<p>기존 프로세스(부모)를 복제하여 새로운 프로세스(자식)를 만들 때, 부모의 코드, 데이터, 힙, 스택을 복사합니다. (실제로는 <code>COW</code> : Copy On Write 기법으로 처음에는 공유만 하다가 수정 시 복사) 자식은 부모의 <code>Pending Signal</code>이나 <code>File Lock</code>은 상속받지 않습니다.</p>
<ul>
<li>부모: 자식의 <code>PID</code> 반환 | 자식: <code>0</code> 반환</li>
<li>파일 디스크립터(FD)도 복사되므로, <code>open</code>된 파일을 부모/자식이 공유하게 됩니다 (<code>lseek</code> 위치 공유).</li>
</ul>
<hr />
<h3 id="1-1-간단한-fork-예제">1-1) 간단한 fork 예제</h3>
<p><code>fork()</code>의 핵심 개념인 <code>복제</code>, <code>동시 실행</code>, <code>메모리 독립</code></p>
<ol>
<li>PID 구분: <code>fork()</code>의 리턴값으로 내가 부모인지 자식인지 판단한다.</li>
<li>동시성(Concurrency): 두 프로세스가 동시에(번갈아 가며) 실행됨을 눈으로 확인한다.</li>
<li>메모리 독립성: 자식에서 변수를 바꿔도 부모 변수는 바뀌지 않음을 확인한다.</li>
</ol>
<h4 id="예제-코드-racec">예제 코드 (race.c)</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;

// 전역 변수 (메모리 독립성 확인용)
int g_score = 0;

int main() {
    printf(&quot;=== [Start] 경기를 시작합니다 (PID: %d) ===\n&quot;, getpid());

    // 1. 여기서 프로세스가 복제됨 (세포 분열)
    pid_t pid = fork();

    // 2. 분기 처리 (복제된 직후)
    if (pid &lt; 0) {
        perror(&quot;Fork 실패&quot;);
        return 1;
    }

    if (pid == 0) {
        // [자식 프로세스 영역]
        // 자식은 pid 변수에 0을 받음
        for (int i = 0; i &lt; 5; i++) {
            g_score += 10; // 점수 증가
            printf(&quot;🐥 자식: 달리는 중... (점수: %d, 내PID: %d, 부모PID: %d)\n&quot;, 
                   g_score, getpid(), getppid());
            sleep(1); // 1초 쉼
        }
    } else {
        // [부모 프로세스 영역]
        // 부모는 pid 변수에 '자식의 PID'를 받음
        for (int i = 0; i &lt; 5; i++) {
            g_score += 1; // 점수 증가 (자식과 다르게 증가)
            printf(&quot;🦕 부모: 관전 중...   (점수: %d, 내PID: %d, 자식PID: %d)\n&quot;, 
                   g_score, getpid(), pid);
            sleep(1); // 1초 쉼
        }
    }

    return 0;
}</code></pre>
<h4 id="1-2-실행-결과-해석-포인트">1-2) 실행 결과 (해석 포인트)</h4>
<pre><code class="language-bash">=== [Start] 경기를 시작합니다 (PID: 1000) ===
🦕 부모: 관전 중...   (점수: 1, 내PID: 1000, 자식PID: 1001)
🐥 자식: 달리는 중... (점수: 10, 내PID: 1001, 부모PID: 1000)
🐥 자식: 달리는 중... (점수: 20, 내PID: 1001, 부모PID: 1000)
🦕 부모: 관전 중...   (점수: 2, 내PID: 1000, 자식PID: 1001)</code></pre>
<h4 id="1-3-궁금한-점">1-3) 궁금한 점</h4>
<ol>
<li>왜 <code>Start</code> 메시지는 한 번만 출력되었는가?<ul>
<li><code>fork()</code> 호출 전에 <code>printf</code>가 있었기 때문이다. <code>fork</code> 이후의 코드만 복제되어 실행</li>
</ul>
</li>
<li>왜 출력 순서가 뒤죽박죽인가?<ul>
<li>OS 스케줄러가 부모와 자식 중 누구에게 CPU를 먼저 줄지 매 순간 결정하기 때문(동시성)</li>
<li>딜레이를 제거하면 뒤죽박죽으로 나온다.</li>
</ul>
</li>
<li>자식이 점수를 50점까지 올렸는데, 왜 부모는 5점밖에 안 올랐는가?<ul>
<li><code>fork</code> 되는 순간 메모리 공간이 완벽히 분리(Copy-on-Write)되었기 때문이다. 자식의 <code>g_score</code>와 부모의 <code>g_score</code>는 이름만 같고 완전히 다른 변수이다.</li>
</ul>
</li>
</ol>
<hr />
<h3 id="2-프로그램-실행-및-교체-exec-family">2. 프로그램 실행 및 교체 (<code>exec</code> family)</h3>
<p><code>fork</code>로 만든 자식 프로세스는 보통 <code>exec</code>를 호출하여 새로운 프로그램으로 변신합니다. 현재 프로세스의 메모리 공간(Text, Data, Stack 등)을 비우고, 새로운 실행 파일의 코드와 데이터로 덮어씁니다. <code>PID</code>는 변하지 않고 유지되며, <code>exec</code> 성공 시, 코드 자체가 바뀌었으므로 기존 코드로 되돌아오지 않습니다.</p>
<p>함수 접미사 규칙:</p>
<ul>
<li><code>l</code> (List): 인자를 나열 (<code>execl</code>)</li>
<li><code>v</code> (Vector): 인자를 배열로 전달 (<code>execv</code>)</li>
<li><code>p</code> (Path): 환경변수 PATH 자동 탐색 (<code>execlp</code>)</li>
<li><code>e</code> (Env): 환경변수 직접 설정 (<code>execle</code>)</li>
</ul>
<hr />
<h3 id="3-종료-및-동기화-exit--wait">3. 종료 및 동기화 (<code>exit</code> &amp; <code>wait</code>)</h3>
<h4 id="a-종료-exit-vs-_exit">A. 종료 (<code>exit</code> vs <code>_exit</code>)</h4>
<ul>
<li><code>exit(int status)</code>: C 라이브러리 함수. <code>atexit</code> 핸들러 실행, stdio 버퍼(printf 등) 비움(flush) 후 종료.</li>
<li><code>_exit(int status)</code>: 시스템 콜. 커널 즉시 종료. 버퍼 정리 안 함. (주로 <code>fork</code> 직후 <code>exec</code> 실패 시 사용).</li>
</ul>
<h4 id="b-좀비-프로세스-zombie와-처리">B. 좀비 프로세스 (Zombie)와 처리</h4>
<p>자식이 죽었는데(<code>exit</code>), 부모가 <code>wait</code>로 상태 코드를 회수해가지 않은 상태.</p>
<ul>
<li>해결책 (<code>wait</code> family):<ul>
<li><code>wait(&amp;status)</code>: 자식이 죽을 때까지 부모가 멈춥니다.(Block)</li>
<li><code>waitpid(pid, &amp;status, options)</code>: 특정 PID를 기다리거나, <code>WNOHANG</code> 옵션으로 멈추지 않고(Non-blocking) 상태만 확인할 수 있습니다.</li>
</ul>
</li>
<li>비동기 처리: <code>SIGCHLD</code> 시그널 핸들러를 등록하여, 자식이 죽었을 때만 <code>waitpid</code>를 호출하는 방식이 효율적입니다.</li>
</ul>
<hr />
<h3 id="4-간편-실행-함수-system-vs-popen">4. 간편 실행 함수 (<code>system</code> vs <code>popen</code>)</h3>
<p>직접 <code>fork</code>-<code>exec</code>-<code>wait</code>를 구현하기 번거로울 때 사용하는 래퍼(Wrapper) 함수들입니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>system()</th>
<th>popen()</th>
</tr>
</thead>
<tbody><tr>
<td>목적</td>
<td>단순히 쉘 명령 실행</td>
<td>명령 실행 후 결과값 읽기/쓰기</td>
</tr>
<tr>
<td>구조</td>
<td><code>fork</code> + <code>exec(/bin/sh)</code> + <code>wait</code></td>
<td><code>fork</code> + <code>exec</code> + <code>pipe</code></td>
</tr>
<tr>
<td>동기화</td>
<td>명령 끝날 때까지 대기 (동기)</td>
<td>스트림(<code>FILE*</code>)을 통해 통신</td>
</tr>
<tr>
<td>종료</td>
<td>함수 리턴 시 명령 종료됨</td>
<td><code>pclose()</code> 호출 시 정리됨</td>
</tr>
</tbody></table>
<hr />
<h3 id="5-과제-코드-ppid-추적">5. 과제 코드 (PPID 추적)</h3>
<p><code>popen</code>으로 <code>ps</code> 명령어를 매번 실행하면 느리고 복잡합니다. 리눅스 커널이 정보를 두는 <code>/proc</code> 파일을 직접 읽는 것이 가장 쉽고 빠르다고 합니다.</p>
<h3 id="아이디어">아이디어</h3>
<ul>
<li>리눅스의 <code>/proc/[PID]/stat</code> 파일에는 프로세스 정보가 한 줄로 들어있습니다.</li>
<li>4번째 숫자가 무조건 PPID입니다.</li>
<li><code>fscanf</code>를 쓰면 문자열 파싱(<code>strtok</code>) 없이 숫자만 쏙 빼낼 수 있습니다.</li>
</ul>
<h3 id="코드-ancestryc">코드 (<code>ancestry.c</code>)</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;

// PID를 주면 PPID를 리턴하는 함수 (핵심)
int get_ppid(int pid) {
    char path[64];
    FILE *fp;
    int ppid;

    // 1. 해당 PID의 정보 파일 열기
    sprintf(path, &quot;/proc/%d/stat&quot;, pid);
    fp = fopen(path, &quot;r&quot;);

    if (fp == NULL) return 0; // 프로세스가 없거나 읽기 실패

    // 2. 포맷 파싱: (1)PID (2)이름 (3)상태 (4)PPID
    // %*d, %*s 등은 읽기만 하고 변수에 저장 안 함(Skip)
    fscanf(fp, &quot;%*d %*s %*c %d&quot;, &amp;ppid);

    fclose(fp);
    return ppid;
}

int main() {
    int pid = getpid(); // 내 PID부터 시작

    printf(&quot;=== 프로세스 족보 추적 ===\n&quot;);
    printf(&quot;나(Me): %d&quot;, pid);

    // PID가 0이나 1(init)이 될 때까지 반복
    while (pid &gt; 1) {
        pid = get_ppid(pid); // 부모 찾기

        if (pid == 0) break; // 에러 처리
        printf(&quot; -&gt; %d&quot;, pid);
    }

    printf(&quot;\n=== 추적 완료 (Root 도달) ===\n&quot;);
    return 0;
}</code></pre>
<h3 id="실행-결과">실행 결과</h3>
<pre><code class="language-bash">=== 프로세스 족보 추적 ===
나(Me): 756332 -&gt; 756322 -&gt; 756320 -&gt; 742339 -&gt; 742074 -&gt; 742019 -&gt; 742015 -&gt; 741984 -&gt; 741966 -&gt; 741965 -&gt; 741957 -&gt; 86526 -&gt; 1
=== 추적 완료 (Root 도달) ===
[1] + Done                       &quot;/usr/bin/gdb&quot; --interpreter=mi --tty=${DbgTerm} 0&lt;&quot;/tmp/Microsoft-MIEngine-In-bk0ipbx0.cxl&quot; 1&gt;&quot;/tmp/Microsoft-MIEngine-Out-iehzgvak.fdq&quot;</code></pre>