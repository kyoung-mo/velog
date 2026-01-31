<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/df217de0-112a-4d1d-8daa-81bd2366b45a/image.png" /></p>
<h3 id="1-셸shell과-프롬프트">1. 셸(Shell)과 프롬프트</h3>
<ul>
<li><p><strong>프롬프트(Prompt):</strong></p>
<ul>
<li>셸이 사용자의 명령 입력을 기다리는 상태를 표시하는 기호.</li>
<li>형식: <code>사용자계정@호스트명:현재위치 $</code> (예: <code>pi@raspberrypi:~ $</code>)</li>
<li><code>~</code>: 현재 사용자의 홈 디렉터리를 의미함.</li>
<li><code>$</code>: 일반 사용자 권한임을 의미함. (<code>#</code>은 관리자/root 권한)
<img alt="" src="https://velog.velcdn.com/images/mommers/post/64cd7093-8697-4f80-8a4f-a55b481ec255/image.png" /></li>
</ul>
</li>
<li><p><strong>자동 완성 기능:</strong></p>
<ul>
<li>명령어나 파일명 입력 도중 <code>Tab</code> 키를 누르면 나머지 부분이 자동 완성됨. 입력 효율성 극대화됨.</li>
</ul>
</li>
</ul>
<h3 id="2-파일-및-디렉터리-조작-명령어">2. 파일 및 디렉터리 조작 명령어</h3>
<p>리눅스 파일 시스템은 <strong>대소문자를 엄격히 구분</strong>함.</p>
<p><strong>2.1 파일 목록 확인 및 이동</strong></p>
<ul>
<li><p><strong>ls (list):</strong> 현재 디렉터리의 파일 목록 출력함.</p>
<ul>
<li><p><code>ls -l</code>: 자세한 정보(권한, 소유자, 크기, 날짜) 표시함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/f8c21431-ca32-41a9-b397-3c28bc23c67d/image.png" /></p>
</li>
<li><p><code>ls -a</code>: 숨김 파일(.으로 시작하는 파일) 포함하여 모든 파일 표시함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/e6bd7de4-3ec9-4078-b0ea-4410763b583a/image.png" /></p>
</li>
<li><p><code>ls -al</code>: 숨김 파일을 포함하여 자세히 표시함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/fa8ff236-412e-4a50-836d-8f87c02af24a/image.png" /></p>
</li>
</ul>
</li>
<li><p><strong>cd (change directory):</strong> 디렉터리 이동함.</p>
<ul>
<li><code>cd /tmp</code>: 절대 경로 /tmp로 이동함.</li>
<li><code>cd ..</code>: 상위(부모) 디렉터리로 이동함.</li>
<li><code>cd ~</code> 또는 <code>cd</code>: 사용자의 홈 디렉터리로 이동함.</li>
<li><code>cd -</code>: 바로 이전 작업 디렉터리로 복귀함.</li>
</ul>
</li>
<li><p><strong>pwd (print working directory):</strong> 현재 작업 중인 디렉터리의 절대 경로 출력함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/f3e494dd-c09e-4157-8c26-72317c503e15/image.png" /></p>
</li>
</ul>
<p><strong>2.2 파일 복사, 이동, 삭제</strong></p>
<ul>
<li><p><strong>cp (copy):</strong> 파일 또는 디렉터리 복사함.</p>
<ul>
<li><p><code>cp a.txt c.txt</code>: a.txt를 c.txt로 복사함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/e21cb13b-f9fd-4dd5-9e8d-e090b829c1c2/image.png" /></p>
</li>
<li><p><code>cp -r dir1 dir2</code>: 디렉터리 dir1을 dir2로 통째로(재귀적) 복사함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/4302173b-98d5-4f58-a07e-926df8db0b60/image.png" /></p>
</li>
</ul>
</li>
<li><p><strong>mv (move):</strong> 파일 이동 또는 이름 변경함.</p>
<ul>
<li><code>mv a.txt b.txt</code>: a.txt의 이름을 b.txt로 변경함.</li>
<li><code>mv a.txt /tmp</code>: a.txt를 /tmp 디렉터리로 이동함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/12f3f2de-e6f6-4154-9b57-b1aa3c6d5896/image.png" /></li>
</ul>
</li>
<li><p><strong>rm (remove):</strong> 파일 삭제함 (복구 불가하므로 주의 요망).</p>
<ul>
<li><code>rm a.txt</code>: 파일 삭제함.</li>
<li><code>rm -f</code>: 묻지 않고 강제로 삭제함.</li>
<li><code>rm -r</code>: 디렉터리 삭제함.</li>
<li><code>rm -rf</code>: 디렉터리와 그 내부 파일을 강제로 모두 삭제함.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/76785f59-8be9-4d85-a0a0-e8e9ab73d26f/image.png" /></li>
</ul>
</li>
</ul>
<p><strong>2.3 디렉터리 생성 및 삭제</strong></p>
<ul>
<li><strong>mkdir (make directory):</strong> 새로운 디렉터리 생성함.<ul>
<li><code>mkdir newdir</code>: newdir 생성함.</li>
<li><code>mkdir -p a/b/c</code>: 하위 디렉터리까지 한 번에 생성함.</li>
</ul>
</li>
<li><strong>rmdir (remove directory):</strong> <strong>비어 있는</strong> 디렉터리 삭제함.<ul>
<li>내용물이 있으면 삭제 불가함 (<code>rm -r</code> 사용해야 함).</li>
</ul>
</li>
</ul>
<p><strong>2.4 파일 내용 보기 및 생성</strong></p>
<ul>
<li><strong>cat (concatenate):</strong> 파일 내용을 화면에 출력함. 파일 합치기에도 사용됨.</li>
<li><strong>more:</strong> 파일 내용이 길 경우 페이지 단위로 끊어서 보여줌. (Space: 다음 페이지, Enter: 한 줄, q: 종료).</li>
<li><strong>head:</strong> 파일의 앞부분(기본 10줄)만 출력함. <code>head -n 5</code> (5줄 출력).</li>
<li><strong>tail:</strong> 파일의 뒷부분(기본 10줄)만 출력함. 로그 파일 확인 시 유용함. <code>tail -f</code> (실시간 감시).</li>
<li><strong>touch:</strong> 빈 파일 생성하거나 파일의 날짜 시간(타임스탬프) 변경함.</li>
</ul>
<p><strong>2.5 리다이렉션(Redirection)과 파이프(Pipe)</strong></p>
<ul>
<li><strong><code>&gt;</code> (출력 리다이렉션):</strong> 명령의 결과를 파일로 저장함 (덮어쓰기).<ul>
<li><code>ls &gt; list.txt</code>: ls 결과를 list.txt에 저장함.</li>
</ul>
</li>
<li><strong><code>&gt;&gt;</code> (추가 리다이렉션):</strong> 명령의 결과를 파일 끝에 추가함.</li>
<li><strong><code>|</code> (파이프):</strong> 앞 명령의 출력을 뒤 명령의 입력으로 연결함.<ul>
<li><code>ls -al | more</code>: 파일 목록이 많을 때 페이지 단위로 봄.</li>
</ul>
</li>
</ul>
<h3 id="3-사용자-계정과-그룹-관리">3. 사용자 계정과 그룹 관리</h3>
<p>리눅스는 다중 사용자 시스템으로 파일마다 소유자와 그룹이 지정됨.</p>
<ul>
<li><strong>chmod:</strong> 파일의 접근 권한 변경함. (예: <code>chmod 755 file</code>)</li>
<li><strong>chown:</strong> 파일의 소유자 변경함.</li>
<li><strong>su (switch user):</strong> 다른 사용자로 전환함. (<code>su -</code>: root로 전환)</li>
<li><strong>sudo:</strong> 일반 사용자가 관리자(root) 권한으로 명령 실행함.</li>
</ul>