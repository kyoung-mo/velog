<h3 id="네트워크-연결-확인-ping-ip-ifconfig">네트워크 연결 확인 (ping, ip, ifconfig)</h3>
<ul>
<li>IP 주소 확인, 인터넷 연결 상태 점검을 목표로</li>
<li><code>ip addr show</code>로 내 IP(Private IP) 확인.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/653cf2d2-43f7-4770-93d3-8c9d636aa87e/image.png" /></p>
<ul>
<li><p><code>ping 8.8.8.8</code>로 외부 인터넷 연결 확인.</p>
</li>
<li><p>본인 IP
<img alt="" src="https://velog.velcdn.com/images/mommers/post/c7f298ce-db91-4902-845d-ef8a1fd5ac27/image.png" /></p>
</li>
<li><p>ping 8.8.8.8
<img alt="" src="https://velog.velcdn.com/images/mommers/post/fcab9ada-0893-4036-a243-4daeefac8c81/image.png" /></p>
</li>
</ul>
<h3 id="결과"><strong>결과</strong></h3>
<p>현재 사용 중인 네트워크의 <strong>공인 IP (Public IP)</strong> 주소 하나만 딱 출력됨.</p>
<p>예시:</p>
<p><strong>Plaintext</strong></p>
<pre><code class="language-bash">210.123.45.67</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8b8ba332-7218-4f61-b635-0547395e74ba/image.png" /></p>
<h3 id="동작-원리"><strong>동작 원리</strong></h3>
<ol>
<li><strong>요청:</strong> 내 컴퓨터(<code>curl</code>)가 <code>ifconfig.me</code>라는 외부 웹사이트에 접속함.</li>
<li><strong>응답:</strong> 웹사이트가 &quot;너는 지금 <strong>이 주소(IP)</strong>를 달고 들어왔어&quot;라고 텍스트로 반송해줌.</li>
<li><strong>의미:</strong> 공유기 내부 주소(192.168...)가 아니라, <strong>전 세계 인터넷 망에서 식별되는 실제 우리 집(혹은 회사) 대문 주소</strong>임.</li>
</ol>
<h3 id="비교-혼동-주의"><strong>비교 (혼동 주의)</strong></h3>
<ul>
<li><strong><code>ifconfig</code> / <code>ip addr</code>:</strong> <strong>사설 IP</strong> (Private IP) 확인용. (공유기 안에서만 통하는 주소. 예: <code>192.168.0.50</code>).</li>
<li><strong><code>curl ifconfig.me</code>:</strong> <strong>공인 IP</strong> (Public IP) 확인용. (외부에서 내 서버로 접속할 때 필요한 주소).</li>
</ul>
<h3 id="꿀팁-대체-명령어"><strong>꿀팁 (대체 명령어)</strong></h3>
<p><code>ifconfig.me</code>가 느리거나 응답 없을 때 아래 것들도 많이 씀.</p>
<ul>
<li><code>curl icanhazip.com</code> (가장 빠르고 간결함)</li>
<li><code>curl ipinfo.io</code> (IP뿐만 아니라 통신사, 국가, 도시 정보까지 JSON으로 줌)</li>
</ul>
<hr />
<h2 id="curl">curl?</h2>
<hr />
<ul>
<li><em>CURL (Client URL)*</em>은 서버와 통신하며 데이터를 보내거나 가져오는 <strong>명령어 도구</strong>이자 <strong>라이브러리</strong>입니다. 임베디드나 백엔드 개발자에게는 <strong>&quot;망치&quot;</strong> 같은 필수 도구입니다.</li>
</ul>
<p>브라우저 없이 터미널에서 웹페이지 소스를 보거나, 파일을 다운로드하거나, API를 테스트할 때 씁니다.</p>
<hr />
<h3 id="자주-사용하는-것-5가지">자주 사용하는 것 5가지</h3>
<h4 id="①-웹페이지-내용-가져오기-get">① 웹페이지 내용 가져오기 (GET)</h4>
<p>그냥 주소만 치면 HTML 소스 코드를 화면에 뱉어냅니다.</p>
<p>Bash</p>
<pre><code class="language-bash">curl https://www.google.com</code></pre>
<h4 id="②-파일-다운로드-o--o">② 파일 다운로드 (<code>O</code> / <code>o</code>)</h4>
<p><strong>대문자 O</strong>를 가장 많이 씁니다. (원본 파일명 그대로 저장)</p>
<p>Bash</p>
<pre><code class="language-bash"># 원본 이름(firmware.bin)으로 저장
curl -O https://example.com/firmware.bin

# 내가 원하는 이름(new_fw.bin)으로 바꿔서 저장
curl -o new_fw.bin https://example.com/firmware.bin</code></pre>
<h4 id="③-api-테스트-데이터-보내기-d--post">③ API 테스트: 데이터 보내기 (<code>d</code> / POST)</h4>
<p>IoT 장비가 서버로 센서 데이터를 보낼 때 잘 되는지 테스트할 때 씁니다.</p>
<p>Bash</p>
<pre><code class="language-bash">curl -X POST -H &quot;Content-Type: application/json&quot; \
     -d '{&quot;temp&quot;: 25, &quot;humid&quot;: 60}' \
     http://my-api-server.com/sensor</code></pre>
<ul>
<li><strong><code>X POST</code></strong>: 보내는 방식 지정 (생략하면 <code>d</code> 있을 시 자동 POST).</li>
<li><strong><code>H</code></strong>: 헤더 설정 (JSON이라고 알려줌).</li>
<li><strong><code>d</code></strong>: 실제 보낼 데이터(Body).</li>
</ul>
<h4 id="④-서버가-죽었나-응답-헤더만-확인-i">④ &quot;서버가 죽었나?&quot; 응답 헤더만 확인 (<code>I</code>)</h4>
<p>내용(HTML)은 필요 없고, 서버가 살아있는지(200 OK)만 빠르게 볼 때.</p>
<p>Bash</p>
<pre><code class="language-bash">curl -I https://www.google.com
# 결과: HTTP/2 200 ...</code></pre>
<h4 id="⑤-리다이렉트-따라가기-l">⑤ 리다이렉트 따라가기 (<code>L</code>)</h4>
<p>사이트가 주소를 옮겼을 때(301, 302), <strong><code>-L</code></strong>이 없으면 &quot;Moved&quot; 메시지만 나오고 끝납니다. 최종 목적지까지 따라가려면 붙여야 합니다.</p>
<pre><code class="language-bash">curl -L http://google.com
# http -&gt; https로 자동 이동해서 결과 보여줌</code></pre>
<hr />
<h3 id="wget과-뭐가-다른가"><code>wget</code>과 뭐가 다른가?</h3>
<ul>
<li><strong><code>curl</code>:</strong> <strong>통신(Data Transfer)</strong>에 집중. API 테스트, 복잡한 업로드/다운로드, 라이브러리(<code>libcurl</code>)로 개발에 활용 가능.</li>
<li><strong><code>wget</code>:</strong> <strong>다운로드(Download)</strong>에 집중. 폴더째로 긁어오기(재귀 다운로드), 네트워크 끊기면 이어받기 등이 더 강력함.</li>
</ul>
<p><strong>한 줄 요약:</strong> 단순 파일 다운로드는 <code>wget</code>, <strong>API 테스트나 정교한 통신 디버깅은 <code>curl</code></strong>.</p>
<hr />
<h4 id="client_loop-send-disconnect-broken-pipe">client_loop: send disconnect: Broken pipe</h4>
<p><strong>SSH 접속이 끊어졌다</strong>는 뜻입니다.</p>
<p>가장 흔한 원인은 <strong>&quot;너무 오랫동안 아무것도 안 쳐서&quot;</strong> 중간에 있는 공유기나 방화벽이 연결을 끊어버린 것입니다. (Time out).</p>
<p>해결 방법은 <strong>&quot;내가 살아있다는 신호(Heartbeat)&quot;</strong>를 주기적으로 보내게 설정하는 것입니다.</p>
<hr />
<h3 id="1-클라이언트에서-설정하기">1. 클라이언트에서 설정하기</h3>
<p>내가 쓰는 PC(노트북)에서 설정을 한 번만 해두면, 어떤 서버(라즈베리 파이)에 접속하든 안 끊깁니다.</p>
<ol>
<li><p><strong>파일 열기 (내 PC 터미널에서):</strong>Bash</p>
<pre><code class="language-bash"> nano ~/.ssh/config</code></pre>
<p> <em>(파일이 없으면 빈 화면이 나옵니다.)</em></p>
</li>
<li><p><strong>내용 추가:</strong>Plaintext</p>
<pre><code class="language-bash"> Host *
     ServerAliveInterval 60
     ServerAliveCountMax 3</code></pre>
<ul>
<li><strong>의미:</strong> 60초마다 서버에 &quot;나 살아있어?&quot;라고 핑을 보냅니다. 이걸 설정하면 공유기가 연결을 안 끊습니다.</li>
</ul>
</li>
</ol>
<hr />
<h3 id="2-서버에서-설정하기-라즈베리-파이">2. 서버에서 설정하기 (라즈베리 파이)</h3>
<p>내 PC뿐만 아니라, 이 파이에 접속하는 <strong>모든 사람</strong>이 안 끊기게 하려면 서버 설정을 고칩니다.</p>
<ol>
<li><p><strong>파일 열기 (라즈베리 파이에서):</strong>Bash</p>
<pre><code class="language-bash"> sudo nano /etc/ssh/sshd_config</code></pre>
</li>
<li><p><strong>내용 수정/추가:</strong>Plaintext</p>
<pre><code class="language-bash"> ClientAliveInterval 60
 ClientAliveCountMax 3</code></pre>
</li>
<li><p><strong>재시작:</strong>Bash</p>
<pre><code class="language-bash"> sudo systemctl restart ssh</code></pre>
</li>
</ol>
<hr />
<h3 id="3-팁-tmux-사용">3. 팁: <code>tmux</code> 사용</h3>
<p>연결이 끊기면 <strong>컴파일하던 거나 코딩하던 게 다 날아가는 게</strong> 큰일입니다.</p>
<p>이걸 방지하기 위해 <strong><code>tmux</code></strong>나 <strong><code>screen</code></strong>을 사용하면 좋습니다.</p>
<ul>
<li><code>Broken pipe</code>로 접속이 끊겨도, 다시 로그인해서 <code>tmux attach</code>라고 치면 작업하던 화면이 그대로 복구되므로, 임베디드 개발 필수 툴이라고 합니다.</li>
</ul>