<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2d386549-f324-4bb5-9b05-429d24d4e5df/image.png" /></p>
<h3 id="ipc-inter-process-communication-및-프로세스-주소-공간-요약">IPC (Inter-Process Communication) 및 프로세스 주소 공간 요약</h3>
<p>프로세스는 독립된 가상 주소 공간(Virtual Address Space)을 가지므로, 서로의 메모리에 직접 접근할 수 없습니다. 따라서 프로세스 간 협력을 위해 커널이 중재하는 IPC 메커니즘이 필수적입니다.</p>
<hr />
<h3 id="1-데이터-전송-data-transfer-모델">1. 데이터 전송 (Data Transfer) 모델</h3>
<p>커널 메모리를 매개체로 데이터를 복사하여 전달하는 방식입니다.</p>
<ul>
<li><code>Write</code> : 송신 프로세스가 사용자 메모리 데이터를 커널 메모리로 복사합니다.</li>
<li><code>Read</code> : 수신 프로세스가 커널 메모리 데이터를 자신의 사용자 메모리로 복사합니다.</li>
</ul>
<h4 id="1-1-바이트-스트림-byte-stream">1-1) 바이트 스트림 (Byte Stream):</h4>
<ul>
<li>구분자 없는 데이터의 흐름 (파이프, FIFO, 스트림 소켓).</li>
<li>쓰기 크기와 읽기 크기가 일치하지 않아도 되며, 임의의 바이트 단위로 읽기 가능.</li>
</ul>
<h4 id="1-2-메시지-message">1-2) 메시지 (Message):</h4>
<ul>
<li>경계가 분명한 메시지 단위 (System V/POSIX 메시지 큐, 데이터그램 소켓).</li>
<li>한 번의 읽기 작업으로 하나의 전체 메시지를 소비함.</li>
<li>파괴적 읽기: 데이터를 읽으면 커널 내에서 해당 데이터는 소멸됨.</li>
<li>자동 동기화: 데이터가 없으면 읽기 작업은 기본적으로 Blocking 되어 동기화가 유지됨.</li>
</ul>
<hr />
<h3 id="2-공유-메모리-shared-memory-모델">2. 공유 메모리 (Shared Memory) 모델</h3>
<p>두 개 이상의 프로세스가 동일한 물리 메모리 영역을 자신의 주소 공간에 매핑하여 사용하는 방식입니다.</p>
<ul>
<li>구현 방식:<ul>
<li>System V 공유 메모리</li>
<li>POSIX 공유 메모리</li>
<li>메모리 매핑 (<code>mmap</code>)</li>
</ul>
</li>
<li>고속 통신: 커널을 거치지 않고 직접 메모리에 접근하므로 데이터 복사 오버헤드가 없음.</li>
<li>비파괴적 읽기: 데이터를 읽어도 메모리에 잔류하여 다른 프로세스가 재사용 가능.</li>
<li>수동 동기화: 커널이 동기화를 보장하지 않음. 데이터 일관성을 위해 세마포어(Semaphore)나 뮤텍스 등의 별도 메커니즘 필요.</li>
</ul>
<hr />
<h3 id="3-비교-요약">3. 비교 요약</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>데이터 전송 (Data Transfer)</th>
<th>공유 메모리 (Shared Memory)</th>
</tr>
</thead>
<tbody><tr>
<td>속도</td>
<td>상대적으로 느림 (Context Switch/Copy 발생)</td>
<td>매우 빠름 (직접 접근)</td>
</tr>
<tr>
<td>복사 횟수</td>
<td>2회 (User → Kernel → User)</td>
<td>0회 (초기 매핑 후 없음)</td>
</tr>
<tr>
<td>동기화</td>
<td>커널이 자동 제공 (Blocking)</td>
<td>개발자가 직접 구현 (Semaphore 등)</td>
</tr>
<tr>
<td>데이터 유지</td>
<td>읽기 후 삭제 (소비성)</td>
<td>명시적 삭제 전까지 유지 (공유성)</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
</tr>
</tbody></table>