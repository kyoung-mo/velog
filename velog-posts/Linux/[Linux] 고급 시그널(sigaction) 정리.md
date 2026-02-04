<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ce3f3c23-3f6a-458f-b5f8-e78f0c1098a4/image.png" /></p>
<hr />
<h3 id="고급시그널-처리-sigaction">고급시그널 처리-sigaction</h3>
<p><code>signal()</code> 함수의 불안정함(시스템별 동작 차이)을 해결하고, 핸들러 실행 중 '다른 시그널 차단' 등 정교한 제어가 가능한 표준 함수</p>
<hr />
<h3 id="1-sigaction을-써야-하는-이유">1. <code>sigaction</code>을 써야 하는 이유</h3>
<ul>
<li>표준화 : 모든 유닉스/리눅스 시스템에서 동일하게 동작함 (POSIX 표준)</li>
<li>블록(Block) 기능 : 핸들러가 실행되는 동안 또 다른 특정 시그널이 끼어들지 못하게 막을 수 있음 (<code>sa_mask</code>)</li>
<li>정보 제공 : 시그널을 누가 보냈는지(PID), 왜 보냈는지 등 상세 정보 확인 가능 (<code>SA_SIGINFO</code>)</li>
</ul>
<hr />
<h3 id="2-구조체-및-원형">2. 구조체 및 원형</h3>
<p>C</p>
<pre><code class="language-cpp">#include &lt;signal.h&gt;

struct sigaction {
    void (*sa_handler)(int);           // 핸들러 함수 포인터
    void (*sa_sigaction)(int, siginfo_t *, void *); // 고급 핸들러
    sigset_t sa_mask;                  // 핸들러 실행 중 블록할 시그널들
    int sa_flags;                      // 동작 옵션
    void (*sa_restorer)(void);         // 내부용 (사용 안 함)
};

void advanced_handler(int signo, siginfo_t *info, void *context) {
    printf(&quot;시그널: %d\n&quot;, signo);
    printf(&quot;보낸 프로세스 PID: %d\n&quot;, info-&gt;si_pid);
    printf(&quot;보낸 UID: %d\n&quot;, info-&gt;si_uid);
}

sa.sa_sigaction = advanced_handler;
sa.sa_flags = SA_SIGINFO;  // 이 플래그 필수</code></pre>
<h3 id="3-예제-안전한-핸들러">3. 예제: &quot;안전한 핸들러&quot;</h3>
<p>이 예제는 <code>SIGINT(Ctrl+C)</code>를 처리하는 도중에 <code>SIGQUIT(Ctrl+\)</code>가 들어와도 무시(블록)하고, 하던 일을 마친 뒤에 처리하는 안정성을 보여줍니다.</p>
<p>C</p>
<pre><code class="language-cpp">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;signal.h&gt;

void my_handler(int signo) {
    printf(&quot;\n[Handler] 시그널 %d번 처리 시작 (3초 소요)...\n&quot;, signo);
    printf(&quot;[Handler] 이 동안에는 Ctrl+\\ (SIGQUIT)을 눌러도 대기합니다.\n&quot;);

    for (int i = 0; i &lt; 3; i++) {
        printf(&quot;... 처리 중 %d\n&quot;, i + 1);
        sleep(1);
    }
    printf(&quot;[Handler] 처리 완료.\n&quot;);
}

int main() {
    struct sigaction act;

    // 1. 핸들러 함수 지정
    act.sa_handler = my_handler;

    // 2. 마스크 설정 (핸들러 실행 중 막을 시그널)
    sigemptyset(&amp;act.sa_mask);
    sigaddset(&amp;act.sa_mask, SIGQUIT); // SIGINT 처리 중엔 SIGQUIT을 블록함!

    // 3. 플래그 설정
    // SA_RESTART: 시그널 처리 후 중단된 시스템 콜(read, write 등)을 자동 재시작
    act.sa_flags = SA_RESTART; 

    // 4. 등록
    if (sigaction(SIGINT, &amp;act, NULL) == -1) {
        perror(&quot;sigaction&quot;);
        exit(1);
    }

    printf(&quot;PID: %d\n&quot;, getpid());
    printf(&quot;Ctrl+C를 눌러보세요. 핸들러 실행 중에 Ctrl+\\도 눌러보세요.\n&quot;);

    while (1) {
        printf(&quot;Main Loop...\n&quot;);
        sleep(1);
    }
    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/32d68080-f6f8-4f44-a799-179306a5e7dd/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d95dbc28-e6bf-425a-9d5c-63014518c7aa/image.png" /></p>
<h3 id="4-실행-및-결과">4. 실행 및 결과</h3>
<ol>
<li><code>Ctrl+C</code> 입력: <code>my_handler</code>가 실행되어 &quot;처리 중 1, 2, 3&quot;을 출력하기 시작함.</li>
<li>도중에 <code>Ctrl+\</code> 입력:<ul>
<li><code>signal()</code> 함수였다면: 핸들러가 멈추고 즉시 <code>Quit (core dumped)</code> 되며 죽음.</li>
<li><code>sigaction()</code> 결과: 아무 반응 없음 (블록됨). <code>my_handler</code>가 &quot;처리 완료&quot; 메시지를 띄우고 리턴된 직후에 <code>Quit</code> 시그널이 처리되어 종료됨.</li>
</ul>
</li>
</ol>
<h3 id="5-주요-flags-sa_flags">5. 주요 Flags (<code>sa_flags</code>)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/44e311cb-d0da-43e7-9b6d-89230439082d/image.png" /></p>
<ul>
<li><code>0</code>: 기본 동작.</li>
<li><code>SA_RESTART</code>: 시그널 때문에 끊긴 <code>read()</code>, <code>write()</code> 등을 에러(<code>EINTR</code>) 내지 않고 자동으로 재시작해줌. (매우 유용).</li>
<li><code>SA_SIGINFO</code>: 핸들러 함수 파라미터를 확장하여, 송신자 PID나 데이터를 받을 수 있게 함. (<code>sa_handler</code> 대신 <code>sa_sigaction</code> 사용).</li>
</ul>
<hr />
<hr />
<blockquote>
<p><em>reference</em> : <a href="https://reakwon.tistory.com/215#google_vignette">https://reakwon.tistory.com/215#google_vignette</a></p>
</blockquote>