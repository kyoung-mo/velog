<h3 id="소프트웨어-계층-구조-hierarchy">소프트웨어 계층 구조 (Hierarchy)</h3>
<p>리눅스 시스템은 <strong>하드웨어 제어(Low-level)</strong>에서 <strong>사용자 경험(High-level)</strong>으로 이어지는 계층 구조를 가집니다.</p>
<table>
<thead>
<tr>
<th><strong>영역 (Level)</strong></th>
<th><strong>구성 요소</strong></th>
<th><strong>주요 특징</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>User Space</strong></td>
<td><strong>Application</strong></td>
<td>고수준 라이브러리 활용 (GUI, 비즈니스 로직)</td>
</tr>
<tr>
<td><strong>User Space</strong></td>
<td><strong>System Software</strong></td>
<td>커널/핵심 라이브러리와 직접 인터페이스 (쉘, 컴파일러, 서버)</td>
</tr>
<tr>
<td><strong>Kernel Space</strong></td>
<td><strong>Kernel / Driver</strong></td>
<td>하드웨어 직접 제어, 리소스 관리, 시스템 호출 처리</td>
</tr>
<tr>
<td><strong>Hardware</strong></td>
<td><strong>Device</strong></td>
<td>CPU, Memory, Disk, Network Interface 등</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/89380104-5405-4868-ad96-2cc4e7ec8abc/image.png" /></p>
<hr />
<h3 id="1-커널의-핵심-역할">1. 커널의 핵심 역할</h3>
<ul>
<li>운영체제(OS)의 <strong>심장(Core)</strong>이자 <strong>관리자(Supervisor)</strong>.<ul>
<li>하드웨어 직접 제어 및 시스템 자원 분배.</li>
<li>상위 계층(응용 프로그램)에 기본적인 시스템 서비스 제공.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="2-자원-관리와-추상화-resource-abstraction">2. 자원 관리와 추상화 (Resource Abstraction)</h3>
<p>커널은 물리적 하드웨어를 소프트웨어가 쓰기 편한 <strong>논리적(추상적) 개념</strong>으로 변환하여 제공합니다.</p>
<table>
<thead>
<tr>
<th><strong>물리적 자원 (Hardware)</strong></th>
<th><strong>추상적 자원 (Logical View)</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>CPU</strong></td>
<td>태스크(Task), 스레드(Thread)</td>
</tr>
<tr>
<td><strong>메모리 (RAM)</strong></td>
<td>세그먼트(Segment), 페이지(Page)</td>
</tr>
<tr>
<td><strong>디스크 (Disk)</strong></td>
<td>파일(File), inode</td>
</tr>
<tr>
<td><strong>네트워크 (NIC)</strong></td>
<td>프로토콜(Protocol), 패킷(Packet)</td>
</tr>
</tbody></table>
<hr />
<h3 id="3-커널의-5대-세부-기능-subsystems">3. 커널의 5대 세부 기능 (Subsystems)</h3>
<h4 id="①-프로세스-관리-process-management">① 프로세스 관리 (Process Management)</h4>
<ul>
<li><strong>생명주기:</strong> 프로세스 생성(<code>fork</code>), 실행, 소멸(<code>exit</code>) 관리.</li>
<li><strong>스케줄링:</strong> 여러 프로세스에 CPU 시간을 공평/효율적으로 분배 (Context Switching).</li>
<li><strong>통신:</strong> 프로세스 간 데이터 교환 (<strong>IPC</strong>: Signal, Pipe, Socket 등).</li>
</ul>
<h4 id="②-메모리-관리-memory-management">② 메모리 관리 (Memory Management)</h4>
<ul>
<li><strong>가상 메모리:</strong> 물리 메모리보다 큰 프로그램을 실행하기 위한 추상화.</li>
<li><strong>하드웨어 제어:</strong> 페이징(Paging), 스와핑(Swapping), 메모리 보호.</li>
</ul>
<h4 id="③-파일-시스템-관리-file-system-management">③ 파일 시스템 관리 (File System Management)</h4>
<ul>
<li><strong>VFS (Virtual File System):</strong> <code>ext4</code>, <code>ntfs</code>, <code>fat</code> 등 서로 다른 파일 시스템을 동일한 API(<code>open</code>, <code>read</code>)로 접근 가능하게 함.</li>
<li><strong>매핑:</strong> 디스크의 물리적 섹터를 논리적인 '파일'과 '디렉터리' 구조로 변환.</li>
</ul>
<h4 id="④-장치-관리-device-management">④ 장치 관리 (Device Management)</h4>
<ul>
<li><strong>I/O 스케줄링:</strong> 디스크 입출력 순서를 최적화하여 성능 향상.</li>
<li><strong>인터럽트 처리:</strong> 하드웨어 신호(키보드 입력, 패킷 수신 등)를 감지하고 처리 루틴 실행.</li>
<li><strong>데이터 전송:</strong> DMA 등을 통해 주변장치와 메모리 간 고속 데이터 이동.</li>
</ul>
<h4 id="⑤-네트워크-관리-network-management">⑤ 네트워크 관리 (Network Management)</h4>
<ul>
<li><strong>프로토콜 스택:</strong> TCP/IP 등 통신 규약 구현.</li>
<li><strong>패킷 처리:</strong> 라우팅(경로 설정), 주소 지정(IP Addressing), 패킷 필터링.</li>
</ul>
<hr />
<h3 id="4-시스템-콜system-call-처리-과정arm">4. 시스템 콜(System Call) 처리 과정–ARM</h3>
<p>&quot;레지스터에 '주문 번호(Syscall No)'를 넣고 <code>SVC</code> 명령을 실행하면, CPU가 익셉션 벡터(Exception Vector)로 점프하여 커널 모드로 진입.&quot;</p>
<p>x86의 int 0x80이나 syscall과 원리는 같으나, 사용하는 명령어와 레지스터가 다릅니다.</p>
<p>x86의 <code>int 0x80</code>이나 <code>syscall</code>과 원리는 같으나, 사용하는 <strong>명령어</strong>와 <strong>레지스터</strong>가 다릅니다.</p>
<h3 id="4-1-핵심-흐름-flow">4-1) 핵심 흐름 (Flow)</h3>
<ol>
<li><strong>준비 (User):</strong> <code>glibc</code> 래퍼가 레지스터에 인자값과 <strong>시스템 콜 번호</strong>를 저장.</li>
<li><strong>발동 (Trigger):</strong> <strong><code>SVC</code> (Supervisor Call)</strong> 명령어 실행 (구 <code>SWI</code>).</li>
<li><strong>진입 (Exception):</strong> CPU가 <strong>User Mode → SVC Mode (또는 EL1)</strong>로 전환되고, <strong>익셉션 벡터 테이블</strong>의 SVC 핸들러 주소로 점프.</li>
<li><strong>처리 (Kernel):</strong> 커널의 <code>vector_swi</code>(32bit) 또는 <code>el0_svc</code>(64bit) 루틴이 실행됨.</li>
<li><strong>복귀 (Return):</strong> 결과값을 레지스터에 싣고 유저 모드로 복귀.</li>
</ol>
<h3 id="4-2-아키텍처별-레지스터-규칙-abi">4-2) 아키텍처별 레지스터 규칙 (ABI)</h3>
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
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody></table>
<h3 id="4-3-단계별-상세-처리-deep-dive">4-3) 단계별 상세 처리 (Deep Dive)</h3>
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