<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/082db8b8-a8fb-4bd3-9a67-6f8b2e1fa5e2/image.png" /></p>
<hr />
<h3 id="1-주요-자료형-data-types">1. 주요 자료형 (Data Types)</h3>
<p><code>&lt;pthread.h&gt;</code>에 정의된 불투명(Opaque) 구조체들입니다. 직접 멤버 변수에 접근하지 말고 전용 함수를 써야 합니다.</p>
<table>
<thead>
<tr>
<th><strong>자료형</strong></th>
<th><strong>역할</strong></th>
<th><strong>실무 팁</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong><code>pthread_t</code></strong></td>
<td><strong>쓰레드 식별자 (ID)</strong></td>
<td><code>int</code>가 아닐 수 있으므로 비교 시 <code>==</code> 대신 <code>pthread_equal()</code> 사용 권장.</td>
</tr>
<tr>
<td><strong><code>pthread_mutex_t</code></strong></td>
<td><strong>뮤텍스 (잠금장치)</strong></td>
<td>공유 자원 보호용. <code>LOCK</code> -&gt; <code>CRITICAL SECTION</code> -&gt; <code>UNLOCK</code></td>
</tr>
<tr>
<td><strong><code>pthread_cond_t</code></strong></td>
<td><strong>조건 변수</strong></td>
<td>&quot;신호(Signal)&quot;를 기다릴 때 사용. 항상 뮤텍스와 짝으로 다님.</td>
</tr>
<tr>
<td><strong><code>pthread_attr_t</code></strong></td>
<td><strong>속성 객체</strong></td>
<td>스택 크기나 Detach 여부를 설정하고 <code>create</code> 할 때 넘겨줌.</td>
</tr>
<tr>
<td><strong><code>pthread_once_t</code></strong></td>
<td><strong>1회 초기화</strong></td>
<td>싱글톤 패턴이나 라이브러리 초기화에 사용 (<code>PTHREAD_ONCE_INIT</code> 필요).</td>
</tr>
</tbody></table>
<hr />
<h3 id="2-주요-api-핵심-함수">2. 주요 API (핵심 함수)</h3>
<p><strong>필수 헤더:</strong> <code>#include &lt;pthread.h&gt;</code> (sched.h는 스케줄링 정책 정의용)</p>
<h4 id="a-쓰레드-제어">A. 쓰레드 제어</h4>
<table>
<thead>
<tr>
<th><strong>함수</strong></th>
<th><strong>설명</strong></th>
<th><strong>비유</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong><code>pthread_create</code></strong></td>
<td><strong>쓰레드 생성</strong></td>
<td>직원 고용. (성공 시 0 반환).</td>
</tr>
<tr>
<td><strong><code>pthread_join</code></strong></td>
<td><strong>종료 대기 (Blocking)</strong></td>
<td>직원이 퇴근할 때까지 문 앞에서 기다림. (자원 회수 필수).</td>
</tr>
<tr>
<td><strong><code>pthread_detach</code></strong></td>
<td><strong>독립 실행 (Non-blocking)</strong></td>
<td>&quot;알아서 하고 퇴근해.&quot; (종료 시 자동 자원 회수). <code>join</code> 불가.</td>
</tr>
<tr>
<td><strong><code>pthread_exit</code></strong></td>
<td><strong>스스로 종료</strong></td>
<td>직원이 &quot;저 먼저 갑니다&quot; 하고 나감.</td>
</tr>
<tr>
<td><strong><code>pthread_self</code></strong></td>
<td><strong>내 ID 확인</strong></td>
<td>&quot;내 사원증 번호가 뭐지?&quot;</td>
</tr>
</tbody></table>
<h4 id="b-동기화-뮤텍스">B. 동기화 (뮤텍스)</h4>
<p>뮤텍스란 동시에 한 스레드만 특정 코드 영역에 들어가게 만드는 공유 자원을 보호하기 위한 도구입니다.
코드 영역에 접근하는 것을 잠구거나 풀어서 공유 자원을 보호하는 역할을 합니다.</p>
<ul>
<li><code>pthread_mutex_init</code> / <code>destroy</code>: 생성 및 소멸</li>
<li><code>pthread_mutex_lock</code> / <code>unlock</code>: 잠그기 및 풀기</li>
</ul>
<hr />
<h3 id="3-쓰레드-기본-속성-pthread_attr_init">3. 쓰레드 기본 속성 (<code>pthread_attr_init</code>)</h3>
<p><code>pthread_create</code>의 두 번째 인자로 <code>NULL</code>을 주면 아래 기본값들이 적용됩니다.</p>
<table>
<thead>
<tr>
<th><strong>속성 (Attribute)</strong></th>
<th><strong>기본값 (Default)</strong></th>
<th><strong>설명</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>Detach State</strong></td>
<td><code>PTHREAD_CREATE_JOINABLE</code></td>
<td><strong>[중요]</strong> 기본적으로 <code>join</code>을 해줘야 메모리가 반환됨.</td>
</tr>
<tr>
<td><strong>Scope</strong></td>
<td><code>PTHREAD_SCOPE_SYSTEM</code></td>
<td>(리눅스 NPTL 기준) 커널이 1:1로 스케줄링함.</td>
</tr>
<tr>
<td><strong>Inherit Sched</strong></td>
<td><code>PTHREAD_INHERIT_SCHED</code></td>
<td>부모(생성한 쓰레드)의 우선순위를 그대로 물려받음.</td>
</tr>
<tr>
<td><strong>Sched Policy</strong></td>
<td><code>SCHED_OTHER</code></td>
<td>일반적인 시분할(Time-sharing) 스케줄링 (비실시간).</td>
</tr>
<tr>
<td><strong>Stack Size</strong></td>
<td>시스템 기본값 (약 2MB~8MB)</td>
<td>임베디드에서는 메모리 아끼려고 이 값을 줄여서(<code>attr</code> 설정) 생성함.</td>
</tr>
</tbody></table>
<blockquote>
<p><strong>참고:</strong> 리눅스(NPTL)는 <code>PTHREAD_SCOPE_PROCESS</code>를 지원하지 않습니다. (항상 커널 레벨 스케줄링).</p>
</blockquote>
<hr />
<h3 id="4-실전-요약-코드-skeleton">4. 실전 요약 코드 (Skeleton)</h3>
<pre><code class="language-c">#include &lt;pthread.h&gt;
#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;

// 쓰레드가 실행할 함수
void* worker_routine(void* arg) {
    int id = *(int*)arg;
    printf(&quot;[Thread] 일하는 중... (ID: %lu)\n&quot;, pthread_self());
    return NULL;
}

int main() {
    pthread_t thread;
    int arg = 100;

    // 1. 쓰레드 생성 (기본 속성 NULL 사용)
    if (pthread_create(&amp;thread, NULL, worker_routine, &amp;arg) != 0) {
        perror(&quot;Create failed&quot;);
        return 1;
    }

    // 2. 메인 쓰레드는 기다림 (Joinable 상태이므로 필수)
    pthread_join(thread, NULL);

    printf(&quot;[Main] 쓰레드가 종료되었습니다.\n&quot;);
    return 0;
}</code></pre>
<h3 id="5-컴파일-주의사항">5. 컴파일 주의사항</h3>
<p>Pthreads는 표준 라이브러리(<code>libc</code>)에 포함되지 않는 경우가 많아, <strong>링크 옵션을 꼭!</strong> 줘야 합니다.</p>
<pre><code class="language-bash">gcc -o my_app my_app.c -pthread
# 또는
gcc -o my_app my_app.c -lpthread</code></pre>
<hr />
<h3 id="6-예제--쓰레드-종료-대기pthread_join-관련">6. 예제 : 쓰레드 종료 대기(pthread_join) 관련</h3>
<table>
<thead>
<tr>
<th><strong>함수</strong></th>
<th><strong>설명</strong></th>
<th><strong>비유</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong><code>pthread_join</code></strong></td>
<td><strong>종료 대기 (Blocking)</strong></td>
<td>직원이 퇴근할 때까지 문 앞에서 기다림. (자원 회수 필수).</td>
</tr>
</tbody></table>
<p><code>pthread_join</code> 함수는 목차 <a href="https://api.velog.io/rss/@mommers#2-%EC%A3%BC%EC%9A%94-api-%ED%95%B5%EC%8B%AC-%ED%95%A8%EC%88%98">2번</a> 에서 봤던 주요 api 핵심 함수 중 하나이다.</p>
<ul>
<li>join을 하지 않으면 메인 스레드가 먼저 종료될 수 있다.</li>
<li>join을 통해 자식 스레드의 반환값을 받을 수 있다.</li>
</ul>
<p>아래 예제를 통해 스레드의 종료 대기 및 자원 회수 메커니즘에 대해 알아보자.</p>
<h4 id="코드">코드</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;pthread.h&gt;
#include &lt;string.h&gt;
#include &lt;stdint.h&gt;

//#define _GNU_SOURCE         /* See feature_test_macros(7) */
#include &lt;unistd.h&gt;
#include &lt;sys/syscall.h&gt;

void *thread_function(void *arg);

int main() {
    int status;
    pthread_t tid;
    void *return_value;
    int i;


    status = pthread_create(&amp;tid, NULL, thread_function, &quot;hello thread\n&quot;);
    if(status !=0){
        perror(&quot;pthread_create&quot;);
        exit(1);
    }

    for(i=1; i&lt;=5; i++){
        printf(&quot;Parent thread %d!!\n&quot;, i);
        sleep(1);
    }

    //
    status = pthread_join(tid, &amp;return_value);
    if(status != 0){
        perror(&quot;pthread_join&quot;);
        exit(1);
    }
    printf(&quot;Thread joined, it returned %s\n&quot;, (char *)return_value); 
    // printf(&quot;Thread joined, it returned %ld\n&quot;, (uintptr_t)return_value); 

    return 0;
}

void *thread_function(void *arg){
    int i;
    pid_t * tpid;
    pthread_t * thread_id;

    tpid=malloc(sizeof(pid_t));
    thread_id=malloc(sizeof(pthread_t));

    *tpid = syscall(SYS_gettid);
    printf(&quot;Thread LWP: %d, Thread PID: %d\n&quot;, *tpid, getpid());

    *thread_id = pthread_self();
    printf(&quot;Thread ID: %lu\n&quot;, *thread_id);

    for(i=1; i&lt;=10; i++){
        printf(&quot;\t\tChild thread %d\n&quot;, i);
        sleep(1);
    }
    pthread_exit(&quot;Good Bye&quot;);
    // return (void *)1;
    //pthread_exit((void *)0);
}</code></pre>
<hr />
<h4 id="6-1-실행-결과-분석-null이-나온-이유">6-1) 실행 결과 분석 (null이 나온 이유)</h4>
<p>마지막 출력 결과가 <code>Thread joined, it returned (null)</code>인 이유는 코드 마지막 줄 때문입니다.</p>
<pre><code class="language-c">// 실제 실행된 코드
pthread_exit((void *)0);</code></pre>
<ul>
<li><code>0</code>은 주소로 치면 <code>NULL</code>입니다.</li>
<li>메인 함수의 <code>printf(&quot;%s&quot;, ...)</code>가 <code>NULL</code> 포인터를 받아서 <code>(null)</code>이라고 출력한 것입니다.</li>
<li>만약 주석 처리된 <code>pthread_exit(&quot;Good Bye&quot;);</code>를 풀었다면, &quot;Thread joined, it returned Good Bye&quot;가 출력되었을 것입니다.</li>
</ul>
<hr />
<h4 id="6-2-pthread_join의-void-이중-포인터-이해하기">6-2) <code>pthread_join</code>의 <code>void</code> (이중 포인터) 이해하기</h4>
<ul>
<li>자식 쓰레드가 남긴 &quot;데이터의 주소(<code>void *</code>)&quot;를 받아오고 싶을 때 사용한다.</li>
<li>내가 가진 포인터 변수(<code>return_value</code>)의 주소(<code>&amp;return_value</code>)를 줘야, 함수가 그 안에 자식의 주소를 채워줄 수 있다.</li>
</ul>
<pre><code class="language-c">void *ptr;          // 1. 자식의 보물을 가리킬 빈 지도
pthread_join(tid, &amp;ptr); // 2. &quot;이 지도에 보물 위치 좀 적어줘&quot; (지도의 주소를 넘김)
// 3. 이제 ptr은 자식이 리턴한 값을 가리킴</code></pre>
<hr />
<h4 id="6-3-pthread_exit-vs-return">6-3) <code>pthread_exit()</code> vs <code>return</code></h4>
<p>쓰레드 함수(<code>thread_function</code>) 끝에서 두 방식은 동일하게 동작합니다.</p>
<ol>
<li><code>return (void*)val;</code>: C언어 문법. 함수가 끝나면서 값을 반환.</li>
<li><code>pthread_exit((void*)val);</code>: 쓰레드 전용 함수. 명시적으로 종료 알림.</li>
</ol>
<p>차이점: <code>pthread_exit</code>는 함수 깊은 곳(중첩된 함수)에서 호출해도 즉시 쓰레드를 종료시킬 수 있습니다.</p>
<hr />
<h4 id="6-4-좀비-쓰레드-zombie-thread-주의">6-4) 좀비 쓰레드 (Zombie Thread) 주의</h4>
<p><code>joinable</code> 쓰레드를 <code>join</code> 하지 않으면 좀비가 됩니다.</p>
<ul>
<li>살아있을 때: 스택(Stack) + 레지스터 등 자원 사용.</li>
<li>죽었지만 join 안 함 (좀비): 종료 코드(Exit Code)를 담은 최소한의 메모리가 커널에 계속 남음.</li>
</ul>
<h4 id="해결방법">해결방법</h4>
<ol>
<li>반드시 <code>pthread_join()</code>을 호출한다.</li>
<li>또는 <code>pthread_detach()</code>로 &quot;결과 필요 없으니 알아서 사라져&quot;라고 설정한다.</li>
</ol>
<hr />
<h4 id="6-5-코드-개선-팁-메모리-누수-방지">6-5) 코드 개선 팁 (메모리 누수 방지)</h4>
<p><code>thread_function</code> 내부의 <code>malloc</code>은 <code>free</code> 되지 않았습니다. 아래처럼 자원을 정리하거나, <code>join</code>한 곳에서 <code>free</code> 할 수 있도록 리턴해줘야 합니다.</p>
<p>C</p>
<pre><code class="language-c">void *thread_function(void *arg){
    // ... (생략) ...
    // tpid, thread_id를 malloc 했지만 리턴하지 않고 함수가 끝남 -&gt; Memory Leak

    // 해결책 1: 다 썼으면 해제하기
    free(tpid);
    free(thread_id);

    pthread_exit(&quot;Good Bye&quot;);
}</code></pre>