<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ea479039-0f50-4dca-a75c-1635c3cd559a/image.png" /></p>
<hr />
<h3 id="실습-순서-정리">실습 순서 정리</h3>
<ol>
<li>Server가 먼저 열려 있어야 Client가 연결 시도를 할 수 있다.</li>
<li><code>gcc basic_server.c -o basic_server</code> -&gt; 서버 실행 파일 만들기</li>
<li><code>gcc basic_client.c -o basic_client</code> -&gt; 서버 실행 파일 만들기</li>
<li>서버 실행 <code>./basic_server [포트]</code> </li>
<li>클라이언트 접속 <code>./basic_client [서버IP_Addr] [포트]</code></li>
</ol>
<hr />
<h3 id="basic_serverc">basic_server.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;arpa/inet.h&gt;

int main(int argc, char *argv[]){
    int server_sfd;
    int client_sfd;

    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;
    socklen_t sock_size;

    int bytes_sent;
    char message[]=&quot;Welcome to Linux Network Programming!&quot;;
    int yes = 1;

    if(argc!=2){
        printf(&quot;Usage : %s &lt;port&gt;\n&quot;, argv[0]);
        exit(1);
    }

    server_sfd=socket(PF_INET, SOCK_STREAM, 0);
    if(server_sfd == -1){
        perror(&quot;socket() error!!&quot;);
        exit(1);
    }

#if 0
    if(setsockopt(server_sfd, SOL_SOCKET, SO_REUSEADDR, &amp;yes, sizeof(int)) == -1){
        perror(&quot;setsockopt() error!!&quot;);
        exit(1);
    }
#endif

    memset(&amp;server_addr, 0, sizeof(server_addr));
    server_addr.sin_family=AF_INET;
    server_addr.sin_addr.s_addr=htonl(INADDR_ANY);
    server_addr.sin_port=htons(atoi(argv[1]));

    if(bind(server_sfd, (struct sockaddr*) &amp;server_addr, sizeof(server_addr))==-1 ){
        perror(&quot;bind() error!!&quot;);
        exit(1);
    }

    if(listen(server_sfd, 10)==-1){
        perror(&quot;listen() error!!&quot;);
        exit(1);
    }

    sock_size=sizeof(client_addr);  
    client_sfd=accept(server_sfd, (struct sockaddr*)&amp;client_addr,&amp;sock_size);
    printf(&quot;Connected to the client port --&gt; %d\n&quot;, htons(client_addr.sin_port));
    if(client_sfd==-1){
        perror(&quot;accept() error!!&quot;);
        exit(1);
    }

    bytes_sent = send(client_sfd, message, strlen(message), 0);
    //bytes_sent=write(client_sfd, message, sizeof(message));
    printf(&quot;bytes_sent : %d\n&quot;, bytes_sent);

    printf(&quot;Press Enter to close the socket!!!&quot;);
    getchar();

    close(client_sfd);    
    close(server_sfd);
    return 0;
}</code></pre>
<hr />
<h3 id="basic_clientc">basic_client.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;arpa/inet.h&gt;
#include &lt;netdb.h&gt;

int main(int argc, char* argv[]){
    int sockfd;
    struct sockaddr_in sockaddr;
    char message[500];
    int bytes_recv;
    socklen_t len;

    if(argc!=3){
        printf(&quot;Usage : %s &lt;IP&gt; &lt;port&gt;\n&quot;, argv[0]);
        exit(1);
    }

    sockfd=socket(PF_INET, SOCK_STREAM, 0);
    if(sockfd == -1){
        perror(&quot;sockfdet() error!!&quot;);
        exit(1);
    }

    memset(&amp;sockaddr, 0, sizeof(sockaddr));
    sockaddr.sin_family=AF_INET;
    sockaddr.sin_addr.s_addr=inet_addr(argv[1]);
    sockaddr.sin_port=htons(atoi(argv[2]));

    if(connect(sockfd, (struct sockaddr*)&amp;sockaddr, sizeof(sockaddr))==-1){
        perror(&quot;connect() error!!&quot;);
        exit(1);
    }

#if 1            //It is to see the peer information in terms of name and port #
    len = sizeof(sockaddr);
    getpeername(sockfd, (struct sockaddr*)&amp;sockaddr, &amp;len);
    printf(&quot;Peer IP address: %s\n&quot;, inet_ntoa(sockaddr.sin_addr));
    printf(&quot;Peer port      : %d\n&quot;, ntohs(sockaddr.sin_port));
#endif
    bzero(&amp;message, sizeof(message));
    bytes_recv=recv(sockfd, message, sizeof(message), 0);
    //bytes_recv=read(sockfd, message, sizeof(message));
    if(bytes_recv==-1){
        perror(&quot;recv() error!!&quot;);
        exit(1);
    }
    printf(&quot;Message from server: %s (%d)\n&quot;, message, bytes_recv); 

    printf(&quot;Press Enter to close the socket!!!&quot;);
    getchar();

    close(sockfd);
    return 0;
}</code></pre>