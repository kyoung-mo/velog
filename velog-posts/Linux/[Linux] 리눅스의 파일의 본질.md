<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f7928a25-30de-4574-8e66-1a5a8eada7d1/image.png" /></p>
<hr />
<p>리눅스에서 모든 객체(하드웨어 포함)는 '파일'로 취급되며, 우리는 <code>fd(정수 번호)</code> 라는 번호표를 통해 커널 안의 실제 파일과 소통한다.</p>
<hr />
<h3 id="1-핵심-철학-everything-is-a-file">1. 핵심 철학: Everything is a file</h3>
<ul>
<li><strong>추상화:</strong> 하드디스크 파일뿐만 아니라 <strong>키보드, 모니터, 프린터, 네트워크 소켓</strong>까지 전부 파일로 간주합니다.</li>
<li><strong>상호작용:</strong> 따라서 장치를 제어하는 방법도 복잡한 명령어가 아닌, <strong>단순한 <code>Read</code>(읽기)와 <code>Write</code>(쓰기)</strong>로 통일됩니다.</li>
</ul>
<h3 id="2-연결-고리-file-descriptor-fd">2. 연결 고리: File Descriptor (fd)</h3>
<ul>
<li><strong>정체:</strong> <strong><code>int</code> (비음수 정수)</strong>. (예: 3, 4, 5...)</li>
<li><strong>역할:</strong> 사용자 프로그램(User)이 커널(Kernel) 내부에 열려 있는 <strong>실제 파일 객체(메타데이터)</strong>를 가리키는 <strong>인덱스(참조 번호)</strong>입니다.</li>
<li><strong>공유:</strong> 커널은 파일을 관리하고, 사용자에게는 이 <strong>번호표(fd)</strong>만 건네줍니다. 사용자는 이 번호만 알면 됩니다.</li>
</ul>
<h3 id="3-시스템-프로그래밍의-표준-흐름-lifecycle">3. 시스템 프로그래밍의 표준 흐름 (Lifecycle)</h3>
<p>리눅스 프로그래밍의 90%는 이 과정을 따릅니다.</p>
<ol>
<li><strong>Open:</strong> &quot;파일 열어줘&quot; → 커널이 확인 후 <strong><code>fd</code> 번호 발급</strong>.</li>
<li><strong>Access:</strong> &quot;이 <code>fd</code>에 써줘&quot; → 커널이 <code>fd</code>를 보고 실제 파일에 기록.</li>
<li><strong>Close:</strong> &quot;이 <code>fd</code> 다 썼어&quot; → 커널이 <code>fd</code> 회수 및 리소스 정리.</li>
</ol>
<h4 id="표준-파일-디스크립터-standard-fd">표준 파일 디스크립터 (Standard FD)</h4>
<p>프로그램이 실행되자마자 기본적으로 할당받는 3가지 <code>fd</code>가 있습니다.</p>
<ul>
<li><strong>0:</strong> 표준 입력 (Stdin) - 키보드</li>
<li><strong>1:</strong> 표준 출력 (Stdout) - 모니터</li>
<li><strong>2:</strong> 표준 에러 (Stderr) - 모니터 (에러용)</li>
</ul>
<p>&quot;Inode는 파일의 '주민등록증(고유 식별자)', fd는 현재 프로세스가 발급받은 '대기 번호표(접근 핸들)'.”</p>
<table>
<thead>
<tr>
<th><strong>비교 항목</strong></th>
<th><strong>Inode (Index Node)</strong></th>
<th><strong>fd (File Descriptor)</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>정체</strong></td>
<td><strong>파일 그 자체 (메타데이터)</strong></td>
<td><strong>파일을 다루기 위한 번호 (핸들)</strong></td>
</tr>
<tr>
<td><strong>위치</strong></td>
<td><strong>디스크</strong> (물리적 저장)</td>
<td><strong>프로세스 메모리</strong> (커널 관리 테이블)</td>
</tr>
<tr>
<td><strong>유효 범위</strong></td>
<td>파일 시스템 전체에서 유일</td>
<td>해당 프로세스 안에서만 유일</td>
</tr>
<tr>
<td><strong>수명</strong></td>
<td>파일이 삭제될 때까지 영구적</td>
<td><code>close()</code> 하거나 프로세스 죽으면 사라짐</td>
</tr>
<tr>
<td><strong>포함 정보</strong></td>
<td>권한, 소유자, 크기, 데이터 위치</td>
<td>현재 읽기/쓰기 위치(Offset), 접근 모드</td>
</tr>
</tbody></table>
<h4 id="연결-구조-kernel-internal">연결 구조 (Kernel Internal)</h4>
<p>리눅스 커널은 이 둘을 <strong>3단계</strong>로 연결합니다.</p>
<ol>
<li><strong>프로세스 (fd 테이블):</strong> <code>fd 3</code>은 단순한 인덱스(번호)일 뿐입니다.</li>
<li><strong>오픈 파일 테이블 (File Table Entry):</strong> <code>fd</code>가 가리키는 곳. <strong>&quot;누가, 어떻게 열었고, 어디까지 읽었나(Offset)&quot;</strong>를 저장.</li>
<li><strong>Inode 테이블 (Vnode):</strong> 실제 디스크의 물리적 위치와 권한 정보.</li>
</ol>
<blockquote>
<p>관계: 여러 프로세스가 같은 파일을 열면?</p>
<ul>
<li><strong>fd:</strong> 서로 다름 (A프로세스: 3, B프로세스: 4).</li>
<li><strong>Open File Table:</strong> 서로 다름 (각자 읽는 위치가 다르니까).</li>
<li><strong>Inode:</strong> <strong>하나를 공유함</strong> (물리적 파일은 하나니까).</li>
</ul>
</blockquote>
<hr />
<h3 id="regular-파일">Regular 파일</h3>
<p>리눅스 파일은 '구조가 없는 바이트의 나열(Stream)'이며, 이름은 껍데기일 뿐 실체는 <strong>Inode</strong>이다.</p>
<hr />
<h3 id="1-파일의-본질-byte-stream">1. 파일의 본질 (Byte Stream)</h3>
<ul>
<li><strong>정의:</strong> 바이트(Byte)들이 선형으로 쭉 늘어선 <strong>배열</strong>.</li>
<li><strong>특징:</strong><ul>
<li><strong>No Structure:</strong> 리눅스 커널은 파일의 내용(이미지인지, 텍스트인지)을 모릅니다. 그냥 0과 1의 덩어리로 취급합니다.</li>
<li><strong>자유도:</strong> 파일 내부는 어떤 값이든 가질 수 있습니다.</li>
</ul>
</li>
</ul>
<h3 id="2-파일-접근과-오프셋-file-offset">2. 파일 접근과 오프셋 (File Offset)</h3>
<ul>
<li><strong>개념:</strong> 현재 파일의 <strong>&quot;어디를 읽고/쓰고 있나&quot;</strong>를 가리키는 위치 커서.</li>
<li><strong>동작:</strong><ul>
<li>파일 열면 <strong>0</strong>에서 시작.</li>
<li>읽거나(<code>read</code>) 쓰면(<code>write</code>) 그만큼 숫자가 <strong>증가</strong>.</li>
</ul>
</li>
<li><strong>주의 (덮어쓰기):</strong><ul>
<li>파일 중간에 데이터를 쓰면 <strong>끼워넣기(Insert)가 아니라 덮어쓰기(Overwrite)</strong>가 됩니다.</li>
<li>파일 크기 확장은 보통 <strong>맨 끝(End of File)</strong>에 쓸 때 일어납니다.</li>
</ul>
</li>
</ul>
<h3 id="3-동시성-및-공유-concurrency">3. 동시성 및 공유 (Concurrency)</h3>
<ul>
<li><strong>다중 오픈:</strong> 하나의 파일을 여러 프로세스가(혹은 한 프로세스가 여러 번) 동시에 <code>open()</code> 할 수 있음.</li>
<li><strong>고유성:</strong> 열 때마다 새로운 *<em><code>fd</code></em>가 발급됨. (서로 다른 오프셋을 가짐).</li>
<li><strong>동기화:</strong> 커널은 교통정리를 안 해줍니다. A가 쓰고 있는데 B가 덮어써도 막지 않습니다. <strong>(사용자 공간에서 <code>flock</code> 등으로 직접 동기화 필수).</strong></li>
</ul>
<h3 id="4-식별자-inode-vs-filename">4. 식별자 (Inode vs Filename)</h3>
<ul>
<li><strong>파일명:</strong> 사용자가 보기 편하게 붙인 <strong>별명(껍데기)</strong>.</li>
<li><strong>Inode (i-number):</strong> 파일 시스템이 파일을 관리하는 <strong>진짜 주민등록번호(실체)</strong>.<ul>
<li>모든 파일 접근은 내부적으로 <code>파일명</code> → <code>Inode 번호</code> 변환을 거쳐 일어납니다.</li>
</ul>
</li>
</ul>
<hr />
<h2 id="inode">Inode</h2>
<p>Inode는 파일의 <code>실체(메타데이터+데이터 위치)</code>이며, 파일명은 이 Inode를 가리키는 <code>문패(Link)</code>일 뿐이다.</p>
<hr />
<h3 id="1-inode의-정체-metadata-store">1. Inode의 정체 (Metadata Store)</h3>
<ul>
<li><strong>정의:</strong> 파일에 대한 <strong>모든 정보(메타데이터)</strong>를 담고 있는 핵심 자료구조.</li>
<li><strong>포함하는 것:</strong><ul>
<li><strong>속성:</strong> 파일 크기, 소유자(UID), 권한(Permission), 시간(Timestamps).</li>
<li><strong>위치 정보:</strong> 실제 데이터가 디스크 어디(Block)에 저장되어 있는지 가리키는 <strong>포인터</strong>.</li>
</ul>
</li>
<li><strong>포함하지 않는 것:</strong> <strong>파일 이름(Filename)</strong>. (이름은 디렉터리가 관리함).</li>
<li><strong>존재 형태:</strong><ul>
<li><strong>물리적:</strong> 디스크의 특정 영역(Inode Table)에 저장된 객체.</li>
<li><strong>논리적:</strong> 리눅스 커널 메모리에 로드된 <code>struct inode</code> 객체.</li>
</ul>
</li>
</ul>
<h3 id="2-파일명과-inode의-관계-the-link">2. 파일명과 Inode의 관계 (The Link)</h3>
<ul>
<li><strong>파일명:</strong> 파일 그 자체가 아니라, <strong>Inode 번호를 가리키는 별명(Link)</strong>에 불과합니다.</li>
<li><strong>디렉터리 엔트리:</strong> 디렉터리는 <code>(파일 이름, Inode 번호)</code> 쌍을 저장하는 리스트입니다.</li>
<li><strong>하드 링크(Hard Link):</strong><ul>
<li>여러 개의 파일명(별명)이 <strong>동일한 Inode 번호</strong>를 가리킬 수 있습니다.</li>
<li>파일명은 달라도 실체(Inode)는 하나이므로 데이터도 같습니다.</li>
</ul>
</li>
</ul>
<h3 id="3-파일-접근-흐름-lookup">3. 파일 접근 흐름 (Lookup)</h3>
<ol>
<li><strong>요청:</strong> 사용자가 <code>/home/pi/test.txt</code> 읽기 요청.</li>
<li><strong>검색:</strong> 커널이 디렉터리를 뒤져 <code>test.txt</code>라는 이름에 매핑된 <strong>Inode 번호</strong>를 찾음.</li>
<li><strong>로딩:</strong> 해당 번호의 <strong>Inode</strong>를 메모리로 읽어옴.</li>
<li><strong>접근:</strong> Inode 안에 적힌 <strong>권한</strong>을 확인하고, <strong>데이터 블록 위치</strong>를 찾아 데이터를 읽음.</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/483e80da-597b-4953-b034-554b9834c267/image.png" /></p>
<hr />
<h3 id="directory와link">Directory와Link</h3>
<hr />
<p><strong>&quot;디렉터리는 파일을 담는 상자가 아니라, '파일 이름'과 'Inode 번호'를 짝지어 놓은 전화번호부(Mapping Table)이다.”</strong></p>
<h3 id="1-디렉터리와-링크의-본질">1. 디렉터리와 링크의 본질</h3>
<ul>
<li><strong>디렉터리 (Directory):</strong><ul>
<li><strong>역할:</strong> 사용자에게 <strong>사람이 읽을 수 있는 이름</strong>을 제공하고, 커널이 쓰는 <strong>Inode 번호</strong>로 변환(Mapping)해주는 특수 파일.</li>
<li><strong>구조:</strong> 내부적으로는 단순히 <strong><code>{파일 이름 : Inode 번호}</code></strong> 쌍(Link)들의 리스트만 담고 있음.</li>
<li><strong>목적:</strong> 복잡한 Inode 번호를 직접 외우는 번거로움을 없애고 접근 제어(보안)를 도움.</li>
</ul>
</li>
<li><strong>링크 (Link):</strong><ul>
<li>디렉터리 안에 기록된 <strong>[파일 이름] + [Inode]</strong>의 매핑 한 줄.</li>
</ul>
</li>
</ul>
<h3 id="2-경로-이름-해석-pathname-resolution">2. 경로 이름 해석 (Pathname Resolution)</h3>
<p>커널이 <code>/home/pi/file.c</code>라는 요청을 받았을 때의 동작 과정입니다.
<strong>&quot;이름 → 디렉터리 뒤지기 → Inode 획득 → 파일 접근&quot;</strong></p>
<ol>
<li><strong>디렉터리 열기:</strong> 해당 이름이 포함된 디렉터리(예: <code>/home</code>)를 읽음.</li>
<li><strong>검색:</strong> 디렉터리 리스트에서 파일 이름(pi)과 일치하는 항목을 찾음.</li>
<li><strong>Inode 추출:</strong> 그 이름 옆에 적힌 <strong>Inode 번호</strong>를 알아냄.</li>
<li><strong>반복/접근:</strong> 최종 파일에 도달할 때까지 이 과정을 반복하여 실제 Inode(데이터)에 접근.</li>
</ol>
<h3 id="3-경로의-종류-pathname">3. 경로의 종류 (Pathname)</h3>
<table>
<thead>
<tr>
<th><strong>종류</strong></th>
<th><strong>설명</strong></th>
<th><strong>예시</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>Absolute Path</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td>(절대 경로)</td>
<td><strong>루트(<code>/</code>)</strong>부터 시작하는 완전한 주소 (Fully Qualified).</td>
<td><code>/home/pi/lab/ch02/access.c</code></td>
</tr>
<tr>
<td><strong>Relative Path</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td>(상대 경로)</td>
<td><strong>현재 위치(<code>pwd</code>)</strong>를 기준으로 찾아가는 주소.</td>
<td><code>lab/ch02/access.c</code></td>
</tr>
</tbody></table>
<h3 id="4-디렉터리-조작-operation">4. 디렉터리 조작 (Operation)</h3>
<p>디렉터리도 파일(<code>dentry</code>)이지만, 구조가 깨지면 파일 시스템 전체가 꼬이기 때문에 <strong>일반적인 쓰기(<code>write</code>)가 금지</strong>되어 있습니다.</p>
<ul>
<li><strong>일반 조작:</strong> <code>open()</code>, <code>write()</code> 불가능.</li>
<li><strong>전용 시스템 콜:</strong><ul>
<li><strong>생성:</strong> <code>mkdir()</code></li>
<li><strong>삭제:</strong> <code>rmdir()</code> (단, 비어있을 때만 가능. <code>rm -r</code>은 재귀적으로 비우고 지우는 유틸리티 기능)</li>
</ul>
</li>
</ul>
<hr />
<h3 id="hard-link-vs-symbolic-link">Hard link vs. Symbolic link</h3>
<hr />
<p><strong>&quot;Hard Link는 '동일한 파일의 또 다른 이름(별명)', Symbolic Link는 '원본 위치를 가리키는 바로가기(Shortcut)'.&quot;</strong></p>
<h3 id="1-hard-link-하드-링크">1. Hard Link (하드 링크)</h3>
<p><strong>&quot;하나의 Inode를 여러 이름이 공유하는 것.&quot;</strong></p>
<ul>
<li><strong>구조:</strong> 원본 파일과 <strong>동일한 Inode 번호</strong>를 가짐.</li>
<li><strong>특징:</strong><ul>
<li>원본과 링크의 구분이 없음 (완벽하게 동등한 파일).</li>
<li><code>rm</code>으로 원본을 지워도, 링크가 남아있다면 <strong>데이터는 삭제되지 않음</strong> (Inode Reference Count가 0이 되어야 삭제됨).</li>
</ul>
</li>
<li><strong>제약:</strong> <strong>같은 파일 시스템(파티션) 내에서만</strong> 생성 가능. (Inode 번호는 파티션마다 따로 관리되므로).</li>
</ul>
<h3 id="2-symbolic-link-심볼릭-링크--soft-link">2. Symbolic Link (심볼릭 링크 / Soft Link)</h3>
<p><strong>&quot;다른 파일을 가리키는 경로(Path)를 담은 별도의 파일.&quot;</strong></p>
<ul>
<li><strong>구조:</strong> <strong>자신만의 고유한 Inode</strong>를 가짐.</li>
<li><strong>내용:</strong> 실제 데이터가 아니라, 원본 파일이 있는 <strong>&quot;경로 문자열&quot;</strong>만 저장하고 있음.</li>
<li><strong>특징:</strong><ul>
<li>윈도우의 '바로가기 아이콘'과 동일.</li>
<li><strong>파일 시스템(파티션)을 넘나들 수 있음.</strong></li>
<li><strong>오버헤드:</strong> 원본을 찾기 위해 경로를 해석하는 과정이 추가되므로 Hard Link보다 느림.</li>
</ul>
</li>
<li><strong>제약:</strong> 원본 파일을 지우면 링크는 <strong>&quot;깨진 링크(Broken Link)&quot;</strong>가 되어 사용 불가.</li>
</ul>
<h3 id="3-비교-요약">3. 비교 요약</h3>
<table>
<thead>
<tr>
<th><strong>구분</strong></th>
<th><strong>Hard Link</strong></th>
<th><strong>Symbolic Link</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>Inode 번호</strong></td>
<td><strong>원본과 같음</strong> (공유)</td>
<td><strong>다름</strong> (새로 생성)</td>
</tr>
<tr>
<td><strong>데이터</strong></td>
<td>원본 데이터 직접 가리킴</td>
<td>원본의 <strong>경로(Path)</strong> 저장</td>
</tr>
<tr>
<td><strong>파티션 이동</strong></td>
<td><strong>불가능</strong> (동일 파티션만)</td>
<td><strong>가능</strong> (어디든 참조 가능)</td>
</tr>
<tr>
<td><strong>원본 삭제 시</strong></td>
<td>파일 살아있음 (접근 가능)</td>
<td><strong>링크 깨짐</strong> (접근 불가)</td>
</tr>
<tr>
<td><strong>속도</strong></td>
<td>빠름 (직접 접근)</td>
<td>약간 느림 (경로 해석 필요)</td>
</tr>
<tr>
<td><strong>명령어</strong></td>
<td><code>ln 원본 링크명</code></td>
<td><code>ln -s 원본 링크명</code></td>
</tr>
</tbody></table>
<hr />
<h3 id="특수-파일special-files">특수 파일(Special files)</h3>
<hr />
<p>&quot;리눅스는 하드웨어 장치(키보드, 디스크)나 통신 채널(소켓)도 전부 '파일'로 취급하여 관리한다.”</p>
<h3 id="1-장치-파일-device-files---dev"><strong>1. 장치 파일 (Device Files) - <code>/dev</code></strong></h3>
<p>하드웨어를 제어하기 위한 인터페이스입니다.</p>
<table>
<thead>
<tr>
<th><strong>구분</strong></th>
<th><strong>Block Device (블록 장치)</strong></th>
<th><strong>Character Device (문자 장치)</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>데이터 구조</strong></td>
<td><strong>바이트 배열 (Array)</strong></td>
<td><strong>선형 큐 (Queue)</strong></td>
</tr>
<tr>
<td><strong>접근 방식</strong></td>
<td><strong>Random Access</strong> (순서 무관, 임의 접근)</td>
<td><strong>Sequential Access</strong> (순서대로, 스트림)</td>
</tr>
<tr>
<td><strong>동작 특징</strong></td>
<td>데이터를 블록 단위로 버퍼링하여 전송</td>
<td>데이터를 한 바이트씩 흐르는 대로 처리</td>
</tr>
<tr>
<td><strong>예시</strong></td>
<td><strong>하드디스크, SSD, USB 메모리</strong></td>
<td><strong>키보드, 마우스, 시리얼 포트, 프린터</strong></td>
</tr>
<tr>
<td><strong>비고</strong></td>
<td><code>lseek</code>으로 위치 이동 가능</td>
<td>이동 불가. (읽을 게 없으면 <code>EOF</code> 또는 대기)</td>
</tr>
</tbody></table>
<h3 id="2-ipc통신-파일---프로세스-간-대화-수단"><strong>2. IPC(통신) 파일 - 프로세스 간 대화 수단</strong></h3>
<h3 id="①-named-pipe-fifo">① Named Pipe (FIFO)</h3>
<ul>
<li><strong>정의:</strong> 파일 시스템에 <strong>이름(파일명)</strong>을 가지고 존재하는 파이프.</li>
<li><strong>특징:</strong><ul>
<li>부모-자식 관계가 아닌 <strong>전혀 다른 프로세스끼리도</strong> 통신 가능.</li>
<li><code>mkfifo</code> 명령어로 생성.</li>
<li>한쪽이 읽기 전까지 쓰기 작업이 블로킹(대기)됨.</li>
</ul>
</li>
</ul>
<h3 id="②-socket-소켓">② Socket (소켓)</h3>
<ul>
<li><strong>정의:</strong> 네트워크 또는 로컬 통신을 위한 <strong>진보된 IPC의 끝점(Endpoint)</strong>.</li>
<li><strong>유형:</strong><ul>
<li><strong>Unix Domain Socket:</strong> <strong>동일 머신</strong> 내에서 가장 빠른 통신 (파일 경로 사용).</li>
<li><strong>Internet Socket:</strong> <strong>다른 머신(네트워크)</strong> 간 통신 (IP 주소 + Port 번호 필요).</li>
</ul>
</li>
<li><strong>특징:</strong> 양방향 통신이 가능하며, 현대 서버 프로그래밍의 핵심.</li>
</ul>