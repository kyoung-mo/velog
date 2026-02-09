<p>멀티프로세스 기반 TCP Server/Client 구현시 좀비 프로세스가 생성되는 예제를 확인해봅시다.</p>
<h3 id="1-mytcpclientc">1. mytcpclient.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;errno.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;arpa/inet.h&gt;

int main(int argc, char *argv[]){
    int sockfd, bytes_recv; 
    struct sockaddr_in sockaddr;
    char tx_buf[128], rx_buf[128];
    int i;

    if(argc != 2){
        fprintf(stderr, &quot;usage : client serverip \n&quot;);
        exit(1);
    }

    //socket open
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
        perror(&quot;socket() error&quot;);
        exit(1);
    }

    sockaddr.sin_family = AF_INET;
    sockaddr.sin_port = htons(10000);
    sockaddr.sin_addr.s_addr = inet_addr(argv[1]);    
    /*  sockaddr.sin_addr.s_addr = inet_addr(&quot;70.12.117.90&quot;);  */
    memset(&amp;(sockaddr.sin_zero), '\0',8);

    printf(&quot;[ %s ]\n&quot;, inet_ntoa(sockaddr.sin_addr));

    //connection request to server
    if(connect(sockfd, (struct sockaddr *)&amp;sockaddr, sizeof(struct sockaddr)) == -1){
        perror(&quot;connect() error&quot;);
        exit(1);
    }

    for(i=1; i&lt;=10; i++) {
        memset(tx_buf, 0, sizeof(tx_buf));
        memset(rx_buf, 0, sizeof(rx_buf));
        sprintf(tx_buf, &quot;Hello_%d server(from %d)!!\n&quot;, i, getpid());
        //messge send to server
        if(send(sockfd, tx_buf, strlen(tx_buf)+1, 0) == -1) 
            perror(&quot;send&quot;);
        //message rx wait from server
        if((bytes_recv = recv(sockfd, rx_buf, sizeof(rx_buf), 0)) == -1){
            perror(&quot;recv&quot;);
            exit(1);
        }
        printf(&quot;-----&gt;Client Received : %s&quot;, rx_buf);
        sleep((getpid()+i)%5);
    }
    //close socket
    close(sockfd);
    return 0;
}</code></pre>
<hr />
<h3 id="2-mytcpserver_fork_wrongc">2. mytcpserver_fork_wrong.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;   
#include &lt;errno.h&gt;
#include &lt;string.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;arpa/inet.h&gt;   
#include &lt;sys/wait.h&gt;


int main(void) {
    int server_sfd, client_sfd, bytes_recv;
    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;
    int sock_size;
    int yes = 1;
    char tx_buf[128], rx_buf[128];
    int i;

    if((server_sfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror(&quot;socket() error&quot;);
        exit(1);
    }

    if(setsockopt(server_sfd, SOL_SOCKET, SO_REUSEADDR, &amp;yes, sizeof(int)) == -1) {
        perror(&quot;setsockopt() error&quot;);
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(10000); //server port number setting
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    memset(&amp;(server_addr.sin_zero), '\0', 8);

    //server ip &amp; port number setting
    if(bind(server_sfd, (struct sockaddr *)&amp;server_addr, sizeof(struct sockaddr)) == -1) {
        perror(&quot;bind() error&quot;);
        exit(1);
    }

    //client backlog setting
    if(listen(server_sfd, 5) == -1) {
        perror(&quot;listen() error&quot;);
        exit(1);
    }

    while(1) {
        sock_size = sizeof(struct sockaddr_in);

        //wait for client request
        if((client_sfd = accept(server_sfd, (struct sockaddr *)&amp;client_addr, &amp;sock_size)) == -1) {
            perror(&quot;accept() error&quot;);
            continue;
        }

        printf(&quot;server : got connection from %s \n&quot;, inet_ntoa(client_addr.sin_addr));

        if(!fork()){
            close(server_sfd);
            for(i=1; ; i++) {
                memset(tx_buf, 0, sizeof(tx_buf));
                memset(rx_buf, 0, sizeof(rx_buf));
                //wait for rx data from client    
                if((bytes_recv = recv(client_sfd, rx_buf, sizeof(rx_buf), 0)) == -1){
                    perror(&quot;recv&quot;);
                    exit(1);
                }
                if(bytes_recv == 0) 
                    break;    
                printf(&quot;Server Rx(%d) : %s&quot;, getpid(), rx_buf);
                sprintf(tx_buf, &quot;Hi_%d, client(from %s)~~\n&quot;, i, inet_ntoa(server_addr.sin_addr));
                //send data to client
                if(send(client_sfd, tx_buf, strlen(tx_buf)+1, 0) == -1) perror(&quot;send&quot;);    
            }
            printf(&quot;Server(%d): Client Connection Socket Closed!!\n&quot;, getpid());
            //close client socket connection        
            close(client_sfd);
            exit(0);
        }
        close(client_sfd);    //parent close the client socket as they are being servered by child
        waitpid(-1, NULL, WNOHANG);
    }
    return 0;
}</code></pre>
<hr />
<h3 id="3-실행">3. 실행</h3>
<pre><code class="language-bash">$ gcc 01.mytcpclient.c -o 01.mytcpclient

$ gcc 02.mytcpserver_fork_wrong.c -o 02.mytcpserver_fork_wrong

$ ./02.mytcpserver_fork_wrong
server : got connection from 127.0.0.1
Server Rx(15574) : Hello_1 server(from 15573)!!
Server Rx(15574) : Hello_2 server(from 15573)!!
Server Rx(15574) : Hello_3 server(from 15573)!!
Server Rx(15574) : Hello_4 server(from 15573)!!
Server Rx(15574) : Hello_5 server(from 15573)!!
Server Rx(15574) : Hello_6 server(from 15573)!!
Server Rx(15574) : Hello_7 server(from 15573)!!
Server Rx(15574) : Hello_8 server(from 15573)!!
Server Rx(15574) : Hello_9 server(from 15573)!!
Server Rx(15574) : Hello_10 server(from 15573)!!
Server(15574): Client Connection Socket Closed!!

=====================================

$ ./01.mytcpclient 127.0.0.1
[ 127.0.0.1 ]
-----&gt;Client Received : Hi_1, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_2, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_3, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_4, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_5, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_6, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_7, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_8, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_9, client(from 0.0.0.0)~~
-----&gt;Client Received : Hi_10, client(from 0.0.0.0)~~</code></pre>
<p>잘 동작하는 것 같지만 Zombie 프로세스가 존재한다는 문제점이 있다.</p>
<hr />
<pre><code class="language-c">$ ps -efl |grep Z
F S UID          PID    PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
1 Z pi         15574   15571  0  80   0 -     0 -      15:20 pts/0    00:00:00 [02.mytcpserver_] &lt;defunct&gt;
0 S pi         15631   14188  0  80   0 -  1523 pipe_r 15:24 pts/2    00:00:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn Z</code></pre>
<p>이 코드가 Wrong인 결정적인 이유는 좀비 프로세스(Zombie Process)가 발생하기 때문입니다.</p>
<hr />
<h3 id="4-잘못된-부분">4. 잘못된 부분</h3>
<p>코드의 81번째 줄 <code>waitpid(-1, NULL, WNOHANG);</code> 위치가 잘못되었습니다.</p>
<ol>
<li>상황: 클라이언트가 접속하면 <code>fork()</code>를 하고, 부모는 <code>waitpid</code>를 딱 한 번 호출합니다.</li>
<li>WNOHANG: 자식 프로세스가 아직 실행 중이라면(대부분 그렇습니다), <code>waitpid</code>는 기다리지 않고 즉시 리턴합니다.</li>
<li>Blocking: 부모는 다시 <code>while</code> 루프의 처음으로 돌아가 <code>accept()</code>에서 멈춰 섭니다(Blocking).</li>
<li>문제 발생: 자식 프로세스가 1분 뒤에 종료되면? 부모는 <code>accept()</code>에서 자고 있느라 자식의 죽음을 모릅니다.</li>
<li>결과: 자식은 부모가 <code>wait</code>를 해줄 때까지 영원히 좀비 상태로 남습니다.</li>
</ol>
<hr />
<p>SIGCHLD 핸들러를 통해 해결할 수 있다. 부모가 <code>accept</code>로 자고 있어도, 자식이 죽으면 커널이 부모를 깨워서 핸들러를 실행시킵니다.</p>
<ul>
<li><p>(수정된 코드) tcpserver_fork_correct.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #include &lt;stdlib.h&gt;
  #include &lt;unistd.h&gt;
  #include &lt;errno.h&gt;
  #include &lt;string.h&gt;
  #include &lt;sys/types.h&gt;
  #include &lt;sys/socket.h&gt;
  #include &lt;arpa/inet.h&gt;
  #include &lt;sys/wait.h&gt;
  #include &lt;signal.h&gt; // [추가] 시그널 처리를 위해 필요

  #define PORT 10000

  // [추가] 좀비 프로세스 청소부 (시그널 핸들러)
  void sigchld_handler(int sig) {
      // 자식이 종료되었다는 신호를 받으면, 좀비가 된 자식을 모두 치운다.
      // WNOHANG: 아직 안 죽은 자식은 기다리지 않음
      while (waitpid(-1, NULL, WNOHANG) &gt; 0);
  }

  int main(void) {
      int server_sfd, client_sfd, bytes_recv;
      struct sockaddr_in server_addr;
      struct sockaddr_in client_addr;
      socklen_t sock_size; // int보다 socklen_t가 표준임
      int yes = 1;
      char tx_buf[128], rx_buf[128];
      int i;
      struct sigaction sa; // [추가] 시그널 설정 구조체

      if((server_sfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
          perror(&quot;socket() error&quot;);
          exit(1);
      }

      if(setsockopt(server_sfd, SOL_SOCKET, SO_REUSEADDR, &amp;yes, sizeof(int)) == -1) {
          perror(&quot;setsockopt() error&quot;);
          exit(1);
      }

      // [추가] SIGCHLD 핸들러 등록 과정
      sa.sa_handler = sigchld_handler; // 핸들러 함수 지정
      sigemptyset(&amp;sa.sa_mask);
      // SA_RESTART: 시그널 처리 후 accept()가 에러(EINTR)내지 않고 재개되도록 함
      sa.sa_flags = SA_RESTART; 
      if (sigaction(SIGCHLD, &amp;sa, NULL) == -1) {
          perror(&quot;sigaction&quot;);
          exit(1);
      }

      server_addr.sin_family = AF_INET;
      server_addr.sin_port = htons(PORT);
      server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
      memset(&amp;(server_addr.sin_zero), '\0', 8);

      if(bind(server_sfd, (struct sockaddr *)&amp;server_addr, sizeof(struct sockaddr)) == -1) {
          perror(&quot;bind() error&quot;);
          exit(1);
      }

      if(listen(server_sfd, 5) == -1) {
          perror(&quot;listen() error&quot;);
          exit(1);
      }

      printf(&quot;Server Start... waiting on port %d\n&quot;, PORT);

      while(1) {
          sock_size = sizeof(struct sockaddr_in);

          // 부모 프로세스는 여기서 대기함
          if((client_sfd = accept(server_sfd, (struct sockaddr *)&amp;client_addr, &amp;sock_size)) == -1) {
              perror(&quot;accept() error&quot;);
              continue;
          }

          printf(&quot;server : got connection from %s\n&quot;, inet_ntoa(client_addr.sin_addr));

          if(!fork()){ 
              // [자식 프로세스 영역]
              close(server_sfd); // 자식은 듣기 소켓 필요 없음

              for(i=1; ; i++) {
                  memset(tx_buf, 0, sizeof(tx_buf));
                  memset(rx_buf, 0, sizeof(rx_buf));

                  if((bytes_recv = recv(client_sfd, rx_buf, sizeof(rx_buf), 0)) == -1){
                      perror(&quot;recv&quot;);
                      exit(1);
                  }
                  if(bytes_recv == 0) // 클라이언트가 연결 끊음
                      break;

                  printf(&quot;Server Rx(%d) : %s&quot;, getpid(), rx_buf);
                  sprintf(tx_buf, &quot;Hi_%d, client(from %s)~~ \n&quot;, i, inet_ntoa(server_addr.sin_addr));

                  if(send(client_sfd, tx_buf, strlen(tx_buf)+1, 0) == -1) 
                      perror(&quot;send&quot;);
              }

              printf(&quot;Server(%d): Client Connection Socket Closed!!\n&quot;, getpid());
              close(client_sfd);
              exit(0); // 자식 종료 -&gt; SIGCHLD 발생 -&gt; 핸들러 호출됨
          }

          // [부모 프로세스 영역]
          close(client_sfd); 

          // [삭제됨] waitpid(-1, NULL, WNOHANG); 
          // 이유: 여기서 기다리는 게 아니라 시그널 핸들러가 알아서 처리함
      }
      return 0;
  }</code></pre>
</li>
</ul>
<hr />
<h3 id="5-수정된-부분">5. 수정된 부분</h3>
<ol>
<li><p><code>sigchld_handler</code> 함수 추가: 자식이 죽으면 호출되어 좀비를 수거합니다.</p>
</li>
<li><p><code>sigaction</code> 설정: <code>SA_RESTART</code> 플래그를 사용하여, 시그널 핸들러가 실행된 뒤 <code>accept()</code>가 에러를 뱉지 않고 계속 대기하도록 설정했습니다.</p>
</li>
<li><p><code>waitpid</code> 삭제: <code>while(1)</code> 루프 안에 있던 어설픈 <code>waitpid</code>를 제거했습니다. 이제 부모는 오직 연결 요청(<code>accept</code>)에만 집중합니다.</p>
</li>
</ol>
<hr />
<pre><code class="language-c">if(setsockopt(server_sfd, SOL_SOCKET, SO_REUSEADDR, &amp;yes, sizeof(int)) == -1)</code></pre>
<p>위 코드의 의미?</p>
<ul>
<li>서버를 껐다가 바로 다시 켤 때 발생하는 에러를 막기 위해 사용</li>
<li>이 코드가 없으면 서버를 Ctrl+C 로 강제 종료하고 다시 실행시, <code>bind() error: Address already in use</code> 에러 발생</li>
</ul>