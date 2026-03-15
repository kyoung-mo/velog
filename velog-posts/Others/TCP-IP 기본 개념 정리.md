<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/748ace8f-a6d8-4286-8e88-cf837467612b/image.png" /></p>
<p>TCP/IP에 대해 대학에서도 수업을 들었었고, 이번 교육동안에도 수업을 진행했었는데 머리속에서 코드가 안 나오고, 실제 코드를 봐도 정확한 설명이 어렵다고 생각해서 기초부터 다시 정리하려합니다.</p>
<hr />
<h2 id="소켓">소켓</h2>
<p>네트워크(인터넷)의 연결 도구
<strong>운영체제에 의해 제공</strong>이 되는 소프트웨어적인 장치</p>
<pre><code class="language-c">#include &lt;sys/socket.h&gt;

int socket(int domain, int type, int protocol);
// 성공 시 파일 디스크립터, 실패 시 -1 반환

int bind(int sockfd, struct sockaddr *myaddr, socklen_t addrlen);
// 성공 시 0, 실패 시 -1 반환

int listen(int sockfd, int backlog);
// 성공 시 0, 실패 시 -1 반환

int accept(int sockfd, struct sockaddr *addr, socklen_t* addrlen);
// 성공 시 파일 디스크립터, 실패 시 -1 반환</code></pre>
<p><strong>소켓의 생성 과정</strong></p>
<ol>
<li>소켓의 생성 : socket 함수 호출</li>
<li>IP와 PORT 번호의 할당 : bind 함수 호출</li>
<li>연결요청 가능상태로 변경 : listen 함수 호출</li>
<li>연결요청에 대한 수락 : accept 함수 호출</li>
</ol>
<pre><code class="language-c">#include &lt;sys/socket.h&gt;

int connect(int sockfd, struct sockaddr* serv_addr, socklen_t addrlen);
// 성공 시 0, 실패 시 -1 반환</code></pre>
<hr />
<h2 id="저-수준-파일-입출력">저 수준 파일 입출력</h2>
<p>ANSI의 표준함수가 아닌, 운영체제가 제공하는 함수 기반의 파일 입출력.
표준이 아니기 때문에 운영체제에 대한 호환성이 없다.
리눅스는 소켓도 파일로 간주하기 때문에 저 수준 파일 입출력 함수를 기반으로 소켓 기반의 데이터 송수신이 가능하다.</p>
<h2 id="파일-디스크립터">파일 디스크립터</h2>
<p>운영체제가 만든 파일(그리고 소켓)을 구분하기 위한 일종의 숫자
저 수준 파일 입출력 함수는 입출력을 목적으로 파일 디스크립터를 요구함
저 수준 파일 입출력 함수에게 소켓의 파일 디스크립터를 전달하면, 소켓을 대상으로 입출력 진행</p>
<table>
<thead>
<tr>
<th>파일 디스크립터</th>
<th>대상</th>
</tr>
</thead>
<tbody><tr>
<td>0</td>
<td>표준 입력 : Standard Input</td>
</tr>
<tr>
<td>1</td>
<td>표준출력: Standard Output</td>
</tr>
<tr>
<td>2</td>
<td>표준에러 : Standard Error</td>
</tr>
</tbody></table>
<hr />
<h2 id="파일-열기와-닫기">파일 열기와 닫기</h2>
<p><strong>파일 열기</strong></p>
<pre><code class="language-c">#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;

int open(const char *path, int flag);
// 성공 시 파일 디스크립터, 실패 시 -1 반환</code></pre>
<ul>
<li>path : 파일 이름을 나타내는 문자열의 주소 값 전달</li>
<li>flag : 파일의 오픈 모드 정보 전달</li>
</ul>
<p><strong>파일 닫기</strong></p>
<pre><code class="language-c">#inclide &lt;unistd.h&gt;

int close(int fd);
// 성공 시 0, 실패 시 -1 반환</code></pre>
<ul>
<li>fd : 닫고자 하는 파일 또는 소켓의 파일 디스크립터 전달</li>
</ul>
<table>
<thead>
<tr>
<th>오픈 모드</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>O_CREAT</td>
<td>필요하면 파일을 생성</td>
</tr>
<tr>
<td>O_TRUNC</td>
<td>기존 데이터 전부 삭제</td>
</tr>
<tr>
<td>O_APPEND</td>
<td>기존 데이터 보존하고, 뒤에 이어서 저장</td>
</tr>
<tr>
<td>O_RDONLY</td>
<td>읽기 전용으로 파일 오픈</td>
</tr>
<tr>
<td>O_WRONLY</td>
<td>쓰기 전용으로 파일 오픈</td>
</tr>
<tr>
<td>O_RDWR</td>
<td>읽기, 쓰기 겸용으로 파일 오픈</td>
</tr>
</tbody></table>
<blockquote>
<p><code>open()</code> 함수 호출 시 반환된 파일 디스크립터를 이용해서 파일 입출력을 진행하게 된다.</p>
</blockquote>
<h2 id="파일에-데이터-쓰기">파일에 데이터 쓰기</h2>
<pre><code class="language-c">#include &lt;unistd.h&gt;

ssize_t write(int fd, const void* buf, size_t nbytes);
// 성공 시 전달한 바이트 수, 실패 시 -1 반환</code></pre>
<ul>
<li>fd : 데이터 전송대상을 나타내는 파일 디스크립터 전달</li>
<li>buf: 전송할 데이터가 저장된 버퍼의 주소 값 전달</li>
<li>nbytes: 전송할 데이터의 바이트 수 전달</li>
</ul>
<h2 id="파일에-저장된-데이터-읽기">파일에 저장된 데이터 읽기</h2>
<pre><code class="language-c">#include &lt;unistd.h&gt;

ssize_t read(int fd, void* buf, size_t nbytes);
// 성공 시 수신한 바이트 수(단 파일의 끝을 만나면 0), 실패 시 -1 반환</code></pre>
<ul>
<li>fd : 데이터 수신 대상을 나타내는 파일 디스크립터 전달</li>
<li>buf: 수신한 데이터를 저장할 버퍼의 주소 값 전달</li>
<li>nbytes: 수신할 최대 바이트 수 전달</li>
</ul>
<hr />
<h2 id="프로토콜">프로토콜</h2>
<p>프로토콜 = 약속
컴퓨터 상호간 데이터 송수신 시 필요한 통신 규약을 의미한다.</p>
<p>** 프로토콜 체계**</p>
<table>
<thead>
<tr>
<th>이름</th>
<th>프로토콜체계(Protocol Family)</th>
</tr>
</thead>
<tbody><tr>
<td>PF_INET</td>
<td>IPv4 인터넷 프로토콜 체계</td>
</tr>
<tr>
<td>PF_INET6</td>
<td>IPv6 인터넷 프로토콜 체계</td>
</tr>
<tr>
<td>PF_LOCAL</td>
<td>로컬 통신을 위한 UNIX 프로토콜 체계</td>
</tr>
<tr>
<td>PF_PACKET</td>
<td>Low Level 소켓을 위한 프로토콜 체계</td>
</tr>
<tr>
<td>PF_IPX</td>
<td>IPX 노벨 프로토콜 체계</td>
</tr>
</tbody></table>
<p>** TCP vs UDP**</p>
<pre><code class="language-c">// TCP 소켓
int tcp_socket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

// UDP 소켓
int udp_socket = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP);</code></pre>
<h2 id="ipv4-기반-주소-표현을-위한-구조체">IPv4 기반 주소 표현을 위한 구조체</h2>
<pre><code class="language-c">struct sockaddr_in
{
    sa_family_t        sin_family;        // 주소 체계
    uint16_t        sin_port;        // PORT 번호
    struct in_addr    sin_addr;        // 32비트 IP 주소
    char            sin_zero[8];    // 사용되지 않음
};


struct in_addr
{
    in_addr_t        s_addr;        // 32비트 IPv4 인터넷 주소
};</code></pre>
<hr />
<h2 id="바이트-순서order와-네트워크-바이트-순서">바이트 순서(Order)와 네트워크 바이트 순서</h2>
<p><strong>빅 엔디안(Big Endian)</strong>
: 상위 바이트의 값을 작은 번지수에 저장</p>
<p><strong>리틀 엔디안(Little Endian)</strong>
: 상위 바이트의 값을 큰 번지수에 저장</p>
<p><strong>호스트 바이트 순서</strong>
: CPU별 데이터 저장 방식을 의미</p>
<p><strong>네트워크 바이트 순서</strong>
: 기준 &gt; 빅엔디안</p>
<h2 id="바이트-순서-변환">바이트 순서 변환</h2>
<pre><code class="language-c">unsigned short htons(unsigned short);
unsigned short ntohs(unsigned short);
unsigned long htons(unsigned long);
unsigned long ntohs(unsigned long);</code></pre>
<p><strong>htons / htonl</strong></p>
<ul>
<li>h : 호스트(host) 바이트 순서</li>
<li>n : 네트워크(network) 바이트 순서</li>
<li>s : 자료형 short</li>
<li>l : 자료형 long</li>
</ul>
<pre><code class="language-c">#include &lt;arpa/inet.h&gt;

in_addr_t inet_addr(const char* string);
// 성공 시 빅 엔디안으로 변환된 32비트 정수 값, 실패 시 INADDR_NONE 반환

int inet_aton(const char* string, struct in_addr* addr);
// 성공 시 1(true), 실패 시 0(false) 반환</code></pre>
<ul>
<li>string : 변환할 IP 주소 정보를 담고 있는 문자열의 주소 값 전달</li>
<li>addr : 변환된 정보를 저장할 in_addr 구조체 변수의 주소 값 전달</li>
</ul>
<pre><code class="language-c">#include &lt;arpa/inet.h&gt;

char* inet_ntoa(struct in_addr adr);
// 성공 시 변환된 문자열의 주소 값, 실패 시 -1 반환</code></pre>
<ul>
<li>INADDR_ANY : 현재 실행중인 컴퓨터의 IP를 소켓에 부여할 때 사용</li>
</ul>