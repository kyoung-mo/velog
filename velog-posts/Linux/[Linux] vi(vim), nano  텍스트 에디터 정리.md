<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/885a1784-db43-4f4a-9603-0c7c0f7a6339/image.png" /></p>
<hr />
<h3 id="텍스트-에디터">텍스트 에디터?</h3>
<p>터미널 환경에서 작업을 진행할 때 텍스트 에디터를 주로 사용하게 된다. 텍스트 에디터로는 <code>vi</code> 혹은 <code>vim</code> 혹은 <code>nano</code> 를 많이 사용한다.</p>
<hr />
<h3 id="vi-vim-에디터">vi (vim) 에디터</h3>
<p>유닉스/리눅스의 표준 에디터. 강력한 기능을 제공하나 모드 개념이 있어 학습 필요함.</p>
<p><strong>vi의 3가지 모드</strong></p>
<ol>
<li><strong>명령 모드 (Command Mode):</strong> 기본 모드. 커서 이동, 삭제, 복사, 붙여넣기 수행함.</li>
<li><strong>입력 모드 (Insert Mode):</strong> 실제 텍스트 입력함. 명령 모드에서 <code>i</code>, <code>a</code> 등을 누르면 진입함.</li>
<li><strong>마지막 행 모드 (Last Line Mode/Ex Mode):</strong> 명령 모드에서 <code>:</code> 누르면 진입함. 저장, 종료, 검색 수행함.</li>
</ol>
<p><strong>주요 단축키</strong></p>
<ul>
<li><strong>모드 전환:</strong><ul>
<li><code>ESC</code>: 입력/마지막 행 모드에서 명령 모드로 복귀함.</li>
</ul>
</li>
<li><strong>입력 진입:</strong><ul>
<li><code>i</code>: 커서 앞에서 입력 시작함.</li>
<li><code>a</code>: 커서 뒤에서 입력 시작함.</li>
<li><code>o</code>: 현재 줄 아래에 빈 줄 삽입하고 입력함.</li>
</ul>
</li>
<li><strong>커서 이동 (명령 모드):</strong><ul>
<li><code>h</code>, <code>j</code>, <code>k</code>, <code>l</code>: 좌, 하, 상, 우 이동함. (방향키도 사용 가능)</li>
<li><code>gg</code>: 문서의 첫 줄로 이동함.</li>
<li><code>G</code>: 문서의 마지막 줄로 이동함.</li>
</ul>
</li>
<li><strong>편집 (명령 모드):</strong><ul>
<li><code>x</code>: 커서 위치 글자 삭제함.</li>
<li><code>dd</code>: 현재 줄 삭제함 (잘라내기).</li>
<li><code>yy</code>: 현재 줄 복사함.</li>
<li><code>p</code>: 붙여넣기함.</li>
<li><code>u</code>: 실행 취소 (Undo).</li>
</ul>
</li>
<li><strong>저장 및 종료 (마지막 행 모드):</strong><ul>
<li><code>:w</code>: 저장함.</li>
<li><code>:q</code>: 종료함.</li>
<li><code>:wq</code>: 저장하고 종료함.</li>
<li><code>:q!</code>: 저장하지 않고 강제 종료함.</li>
<li><code>:set nu</code>: 줄 번호 표시함.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="nano-에디터">nano 에디터</h3>
<ul>
<li>초보자가 사용하기 쉬운 직관적인 에디터임. 화면 하단에 단축키 도움말이 표시됨.</li>
<li><strong>실행:</strong> <code>nano 파일명</code></li>
<li><strong>주요 단축키 (Ctrl 키 조합):</strong><ul>
<li><code>Ctrl + O</code>: 저장하기 (Write Out).</li>
<li><code>Ctrl + X</code>: 종료하기 (Exit). (변경 사항 있으면 저장 여부 물음)</li>
<li><code>Ctrl + K</code>: 한 줄 잘라내기.</li>
<li><code>Ctrl + U</code>: 붙여넣기.</li>
<li><code>Ctrl + W</code>: 검색하기.</li>
</ul>
</li>
</ul>
<hr />