<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fdeb1be0-6800-4374-bf95-682ad2500299/image.png" /></p>
<hr />
<p>라즈베리 파이 5는 성능이 매우 좋아서(쿼드코어 Cortex-A76), PC 없이 자체적으로 커널을 빌드해도 <strong>약 40분 ~ 1시간</strong> 정도면 충분합니다. (과거 라즈베리 파이 3에서는 반나절이 걸렸던 작업입니다.)</p>
<p>다음은 라즈베리 파이 5 터미널에서 직접 커널을 빌드하고 설치하는 단계별 가이드입니다.</p>
<hr />
<h3 id="⚠️-사전-준비-필수">⚠️ 사전 준비 (필수)</h3>
<ol>
<li><strong>쿨링 팬:</strong> 빌드 중 CPU를 100% 사용하므로 발열이 심합니다. <strong>액티브 쿨러(팬)</strong>가 반드시 돌아가고 있어야 합니다.</li>
<li><strong>저장 공간:</strong> 최소 <strong>10GB 이상</strong>의 여유 공간이 필요합니다.</li>
<li><strong>OS:</strong> 라즈베리 파이 OS (Bookworm 64-bit) 기준입니다.</li>
</ol>
<hr />
<h3 id="1단계-필수-도구-설치">1단계: 필수 도구 설치</h3>
<p>터미널을 열고 빌드에 필요한 패키지들을 설치합니다.</p>
<p>Bash</p>
<pre><code class="language-c">sudo apt update
sudo apt install git bc bison flex libssl-dev make libc6-dev libncurses5-dev</code></pre>
<h3 id="2단계-커널-소스-다운로드-git-clone">2단계: 커널 소스 다운로드 (Git Clone)</h3>
<p>공식 저장소에서 소스를 가져옵니다. 시간을 아끼기 위해 <code>--depth=1</code> 옵션(최신 커밋만 받기)을 사용합니다.
(현재 RPi 5의 주력 커널 버전은 <strong>6.6</strong>입니다.)</p>
<p>Bash</p>
<pre><code class="language-c">
# 홈 디렉토리로 이동
cd ~

# 소스 다운로드 (약 5분 소요)
git clone --depth=1 --branch rpi-6.12.y https://github.com/raspberrypi/linux
cd linux</code></pre>
<h3 id="3단계-rpi-5용-설정-configuration">3단계: RPi 5용 설정 (Configuration)</h3>
<p>라즈베리 파이 5의 칩셋인 <strong>BCM2712</strong>에 맞는 기본 설정을 불러옵니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 기본 설정 로드
make bcm2712_defconfig

# (선택사항) 커널 설정을 바꾸고 싶다면 아래 명령 실행
# make menuconfig</code></pre>
<h3 id="4단계-커널-빌드-build">4단계: 커널 빌드 (Build)</h3>
<p>이제 실제로 컴파일을 시작합니다. RPi 5는 4코어이므로 <code>-j4</code> 옵션을 줍니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 커널 이미지, 모듈, 디바이스 트리(dtb) 모두 빌드
# (약 40~60분 소요, 팬 소리가 커질 것입니다)
make -j4 Image.gz modules dtbs</code></pre>
<h3 id="5단계-설치-install">5단계: 설치 (Install)</h3>
<p>빌드가 완료되면 결과물을 시스템 폴더(<code>/boot/firmware</code> 및 <code>/lib/modules</code>)에 설치합니다.</p>
<h3 id="1-모듈-설치">1. 모듈 설치</h3>
<p>Bash</p>
<pre><code class="language-c">sudo make modules_install</code></pre>
<h3 id="2-디바이스-트리dtb-복사">2. 디바이스 트리(DTB) 복사</h3>
<p>Bash</p>
<pre><code class="language-c"># RPi 5용 dtb 복사
sudo cp arch/arm64/boot/dts/broadcom/bcm2712-rpi-5-b.dtb /boot/firmware/

# 오버레이(dtoverlay) 파일들 복사
sudo cp arch/arm64/boot/dts/overlays/*.dtb* /boot/firmware/overlays/
sudo cp arch/arm64/boot/dts/overlays/README /boot/firmware/overlays/</code></pre>
<h3 id="3-커널-이미지-복사-중요">3. 커널 이미지 복사 (중요!)</h3>
<p>안전하게 기존 커널을 덮어쓰지 않고, <strong>새 이름(<code>kernel_my.img</code>)</strong>으로 저장한 뒤 설정 파일에서 바꿔치기 하는 방식을 추천합니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 빌드된 이미지를 부트 파티션으로 복사
sudo cp arch/arm64/boot/Image.gz /boot/firmware/kernel_my.img</code></pre>
<hr />
<h3 id="4단계-커널-빌드-build-1">4단계: 커널 빌드 (Build)</h3>
<p>이제 실제로 컴파일을 시작합니다. RPi 5는 4코어이므로 <code>-j4</code> 옵션을 줍니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 커널 이미지, 모듈, 디바이스 트리(dtb) 모두 빌드
# (약 40~60분 소요, 팬 소리가 커질 것입니다)
make -j4 Image.gz modules dtbs</code></pre>
<hr />
<h3 id="5단계-설치-install-⇒-하지-마세요">5단계: 설치 (Install) ⇒ 하지 마세요!!!</h3>
<p>빌드가 완료되면 결과물을 시스템 폴더(<code>/boot/firmware</code> 및 <code>/lib/modules</code>)에 설치합니다.</p>
<h3 id="1-모듈-설치-1">1. 모듈 설치</h3>
<p>Bash</p>
<pre><code class="language-c">sudo make modules_install</code></pre>
<h3 id="2-디바이스-트리dtb-복사-1">2. 디바이스 트리(DTB) 복사</h3>
<p>Bash</p>
<pre><code class="language-c"># RPi 5용 dtb 복사
sudo cp arch/arm64/boot/dts/broadcom/bcm2712-rpi-5-b.dtb /boot/firmware/

# 오버레이(dtoverlay) 파일들 복사
sudo cp arch/arm64/boot/dts/overlays/*.dtb* /boot/firmware/overlays/
sudo cp arch/arm64/boot/dts/overlays/README /boot/firmware/overlays/</code></pre>
<h3 id="cd3-커널-이미지-복사-중요">cd3. 커널 이미지 복사 (중요!)</h3>
<p>안전하게 기존 커널을 덮어쓰지 않고, <strong>새 이름(<code>kernel_my.img</code>)</strong>으로 저장한 뒤 설정 파일에서 바꿔치기 하는 방식을 추천합니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 빌드된 이미지를 부트 파티션으로 복사
sudo cp arch/arm64/boot/Image.gz /boot/firmware/kernel_my.img</code></pre>
<hr />
<h3 id="6단계-부팅-설정-변경-configtxt">6단계: 부팅 설정 변경 (<code>config.txt</code>)</h3>
<p>방금 만든 <code>kernel_my.img</code>로 부팅하도록 설정을 바꿉니다.</p>
<p>Bash</p>
<pre><code class="language-c">sudo vi /boot/firmware/config.txt</code></pre>
<p>파일 내에 <code>[all]</code> 섹션이나 맨 아래에 다음 줄을 추가합니다.</p>
<p>Ini, TOML</p>
<pre><code class="language-c">kernel=kernel_my.img</code></pre>
<h3 id="7단계-재부팅-및-확인">7단계: 재부팅 및 확인</h3>
<p>Bash</p>
<pre><code class="language-c">sudo reboot</code></pre>
<p>재부팅 후 터미널에서 다음 명령어로 빌드한 커널이 적용되었는지 확인합니다.</p>
<p>Bash</p>
<pre><code class="language-c">uname -a</code></pre>
<p>날짜와 시간이 <strong>방금 빌드한 시간</strong>으로 나온다면 성공입니다!</p>
<hr />
<h3 id="💡-빌드-시간을-줄이려면">💡 빌드 시간을 줄이려면?</h3>
<p>만약 커널 소스를 조금만 수정하고 다시 빌드할 때는 <code>make clean</code>을 하지 마세요. 변경된 부분만 컴파일하므로 1~5분 안에 끝납니다.</p>