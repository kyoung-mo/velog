<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/601651da-1e6f-4783-99ce-da150919b45f/image.png" /></p>
<hr />
<h2 id="1-파일-시스템과-탐색">1. 파일 시스템과 탐색</h2>
<p><strong>목표:</strong> 리눅스 디렉토리 구조(Tree)를 이해하고, 마우스 없이 자유자재로 이동하고 파일을 조작한다.</p>
<h3 id="이론">이론</h3>
<ul>
<li><p>리눅스 디렉토리 구조(Tree)를 가진다.</p>
</li>
<li><p><strong>리눅스 파일 시스템 구조:</strong></p>
<ul>
<li><code>/</code> (Root): 모든 것의 시작.</li>
<li><code>/home/user</code> (~) : 내 앞마당 (유일하게 마음대로 쓸 수 있는 곳).</li>
<li><code>/bin</code>, <code>/etc</code>, <code>/dev</code>: 명령어, 설정, 장치 파일 위치 (임베디드에서 중요).</li>
</ul>
</li>
<li><p><strong>절대 경로 vs 상대 경로:</strong></p>
<ul>
<li><code>/home/pi/project</code> vs <code>../../project</code></li>
</ul>
</li>
<li><p><strong>필수 명령어 5대장:</strong></p>
<ul>
<li><code>ls -al</code>: 숨김 파일까지 자세히 보기.</li>
<li><code>cd</code>: 이동 (<code>cd ..</code>, <code>cd ~</code>, <code>cd -</code>).</li>
<li><code>pwd</code>: 현재 위치 확인.</li>
<li><code>mkdir -p</code>: 디렉토리 생성 (중간 경로 포함 생성).</li>
<li><code>rm -rf</code>: <strong>(주의)</strong> 묻지도 따지지도 않고 삭제.</li>
<li><code>nano ~/.bashrc</code></li>
<li><code>alias rm=”rm -i”</code></li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c4ebd4ec-16c2-4e13-aebf-3ad2f5ad85a7/image.png" /></p>
<hr />
<h3 id="실습">실습</h3>
<p>터미널을 열고 다음 미션을 순서대로 수행하세요.</p>
<ol>
<li>홈 디렉토리(<code>~</code>)로 이동.</li>
<li><code>workspace/embedded/project_A</code> 디렉토리를 명령어 한 줄로 생성 (<code>p</code> 옵션).</li>
<li><code>project_A</code> 안으로 이동.</li>
<li><code>main.c</code>라는 빈 파일 생성 (<code>touch</code> 명령어 사용).</li>
<li><code>main.c</code>를 복사하여 <code>backup.c</code> 만들기 (<code>cp</code>).</li>
<li>상위 디렉토리(<code>embedded</code>)로 나와서 <code>project_A</code> 폴더 이름을 <code>final_project</code>로 변경 (<code>mv</code>).</li>
<li><code>final_project</code> 폴더를 통째로 삭제 (<code>rm</code>).</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cb358736-5a64-43af-864d-17c90613f42f/image.png" /></p>
<h2 id="2-권한permission과-프로세스-제어">2. 권한(Permission)과 프로세스 제어</h2>
<p><strong>목표:</strong> &quot;Permission denied&quot; 에러를 해결하고, 죽은 프로그램을 강제로 종료시킨다.</p>
<h3 id="1-이론">1. 이론</h3>
<ul>
<li><strong>권한의 3요소:</strong> <code>r</code>(읽기, 4), <code>w</code>(쓰기, 2), <code>x</code>(실행, 1).<ul>
<li><code>chmod 755</code>: 소유자는 다 하고, 남들은 실행/읽기만.</li>
<li><code>chmod +x</code>: 실행 권한 추가 (스크립트/실행파일 필수).</li>
</ul>
</li>
<li><strong>슈퍼유저 (Root):</strong><ul>
<li><code>sudo</code>: &quot;관리자 권한으로 실행하라&quot;.</li>
</ul>
</li>
<li><strong>프로세스 관리:</strong><ul>
<li><code>ps -ef</code>: 현재 실행 중인 프로세스 목록.</li>
<li><code>kill -9 &lt;PID&gt;</code>: 좀비 프로세스나 응답 없는 프로그램 강제 종료.</li>
<li><code>| grep</code> (맛보기): 너무 많은 출력 중 원하는 단어 찾기.</li>
</ul>
</li>
</ul>
<h3 id="2-실습-비밀-파일과-실행-파일">2. 실습: &quot;비밀 파일과 실행 파일&quot;</h3>
<ol>
<li><code>secret.txt</code> 파일을 만들고 내용 입력 (&quot;This is top secret&quot;).</li>
<li><code>chmod 000 secret.txt</code> 명령 후 <code>cat secret.txt</code>로 읽기 시도 (에러 확인).</li>
<li><code>chmod 400 secret.txt</code> 후 다시 읽기 시도 (성공).</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5f5b3d4e-98a4-4483-a38f-9d7ab4c05010/image.png" /></p>
<ol start="4">
<li><strong>C언어 컴파일러 실행 권한 실습:</strong><ul>
<li>간단한 <code>hello.c</code> 작성 (nano 또는 vim 사용).</li>
<li><code>gcc hello.c -o hello</code> 로 빌드.</li>
<li><code>./hello</code>로 실행 확인.</li>
<li><code>chmod -x hello</code> 후 실행 시도 (&quot;Permission denied&quot; 확인).</li>
</ul>
</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f2a9cee4-ec38-4ecb-8944-6c3e1eea1338/image.png" /></p>
<hr />
<h2 id="3-파이프pipe와-리다이렉션">3. 파이프(Pipe)와 리다이렉션</h2>
<p><strong>목표:</strong> 명령어들의 출력을 연결하고, 로그 파일을 가공하여 원하는 정보만 추출한다.</p>
<h3 id="1-이론-1">1. 이론</h3>
<ul>
<li><strong>표준 입출력:</strong> <code>stdin</code>(0), <code>stdout</code>(1), <code>stderr</code>(2).</li>
<li><strong>리다이렉션 (Redirection):</strong><ul>
<li><code>&gt;</code> : 덮어쓰기 (화면 출력을 파일로 저장).</li>
<li><code>&gt;&gt;</code> : 이어쓰기 (로그 쌓을 때 사용).</li>
</ul>
</li>
<li><strong>파이프 (Pipe, <code>|</code>):</strong><ul>
<li>A 명령어의 결과를 B 명령어의 입력으로 넘김.</li>
<li>예: <code>cat large_log.txt | grep &quot;Error&quot;</code></li>
</ul>
</li>
<li><strong>검색 도구 (<code>grep</code>):</strong><ul>
<li>파일 내에서 특정 문자열 찾기. (개발자의 눈).</li>
<li><code>grep -r &quot;main&quot; .</code>: 현재 폴더 하위의 모든 파일에서 &quot;main&quot; 찾기.</li>
</ul>
</li>
</ul>
<h3 id="2-실습-로그-분석-시뮬레이션">2. 실습: &quot;로그 분석 시뮬레이션&quot;</h3>
<ol>
<li><p>가상의 로그 파일 생성 (아래 내용을 <code>sys.log</code>로 저장).Plaintext</p>
<pre><code class="language-bash"> [INFO] System Boot
 [INFO] Network Start
 [ERROR] WiFi Connection Failed
 [WARN] Battery Low
 [ERROR] Sensor Timeout</code></pre>
</li>
<li><p><code>sys.log</code>에서 &quot;ERROR&quot;가 포함된 줄만 뽑아서 <code>error_report.txt</code>에 저장 (<code>grep</code>과 <code>&gt;</code> 사용).</p>
</li>
<li><p><code>ps -ef</code> 명령어로 현재 실행 중인 모든 프로세스를 출력하되, <code>bash</code>라는 글자가 들어간 프로세스만 화면에 출력 (<code>| grep</code> 사용).</p>
</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f3b5d92d-103f-4d93-9c0a-a70c9d26129f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/09043cf8-3c61-4fdb-9202-485d0ca43b31/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/12d09ace-beb3-4875-b78f-77922b5a9455/image.png" /></p>
<hr />
<h2 id="4-쉘-스크립트shell-script-기초">4. 쉘 스크립트(Shell Script) 기초</h2>
<p><strong>목표:</strong> 반복되는 컴파일, 배포 작업을 자동화하는 스크립트 작성 (.sh).</p>
<h3 id="1-이론-2">1. 이론</h3>
<ul>
<li><strong>Shebang (<code>#!/bin/bash</code>):</strong> 이 파일은 bash로 실행하라는 선언.</li>
<li><strong>변수 사용:</strong><ul>
<li>선언: <code>NAME=&quot;Raspberry&quot;</code> (띄어쓰기 금지).</li>
<li>사용: <code>echo $NAME</code>.</li>
</ul>
</li>
<li><strong>인자 받기:</strong> <code>$1</code>, <code>$2</code> (스크립트 실행 시 넘겨주는 값).</li>
<li><strong>조건문 (<code>if</code>)과 반복문 (<code>for</code>):</strong><ul>
<li>파일이 존재하는지 확인 (<code>f</code>).</li>
<li>폴더 내의 모든 파일에 대해 작업 반복.</li>
</ul>
</li>
</ul>
<h3 id="2-실습-자동-빌드-스크립트-만들기">2. 실습: &quot;자동 빌드 스크립트 만들기&quot;</h3>
<p>C언어 소스 파일이 여러 개일 때, 한 번에 빌드하고 실행까지 해주는 <code>build.sh</code>를 만듭니다.</p>
<ol>
<li><code>build.sh</code> 파일 생성 및 작성:Bash</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/530146d3-935a-4bca-892e-140d3f867f7d/image.png" /></p>
<pre><code class="language-bash">#!/bin/bash

TARGET=&quot;my_app&quot;
SRC=&quot;main.c&quot;

echo &quot;--- 빌드를 시작합니다: $TARGET ---&quot;

# 1. gcc로 컴파일 시도
if gcc $SRC -o $TARGET; then
    echo &quot;✅ 빌드 성공!&quot;

    echo &quot;--- 프로그램을 실행합니다 ---&quot;
    ./$TARGET
else
    echo &quot;❌ 빌드 실패! 코드를 확인하세요.&quot;
fi</code></pre>
<ol start="2">
<li><code>chmod +x build.sh</code>로 실행 권한 부여.</li>
<li><code>main.c</code>에 고의로 문법 에러를 내보고 스크립트 실행 -&gt; &quot;❌ 빌드 실패&quot; 확인.</li>
<li><code>main.c</code> 수정 후 스크립트 실행 -&gt; &quot;✅ 빌드 성공&quot; 및 프로그램 실행 확인.</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d3ed79ef-2a2e-4589-be71-4160d177e2fc/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8644c1ea-1aae-4692-b49c-d33aa9aa5106/image.png" /></p>
<hr />
<h2 id="팁">팁</h2>
<ol>
<li><strong>Tab 자동완성:</strong>: &quot;Tab 키를 안 쓰는 것은 인생의 낭비입니다&quot;</li>
<li><strong>명령어 히스토리:</strong> 방향키 <code>↑</code> <code>↓</code>로 이전 명령어 불러오기. 오타 수정할 때 필수</li>
<li><strong>Visual Studio Code 활용:</strong> VSCode의 'Remote - SSH' 기능</li>
<li><strong>임베디드와의 연관성 :</strong><ul>
<li><code>ls /dev</code> : 센서와 장치</li>
<li><code>sudo</code> : GPIO 핀 제어할 때 권한 없으면 에러.</li>
<li><code>grep</code> : 커널 로그(<code>dmesg</code>)에서 에러 찾을 때 씁니다.</li>
</ul>
</li>
</ol>