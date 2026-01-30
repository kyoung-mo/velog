<h3 id="디렉터리-탐색-ls-cd-pwd">디렉터리 탐색 (ls, cd, pwd)</h3>
<ul>
<li><strong>학습:</strong> 절대경로 vs 상대경로 개념 완벽 이해. 숨김 파일(<code>.</code>)과 부모 디렉터리(<code>..</code>)의 의미.</li>
<li><strong>실습:</strong><ul>
<li>최상위 루트(<code>/</code>)에서 자신의 홈 디렉터리까지 <code>cd</code>로 이동하되, 절대경로와 상대경로 번갈아 5회 왕복.</li>
<li><code>ls -al</code>, <code>ls -R</code> (하위 포함), <code>ls -lh</code> (용량 보기) 차이점 확인.</li>
<li><code>ls -lt</code> (시간순 정렬)로 <code>/var/log</code> 내부 파일 중 가장 최근 것 찾기.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="ls--lt에-대한-심층학습">ls -lt에 대한 심층학습</h3>
<p><code>ls -t</code> (시간순 정렬) 핵심 응용 5가지 요약.</p>
<h4 id="1-기본-조회-눈이-편한-방식">1. 기본 조회 (눈이 편한 방식)</h4>
<ul>
<li><strong><code>ls -lt</code></strong>: 최신 파일이 <strong>맨 위</strong>. (파일 적을 때 추천)</li>
<li><strong><code>ls -ltr</code></strong>: 최신 파일이 <strong>맨 아래</strong>. (파일 많을 때 추천, 커서 바로 위라 보기 편함)</li>
</ul>
<h4 id="2-최신오래된-파일-하나만-뽑기">2. 최신/오래된 파일 하나만 뽑기</h4>
<ul>
<li><strong><code>ls -t | head -1</code></strong>: 가장 <strong>최신</strong> 파일 1개 출력.</li>
<li><strong><code>ls -t | tail -1</code></strong>: 가장 <strong>오래된</strong> 파일 1개 출력.</li>
</ul>
<h4 id="3-방금-만든-파일-바로-편집하기-꿀팁">3. 방금 만든 파일 바로 편집하기 (꿀팁)</h4>
<ul>
<li><strong><code>vi $(ls -t | head -1)</code></strong>: 일일이 타이핑 안 하고 가장 최근 파일 엶.</li>
</ul>
<h4 id="4-특정-확장자-중-최신-파일-보기">4. 특정 확장자 중 최신 파일 보기</h4>
<ul>
<li><strong><code>ls -lt *.log | head -3</code></strong>: 로그 파일(<code>.log</code>) 중에서 최신 3개만 확인.</li>
</ul>
<h4 id="5-최신-n개만-남기고-싹-지우기-자동화">5. 최신 n개만 남기고 싹 지우기 (자동화)</h4>
<ul>
<li><strong><code>ls -t | tail -n +6 | xargs rm -f</code></strong><ul>
<li>1~5등(최신)은 살리고, 6등부터 끝까지(옛날 파일) 삭제.</li>
<li>백업 폴더 정리할 때 필수 명령어.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="ls-명령어-실전-문제">ls 명령어 실전 문제</h3>
<h4 id="1-로그-분석-에러-추적">1. [로그 분석] 에러 추적</h4>
<p><strong>상황:</strong> 서버에 에러가 터졌다. <code>/var/log</code> 폴더에는 수백 개의 로그 파일이 있다.
<strong>문제:</strong> 확장자가 <code>.log</code>인 파일 중 <strong>가장 최근에 수정된 3개</strong>만 자세히(<code>-l</code>) 출력하시오.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/c98eb803-8a11-4423-a0f0-c80955c223c5/image.png" /></p>
<h4 id="2-디스크-정리-용량-돼지-찾기">2. [디스크 정리] 용량 돼지 찾기</h4>
<p><strong>상황:</strong> 디스크가 꽉 찼다는 경고가 떴다. 현재 폴더에 범인이 있는 것 같다.
<strong>문제:</strong> 파일들을 <strong>용량이 큰 순서대로(내림차순)</strong> 정렬해서 자세히 출력하시오.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/6cb999de-dd5d-4155-9c09-6b8c9fb62abb/image.png" /></p>
<h4 id="3-작업-효율-커서-위치-최적화">3. [작업 효율] 커서 위치 최적화</h4>
<p><strong>상황:</strong> 작업 파일이 100개 넘게 있는 폴더에서 <code>ls -l</code>을 쳤더니, 최신 파일이 화면 위로 넘어가 버려서 스크롤을 올려야 한다.
<strong>문제:</strong> <strong>가장 최신 파일이 화면 맨 아래(내 커서 바로 위)</strong>에 오도록 정렬하여 출력하시오.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/8989265d-828b-4f54-b818-d94bb108f6d9/image.png" /></p>
<h4 id="4-설정-관리-안-보이는-파일-찾기">4. [설정 관리] 안 보이는 파일 찾기</h4>
<p><strong>상황:</strong> 홈 디렉터리에서 <code>.bashrc</code> 파일을 수정하려는데 <code>ls</code>를 쳐도 안 보인다.
<strong>문제:</strong> 점(<code>.</code>)으로 시작하는 <strong>숨김 파일까지 포함</strong>해서, 권한과 소유자 정보까지 자세히 출력하시오.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/55611eb8-066f-4b5a-8972-c9deb0052c97/image.png" /></p>
<h4 id="5-파일-카운팅-개수-세기">5. [파일 카운팅] 개수 세기</h4>
<p><strong>상황:</strong> /dev/폴더에 많은 디바이스가 있다. tty로 시작하는 디바이스 갯수가 몇개인가?
<strong>문제:</strong> 눈으로 세지 말고, 파이프(<code>|</code>)와 <code>wc</code> 명령어를 조합해 tty <strong>파일의 개수</strong>를 숫자로 출력하시오</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9173c658-7f72-42a9-87ef-69f64e83cbfb/image.png" /></p>
<p>5번 맞는지 틀렸는지 잘 모르겠다..</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8d4e180d-403a-460e-b8b7-7453961c2d43/image.png" /></p>
<p><del>세기 너무 힘들어용</del>
68개? 맞다고 합니다.</p>