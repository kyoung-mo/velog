<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/988223cf-e145-4241-9043-c662b8c38955/image.png" /></p>
<hr />
<h3 id="테스트-파일-만들기">테스트 파일 만들기</h3>
<pre><code class="language-bash"># 실습 디렉터리 생성
mkdir ~/text_practice
cd ~/text_practice</code></pre>
<pre><code class="language-bash"># 여러 파일 생성
cat &gt; file1.txt &lt;&lt; EOF
TODO: Fix the login bug
Error: Connection failed
error: Database timeout
This is a normal line
TODO: Update documentation
EOF

cat &gt; file2.txt &lt;&lt; EOF
Function: calculateTotal()
ERROR: Memory overflow
Success: Login completed
TODO: Add error handling
EOF

cat &gt; config.conf &lt;&lt; EOF
# This is a comment
ServerPort=8080
# Another comment

DatabaseURL=localhost
# End of config
EOF</code></pre>
<hr />
<h3 id="텍스트-필터-1-grep">텍스트 필터 1. grep</h3>
<ul>
<li><strong>학습:</strong> 파일 내 특정 문자열 검색. 정규표현식 맛보기.</li>
<li><strong>실습:</strong><ul>
<li>프로젝트 폴더 내 모든 파일에서 <code>TODO</code> 주석 찾기 
(<code>grep -r &quot;TODO&quot; .</code>).</li>
<li>대소문자 무시(<code>i</code>), 줄 번호 출력(<code>n</code>), 매칭 안 되는 것 출력(<code>v</code>) 실습.</li>
<li><code>| grep</code> 파이프라인 연계 연습.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="실전-예제">실전 예제</h3>
<h4 id="1-이-함수-어디에-정의돼-있지-프로젝트-전체-검색">1. &quot;이 함수 어디에 정의돼 있지?&quot; (프로젝트 전체 검색)</h4>
<p>가장 많이 씀. 현재 폴더 하위의 모든 파일에서 특정 문자열을 찾음.</p>
<p>Bash</p>
<pre><code class="language-bash">grep -rni &quot;함수이름&quot; .</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d433b2d5-38db-454d-bb23-68202fb94b14/image.png" /></p>
<ul>
<li><strong><code>r</code> (Recursive):</strong> 하위 폴더까지 싹 다 뒤짐.</li>
<li><strong><code>n</code> (Line Number):</strong> 몇 번째 줄인지 알려줌.</li>
<li><strong><code>i</code> (Ignore case):</strong> 대소문자 구분 안 함 (Error, error 다 찾음).</li>
<li><strong><code>.</code></strong>: 현재 위치에서 시작.</li>
</ul>
<h4 id="2-프로세스가-죽었나-살았나-실행-중인-프로세스-확인">2. &quot;프로세스가 죽었나 살았나?&quot; (실행 중인 프로세스 확인)</h4>
<p>특정 프로그램이 실행 중인지 확인할 때 사용.</p>
<p>Bash</p>
<pre><code class="language-bash">ps -ef | grep &quot;python&quot; | grep -v &quot;grep&quot;</code></pre>
<ul>
<li><strong><code>ps -ef</code></strong>: 모든 프로세스 출력.</li>
<li><strong><code>|</code> (Pipe):</strong> 앞의 결과를 grep에게 넘김.</li>
<li><strong><code>grep -v &quot;grep&quot;</code></strong>: 검색하고 있는 나 자신(<code>grep</code> 명령어)은 결과에서 뺌. (이게 꿀팁).<pre><code class="language-bash">pi@pi-222:~/project/text_practice $ ps -ef | grep &quot;python&quot; | grep -v &quot;grep&quot;
root        1331       1  0 Jan29 ?        00:00:00 python /usr/sbin/wayvnc-control.py</code></pre>
</li>
</ul>
<h4 id="3-에러-났는데-그-앞뒤-상황-좀-보자-전후-문맥-확인">3. &quot;에러 났는데, 그 앞뒤 상황 좀 보자&quot; (전후 문맥 확인)</h4>
<p>로그 파일에서 &quot;Error&quot;만 딱 보면 원인을 모름. 에러 발생 <strong>전후 5줄</strong>을 같이 뽑아봄.</p>
<p>Bash</p>
<pre><code class="language-bash">grep -C 5 &quot;Error&quot; file1.txt
sudo grep -C 5 &quot;error&quot; /var/log/syslog
sudo grep -C 5 &quot;Failed&quot; /var/log/auth.log</code></pre>
<ul>
<li><strong><code>C 5</code> (Context):</strong> 해당 단어 위아래 5줄씩 같이 출력.</li>
<li><strong><code>B 5</code> (Before):</strong> 위(이전) 5줄만.</li>
<li><strong><code>A 5</code> (After):</strong> 아래(이후) 5줄만.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7737068c-6a8a-479e-bb9f-3101f36efa52/image.png" /></p>
<h4 id="4-주석이랑-빈-줄-다-빼고-알맹이만-줘-설정-파일-읽기">4. &quot;주석이랑 빈 줄 다 빼고 알맹이만 줘&quot; (설정 파일 읽기)</h4>
<p><code>conf</code> 파일이나 소스 코드에서 주석(<code>#</code>)과 공백을 제거하고 진짜 설정값만 보고 싶을 때.</p>
<p>Bash</p>
<pre><code class="language-bash">grep -v &quot;^#&quot; config.conf | grep -v &quot;^$&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/acecbf73-cbf9-432e-ba48-f9514f786557/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/423257b3-7106-4ff8-a4a9-6998c69abf48/image.png" /></p>
<ul>
<li><strong><code>v</code> (Invert):</strong> 해당 패턴을 <strong>제외</strong>하고 출력.</li>
<li><strong><code>^#</code></strong>: <code>#</code>으로 시작하는 줄 (주석).</li>
<li><strong><code>^$</code></strong>: 아무것도 없는 줄 (빈 줄).</li>
</ul>
<h4 id="5-그래서-에러가-몇-번-났는데-개수-세기">5. &quot;그래서 에러가 몇 번 났는데?&quot; (개수 세기)</h4>
<p>로그 파일 열어서 눈으로 세지 말고 숫자로 바로 확인.</p>
<p>Bash</p>
<pre><code class="language-bash">grep -c &quot;Failed&quot; auth.log
grep -c &quot;Error&quot; file1.txt
grep -c &quot;Error&quot; file1.txt</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b161f560-9faa-4331-a719-5fbacee8f4be/image.png" /></p>
<ul>
<li><strong><code>c</code> (Count):</strong> 검색된 줄의 <strong>개수</strong>만 출력.</li>
<li><strong>응용:</strong> <code>cat *.log | grep -c &quot;Error&quot;</code> (모든 로그 합쳐서 에러 카운트).</li>
</ul>
<hr />
<h3 id="텍스트-필터-2-awk-sed">텍스트 필터 2. awk, sed</h3>
<ul>
<li><strong>학습:</strong> 데이터 가공 및 치환.</li>
<li><strong>실습:</strong></li>
</ul>
<p><code>ls -l | awk '{print $9}'</code>은 가장 흔하게 쓰이지만, <strong>치명적인 약점(공백)</strong>이 있는 방법임. </p>
<hr />
<h3 id="ls--l-결과에서-파일명9번째-필드만-뽑아내기-awk-print-9">ls -l 결과에서 파일명(9번째 필드)만 뽑아내기 (awk '{print $9}').</h3>
<p><code>awk</code>는 기본적으로 <strong>&quot;공백(Space)&quot;</strong>을 기준으로 문장을 쪼개서 <code>$1, $2, $3...</code>에 담음.</p>
<h4 id="1-동작-원리-해부">1. 동작 원리 (해부)</h4>
<p><code>ls -l</code>의 결과는 보통 9개의 덩어리로 이루어져 있음.</p>
<pre><code class="language-bash">rw-r--r-- 1 root root 4096 Jan 29 20:30 my_file.txt
[ $1 ] [$2] [$3] [$4] [$5] [$6] [$7] [$8] [ $9 ]</code></pre>
<ul>
<li><strong>$1:</strong> 권한 (<code>rw-r--r--</code>)</li>
<li><strong>$3:</strong> 소유자 (<code>root</code>)</li>
<li><strong>$5:</strong> 파일 크기 (<code>4096</code>)</li>
<li><strong>$9:</strong> <strong>파일 이름</strong> (<code>my_file.txt</code>)</li>
</ul>
<p>따라서 <code>print $9</code>를 하면 맨 뒤에 있는 파일 이름만 쏙 뽑혀 나옴.</p>
<hr />
<h4 id="2-치명적인-약점-공백이-있는-파일">2. 치명적인 약점 (공백이 있는 파일)</h4>
<p>파일 이름에 띄어쓰기가 있으면 망함.</p>
<ul>
<li><strong>파일 이름:</strong> <code>Important Data.txt</code></li>
<li><strong>인식:</strong><ul>
<li><code>$9</code> : <code>Important</code></li>
<li><code>$10</code>: <code>Data.txt</code></li>
</ul>
</li>
<li><strong>결과:</strong> <code>print $9</code>를 하면 <strong>&quot;Important&quot;</strong>만 출력되고 뒤는 잘림.</li>
</ul>
<hr />
<h4 id="3-해결책">3. 해결책</h4>
<h4 id="방법-a-awk로-끝까지-다-찍기-복잡">방법 A. AWK로 끝까지 다 찍기 (복잡)</h4>
<p><code>$9</code>부터 문장 끝(<code>$NF</code>)까지 반복문을 돌려야 함.</p>
<p>Bash</p>
<pre><code class="language-bash">ls -l | awk '{for(i=9; i&lt;=NF; i++) printf $i &quot; &quot;; print &quot;&quot;}'</code></pre>
<h4 id="방법-b-그냥-ls-옵션-쓰기">방법 B. 그냥 ls 옵션 쓰기</h4>
<p><code>awk</code>를 쓸 필요 없이, <code>ls</code> 자체 기능으로 이름만 출력하는 게 제일 빠르고 정확함.</p>
<p>Bash</p>
<p><code>ls -1</code></p>
<ul>
<li><strong>숫자 1:</strong> 한 줄에 하나씩 이름만 출력하라는 옵션.</li>
<li>공백이 있어도 완벽하게 한 줄에 하나씩 나옴.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fae1f472-a6cb-4a43-84f6-752eda8d90a8/image.png" /></p>
<hr />
<h3 id="ls--l에서-두번째-나오는-숫자의-의미">ls -l에서 두번째 나오는 숫자의 의미</h3>
<p><code>ls -l</code>에서 두 번째 필드(<code>$2</code>)는 <strong>&quot;하드 링크(Hard Link)의 수&quot;</strong>임.</p>
<p>쉽게 말해, <strong>&quot;이 데이터(inode)를 가리키고 있는 이름표가 세상에 몇 개 붙어있나?&quot;</strong>를 뜻하는 숫자.</p>
<h4 id="1-일반-파일일-때-file">1. 일반 파일일 때 (File)</h4>
<ul>
<li><strong>기본값: 1</strong> (유일한 파일).</li>
<li><strong>의미:</strong> 파일 데이터에 접근하는 경로가 하나뿐임.</li>
<li><strong>숫자가 2 이상이라면?</strong><ul>
<li>누군가 <code>ln</code> 명령어(하드 링크)로 이 파일에 대한 <strong>&quot;바로가기(복제본 아님)&quot;</strong>를 하나 더 만든 상태.</li>
<li>이 경우, 파일 하나를 지워도 숫자가 1로 줄어들 뿐 <strong>데이터는 안 지워짐</strong>. 숫자가 <strong>0</strong>이 되어야 디스크에서 삭제됨.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/b913e780-1848-4246-9157-3f71b01ba2c4/image.png" /></li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9e8adcfd-3d78-46f9-9434-7adc57c6af26/image.png" /></p>
<h4 id="2-디렉터리폴더일-때-directory">2. 디렉터리(폴더)일 때 (Directory)</h4>
<ul>
<li><strong>기본값: 2</strong> (빈 폴더일 때).</li>
<li><strong>왜 2인가?</strong><ol>
<li>부모 폴더에 있는 <strong>내 이름</strong> (예: <code>/home/pi</code>)</li>
<li>내 폴더 안에 있는 <strong><code>.</code></strong> (자기 자신을 가리키는 점)</li>
</ol>
</li>
<li><strong>숫자가 늘어나는 원리:</strong><ul>
<li>이 폴더 안에 <strong>새 폴더(Sub-directory)</strong>를 만들 때마다 숫자가 <strong>1씩 증가</strong>함.</li>
<li>(새 폴더 안에 생기는 <strong><code>..</code></strong> (부모 가리킴) 때문).</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e0d42eaf-5db0-46f5-85f9-9ebb21c75bad/image.png" /></p>
<h4 id="3-활용">3. 활용</h4>
<p>디렉터리의 <code>$2</code> 숫자를 보면 <strong>&quot;이 안에 서브 폴더가 대충 몇 개 있는지&quot;</strong> <code>ls</code> 안 해보고도 알 수 있음.</p>
<ul>
<li><strong>공식:</strong> <code>링크 수 - 2</code> = <strong>서브 폴더(자식 폴더) 개수</strong></li>
</ul>
<hr />
<h3 id="sed를-사용해-파일-내-apple-단어를-orange로-일괄-치환하여-출력-soldnewg">sed를 사용해 파일 내 apple 단어를 orange로 일괄 치환하여 출력 (s/old/new/g)</h3>
<h4 id="1-화면에만-결과-출력-dry-run">1. 화면에만 결과 출력 (Dry Run)</h4>
<p>원본 파일은 건드리지 않고, <strong>&quot;바뀌면 어떻게 될지&quot;</strong> 미리보기만 함.</p>
<p>Bash</p>
<pre><code class="language-bash">sed 's/apple/orange/g' 파일명</code></pre>
<h4 id="2-원본-파일-덮어쓰기-i">2. 원본 파일 덮어쓰기 (<code>i</code>)</h4>
<p>확인 끝났으면 실제로 파일 내용을 변경해서 저장함.</p>
<p>Bash</p>
<pre><code class="language-bash">sed -i 's/apple/orange/g' 파일명</code></pre>
<ul>
<li><strong><code>i</code> (in-place):</strong> 파일을 직접 수정하라는 핵심 옵션.</li>
</ul>
<h4 id="구문-해부-soldnewg">구문 해부 (<code>s/old/new/g</code>)</h4>
<ul>
<li><strong><code>s</code> (Substitute):</strong> 치환 명령.</li>
<li><strong><code>g</code> (Global):</strong> 한 줄에 <code>apple</code>이 여러 번 나오면 <strong>몽땅</strong> 바꿈.<ul>
<li><strong>주의:</strong> <code>g</code>를 빼면 <strong>맨 처음 나온 <code>apple</code> 하나만</strong> 바뀌고 뒤에 건 안 바뀜.</li>
</ul>
</li>
</ul>
<h4 id="고수들의-디테일-b-경계">고수들의 디테일 (<code>\b</code> 경계)</h4>
<p>그냥 <code>apple</code>로 바꾸면 <strong><code>pineapple</code></strong>이 <strong><code>pineorange</code></strong>가 되는 대참사가 발생함.
정확히 단어 <code>apple</code>만 바꾸려면 <strong>단어 경계(Boundary)</strong>를 지정해야 함.</p>
<p>Bash</p>
<pre><code class="language-bash">sed -i 's/\bapple\b/orange/g' 파일명</code></pre>
<ul>
<li><strong><code>\b</code></strong>: 단어의 시작과 끝을 의미. (pine<strong>apple</strong> 같은 포함 단어는 제외됨).</li>
</ul>
<hr />
<ul>
<li>CSV 파일 같은 텍스트 데이터의 특정 열만 추출하기.</li>
</ul>