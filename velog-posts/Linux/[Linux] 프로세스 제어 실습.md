<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8a9843df-dbbd-4446-9203-97f68a3d7dec/image.png" /></p>
<hr />
<h3 id="프로세스-제어-kill-pkill-killall">프로세스 제어 (kill, pkill, killall)</h3>
<ul>
<li><strong>학습:</strong> 시그널(9:강제종료, 15:정상종료) 차이.</li>
<li><strong>실습:</strong><ul>
<li><code>sleep 1000</code> 명령어로 멍 때리는 프로세스 백그라운드 실행.</li>
<li><code>pid</code>를 찾아 <code>kill -9 [PID]</code>로 죽이기.</li>
<li>이름으로 죽이기(<code>pkill sleep</code>) 실습.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="명령어-kill--l"><strong>명령어: <code>kill -l</code></strong></h3>
<p>터미널에 <code>kill -l</code> (소문자 L)을 입력하면 시스템에서 지원하는 모든 시그널(1번~64번)의 <strong>번호와 이름</strong>을 쫙 보여줌.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/64a96ed7-e801-45ad-8f2b-a5d44c4965ce/image.png" /></p>
<h4 id="1-필수-개념-5가지">1. 필수 개념 5가지!</h4>
<p>64개가 나오지만, 실무에서는 아래 5개만 알면 됨.</p>
<table>
<thead>
<tr>
<th>번호</th>
<th>이름</th>
<th>키(Key)</th>
<th>설명</th>
<th>특징</th>
</tr>
</thead>
<tbody><tr>
<td><strong>2</strong></td>
<td><strong>SIGINT</strong></td>
<td><code>Ctrl + C</code></td>
<td><strong>인터럽트 (Interrupt)</strong></td>
<td>실행 중단 요청. 프로그램이 <strong>거부(무시) 가능</strong>.</td>
</tr>
<tr>
<td><strong>9</strong></td>
<td><strong>SIGKILL</strong></td>
<td>-</td>
<td><strong>강제 종료 (Kill)</strong></td>
<td><strong>즉사.</strong> 프로그램이 거부할 수 없음. 뒷정리(파일 저장 등) 못 하고 죽음.</td>
</tr>
<tr>
<td><strong>11</strong></td>
<td><strong>SIGSEGV</strong></td>
<td>-</td>
<td><strong>세그폴트 (Segfault)</strong></td>
<td><strong>메모리 침범.</strong> 포인터 잘못 썼을 때 OS가 강제로 죽임.</td>
</tr>
<tr>
<td><strong>15</strong></td>
<td><strong>SIGTERM</strong></td>
<td><code>kill [PID]</code></td>
<td><strong>종료 요청 (Terminate)</strong></td>
<td><strong>기본값.</strong> &quot;제발 꺼져줄래?&quot;라고 정중하게 요청. 프로그램이 뒷정리하고 스스로 죽음.</td>
</tr>
<tr>
<td><strong>19</strong></td>
<td><strong>SIGSTOP</strong></td>
<td><code>Ctrl + Z</code></td>
<td><strong>일시 정지 (Stop)</strong></td>
<td>프로세스를 메모리에 둔 채 멈춤(Pause). <code>fg</code>로 재개 가능.</td>
</tr>
</tbody></table>
<h4 id="2-상세-스펙-확인법"><strong>2. 상세 스펙 확인법</strong></h4>
<p>각 시그널이 정확히 어떤 동작을 하는지(기본 액션이 종료인지, 코어 덤프인지 등) 보고 싶다면 매뉴얼 페이지를 봐야 함.</p>
<pre><code class="language-bash">man 7 signal</code></pre>
<ul>
<li>리눅스 표준 시그널 설명서가 나옴.</li>
</ul>
<h3 id="팁">팁</h3>
<ul>
<li><strong>죽일 때 순서:</strong> 무조건 <code>kill -9</code>부터 날리지 말 것.<ol>
<li><strong><code>kill -15 [PID]</code></strong> (먼저 정중하게 종료 요청)</li>
<li>안 죽으면 <strong><code>kill -2 [PID]</code></strong> (Ctrl+C 효과)</li>
<li>그래도 안 죽으면 <strong><code>kill -9 [PID]</code></strong> (최후의 수단)</li>
</ol>
</li>
</ul>