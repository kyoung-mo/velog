<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3183c8f0-6f79-4d7a-b1ea-1f334c527922/image.png" /></p>
<h3 id="리눅스에서-signal과-socket-통신-비교">리눅스에서 Signal과 Socket 통신 비교</h3>
<hr />
<h3 id="1-시그널--초인종-소켓--우편물">1. 시그널 = 초인종, 소켓 = 우편물</h3>
<p>Signal: 초인종 </p>
<ul>
<li>내용물은 없고 &quot;누군가 왔다(이벤트 발생)&quot;는 사실만 즉시 알리고 끝납니다.</li>
<li>받는 사람이 뭘 하고 있든 강제로 중단시키고 벨을 울립니다. (비동기)</li>
</ul>
<p>Socket: 우편함</p>
<ul>
<li>실제 편지(데이터)가 담겨 있습니다.</li>
<li>받는 사람이 시간 날 때 우편함을 열어봐야 합니다. (동기/비동기 선택 가능)</li>
</ul>
<h3 id="2-두-통신의-선택-기준deep-dive">2. 두 통신의 선택 기준(Deep Dive)</h3>
<table>
<thead>
<tr>
<th>비교 항목</th>
<th>Signal</th>
<th>Socket (Unix Domain)</th>
</tr>
</thead>
<tbody><tr>
<td>핵심 역할</td>
<td>제어 (Control) 및 인터럽트</td>
<td>데이터 전송 (Transport)</td>
</tr>
<tr>
<td>데이터 크기</td>
<td>없음 (또는 정수 하나)</td>
<td>제한 없음 (Byte Stream)</td>
</tr>
<tr>
<td>전달 보장</td>
<td>낮음 (표준 시그널은 중복 발생 시 하나로 뭉쳐짐 - Coalescing)</td>
<td>높음 (버퍼에 큐잉됨)</td>
</tr>
<tr>
<td>네트워크</td>
<td>불가능 (OS 커널 내 한정)</td>
<td>가능 (로컬 및 원격)</td>
</tr>
<tr>
<td>주 사용처</td>
<td>데몬 리로드(<code>SIGHUP</code>), 강제 종료(<code>SIGKILL</code>), 자식 관리(<code>SIGCHLD</code>)</td>
<td>로그 전송, DB 연결, 프로세스 간 데이터 파이프라인</td>
</tr>
</tbody></table>
<h3 id="3-signal을-사용하는-이유">3. Signal을 사용하는 이유</h3>
<ol>
<li>커널이 주는 유일한 알람:<ul>
<li>CPU 명령어가 0으로 나누기를 하거나(<code>SIGFPE</code>), 메모리를 잘못 건드렸을 때(<code>SIGSEGV</code>), 커널이 프로세스에게 알려주는 유일한 수단입니다. 소켓으로는 이 정보를 받을 수 없습니다.</li>
</ul>
</li>
<li>구현 비용 <code>0</code> :<ul>
<li>소켓을 쓰려면 <code>socket()</code>, <code>bind()</code>, <code>connect()</code>, <code>accept()</code> 등 코드가 길어집니다.</li>
<li>시그널은 <code>kill(pid, SIGUSR1)</code> 한 줄이면 끝납니다. 단순 트리거용으로는 가성비가 최고입니다.</li>
</ul>
</li>
<li>관리자 제어 표준:<ul>
<li>시스템 관리자나 스크립트가 외부에서 <code>kill</code> 명령어로 프로세스를 제어하는 표준 인터페이스입니다.</li>
</ul>
</li>
</ol>
<h3 id="4-시그널의-한계-senior-level">4. 시그널의 한계 (Senior Level)</h3>
<ol>
<li>정보 소실 (Coalescing)</li>
</ol>
<ul>
<li>프로세스가 바쁜 사이에 <code>SIGUSR1</code>이 100번 도착해도, 핸들러는 딱 1번만 실행될 수 있습니다. (표준 시그널은 큐에 쌓이지 않음).</li>
<li>반면 소켓은 데이터가 버퍼에 쌓이므로 소실되지 않습니다.</li>
</ul>
<ol start="2">
<li>비동기 처리의 위험성</li>
</ol>
<ul>
<li>핸들러 내부에서는 할 수 있는 일이 극히 제한적입니다. 
(예를 들어<code>printf</code>, <code>malloc</code> 사용 불가).</li>
</ul>