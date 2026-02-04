<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9f51db3e-823e-46d0-94f7-01a685231767/image.png" /></p>
<hr />
<h3 id="패키지-관리-apt-dpkg">패키지 관리 (apt, dpkg)</h3>
<ul>
<li>프로그램 설치/삭제/업데이트 원리, 의존성에 대해 확인</li>
<li><code>sudo apt update</code>와 <code>upgrade</code> 차이 이해 및 실행</li>
<li><code>sudo apt install [패키지명]</code>으로 <code>tree</code>, neofastfetch등 설치</li>
<li><code>dpkg -l</code>로 설치된 모든 패키지 리스트 확인 및 검색</li>
</ul>
<p><code>apt</code>는 <code>자동</code>(인터넷+의존성 해결), <code>dpkg</code>는 <code>수동</code>(파일 직접 설치) 도구입니다.</p>
<hr />
<h3 id="1-차이점">1. 차이점</h3>
<ul>
<li><code>apt</code> : 인터넷에서 다운로드 + 필요한 부속품(의존성)까지 알아서 설치됩니다.</li>
<li><code>dpkg</code> : 내가 가진 <code>.deb</code> 파일 하나만 강제로 설치합니다. (부속품 없으면 에러)</li>
</ul>
<h3 id="2-자주-쓰이는-명령어">2. 자주 쓰이는 명령어</h3>
<table>
<thead>
<tr>
<th>기능</th>
<th>명령어</th>
<th>비고</th>
</tr>
</thead>
<tbody><tr>
<td>설치 (.deb)</td>
<td><code>sudo dpkg -i 파일명.deb</code></td>
<td>install</td>
</tr>
<tr>
<td>목록 확인</td>
<td>`dpkg -l</td>
<td>grep 이름`</td>
</tr>
<tr>
<td>파일 주인 찾기</td>
<td><code>dpkg -S /bin/ls</code></td>
<td>Search (이 파일 어느 패키지 꺼?)</td>
</tr>
<tr>
<td>설치 위치 확인</td>
<td><code>dpkg -L 패키지명</code></td>
<td>List files (이 패키지 어디에 깔렸어?)</td>
</tr>
</tbody></table>
<h3 id="3-의존성-에러-해결">3. 의존성 에러 해결</h3>
<p><code>dpkg -i</code>로 설치하다가 &quot;의존성 에러(Dependency Error)&quot;가 뜨면 당황하지 말고 아래 명령 실행.</p>
<pre><code class="language-bash">sudo apt --fix-broken install // 의존성 문제 해결</code></pre>
<p>이후</p>
<pre><code class="language-bash">sudo apt autoremove // 불필요한 파일 제거</code></pre>