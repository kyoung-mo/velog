<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/da0ac5c0-d153-4314-a565-d3830985e414/image.png" /></p>
<h3 id="네트워크-프로그래밍의-구조">네트워크 프로그래밍의 구조</h3>
<p> 하드웨어의 복잡성을 운영체제(OS)가 감추고, 우리는 소켓이라는 구멍만 보고 코딩하면 됩니다.</p>
<hr />
<h3 id="1-소켓의-위치">1. 소켓의 위치</h3>
<p>소켓은 응용 프로그램(Application)과 운영체제(Kernel) 사이의 &quot;인터페이스(Interface)&quot;이자 &quot;창구&quot;입니다. 개발자는 복잡한 TCP/IP 패킷 구조를 몰라도 소켓에 데이터를 쓰기만 하면 전송이 됩니다.</p>
<ul>
<li>Application 관점: 소켓은 그냥 파일(File)입니다. (데이터를 넣고 뺄 수 있는 구멍).</li>
<li>Kernel 관점: 소켓은 네트워크 통신을 위한 제어 정보(IP, Port, 프로토콜 상태)를 담고 있는 구조체입니다.</li>
</ul>
<hr />
<h3 id="2-핵심-비유-소켓--전화기">2. 핵심 비유: 소켓 = 전화기</h3>
<p>소켓 통신은 전화 시스템과 완벽하게 대응됩니다.</p>
<table>
<thead>
<tr>
<th>소켓 개념</th>
<th>전화기 비유</th>
</tr>
</thead>
<tbody><tr>
<td>Socket</td>
<td>전화기 (통신을 위한 도구)</td>
</tr>
<tr>
<td>IP 주소</td>
<td>전화번호 (상대방의 위치)</td>
</tr>
<tr>
<td>Port 번호</td>
<td>내선 번호 (누구랑 통화할지 - 김대리, 이과장)</td>
</tr>
<tr>
<td><code>socket()</code></td>
<td>전화기 설치 (통신 준비)</td>
</tr>
<tr>
<td><code>bind()</code></td>
<td>전화번호 개통 (내 번호 할당)</td>
</tr>
<tr>
<td><code>listen()</code></td>
<td>전화선 연결해두기 (벨 울릴 준비)</td>
</tr>
<tr>
<td><code>accept()</code></td>
<td>수화기 들기 (연결 성립)</td>
</tr>
<tr>
<td><code>connect()</code></td>
<td>다이얼 돌리기 (상대방에게 연결 요청)</td>
</tr>
<tr>
<td><code>read/write()</code></td>
<td>말하고 듣기 (데이터 송수신)</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-일반-파일-io-vs-소켓-io">3. 일반 파일 I/O vs 소켓 I/O</h3>
<p> 어플리케이션이 어떻게 오픈하는가에 차이가 있습니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>일반 파일 (File I/O)</th>
<th>소켓 (Socket I/O)</th>
</tr>
</thead>
<tbody><tr>
<td>생성/오픈</td>
<td><code>open()</code> 함수 하나로 끝.</td>
<td>복잡함. <code>socket()</code> → <code>bind()</code> → <code>listen()</code> → <code>accept()</code> (서버 기준) 과정을 거쳐야 함.</td>
</tr>
<tr>
<td>식별자</td>
<td>파일 경로 (<code>/home/user/test.txt</code>)</td>
<td>IP 주소 + 포트 번호</td>
</tr>
<tr>
<td>데이터 흐름</td>
<td>단방향 또는 양방향 (보통 디스크 저장)</td>
<td>양방향 (Full Duplex) 통신 (네트워크 전송)</td>
</tr>
<tr>
<td>공통점</td>
<td>둘 다 <code>int</code>형의 파일 디스크립터(FD)를 반환하며, <code>read()</code>, <code>write()</code>, <code>close()</code> 함수를 똑같이 사용함.</td>
<td></td>
</tr>
</tbody></table>
<hr />
<h3 id="4-소켓-사용-실습">4. 소켓 사용 실습</h3>
<p>리눅스 커널에서 소켓을 파일처럼 사용하면 됩니다.</p>
<pre><code class="language-c">#include &lt;sys/socket.h&gt;
#include &lt;unistd.h&gt;

int main() {
    // 1. 소켓 생성 (전화기 구입)
    // 반환값 server_fd는 그냥 정수(Integer)입니다. (예: 3)
    int server_fd = socket(AF_INET, SOCK_STREAM, 0); 

    // ... (bind, listen, accept 과정 생략) ...

    // 2. 클라이언트와 연결되면 새로운 소켓 FD가 나옴 (예: 4)
    int client_fd = accept(server_fd, ...);

    // 3. 파일처럼 쓰기 (Write)
    // write 함수는 이게 파일인지 소켓인지 신경 안 씁니다.
    // 그냥 &quot;4번 디스크립터에 데이터를 써라&quot;라고 커널에 요청할 뿐입니다.
    char *msg = &quot;Hello World&quot;;
    write(client_fd, msg, strlen(msg)); 

    // 4. 파일처럼 닫기 (Close)
    close(client_fd);
    close(server_fd);

    return 0;
}</code></pre>
<hr />
<h3 id="5-버클리-소켓-berkeley-sockets의-의의">5. 버클리 소켓 (Berkeley Sockets)의 의의</h3>
<p> 1983년 BSD 유닉스에서 만든 이 인터페이스가 사실상 표준(De facto standard)이 되었습니다.</p>
<ul>
<li>현재 윈도우(Winsock), 자바, 파이썬 등 지구상의 거의 모든 네트워크 프로그램은 이 버클리 소켓 구조를 그대로 따르고 있습니다.</li>
<li>즉, 리눅스 소켓을 배우면 모든 언어와 OS의 네트워크 프로그래밍 원리를 배우는 것과 같습니다.</li>
</ul>