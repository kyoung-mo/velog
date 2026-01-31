<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/97f24a96-3867-44db-b13b-b4bc7f6bb99a/image.png" /></p>
<hr />
<h3 id="파일-링크-ln">파일 링크 (ln)</h3>
<ul>
<li><p><strong>학습:</strong> 하드 링크 vs 심볼릭 링크(바로가기)의 결정적 차이 (inode 개념).</p>
</li>
<li><p><strong>실습(1h):</strong></p>
<ul>
<li>원본 파일 생성 후 하드 링크와 심볼릭 링크 각각 생성.</li>
<li>원본 파일 삭제 시 심볼릭 링크는 깨지고(<code>broken</code>), 하드 링크는 살아있는 현상 확인.</li>
<li><code>ls -i</code>로 inode 번호가 같은지 확인.</li>
</ul>
</li>
<li><p><strong>심볼릭 링크 (<code>ln -s</code>):</strong> 윈도우의 <strong>&quot;바로가기&quot;</strong>. 원본이 지워지면 링크는 깨짐.</p>
</li>
<li><p><strong>하드 링크 (<code>ln</code>):</strong> 하나의 파일 데이터(Inode)에 이름표를 하나 더 붙이는 <strong>&quot;복제 없는 복제&quot;</strong>. 원본을 지워도 데이터는 살아있음.</p>
</li>
</ul>
<pre><code class="language-bash">mkdir link_practice
cd link_practice</code></pre>
<hr />
<h3 id="1-심볼릭-링크-symbolic-link-사용-예제">1. 심볼릭 링크 (Symbolic Link) 사용 예제</h3>
<ul>
<li>*&quot;경로(Path)를 가리키는 이정표&quot;**가 필요할 때 씁니다.</li>
</ul>
<h4 id="프로그램-버전-관리-가장-흔함">프로그램 버전 관리 (가장 흔함)</h4>
<p>시스템에는 여러 버전의 파이썬이나 라이브러리가 깔려 있습니다. <code>python</code>이라고 쳤을 때 실행될 버전을 심볼릭 링크로 관리합니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 실제 실행 파일은 복잡한 이름을 가짐
/usr/bin/python3.10
/usr/bin/python3.11

# 사용자는 그냥 'python'만 치면 됨 (링크가 최신 버전을 가리킴)
ln -s /usr/bin/python3.11 /usr/bin/python</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0e20b274-62a3-424a-a138-9166417dd9c1/image.png" /></p>
<ul>
<li><strong>장점:</strong> 원본을 덮어쓰지 않고 링크만 바꿔서 버전을 스위칭할 수 있음.</li>
</ul>
<h4 id="복잡한-경로-단축--설정-관리-nginxapache">복잡한 경로 단축 &amp; 설정 관리 (Nginx/Apache)</h4>
<p>웹 서버 설정에서 많이 씁니다. 실제 파일은 깊숙한 곳에 두고, 짧은 경로로 링크를 겁니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 실제 프로젝트 위치 (너무 깊음)
/home/user/projects/my-web-app/config/nginx.conf

# 시스템이 읽는 표준 위치로 링크
ln -s /home/user/projects/my-web-app/config/nginx.conf /etc/nginx/sites-enabled/myapp</code></pre>
<ul>
<li><strong>장점:</strong> 파일을 복사하지 않으므로, 원본(<code>projects/...</code>)을 수정하면 서버 설정도 즉시 반영됨.</li>
</ul>
<h4 id="용량-부족-해결-파티션-건너뛰기">용량 부족 해결 (파티션 건너뛰기)</h4>
<p>하드 링크는 다른 파티션(드라이브)으로 못 만들지만, 심볼릭 링크는 가능합니다.</p>
<p>Bash</p>
<pre><code class="language-c"># /home (SSD) 용량이 꽉 참.
# /data (HDD)에 큰 로그 폴더를 옮겨두고 링크만 걸어둠.
mv /home/user/logs /data/large_hdd/logs
ln -s /data/large_hdd/logs /home/user/logs</code></pre>
<ul>
<li><strong>장점:</strong> 프로그램은 여전히 <code>/home/user/logs</code>에 파일이 있다고 착각하고 정상 작동함.</li>
</ul>
<hr />
<h3 id="2-하드-링크-hard-link-사용-예제">2. 하드 링크 (Hard Link) 사용 예제</h3>
<p><strong>&quot;데이터는 하나지만, 여러 곳에서 동시에 소유해야 할 때&quot;</strong> 씁니다.</p>
<h4 id="공간-절약형-백업-time-machine-원리">공간 절약형 백업 (Time Machine 원리)</h4>
<p><code>rsync</code> 등을 이용한 증분 백업에서 핵심 기술입니다.</p>
<ul>
<li>어제 백업 파일: 100GB</li>
<li>오늘 백업 파일: 어제와 똑같음.</li>
<li>이때 <strong>파일을 복사하는 게 아니라 하드 링크를 겁니다.</strong></li>
</ul>
<p>Bash</p>
<pre><code class="language-c"># 파일 내용은 똑같지만, 별도의 파일처럼 보임.
# 하지만 실제 디스크 용량은 0바이트 추가됨 (Inode 공유).
ln yesterday/big_file.iso today/big_file.iso</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/11c4bd6c-f383-40ce-857d-dda837b1d997/image.png" /></p>
<ul>
<li>ID 같은것을 확인할 수 있다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/131b128c-2655-4379-a970-42ad5b4be46d/image.png" /></li>
</ul>
<ul>
<li><strong>장점:</strong> 100GB 파일이 10개 있어도 디스크는 100GB만 차지함.</li>
</ul>
<h4 id="실수-방지용-안전장치">실수 방지용 '안전장치'</h4>
<p>중요한 데이터베이스 파일이나 로그 파일을 실수로 <code>rm</code> 하는 것을 막기 위해 사용합니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 원본 데이터
/var/www/critical_data.db

# 관리자 홈에 하드 링크 생성
ln /var/www/critical_data.db /root/backup/critical_data_hardlink</code></pre>
<ul>
<li><strong>장점:</strong> 누군가 실수로 <code>/var/www/critical_data.db</code>를 삭제해도, <code>/root/...</code>에 링크가 남아있기 때문에 <strong>데이터는 디스크에서 삭제되지 않고 살아있습니다.</strong> (Inode 참조 카운트가 1 남았기 때문)</li>
</ul>
<h4 id="여러-프로젝트에서-동일-파일-공유-read-only">여러 프로젝트에서 동일 파일 공유 (Read-Only)</h4>
<p>여러 프로젝트 폴더에서 공통으로 쓰는 거대한 데이터셋(예: AI 학습용 이미지 50GB)이 필요할 때.</p>
<p>Bash</p>
<pre><code class="language-c">project_A/dataset/ (50GB)
project_B/dataset/ (하드링크 생성)</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8daf7447-36d4-4e8e-8fbb-7be803d5af64/image.png" /></p>
<ul>
<li><strong>장점:</strong> 심볼릭 링크와 달리, <code>project_A</code>를 지워버려도 <code>project_B</code>의 데이터는 안전하게 유지됩니다. 각 프로젝트가 파일을 &quot;독립적&quot;으로 소유한 효과를 냅니다.</li>
</ul>
<hr />
<h3 id="정리">정리</h3>
<table>
<thead>
<tr>
<th><strong>상황</strong></th>
<th><strong>추천</strong></th>
<th><strong>이유</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>다른 드라이브</strong>로 연결해야 함</td>
<td><strong>심볼릭</strong></td>
<td>하드 링크는 파티션을 못 건너감.</td>
</tr>
<tr>
<td><strong>디렉터리(폴더)</strong>를 연결해야 함</td>
<td><strong>심볼릭</strong></td>
<td>하드 링크는 디렉터리 연결이 (거의) 불가능.</td>
</tr>
<tr>
<td><strong>백업/스냅샷</strong>을 만들고 싶음</td>
<td><strong>하드</strong></td>
<td>용량 차지 없이 독립된 파일처럼 동작.</td>
</tr>
<tr>
<td><strong>원본 삭제 시</strong> 같이 죽어야 함</td>
<td><strong>심볼릭</strong></td>
<td>바로가기니까 원본 없으면 무효.</td>
</tr>
<tr>
<td><strong>원본 삭제 돼도</strong> 데이터는 살려야 함</td>
<td><strong>하드</strong></td>
<td>마지막 하나가 지워질 때까지 데이터 생존.</td>
</tr>
</tbody></table>