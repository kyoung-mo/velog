<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b1cb3505-e8e2-4bd4-8e6e-99bdf410c207/image.png" /></p>
<hr />
<h3 id="포트-확인-netstat-ss">포트 확인 (netstat, ss)</h3>
<ul>
<li>어떤 프로그램이 통신 중인가? Listening 포트 개념에 대해 확인</li>
<li><code>sudo ss -tulpn</code> (또는 <code>netstat</code>)으로 현재 열려있는 포트 확인</li>
<li>SSH(22번), Web(80번) 5900포트가 열려있는지 확인</li>
<li>특정 포트를 사용 중인 프로세스 이름 알아내기</li>
</ul>
<hr />
<h3 id="ss-vs-netstat">SS vs netstat</h3>
<hr />
<p><code>netstat</code>에 비해 <code>ss</code>가 더 빠르고 강력한 최신 표준(Modern Standard)이라고 합니다.</p>
<p>대부분 라즈베리 파이 최신 OS를 포함한 대부분의 배포판에서 <code>netstat</code>은 Deprecated(사용 중단 예정) 상태이며, <code>ss</code>가 기본입니다.</p>
<h3 id="1-기술적-차이점">1. 기술적 차이점</h3>
<table>
<thead>
<tr>
<th><strong>특징</strong></th>
<th><strong>netstat (구형)</strong></th>
<th><strong>ss (신형)</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>소속 패키지</strong></td>
<td><code>net-tools</code> (더 이상 업데이트 안 됨)</td>
<td><code>iproute2</code> (현재 리눅스 표준)</td>
</tr>
<tr>
<td><strong>데이터 출처</strong></td>
<td><strong><code>/proc</code> 파일 시스템</strong> 읽기</td>
<td><strong>Netlink API</strong> (커널 직접 통신)</td>
</tr>
<tr>
<td><strong>속도</strong></td>
<td>연결이 많으면 <strong>엄청 느려짐</strong> (텍스트 파싱)</td>
<td>연결이 수만 개여도 <strong>빠름</strong> (바이너리 통신)</td>
</tr>
<tr>
<td><strong>정보량</strong></td>
<td>기본적인 TCP/IP 정보</td>
<td>TCP 타이머, 큐(Queue) 상태, 메모리 사용량 등 상세 정보</td>
</tr>
</tbody></table>
<ul>
<li><strong>왜 <code>ss</code>인가?</strong></li>
</ul>
<p><code>netstat</code>은 <code>/proc/net/tcp</code> 같은 텍스트 파일을 열어서 한 줄씩 읽습니다. 연결이 많으면 이 파일을 만드는 커널도 힘들고, 읽는 <code>netstat</code>도 힘듭니다.</p>
<p>반면 <code>ss</code>는 커널 내부의 소켓 정보를 <strong>Netlink</strong>라는 고속 인터페이스로 직접 긁어옵니다.</p>
<hr />
<h3 id="2-명령어-비교">2. 명령어 비교</h3>
<p><code>netstat</code> 과 <code>ss</code> 의 옵션이 거의 똑같기 때문에 <code>netstat</code> 자리에 <code>ss</code> 만 넣으면 대부분은 호환됩니다.</p>
<hr />
<h3 id="모든-포트-확인-가장-많이-씀">모든 포트 확인 (가장 많이 씀)</h3>
<ul>
<li><strong>netstat:</strong> <code>netstat -antp</code></li>
<li><strong>ss:</strong> <strong><code>ss -antp</code></strong><ul>
<li><code>a</code>: All (전체)</li>
<li><code>n</code>: Numeric (이름 말고 숫자로 포트 표시)</li>
<li><code>t</code>: TCP만</li>
<li><code>p</code>: Process (어떤 프로그램이 쓰는지 표시 - <strong>sudo 필요</strong>)</li>
</ul>
</li>
</ul>
<h3 id="리슨-중인열린-포트만-보기-서버-점검용">리슨 중인(열린) 포트만 보기 (서버 점검용)</h3>
<ul>
<li><strong>netstat:</strong> <code>netstat -lntp</code></li>
<li><strong>ss:</strong> <strong><code>ss -lntp</code></strong><ul>
<li><code>l</code>: Listening (열려있는 포트만)</li>
</ul>
</li>
</ul>
<h3 id="메모리-사용량까지-보기-ss만의-장점">메모리 사용량까지 보기 (ss만의 장점)</h3>
<ul>
<li><strong>ss:</strong> <code>ss -amtp</code><ul>
<li><code>m</code>: 소켓이 사용하는 메모리 양을 보여줍니다. (메모리 누수 잡을 때 유용).</li>
</ul>
</li>
</ul>
<hr />
<h3 id="3-ss만의-강력한-필터링-기능">3. <code>ss</code>만의 강력한 필터링 기능</h3>
<p><code>grep</code>을 안 써도 자체 필터링이 가능하다고 합니다.</p>
<hr />
<pre><code class="language-bash"># 목적지 포트가 22번(SSH)인 것만 보여줘
ss -at '( dport = :22 )'

# 상태가 ESTABLISHED(연결됨)인 것만 보여줘
ss -t state established</code></pre>
<h3 id="결론">결론</h3>
<ul>
<li><strong>라즈베리 파이에서:</strong> <code>netstat</code> 명령어가 없어서 당황할 수 있지만, <code>sudo apt install net-tools</code> 를 통해 설치할 수 있습니다.</li>
<li><code>netstat</code> 대신 <code>ss</code>에 익숙해지는게 좋다고 합니다.</li>
</ul>