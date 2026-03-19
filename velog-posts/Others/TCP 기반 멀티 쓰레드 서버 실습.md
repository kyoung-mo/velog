<p><a href="https://velog.io/@mommers/TCP-%EB%8B%A4%EC%A4%91-%EC%A0%91%EC%86%8D-%EC%84%9C%EB%B2%84">이전 글 : TCP 다중 접속 서버</a></p>
<p>멀티 프로세스 방식, 멀티 플렉싱 방식의 단점을 보완한 멀티쓰레드 서버에 관련된 실습을 정리해보고자 합니다.</p>
<hr />
<ul>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/TCPIP_Src/Chapter18/chat_serv.c">chat_serv.c</a></li>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/TCPIP_Src/Chapter18/chat_clnt.c">chat_clnt.c</a></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d2148b1c-d20e-4dbc-b0cb-ef573192fc58/image.png" /></p>
<p>전체 동작은 위 사진과 같습니다.
서버를 열어두고, client 2명에서 대화 가능하도록 구현된 예제인데, 각각의 클라이언트가 접속할 때 쓰레드가 생성이 됩니다.</p>
<p>뮤텍스를 통해 lock, unlock을 하는 과정은 </p>
<ul>
<li>클라이언트 접속 시 → clnt_socks[]에 추가</li>
<li>클라이언트 연결 해제 시 → clnt_socks[]에서 제거</li>
<li>send_msg() 에서 전체 브로드캐스트 시 </li>
</ul>
<p>생성됩니다.</p>
<hr />
<h2 id="chat_servc">chat_serv.c</h2>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;arpa/inet.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;netinet/in.h&gt;
#include &lt;pthread.h&gt;

#define BUF_SIZE 100
#define MAX_CLNT 256

void * handle_clnt(void * arg);
void send_msg(char * msg, int len);
void error_handling(char * msg);

int clnt_cnt=0;
int clnt_socks[MAX_CLNT];
pthread_mutex_t mutx;

int main(int argc, char *argv[])
{
    int serv_sock, clnt_sock;
    struct sockaddr_in serv_adr, clnt_adr;
    int clnt_adr_sz;
    pthread_t t_id;
    if(argc!=2) {
        printf(&quot;Usage : %s &lt;port&gt;\n&quot;, argv[0]);
        exit(1);
    }

    pthread_mutex_init(&amp;mutx, NULL);
    serv_sock=socket(PF_INET, SOCK_STREAM, 0);

    memset(&amp;serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family=AF_INET; 
    serv_adr.sin_addr.s_addr=htonl(INADDR_ANY);
    serv_adr.sin_port=htons(atoi(argv[1]));

    if(bind(serv_sock, (struct sockaddr*) &amp;serv_adr, sizeof(serv_adr))==-1)
        error_handling(&quot;bind() error&quot;);
    if(listen(serv_sock, 5)==-1)
        error_handling(&quot;listen() error&quot;);

    while(1)
    {
        clnt_adr_sz=sizeof(clnt_adr);
        clnt_sock=accept(serv_sock, (struct sockaddr*)&amp;clnt_adr,&amp;clnt_adr_sz);

        pthread_mutex_lock(&amp;mutx);
        clnt_socks[clnt_cnt++]=clnt_sock;
        pthread_mutex_unlock(&amp;mutx);

        pthread_create(&amp;t_id, NULL, handle_clnt, (void*)&amp;clnt_sock);
        pthread_detach(t_id);
        printf(&quot;Connected client IP: %s \n&quot;, inet_ntoa(clnt_adr.sin_addr));
    }
    close(serv_sock);
    return 0;
}

void * handle_clnt(void * arg)
{
    int clnt_sock=*((int*)arg);
    int str_len=0, i;
    char msg[BUF_SIZE];

    while((str_len=read(clnt_sock, msg, sizeof(msg)))!=0)
        send_msg(msg, str_len);

    pthread_mutex_lock(&amp;mutx);
    for(i=0; i&lt;clnt_cnt; i++)   // remove disconnected client
    {
        if(clnt_sock==clnt_socks[i])
        {
            while(i++&lt;clnt_cnt-1)
                clnt_socks[i]=clnt_socks[i+1];
            break;
        }
    }
    clnt_cnt--;
    pthread_mutex_unlock(&amp;mutx);
    close(clnt_sock);
    return NULL;
}
void send_msg(char * msg, int len)   // send to all
{
    int i;
    pthread_mutex_lock(&amp;mutx);
    for(i=0; i&lt;clnt_cnt; i++)
        write(clnt_socks[i], msg, len);
    pthread_mutex_unlock(&amp;mutx);
}
void error_handling(char * msg)
{
    fputs(msg, stderr);
    fputc('\n', stderr);
    exit(1);
}</code></pre>
<p><code>pthread_mutex_t mutx;</code>로 뮤텍스를 생성해준다.</p>
<p>main 코드</p>
<ul>
<li><code>serv_sock, clnt_sock;</code> 이후 뮤텍스 변수를 NULL로 초기화</li>
<li><code>serv_sock</code> socket 생성 및 초기화</li>
<li><code>bind()</code> 이후 <code>listen()</code> 에서 최대 5개의 소켓이 대기 가능하게 버퍼 생성
{
while(1)</li>
<li><code>clnt_sock</code> 생성 및 <code>accept()</code>를 통해 서버의 <code>listen()</code> 소켓과 연결</li>
<li><code>clnt_socks[]</code> 버퍼에 클라이언트 소켓을 저장</li>
<li>client가 들어오면 쓰레드 생성  </li>
<li>클라 인덱스 값에 따라 <code>printf()</code> 문 출력
}</li>
<li>이후 <code>serv_sock</code> 을 <code>close()</code></li>
</ul>
<p>handle_clnt 함수</p>
<ul>
<li>clnt sock 변수와, str 길이를 저장할 변수를 초기화</li>
<li>while문에서 입력한 메세지의 길이를 <code>read()</code> 를 통해 읽어와 str_len 값을 저장, 및 에러처리</li>
<li>접속이 끊어진 client disconnect 처리? -&gt; 다시 공부</li>
<li><code>close()</code> 를 통해 clnt_sock 닫기</li>
</ul>
<p>send_msg 함수</p>
<ul>
<li>mutex로 <code>lock()</code>을 걸고, clnt_socks[i]에서 len의 길이 만큼 msg 버퍼에서 출력</li>
<li>mutex <code>unlock()</code></li>
</ul>
<p>error_handling 함수</p>
<ul>
<li>msg 포인터 변수에 따른 에러 출력</li>
</ul>
<hr />
<h2 id="chat_clntc">chat_clnt.c</h2>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt; 
#include &lt;string.h&gt;
#include &lt;arpa/inet.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;pthread.h&gt;

#define BUF_SIZE 100
#define NAME_SIZE 20

void * send_msg(void * arg);
void * recv_msg(void * arg);
void error_handling(char * msg);

char name[NAME_SIZE]=&quot;[DEFAULT]&quot;;
char msg[BUF_SIZE];

int main(int argc, char *argv[])
{
    int sock;
    struct sockaddr_in serv_addr;
    pthread_t snd_thread, rcv_thread;
    void * thread_return;
    if(argc!=4) {
        printf(&quot;Usage : %s &lt;IP&gt; &lt;port&gt; &lt;name&gt;\n&quot;, argv[0]);
        exit(1);
     }

    sprintf(name, &quot;[%s]&quot;, argv[3]);
    sock=socket(PF_INET, SOCK_STREAM, 0);

    memset(&amp;serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family=AF_INET;
    serv_addr.sin_addr.s_addr=inet_addr(argv[1]);
    serv_addr.sin_port=htons(atoi(argv[2]));

    if(connect(sock, (struct sockaddr*)&amp;serv_addr, sizeof(serv_addr))==-1)
        error_handling(&quot;connect() error&quot;);

    pthread_create(&amp;snd_thread, NULL, send_msg, (void*)&amp;sock);
    pthread_create(&amp;rcv_thread, NULL, recv_msg, (void*)&amp;sock);
    pthread_join(snd_thread, &amp;thread_return);
    pthread_join(rcv_thread, &amp;thread_return);
    close(sock);  
    return 0;
}

void * send_msg(void * arg)   // send thread main
{
    int sock=*((int*)arg);
    char name_msg[NAME_SIZE+BUF_SIZE];
    while(1) 
    {
        fgets(msg, BUF_SIZE, stdin);
        if(!strcmp(msg,&quot;q\n&quot;)||!strcmp(msg,&quot;Q\n&quot;)) 
        {
            close(sock);
            exit(0);
        }
        sprintf(name_msg,&quot;%s %s&quot;, name, msg);
        write(sock, name_msg, strlen(name_msg));
    }
    return NULL;
}

void * recv_msg(void * arg)   // read thread main
{
    int sock=*((int*)arg);
    char name_msg[NAME_SIZE+BUF_SIZE];
    int str_len;
    while(1)
    {
        str_len=read(sock, name_msg, NAME_SIZE+BUF_SIZE-1);
        if(str_len==-1) 
            return (void*)-1;
        name_msg[str_len]=0;
        fputs(name_msg, stdout);
    }
    return NULL;
}

void error_handling(char *msg)
{
    fputs(msg, stderr);
    fputc('\n', stderr);
    exit(1);
}</code></pre>
<p>main 함수</p>
<ul>
<li><code>sock=socket(PF_INET, SOCK_STREAM, 0);</code> 소켓 생성 및 fd 번호 할당</li>
<li><code>if(connect(sock, (struct sockaddr*)&amp;serv_addr, sizeof(serv_addr))==-1)</code> listen 소켓에 <code>connect()</code> 요청</li>
<li>이후 pthread_create로 <code>snd_thread</code> , <code>rcv_thread</code> 두 개의 쓰레드를 생성해 send를 하는동안에도 recieve가 가능</li>
<li><code>close()</code> 로 sock fd 반환</li>
</ul>
<p>send_msg 함수</p>
<ul>
<li>stdin(입력)을 최대 BUF_SIZE만큼 받아 msg 버퍼에 출력 (최대 100)</li>
<li>문자열 비교 함수 strcmp를 통해 q, Q가 입력되었을 때 sock <code>close()</code></li>
</ul>
<p>recv_msg 함수</p>
<ul>
<li><code>str_len=read(sock, name_msg, NAME_SIZE+BUF_SIZE-1);</code>  sock fd에서 NAME_SIZE+BUF_SIZE-1 만큼의 크기를 name_msg 버퍼에서 읽어서, str_len 변수에 저장</li>
<li><code>name_msg[str_len]=0</code> 을 통해 <code>\0</code> 문자 삽입</li>
<li>stdout에 name_msg에서 내용 출력</li>
</ul>
<p>error_handling 함수</p>
<ul>
<li>msg 포인터 변수에 따른 에러 출력</li>
</ul>
<hr />
<p>접속이 끊어진 client disconnect 처리? -&gt; 다시 공부 부분 정리</p>
<pre><code class="language-c">// disconnct 감지
while((str_len=read(clnt_sock, msg, sizeof(msg)))!=0) 
    send_msg(msg, str_len);
/* 
이 과정에서 disconnect 감지
read()는 상대방이 연결을 끊으면 0을 반환
그 순간 while을 탈출하고 아래 제거 로직으로 진입
*/

// 배열에서 해당 소켓 찾기
pthread_mutex_lock(&amp;mutx);
for(i=0; i&lt;clnt_cnt; i++)   
{
    if(clnt_sock==clnt_socks[i]) // 끊긴 소켓 위치 탐색
    { // clnt_sock[] 배열에서 끊긴 소켓 인덱스 i를 찾음
        while(i++&lt;clnt_cnt-1) // 빈 자리 당겨서 채우기
            clnt_socks[i]=clnt_socks[i+1];
        break;
    }
}
clnt_cnt--;
pthread_mutex_unlock(&amp;mutx);</code></pre>