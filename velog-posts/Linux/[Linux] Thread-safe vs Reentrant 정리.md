<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b25dca9d-e8bf-4728-9e52-382a0268ff4b/image.png" /></p>
<h3 id="thread-safe-vs-reentrant-정리">Thread-safe vs Reentrant 정리</h3>
<ul>
<li><code>Thread-safe</code> : 여러 쓰레드가 동시에 호출해도 안전함 (주로 Lock/Mutex 사용)</li>
<li><code>Reentrant</code> : 실행 도중 중단되었다가 다시 호출되어도 안전함 (공유 상태 사용 금지)</li>
<li>일반적으로 Reentrant 함수는 Thread-safe하다. 그러나 Thread-safe 함수가 반드시 Reentrant인 것은 아니다.</li>
</ul>
<hr />
<h3 id="2-thread-safe">2. Thread-safe</h3>
<p>여러 스레드가 동시에 실행해도 데이터 레이스가 발생하지 않도록 보호된 함수.</p>
<p>예시:</p>
<pre><code class="language-c">int g_cnt = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void thread_safe_func() {
    pthread_mutex_lock(&amp;lock);
    g_cnt++;
    pthread_mutex_unlock(&amp;lock);
}</code></pre>
<p>특징:</p>
<ul>
<li>공유 자원 접근 시 Lock 사용 가능</li>
<li>동시 실행은 안전</li>
<li>인터럽트 중 재진입 시 Deadlock 가능</li>
</ul>
<hr />
<h3 id="3-reentrant">3. Reentrant</h3>
<p>함수가 실행 도중 인터럽트되거나 시그널 핸들러에서 다시 호출되어도 안전한 함수.</p>
<p>조건:</p>
<ul>
<li>전역 변수 사용 금지</li>
<li>static 변수 사용 금지</li>
<li>Lock 사용 금지</li>
<li>모든 상태는 호출자가 제공</li>
</ul>
<p>예시:</p>
<pre><code class="language-c">void reentrant_func(int *counter) {
    (*counter)++;
}</code></pre>
<p>특징:</p>
<ul>
<li>오직 인자와 지역 변수만 사용</li>
<li>중단 후 재진입 가능</li>
<li>인터럽트 환경에서도 안전</li>
</ul>
<hr />
<h3 id="4-대표적인-예시-strtok-vs-strtok_r">4. 대표적인 예시: strtok vs strtok_r</h3>
<hr />
<h3 id="4-1-strtok-non-reentrant-not-thread-safe">4-1) strtok (Non-reentrant, Not Thread-safe)</h3>
<ul>
<li>내부 static 변수를 사용</li>
<li>여러 스레드에서 동시에 사용하면 충돌 발생</li>
</ul>
<h3 id="4-2-strtok_r-reentrant">4-2) strtok_r (Reentrant)</h3>
<ul>
<li>상태 저장용 포인터를 호출자가 직접 관리</li>
<li>스택 기반 상태 관리</li>
<li>Thread-safe 및 Reentrant</li>
</ul>
<hr />
<h3 id="5-async-signal-safe-개념">5. Async-Signal-Safe 개념</h3>
<p>시그널 핸들러 내부에서 호출 가능한 함수 집합.</p>
<p>중요:</p>
<ul>
<li>printf, malloc, free 등은 대부분 Async-Signal-Safe가 아님</li>
<li>signal handler 안에서 호출하면 Undefined Behavior 가능</li>
<li>POSIX에서 안전하다고 명시한 함수만 사용해야 함 (예: write, _exit 등)</li>
</ul>
<hr />
<h3 id="결론">결론</h3>
<h4 id="1-thread-safe-동시에-여러-명이-써도-되는가">1. Thread-safe: &quot;동시에 여러 명이 써도 되는가?&quot;</h4>
<p>→ YES (Mutex 써서 줄 세워도 됨).</p>
<h4 id="2-reentrant-쓰다가-중간에-멈추고-다시-처음부터-실행해도-되는가">2. Reentrant: &quot;쓰다가 중간에 멈추고, 다시 처음부터 실행해도 되는가?&quot;</h4>
<p>→ YES (Mutex 쓰면 안 됨, 오직 Stack만 사용).</p>
<h4 id="3-임베디드시스템-개발자라면">3. 임베디드/시스템 개발자라면</h4>
<ul>
<li>인터럽트 핸들러나 시그널 핸들러 내부에서는 반드시 Reentrant 함수(Async-Signal-Safe)만 호출해야 한다.</li>
<li>printf, malloc 등은 대부분 Non-reentrant이므로 사용하면 안 된다.</li>
<li>멀티스레드 환경에서는 Thread-safe만으로 충분할 수 있지만, 인터럽트/시그널 환경에서는 Reentrant + Async-Signal-Safe가 필수이다.</li>
</ul>