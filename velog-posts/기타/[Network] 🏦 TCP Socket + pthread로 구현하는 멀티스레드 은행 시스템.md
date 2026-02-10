<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aa36e92d-0503-4e64-bad2-77b83bacb5cf/image.png" /></p>
<blockquote>
<p>TCP 소켓 프로그래밍과 POSIX 스레드를 활용한 실시간 은행 업무 처리 시스템 구현기</p>
</blockquote>
<h3 id="📌-프로젝트-개요">📌 프로젝트 개요</h3>
<p>TCP는 연결 지향형(Connection-oriented) 프로토콜로서, 신뢰성을 보장하는 1:1 통신이라는 특징이 있습니다. 이러한 특성이 마치 은행 창구에 방문하는 고객과 은행원의 상담 과정과 유사하다는 점에서 착안하여, 은행 창구 시스템을 구현해보았습니다.</p>
<h3 id="💡-핵심-아이디어">💡 핵심 아이디어</h3>
<pre><code>🏦 은행 = 서버 (메인 스레드 + 워커 스레드들)
👤 고객 = 클라이언트
🪟 창구 = 워커 스레드 (최대 5개)
🎫 대기열 = 원형 큐 구조</code></pre><hr />
<h3 id="🎯-시스템-설계">🎯 시스템 설계</h3>
<h3 id="시나리오-기반-설계">시나리오 기반 설계</h3>
<p>실제 은행 방문 경험을 시스템으로 옮겼습니다:</p>
<h4 id="1️⃣-처음-방문-db에-계정-없음">1️⃣ 처음 방문 (DB에 계정 없음)</h4>
<ul>
<li>입출금 업무 시도 → &quot;통장이 없습니다&quot;</li>
<li>통장 개설 안내 → 본인 계좌만 개설 가능</li>
<li>DB에 계정 추가</li>
</ul>
<h4 id="2️⃣-재방문-db에-계정-있음">2️⃣ 재방문 (DB에 계정 있음)</h4>
<ul>
<li>입금: 본인 또는 타인 계좌 가능</li>
<li>출금: 본인 계좌만 가능 (비밀번호 인증 필요)</li>
<li>통장 목록 조회 가능</li>
<li>추가 통장 개설 가능 (최대 5개)</li>
</ul>
<h4 id="3️⃣-창구-혼잡-상황">3️⃣ 창구 혼잡 상황</h4>
<ul>
<li>모든 창구(5개) 사용 중일 때</li>
<li>번호표 발급 및 대기 인원 안내</li>
<li>창구가 비면 순서대로 배정</li>
</ul>
<hr />
<h2 id="아키텍처">아키텍처</h2>
<h3 id="전체-구조">전체 구조</h3>
<pre><code>┌─────────────────────────────────────────────────┐
│              메인 스레드 (은행)               
│  - accept(): 클라이언트 연결 수락              
│  - IP 인증 (10.10.16.200~224)                
│  - 창구 배정 또는 대기 큐 추가                 
└──────────┬──────────────────────────────────────┘
           │
           ├─► 워커 스레드 1 (창구 1) ─► 클라이언트 A
           ├─► 워커 스레드 2 (창구 2) ─► 클라이언트 B
           ├─► 워커 스레드 3 (창구 3) ─► 클라이언트 C
           ├─► 워커 스레드 4 (창구 4) ─► 클라이언트 D
           ├─► 워커 스레드 5 (창구 5) ─► 클라이언트 E
           │
           └─► 대기 큐 (원형 큐)
                ├─ 클라이언트 F (1번째 대기)
                ├─ 클라이언트 G (2번째 대기)
                └─ ...</code></pre><h3 id="데이터-구조">데이터 구조</h3>
<h4 id="클라이언트-정보">클라이언트 정보</h4>
<pre><code class="language-c">typedef struct {
    char client_id[10];         // pi200 ~ pi224
    int ip_last_digit;          // IP 마지막 숫자 = 비밀번호
    Account accounts[5];        // 최대 5개 통장
    int account_count;          // 현재 통장 개수
} ClientInfo;</code></pre>
<h4 id="통장-정보">통장 정보</h4>
<pre><code class="language-c">typedef struct {
    char bank_name[50];         // 은행명
    int balance;                // 잔고
    bool is_active;             // 활성화 여부
} Account;</code></pre>
<hr />
<h2 id="통신-흐름도">통신 흐름도</h2>
<h3 id="정상-연결-시-창구-여유-있음">정상 연결 시 (창구 여유 있음)</h3>
<pre><code>클라이언트                    서버
    │                           │
    ├──► connect() ─────────────┤
    │                           ├─► IP 인증 (10.10.16.XXX)
    │                           ├─► 빈 창구 찾기
    │                           ├─► 워커 스레드 배정
    │                           │
    │◄──── 환영 메시지 ─────────┤
    │                           │
    ├──► &quot;통장 개설&quot; ───────────┤
    │◄──── &quot;은행명 입력&quot; ────────┤
    ├──► &quot;KB국민&quot; ──────────────┤
    │◄──── &quot;개설 완료&quot; ──────────┤
    │                           │
    ├──► &quot;입금&quot; ────────────────┤
    │◄──── &quot;대상 ID 입력&quot; ───────┤
    ├──► &quot;pi222&quot; ───────────────┤
    │◄──── &quot;통장 선택&quot; ──────────┤
    ├──► &quot;1&quot; ───────────────────┤
    │◄──── &quot;금액 입력&quot; ──────────┤
    ├──► &quot;100000&quot; ──────────────┤
    │◄──── &quot;입금 완료&quot; ──────────┤
    │                           │
    │◄──── &quot;추가 업무?&quot; ─────────┤
    ├──► &quot;아니요&quot; ──────────────┤
    │◄──── &quot;감사합니다&quot; ─────────┤
    │                           │
    └──► close() ───────────────┴─► 창구 반환</code></pre><h3 id="창구-만석-시-대기-큐-사용">창구 만석 시 (대기 큐 사용)</h3>
<pre><code>클라이언트                    서버
    │                           │
    ├──► connect() ─────────────┤
    │                           ├─► 모든 창구 사용 중!
    │                           ├─► 대기 큐에 추가
    │                           │
    │◄──── &quot;대기 중...&quot; ─────────┤
    │      (내 앞 대기: 2명)      │
    │                           │
    │        ... 대기 ...        │
    │                           │
    │                           ├─► 창구 1번 비워짐
    │                           ├─► dequeue() 호출
    │◄──── &quot;창구 준비 완료&quot; ─────┤
    │                           │
    └──► [정상 업무 진행] ───────┘</code></pre><hr />
<h3 id="보안-및-동기화">보안 및 동기화</h3>
<h3 id="mutex를-통한-동시성-제어">Mutex를 통한 동시성 제어</h3>
<h4 id="1-db-mutex">1. DB Mutex</h4>
<pre><code class="language-c">pthread_mutex_t db_mutex;  // 클라이언트 DB 보호

pthread_mutex_lock(&amp;db_mutex);
client-&gt;accounts[idx].balance += amount;  // 입금
pthread_mutex_unlock(&amp;db_mutex);</code></pre>
<p>보호 대상: </p>
<ul>
<li>통장 개설</li>
<li>입금/출금 시 잔고 변경</li>
<li>계좌 정보 조회</li>
</ul>
<h4 id="2-workers-mutex">2. Workers Mutex</h4>
<pre><code class="language-c">pthread_mutex_t workers_mutex;  // 워커 상태 관리

pthread_mutex_lock(&amp;workers_mutex);
workers[i].is_busy = true;  // 창구 배정
pthread_cond_broadcast(&amp;waiting_queue.cond);  // 모든 워커 깨우기
pthread_mutex_unlock(&amp;workers_mutex);</code></pre>
<p>보호 대상:</p>
<ul>
<li>워커 스레드 상태 (busy/idle)</li>
<li>창구 배정 작업</li>
</ul>
<h4 id="3-queue-mutex">3. Queue Mutex</h4>
<pre><code class="language-c">pthread_mutex_t queue_mutex;  // 대기 큐 보호

pthread_mutex_lock(&amp;waiting_queue.mutex);
waiting_queue.queue[rear] = client_fd;  // 대기 큐에 추가
waiting_queue.count++;
pthread_mutex_unlock(&amp;waiting_queue.mutex);</code></pre>
<p>보호 대상:</p>
<ul>
<li>대기 큐 삽입/삭제</li>
<li>대기 인원 카운트</li>
</ul>
<h3 id="조건-변수-활용">조건 변수 활용</h3>
<pre><code class="language-c">pthread_cond_t waiting_queue.cond;

// 워커 스레드: 업무 대기
pthread_cond_wait(&amp;waiting_queue.cond, &amp;workers_mutex);

// 메인 스레드: 워커 깨우기
pthread_cond_broadcast(&amp;waiting_queue.cond);</code></pre>
<hr />
<h3 id="주요-기능">주요 기능</h3>
<h3 id="1-통장-개설">1. 통장 개설</h3>
<ul>
<li>키워드: &quot;통장&quot; AND &quot;개설&quot; 모두 포함</li>
<li>제약: 본인만 가능, 최대 5개</li>
<li>초기 잔고: 0원</li>
</ul>
<pre><code>입력: 통장 개설하고 싶어요
&gt; KB국민
✅ 통장 개설 완료! (잔고: 0원)</code></pre><h3 id="2-입금">2. 입금</h3>
<ul>
<li>키워드: &quot;입금&quot;</li>
<li>대상: 본인 또는 타인</li>
<li>제약: 대상이 통장을 가지고 있어야 함</li>
</ul>
<pre><code>입력: 입금하려고요
&gt; pi222 (대상 ID)
&gt; 1 (통장 선택)
&gt; 100000 (금액)
✅ 입금 완료! (잔고: 100000원)</code></pre><h3 id="3-출금">3. 출금</h3>
<ul>
<li>키워드: &quot;출금&quot;</li>
<li>대상: 본인만</li>
<li>인증: 비밀번호 (IP 뒷 3자리)</li>
</ul>
<pre><code>입력: 출금할게요
&gt; 1 (통장 선택)
&gt; 222 (비밀번호)
&gt; 50000 (금액)
✅ 출금 완료! (잔고: 50000원)</code></pre><hr />
<h3 id="구현-세부사항">구현 세부사항</h3>
<h3 id="thread-pool-패턴">Thread Pool 패턴</h3>
<p>워커 스레드를 미리 생성하여 재사용하는 방식:</p>
<pre><code class="language-c">// 서버 시작 시 워커 스레드 5개 생성
for (int i = 0; i &lt; MAX_WORKERS; i++) {
    workers[i].worker_id = i + 1;
    workers[i].is_busy = false;
    pthread_create(&amp;workers[i].thread, NULL, worker_thread_func, &amp;workers[i]);
}</code></pre>
<p>장점:</p>
<ul>
<li>스레드 생성/소멸 오버헤드 제거</li>
<li>동시 처리 성능 향상</li>
<li>리소스 제어 용이</li>
</ul>
<h3 id="원형-큐-circular-queue">원형 큐 (Circular Queue)</h3>
<p>대기 고객을 FIFO 방식으로 관리:</p>
<pre><code class="language-c">typedef struct {
    int queue[MAX_QUEUE];
    int front;
    int rear;
    int count;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} WaitingQueue;</code></pre>
<p>연산:</p>
<ul>
<li><code>enqueue()</code>: 대기 큐에 추가</li>
<li><code>dequeue()</code>: 대기 큐에서 꺼내기</li>
<li>원형 구조로 메모리 효율적 사용</li>
</ul>
<h3 id="ip-기반-클라이언트-식별">IP 기반 클라이언트 식별</h3>
<pre><code class="language-c">ClientInfo* find_client_by_ip(char* ip) {
    int last_octet;
    sscanf(ip, &quot;10.10.16.%d&quot;, &amp;last_octet);  // 마지막 숫자 추출

    if (last_octet &gt;= 200 &amp;&amp; last_octet &lt;= 224) {
        return &amp;client_db[last_octet - 200];  // pi200 ~ pi224
    }
    return NULL;
}</code></pre>
<p>인증 시스템:</p>
<ul>
<li>IP 범위: <code>10.10.16.200</code> ~ <code>10.10.16.224</code> (총 25명)</li>
<li>비밀번호: IP 마지막 3자리</li>
<li>예: <code>10.10.16.222</code> → ID: <code>pi222</code>, PW: <code>222</code></li>
</ul>
<hr />
<h3 id="트러블슈팅">트러블슈팅</h3>
<h3 id="문제-1-두-번째-접속-시-메뉴-안-나오는-현상">문제 1: 두 번째 접속 시 메뉴 안 나오는 현상</h3>
<p>원인:</p>
<pre><code class="language-c">pthread_cond_signal(&amp;waiting_queue.cond);  // ❌ 하나만 깨움</code></pre>
<ul>
<li><code>pthread_cond_signal()</code>은 대기 중인 스레드 하나만 깨움</li>
<li>깨어난 스레드가 <code>is_busy=false</code>이면 다시 대기</li>
<li>정작 <code>is_busy=true</code>인 워커는 영원히 깨어나지 못함</li>
</ul>
<p>해결:</p>
<pre><code class="language-c">pthread_cond_broadcast(&amp;waiting_queue.cond);  // ✅ 모두 깨움</code></pre>
<ul>
<li>모든 워커를 깨운 후, 각 워커가 자신의 상태 확인</li>
<li><code>is_busy=true</code>인 워커만 작업 진행</li>
</ul>
<h3 id="문제-2-추가-업무-질문이-클라이언트에-표시되지-않음">문제 2: 추가 업무 질문이 클라이언트에 표시되지 않음</h3>
<p>원인:</p>
<pre><code class="language-c">// 서버가 보내는 메시지
&quot;💡 추가로 처리하실 업무가 있으신가요? (예/아니오): &quot;

// 클라이언트가 감지하는 패턴
if (strstr(buffer, &quot;(예/아니오):&quot;) != NULL)  // ❌ 띄어쓰기 차이</code></pre>
<p>해결:</p>
<pre><code class="language-c">if (strstr(buffer, &quot;예/아니오&quot;) != NULL)  // ✅ 괄호/콜론 제거</code></pre>
<h3 id="문제-3-stdin-버퍼-문제-사용자-입력-타이밍">문제 3: stdin 버퍼 문제 (사용자 입력 타이밍)</h3>
<p>원인:</p>
<ul>
<li>사용자가 프롬프트 전에 미리 타이핑</li>
<li>stdin 버퍼에 남아있다가 <code>fgets()</code> 호출 시 즉시 읽힘</li>
</ul>
<p>해결:</p>
<pre><code class="language-c">// 빈 입력 감지 및 재입력 요청
while (input[0] == '\n' &amp;&amp; strlen(input) &lt;= 1) {
    printf(&quot;(입력해주세요): &quot;);
    fflush(stdout);
    fgets(input, BUFFER_SIZE, stdin);
}</code></pre>
<hr />
<h3 id="성능-및-확장성">성능 및 확장성</h3>
<h3 id="현재-스펙">현재 스펙</h3>
<ul>
<li>동시 처리: 최대 5명</li>
<li>대기 큐: 최대 20명</li>
<li>클라이언트: 총 25명 (pi200~pi224)</li>
<li>통장/인당: 최대 5개</li>
</ul>
<h3 id="확장-가능성">확장 가능성</h3>
<h4 id="1-창구-개수-조절">1. 창구 개수 조절</h4>
<pre><code class="language-c">#define MAX_WORKERS 10  // 5 → 10으로 증가</code></pre>
<h4 id="2-대기-큐-크기-조절">2. 대기 큐 크기 조절</h4>
<pre><code class="language-c">#define MAX_QUEUE 50  // 20 → 50으로 증가</code></pre>
<h4 id="3-클라이언트-범위-확장">3. 클라이언트 범위 확장</h4>
<pre><code class="language-c">#define MAX_CLIENTS 100  // pi200~pi299</code></pre>
<h4 id="4-데이터-영속성">4. 데이터 영속성</h4>
<ul>
<li>현재: 메모리 기반 (서버 재시작 시 데이터 소실)</li>
<li>개선: SQLite, MySQL 등 DB 연동</li>
</ul>
<hr />
<h3 id="학습-포인트">학습 포인트</h3>
<h3 id="1-tcp-소켓-프로그래밍">1. TCP 소켓 프로그래밍</h3>
<ul>
<li><code>socket()</code>, <code>bind()</code>, <code>listen()</code>, <code>accept()</code>, <code>connect()</code></li>
<li>연결 지향형 통신의 특성 이해</li>
<li>클라이언트-서버 모델 구현</li>
</ul>
<h3 id="2-posix-스레드-프로그래밍">2. POSIX 스레드 프로그래밍</h3>
<ul>
<li><code>pthread_create()</code>, <code>pthread_join()</code>, <code>pthread_detach()</code></li>
<li>Mutex를 통한 임계 구역 보호</li>
<li>조건 변수를 통한 스레드 동기화</li>
</ul>
<h3 id="3-동시성-제어">3. 동시성 제어</h3>
<ul>
<li>Race Condition 방지</li>
<li>Deadlock 회피</li>
<li>Thread-safe한 자료구조 설계</li>
</ul>
<h3 id="4-자료구조">4. 자료구조</h3>
<ul>
<li>원형 큐 (Circular Queue)</li>
<li>Thread Pool</li>
<li>구조체 배열을 통한 메모리 DB</li>
</ul>
<h3 id="5-시스템-프로그래밍">5. 시스템 프로그래밍</h3>
<ul>
<li>네트워크 바이트 오더 (<code>htons</code>, <code>ntohs</code>)</li>
<li>IP 주소 변환 (<code>inet_ntop</code>, <code>inet_pton</code>)</li>
<li>소켓 옵션 설정 (<code>SO_REUSEADDR</code>)</li>
</ul>
<hr />
<h3 id="실행-방법">실행 방법</h3>
<h3 id="컴파일">컴파일</h3>
<pre><code class="language-bash"># 서버
gcc -Wall -pthread -o bank_server bank_server.c

# 클라이언트
gcc -Wall -pthread -o bank_client bank_client.c</code></pre>
<h3 id="실행">실행</h3>
<pre><code class="language-bash"># 터미널 1: 서버 시작
./bank_server

# 터미널 2: 클라이언트 접속
./bank_client
&gt; 10.10.16.222  # 서버 IP 입력</code></pre>
<h3 id="사용-예시">사용 예시</h3>
<pre><code>입력: 통장 개설하고 싶어요
&gt; KB국민

입력: 입금
&gt; pi222
&gt; 1
&gt; 100000

입력: 출금
&gt; 1
&gt; 222
&gt; 50000

추가 업무? 아니요</code></pre><hr />
<h2 id="📚-참고-자료">📚 참고 자료</h2>
<ul>
<li><a href="https://beej.us/guide/bgnet/">Beej's Guide to Network Programming</a></li>
<li><a href="https://computing.llnl.gov/tutorials/pthreads/">POSIX Threads Programming</a></li>
<li><a href="https://www.oreilly.com/library/view/linux-system-programming/9781449341527/">Linux System Programming</a></li>
<li><a href="https://www.amazon.com/TCP-Illustrated-Vol-Addison-Wesley-Professional/dp/0201633469">TCP/IP Illustrated, Volume 1</a></li>
</ul>
<hr />
<h2 id="🔗-github">🔗 GitHub</h2>
<p>전체 소스코드는 GitHub에서 확인하실 수 있습니다:</p>
<p>👉 <a href="https://github.com/kyoung-mo/tcp-multithread-bank-system">GitHub Repository</a></p>
<hr />
<h2 id="마치며">마치며</h2>
<p>이번 프로젝트를 통해 TCP 소켓 프로그래밍과 멀티스레드 프로그래밍의 핵심 개념을 실제로 구현해볼 수 있었습니다. </p>
<p>특히 Thread Pool 패턴, 동기화 메커니즘, 대기 큐 관리 등 실무에서 자주 사용되는 패턴들을 직접 경험하며, 단순히 이론으로만 알던 개념들이 실제로 어떻게 동작하는지 체감할 수 있었습니다.</p>
<p>처음에는 간단한 에코 서버로 시작했지만, 점차 기능을 추가하면서 동시성 제어의 중요성과 디버깅의 어려움을 몸소 느꼈습니다. 특히 <code>pthread_cond_signal()</code>과 <code>pthread_cond_broadcast()</code>의 차이를 깨닫는 과정에서, 멀티스레드 프로그래밍에서 세심한 주의가 얼마나 중요한지 배웠습니다.</p>
<hr />
<p>궁금한 점이나 개선 사항이 있으시면 댓글로 남겨주세요! 🙌</p>