<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ff249d97-ce46-455c-919a-02270208c1bb/image.png" /></p>
<h2 id="j1c란">J1C란?</h2>
<p>소켓 프로그래밍을 개발하다 보면 서버 또는 클라이언트 중 한쪽이 아직 구현되지 않은 상황이 자주 발생합니다.
이럴 때 직접 서버/클라이언트를 따로 구현하지 않고도 통신을 테스트할 수 있는 도구가 <strong>J1 Communication(J1C)</strong> 입니다.</p>
<blockquote>
<p><strong>J1C 다운로드</strong>: <a href="http://www.j1lab.com">http://www.j1lab.com</a></p>
</blockquote>
<hr />
<h2 id="주요-특징">주요 특징</h2>
<ul>
<li>TCP 서버 / 클라이언트 모드 지원</li>
<li>송수신 데이터 실시간 확인</li>
<li>HEX 모드 지원 (16진수 송수신 확인)</li>
<li>별도 코딩 없이 즉시 사용 가능</li>
</ul>
<hr />
<h2 id="기본-사용법">기본 사용법</h2>
<h3 id="서버-설정">서버 설정</h3>
<p>서버 측은 <strong>포트 번호만</strong> 설정하면 됩니다.</p>
<ol>
<li>TCP Option → Port에 포트 번호 입력 (예: <code>5000</code>)</li>
<li><code>Server</code> 라디오 버튼 선택</li>
<li><code>Connect</code> 클릭 → 상태바에 <code>TCP : Listening</code> 표시</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/766108c1-c2dd-4243-a599-bafb88f10439/image.png" /></p>
<hr />
<h3 id="클라이언트-설정">클라이언트 설정</h3>
<p>클라이언트 측은 서버 IP와 포트를 입력합니다.</p>
<ol>
<li>TCP Option → IP에 서버 IP 입력 (로컬 테스트 시 <code>127.0.0.1</code>)</li>
<li>Port에 서버와 동일한 포트 입력 (예: <code>5000</code>)</li>
<li><code>Client</code> 라디오 버튼 선택</li>
<li><code>Connect</code> 클릭 → 상태바에 <code>TCP : Connect</code> 표시</li>
</ol>
<hr />
<h3 id="데이터-송수신">데이터 송수신</h3>
<p>연결이 완료되면 하단 <code>Edit Data(Send Data)</code> 필드에 전송할 내용을 입력하고 <code>Send</code>를 클릭합니다.</p>
<p><strong>Communication Data 영역 색상 규칙:</strong></p>
<table>
<thead>
<tr>
<th>색상</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>🔵 파란색</td>
<td>내가 보낸 데이터 (Send)</td>
</tr>
<tr>
<td>🔴 빨간색</td>
<td>내가 받은 데이터 (Recv)</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/39e20279-9f71-43a6-98b2-21e571d8cadc/image.png" /></p>
<hr />
<h2 id="hex-모드">HEX 모드</h2>
<p>서버 측에서 <code>Show HEX</code>를 체크하면 클라이언트에서 수신된 데이터를 <strong>16진수</strong>로 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1100f1bf-aa58-4e5b-88fa-4e5da47e4420/image.png" /></p>
<p>예를 들어 클라이언트에서 <code>68 69</code>를 전송하면 서버에서는 아래와 같이 표시됩니다.</p>
<pre><code>0003 - R ( 09:29:29'888 ) : 68 69 00 00 00 00 00 00 ...</code></pre><p>이를 통해 실제 바이트 단위로 어떤 데이터가 오가는지 확인할 수 있어 디버깅에 유용합니다.</p>
<hr />
<h2 id="활용-예시">활용 예시</h2>
<p>저번 실습때 사용했던 <code>iot_server</code> 를 이용하여 접속해봤습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6548405f-ebe7-494f-89ac-e4139fcaddb5/image.png" /></p>
<p>Qt 소켓 프로그래밍 개발 시 아래와 같이 활용할 수 있습니다.</p>
<pre><code>[J1C - Server]  ←→  [내가 개발 중인 Qt Client]
[내가 개발 중인 Qt Server]  ←→  [J1C - Client]</code></pre><p>서버와 클라이언트를 각각 J1C로 띄워 <strong>PC 내부에서 루프백(127.0.0.1) 테스트</strong>도 가능합니다.</p>
<hr />
<h2 id="send-crlf">Send CR/LF</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b422f26f-d103-4bab-836a-fcb79eef3cf6/image.png" /></p>
<p>CR/LF는 줄바꿈 문자입니다.</p>
<table>
<thead>
<tr>
<th>문자</th>
<th>표기</th>
<th>16진수</th>
</tr>
</thead>
<tbody><tr>
<td>CR</td>
<td>Carriage Return (<code>\r</code>)</td>
<td>0x0D</td>
</tr>
<tr>
<td>LF</td>
<td>Line Feed (<code>\n</code>)</td>
<td>0x0A</td>
</tr>
</tbody></table>
<p><code>Send CR, LF</code>를 체크하면 데이터를 전송할 때 문자열 끝에 <code>\r\n</code>을 자동으로 붙여서 보냅니다.</p>
<p>서버 쪽에서 메시지 끝을 <code>\r\n</code>으로 구분하는 경우, 체크하지 않으면 <code>strcmp</code> 등의 문자열 비교 함수에서 정상적으로 파싱되지 않을 수 있습니다.</p>
<pre><code class="language-c">// \r\n이 포함된 경우 strcmp 실패 예시
strcmp(buf, &quot;HELLO&quot;)   // → 불일치 (\r\n이 붙어있기 때문)
strcmp(buf, &quot;HELLO\r\n&quot;) // → 일치</code></pre>
<p>서버 파싱 방식에 맞게 체크 여부를 결정해야 합니다.</p>
<hr />
<h2 id="정리">정리</h2>
<p>J1C는 소켓 통신 개발 시 상대방 구현체 없이도 빠르게 송수신을 검증할 수 있는 가벼운 테스트 툴입니다.
HEX 모드까지 지원하기 때문에 바이트 단위 디버깅이 필요한 임베디드/IoT 환경에서도 유용하게 사용할 수 있습니다.</p>