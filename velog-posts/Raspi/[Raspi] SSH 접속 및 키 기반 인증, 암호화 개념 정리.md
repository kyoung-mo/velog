<h2 id="ssh-개념">SSH 개념</h2>
<p>SSH(Secure Shell)의 동작 과정은 비대칭키(인증)와 대칭키(암호화)방식을 혼합하여 안전하게 통신 채널을 만들어 사용하는 방식이다.</p>
<hr />
<h3 id="1-접속-초기화-및-키-교환key-exchange">1. 접속 초기화 및 키 교환(Key Exchange)</h3>
<ul>
<li>클라이언트와 서버가 서로 지원하는 암호화 방식과 해시 알고리즘을 확인한다.</li>
<li>세션키 생성 시 디피-헬만(Diffie-Hellman) 알고리즘을 사용한다.
서로의 비밀키를 네트워크에 노출하지 않고, 양쪽이 동일한 공통 대칭키(세션 키)를 공유하게 된다.
이후 모든 데이터 전송은 이 세션 키로 암호화된다.</li>
</ul>
<h3 id="2-서버-인증server-authentication">2. 서버 인증(Server Authentication)</h3>
<ul>
<li>내가 접속하려는 서버가 진짜인지, 가짜 서버인지(해커 등에 의해) 확인하는 목적</li>
<li>과정<ul>
<li><ol>
<li>서버가 자신의 공개 호스트 키(Host Key)를 클라이언트에게 전송한다.</li>
</ol>
</li>
<li><ol start="2">
<li>클라이언트는 자신의 PC 내 <code>~/.ssh/known_hosts</code> 파일에 저장된 키와 비교한다.</li>
</ol>
</li>
<li><ol start="3">
<li>일치하면 &gt; 신뢰하고 진행한다.</li>
</ol>
</li>
<li><ol start="4">
<li>불일치하거나, 파일 내에 저장이 되어있지 않다면 &gt; 경고 메시지를 출력한다.
<code>&quot;Are you sure you want to continue connecting?&quot;</code></li>
</ol>
</li>
</ul>
</li>
</ul>
<h3 id="3-사용자-인증user-authentication">3. 사용자 인증(User Authentication)</h3>
<ul>
<li>서버가 클라이언트(사용자=WSL)의 접속 권한을 확인하는 목적</li>
<li>방식 A : 비밀번호(Password)<ul>
<li>이미 암호화된 터널을 통해 비밀번호를 전송하여 서버가 확인한다.</li>
</ul>
</li>
<li>방식 B : 키 페어(Key Pair)<ul>
<li>서버 : 임의의 문제(난수)를 생성해 등록된 사용자의 공개키로 암호화하여 보낸다.</li>
<li>-&gt; 클라이언트 : 자신의 개인키로 이를 복호화하여 정답을 보낸다.</li>
<li>-&gt; 서버 : 정답이 맞으면 접속을 허용한다. (개인 키가 네트워크를 건너지 않음)</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c9525775-2b9f-429a-895a-6b459404e3e1/image.png" /></p>
<h3 id="4-데이터-암호화data-transfer">4. 데이터 암호화(Data Transfer)</h3>
<ul>
<li>터널링 : 인증이 끝나면 쉘 명령어나 파일 전송을 시작</li>
<li>대칭키 사용 : 1번 단계에서 만든 세션 키(대칭키)를 사용하여 데이터를 암호화/복호화<ul>
<li>비대칭키(RSA 등)는 연산이 느리기 때문이다.</li>
<li>대칭키(AES 등)가 훨씬 빨라서 데이터 전송에 유리하다.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="서버에서-보낸-공개키는-어디에-저장되는가">서버에서 보낸 공개키는 어디에 저장되는가?</h3>
<p>서버에서 전송받은 공개키(Host Key)는 클라이언트 컴퓨터의 <code>known_hosts</code> 라는 파일에 저장된다.
이 파일은 클라이언트가 &quot;내가 접속하려는 서버가 과거에 접속했던 그 서버가 맞는지&quot; 신원을 확인(Server Authentication 과정)하는 데 사용된다.</p>
<h3 id="운영체제별-저장-위치">운영체제별 저장 위치</h3>
<p>대부분의 운영체제에서 SSH 설정 폴더인 <code>.ssh</code> 디렉터리 내부에 위치한다.</p>
<ul>
<li><strong>Linux / macOS :</strong> <code>~/.ssh/known_hosts</code></li>
<li><strong>Windows (PowerShell/Cmd) :</strong> <code>C:\Users\사용자명\.ssh\known_hosts</code></li>
</ul>
<h3 id="저장-및-확인-과정">저장 및 확인 과정</h3>
<p>사용자가 SSH로 서버에 접속할 때 다음과 같은 순서로 처리가 이루어진다.</p>
<ol>
<li><strong>최초 접속 시:</strong><ul>
<li>클라이언트는 <code>known_hosts</code> 파일에 해당 서버의 정보가 있는지 찾는다.</li>
<li>정보가 없다면 사용자에게 &quot;이 서버의 지문(Fingerprint)을 신뢰하겠습니까?&quot;라고 묻습니다. 
(<code>Are you sure you want to continue connecting?</code>)</li>
<li>사용자가 <code>yes</code>를 입력하면, 서버의 <strong>공개키</strong>가 <code>known_hosts</code> 파일에 <strong>추가</strong>됩니다.</li>
</ul>
</li>
<li><strong>재접속 시:</strong><ul>
<li>클라이언트는 서버가 보내온 공개키와 <code>known_hosts</code>에 저장된 키를 비교합니다.</li>
<li><strong>일치하면:</strong> 안전한 서버로 판단하고 연결을 진행합니다.</li>
<li><strong>일치하지 않으면:</strong> 누군가 서버를 사칭하고 있을 가능성(Man-in-the-Middle 공격 등)이 있거나 
서버가 재설치된 경우이므로, <strong>강력한 경고 메시지</strong>(<code>WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!</code>)를 띄우고 접속을 차단합니다.</li>
</ul>
</li>
</ol>
<h3 id="주의-authorized_keys와의-차이점">주의: <code>authorized_keys</code>와의 차이점</h3>
<p>SSH를 사용할 때 가장 많이 혼동하는 두 파일의 차이점</p>
<table>
<thead>
<tr>
<th><strong>파일명</strong></th>
<th><strong>저장 위치</strong></th>
<th><strong>저장되는 키</strong></th>
<th><strong>목적</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong><code>known_hosts</code></strong></td>
<td><strong>클라이언트 PC</strong></td>
<td><strong>서버</strong>의 공개키</td>
<td>클라이언트가 <strong>서버를 인증</strong>하기 위함</td>
</tr>
<tr>
<td><code>authorized_keys</code></td>
<td><strong>서버 (원격지)</strong></td>
<td><strong>클라이언트</strong>의 공개키</td>
<td>서버가 <strong>접속하는 사용자(클라이언트)를 인증</strong>하기 위함 (비밀번호 없이 접속 등)</td>
</tr>
</tbody></table>
<hr />
<h2 id="비밀번호-없이-rasp-로그인">비밀번호 없이 rasp 로그인</h2>
<p>WSL에서 <code>ssh-keygen -t ed25519 -C &quot;my-rpi5-key&quot;</code> 입력
이 과정은 클라이언트(WSL)에 공개키, 개인키로 이루어진 SSH 키 페어를 생성하는 단계로,
생성된 개인키는 로컬에만 저장되며, 공개키만 서버에 등록된다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/79fff1fc-0cc7-4840-ba96-94baf303cfa4/image.png" /></p>
<p>이후 <code>ssh-copy-id pi@10.10.16.200(본인 IP)</code> 입력하여, 라즈베리파이에 대한 키 생성
이 명령은 클라이언트의 공개키를 라즈베리파이의 <code>~/.ssh/authorized_keys</code> 파일에 등록하여 해당 사용자(pi)에 대해 키 기반 인증을 허용하도록 설정하는 과정이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/91769558-ef38-46f3-8cc3-28b616798cd8/image.png" /></p>
<p><code>~</code> 위치에서 <code>ls-al</code> 명령어를 통해 <code>.ssh</code>가 생긴 것을 확인할 수 있다. 이후 ssh를 통해 raspberry pi5에 접속하면,</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c51cbf7f-1a68-4ac4-8b26-91f0d45d055c/image.png" /></p>
<p>서버가 공개키 기반 인증을 수행하므로, 비밀번호 입력 없이 자동으로 사용자 인증이 완료된다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/272d5a64-5ab0-45ff-936a-b4232c35590b/image.png" /></p>
<p>Raspberry Pi 측에서도 <code>.ssh</code> 디렉터리와 <code>authorized_keys</code> 파일이 생성된 것을 확인할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/05b23f2a-a6b0-45c4-8f0c-60df206d4cc7/image.png" /></p>