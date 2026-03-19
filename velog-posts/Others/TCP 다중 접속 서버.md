<p>수업 내용 복습용으로 쭉 적어보겠습니당</p>
<hr />
<p>TCP/IP 방식은 연결 지향형 통신으로, 서버에서의 <code>socket() -&gt; bind() -&gt; listen()</code> 이후 클라이언트에서 <code>connect()</code> 요청이 왔을 때, 서버에서 <code>accept()</code> 하는 과정을 거쳐 통신을 진행하기 때문에 1:1 통신만 가능하다.</p>
<p>하지만 하나의 서버로 여러 클라이언트랑 연결할 수 있는데, 다중 접속 서버를 통해 구현 가능하다.</p>
<hr />
<h2 id="다중-접속-서버의-구현-방법">다중 접속 서버의 구현 방법</h2>
<p>다중 접속 서버란 둘 이상의 클라이언트에게 동시에 접속을 허용하여, 동시에 둘 이상의 클라이언트에게 서비스를 제공하는 서버를 의미한다.</p>
<ol>
<li><p>멀티프로세스 기반 서버
: 다수의 프로세스를 생성</p>
</li>
<li><p>멀티플렉싱 기반 서버
: 입출력 대상을 묶어서 관리하는 방식</p>
</li>
<li><p>멀티쓰레딩 기반 서버
: 클라이언트의 수만큼 쓰레드를 생성</p>
</li>
</ol>
<hr />
<h2 id="멀티프로세스-기반-서버">멀티프로세스 기반 서버</h2>
<p>멀티 프로세스 기반 서버는 말 그대로 다수의 프로세스를 생성하여 클라이언트에게 서비스를 제공한다.</p>
<p>그렇다면 프로세스란 무엇인가?
프로세스란 간단히 설명하면 <strong>실행중인 프로그램</strong>을 뜻한다.</p>
<p><a href="https://velog.io/@mommers/C-%EB%A9%94%EB%AA%A8%EB%A6%AC-%EA%B5%AC%EC%A1%B0%EB%A5%BC-%EC%99%9C-%EC%95%8C%EC%95%84%EC%95%BC%ED%95%B4">[이전 글] : C에서 메모리 구조를 왜 알아야해?</a></p>
<p>저번에 메모리 구조를 공부했었는데, 
Code 영역, Data 영역, Heap 영역, Stack 영역이 각각의 프로세스마다 존재한다.</p>
<p>데이터를 공유하는 영역이 없어서, 앞의 프로세스의 결과값을 뒤에 오는 프로세스의 입력 값으로 넣어줘야한다.</p>
<p>또한 컨텍스트 스위칭을 거치기 때문에 성능 저하가 존재. 즉 매우 느리며 데이터 교환이 어렵다는 특징이 있다.</p>
<hr />
<h2 id="멀티-플렉싱-기반-서버">멀티 플렉싱 기반 서버</h2>
<p>멀티 플렉싱 기반 서버는 입출력 대상을 묶어서 관리하는 방식으로 서비스를 제공한다. 입출력 대상을 묶어서 관리하기 때문에, 멀티프로세스 기반 서버에 비해 데이터 교환이 용이하다는 특징이 있다.</p>
<p>하지만, 누군가가 입출력 대상을 묶어주는 핸들링 과정을 거쳐야 하는데 이 때 <code>select</code>가 쓰인다.</p>
<p>하지만 <code>select</code>는 운영체제마다 정해진 최대 개수가 존재하기 때문에, 클라이언트 수가 <code>select</code>의 수를 넘어갈 수 없다는 단점이 있다.</p>
<hr />
<h2 id="멀티-쓰레드-기반-서버">멀티 쓰레드 기반 서버</h2>
<p><code>멀티 쓰레드 방식</code>은 <code>멀티 프로세스 방식</code>, <code>멀티 플렉싱 방식</code> 의 단점을 보완하는 방식이다.</p>
<p>일단 쓰레드의 개념은 이전에 정리해둔 글이 있어서 링크를 남겨두겠습니다.</p>
<p><a href="https://velog.io/@mommers/Linux-%EC%93%B0%EB%A0%88%EB%93%9C-Thread-%EC%A0%95%EB%A6%AC">이전 글 : [Linux] 쓰레드 (Thread) 정리</a></p>
<p>간단하게만 설명하면 하나의 프로세스 안에서 여러 쓰레드가 생성될 수 있는데, 각각의 쓰레드는 Code 영역, Data 영역, Heap 영역을 공유한다.</p>
<p>하지만 Stack 영역을 각각의 쓰레드가 갖고 있다.</p>
<p>A 쓰레드에서 전역변수 k를 1 증가했을 때, 같은 프로세스 내에 있는 B 쓰레드에서도 전역변수 k 값이 1이 증가한다.</p>
<p>메모리 관리가 굉장히 용이하다는 특징이 있다. 그렇다면 멀티 쓰레드 방식의 단점은 무엇일까?</p>
<hr />
<h2 id="mul-thread-방식-단점">mul-thread 방식 단점</h2>
<p>수업시간에 진행했던 예제를 가져왔습니다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;pthread.h&gt;
#define NUM_THREAD    100

void * thread_inc(void * arg);
void * thread_des(void * arg);
long long num=0;

int main(int argc, char *argv[]) 
{
    pthread_t thread_id[NUM_THREAD];
    int i;

    printf(&quot;sizeof long long: %ld \n&quot;, sizeof(long long));
    for(i=0; i&lt;NUM_THREAD; i++)
    {
        if(i%2)
            pthread_create(&amp;(thread_id[i]), NULL, thread_inc, NULL);
        else
            pthread_create(&amp;(thread_id[i]), NULL, thread_des, NULL);    
    }    

    for(i=0; i&lt;NUM_THREAD; i++)
        pthread_join(thread_id[i], NULL);

    printf(&quot;result: %lld \n&quot;, num);
    return 0;
}

void * thread_inc(void * arg) 
{
    int i;
    for(i=0; i&lt;50000000; i++)
        num+=1;
    return NULL;
}
void * thread_des(void * arg)
{
    int i;
    for(i=0; i&lt;50000000; i++)
        num-=1;
    return NULL;
}</code></pre>
<p>실행 결과는 아래와 같다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1af9300e-8b22-4c7f-b8eb-86db74ccd666/image.png" /></p>
<p>이론 상 <code>thread_inc</code> 는 값을 1 증가, <code>thread_des</code> 는 값을 1 감소 하는 과정을 똑같이 5000만번 씩 실행하는데, 실행 결과는 실행할 때마다 다른 것을 확인할 수 있다.</p>
<p>이는 <code>thread_inc</code> 와 <code>thread_des</code> 가 동시에 변수에 접근하기 때문에 생기는 상황이다.</p>
<hr />
<pre><code class="language-c">long long num = 99;
long long i;
i=num; // i=99
i++;  // i=100
num=i;  // num=100</code></pre>
<p>위 코드가 하나의 쓰레드라고 가정할 때 하나의 쓰레드만 있다면 문제가 되지 않는다.</p>
<p>만약 thread1, thread2 이렇게 두 개가 있다고 가정해보자. </p>
<pre><code class="language-c">// thread 1
long long num = 99;
long long i;
i=num; // i=99
i++;  // i=100 &amp;&amp; (1) context switching 일어났다고 가정
// (2) num 값 업데이트 안된 상태로 thread 2로 넘어감
num=i; // (7) num에 100값 저장

-&gt; (8) num = 100  // 기댓값 num = 101
======================

// (3) thread 2
long long num = 99;
long long i;
i=num; // i=99
i++;  // i=100
num=i;  // num=100 -&gt; (4) 실행 완료 -&gt; (5) 다시 thread 1으로 넘어감

-&gt; (6) num = 100</code></pre>
<p>기댓값은 101이나, 실제 num 전역변수에 저장된 값은 100이다.</p>
<p>이러한 상황을 방지하고자 사용하는게 뮤텍스이다.</p>
<hr />
<h2 id="뮤텍스">뮤텍스</h2>
<pre><code class="language-c">long long num = 99;
long long i;  // lock
i=num; 
i++;  
num=i;  // unlock</code></pre>
<p>뮤텍스는 어떤 한 쓰레드가 전역변수에 접근을 할 때, 작업이 끝나기 전까지 lock, unlock을 걸어 다른 쓰레드가 동시에 접근하지 못하게 막는 역할을 한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/78db5a1f-c944-49d2-8031-fc97df46ab48/image.png" /></p>
<p>39줄, 50줄에서 lock / 42, 52줄에서 unlock</p>
<p><code>thread_inc()</code> 와 <code>thread_des()</code>  함수의 차이점은 for문 밖에 <code>lock()</code> , <code>unlock()</code> 을 하느냐, 안에 하느냐이다.</p>
<p>함수는 오버헤드가 존재한다. 따라서 for문 안에 넣어주게 되면, for문 한번 돌 때마다 함수를 두번을 거쳐야 하기 때문에 <code>inc</code> 보다 <code>des</code> 가 시간이 훨씬 많이 걸린다.</p>
<p><strong>TEST</strong></p>
<ol>
<li>for문 안에 <code>pthread_mutex_lock</code>  , <code>pthread_mutex_unlock</code> </li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8e4de38a-9b00-42bd-98ab-e8f324d07a6f/image.png" /></p>
<ol>
<li>for문 밖에 <code>pthread_mutex_lock</code>  , <code>pthread_mutex_unlock</code> </li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ce816ce0-6e86-42da-846f-ef5a53db7273/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2f3ec478-cf76-4e63-b069-98588a674dd7/image.png" /></p>
<p><strong>결과 비교</strong></p>
<p>1m 47.927s &gt;&gt;&gt;&gt;&gt; 0m 3.144s</p>
<hr />
<h2 id="세마포어semaphore">세마포어(Semaphore)</h2>
<p>세마포어는 세마포어 카운트 값을 통해서 임계 영역에 동시 접근 가능한 쓰레드의 수를 제한할 수 있다.</p>
<p>세마포어  카운트가 0이면 진입 불가, 0보다 크면 진입 가능</p>
<p><del>wait 는 1일 때 들어간다?</del></p>
<pre><code class="language-c">#include &lt;semaphore.h&gt;

int sem_init(sem_t* sem, int pshared, unsigned int value);
int sem_destroy(sem_t* sem);
// 성공 시 0, 실패 시 0 이외의 값 반환</code></pre>
<hr />