<h3 id="백그라운드-작업-jobs-bg-fg-nohup">백그라운드 작업 (jobs, bg, fg, nohup)</h3>
<ul>
<li><strong>학습:</strong> 멀티태스킹. 터미널 꺼도 돌아가게 하기.</li>
<li><strong>실습:</strong><ul>
<li>프로그램 실행 중 sleep 100 <code>Ctrl+Z</code>로 멈추고 <code>bg</code>로 백그라운드 보내기.</li>
<li><code>jobs</code> 목록 확인 후 <code>fg</code>로 다시 불러오기.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="nohup-my_script--실행-후-터미널-끄고-다시-접속해서-프로세스-살아있는지-확인">nohup ./my_script &amp; 실행 후 터미널 끄고 다시 접속해서 프로세스 살아있는지 확인</h3>
<p><strong>의미:</strong>
터미널을 끄거나 로그아웃해도 <strong>죽지 않고 백그라운드에서 계속 실행</strong>하라는 명령어. 서버 개발자의 필수품임.</p>
<h3 id="1-명령어-해부">1. 명령어 해부</h3>
<ul>
<li><strong><code>nohup</code> (No Hang Up):</strong> &quot;전화 끊지 마&quot;라는 뜻. 터미널 연결이 끊겨도(로그아웃) 프로세스가 종료 시그널(HUP)을 무시하게 만듦.</li>
<li><strong><code>&amp;</code> (Ampersand):</strong> 프로세스를 <strong>백그라운드(뒷단)</strong>로 보내서, 터미널을 계속 쓸 수 있게 함.</li>
</ul>
<h3 id="2-실행-결과-자동-저장">2. 실행 결과 (자동 저장)</h3>
<ul>
<li>화면에 나올 출력 내용이 *<em><code>nohup.out</code></em>이라는 파일에 자동으로 저장됨.</li>
<li>(별도로 리다이렉션을 지정하지 않았을 경우).</li>
</ul>
<h3 id="3-더-깔끔한-실전-예제">3. 더 깔끔한 실전 예제</h3>
<p><code>nohup.out</code> 파일이 계속 커지면 디스크가 꽉 찰 수 있음. 로그를 관리하거나 버리는 것이 좋음.</p>
<pre><code class="language-bash"># 테스트 스크립트 생성
cat &gt; my_script.sh &lt;&lt; 'EOF'
#!/bin/bash
while true; do
    echo &quot;Running at $(date)&quot;
    sleep 5
done
EOF

# 실행 권한 부여
chmod +x my_script.sh

# 확인
ls -l my_script.sh</code></pre>
<p><strong>로그를 버리고 싶을 때</strong></p>
<p>Bash</p>
<pre><code class="language-bash">nohup ./my_script.sh &gt; /dev/null 2&gt;&amp;1 &amp;
ps -ef | grep my_script | grep -v grep</code></pre>
<ul>
<li>설명: 아무것도 기록하지 않고 조용히 실행만 함.</li>
</ul>
<h3 id="4-종료하는-법">4. 종료하는 법</h3>
<p>터미널을 껐다 켜면 <code>jobs</code> 명령어로 안 보일 수 있음. 직접 찾아서 죽여야 함.</p>
<p>Bash</p>
<pre><code class="language-bash">ps -ef | grep my_script | grep -v grep
kill -9 [PID]</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f16a557e-5144-4782-830b-2bd12e7fc729/image.png" /></p>
<hr />
<h3 id="ptso">pts/o</h3>
<p><strong><code>pts/0</code> = 가상 터미널 (Pseudo Terminal Slave) 0번</strong></p>
<p>물리적인 모니터 앞에 앉은 것이 아니라, <strong>SSH(원격)</strong>로 접속했거나 <strong>GUI 환경의 터미널 창</strong>을 띄웠다는 뜻임.</p>
<h3 id="1-해부">1. 해부</h3>
<ul>
<li><strong><code>pts</code> (Pseudo Terminal Slave):</strong> 가짜(가상) 터미널. 실제 하드웨어 장치가 아니라 커널이 소프트웨어적으로 만들어준 터미널 인터페이스.</li>
<li><strong><code>/0</code> (Number):</strong> 접속 순서 번호.<ul>
<li>가장 먼저 접속한 창이 <code>0</code>.</li>
<li>터미널을 하나 더 띄우거나 다른 사람이 들어오면 <code>pts/1</code>, <code>pts/2</code>로 늘어남.</li>
</ul>
</li>
</ul>
<h3 id="2-비교-tty-vs-pts">2. 비교: TTY vs PTS</h3>
<p>리눅스 서버 관리 시 이 둘을 구분하는 게 중요함.</p>
<table>
<thead>
<tr>
<th><strong>구분</strong></th>
<th><strong>이름</strong></th>
<th><strong>설명</strong></th>
<th><strong>상황</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>물리 터미널</strong></td>
<td><strong>tty</strong> (1~6)</td>
<td><strong>TeleTYpewriter.</strong> 서버 본체에 키보드/모니터를 직접 꽂고 쓰는 곳.</td>
<td>데이터센터 현장 작업, 부팅 복구 시. (<code>Ctrl</code>+<code>Alt</code>+<code>F1</code>~<code>F6</code>)</td>
</tr>
<tr>
<td><strong>가상 터미널</strong></td>
<td><strong>pts</strong> (0~N)</td>
<td><strong>Pseudo Terminal.</strong> 네트워크나 윈도우 창을 통해 연결된 가상의 통로.</td>
<td><strong>SSH 접속</strong>, Xshell, Putty, VS Code 터미널 등 99%의 상황.</td>
</tr>
</tbody></table>
<h3 id="3-내-터미널-확인법">3. 내 터미널 확인법</h3>
<p>지금 내가 쓰고 있는 창이 몇 번인지 알고 싶다면:</p>
<p>Bash</p>
<pre><code class="language-bash">tty
# 결과: /dev/pts/0  (나는 0번방에 있구나)</code></pre>
<p>또는 누가 들어와 있는지 전체 확인:</p>
<p>Bash</p>
<pre><code class="language-bash">who
# 결과:
# pi      tty1         Jan 29 09:00  (본체에 로그인한 사람)
# pi      pts/0        Jan 29 21:10  (SSH로 들어온 나)</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6decfb0f-cc5e-4993-ac22-a11aeff4e0a4/image.png" /></p>
<hr />