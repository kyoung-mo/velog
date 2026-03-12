<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4b9ec4ad-2320-4ebd-9a14-d8f64cb5ccf2/image.png" /></p>
<h1 id="putty-정리-ssh-접속-도구">PuTTY 정리 (SSH 접속 도구)</h1>
<h2 id="1-putty란-무엇인가">1. PuTTY란 무엇인가</h2>
<p><strong>PuTTY</strong>는 Windows 환경에서 가장 널리 사용되는 <strong>SSH 클라이언트
프로그램</strong>이다.
원격 서버에 접속하여 터미널을 통해 명령어를 실행할 수 있도록 해주는 도구이며, 주로 다음과 같은 환경에서 많이 사용된다.</p>
<ul>
<li>Linux 서버 원격 접속</li>
<li>Raspberry Pi 원격 제어</li>
<li>네트워크 장비 관리</li>
<li>개발 서버 관리</li>
</ul>
<p>PuTTY는 가볍고 설치가 간단하며 SSH 뿐 아니라 여러 네트워크 프로토콜을 지원한다.</p>
<h3 id="지원-프로토콜">지원 프로토콜</h3>
<ul>
<li>SSH (Secure Shell)</li>
<li>Telnet</li>
<li>Serial</li>
<li>Rlogin</li>
<li>Raw TCP</li>
</ul>
<p>특히 <strong>SSH 접속용으로 가장 많이 사용되는 프로그램</strong>이다.</p>
<hr />
<h1 id="2-putty-설치-시-함께-설치되는-프로그램">2. PuTTY 설치 시 함께 설치되는 프로그램</h1>
<p>PuTTY를 설치하면 SSH 접속 프로그램 외에도 여러 유용한 도구들이 함께
설치된다. 대표적으로 다음 프로그램들을 자주 사용한다.</p>
<hr />
<h2 id="21-putty">2.1 PuTTY</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ed760daf-ba69-41b0-b2ff-b641abdfe34a/image.png" /></p>
<p>PuTTY 패키지의 <strong>메인 프로그램</strong>이다.</p>
<p>주요 기능</p>
<ul>
<li>SSH 원격 접속</li>
<li>Telnet 접속</li>
<li>Serial 통신 접속</li>
<li>접속 세션 저장</li>
<li>키 기반 인증 사용 가능</li>
</ul>
<p>예시</p>
<pre><code>Host Name: 192.168.0.10
Port: 22
Connection type: SSH</code></pre><p>위와 같이 입력하면 해당 서버로 SSH 접속이 가능하다.</p>
<hr />
<h2 id="22-psftp">2.2 PSFTP</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/df4037f9-077a-48e7-9d7d-2b51812829f4/image.png" /></p>
<p><strong>PSFTP (PuTTY Secure File Transfer Protocol)</strong> 은 SSH 기반 파일 전송
프로그램이다.</p>
<p>쉽게 말해 <strong>SFTP 클라이언트</strong>이다.</p>
<p>기능</p>
<ul>
<li>서버 ↔ 로컬 파일 업로드/다운로드</li>
<li>SSH 기반 안전한 파일 전송</li>
</ul>
<p>사용 예시</p>
<pre><code>psftp user@192.168.0.10</code></pre><p>접속 후 사용 가능한 명령어</p>
<pre><code>put file.txt
get file.txt
ls
cd</code></pre><p>즉, <strong>SSH 환경에서 FTP처럼 파일을 전송할 수 있는 도구</strong>이다.</p>
<hr />
<h2 id="23-puttygen">2.3 PuTTYgen</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a162b720-c322-4c50-9e8c-1b12fe5de380/image.png" /></p>
<p><strong>PuTTYgen</strong>은 SSH 접속에 사용하는 <strong>키 생성 프로그램</strong>이다.</p>
<p>SSH 접속 방식에는 두 가지가 있다.</p>
<p>1️⃣ 비밀번호 인증
2️⃣ 공개키 인증 (Public Key Authentication)</p>
<p>PuTTYgen은 <strong>공개키 / 개인키 쌍을 생성하는 도구</strong>이다.</p>
<p>사용 목적</p>
<ul>
<li>서버 SSH 키 생성</li>
<li>GitHub SSH 키 생성</li>
<li>비밀번호 없이 서버 접속</li>
</ul>
<p>생성되는 키</p>
<ul>
<li>Private Key (.ppk)</li>
<li>Public Key</li>
</ul>
<p>보안성이 높아 <strong>서버 운영 시 매우 많이 사용된다.</strong></p>
<hr />
<h2 id="24-pageant">2.4 Pageant</h2>
<p><strong>Pageant</strong>는 PuTTY의 <strong>SSH 키 관리 프로그램</strong>이다.</p>
<p>기능</p>
<ul>
<li>SSH 키 메모리 저장</li>
<li>여러 서버 접속 시 자동 인증</li>
<li>매번 키 입력할 필요 없음</li>
</ul>
<p>쉽게 말하면</p>
<blockquote>
<p>SSH Key Agent 프로그램</p>
</blockquote>
<p>예시</p>
<p>Git 서버 + 여러 서버 접속 시
PuTTYgen으로 만든 키를 Pageant에 등록하면
SSH 접속 시 자동으로 인증된다.</p>
<hr />
<h2 id="25-putty-manual">2.5 PuTTY Manual</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1be2e926-2060-4298-9c66-5d2f70910085/image.png" /></p>
<p>PuTTY의 공식 <strong>사용 설명서</strong>이다.</p>
<p>내용</p>
<ul>
<li>PuTTY 사용 방법</li>
<li>SSH 설정 설명</li>
<li>키 인증 방법</li>
<li>포트 포워딩</li>
</ul>
<p>PuTTY 설정이 복잡할 때 참고하면 좋다.</p>
<hr />
<h1 id="3-putty-패키지-구성-요약">3. PuTTY 패키지 구성 요약</h1>
<table>
<thead>
<tr>
<th>프로그램</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>PuTTY</td>
<td>SSH 접속 프로그램</td>
</tr>
<tr>
<td>PSFTP</td>
<td>SFTP 파일 전송</td>
</tr>
<tr>
<td>PuTTYgen</td>
<td>SSH 키 생성</td>
</tr>
<tr>
<td>Pageant</td>
<td>SSH 키 관리</td>
</tr>
<tr>
<td>PuTTY Manual</td>
<td>공식 설명서</td>
</tr>
</tbody></table>
<hr />
<h1 id="4-putty가-많이-사용되는-이유">4. PuTTY가 많이 사용되는 이유</h1>
<p>PuTTY가 오래도록 많이 사용되는 이유는 다음과 같다.</p>
<ul>
<li>가벼운 프로그램</li>
<li>설치가 매우 간단</li>
<li>SSH 접속 안정성 높음</li>
<li>무료 오픈소스</li>
<li>서버 개발 환경에서 표준처럼 사용</li>
</ul>
<p>특히 <strong>Linux 서버 관리 / Raspberry Pi / 클라우드 서버 접속</strong>에서는 주로 CLI 환경을 사용하기 때문에 매우 많이 사용된다고 한다.</p>