<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b1bf162d-448a-4440-8c35-5684a59eaa94/image.svg" /></p>
<hr />
<h3 id="쓰레드thread">쓰레드(Thread)</h3>
<p>메모리(Code, Data, Heap)는 공유하되, 실행 흐름(Stack)만 따로 가지는 경량 프로세스(LWP)</p>
<hr />
<h3 id="1-리눅스-커널이-보는-쓰레드-lwp">1. 리눅스 커널이 보는 쓰레드 (LWP)</h3>
<p>사용자가 제공한 텍스트의 핵심입니다. 리눅스 커널은 '쓰레드'라는 별도의 객체를 모릅니다.</p>
<p>User 관점: &quot;쓰레드&quot; (하나의 프로그램 안에서 여러 함수가 동시에 도는 것)</p>
<p>Kernel 관점: &quot;LWP (Light Weight Process)&quot;</p>
<ul>
<li>커널 입장에서는 그냥 프로세스(task_struct)입니다. 단, &quot;부모와 메모리 방을 같이 쓰도록(공유하도록)&quot; 설정된 특이한 프로세스일 뿐입니다.</li>
<li>리눅스 시스템 콜 <code>clone()</code>을 호출할 때 <code>CLONE_VM</code>, <code>CLONE_FS</code> 등의 플래그를 켜서 생성합니다.</li>
</ul>
<hr />
<h3 id="2-메모리-구조">2. 메모리 구조</h3>
<p>쓰레드와 일반 프로세스의 결정적 차이는 &quot;무엇을 공유하는가&quot;입니다.</p>
<ul>
<li>코드 : 하나만 있으면 됨</li>
<li>데이터 : 전역변수</li>
<li>힙 : malloc -&gt; 모든 쓰레드가 접근 가능</li>
<li>스택 : 각 쓰레드는 서로 다른 함수 실행</li>
</ul>
<table>
<thead>
<tr>
<th>영역</th>
<th>공유 여부</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>Code</td>
<td>공유함</td>
<td>프로그램 코드는 하나만 있으면 됨.</td>
</tr>
<tr>
<td>Data</td>
<td>공유함</td>
<td>전역 변수(Global Variable)를 통해 쓰레드 간 통신 가능 (IPC 불필요).</td>
</tr>
<tr>
<td>Heap</td>
<td>공유함</td>
<td><code>malloc</code>으로 잡은 메모리는 모든 쓰레드가 접근 가능.</td>
</tr>
<tr>
<td>Stack</td>
<td>독립적</td>
<td>(핵심) 각 쓰레드는 서로 다른 함수를 실행하므로, 지역 변수와 함수 호출 기록은 따로 가져야 함.</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-프로세스-vs-쓰레드-비교">3. 프로세스 vs 쓰레드 비교</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/444aaa9a-b66e-4f53-b4fa-88acaa042211/image.png" /></p>
<table>
<thead>
<tr>
<th>비교 항목</th>
<th>프로세스 (Process)</th>
<th>쓰레드 (Thread / LWP)</th>
</tr>
</thead>
<tbody><tr>
<td>생성 비용</td>
<td>상대적으로 비쌈 (메모리 구조 전체 복사)</td>
<td>저렴 (메모리 포인터만 복사)</td>
</tr>
<tr>
<td>통신 방법</td>
<td>어렵다 (IPC: 파이프, 소켓 등 필요)</td>
<td>쉽다 (전역 변수, 힙 메모리 직접 접근)</td>
</tr>
<tr>
<td>문맥 전환</td>
<td>느림 (캐시/TLB 비워야 함)</td>
<td>빠름 (메모리 맵이 같아서 캐시 유지 유리)</td>
</tr>
<tr>
<td>안전성</td>
<td>하나 죽어도 다른 프로세스 영향 없음</td>
<td>하나 죽으면(Segfault) 프로세스 전체 사망</td>
</tr>
</tbody></table>
<hr />
<h3 id="4-pthread-예제">4. pthread 예제</h3>
<p>전역 변수를 공유한다는 특징을 보여주는 간단한 예제</p>
<pre><code class="language-c">#include &lt;pthread.h&gt;
#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;

// [Data 영역] 모든 쓰레드가 공유하는 전역 변수
int g_counter = 0; 

void* worker(void* arg) {
    // [Stack 영역] 이 변수는 이 쓰레드만 가짐
    int local_val = 0; 

    g_counter++; // 옆 쓰레드와 같이 쓰는 변수 수정
    printf(&quot;쓰레드 실행 중... 공유값: %d\n&quot;, g_counter);
    return NULL;
}

int main() {
    pthread_t t1, t2;

    // 쓰레드(=LWP) 생성
    pthread_create(&amp;t1, NULL, worker, NULL);
    pthread_create(&amp;t2, NULL, worker, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return 0;
}</code></pre>
<hr />
<p>실행 결과</p>
<pre><code class="language-bash">쓰레드 실행 중... 공유값: 1
쓰레드 실행 중... 공유값: 2
[1] + Done                       &quot;/usr/bin/gdb&quot; --interpreter=mi --tty=${DbgTerm} 0&lt;&quot;/tmp/Microsoft-MIEngine-In-2eya5ony.p44&quot; 1&gt;&quot;/tmp/Microsoft-MIEngine-Out-2l3o11ba.oxb&quot;</code></pre>
<hr />
<h3 id="4-2-10000개의-쓰레드를-돌리는-simple_thread">4-2) 10000개의 쓰레드를 돌리는 simple_thread</h3>
<pre><code class="language-c">#include &lt;pthread.h&gt;
#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#define thread_count 10000

// [Data 영역] 모든 쓰레드가 공유하는 전역 변수
int g_counter = 0; 

void* worker(void* arg) {
    // [Stack 영역] 이 변수는 이 쓰레드만 가짐
    int local_val = 0; 
    long my_id=(long)arg;

    printf(&quot;Thread : %ld &quot;, my_id);

    g_counter++; // 옆 쓰레드와 같이 쓰는 변수 수정
    printf(&quot;쓰레드 실행 중... 공유값: %d\n&quot;, g_counter);
    return NULL;
}

int main() {
    pthread_t t[thread_count];

    // 쓰레드(=LWP) 생성
    for (size_t i = 0; i &lt; thread_count; i++)
    {
        pthread_create(&amp;t[i], NULL, worker, (void*)i);
    }


    for (size_t i = 0; i &lt; thread_count; i++)
    {
        pthread_join(t[i], NULL);
    }



    return 0;
}</code></pre>
<hr />
<p>실행 결과</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/51b3cf1c-cb65-47b7-84cc-66ca888651bd/image.png" /></p>
<hr />
<blockquote>
<p>사진 출처 : <a href="https://rhksgml78.tistory.com/m/379">https://rhksgml78.tistory.com/m/379</a></p>
</blockquote>