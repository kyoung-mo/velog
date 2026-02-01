<p><del>썸넬</del>
<img alt="" src="https://velog.velcdn.com/images/mommers/post/60c2eea2-34b4-4d9e-a88d-75ca74607069/image.png" /></p>
<hr />
<h3 id="1-권한-설정-chmod">1. 권한 설정 (chmod)</h3>
<ul>
<li><strong>학습:</strong> <code>rwx</code> (읽기/쓰기/실행) 의미. 8진수(755, 644) 표기법.</li>
<li><strong>실습:</strong><ul>
<li>스크립트 파일 생성 후 <code>chmod +x</code>로 실행 권한 부여 전후 비교.</li>
<li><code>ls -al</code> 로 파일 별 설정되어있는 권한 확인 가능.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="chmod-777--보안-자살-행위"><code>chmod 777</code> = 보안 자살 행위</h3>
<p>집 현관문을 뜯어내고 &quot;누구나 들어와서 자고 가도 됨&quot;이라고 써 붙이는 것과 동일하다..
<strong>읽기(4) + 쓰기(2) + 실행(1)</strong> 모든 권한을 <strong>모두(User, Group, Others)</strong>에게 부여하는 최악의 설정이니 사용 시 주의할 것.</p>
<blockquote>
<p>다시 한번.. <code>읽기(4) + 쓰기(2) + 실행(1)</code></p>
</blockquote>
<h4 id="3대-치명적-위험">3대 치명적 위험</h4>
<ol>
<li><strong>서버 탈취 (웹쉘 공격):</strong><ul>
<li>웹 서버 업로드 폴더가 777이면, 해커가 악성 스크립트(웹쉘)를 <strong>업로드(Write)</strong>하고 즉시 <strong>실행(Execute)</strong> 가능.</li>
<li>결과: 서버 관리자 권한 뺏김.</li>
</ul>
</li>
<li><strong>데이터 증발:</strong><ul>
<li>로그인 가능한 아무나(Others) 시스템 설정 파일이나 DB 파일을 삭제/변조 가능.</li>
</ul>
</li>
<li><strong>서비스 실행 거부 (Self-Defense):</strong><ul>
<li>보안이 생명인 서비스(SSH, DB 등)는 중요 파일(예: <code>id_rsa</code>, <code>my.cnf</code>) 권한이 777이면 <strong>&quot;위험하다&quot;고 판단해 실행 자체를 거부</strong>함.</li>
</ul>
</li>
</ol>
<h4 id="정석-해결법">정석 해결법</h4>
<p>권한 오류 뜬다고 무지성 777 금지. 학부 연구생 때 권한 오류 뜬다고 chown 777 했다가 교수님께 혼났다. <del>그때는 뭐가 문제인지 잘 몰랐다.</del> 아래 규칙 준수할 것.</p>
<ul>
<li><strong>폴더(Directory):</strong> <code>755</code> (나만 쓰기, 남은 들어오기만 가능)</li>
<li><strong>파일(File):</strong> <code>644</code> (나만 쓰기, 남은 읽기만 가능)</li>
<li><strong>실행 스크립트:</strong> <code>755</code></li>
<li><strong>그래도 안 되면:</strong> <code>chmod</code>가 아니라 *<em><code>chown</code></em>으로 소유자를 변경하는 것이 정답.</li>
</ul>
<hr />
<ul>
<li><code>chmod 600</code> (나만 읽기/쓰기) 설정 후 다른 사용자로 접근 시도해보기 (Permission denied 유도).</li>
</ul>
<hr />
<h3 id="2-소유권-관리-chown-chgrp">2. 소유권 관리 (chown, chgrp)</h3>
<ul>
<li><strong>학습:</strong> User와 Group의 개념. Root의 권한.</li>
<li><strong>실습:</strong><ul>
<li><code>sudo touch</code>로 루트 소유 파일 생성 후, 내 계정으로 소유권 가져오기(<code>chown user:user</code>).</li>
<li><code>R</code> 옵션으로 디렉터리 하위 모든 파일 소유권 한 번에 변경.</li>
</ul>
</li>
</ul>
<hr />
<p><strong><code>/etc/passwd</code></strong>와 <strong><code>/etc/group</code></strong>.</p>
<p>이 두 파일을 열어보면 모든 사용자와 그룹의 ID 정보를 원본 그대로 확인할 수 있음.</p>
<h4 id="사용자-정보--주-그룹-gid-확인-etcpasswd">사용자 정보 &amp; 주 그룹 (GID) 확인: <code>/etc/passwd</code></h4>
<p>사용자의 <strong>UID(User ID)</strong>와 <strong>기본 그룹(Primary GID)</strong>을 확인하는 파일.</p>
<ul>
<li><strong>명령어:</strong> <code>cat /etc/passwd</code></li>
<li><strong>형식:</strong> <code>사용자명:암호:UID:GID:설명:홈디렉터리:쉘</code></li>
<li><strong>예시:</strong> <code>ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash</code><ul>
<li><strong>1000 (첫 번째 숫자):</strong> UID (내 아이디 번호)</li>
<li><strong>1000 (두 번째 숫자):</strong> GID (내가 속한 메인 그룹 번호)</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/37460bc8-f243-4d1c-a940-6dc4af31dac8/image.png" /></p>
<h4 id="그룹-상세--보조-그룹-확인-etcgroup">그룹 상세 &amp; 보조 그룹 확인: <code>/etc/group</code></h4>
<p>그룹의 이름과 <strong>GID</strong>, 그리고 해당 그룹에 속한 <strong>멤버 목록</strong>을 확인하는 파일.</p>
<ul>
<li><strong>명령어:</strong> <code>cat /etc/group</code></li>
<li><strong>형식:</strong> <code>그룹명:암호:GID:멤버리스트</code></li>
<li><strong>예시:</strong> <code>sudo:x:27:ubuntu,pi</code><ul>
<li><strong>sudo:</strong> 그룹 이름</li>
<li><strong>27:</strong> GID (그룹 번호)</li>
<li><strong>ubuntu,pi:</strong> 이 그룹에 포함된 사용자들 (보조 그룹)</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/01d7e901-f32c-4ff7-a28e-c6db98793624/image.png" /></p>
<h3 id="쉬운-확인법-명령어">쉬운 확인법 (명령어)</h3>
<p>파일을 눈으로 읽기 힘들다면 그냥 <code>id</code> 명령어를 치는 것이 제일 빠름.</p>
<p>Bash</p>
<pre><code class="language-c">id          # 내 정보 확인
id pi   # 특정 사용자 정보 확인</code></pre>
<ul>
<li><strong>출력:</strong> <code>uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),4(adm),24(cdrom)...</code></li>
<li><strong>해석:</strong> 현재 내 UID, 기본 GID, 그리고 속해 있는 모든 그룹(groups)을 한눈에 보여줌.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0ee560d6-74a1-4e32-ad0e-9f92751b31bd/image.png" /></p>
<p>group id는 잘 기억해야한다.. </p>
<hr />
<h3 id="id-groups이-있는-파일을-수정해도-되나">id, groups이 있는 파일을 수정해도 되나?</h3>
<p><strong>가능은 하지만, &quot;시스템 자폭 버튼&quot;을 누르는 것과 같음. 절대 권장하지 않음.</strong></p>
<p>단순 텍스트 파일처럼 보이지만, 리눅스 시스템의 <strong>척추</strong>에 해당함. <code>vi</code>나 <code>nano</code>로 직접 열어서 수정하면 발생하는 치명적 문제점과 안전한 대안을 정리함.</p>
<h3 id="1-직접-수정하면-안-되는-이유-3대-위험">1. 직접 수정하면 안 되는 이유 (3대 위험)</h3>
<ol>
<li><strong>문법 오류 = 부팅/로그인 불가</strong><ul>
<li>파일 형식이 매우 엄격함 (<code>user:x:1000:...</code>).</li>
<li>실수로 콜론(<code>:</code>) 하나를 지우거나 오타를 낸 상태로 저장하면, <strong>즉시 모든 사용자의 로그인이 막히거나 부팅 중 시스템이 멈춤.</strong> (복구하려면 싱글 유저 모드로 들어가야 하는 대공사 발생).</li>
</ul>
</li>
<li><strong>파일 간 불일치 (Sync 깨짐)</strong><ul>
<li>사용자 정보는 <code>/etc/passwd</code>에만 있는 게 아님.</li>
<li>비밀번호는 <strong><code>/etc/shadow</code></strong>, 그룹 비밀번호는 *<em><code>/etc/gshadow</code></em>에 분산 저장됨.</li>
<li>직접 수정하면 이 파일들 간의 연결 고리(Mapping)가 깨져서 계정이 꼬임.</li>
</ul>
</li>
<li><strong>파일 잠금(Locking) 부재</strong><ul>
<li><code>vi</code>로 열고 있는 동안 시스템이 계정 정보를 업데이트하려 하면 충돌 발생. 데이터 손실 가능성 있음.</li>
</ul>
</li>
</ol>
<h3 id="2-정석-해결법-전용-명령어-사용">2. 정석 해결법: 전용 명령어 사용</h3>
<p>리눅스는 안전하게 수정하라고 전용 도구를 만들어 둠. 이걸 쓰는 것이 <strong>국룰</strong>.</p>
<ul>
<li><strong>ID 변경:</strong> <code>usermod -u [새UID] [사용자명]</code></li>
<li><strong>그룹 변경:</strong> <code>groupmod -g [새GID] [그룹명]</code></li>
<li><strong>그룹 추가:</strong> <code>usermod -aG [그룹명] [사용자명]</code> </li>
<li><blockquote>
<p>많이 사용하는 편</p>
</blockquote>
</li>
<li><strong>장점:</strong> <code>/etc/shadow</code>, 홈 디렉터리 권한, 관련 그룹 정보까지 <strong>알아서 싹 다 맞춰줌.</strong></li>
</ul>
<hr />
<p>사용자 아이디(이름) 자체를  pi 에서 <code>andrew</code>로 바꾸려면 <strong><code>-l</code> (Login name)</strong> 옵션을 써야 함. 또한, 이름만 바꾸면 홈 디렉터리 이름은 그대로 남으므로 <strong>홈 디렉터리도 같이 이동</strong>시켜야 완벽함.</p>
<h3 id="필수-전제-조건">필수 전제 조건</h3>
<p><strong>로그인 중인 계정은 이름을 바꿀 수 없음.</strong><code>pi</code> 계정을 수정하려면, <code>pi</code>에서 로그아웃하고 <strong><code>root</code></strong>나 <strong>다른 관리자 계정</strong>으로 로그인해야 함.</p>
<hr />
<h3 id="만약-진짜-u를-쓰고-싶다면">만약 진짜 u를 쓰고 싶다면?</h3>
<p>진짜로 <strong>UID(식별 번호)</strong>를 바꾸고 싶은 경우라면 아래처럼 사용함.</p>
<p>Bash</p>
<pre><code class="language-bash">sudo usermod -u 2000 andrew</code></pre>
<ul>
<li>결과: <code>andrew</code>의 내부 ID 번호가 1000번에서 2000번으로 바뀜. (파일 소유권 문제 생길 수 있어 주의 필요).</li>
</ul>
<hr />
<p>라즈베리 파이의 Root 계정은 기본적으로 <strong>잠겨 있음(Locked)</strong>. (비밀번호가 없어서 로그인 불가).</p>
<p>상황에 따라 두 가지 방법이 있음.</p>
<h3 id="1-터미널에서-잠시-root-권한만-얻기-가장-권장"><strong>1. 터미널에서 잠시 Root 권한만 얻기 (가장 권장)</strong></h3>
<p>현재 계정(pi)에서 Root 쉘로 전환만 하는 방법. 가장 안전함.</p>
<p><strong>Bash</strong></p>
<pre><code class="language-bash">sudo -i</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7dd2123e-c8dd-47ef-8ef5-3cd3c37851df/image.png" /></p>
<ul>
<li><strong>결과:</strong> 프롬프트가 <code>$</code>에서 <code>#</code>으로 바뀌며 Root 권한 획득.</li>
<li><strong>복귀:</strong> <code>exit</code> 입력하면 원래 계정으로 돌아옴.</li>
</ul>
<hr />
<h3 id="2-진짜-root-계정-활성화-비밀번호-설정"><strong>2. 진짜 Root 계정 활성화 (비밀번호 설정)</strong></h3>
<p>로그인 화면에서 ID에 <code>root</code>를 입력하고 싶다면 비밀번호를 만들어야 함.</p>
<p><strong>Bash</strong></p>
<pre><code class="language-bash">sudo passwd root</code></pre>
<ul>
<li>새 비밀번호를 두 번 입력하면 <strong>활성화 완료</strong>.</li>
<li>이제 모니터(HDMI)나 시리얼 연결 시 <code>root</code>로 로그인 가능.</li>
</ul>
<hr />
<h3 id="3-ssh원격에서도-root-로그인-허용하기"><strong>3. SSH(원격)에서도 Root 로그인 허용하기</strong></h3>
<p>위 2번을 해도 <strong>SSH 접속은 기본적으로 차단</strong>되어 있음. 설정 파일을 고쳐야 함.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/02fb97f4-8041-401d-b312-17eab4843a14/image.png" /></p>
<ul>
<li>비밀번호를 설정해도 <code>/etc/ssh/sshd_config</code> 파일에서 설정이 안되어있기 때문에 비밀번호를 입력해도 접속이 안되는 모습</li>
</ul>
<ol>
<li><p><strong>설정 파일 열기:</strong></p>
<p> <strong>Bash</strong></p>
<pre><code class="language-bash"> sudo vi /etc/ssh/sshd_config</code></pre>
</li>
</ol>
<ol start="2">
<li><p><strong>내용 수정:</strong></p>
<ul>
<li><p><code>PermitRootLogin</code> 항목을 찾음 (보통 주석 <code>#</code> 처리 되어 있음).</p>
</li>
<li><p>주석을 풀고 값을 <code>yes</code>로 변경.</p>
</li>
<li><p><em>Ini, TOML*</em></p>
<pre><code class="language-bash">#PermitRootLogin prohibit-password

PermitRootLogin yes</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3446992c-0fb1-4b32-a2c9-534f152b26d4/image.png" /></p>
</li>
</ul>
</li>
<li><p><strong>SSH 재시작:</strong></p>
<p> <strong>Bash</strong></p>
<pre><code class="language-bash"> sudo systemctl restart ssh</code></pre>
<p> <img alt="" src="https://velog.velcdn.com/images/mommers/post/3d5ffd98-4220-430f-8f45-726a03269df0/image.png" /></p>
</li>
</ol>
<h3 id="⚠️-보안-경고"><strong>⚠️ 보안 경고</strong></h3>
<p>Root 계정 원격 접속 허용은 <strong>해킹 1순위 타겟</strong>이 됨.
가능하면 <strong>1번 방법(<code>sudo -i</code>)</strong>을 사용하고, 외부 인터넷에 연결된 기기라면 3번은 절대 하지 말 것.</p>
<hr />
<p><code>root</code> 계정을 다시 잠그려면 <strong>비밀번호를 잠금(Lock)</strong> 상태로 만들면 됩니다.</p>
<h3 id="1-계정-잠그기-명령어-한-줄">1. 계정 잠그기 (명령어 한 줄)</h3>
<p>터미널에 아래 명령어를 입력하세요.</p>
<p>Bash</p>
<pre><code class="language-bash">sudo passwd -l root</code></pre>
<ul>
<li><strong><code>l</code> (Lock):</strong> 비밀번호를 무효화하여 잠급니다.</li>
<li><strong>결과:</strong> 이제 로그인 화면이나 터미널에서 <code>root</code>로 로그인이 거부됩니다.</li>
<li><strong>참고:</strong> <code>sudo -i</code>를 통한 루트 권한 획득은 여전히 <strong>가능</strong>합니다 (이건 관리자 기능이라 정상임).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c0e2e506-4876-4ca2-a158-59a31c1889a9/image.png" /></p>
<hr />
<h3 id="2-ssh-설정-되돌리기-수정했다면-필수">2. SSH 설정 되돌리기 (수정했다면 필수)</h3>
<p>만약 아까 <code>/etc/ssh/sshd_config</code>에서 원격 접속을 허용(<code>yes</code>)했다면, 다시 막아야 안전합니다.</p>
<ol>
<li><p><strong>파일 열기:</strong>Bash</p>
<pre><code class="language-bash"> sudo vi /etc/ssh/sshd_config</code></pre>
</li>
<li><p><strong>수정:</strong></p>
<ul>
<li><code>PermitRootLogin yes</code> → <strong><code>PermitRootLogin prohibit-password</code></strong> (또는 <code>no</code>)로 변경.</li>
<li>혹은 해당 줄 맨 앞에 <code>#</code>을 붙여서 주석 처리 (기본값으로 돌아감).</li>
</ul>
</li>
<li><p><strong>적용:</strong>Bash</p>
<pre><code class="language-bash"> sudo systemctl restart ssh</code></pre>
<p> <img alt="" src="https://velog.velcdn.com/images/mommers/post/055eed30-2bff-469b-b19e-2e5753e02441/image.png" /></p>
</li>
</ol>
<p>다시 원상복구 해놨다.</p>
<hr />
<p>두 가지 방법이 있음. <strong><code>adduser</code></strong>를 쓰는 것이 훨씬 편하고 강력함.</p>
<h3 id="1-쉬운-방법-adduser-추천">1. 쉬운 방법: <code>adduser</code> (추천)</h3>
<p>우분투/라즈베리 파이 같은 데비안 계열에서 쓰는 대화형 명령어. <strong>알아서 홈 폴더 만들고, 쉘 설정하고, 비밀번호까지 물어봐줌.</strong></p>
<p>Bash</p>
<pre><code class="language-bash">sudo adduser [새사용자명]</code></pre>
<ul>
<li><strong>동작:</strong> <code>/home/[새사용자명]</code> 자동 생성 + 기본 설정 파일(<code>.bashrc</code> 등) 자동 복사.</li>
<li><strong>장점:</strong> 그냥 시키는 대로 입력만 하면 끝남.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/94d77cf8-034a-43f5-b63d-3ad6f89dc203/image.png" /></p>
<hr />
<h3 id="2-정석-방법-useradd--m-옵션-필수">2. 정석 방법: <code>useradd -m</code> (옵션 필수)</h3>
<p>리눅스 표준 명령어. 옵션 없이 쓰면 홈 폴더를 <strong>안 만듦</strong>. 반드시 <strong><code>-m</code></strong> 옵션을 붙여야 함.</p>
<p>Bash</p>
<pre><code class="language-bash">sudo useradd -m [새사용자명]</code></pre>
<ul>
<li><strong><code>m</code> (Make home):</strong> 홈 디렉터리를 생성하라는 옵션.</li>
<li><strong>주의:</strong> 이 명령어는 비밀번호를 안 물어봄. 생성 후 <code>sudo passwd [새사용자명]</code>으로 비번을 따로 설정해줘야 함.</li>
</ul>
<p><img alt="업로드중.." src="blob:https://velog.io/d07849f8-6b81-4c80-8bbc-ae9307d3cf73" /></p>
<h3 id="요약">요약</h3>
<ul>
<li><strong>사람이 할 때:</strong> <code>sudo adduser newuser</code> (편함)</li>
<li><strong>스크립트 짤 때:</strong> <code>sudo useradd -m newuser</code> (깔끔함)</li>
</ul>