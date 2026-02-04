<h3 id="서비스-관리-systemctl">서비스 관리 (systemctl)</h3>
<ul>
<li>부팅 시 자동 실행(Enable), 서비스 시작/중</li>
<li><code>systemctl status ssh</code>로 SSH 데몬 상태 확인.</li>
<li>서비스 재시작(<code>restart</code>), 중지(<code>stop</code>), 시작(<code>start</code>).</li>
<li>부팅 시 자동 실행 끄기(<code>disable</code>) 및 켜기(<code>enable</code>) 테스트.</li>
</ul>
<hr />
<h3 id="systemctl-서비스되는-모든-리스트를-보기">systemctl 서비스되는 모든 리스트를 보기</h3>
<p>현재 시스템에 등록된 모든 서비스(켜진 것 + 꺼진 것 포함)를 보려면 아래 명령어를 사용합니다.</p>
<pre><code class="language-bash">systemctl list-units --type=service --all</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/601a8f37-59f9-44a3-93b2-47fc9fea1d17/image.png" /></p>
<hr />
<h3 id="1-옵션-설명">1. 옵션 설명</h3>
<ul>
<li><code>list-units</code>: 현재 메모리에 로드된 유닛들을 보여줘라.</li>
<li><code>-type=service</code>: 마운트나 소켓 같은 거 말고 오직 서비스(.service)만 보여줘라.</li>
<li><code>-all</code>: 가장 중요. 이걸 안 붙이면 <code>Active(실행 중)</code>인 것만 보여줍니다. 죽어있는(<code>inactive</code>) 서비스까지 다 보려면 필수입니다.</li>
</ul>
<hr />
<h3 id="2-상황-별-명령어">2. 상황 별 명령어</h3>
<hr />
<h3 id="a-부팅할-때-켜지는지enabled-확인하고-싶을-때">A. 부팅할 때 켜지는지(Enabled) 확인하고 싶을 때</h3>
<p>위의 <code>list-units</code>는 '현재 상태'를 보여주는 것이고, '설치된 서비스 목록과 부팅 설정'을 보려면 명령어가 다릅니다.</p>
<pre><code class="language-bash">systemctl list-unit-files --type=service</code></pre>
<p>뒤에 <code>-all</code> 인자를 안 붙이면 실행중인 서비스만 보입니다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/ec0c98dc-366b-4424-9a30-fce94a8c9cd9/image.png" /></p>
<ul>
<li>결과: <code>enabled</code> (부팅 시 자동 실행), <code>disabled</code> (수동 실행), <code>masked</code> (완전 차단) 여부가 나옵니다.</li>
</ul>
<h3 id="b-특정-서비스만-찾고-싶을-때-grep">B. 특정 서비스만 찾고 싶을 때 (<code>grep</code>)</h3>
<p>목록이 너무 기니까 파이프(<code>|</code>)와 <code>grep</code>을 섞어 쓰는 게 국룰입니다.</p>
<p>Bash</p>
<pre><code class="language-bash"># 이름에 'ssh'가 들어가는 서비스 찾기
systemctl list-units --type=service --all | grep ssh</code></pre>
<h3 id="3-화면-조작법">3. 화면 조작법</h3>
<p>명령어를 치면 화면이 <code>less</code> 모드(페이지 뷰어)로 바뀝니다.</p>
<ul>
<li>화살표 위/아래: 스크롤.</li>
<li><code>/</code> (슬래시): 검색 모드 (예: <code>/cron</code> 입력 후 엔터).</li>
<li><code>q</code>: 나가기.</li>
</ul>
<hr />
<h3 id="user1000service"><a href="mailto:user@1000.service">user@1000.service</a></h3>
<p>&quot;UID 1000번(주로 첫 번째 사용자)을 위한 '개인용 systemd 관리자'입니다.&quot;</p>
<p>리눅스 시스템 전체를 관리하는 <code>systemd</code>(PID 1)가 있고, 그 아래에서 특정 사용자만의 서비스를 따로 관리하기 위해 실행된 '새끼 systemd'라고 보시면 됩니다.</p>
<hr />
<h3 id="1-이름-해부-user1000service">1. 이름 해부 (<code>user@1000.service</code>)</h3>
<p><code>user@.service</code>: 템플릿 서비스입니다. 사용자가 로그인하면 시스템이 이 템플릿을 복사해서 실행합니다.
<code>1000</code>: UID (User ID)입니다.</p>
<ul>
<li>리눅스(라즈비안, 우분투 등)에서 처음 생성한 계정(예: <code>pi</code>)은 보통 1000번을 부여받습니다.</li>
<li>즉, <code>pi</code> 계정이 로그인해서 활동할 수 있도록 뒷받침하는 배경 서비스입니다.</li>
</ul>
<h3 id="2-이게-왜-필요한가-시스템-vs-유저">2. 이게 왜 필요한가? (시스템 vs 유저)</h3>
<p>과거에는 모든 서비스가 <code>root</code> 권한으로 시스템 전체에서 돌아갔지만, 최신 리눅스는 보안과 편의를 위해 영역을 분리합니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>systemd (시스템)</th>
<th>systemd (유저/user@1000)</th>
</tr>
</thead>
<tbody><tr>
<td>권한</td>
<td>Root (관리자)</td>
<td>User (일반 사용자)</td>
</tr>
<tr>
<td>명령어</td>
<td><code>sudo systemctl ...</code></td>
<td><code>systemctl --user ...</code></td>
</tr>
<tr>
<td>담당</td>
<td>웹서버, DB, SSH, 네트워크</td>
<td>사운드(PulseAudio/PipeWire), 화면보호기, 사용자 자동실행 스크립트</td>
</tr>
</tbody></table>
<h3 id="3-여기서-뭐가-돌아가고-있나">3. 여기서 뭐가 돌아가고 있나?</h3>
<p>사용자(UID 1000)가 로그인했을 때만 필요한 백그라운드 프로그램들이 이 안에서 돕니다.</p>
<pre><code class="language-bash">systemctl --user status</code></pre>
<ul>
<li>보통 소리(Sound) 관련 서비스나, 그놈(GNOME)/KDE 같은 데스크탑 환경의 설정들이 주렁주렁 매달려 있는 것을 볼 수 있습니다.</li>
</ul>
<h3 id="로그아웃해도-계속-돌게-하고-싶다면">로그아웃해도 계속 돌게 하고 싶다면?</h3>
<p>기본적으로 이 서비스(<code>user@1000.service</code>)는 사용자가 로그아웃하면 같이 꺼집니다.</p>
<p>만약 서버처럼 로그아웃 후에도 내 유저 서비스(예: 봇, 스크립트)가 계속 돌길 원한다면 <code>loginctl</code>로 설정을 바꿔야 합니다.</p>
<pre><code class="language-bash">sudo loginctl enable-linger 1000
# 1000번 유저는 로그아웃해도 systemd 인스턴스를 죽이지 마라 (Linger: 남아있다)</code></pre>