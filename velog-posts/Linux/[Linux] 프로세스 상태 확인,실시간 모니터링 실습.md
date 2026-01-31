<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d13c2d59-6942-4785-860a-41e1a667e7ee/image.png" /></p>
<hr />
<h3 id="프로세스-상태-확인-ps-pstree">프로세스 상태 확인 (ps, pstree)</h3>
<ul>
<li><strong>학습:</strong> PID, PPID 개념. 데몬(Daemon) 이해.</li>
<li><strong>실습:</strong><ul>
<li><code>ps aux</code>로 전체 프로세스 확인.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/f7f5beb5-a70e-4cb5-96de-f5f608f2f36c/image.png" /></li>
<li><code>ps -ef | grep python</code>으로 특정 프로그램 실행 여부 확인.</li>
<li><code>pstree</code>로 부모-자식 프로세스 관계 시각적으로 확인.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/22eef2d4-8ee6-4bd0-9d57-91bded92cccf/image.png" /></li>
</ul>
</li>
</ul>
<hr />
<h3 id="실시간-리소스-모니터링-top-htop">실시간 리소스 모니터링 (top, htop)</h3>
<ul>
<li><strong>학습:</strong> CPU, 메모리 점유율 분석. Load Average 의미.</li>
<li><strong>실습:</strong><ul>
<li><code>top</code> 실행 후 메모리 순(<code>M</code>), CPU 순(<code>P</code>) 정렬 변경.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="htop-설치-및-실행-색상-마우스-지원-확인">htop 설치 및 실행 (색상, 마우스 지원 확인)</h3>
<p><code>htop</code> 상단(Header)에 있는 정보와 메인 리스트에서의 구분법을 명쾌하게 정리함.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d13c2d59-6942-4785-860a-41e1a667e7ee/image.png" /></p>
<h4 id="1-상단-요약-정보-header-의미">1. 상단 요약 정보 (Header) 의미</h4>
<p>좌측 상단 <code>Tasks: ...</code> 줄에 나오는 숫자들의 뜻.</p>
<ul>
<li><strong>Tasks (프로세스):</strong><ul>
<li>현재 시스템에 존재하는 <strong>프로세스(Process)의 총 개수</strong>.</li>
<li>정확히는 '스레드 리더(Main Thread)'들의 합.</li>
</ul>
</li>
<li><strong>thr (User Threads):</strong><ul>
<li><em>사용자 영역(User Space)*</em>에서 생성된 스레드 개수.</li>
<li>예: 크롬 탭 하나가 여러 개의 스레드를 씀. 부모 프로세스의 메모리를 공유하는 가벼운 일꾼들.</li>
</ul>
</li>
<li><strong>kthr (Kernel Threads):</strong><ul>
<li><em>커널 영역(Kernel Space)*</em>에서 생성된 스레드 개수.</li>
<li>하드웨어 제어, 파일 시스템 관리 등 OS가 직접 굴리는 백그라운드 일꾼들.</li>
</ul>
</li>
</ul>
<hr />
<h4 id="2-프로세스-리스트에서-3가지-구분하는-법">2. 프로세스 리스트에서 3가지 구분하는 법</h4>
<p>메인 화면(리스트)에서 눈으로 딱 보고 구별하는 포인트임.</p>
<h4 id="a-일반-프로세스-process--tasks">A. 일반 프로세스 (Process / Tasks)</h4>
<ul>
<li><strong>모양:</strong> 일반적인 프로그램 이름 (예: <code>python</code>, <code>bash</code>, <code>sshd</code>).</li>
<li><strong>특징:</strong> <strong>PID</strong>를 가지고 독립적인 메모리 공간을 차지함.</li>
<li><strong>색상:</strong> (테마 기본값 기준) 흰색 혹은 회색 텍스트.</li>
</ul>
<h4 id="b-사용자-스레드-thr">B. 사용자 스레드 (thr)</h4>
<ul>
<li><strong>모양:</strong> 프로세스 이름과 같거나 비슷함.</li>
<li><strong>구분법:</strong><ol>
<li><strong>트리 뷰(F5):</strong> 부모 프로세스 아래에 <strong>가지(└─)</strong> 모양으로 매달려 있음.</li>
<li><strong>색상:</strong> 설정(F2)에서 &quot;Highlight program path&quot;가 켜져 있다면, 스레드는 보통 <strong>초록색</strong>으로 표시됨.</li>
<li><strong>토글 단축키:</strong> *<em><code>Shift + H</code></em>를 누르면 숨겼다 보였다 함. (이걸로 확인하는 게 제일 확실함).</li>
</ol>
</li>
</ul>
<h4 id="c-커널-스레드-kthr">C. 커널 스레드 (kthr)</h4>
<ul>
<li><strong>모양:</strong> 이름이 무조건 <strong>대괄호 <code>[ ]</code></strong> 로 감싸져 있음.<ul>
<li>예: <code>[kworker/u...]</code>, <code>[ksoftirqd/0]</code>, <code>[jbd2/sda1...]</code></li>
</ul>
</li>
<li><strong>특징:</strong><ul>
<li>사용자 메모리(RES)를 거의 먹지 않음.</li>
<li>절대 죽이면 안 됨 (OS 멈춤).</li>
</ul>
</li>
<li><strong>토글 단축키:</strong> *<em><code>Shift + K</code></em>를 누르면 숨겼다 보였다 함.</li>
</ul>
<table>
<thead>
<tr>
<th><strong>종류</strong></th>
<th><strong>표시 예시</strong></th>
<th><strong>단축키(숨김/표시)</strong></th>
<th><strong>위치</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>Process</strong></td>
<td><code>python3 app.py</code></td>
<td>-</td>
<td>User Space</td>
</tr>
<tr>
<td><strong>Thread</strong></td>
<td><code>└─ python3 app.py</code> (초록색)</td>
<td><strong>Shift + H</strong></td>
<td>User Space</td>
</tr>
<tr>
<td><strong>K-Thread</strong></td>
<td><strong><code>[kworker/0:1]</code></strong> (대괄호)</td>
<td><strong>Shift + K</strong></td>
<td>Kernel Space</td>
</tr>
</tbody></table>
<hr />
<h3 id="htop-상단-바-설명">htop 상단 바 설명</h3>
<p><code>htop</code> 상단 헤더는 프로세스의 <strong>신분증</strong>이자 <strong>건강검진표</strong>임. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4bff783a-eebf-448b-9143-433627f43703/image.png" /></p>
<h4 id="1-기본-신원-identity">1. 기본 신원 (Identity)</h4>
<ul>
<li><strong>PID (Process ID):</strong> 프로세스 주민등록번호. <code>kill</code> 명령어로 죽일 때 이 번호가 필요함.</li>
<li><strong>USER:</strong> 프로세스의 주인 (실행시킨 계정).</li>
</ul>
<h4 id="2-우선순위-priority---중요">2. 우선순위 (Priority) - <strong>중요</strong></h4>
<p>CPU가 누구를 먼저 처리할지 결정하는 계급장. <strong>숫자가 낮을수록 높으신 분(우선순위 높음).</strong></p>
<ul>
<li><strong>PRI (Priority):</strong> <strong>커널(OS)</strong>이 보는 실제 우선순위.</li>
<li><strong>NI (Nice):</strong> <strong>사용자</strong>가 설정한 우선순위 조절 값.<ul>
<li><strong>범위:</strong> <code>20</code>(제일 급함/이기적) ~ <code>19</code>(제일 착함/양보).</li>
<li><strong>관계:</strong> 보통 <code>PRI = 20 + NI</code>.</li>
</ul>
</li>
</ul>
<h4 id="3-메모리-3대장-memory---가장-헷갈림">3. 메모리 3대장 (Memory) - <strong>가장 헷갈림</strong></h4>
<ul>
<li><strong>VIRT (Virtual Image):</strong> <strong>&quot;나 이만큼 필요할 수도 있어&quot;</strong>라고 선언한 가상 크기.<ul>
<li>라이브러리, 코드, 스왑 포함. 실제 물리 메모리 사용량이 아님 (허수). 겁먹지 말 것.</li>
</ul>
</li>
<li><strong>RES (Resident size):</strong> <strong>&quot;지금 당장 쓰고 있는 RAM&quot;</strong> 크기.<ul>
<li><strong>가장 중요.</strong> 실제 물리 메모리 점유율은 이걸 봐야 함 (진수).</li>
</ul>
</li>
<li><strong>SHR (Shared Mem):</strong> 다른 프로세스와 <strong>같이 쓰는</strong> 메모리.<ul>
<li>예: <code>libc.so</code> 같은 공유 라이브러리.</li>
</ul>
</li>
</ul>
<h4 id="4-상태-및-활동-status--activity">4. 상태 및 활동 (Status &amp; Activity)</h4>
<ul>
<li><strong>S (State):</strong> 현재 프로세스의 상태.<ul>
<li><strong><code>R</code> (Running):</strong> 일하는 중.</li>
<li><strong><code>S</code> (Sleeping):</strong> 대기 중 (대부분의 상태).</li>
<li><strong><code>D</code> (Disk Sleep):</strong> 디스크 I/O 기다리는 중 (강제 종료 불가능, 위험 신호).</li>
<li><strong><code>Z</code> (Zombie):</strong> 죽었는데 부모가 시신 수습 안 해줌.</li>
</ul>
</li>
<li><strong>CPU% / MEM%:</strong> CPU와 메모리(RES 기준) 점유율.</li>
<li><strong>TIME+:</strong> 프로세스가 시작된 후 <strong>CPU를 실제로 사용한 누적 시간</strong>. (켜놓은 시간이 아님).</li>
<li><strong>Command:</strong> 실행된 명령어 경로.</li>
</ul>
<h4 id="요약">요약</h4>
<ul>
<li><strong>메모리 누수 의심될 때:</strong> <strong>RES</strong>만 보면 됨.</li>
<li><strong>시스템 렉 걸릴 때:</strong> <strong>CPU%</strong> 높은 놈과 <strong>D</strong> 상태인 놈을 찾을 것.</li>
</ul>
<hr />
<ul>
<li>무거운 프로그램 실행 후 CPU/RAM 변화 관찰.</li>
</ul>