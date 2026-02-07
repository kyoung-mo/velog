<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/358edbc1-39ca-4496-8c9c-019298b8a73c/image.png" /></p>
<h2 id="📚-목차">📚 목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-%EA%B8%B0%EB%B3%B8-%EC%9B%90%EC%B9%99">기본 원칙</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-%EC%86%8C%EC%BC%93%EC%9D%98-%EC%9C%A0%EC%9D%BC%EC%84%B1-4-tuple">소켓의 유일성 (4-Tuple)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-port-%EB%B2%88%ED%98%B8-%EB%B2%94%EC%9C%84">Port 번호 범위</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-bind-%ED%95%A8%EC%88%98%EC%9D%98-%EC%97%AD%ED%95%A0">bind() 함수의 역할</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-%EC%86%8C%EC%BC%93-%EC%A3%BC%EC%86%8C-%EA%B5%AC%EC%A1%B0%EC%B2%B4">소켓 주소 구조체</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-%EB%B0%94%EC%9D%B4%ED%8A%B8-%EC%88%9C%EC%84%9C-%EB%B3%80%ED%99%98-endian">바이트 순서 변환 (Endian)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-%ED%8A%B9%EC%88%98-ip-%EC%A3%BC%EC%86%8C">특수 IP 주소</a></li>
<li><a href="https://api.velog.io/rss/@mommers#8-ip-%EC%A3%BC%EC%86%8C-%EB%AC%B8%EC%9E%90%EC%97%B4-%EB%B3%80%ED%99%98">IP 주소 문자열 변환</a></li>
<li><a href="https://api.velog.io/rss/@mommers#9-%EC%A0%95%EB%A6%AC">정리</a></li>
</ol>
<hr />
<h3 id="1-기본-원칙">1. 기본 원칙</h3>
<p><strong>&quot;IP는 호스트(컴퓨터)를 찾고, Port는 프로세스(애플리케이션)를 찾는다&quot;</strong></p>
<h4 id="주소-체계">주소 체계</h4>
<table>
<thead>
<tr>
<th>구분</th>
<th>역할</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>IP 주소</strong></td>
<td>호스트 식별</td>
<td>네트워크에서 특정 컴퓨터를 찾음</td>
</tr>
<tr>
<td><strong>Port 번호</strong></td>
<td>프로세스 식별</td>
<td>해당 컴퓨터에서 실행 중인 특정 애플리케이션을 찾음</td>
</tr>
<tr>
<td><strong>Socket</strong></td>
<td>통신 엔드포인트</td>
<td>실제 데이터가 송수신되는 통로</td>
</tr>
</tbody></table>
<p><strong>예시:</strong></p>
<pre><code>웹 서버 접속: 192.168.1.100:80
               ↑           ↑
             IP 주소    Port 번호
              (서버)     (HTTP)</code></pre><hr />
<h3 id="2-소켓의-유일성-4-tuple">2. 소켓의 유일성 (4-Tuple)</h3>
<h3 id="2-1-연결connection-식별">2-1. 연결(Connection) 식별</h3>
<p>인터넷상의 모든 TCP 연결은 <strong>4가지 정보</strong>로 유일하게 식별됩니다:</p>
<pre><code>하나의 연결 = {송신지 IP, 송신지 Port, 수신지 IP, 수신지 Port}</code></pre><p><strong>예시:</strong></p>
<pre><code>연결 1: {192.168.1.10:54321, 8.8.8.8:80}
연결 2: {192.168.1.10:54322, 8.8.8.8:80}  ← 포트 하나만 달라도 다른 연결!</code></pre><h3 id="2-2-5-tuple-프로토콜-포함">2-2. 5-Tuple (프로토콜 포함)</h3>
<p>방화벽이나 NAT에서는 프로토콜까지 포함한 <strong>5-Tuple</strong> 사용:</p>
<pre><code>{송신지 IP, 송신지 Port, 수신지 IP, 수신지 Port, 프로토콜(TCP/UDP)}</code></pre><hr />
<h3 id="3-port-번호-범위">3. Port 번호 범위</h3>
<h3 id="3-1-전체-범위-0--65535">3-1. 전체 범위 (0 ~ 65535)</h3>
<table>
<thead>
<tr>
<th>범위</th>
<th>이름</th>
<th>용도</th>
<th>예시</th>
</tr>
</thead>
<tbody><tr>
<td><strong>0 ~ 1023</strong></td>
<td>Well-Known Ports</td>
<td>시스템/표준 서비스 (Root 권한 필요)</td>
<td>HTTP(80), SSH(22), FTP(21), HTTPS(443)</td>
</tr>
<tr>
<td><strong>1024 ~ 49151</strong></td>
<td>Registered Ports</td>
<td>특정 애플리케이션이 등록하여 사용</td>
<td>MySQL(3306), PostgreSQL(5432), Tomcat(8080)</td>
</tr>
<tr>
<td><strong>49152 ~ 65535</strong></td>
<td>Dynamic/Private Ports</td>
<td>클라이언트 임시 포트 (Ephemeral)</td>
<td>웹 브라우저가 서버 접속 시 사용</td>
</tr>
</tbody></table>
<h3 id="3-2-리눅스-기본-설정">3-2. 리눅스 기본 설정</h3>
<p>리눅스 커널의 <strong>동적 포트 범위</strong> 기본값:</p>
<pre><code class="language-bash">$ sudo sysctl -a | grep port_range
net.ipv4.ip_local_port_range = 32768    60999</code></pre>
<p><strong>설명:</strong></p>
<ul>
<li>클라이언트가 <code>connect()</code> 호출 시 이 범위에서 자동 할당</li>
<li>서버는 고정 포트를 사용하므로 이 범위와 무관</li>
</ul>
<p><strong>범위 변경 (대용량 서버 튜닝):</strong></p>
<pre><code class="language-bash"># 동적 포트 범위 확대
sudo sysctl -w net.ipv4.ip_local_port_range=&quot;10000 65535&quot;</code></pre>
<hr />
<h3 id="4-bind-함수의-역할">4. bind() 함수의 역할</h3>
<h3 id="4-1-정의">4-1. 정의</h3>
<p><strong><code>bind()</code></strong> = 소켓에 IP 주소와 Port 번호를 할당하는 함수</p>
<pre><code class="language-c">int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);</code></pre>
<h3 id="4-2-서버-vs-클라이언트">4-2. 서버 vs 클라이언트</h3>
<h4 id="서버-server">서버 (Server)</h4>
<ul>
<li><strong>반드시 <code>bind()</code> 호출 필요</strong></li>
<li>클라이언트가 찾아올 수 있도록 <strong>고정된 주소</strong> 할당</li>
</ul>
<pre><code class="language-c">struct sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);           // 고정 포트
server_addr.sin_addr.s_addr = INADDR_ANY;     // 모든 IP 수신

bind(server_fd, (struct sockaddr*)&amp;server_addr, sizeof(server_addr));</code></pre>
<h4 id="클라이언트-client">클라이언트 (Client)</h4>
<ul>
<li><strong>보통 <code>bind()</code> 생략</strong></li>
<li><code>connect()</code> 호출 시 커널이 <strong>자동으로 동적 포트 할당</strong> (Implicit Bind)</li>
</ul>
<pre><code class="language-c">// bind() 없이 바로 connect()
connect(client_fd, (struct sockaddr*)&amp;server_addr, sizeof(server_addr));

// 커널이 자동으로 32768~60999 범위에서 남는 포트 할당</code></pre>
<hr />
<h3 id="5-소켓-주소-구조체">5. 소켓 주소 구조체</h3>
<h3 id="5-1-struct-sockaddr_in-ipv4">5-1. struct sockaddr_in (IPv4)</h3>
<pre><code class="language-c">#include &lt;netinet/in.h&gt;

struct sockaddr_in {
    sa_family_t    sin_family;  // 주소 체계 (AF_INET = IPv4)
    in_port_t      sin_port;    // Port 번호 (16비트, Big Endian)
    struct in_addr sin_addr;    // IP 주소 (32비트, Big Endian)
    char           sin_zero[8]; // 패딩 (사용 안 함)
};

struct in_addr {
    in_addr_t s_addr;           // 32비트 IP 주소
};</code></pre>
<h3 id="5-2-필드-설명">5-2. 필드 설명</h3>
<table>
<thead>
<tr>
<th>필드</th>
<th>타입</th>
<th>크기</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>sin_family</code></td>
<td><code>sa_family_t</code></td>
<td>2바이트</td>
<td>주소 체계 (<code>AF_INET</code>, <code>AF_INET6</code>)</td>
</tr>
<tr>
<td><code>sin_port</code></td>
<td><code>in_port_t</code></td>
<td>2바이트</td>
<td>Port 번호 (네트워크 바이트 순서)</td>
</tr>
<tr>
<td><code>sin_addr</code></td>
<td><code>struct in_addr</code></td>
<td>4바이트</td>
<td>IP 주소 (네트워크 바이트 순서)</td>
</tr>
<tr>
<td><code>sin_zero</code></td>
<td><code>char[8]</code></td>
<td>8바이트</td>
<td>패딩 (전체 크기를 16바이트로 맞춤)</td>
</tr>
</tbody></table>
<hr />
<h3 id="5-3-사용-예시">5-3. 사용 예시</h3>
<pre><code class="language-c">#include &lt;sys/socket.h&gt;
#include &lt;netinet/in.h&gt;
#include &lt;arpa/inet.h&gt;

int main() {
    // 1. 소켓 생성
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    // 2. 주소 구조체 설정
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;                    // IPv4
    addr.sin_port = htons(8080);                  // 포트 8080 (Host to Network Short)
    addr.sin_addr.s_addr = htonl(INADDR_ANY);     // 모든 IP에서 수신 (0.0.0.0)

    // 또는 특정 IP 지정
    // inet_pton(AF_INET, &quot;192.168.1.10&quot;, &amp;addr.sin_addr);

    // 3. 소켓에 주소 바인딩
    bind(server_fd, (struct sockaddr*)&amp;addr, sizeof(addr));

    return 0;
}</code></pre>
<hr />
<h3 id="6-바이트-순서-변환-endian">6. 바이트 순서 변환 (Endian)</h3>
<h3 id="6-1-왜-필요한가">6-1. 왜 필요한가?</h3>
<ul>
<li><strong>네트워크 바이트 순서</strong>: Big Endian (표준)</li>
<li><strong>호스트 바이트 순서</strong>: CPU 아키텍처에 따라 다름 (Intel/AMD = Little Endian)</li>
</ul>
<p><strong>문제:</strong></p>
<pre><code>숫자 1234를 네트워크로 전송할 때:
Intel CPU: 0xD2 0x04 (Little Endian)
Network:   0x04 0xD2 (Big Endian)
→ 변환 필요!</code></pre><h3 id="6-2-변환-함수">6-2. 변환 함수</h3>
<table>
<thead>
<tr>
<th>함수</th>
<th>설명</th>
<th>예시</th>
</tr>
</thead>
<tbody><tr>
<td><code>htons()</code></td>
<td>Host to Network Short (16비트)</td>
<td>Port 번호 변환</td>
</tr>
<tr>
<td><code>htonl()</code></td>
<td>Host to Network Long (32비트)</td>
<td>IP 주소 변환</td>
</tr>
<tr>
<td><code>ntohs()</code></td>
<td>Network to Host Short (16비트)</td>
<td>Port 번호 변환</td>
</tr>
<tr>
<td><code>ntohl()</code></td>
<td>Network to Host Long (32비트)</td>
<td>IP 주소 변환</td>
</tr>
</tbody></table>
<p><strong>예시:</strong></p>
<pre><code class="language-c">// 호스트 → 네트워크
uint16_t port = 8080;
uint16_t net_port = htons(port);        // 8080 → Big Endian

// 네트워크 → 호스트
uint16_t recv_port = ntohs(net_port);   // Big Endian → 8080</code></pre>
<hr />
<h3 id="7-특수-ip-주소">7. 특수 IP 주소</h3>
<h3 id="7-1-inaddr_any-0000">7-1. INADDR_ANY (0.0.0.0)</h3>
<p><strong>의미:</strong></p>
<ul>
<li>&quot;모든 네트워크 인터페이스에서 수신&quot;</li>
<li>서버가 여러 IP를 가진 경우 모든 IP로 들어오는 연결 수락</li>
</ul>
<pre><code class="language-c">addr.sin_addr.s_addr = htonl(INADDR_ANY);  // 0.0.0.0</code></pre>
<p><strong>사용 예:</strong></p>
<pre><code>서버의 IP:
- eth0: 192.168.1.10
- eth1: 10.0.0.5

INADDR_ANY로 bind → 두 IP 모두에서 연결 수락</code></pre><h3 id="7-2-inaddr_loopback-127001">7-2. INADDR_LOOPBACK (127.0.0.1)</h3>
<p><strong>의미:</strong></p>
<ul>
<li>자기 자신 (Loopback)</li>
<li>같은 컴퓨터 내에서만 통신</li>
</ul>
<pre><code class="language-c">addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);  // 127.0.0.1</code></pre>
<hr />
<h3 id="8-ip-주소-문자열-변환">8. IP 주소 문자열 변환</h3>
<h3 id="8-1-문자열-→-이진-inet_pton">8-1. 문자열 → 이진 (inet_pton)</h3>
<pre><code class="language-c">#include &lt;arpa/inet.h&gt;

struct sockaddr_in addr;
inet_pton(AF_INET, &quot;192.168.1.10&quot;, &amp;addr.sin_addr);
// &quot;192.168.1.10&quot; → 32비트 이진 데이터</code></pre>
<h3 id="8-2-이진-→-문자열-inet_ntop">8-2. 이진 → 문자열 (inet_ntop)</h3>
<pre><code class="language-c">char ip_str[INET_ADDRSTRLEN];  // 16바이트 버퍼
inet_ntop(AF_INET, &amp;addr.sin_addr, ip_str, INET_ADDRSTRLEN);
// 32비트 이진 → &quot;192.168.1.10&quot;</code></pre>
<p><strong>참고:</strong></p>
<ul>
<li><code>inet_addr()</code>, <code>inet_ntoa()</code>는 구식 함수 (사용 권장 안 함)</li>
<li><code>inet_pton()</code>, <code>inet_ntop()</code>가 IPv4/IPv6 모두 지원</li>
</ul>
<hr />
<h3 id="9-정리">9. 정리</h3>
<h3 id="핵심-요약">핵심 요약</h3>
<table>
<thead>
<tr>
<th>개념</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>IP 주소</strong></td>
<td>네트워크에서 호스트(컴퓨터) 식별</td>
</tr>
<tr>
<td><strong>Port 번호</strong></td>
<td>호스트 내에서 프로세스(애플리케이션) 식별</td>
</tr>
<tr>
<td><strong>4-Tuple</strong></td>
<td>{송신지 IP, 송신지 Port, 수신지 IP, 수신지 Port}</td>
</tr>
<tr>
<td><strong>bind()</strong></td>
<td>소켓에 IP와 Port 할당 (서버 필수, 클라이언트 선택)</td>
</tr>
<tr>
<td><strong>Well-Known Port</strong></td>
<td>0~1023 (시스템 서비스)</td>
</tr>
<tr>
<td><strong>Ephemeral Port</strong></td>
<td>49152~65535 (클라이언트 임시 포트)</td>
</tr>
<tr>
<td><strong>Endian 변환</strong></td>
<td><code>htons()</code>, <code>htonl()</code>, <code>ntohs()</code>, <code>ntohl()</code></td>
</tr>
</tbody></table>
<h3 id="기억할-점">기억할 점</h3>
<ul>
<li>IP는 &quot;어느 컴퓨터&quot;, Port는 &quot;어떤 프로그램&quot;</li>
<li>서버는 반드시 <code>bind()</code> 필요 (고정 주소)</li>
<li>클라이언트는 <code>bind()</code> 생략 가능 (자동 할당)</li>
<li>네트워크 전송 시 항상 Big Endian 변환</li>
<li><code>INADDR_ANY</code> = 모든 IP에서 수신</li>
<li>하나의 TCP 연결 = 고유한 4-Tuple</li>
</ul>