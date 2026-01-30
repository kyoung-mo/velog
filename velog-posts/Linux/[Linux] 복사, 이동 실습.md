<h3 id="복사와-이동-cp-mv">복사와 이동 (cp, mv)</h3>
<ul>
<li><strong>학습:</strong> 파일명 변경(<code>mv</code>의 활용). 백업 습관.</li>
<li><strong>실습:</strong><ul>
<li><code>cp -r</code>로 디렉터리 통째로 백업본 만들기 (<code>_bak</code> 붙이기).</li>
<li><code>mv</code>를 사용해 파일 10개의 확장자를 <code>.txt</code>에서 <code>.bak</code>으로 일괄 변경(와일드카드  활용).</li>
<li>덮어쓰기 경고 옵션 <code>i</code> 테스트. ⇒~/ .bashrc 맨 아래에 추가.</li>
</ul>
</li>
</ul>
<pre><code class="language-bash">alias rm=&quot;rm -i&quot;</code></pre>
<ul>
<li><em>브레이스 확장(<code>{}</code>)*</em>과 <strong><code>rename</code></strong> 명령어를 쓰면 순식간에 처리됨.</li>
</ul>
<hr />
<h3 id="1-폴더-생성-및-파일-10개-만들기">1. 폴더 생성 및 파일 10개 만들기</h3>
<p>숫자 범위를 지정하는 <code>{1..10}</code> 문법이 핵심.</p>
<p>Bash</p>
<pre><code class="language-bash"># 1.txt ~ 10.txt 한 방에 생성
touch ~/project/my_app/build/{1..10}.txt</code></pre>
<h3 id="2-확장자-일괄-변경-txt-→-bak">2. 확장자 일괄 변경 (.txt → .bak)</h3>
<p>가장 쉬운 방법은 <code>rename</code> 명령어를 쓰는 것임.</p>
<p>Bash</p>
<pre><code class="language-bash"># 문법: rename 's/찾을문자/바꿀문자/' 대상파일
rename 's/.txt/.bak/' *.txt</code></pre>
<h3 id="rename-명령어가-없다면">rename 명령어가 없다면?</h3>
<p>우분투/라즈베리파이에 기본으로 없을 수 있음. 설치하거나 <code>for</code>문을 써야 함.</p>
<ul>
<li><strong>설치:</strong> <code>sudo apt install rename</code></li>
<li><strong>설치 없이 하기 (쉘 스크립트):</strong>Bash</li>
</ul>
<pre><code class="language-bash">for f in *.txt; do mv &quot;$f&quot; &quot;${f%.txt}.bak&quot;; done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f340c239-cbfc-44bd-8597-3494c959fe2b/image.png" /></p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/735d91a2-2cd1-4209-9baa-3a43a4ae8d14/image.png" /></p>
<pre><code class="language-bash">for f in *.txt; do mv &quot;$f&quot; &quot;${f%.txt}.bak&quot;; done</code></pre>
<p>이 코드가 어떻게 동작하는건지 알아보고 싶어서 이것저것 만져봤다..</p>
<ol>
<li><code>for f in *.txt;</code> : <code>.txt</code>로 끝난 모든 파일마다 반복</li>
<li><code>do mv &quot;~~&quot;</code> : do-while 문에서 do 내용은 한번 무조건 실행하고, 그 뒤에 while문 조건에 맞게 안의 내용을 반복하는 느낌이였으니까 do 뒤에 문장을 실행해라. 이런 의미로 받아들임</li>
<li><code>mv &quot;$f&quot; &quot;${f%.txt}.bak&quot;</code> : 파일 이름을 수정하는데, <code>${f%.txt}</code>에 해당하는 부분을 <code>$f</code> .bak 을 붙게 하도록 파일 이름을 바꾼다.</li>
</ol>