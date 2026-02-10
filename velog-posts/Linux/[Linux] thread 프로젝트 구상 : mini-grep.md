<p>병렬 처리와 Thread 동기화에 대한 1~2시간을 투자한 미니 프로젝트를 구성해보았습니다.</p>
<p>저희는 멀티스레드 파일 검색기(mini-grep)을 만들어보고자 하였습니다.</p>
<hr />
<h3 id="멀티스레드-파일-검색기-mini-grep">멀티스레드 파일 검색기 (mini-grep)</h3>
<h3 id="1️⃣-프로젝트-소개">1️⃣ 프로젝트 소개</h3>
<p><strong><code>특정 키워드</code></strong>를 포함한 파일을 빠르게 찾는 멀티스레드 프로그램</p>
<pre><code class="language-bash">./mini-grep [PATH] [TODO]</code></pre>
<p><code>[PATH]</code> 하위 경로의 문자열 <code>[TODO]</code>가 포함된 모든 파일 찾기</p>
<h3 id="왜-만들었나">왜 만들었나?</h3>
<ul>
<li>큰 프로젝트에서 TODO, FIXME 주석 찾기</li>
<li>순차 검색은 느림 → 멀티스레드로 해결</li>
</ul>
<hr />
<h3 id="2️⃣-핵심-기술">2️⃣ 핵심 기술</h3>
<h3 id="thread-pool-방식-4개-core-8개-worker">Thread Pool 방식 (4개 Core, 8개 Worker)</h3>
<p><strong>1. 싱글스레드 (순차)</strong></p>
<pre><code>========================
파일1 → 파일2 → 파일3 → ... → 파일100
========================
(느림 😴)</code></pre><p><strong>2. 멀티스레드 (병렬)</strong></p>
<pre><code>================
Thread1: 파일 1, 9, 17, 25...
Thread2: 파일 2, 10, 18, 26...
Thread3: 파일 3, 11, 19, 27...
...
Thread8: 파일 8, 16, 24, 32...
================
(빠름 ⚡)</code></pre><h3 id="핵심-구현">핵심 구현</h3>
<ul>
<li><strong>Queue 기반 작업 분배 (FIFO)</strong></li>
<li><strong>Mutex로 동기화</strong></li>
<li><strong>Condition Variable 사용</strong><ul>
<li>큐에 작업이 없으면 스레드를 잠재움 (CPU 낭비 방지)</li>
<li>새 작업이 추가되면 대기 중인 스레드를 깨움</li>
</ul>
</li>
</ul>
<hr />
<h3 id="3️⃣-코드-구조">3️⃣ 코드 구조</h3>
<h3 id="자료구조">자료구조</h3>
<pre><code class="language-c">typedef struct {
    char **buf;            // 동적 파일 경로 배열
    size_t cap;            // 버퍼 용량 (자동 확장)
    size_t head;           // pop 위치
    size_t tail;           // push 위치
    size_t count;          // 현재 작업 수
    int scan_done;         // 탐색 완료 플래그

    pthread_mutex_t lock;
    pthread_cond_t  cond;
} TaskQueue;</code></pre>
<h3 id="동작-흐름">동작 흐름</h3>
<ol>
<li><strong>Main Thread</strong> → 디렉터리 재귀 탐색 후 Queue에 파일 추가 (Producer)</li>
<li><strong>Worker Threads 8개</strong> 생성 (Consumer)</li>
<li>먼저 끝난 스레드가 다음 작업 가져감</li>
<li>모든 파일 처리 완료 후 종료</li>
</ol>
<hr />
<h3 id="4️⃣-성능-비교">4️⃣ 성능 비교</h3>
<h3 id="1-결과에서_500개-제한-초기-버전">1. 결과에서_500개 제한 (초기 버전)</h3>
<ul>
<li>파일: 80개 (.c, .txt, .h, .py, .md)</li>
<li>CPU: Raspberry Pi 5 (4 cores)</li>
</ul>
<table>
<thead>
<tr>
<th>방식</th>
<th>소요 시간</th>
<th>파일당 시간</th>
<th>결과</th>
</tr>
</thead>
<tbody><tr>
<td>싱글 스레드</td>
<td>0.003초</td>
<td>약 37.5 μs</td>
<td>기준</td>
</tr>
<tr>
<td>멀티 스레드</td>
<td>0.003초</td>
<td>약 37.5 μs</td>
<td>비슷함</td>
</tr>
</tbody></table>
<p><strong>멀티 vs 싱글 비교</strong> → 성능 차이 없음 (파일 수가 너무 적음)</p>
<hr />
<h3 id="2-결과에서_파일-개수-제한-없음-최종-버전">2. 결과에서_파일 개수 제한 없음 (최종 버전)</h3>
<ul>
<li>파일: 40,127개 (.c, .txt, .h, .py, .md)</li>
<li>CPU: Raspberry Pi 5 (4 cores)</li>
</ul>
<table>
<thead>
<tr>
<th>방식</th>
<th>소요 시간</th>
<th>파일당 시간</th>
<th>결과</th>
</tr>
</thead>
<tbody><tr>
<td>싱글 스레드</td>
<td>0.316초</td>
<td>약 7.88 μs</td>
<td>기준</td>
</tr>
<tr>
<td>멀티 스레드</td>
<td>0.146초</td>
<td>약 3.64 μs</td>
<td><strong>53.8% 빨라짐</strong></td>
</tr>
</tbody></table>
<p><strong>멀티 vs 싱글 비교</strong> → <strong>약 2.16배 빠름</strong></p>
<h3 id="왜-빠른가">왜 빠른가?</h3>
<ul>
<li><strong>싱글</strong>: CPU 1개만 사용</li>
<li><strong>멀티</strong>: CPU 4개 모두 활용</li>
<li>이론상 4배 빨라야 하지만, <strong>실제 2.16배</strong><ul>
<li>동기화 오버헤드 (Mutex, Condition Variable)</li>
<li>파일 I/O 경합</li>
</ul>
</li>
</ul>
<hr />
<h3 id="5️⃣-핵심-코드-설명">5️⃣ 핵심 코드 설명</h3>
<pre><code class="language-c">void* worker_thread(void* arg) {
    while (1) {
        pthread_mutex_lock(&amp;q-&gt;lock);

        // 작업이 없으면 대기
        while (q-&gt;count == 0 &amp;&amp; !q-&gt;scan_done) {
            pthread_cond_wait(&amp;q-&gt;cond, &amp;q-&gt;lock);
        }

        // 작업 가져오기
        char* filepath = queue_pop(q);
        pthread_mutex_unlock(&amp;q-&gt;lock);

        if (filepath) {
            search_file(filepath, keyword);
            free(filepath);
        }
    }
}</code></pre>
<h3 id="핵심">핵심</h3>
<ul>
<li><strong>Queue 접근 시 Mutex 사용</strong> → 동시 접근 방지</li>
<li><strong>검색 시 Mutex 해제</strong> → 병렬 처리</li>
<li><strong>Condition Variable로 대기</strong> → CPU 낭비 방지</li>
</ul>
<hr />
<h3 id="6️⃣-실행-결과">6️⃣ 실행 결과</h3>
<h3 id="싱글스레드-vs-멀티스레드-비교">싱글스레드 vs 멀티스레드 비교</h3>
<p><strong>📌 테스트 환경</strong></p>
<ul>
<li>검색 경로: <code>/home/pi</code> (40,127개 파일)</li>
<li>검색 키워드: <code>&quot;TODO&quot;</code></li>
<li>하드웨어: Raspberry Pi 5 (4 cores)</li>
</ul>
<h4 id="싱글스레드-실행">싱글스레드 실행</h4>
<pre><code class="language-bash">$ ./single-mini-grep /home/pi TODO
=== 싱글스레드 파일 검색기 ===
검색 경로: /home/pi
검색 키워드: &quot;TODO&quot;

📁 파일 탐색 + 검색 중...

매칭: /home/pi/project/example.c
  크기: 3184 bytes
  수정: 2026-02-03 10:19:32
    12:  * TODO: This filter does NOT block socketcall()

매칭: /home/pi/project/main.c
  크기: 9965 bytes
  수정: 2026-02-05 17:08:12
   285:         printf(&quot;예시: %s /home/pi/project \&quot;TODO\&quot;\n&quot;, argv[0]);

========================================
검색 완료!
총 40127개 파일 스캔, 33개 파일에서 매칭
소요 시간: 0.317초
========================================</code></pre>
<h4 id="멀티스레드-실행-8-workers">멀티스레드 실행 (8 Workers)</h4>
<pre><code class="language-bash">$ ./mini-grep /home/pi TODO
=== 멀티스레드 파일 검색기 ===
검색 경로: /home/pi
검색 키워드: &quot;TODO&quot;
스레드 개수: 8

📁 파일 탐색 + 검색 중...

[Thread 5] 매칭: /home/pi/project/example.c
  크기: 3184 bytes
  수정: 2026-02-03 10:19:32
    13:  * TODO: This filter does NOT block socketcall()

[Thread 3] 매칭: /home/pi/project/main.c
  크기: 9965 bytes
  수정: 2026-02-05 17:08:12
   250:         printf(&quot;예시: %s /home/pi/project \&quot;TODO\&quot;\n&quot;, argv[0]);

[Thread 7] 매칭: /home/pi/project/utils.c
  크기: 5539 bytes
  수정: 2026-02-06 08:47:47
    14:  *   ./mini_grep_mt /path &quot;TODO&quot;

========================================
검색 완료!
총 40129개 파일 스캔, 35개 파일에서 매칭
소요 시간: 0.133초
========================================</code></pre>
<h3 id="핵심-차이점">핵심 차이점</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>싱글스레드</th>
<th>멀티스레드</th>
<th>차이</th>
</tr>
</thead>
<tbody><tr>
<td><strong>소요 시간</strong></td>
<td>0.317초</td>
<td>0.133초</td>
<td><strong>2.38배 빠름</strong></td>
</tr>
<tr>
<td><strong>출력 형식</strong></td>
<td>순차적</td>
<td><code>[Thread N]</code> 태그</td>
<td>병렬 처리 확인</td>
</tr>
<tr>
<td><strong>스캔 파일</strong></td>
<td>40,127개</td>
<td>40,129개</td>
<td>거의 동일</td>
</tr>
<tr>
<td><strong>CPU 사용률</strong></td>
<td>~25% (1코어)</td>
<td>~95% (4코어 모두)</td>
<td>효율적 활용</td>
</tr>
</tbody></table>
<hr />
<h3 id="적용-기술">적용 기술</h3>
<ul>
<li><strong>Thread Pool</strong> (Producer-Consumer 패턴)</li>
<li><strong>동적 Queue</strong> (자동 확장)</li>
<li><strong>Mutex 동기화</strong></li>
<li><strong>Condition Variable</strong></li>
</ul>
<p>→ <strong>파일 4만개 기준 약 2.16배 성능 향상</strong></p>
<hr />
<p>코드 : <a href="https://github.com/kyoung-mo/mini-grep-multithread">github(mini-grep-multithread)</a></p>