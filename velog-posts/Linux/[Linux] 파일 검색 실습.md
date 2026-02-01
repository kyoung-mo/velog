<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aef139ee-348f-4368-b447-8909aec6f16a/image.png" /></p>
<hr />
<h3 id="파일-검색-find">파일 검색 (find)</h3>
<ul>
<li><strong>학습:</strong> 리눅스에서 가장 강력한 검색 도구.</li>
<li><strong>실습:</strong><ul>
<li>파일명으로 찾기: <code>find /etc -name &quot;*.conf&quot;</code></li>
<li>크기로 찾기: 내 홈 폴더에서 100MB 이상인 파일 찾기 (<code>size +100M</code>).</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a0f81cac-e5f8-4a8f-9371-c1ba65d27595/image.png" /></p>
<hr />
<h3 id="찾은-파일만-ls--al을-통해서-보기">찾은 파일만 <code>ls -al</code>을 통해서 보기</h3>
<p><code>ls</code> 명령어는 파이프(<code>|</code>)로 넘어온 데이터를 파일 목록으로 받아들이지 못하기 때문에, 중간에 <strong><code>xargs</code></strong> 라는 명령어가 필요합니다.</p>
<p><code>xargs</code>는 파이프로 넘어온 <strong>&quot;글자(Text)&quot;를 &quot;명령어의 인자(Argument)&quot;로 변환</strong>해주는 역할을 합니다.</p>
<h3 id="1-파이프를-꼭-써야-한다면-xargs-사용">1. 파이프를 꼭 써야 한다면 (<code>xargs</code> 사용)</h3>
<p>Bash</p>
<pre><code class="language-c">sudo find /etc -size +100k | xargs ls -al</code></pre>
<p><strong>설명:</strong></p>
<ol>
<li><code>find</code>가 파일 경로들을 텍스트로 뱉어냅니다.</li>
<li><code>|</code> (파이프)가 그 텍스트를 넘겨줍니다.</li>
<li><code>xargs</code>가 그 텍스트를 받아서 <code>ls -al 파일1 파일2 파일3...</code> 처럼 문장을 완성해서 실행해줍니다.</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e423f581-aead-4008-90b6-43c5db0d7ea4/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/06dee079-4189-4f9b-bf74-7bd92ac38939/image.png" /></p>
<hr />
<h3 id="2-파이프-없이-하는-더-좋은-방법-exec-사용">2. 파이프 없이 하는 더 좋은 방법 (<code>exec</code> 사용)</h3>
<p><code>xargs</code>보다 공백 문자 처리가 안전하고 확실한 방법입니다.</p>
<p>Bash</p>
<pre><code class="language-c">sudo find /etc -size +100k -exec ls -al {} +</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b4ca4d80-bf2b-44c2-a9b0-f8ddbc595349/image.png" /></p>
<ul>
<li><strong><code>exec</code></strong>: 찾은 파일마다 명령어를 실행해라.</li>
<li><strong><code>{}</code></strong>: 찾은 파일 이름이 들어갈 자리.</li>
<li><strong><code>+</code></strong>: 파일들을 최대한 모아서 한 번에 실행해라 (xargs와 같은 효과).</li>
</ul>
<hr />
<h3 id="3-가장-쉬운-방법-find-자체-기능">3. 가장 쉬운 방법 (<code>find</code> 자체 기능)</h3>
<p>사실 <code>find</code> 명령어 자체에 <code>ls -l</code>과 비슷한 기능이 내장되어 있습니다.</p>
<p>Bash</p>
<p><code>sudo find /etc -size +100k -ls</code></p>
<ul>
<li><strong><code>ls</code></strong>: 찾은 파일의 상세 정보를 바로 출력함 (<code>ls -dils</code>와 유사한 형식).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1e65c7ef-454a-40a2-bb6d-93b5fdfc0546/image.png" /></p>
<hr />
<h3 id="최근-10분-내-수정된-파일-찾기">최근 10분 내 수정된 파일 찾기</h3>
<p><strong>명령어:</strong></p>
<p>Bash</p>
<pre><code class="language-c">find . -type f -mmin -10</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/75360399-0fd8-444a-85cf-cb9cc15b40d0/image.png" /></p>
<p><strong>옵션 설명:</strong></p>
<ul>
<li><code>.</code>: 현재 디렉터리부터 검색.</li>
<li><code>type f</code>: <strong>파일</strong>만 검색 (디렉터리 제외). type  d</li>
<li><code>mmin -10</code>: <strong>10분 미만</strong>(최근)에 수정됨.<ul>
<li><code>10</code>: 10분 <strong>이내</strong> (현재 ~ 10분 전)</li>
<li><code>+10</code>: 10분 <strong>이전</strong> (10분 전 ~ 과거)</li>
</ul>
</li>
</ul>
<p><strong>비교 (분 vs 일):</strong></p>
<ul>
<li><code>mmin -10</code>: 10<strong>분</strong> 이내.</li>
<li><code>mtime -1</code>: 24<strong>시간</strong>(1일) 이내.</li>
</ul>
<hr />
<h3 id="찾은-파일을-바로-삭제delete하거나-이동exec-mv-시키는-명령어-조합">찾은 파일을 바로 삭제(delete)하거나 이동(exec mv) 시키는 명령어 조합</h3>
<h3 id="1-찾아서-바로-삭제-delete">1. 찾아서 바로 삭제 (Delete)</h3>
<p><strong>가장 쉽고 빠른 방법 (<code>-delete</code> 옵션)</strong></p>
<p>Bash</p>
<pre><code class="language-c">find . -name *.tmp -or -name *.c

find . -name &quot;*.tmp&quot; -delete</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4e83a338-62a6-4706-81e6-5c22cfbe3cc9/image.png" /></p>
<p>음 찾아서 practice 안에 있는 파일들은 남기고 싶었는데 실수해서 전부 삭제되었슴다..</p>
<ul>
<li>설명: 검색된 파일을 즉시 삭제.</li>
</ul>
<p><strong>고전적인 방법 (<code>rm</code> 명령어 실행)</strong></p>
<p>Bash</p>
<pre><code class="language-c">find . -name &quot;*.tmp&quot; -exec rm {} \;</code></pre>
<ul>
<li>설명: <code>exec</code> 뒤에 <code>rm</code> 명령어를 수행.</li>
</ul>
<hr />
<h3 id="2-찾아서-이동-move">2. 찾아서 이동 (Move)</h3>
<p><strong>특정 폴더로 이동 (<code>mv</code> 명령어 실행)</strong></p>
<p>Bash</p>
<pre><code class="language-c">find . -name &quot;*.log&quot; -exec mv {} ./backup/ \;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ce53a151-6149-4587-9a29-e18955ea8158/image.png" /></p>
<p>이미 옮겨놨나봅니다</p>
<ul>
<li><strong><code>{}</code></strong>: <code>find</code>가 찾아낸 파일 이름이 들어갈 자리.</li>
<li><strong><code>./backup/</code></strong>: 이동할 목적지 폴더.</li>
<li><strong><code>\;</code></strong>: 명령어의 끝을 알림 (역슬래시 필수).</li>
</ul>
<hr />
<h3 id="⚠️-주의사항-safety-first">⚠️ 주의사항 (Safety First)</h3>
<p>삭제나 이동 명령어를 실행하기 전에, 반드시 <strong><code>ls</code></strong>로 먼저 확인하세요.</p>
<p>Bash</p>
<pre><code class="language-c"># 1. 먼저 확인 (안전)
find . -name &quot;*.tmp&quot; -ls

# 2. 확인 후 실행
find . -name &quot;*.tmp&quot; -delete</code></pre>