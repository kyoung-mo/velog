<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ddc27e3c-6431-4a45-89b1-60986b48e861/image.png" /></p>
<h3 id="전통적인-비동기-방식-non-blocking-io--selectpoll">전통적인 비동기 방식 (Non-blocking I/O + <code>select</code>/<code>poll</code>)</h3>
<ul>
<li>&quot;읽어라!&quot; 명령하고, &quot;다 됐니?&quot; 계속 확인하거나 콜백(Callback) 함수를 등록해야 함</li>
<li>코드의 흐름이 뚝뚝 끊김(Fragmented) <code>read</code> 요청하는 곳과 데이터를 처리하는 곳이 물리적으로 멀리 떨어져 있음</li>
<li>상태 관리: &quot;지금 데이터를 30% 읽은 상태&quot;라는 문맥(Context)을 전역 변수나 구조체로 개발자가 직접 관리해야 함</li>
</ul>
<h3 id="멀티-쓰레드-방식-synchronous-blocking-io">멀티 쓰레드 방식 (Synchronous Blocking I/O)</h3>
<ul>
<li>그냥 별도 쓰레드 하나 만들어서 <code>read()</code>를 호출해버림.</li>
<li><code>read()</code>가 끝날 때까지 그 쓰레드는 멈추지만(Block), 코드 흐름은 위에서 아래로 순차적(Sequential)임.</li>
<li>개발자는 직관적인 &quot;순차적 사고&quot;를 할 수 있어 로직 작성이 훨씬 쉬움.</li>
</ul>
<hr />
<h3 id="2-코드-구조-비교-가독성-차이">2. 코드 구조 비교 (가독성 차이)</h3>
<p>서버에서 클라이언트 데이터를 받아서 처리하는 로직을 짠다고 가정해 봅시다.</p>
<h4 id="상황-1-비동기-방식-single-thread--event-loop">[상황 1] 비동기 방식 (Single Thread + Event Loop)</h4>
<p>코드가 이벤트 처리를 위해 쪼개져 있어 흐름 파악이 어렵습니다.</p>
<pre><code class="language-c">// 상태 머신을 만들어야 함
void on_data_received(int socket, char* data) {
    // 2. 데이터가 오면 이 함수가 나중에 호출됨
    process(data);
}

void main_loop() {
    // 1. 읽기 요청만 해두고 딴짓 하러 감
    async_read(socket, on_data_received);

    while(1) {
        // 이벤트 루프가 계속 돔
        handle_events();
    }
}</code></pre>
<h4 id="상황-2-멀티-쓰레드-방식-blocking-io">[상황 2] 멀티 쓰레드 방식 (Blocking I/O)</h4>
<p>우리가 글을 읽는 순서와 코드 실행 순서가 일치합니다.</p>
<pre><code class="language-c">void* client_thread(void* arg) {
    int sock = *(int*)arg;

    // 1. 여기서 읽을 때까지 대기 (Blocking)
    // 하지만 다른 쓰레드들은 잘 돌아가므로 전체 시스템은 멈추지 않음!
    int n = read(sock, buf, SIZE);

    // 2. 읽기가 끝나면 바로 아랫줄 실행
    process(buf);

    return NULL;
}</code></pre>
<hr />
<h3 id="3-모듈화와-독립성-modularity">3. 모듈화와 독립성 (Modularity)</h3>
<p>작성해주신 &quot;독립적인 이벤트들 간의 관계를 명확하게 보여준다&quot;는 점은 시스템 설계에서 아주 중요합니다.</p>
<ul>
<li>UI 쓰레드: 오직 화면 그리는 일만 신경 씀.</li>
<li>네트워크 쓰레드: 오직 패킷 주고받는 일만 신경 씀.</li>
<li>워커 쓰레드: 오직 복잡한 계산만 신경 씀.</li>
<li>결과: 각 쓰레드는 서로의 내부 사정(루프가 언제 도는지 등)을 몰라도 되며, 공유하는 데이터(Queue 등)만 잘 정의하면 완벽하게 분리(Decoupling)됩니다.</li>
</ul>
<hr />
<h3 id="4-멀티-쓰레드를-사용한-병렬-처리-프로그래밍">4. 멀티 쓰레드를 사용한 병렬 처리 프로그래밍</h3>
<ul>
<li>2 개의 숫자를 입력 받아서 동시에 병렬로 소수 여부를 판단하는 2 개의 쓰레드</li>
<li>프로세스 진행 상황을 알려주는 쓰레드 등 3개의 쓰레드 실행</li>
<li>소수 여부의 결과를 쓰레드에서 출력</li>
<li>입력 받은 숫자의 순서에 상관없이 소수 판단이 먼저 종료된 쓰레드에서 결과를 출력</li>
<li>htop 명령을 이용하여 cpu 부하 등을 확인</li>
</ul>
<hr />
<h4 id="01multi-threadc">01.multi-thread.c</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;pthread.h&gt;

void *isprime(void *arg);
void *progress(void *arg);

int main(int argc, char *argv[]){
  long long num1;
  long long num2;
  pthread_t tid1, tid2, tid3;
  pthread_attr_t attr;
  if (argc != 3) {
    fprintf(stderr, &quot;Please supply two numbers.\n&quot; &quot;Example: %s 9 7\n&quot;, argv[0]);
    return 1;
  }
  num1 = atoll(argv[1]);
  num2 = atoll(argv[2]);

  pthread_attr_init(&amp;attr);

  pthread_create(&amp;tid3, &amp;attr, progress, NULL);
  pthread_detach(tid3);

  pthread_create(&amp;tid1, &amp;attr, isprime, &amp;num1);
  pthread_create(&amp;tid2, &amp;attr, isprime, &amp;num2);

  pthread_join(tid1, NULL);
  pthread_join(tid2, NULL);

  pthread_attr_destroy(&amp;attr);
  if (pthread_cancel(tid3) != 0)
     fprintf(stderr, &quot;Couldn't cancel progress thread\n&quot;);
  printf(&quot;Done!\n&quot;);
    sleep(3);
  return 0;
}

void *isprime(void *arg){
   long long int number = *((long long*)arg);
   long long int j;
   int prime = 1;

   for(j=2; j&lt;number; j++) {
      if(number%j == 0){
         prime = 0;
      }
   }
   if(prime == 1){
      printf(&quot;\n%lld is a prime number\n&quot;, number);
      return NULL;
   }else{
      printf(&quot;\n%lld is not a prime number\n&quot;, number);
      return NULL;
   }
}

void *progress(void *arg){
   while(1) {
      sleep(1);
      printf(&quot;.&quot;);
      fflush(stdout);
   }
   return NULL;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/74ea558f-0f8a-463b-af21-c61ce2d9d29c/image.png" /></p>
<pre><code class="language-c">$ gcc 01.multi-threaded.c -o 01.multi-threaded

$ ./01.multi-threaded  4412345678 441234567
..
441234567 is not a prime number
....................
4412345678 is not a prime number
Done!

$ ./01.multi-threaded  441234567 4412345678
..
441234567 is not a prime number
....................
4412345678 is not a prime number
Done!</code></pre>
<hr />
<h4 id="02thread-returnc">02.thread-return.c</h4>
<ul>
<li>메인이 쓰레드로부터 소수 여부의 결과를 받아서 출력</li>
<li>pthread_join은 쓰레드가 join된 순서대로 종료처리된다</li>
<li>즉, pthread_join은 해당 쓰레드가 종료될 때까지 호출하는 프로세스를 차단하기 때문에 판단이 오래 걸리는 숫자를 먼저 입력하는 경우 해당 쓰레드가 종료될 때까지 결과가 출력되지 않는다.</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;pthread.h&gt;
#include &lt;stdint.h&gt;

void *isprime(void *arg);
void *progress(void *arg);

int main(int argc, char *argv[]){
   long long num1;
   long long num2;
   pthread_t tid1;
   pthread_t tid2;
   pthread_t tid3;
   void *result1;
   void *result2;
   if (argc != 3){
      fprintf(stderr, &quot;Please supply two numbers.\n&quot; &quot;Example: %s 9 7\n&quot;, argv[0]);
      return 1;
   }
   num1 = atoll(argv[1]);
   num2 = atoll(argv[2]);

   pthread_create(&amp;tid3, NULL, progress, NULL);  
   pthread_detach(tid3);

   pthread_create(&amp;tid1, NULL, isprime, &amp;num1);
   pthread_create(&amp;tid2, NULL, isprime, &amp;num2);

   pthread_join(tid1, &amp;result1);
   if ((uintptr_t)result1 == 1)
      printf(&quot;\n%lld is a prime number\n&quot;, num1);
   else
      printf(&quot;\n%lld is not a prime number\n&quot;, num1);

   pthread_join(tid2, &amp;result2);   
   if ((uintptr_t)result2 == 1)
      printf(&quot;\n%lld is a prime number\n&quot;, num2);
   else
      printf(&quot;\n%lld is not a prime number\n&quot;, num2);

   if ( pthread_cancel(tid3) != 0 )
      fprintf(stderr, &quot;Couldn't cancel progress thread\n&quot;);
   return 0;
}

void *isprime(void *arg) {
   long long int number = *((long long*)arg);
   long long int j;
   int prime = 1;

   for(j=2; j&lt;number; j++){
      if(number%j == 0)
         prime = 0;
   }
   if(prime == 1)
      return (void*)1;
   else
      return (void*)0;
}

void *progress(void *arg){
   while(1){
      sleep(1);
      printf(&quot;.&quot;);
      fflush(stdout);
   }
   return NULL;
}</code></pre>
<pre><code class="language-c">$ gcc 02.threads-return.c  -o 02.threads-return

$ ./02.threads-return 331234567 3312345678
.
331234567 is not a prime number
................
3312345678 is not a prime number

$ ./02.threads-return 3312345678 331234567
.................
3312345678 is not a prime number

331234567 is not a prime number</code></pre>
<hr />
<h3 id="5-요약표">5. 요약표</h3>
<table>
<thead>
<tr>
<th>특징</th>
<th>비동기 프로그래밍 (Single Thread)</th>
<th>멀티 쓰레드 프로그래밍 (Blocking I/O)</th>
</tr>
</thead>
<tbody><tr>
<td>I/O 처리</td>
<td>Non-blocking (복잡함)</td>
<td>Blocking (단순함)</td>
</tr>
<tr>
<td>코드 흐름</td>
<td>이벤트 기반 (Event-driven), 콜백</td>
<td>절차 지향 (Procedural)</td>
</tr>
<tr>
<td>컨텍스트 관리</td>
<td>개발자가 직접 저장해야 함</td>
<td>OS가 스택(Stack)으로 관리해줌</td>
</tr>
<tr>
<td>디버깅</td>
<td>흐름 추적이 어려움</td>
<td>각 쓰레드별 스택 추적 가능</td>
</tr>
<tr>
<td>적합한 곳</td>
<td>수만 개의 연결 (C10K 문제, Nginx, Node.js)</td>
<td>로직의 복잡도가 높은 서버, 임베디드 제어</td>
</tr>
</tbody></table>
<p>결론적으로, &quot;멀티 쓰레드는 사람이 생각하기 편한 방식(순차적 실행)을 유지하면서도, 기계의 성능(병렬성+I/O대기 활용)을 뽑아낼 수 있는 가장 현실적인 모델&quot;입니다.</p>
<blockquote>
<p>썸넬  : <a href="https://x.com/programmer_pic/status/1208022091968045059">https://x.com/programmer_pic/status/1208022091968045059</a></p>
</blockquote>