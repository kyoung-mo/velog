<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7539d904-8296-4739-b91e-976c8415b45c/image.gif" /></p>
<h3 id="압축과-해제-tar-zip-gzip">압축과 해제 (tar, zip, gzip)</h3>
<ul>
<li>파일 여러 개를 <code>tar -cvf</code>로 묶고, <code>gzip</code>으로 압축.</li>
<li>한 방에 하기: <code>tar -czvf result.tar.gz ./folder</code>.</li>
<li>압축 풀기: <code>tar -xzvf result.tar.gz</code>.</li>
<li><code>zip</code>과 <code>unzip</code> 명령어 사용법 비교.</li>
</ul>
<p><strong><code>xz</code> (XZ Utils)</strong> 백도어 사태(CVE-2024-3094)를 말씀하시는 것으로 보임.</p>
<hr />
<h3 id="1-해킹당한-도구와-버전">1. 해킹당한 도구와 버전</h3>
<ul>
<li><strong>대상:</strong> <strong><code>xz</code> (xz-utils)</strong> / <code>liblzma</code> 라이브러리.</li>
<li><strong>문제 버전:</strong> <strong>5.6.0</strong> 및 <strong>5.6.1</strong>.</li>
<li><strong>사건:</strong> 유지보수 권한을 얻은 해커가 SSH 접속을 가로채는 <strong>백도어</strong>를 심었다. 리눅스 역사상 최악의 보안 사고가 될 뻔했다.</li>
</ul>
<h3 id="2-라즈베리-파이-raspberry-pi-os-상황">2. 라즈베리 파이 (Raspberry Pi OS) 상황</h3>
<p><strong>결론: 기본적으로 안전함.</strong></p>
<ul>
<li><strong>이유:</strong> 라즈베리 파이 OS는 <strong>Debian Stable (안정화 버전)</strong>을 기반으로 함. 업데이트가 매우 보수적이라 문제의 최신 버전(5.6.x)이 적용되기 전에 사태가 발각됨.</li>
<li><strong>사용 버전:</strong> 현재 최신 라즈베리 파이 OS(Bookworm) 기준 <strong>5.4.x</strong> 버전을 사용 중임. (안전).</li>
</ul>
<h3 id="3-내-버전-확인-및-조치-방법">3. 내 버전 확인 및 조치 방법</h3>
<p>터미널에서 바로 확인 가능하다.</p>
<pre><code class="language-bash">xz --version

xz (XZ Utils) 5.8.1
liblzma 5.8.1</code></pre>
<p><strong>판독:</strong></p>
<ul>
<li>✅ <strong>5.4.x 이하 (예: 5.4.5, 5.2.5):</strong> <strong>안전.</strong> 아무것도 안 해도 됨.</li>
<li>❌ <strong>5.6.0 / 5.6.1:</strong> <strong>위험.</strong> 즉시 다운그레이드하거나 OS 재설치 필요. (Kali Linux나 Arch Linux 같은 최신 배포판을 파이에서 돌린다면 확인 필수).</li>
</ul>