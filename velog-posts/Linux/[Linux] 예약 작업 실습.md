<h3 id="예약-작업-cron">예약 작업 (cron)</h3>
<ul>
<li>주기적인 자동 실행.</li>
<li><code>crontab -e</code>로 편집기 열기.</li>
<li>1분마다 현재 시간을 파일에 기록하는 작업 등록 (<code>* * * * date &gt;&gt; time.log</code>).</li>
<li>로그 파일 쌓이는 것 확인 후 크론탭 삭제.</li>
</ul>
<hr />
<h3 id="crontab-심화">crontab 심화</h3>
<p>리눅스 내장 '알람 시계'. 특정 시간에 특정 명령어를 자동으로 실행해주는 스케줄러</p>
<p>임베디드/서버 관리의 핵심 도구. 백업, 로그 정리, 센서 데이터 수집 등 '주기적 작업'을 담당한다.</p>
<h3 id="1-문법-5개의-별">1. 문법 (5개의 별)</h3>
<p>가장 중요함. 순서를 외워야 함.</p>
<pre><code class="language-bash">* * * * [실행할 명령어]
┬ ┬ ┬ ┬ ┬
│ │ │ │ └─ 요일 (0~7, 0/7=일요일, 1=월요일)
│ │ │ └──── 월 (1~12)
│ │ └─────── 일 (1~31)
│ └────────── 시 (0~23)
└───────────── 분 (0~59)</code></pre>
<h3 id="2-핵심-명령어">2. 핵심 명령어</h3>
<ul>
<li><code>crontab -e</code>: 편집 (Edit). 설정 파일을 엶. (가장 많이 씀)</li>
<li><code>crontab -l</code>: 조회 (List). 현재 예약된 작업 목록 확인.</li>
<li><code>crontab -r</code>: 삭제 (Remove). 주의: 묻지도 따지지도 않고 싹 다 지움.</li>
</ul>
<h3 id="3-실전-예제">3. 실전 예제</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7feeb434-357c-4737-ae97-b122a05a56f9/image.png" /></p>
<h3 id="a-주기적-실행">A. 주기적 실행</h3>
<ul>
<li><p>매분 실행:Bash</p>
<pre><code class="language-bash">  * * * * /home/pi/check_status.sh</code></pre>
</li>
<li><p>매일 새벽 4시 30분 (백업):Bash</p>
<pre><code class="language-bash">  30 4 * * * /home/pi/backup.sh</code></pre>
</li>
<li><p>매주 월요일 아침 9시:Bash</p>
<pre><code class="language-bash">  0 9 * * 1 /home/pi/report.sh</code></pre>
</li>
</ul>
<h3 id="b-특수-기호-활용">B. 특수 기호 활용</h3>
<ul>
<li><p>간격 실행 (<code>/</code>): 5분마다 실행.Bash</p>
<pre><code class="language-bash">  /5 * * * * /home/pi/sensor_read.sh</code></pre>
</li>
<li><p>범위 실행 (): 평일(월~금) 아침 9시.Bash</p>
<pre><code class="language-bash">  0 9 * * 1-5 /home/pi/work.sh</code></pre>
</li>
<li><p>복수 선택 (<code>,</code>): 매시 0분, 30분마다.Bash</p>
<pre><code class="language-bash">  0,30 * * * * /home/pi/ping.sh</code></pre>
</li>
</ul>
<h3 id="c-임베디드-필수-reboot">C. 임베디드 필수 (<code>@reboot</code>)</h3>
<ul>
<li><p>부팅 되자마자 실행: (rc.local 대신 많이 씀)Bash</p>
<pre><code class="language-bash">  @reboot /home/pi/startup.sh</code></pre>
</li>
</ul>
<h3 id="4-주의사항">4. 주의사항</h3>
<ol>
<li><p>절대 경로 필수:</p>
<ul>
<li><p>cron은 환경변수($PATH)를 거의 모름.</p>
<pre><code class="language-bash">python3 script.py (X) → /usr/bin/python3 /home/pi/script.py (O)</code></pre>
</li>
</ul>
</li>
<li><p>로그 남기기 (디버깅):Bash</p>
<ul>
<li><p>cron은 실행 결과(출력)를 화면에 안 보여줌. 에러 나도 모름.</p>
</li>
<li><p>반드시 파일로 저장하거나 버려야 함.</p>
<p>```bash</p>
<h1 id="로그-저장-표준-출력--에러-출력-모두">로그 저장 (표준 출력 + 에러 출력 모두)</h1>
</li>
<li><ul>
<li><ul>
<li><ul>
<li><ul>
<li>/home/pi/task.sh &gt;&gt; /home/pi/task.log 2&gt;&amp;1</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<h1 id="로그-버리기-조용히-실행">로그 버리기 (조용히 실행)</h1>
</li>
<li><ul>
<li><ul>
<li><ul>
<li><ul>
<li>/home/pi/task.sh &gt; /dev/null 2&gt;&amp;1
```</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ol>