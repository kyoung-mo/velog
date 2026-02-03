<h3 id="디스크-용량-확인-df-du">디스크 용량 확인 (df, du)</h3>
<ul>
<li><code>df -h</code>로 전체 파일 시스템 용량 및 마운트 지점 파악.</li>
<li><code>du -sh *</code> 명령어로 현재 폴더 내에서 누가 용량을 가장 많이 먹는지 범인 색출.</li>
<li><code>/var/log</code> 폴더 용량 분석해보기.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1a105710-8513-4ea4-ab81-5154eb82e2b9/image.png" /></p>
<hr />
<h3 id="1-df--disk-free">1. df = Disk Free</h3>
<p>&quot;디스크에 빈 공간(Free)이 얼마나 남았니?&quot;</p>
<ul>
<li>대상: 파일 시스템 전체 (SD카드 전체, 하드디스크 전체).</li>
<li>비유: 자동차의 &quot;연료 게이지&quot;. (연료통 전체에 기름이 얼마나 남았는지 확인).</li>
<li>특징: 파일 시스템의 요약 정보를 읽기 때문에 파일이 많아도 결과가 순식간에 나옴.</li>
</ul>
<h3 id="2-du--disk-usage">2. du = Disk Usage</h3>
<p>&quot;이 파일/폴더가 디스크를 얼마나 사용(Usage)하고 있는가?&quot;</p>
<ul>
<li>대상: 특정 디렉터리나 파일.</li>
<li>비유: 마트 계산대의 &quot;저울&quot;. (바구니에 담긴 물건 하나하나의 무게를 잼).</li>
<li>특징: 폴더 안의 파일들을 일일이 찾아다니며 합산하기 때문에, 파일이 많으면 시간이 좀 걸림.</li>
</ul>
<blockquote>
<p><code>df</code>는 전체 용량을 확인하고, <code>du</code>는 폴더별 용량을 확인할 때 씁니다.</p>
</blockquote>
<hr />
<h3 id="사례-1-용량-부족-알림이-떴을-때-health-check">사례 1. 용량 부족 알림이 떴을 때 (Health Check)</h3>
<p>라즈베리 파이가 &quot;No space left on device&quot; 에러를 뱉은 상황</p>
<ul>
<li>해결 : 전체 디스크 상태 확인 (<code>df</code>).</li>
</ul>
<p><strong>1. 전체 용량 확인 (가독성 좋게)</strong></p>
<p>Bash</p>
<pre><code class="language-bash">df -h</code></pre>
<ul>
<li><code>h</code> (Human): 바이트 단위 대신 GB, MB로 보여줌.</li>
<li>체크 포인트: <code>Use%</code>가 100%에 가까운 파티션이 어딘지 확인 (보통 <code>/</code> 또는 <code>/var</code>).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b6dbf6e3-9e06-4b44-a17d-a8f358d5e5e6/image.png" /></p>
<p><strong>2. 아이노드(Inode) 고갈 확인</strong></p>
<p>Bash</p>
<pre><code class="language-bash">df -i</code></pre>
<ul>
<li>상황: 용량(GB)은 남았는데 파일 생성이 안 됨.</li>
<li>이유: 작은 파일(캐시, 로그)이 수백만 개 생겨서 '파일 개수 제한(Inode)'이 꽉 찬 경우.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/392b351a-2b4e-4ee9-b398-fe8964a4e61f/image.png" /></p>
<hr />
<h3 id="사례-2-도대체-뭐가-용량을-잡아먹지-root-cause">사례 2. 도대체 뭐가 용량을 잡아먹지? (Root Cause)</h3>
<p><code>df</code>로 확인하니 <code>/</code>가 99%일때, 용량을 잡아먹는 파일을 찾는 법</p>
<ul>
<li>해결: 디렉터리별 용량 추적 (<code>du</code>).</li>
</ul>
<p><strong>1. 현재 폴더의 1단계 하위 용량만 보기 (필수 명령어)</strong>
그냥 <code>du</code> 치면 화면이 폭발한다. 딱 1단계 깊이만 봐야 합니다.</p>
<p>시간 오래걸림→ 검색하려는 폴더 선택 잘하세요.</p>
<pre><code class="language-bash">du -h --max-depth=1 | sort -hr
# 또는 짧게
du -h -d 1 | sort -hr</code></pre>
<ul>
<li><code>d 1</code>: 깊이(Depth)를 1로 제한.</li>
<li><code>sort -hr</code>: 용량 큰 순서대로 정렬 (Human readable, Reverse).</li>
<li>결과: <code>/var</code>가 10GB네? -&gt; <code>cd /var</code> -&gt; 다시 <code>du</code> 실행 -&gt; <code>/var/log</code>가 범인이네? (추적 과정).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/918eecf9-4099-4e21-a917-691b6fc99670/image.png" /></p>
<p>서로 같은 결과가 나오는 것을 알 수 있다.</p>
<p>** 2. 특정 파일 하나만 볼 때**</p>
<p>Bash</p>
<pre><code class="language-bash">du -sh my_build_folder/</code></pre>
<ul>
<li><code>s</code> (Summary): 주절주절 안 나오고 합계만 딱 보여줌.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c71ee77a-13a0-45c1-bb96-28cc092a81ab/image.png" /></p>
<hr />
<h3 id="사례-3-파일을-지웠는데-용량이-안-줄어들어요-ghost-file">사례 3. &quot;파일을 지웠는데 용량이 안 줄어들어요!&quot; (Ghost File)</h3>
<p>상황: <code>rm big_log.log</code>로 10GB짜리 로그를 지웠음. 근데 <code>df -h</code>는 여전히 100%라고 함.
원인: 어떤 프로세스가 그 파일을 아직 잡고(Open) 있어서 실제로 삭제가 안 된 상태. (<code>du</code>에서는 안 보이고 <code>df</code>에서는 보임).</p>
<p>해결: 잡고 있는 놈 찾아서 죽이기.</p>
<p>Bash</p>
<pre><code class="language-bash"># 삭제되었지만(deleted) 열려있는 파일 찾기
lsof | grep deleted</code></pre>
<ul>
<li>조치: 해당 프로세스(예: <code>python3</code>, <code>rsyslogd</code>)를 재시작(<code>systemctl restart ...</code>)하거나 죽이면 용량이 즉시 확보됨.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/02fea3a6-d514-4ab9-8db5-88a9cdeac20a/image.png" /></p>
<p>&quot;List Open Files. '누가 이 파일을(또는 포트를) 붙잡고 있냐?'를 따지는 탐정 도구.&quot;</p>
<p>리눅스에서는 &quot;모든 것이 파일(Everything is a file)&quot;입니다. 하드디스크 파일뿐만 아니라, 네트워크 포트, 디바이스, 파이프까지 전부 파일로 취급합니다. 그래서 <code>lsof</code> 하나면 시스템의 모든 연결 상태를 볼 수 있습니다.</p>
<hr />
<h3 id="1-자주-발생하는-문제">1. 자주 발생하는 문제</h3>
<h3 id="①-이-포트-누가-쓰고-있어-포트-충돌-해결">① &quot;이 포트 누가 쓰고 있어?&quot; (포트 충돌 해결)</h3>
<p>서버를 띄우려는데 <code>Address already in use</code> 에러가 날 때, 범인을 찾습니다.</p>
<p>Bash</p>
<pre><code class="language-bash"># 8080 포트를 쓰고 있는 프로세스 찾기
sudo lsof -i :8080</code></pre>
<ul>
<li>결과: <code>PID</code>를 알려줍니다. <code>kill -9 [PID]</code>로 죽이면 해결됩니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e82f8e43-0332-40f1-ac33-6e35fc485f63/image.png" /></p>
<h3 id="②-usb가-안-빠져요-device-is-busy">② &quot;USB가 안 빠져요!&quot; (Device is busy)</h3>
<p><code>umount</code> 하려는데 &quot;Target is busy&quot;라고 나올 때, 누가 그 폴더에 들어가 있는지 찾습니다.</p>
<p>Bash</p>
<pre><code class="language-bash"># /mnt/usb 를 잡고 있는 범인 찾기
sudo lsof /mnt/usb</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5df33731-6fec-4697-b36f-8a0cee97eb96/image.png" /></p>
<ul>
<li>결과: 보통 자신이 켠 터미널 하나가 그 폴더 안에 <code>cd</code>로 들어가 있는 경우가 많습니다.</li>
</ul>
<h3 id="③-파일을-지웠는데-용량이-안-늘어나요-유령-파일">③ &quot;파일을 지웠는데 용량이 안 늘어나요&quot; (유령 파일)</h3>
<p>아까 <code>df</code>/<code>du</code> 질문에서 언급했던, '지워졌지만(Deleted) 프로세스가 잡고 있는 파일'을 찾을 때 씁니다.</p>
<p>Bash</p>
<pre><code class="language-bash">sudo lsof | grep deleted</code></pre>
<ul>
<li>결과: 이 목록에 뜨는 프로세스를 재시작하면 디스크 용량이 돌아옵니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/72a28439-e985-43c6-bed3-4e2f4f2708f9/image.png" /></p>
<hr />
<h3 id="2-특정-타겟-감시하기">2. 특정 타겟 감시하기</h3>
<h3 id="특정-프로세스가-무슨-파일을-여는지-감시-p">특정 프로세스가 무슨 파일을 여는지 감시 (<code>p</code>)</h3>
<p>내가 만든 프로그램(PID 1234)이 엉뚱한 로그 파일을 쓰고 있는지, 라이브러리는 뭘 로딩했는지 궁금할 때.</p>
<p>Bash</p>
<pre><code class="language-bash">lsof -p 1234</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4d201442-0cd6-4c30-8b61-d01e4d2bc69b/image.png" /></p>
<h3 id="특정-사용자가-연-모든-것-u">특정 사용자가 연 모든 것 (<code>u</code>)</h3>
<p><code>pi</code> 계정이 실행한 모든 걸 보고 싶을 때.</p>
<p>Bash</p>
<pre><code class="language-bash">lsof -u pi</code></pre>
<h3 id="주의사항-sudo">주의사항 (<code>sudo</code>)</h3>
<p><code>lsof</code>는 내 권한으로 볼 수 있는 것만 보여줍니다.
시스템 전체(다른 사용자나 시스템 데몬)를 보려면 반드시 <code>sudo lsof ...</code> 라고 쳐야 정확합니다.</p>
<blockquote>
<p>둘 다 진짜 하드디스크(SD카드)가 아닌 <code>가상의 공간</code></p>
</blockquote>
<h3 id="1-tmpfs-temporary-file-system">1. <code>tmpfs</code> (Temporary File System)</h3>
<ul>
<li>RAM(메모리)을 하드디스크처럼 쓰는 공간</li>
<li>물리적인 디스크(저장장치)가 아니라, 시스템의 RAM 일부를 뚝 떼어서 폴더처럼 보여주는 것<ol>
<li>엄청나게 빠름: RAM 속도니까 SSD보다 비교도 안 되게 빠릅니다.</li>
<li>휘발성: 재부팅하면 안에 있는 내용이 싹 날아갑니다. (전원 끄면 RAM이 비워지니까요).</li>
</ol>
</li>
<li>주요 용도:<ul>
<li><code>/run</code>: 실행 중인 프로세스 ID(PID) 파일이나 소켓 파일 저장. (재부팅하면 어차피 필요 없으니까).</li>
<li><code>/dev/shm</code>: 프로그램끼리 고속으로 데이터를 주고받는 '공유 메모리(Shared Memory)' 공간.</li>
<li><code>/tmp</code>: (설정에 따라) 임시 파일을 빠르게 쓰고 지울 때.</li>
</ul>
</li>
</ul>
<blockquote>
<p>이 위치에 중요한 파일(소스코드, 로그 등)을 저장하면 재부팅 순간 영구 삭제되니 주의</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ffdb8f51-0616-4d5b-b4db-7fed80df8dbe/image.png" /></p>
<hr />
<h3 id="2-efivarfs-efi-variable-file-system">2. <code>efivarfs</code> (EFI Variable File System)</h3>
<ul>
<li>메인보드의 BIOS(UEFI) 설정값에 접근하는 통로입니다.</li>
<li>하드디스크에 있는 파일이 아니라, 메인보드에 붙어있는 NVRAM(비휘발성 메모리) 칩의 데이터를 폴더처럼 보여주는 것입니다.</li>
<li>리눅스 커널이 부팅할 때 부트로더 설정이나, 부팅 순서, Secure Boot 키 같은 하드웨어 펌웨어 설정을 읽거나 쓸 때 사용합니다.</li>
<li>보이는 곳: 주로 <code>/sys/firmware/efi/efivars</code>에 마운트됩니다.</li>
</ul>
<blockquote>
<p>절대 주의 : rm -rf / 같은 걸 실수로 돌렸을 때, 일반 디스크 파일뿐만 아니라 이 efivarfs 안의 파일까지 지워지면 메인보드가 벽돌(Brick)이 될 수 있습니다. (BIOS 설정이 날아가서 부팅 불가가 됨).
최신 리눅스는 이를 방지하기 위해 읽기 전용(ro)으로 보호하거나 immutable 속성을 걸기도 합니다.</p>
</blockquote>