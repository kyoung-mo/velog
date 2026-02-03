<h3 id="시스템-콜-（system-call">시스템 콜 （System call</h3>
<p>사용자 공간(App)이 커널 공간(OS)의 기능을 빌려 쓰기 위한 '공식 요청 창구(API)'</p>
<p>리눅스는 '모든 것이 파일'이라는 철학에 따라, 하드웨어 제어(드라이버)도 파일 시스템 호출을 공유함</p>
<hr />
<h3 id="1-정의-및-역할">1. 정의 및 역할</h3>
<p>사용자 어플리케이션이 운영체제(커널)의 자원이나 서비스를 요청하기 위해 커널 모드로 진입하는 관문. <code>시스템 콜</code> = <code>커널 API</code> 라고도 부른다.(외부로 노출된 커널 함수).</p>
<ul>
<li>예시: 
<code>read()</code>, <code>write()</code>
<code>get_thread_area()</code>
<code>set_tid_address()</code></li>
</ul>
<hr />
<h3 id="2-아키텍처별-호출-방식-software-interrupt">2. 아키텍처별 호출 방식 (Software Interrupt)</h3>
<p>CPU 아키텍처마다 커널 모드로 전환(Context Switch)하기 위한 어셈블리 명령어가 다릅니다.</p>
<table>
<thead>
<tr>
<th><strong>아키텍처</strong></th>
<th><strong>호출 명령어 (Trigger)</strong></th>
<th><strong>비고</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>i386</strong> (32bit)</td>
<td><code>int 0x80</code></td>
<td>레거시 인터럽트 방식</td>
</tr>
<tr>
<td><strong>x86_64</strong> (64bit)</td>
<td><code>syscall</code></td>
<td>고속 시스템 콜 전용 명령어 (약 300여 개 존재)</td>
</tr>
<tr>
<td><strong>ARM / EABI</strong></td>
<td><code>swi 0x18</code></td>
<td>Software Interrupt (또는 <code>svc</code>)</td>
</tr>
</tbody></table>
<h3 id="3-동작-메커니즘-wrapper-routine">3. 동작 메커니즘 (Wrapper Routine)</h3>
<p>개발자가 어셈블리(<code>int 0x80</code> 등)를 직접 짜지 않아도 되는 이유는 <strong>C 라이브러리(glibc)</strong>가 감싸주고 있기 때문입니다.</p>
<ul>
<li><code>glibc</code> (GNU C Library) 내부에 존재</li>
<li>레지스터에 인자 값을 세팅하고 커널 진입 명령을 대신 실행함<ul>
<li>사용자 호출: <strong><code>open()</code></strong> (Wrapper Routine)</li>
<li>실제 커널 함수: <strong><code>sys_open</code></strong> (System Call Handler)</li>
</ul>
</li>
</ul>
<hr />
<h3 id="4-시스템-콜-분류-및-예시">4. 시스템 콜 분류 및 예시</h3>
<table>
<thead>
<tr>
<th><strong>관리 영역 (Subsystem)</strong></th>
<th><strong>역할</strong></th>
<th><strong>대표 시스템 콜</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>프로세스 관리</strong></td>
<td>프로세스 생성, 실행, 제어, 신호 처리</td>
<td><code>fork()</code>, <code>execve()</code>, <code>getpid()</code>, <code>signal()</code></td>
</tr>
<tr>
<td><strong>파일 시스템</strong></td>
<td>파일 열기, 읽기/쓰기, 닫기</td>
<td><code>open()</code>, <code>read()</code>, <code>write()</code>, <code>close()</code></td>
</tr>
<tr>
<td><strong>메모리 관리</strong></td>
<td>데이터 세그먼트 크기 변경 (힙 메모리 할당)</td>
<td><code>brk()</code>, <code>sbrk()</code></td>
</tr>
<tr>
<td><strong>네트워크</strong></td>
<td>소켓 통신 연결 및 데이터 전송</td>
<td><code>socket()</code>, <code>bind()</code>, <code>connect()</code>, <code>listen()</code>, <code>accept()</code></td>
</tr>
<tr>
<td><strong>디바이스 드라이버</strong></td>
<td><strong>독자적인 시스템 콜 없음</strong> (파일 시스템 콜을 빌려 씀)</td>
<td><code>open</code>, <code>read</code>, <code>write</code>, <strong><code>ioctl()</code></strong>(하드웨어 제어 핵심)</td>
</tr>
</tbody></table>
<hr />
<h4 id="디바이스-드라이버">디바이스 드라이버</h4>
<ul>
<li><strong>특징:</strong> 리눅스에서 하드웨어 장치는 <code>/dev/</code> 아래의 <strong>특수 파일(Device File)</strong>로 취급됩니다.</li>
<li><strong>동작:</strong> 따라서 별도의 드라이버 전용 함수 대신, <strong>파일 시스템용 시스템 콜(<code>open</code>, <code>read</code>, <code>write</code>)</strong>을 그대로 사용하여 하드웨어를 제어합니다.<ul>
<li>예: LED를 켜기 위해 <code>write()</code> 사용, 센서 설정을 바꾸기 위해 <code>ioctl()</code> 사용.</li>
</ul>
</li>
</ul>
<blockquote>
<p>하드웨어를 제어하는 소프트웨어를 디바이스 드라이버라고 한다.</p>
</blockquote>
<hr />
<h3 id="system-call--wrapper-함수와-system-call-handler">System call  wrapper 함수와 system call handler</h3>
<p><code>Wrapper(요청 준비)</code> → <code>Interrupt(커널 진입)</code> → <code>Handler(실제 수행)</code> → <code>Return(복귀)</code> 의 순환 과정</p>
<hr />
<h3 id="1-실행-흐름-4단계-step-by-step">1. 실행 흐름 4단계 (Step-by-Step)</h3>
<h4 id="①-사용자-모드-user-space">① 사용자 모드 (User Space)</h4>
<ul>
<li><strong>호출:</strong> 응용 프로그램이 <code>open()</code>, <code>read()</code> 등 표준 함수 호출</li>
<li><strong>Wrapper 루틴 (glibc):</strong><ul>
<li>CPU 레지스터에 인자 값과 <strong>시스템 콜 번호</strong>를 저장</li>
<li>커널 모드로 전환하기 위한 <strong>트랩(Trap) 명령어</strong> 실행</li>
</ul>
</li>
</ul>
<h4 id="②-모드-전환-context-switch">② 모드 전환 (Context Switch)</h4>
<ul>
<li><strong>진입 (Entry):</strong><ul>
<li><strong>Legacy (x86):</strong> <code>int 0x80</code> (소프트웨어 인터럽트)</li>
<li><strong>Modern (x86_64):</strong> <code>sysenter</code> 또는 <code>syscall</code> (고속 전용 명령)</li>
</ul>
</li>
<li>CPU가 사용자 모드에서 <strong>커널 모드(Privileged Mode)</strong>로 권한 상승</li>
</ul>
<h4 id="③-커널-모드-kernel-space">③ 커널 모드 (Kernel Space)</h4>
<ul>
<li><strong>System Call Handler:</strong><ul>
<li>인터럽트를 감지하고 레지스터에 저장된 <strong>번호(Table Index)</strong>를 확인</li>
</ul>
</li>
<li><strong>Service Routine:</strong><ul>
<li>실제 기능을 수행하는 커널 함수 실행 (예: <code>sys_open</code>, <code>sys_read</code>)</li>
</ul>
</li>
</ul>
<h4 id="④-복귀-return">④ 복귀 (Return)</h4>
<ul>
<li><strong>종료 (Exit):</strong><ul>
<li><strong>Legacy:</strong> <code>iret</code> (Interrupt Return)</li>
<li><strong>Modern:</strong> <code>sysexit</code> 또는 <code>sysret</code></li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/76302186-4c56-4c19-a95d-7f39db82ffd2/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/912758e8-cab5-4458-9942-814cab3a4674/image.png" /></p>
<p>swi : 소프트웨어 인터럽트</p>
<hr />
<h3 id="시스템-콜system-call-처리-과정arm">시스템 콜(System Call) 처리 과정–ARM</h3>
<p>레지스터에 '주문 번호(Syscall No)'를 넣고 <code>SVC</code> 명령을 실행하면, CPU가 익셉션 벡터(Exception Vector)로 점프하여 커널 모드로 진입</p>
<p>x86의 int 0x80이나 syscall과 원리는 같으나, 사용하는 명령어와 레지스터가 다릅니다.</p>
<p>x86의 <code>int 0x80</code>이나 <code>syscall</code>과 원리는 같으나, 사용하는 <strong>명령어</strong>와 <strong>레지스터</strong>가 다릅니다.</p>
<hr />
<h3 id="1-핵심-흐름-flow">1. 핵심 흐름 (Flow)</h3>
<ol>
<li><strong>준비 (User):</strong> <code>glibc</code> 래퍼가 레지스터에 인자값과 <strong>시스템 콜 번호</strong>를 저장</li>
<li><strong>발동 (Trigger):</strong> <strong><code>SVC</code> (Supervisor Call)</strong> 명령어 실행 (구 <code>SWI</code>)</li>
<li><strong>진입 (Exception):</strong> CPU가 <strong>User Mode → SVC Mode (또는 EL1)</strong>로 전환되고, <strong>익셉션 벡터 테이블</strong>의 SVC 핸들러 주소로 점프</li>
<li><strong>처리 (Kernel):</strong> 커널의 <code>vector_swi</code>(32bit) 또는 <code>el0_svc</code>(64bit) 루틴이 실행됨</li>
<li><strong>복귀 (Return):</strong> 결과값을 레지스터에 싣고 유저 모드로 복귀</li>
</ol>
<hr />
<h3 id="2-아키텍처별-레지스터-규칙-abi">2. 아키텍처별 레지스터 규칙 (ABI)</h3>
<p>개발자가 가장 신경 써야 할 <strong>&quot;데이터 전달 약속&quot;</strong>입니다.</p>
<table>
<thead>
<tr>
<th><strong>구분</strong></th>
<th><strong>ARM 32-bit (EABI)</strong></th>
<th><strong>ARM 64-bit (AArch64)</strong></th>
<th><strong>비고</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>명령어</strong></td>
<td><code>svc 0</code> (또는 <code>swi</code>)</td>
<td><code>svc 0</code></td>
<td>Supervisor Call</td>
</tr>
<tr>
<td><strong>시스템 콜 번호</strong></td>
<td><strong>R7</strong></td>
<td><strong>X8</strong></td>
<td>&quot;몇 번 함수 실행해줘?&quot;</td>
</tr>
<tr>
<td><strong>인자 (Args)</strong></td>
<td><strong>R0 ~ R6</strong></td>
<td><strong>X0 ~ X5</strong></td>
<td>함수 파라미터 전달</td>
</tr>
<tr>
<td><strong>결과값 (Return)</strong></td>
<td><strong>R0</strong></td>
<td><strong>X0</strong></td>
<td>실행 결과 (성공/에러)</td>
</tr>
<tr>
<td><strong>모드 전환</strong></td>
<td>User → SVC Mode</td>
<td>EL0 → EL1</td>
<td>Exception Level 상승</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-단계별-상세-처리-deep-dive">3. 단계별 상세 처리 (Deep Dive)</h3>
<h4 id="①-wrapper-routine-glibc">① Wrapper Routine (glibc)</h4>
<ul>
<li>사용자가 <code>open()</code> 호출.</li>
<li><code>glibc</code> 내부:<ul>
<li><code>R0</code> = 파일 경로 포인터</li>
<li><code>R1</code> = 플래그 (Read/Write)</li>
<li><strong><code>R7</code> = 5 (open의 시스템 콜 번호)</strong></li>
<li><strong><code>svc 0</code> 실행!</strong></li>
</ul>
</li>
</ul>
<h4 id="②-exception-vector-table-hw">② Exception Vector Table (H/W)</h4>
<ul>
<li><code>SVC</code> 명령을 만나면 CPU는 하드웨어적으로 정해진 주소(Vector Base Address + Offset)로 강제 점프함.</li>
<li>이곳에는 커널의 <strong>진입점(Entry Point)</strong> 코드가 있음.</li>
</ul>
<h4 id="③-dispatcher-kernel-sw">③ Dispatcher (Kernel S/W)</h4>
<ul>
<li>어셈블리 코드(<code>entry-common.S</code>)가 실행됨.</li>
<li><strong>Context Save:</strong> 현재 유저 모드의 레지스터 값들을 스택(Kernel Stack)에 백업.</li>
<li><strong>Table Lookup:</strong> <code>sys_call_table</code>에서 <code>R7</code>(또는 <code>X8</code>)에 해당하는 함수 주소를 찾음.</li>
<li><strong>Execution:</strong> <code>sys_open</code> 함수 실행.</li>
</ul>
<h4 id="④-return-path">④ Return Path</h4>
<ul>
<li><code>sys_open</code>이 파일 디스크립터(fd)를 반환.</li>
<li>커널은 이 값을 <code>R0</code>(또는 <code>X0</code>)에 저장.</li>
<li><strong>Context Restore:</strong> 스택에 백업해둔 유저 레지스터 복원.</li>
<li><code>movs pc, lr</code> (32bit) 또는 <code>eret</code> (64bit) 명령어로 유저 모드 복귀.</li>
</ul>