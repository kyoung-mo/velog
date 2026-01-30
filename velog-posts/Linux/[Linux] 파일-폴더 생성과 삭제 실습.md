<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d7fc47ba-f7e0-4794-9750-37e09cac2ba5/image.png" /></p>
<h3 id="파일폴더-생성과-삭제-mkdir-touch-rm">파일/폴더 생성과 삭제 (mkdir, touch, rm)</h3>
<ul>
<li><strong>학습:</strong> 디렉터리 트리 구조 생성. <code>rm</code>의 위험성 (-<code>rf</code>) 인지.</li>
<li><strong>실습:</strong><ul>
<li><code>mkdir -p project/src/main</code> 옵션으로 한 번에 깊은 경로 생성.</li>
<li><code>touch</code>로 파일 날짜(타임스탬프) 변경해보기.</li>
<li>빈 폴더 삭제(<code>rmdir</code>)와 내용물 있는 폴더 삭제(<code>rm -rf</code>) 차이 실습.</li>
</ul>
</li>
</ul>
<p>복잡한 디렉터리 구조 생성과 특정 폴더 삭제 실습.</p>
<h3 id="1-숲트리-한-방에-만들기">1. 숲(트리) 한 방에 만들기</h3>
<p>중괄호 <code>{}</code>를 쓰면 명령어 한 줄로 복잡한 구조가 생성됨.</p>
<p>Bash</p>
<pre><code class="language-bash">mkdir -p ~/project/my_app/{src/{main,test,utils},build/{logs,temp},docs}</code></pre>
<ul>
<li><strong><code>p</code></strong>: 상위 폴더 없으면 자동 생성.</li>
<li><strong><code>{a,b}</code></strong>: a와 b를 동시에 만듦.</li>
</ul>
<h3 id="2-특정-가지temp만-잘라내기">2. 특정 가지(<code>temp</code>)만 잘라내기</h3>
<p>만들어진 구조에서 불필요한 폴더 하나만 콕 집어서 삭제.</p>
<p>Bash</p>
<pre><code class="language-bash">rm -rf ~/project/my_app/build/temp</code></pre>
<ul>
<li><strong><code>r</code></strong>: 폴더 내용물까지 삭제.</li>
<li><strong><code>f</code></strong>: 묻지 말고 강제 삭제.</li>
</ul>
<h3 id="3-결과-확인">3. 결과 확인</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8a8e6423-dea8-49f7-aa93-54ff005d6171/image.png" /></p>
<p>Bash</p>
<pre><code class="language-bash">find my_app</code></pre>
<ul>
<li><code>temp</code> 폴더만 사라지고 나머지는 그대로 살아있음.</li>
</ul>