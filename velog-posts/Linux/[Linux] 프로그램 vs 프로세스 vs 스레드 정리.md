<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9bd8b86f-c830-46e4-aa12-08864c99daef/image.png" /></p>
<p><a href="https://velog.io/@gparkkii/ProgramProcessThread"><del>썸넬</del></a></p>
<hr />
<h3 id="프로그램-프로세스-스레드">프로그램? 프로세스? 스레드?</h3>
<hr />
<h4 id="📦-1-프로그램-program">📦 1. 프로그램 (Program)</h4>
<h4 id="정의">정의</h4>
<ul>
<li><strong>저장 장치에 저장된 실행 가능한 파일</strong></li>
<li>실행되기 전의 정적인 상태</li>
<li>코드와 데이터의 집합</li>
</ul>
<h4 id="특징">특징</h4>
<ul>
<li>디스크에 존재하는 파일 (<code>.exe</code>, <code>.out</code> 등)</li>
<li>아직 메모리에 로드되지 않음</li>
<li>실행되기를 기다리는 상태</li>
</ul>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0e04cd69-bf30-4b62-af0a-4e4677d12dd4/image.png" /></p>
<h4 id="🏃-2-프로세스-process">🏃 2. 프로세스 (Process)</h4>
<h4 id="정의-1">정의</h4>
<ul>
<li><strong>실행 중인 프로그램</strong></li>
<li>메모리에 로드되어 CPU를 할당받을 수 있는 상태</li>
<li>OS가 관리하는 실행의 기본 단위</li>
</ul>
<h4 id="특징-1">특징</h4>
<ul>
<li>독립적인 메모리 공간 보유<ul>
<li>코드(Code)</li>
<li>데이터(Data)</li>
<li>힙(Heap)</li>
<li>스택(Stack)</li>
</ul>
</li>
<li>고유한 PID(Process ID) 부여</li>
<li>다른 프로세스와 메모리 공유 불가 (격리됨)</li>
<li>프로세스 간 통신은 IPC 필요 (Pipe, Socket 등)</li>
</ul>
<h4 id="메모리-구조">메모리 구조</h4>
<pre><code>┌─────────────────┐
│   Stack         │ ← 지역변수, 함수 호출
├─────────────────┤
│   Heap          │ ← 동적 할당 (malloc)
├─────────────────┤
│   Data          │ ← 전역변수, 정적변수
├─────────────────┤
│   Code (Text)   │ ← 실행 코드
└─────────────────┘</code></pre><h4 id="예시">예시</h4>
<pre><code class="language-bash"># 프로그램 실행 → 프로세스 생성
./my_program &amp;

# 프로세스 확인
ps aux | grep my_program
pi  1234  0.0  0.1  my_program

# PID: 1234</code></pre>
<hr />
<h4 id="🧵-3-스레드-thread">🧵 3. 스레드 (Thread)</h4>
<h4 id="정의-2">정의</h4>
<ul>
<li><strong>프로세스 내부의 실행 흐름</strong></li>
<li>프로세스의 자원을 공유하는 경량 실행 단위</li>
<li>&quot;Light Weight Process&quot;</li>
</ul>
<h4 id="특징-2">특징</h4>
<ul>
<li>같은 프로세스 내 스레드들은 <strong>메모리 공유</strong><ul>
<li>코드, 데이터, 힙 공유 ✅</li>
<li>스택만 독립적 ❌</li>
</ul>
</li>
<li>고유한 TID(Thread ID) 보유</li>
<li>프로세스보다 생성/전환 비용 적음</li>
<li>빠른 데이터 공유 가능 (단, 동기화 필요)</li>
</ul>
<h4 id="메모리-구조-멀티스레드">메모리 구조 (멀티스레드)</h4>
<pre><code>프로세스 메모리 공간:
┌─────────────────┐
│ Thread 1 Stack  │ ← 독립
├─────────────────┤
│ Thread 2 Stack  │ ← 독립
├─────────────────┤
│ Thread 3 Stack  │ ← 독립
├─────────────────┤
│   Heap (공유)   │ ← 공유
├─────────────────┤
│   Data (공유)   │ ← 공유
├─────────────────┤
│   Code (공유)   │ ← 공유
└─────────────────┘</code></pre><h4 id="예시-1">예시</h4>
<pre><code class="language-c">#include 

void* thread_func(void* arg) {
    printf(&quot;Thread running!\n&quot;);
    return NULL;
}

int main() {
    pthread_t tid;
    pthread_create(&amp;tid, NULL, thread_func, NULL);
    pthread_join(tid, NULL);
    return 0;
}</code></pre>
<hr />
<h3 id="1-비교">1. 비교</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>프로그램 (Program)</th>
<th>프로세스 (Process)</th>
<th>스레드 (Thread)</th>
</tr>
</thead>
<tbody><tr>
<td>상태</td>
<td>정적 (Passive)</td>
<td>동적 (Active)</td>
<td>동적 (Active)</td>
</tr>
<tr>
<td>위치</td>
<td>디스크 (HDD/SSD)</td>
<td>메모리 (RAM)</td>
<td>메모리 (RAM)</td>
</tr>
<tr>
<td>정의</td>
<td>코드 덩어리 (Binary)</td>
<td>자원 할당의 단위 (컨테이너)</td>
<td>CPU 실행/스케줄링의 단위</td>
</tr>
<tr>
<td>자원 공유</td>
<td>-</td>
<td>공유 안 함 (독립적)</td>
<td>메모리 공유 (Code, Data, Heap)</td>
</tr>
<tr>
<td>통신</td>
<td>-</td>
<td>IPC (복잡, 느림)</td>
<td>공유 메모리 (간단, 빠름, 동기화 필요)</td>
</tr>
</tbody></table>
<h3 id="2-메모리-구조-중요">2. 메모리 구조 (중요)</h3>
<h4 id="1-프로세스">1. 프로세스</h4>
<ul>
<li>부모-자식 간이라도 메모리 공간이 완전히 분리됨 (<code>Copy-on-Write</code>).</li>
<li>한 프로세스가 죽어도 다른 프로세스에 영향 없음.</li>
</ul>
<h4 id="2-스레드">2. 스레드</h4>
<ul>
<li>공유 : Code, Data(전역변수), Heap(동적할당), File Descriptor.</li>
<li>독립: Stack(지역변수, 함수호출), Register(PC, SP).</li>
<li>주의: 하나의 스레드에서 메모리 침범(Segfault) 발생 시, 프로세스 전체가 죽음.</li>
</ul>
<h3 id="3-리눅스-특이사항">3. 리눅스 특이사항</h3>
<p>• PID: 리눅스 커널은 스레드도 내부적으로는 '가벼운 프로세스(LWP)'로 취급하여 고유의 ID를 가집니다 (TID). 하지만 사용자 입장에서는 PID 하나로 묶여 보입니다.
• 생성: 프로세스는 <code>fork()</code>로 복제하지만, 스레드는 <code>pthread_create()</code> (내부적으로 <code>clone()</code>) 시스템 콜을 사용합니다.</p>
<blockquote>
<p><em>썸넬 Reference</em> : <a href="https://velog.io/@gparkkii/ProgramProcessThread">https://velog.io/@gparkkii/ProgramProcessThread</a></p>
</blockquote>