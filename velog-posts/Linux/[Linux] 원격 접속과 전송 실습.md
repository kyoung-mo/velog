<h3 id="원격-접속과-전송">원격 접속과 전송</h3>
<p>서버 관리의 기본 개념, 비밀번호 없이 접속하기(Key) 실습</p>
<ul>
<li><code>ssh user@ip</code>로 라즈베리 파이나 다른 PC 접속.</li>
<li><code>ssh-keygen</code>으로 키 생성 후 <code>ssh-copy-id</code>로 전송 (비번 없이 로그인).</li>
<li><code>scp</code>로 로컬 파일을 원격지로 전송 및 수신.</li>
</ul>
<hr />
<h3 id="scp-로-파일-폴더-복사하기">scp 로 파일, 폴더 복사하기</h3>
<ul>
<li><code>scp</code> (Secure Copy)는 SSH를 이용해 네트워크로 파일을 주고받는 명령어입니다.</li>
</ul>
<p>가장 중요한 공식은 <code>scp [보낼것] [받을곳]</code> 순서입니다.</p>
<ul>
<li><p>받을 ip 주소 확인 <code>ifconfig</code></p>
</li>
<li><p><code>sudo apt install net-tools</code> 를 통해 깔아줌</p>
</li>
<li><p>IP Address : 172.21.223.182 확인
<img alt="" src="https://velog.velcdn.com/images/mommers/post/9151e374-71bf-4fa4-b28d-afa1a941d8fb/image.png" /></p>
</li>
<li><p>파일을 받을 환경에서는 SSH 서버를 켜줘야 한다.</p>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7a55ce89-a418-47ab-8592-1d3d95327a18/image.png" /></p>
<pre><code class="language-bash">sudo apt install openssh-server
// 이후 /etc/ssh/sshd_config 수정
sudo nano /etc/ssh/sshd_config</code></pre>
<ol>
<li><code>Port 22</code> 주석해제</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fc1160cd-cf90-4455-951d-ce95dba1033c/image.png" /></p>
<ol start="2">
<li><p><code>PasswordAuthentication yes</code> 주석 해제 : 비밀번호 인증 허용
<img alt="" src="https://velog.velcdn.com/images/mommers/post/c7f0b1e6-c7e5-45ed-987f-3edcd91044eb/image.png" /></p>
</li>
<li><p><code>PermitRootLogin no</code> 추가 : root 로그인 금지
<img alt="" src="https://velog.velcdn.com/images/mommers/post/d2665055-2769-4709-8a38-83120256d631/image.png" /></p>
</li>
</ol>
<p>위 과정까지 다 끝냈다면</p>
<pre><code>sudo service ssh start    // ssh 키기
sudo service ssh status // 상태 확인</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/255e2aa2-fb6b-4e21-bf29-b6a17717c41f/image.png" /></p>
<hr />
<p><code>+ 방화벽 이슈 추가</code></p>
<p>⭐<code>Window PowerShell 관리자의 권한으로 실행</code> 이후 아래 명령어 입력</p>
<pre><code class="language-bash">New-NetFirewallRule -DisplayName &quot;WSL SSH&quot; -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow
// 이후 아래 내용으로 확인
Get-NetFirewallRule -DisplayName &quot;WSL SSH&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/225713bb-30a9-44e1-9aaf-7cb31f762cbb/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/67a0e045-27f9-400c-9310-3c6262224063/image.png" /></p>
<pre><code class="language-bash"># 기존 규칙 삭제
Remove-NetFirewallRule -DisplayName &quot;WSL SSH&quot;

# 모든 프로필에 대해 새로 추가
New-NetFirewallRule -DisplayName &quot;WSL SSH&quot; -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow -Profile Any

# 확인
Get-NetFirewallRule -DisplayName &quot;WSL SSH&quot; | Select-Object DisplayName,Enabled,Profile,Direction,Action</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2c073302-42df-444b-968b-1202b864b00c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0a708bc1-e2d3-4654-a186-89f8d0aa8c8a/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e5a17203-62ae-4e5b-8638-c992470cf524/image.png" /></p>
<pre><code class="language-bash">sudo service ssh restart
sudo service ssh status</code></pre>
<p>이제 test 용도로 raspi -&gt; wsl ssh 접속을 해보면</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8353cf56-77a4-4dbf-810e-413f8a461f2c/image.png" /></p>
<p>잘 되는것을 확인할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5bffd5c6-147c-4337-8d9d-a261c2d6edee/image.png" /></p>
<p>근데 여기서 또 막히네요.. 나중에 다시 정리</p>
<p>raspi -&gt; wsl 실패, wsl -&gt; raspi 정상 작동</p>
<hr />
<h3 id="1-내-컴퓨터-→-라즈베리-파이로-보내기-업로드">1. 내 컴퓨터 → 라즈베리 파이로 보내기 (업로드)</h3>
<h3 id="a-파일-하나-보낼-때">A. 파일 하나 보낼 때</h3>
<pre><code class="language-bash"># 사용법: scp [내파일] [계정]@[IP]:[저장할경로]
scp main.c pi@10.10.16.220:~/project/</code></pre>
<ul>
<li>주의: IP 뒤에 콜론(<code>:</code>)을 꼭 찍어야 합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/07777788-c20f-478d-a78b-73a706f030c7/image.png" /></p>
<h3 id="b-폴더-통째로-보낼-때--r">B. 폴더 통째로 보낼 때 (<code>-r</code>)</h3>
<p>폴더는 그냥 보내면 에러 납니다. <code>-r</code> (recursive) 옵션이 필수입니다.</p>
<p>Bash</p>
<pre><code class="language-bash"># my_code 폴더를 통째로 전송
scp -r my_code pi@10.10.16.220:~/</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6168d7ef-d1c9-4bdd-93ed-85f6ee142014/image.png" /></p>
<hr />
<h3 id="2-라즈베리-파이-→-내-컴퓨터로-가져오기-다운로드">2. 라즈베리 파이 → 내 컴퓨터로 가져오기 (다운로드)</h3>
<p>순서만 바꾸면 됩니다. [서버에있는파일] [내위치]</p>
<h3 id="a-파일-가져오기">A. 파일 가져오기</h3>
<pre><code class="language-bash"># 사용법: scp [계정]@[IP]:[파일경로] [내컴퓨터저장위치]
scp pi@10.10.16.220:~/log.txt .</code></pre>
<ul>
<li>마지막 점(<code>.</code>): &quot;현재 내 터미널 위치에 저장해라&quot;라는 뜻입니다. (이거 안 쓰면 에러 남).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2e76327a-3063-42e6-bd33-ed06ffcbb110/image.png" /></p>
<h3 id="b-폴더-가져오기">B. 폴더 가져오기</h3>
<pre><code class="language-bash">scp -r pi@10.10.16.220:~/logs .</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5a979d0e-5378-472d-bced-0f62bbf1adb7/image.png" /></p>
<hr />
<h3 id="3-자주-틀리는-옵션-대소문자-주의">3. 자주 틀리는 옵션 (대소문자 주의)</h3>
<table>
<thead>
<tr>
<th>옵션</th>
<th>설명</th>
<th>주의사항</th>
</tr>
</thead>
<tbody><tr>
<td><code>-r</code></td>
<td>폴더 복사</td>
<td>소문자 r. 이거 없으면 &quot;not a regular file&quot; 에러 뜸</td>
</tr>
<tr>
<td><code>-P</code></td>
<td>포트 지정</td>
<td>대문자 P. SSH 포트가 22번이 아닐 때 사용. (ssh 명령어는 소문자 <code>-p</code>라서 헷갈림 주의)</td>
</tr>
</tbody></table>
<p>예시 (포트가 2222번일 때):</p>
<pre><code class="language-bash">scp -P 2222 main.c pi@10.10.16.200:~/</code></pre>