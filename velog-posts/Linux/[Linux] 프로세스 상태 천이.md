<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d4805aa1-e35a-4762-9a42-4d72aec293f0/image.png" /></p>
<hr />
<h3 id="프로세스-상태-천이">프로세스 상태 천이</h3>
<p>프로세스는 CPU를 쓰다가(Running), 쉬다가(Sleeping), 멈추고(Stopped), 결국 죽어서(Zombie) 사라진다.</p>
<p>리눅스 커널은 프로세스 상태를 <code>task_struct</code> 내의 <code>state</code> 필드로 관리합니다.</p>
<hr />
<h3 id="1-주요-상태-process-states">1. 주요 상태 (Process States)</h3>
<p><code>ps</code>나 <code>top</code> 명령의 STAT 컬럼에서 볼 수 있는 문자입니다.</p>
<table>
<thead>
<tr>
<th>상태 코드</th>
<th>커널 상수명</th>
<th>설명</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td>R</td>
<td><code>TASK_RUNNING</code></td>
<td>실행 중 또는 실행 대기(Ready)</td>
<td>CPU를 점유 중이거나, 런큐(RunQueue)에서 줄 서 있는 상태.</td>
</tr>
<tr>
<td>S</td>
<td><code>TASK_INTERRUPTIBLE</code></td>
<td>대기 (Sleep)</td>
<td>이벤트(키보드, 소켓 등) 대기. 시그널이 오면 깨어남.</td>
</tr>
<tr>
<td>D</td>
<td><code>TASK_UNINTERRUPTIBLE</code></td>
<td>특수 대기 (Deep Sleep)</td>
<td>디스크 I/O 등 하드웨어 대기. 강제 종료(<code>kill -9</code>) 불가.</td>
</tr>
<tr>
<td>T</td>
<td><code>TASK_STOPPED</code></td>
<td>정지</td>
<td><code>Ctrl+Z</code>나 디버거에 의해 멈춤. <code>SIGCONT</code>로 재개 가능.</td>
</tr>
<tr>
<td>Z</td>
<td><code>EXIT_ZOMBIE</code></td>
<td>좀비</td>
<td>종료(<code>exit</code>)했으나 부모가 확인(<code>wait</code>) 안 함. 껍데기만 남음.</td>
</tr>
<tr>
<td>X</td>
<td><code>EXIT_DEAD</code></td>
<td>사망</td>
<td>부모가 확인 완료. 완전히 메모리에서 삭제됨. (거의 안 보임).</td>
</tr>
</tbody></table>
<h3 id="2-상태-천이-과정-lifecycle-flow">2. 상태 천이 과정 (Lifecycle Flow)</h3>
<ol>
<li>생성 (<code>fork</code>): 프로세스 탄생 → <code>R</code> (Ready) 상태로 런큐 진입.</li>
<li>디스패치 (Schedule): 스케줄러가 선택 → <code>R</code> (Running) CPU 점유.</li>
<li>시스템 콜 (<code>sleep</code>/<code>read</code>): I/O 요청 등으로 대기 필요 → <code>S</code> 또는 <code>D</code>로 이동 (CPU 반납).</li>
<li>깨어남 (Wake Up): I/O 완료 인터럽트 발생 → 다시 <code>R</code> (Ready)로 이동.</li>
<li>선점 (Preemption): 타임 슬라이스(할당 시간) 종료 → 강제로 <code>R</code> (Ready)로 밀려남.</li>
<li>종료 (<code>exit</code>): 할 일 다 함 → <code>Z</code> (Zombie) 상태가 되어 부모 기다림.</li>
</ol>
<h3 id="3-상태-확인-예제">3. 상태 확인 예제</h3>
<p>Bash</p>
<pre><code class="language-bash"># STAT 열 확인
$ ps -eo pid,stat,comm
  PID STAT COMMAND
 1234 R+   my_program   (Running, Foreground)
 5678 Ss   bash         (Sleeping, Session Leader)
 9999 Z    defunct      (Zombie - 죽여도 안 죽는 상태)</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2361d21d-f036-4378-bebc-b86682ab27f5/image.png" /></p>