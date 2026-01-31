<h3 id="표준-입출력과-리다이렉션----">표준 입출력과 리다이렉션 (&gt;, &gt;&gt;, &lt;, |)**</h3>
<ul>
<li><strong>학습:</strong> 리눅스 철학(모든 것은 파일이다)의 핵심.</li>
<li><strong>실습:</strong><ul>
<li>명령어 결과를 파일로 저장(<code>&gt;</code>), 기존 파일 뒤에 덧붙이기(<code>&gt;&gt;</code>).</li>
</ul>
</li>
</ul>
<pre><code class="language-bash">mkdir ~/redirect_practice
cd ~/redirect_practice</code></pre>
<hr />
<h3 id="에러-메시지만-따로-파일로-저장하기-2-errorlog">에러 메시지만 따로 파일로 저장하기 (2&gt; error.log)</h3>
<p>시스템의 모든 로그가 아니라, <strong>&quot;에러 메시지(Standard Error)&quot;</strong>만 콕 집어서 파일로 저장하는 것임.</p>
<p>리눅스는 프로그램이 뱉는 말을 두 가지 채널(수도꼭지)로 분리해서 관리함.</p>
<h4 id="1-숫자의-의미-file-descriptor">1. 숫자의 의미 (File Descriptor)</h4>
<ul>
<li><strong>1번 (Standard Output):</strong> 정상적인 실행 결과. (생략 가능, 그냥 <code>&gt;</code> 하면 1번임)</li>
<li><strong>2번 (Standard Error):</strong> 에러, 경고 메시지.</li>
<li><strong>결과:</strong> <code>2&gt; error.log</code>를 하면, <strong>정상 결과는 화면</strong>에 나오고 <strong>에러만 파일</strong>에 저장됨.</li>
</ul>
<h4 id="2-동작-방식-덮어쓰기-vs-이어쓰기">2. 동작 방식 (덮어쓰기 vs 이어쓰기)</h4>
<ul>
<li><strong><code>2&gt; error.log</code> (덮어쓰기):</strong><ul>
<li>파일이 없으면 새로 만듦.</li>
<li>파일이 이미 있으면 <strong>기존 내용을 싹 지우고</strong> 새로 씀. (주의!)</li>
</ul>
</li>
<li><strong><code>2&gt;&gt; error.log</code> (이어쓰기):</strong><ul>
<li>기존 내용 끝에 에러를 <strong>추가(Append)</strong>함. 로그 남길 땐 이게 정석.</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b4ec4bbe-18fd-4ff5-a5dc-2d6f5564a598/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f1856573-0e9a-4d2d-ab0b-2cc0801c60df/image.png" /></p>
<h4 id="3-실무-필수-조합">3. 실무 필수 조합</h4>
<p>가장 많이 쓰는 패턴 3가지.</p>
<ol>
<li><p><strong>에러만 버리기 (침묵 모드):</strong>Bash</p>
<pre><code class="language-bash"> make 2&gt; /dev/null</code></pre>
<ul>
<li><p>설명: 에러 메시지는 꼴 보기 싫으니 휴지통(<code>/dev/null</code>)에 버림.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/39f7230d-7846-4dad-bee2-290781fa7713/image.png" /></p>
</li>
</ul>
</li>
</ol>
<ol start="2">
<li><p><strong>분리 수거 (정상 따로, 에러 따로):</strong>Bash</p>
<pre><code class="language-bash"> ./server &gt; output.log 2&gt; error.log</code></pre>
<ul>
<li>설명: 1번은 <code>output.log</code>에, 2번은 <code>error.log</code>에 각각 저장.</li>
</ul>
</li>
<li><p><strong>합쳐서 저장 (몽땅 저장):</strong>Bash</p>
<pre><code class="language-bash"> ./server &gt; all.log 2&gt;&amp;1</code></pre>
<ul>
<li>설명: <code>2&gt;&amp;1</code>은 &quot;2번(에러)을 1번(정상)이 가는 곳으로 같이 보내라&quot;는 뜻. 즉, 순서대로 <code>all.log</code>에 다 들어감.</li>
</ul>
</li>
</ol>
<hr />
<ul>
<li><code>cat file.txt | grep &quot;error&quot; | sort | uniq</code> 처럼 3단 파이프라인 구성해보기.</li>
</ul>