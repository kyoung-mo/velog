<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/236afb22-213a-4a7b-9146-a9d936a87fd4/image.png" /></p>
<p>이 글에서는 mjpg-streamer를 사용하여 USB 웹캠 영상을 HTTP로 스트리밍하는 방법을 정리하였습니다.
Ubuntu 22.04 (VirtualBox) 환경과 Raspberry Pi 환경 두 가지를 기준으로 설명합니다.</p>
<hr />
<h2 id="1-mjpg-streamer란">1. mjpg-streamer란?</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d6bb0932-fd28-41eb-a9a9-e7842f64f124/image.png" /></p>
<p>mjpg-streamer는 웹캠에서 JPEG 프레임을 캡처하여 HTTP로 스트리밍하는 경량 커맨드라인 도구입니다.
브라우저, VLC, OpenCV 등 다양한 클라이언트에서 스트림을 수신할 수 있습니다.</p>
<hr />
<h2 id="2-ubuntu-virtualbox-환경">2. Ubuntu (VirtualBox) 환경</h2>
<p>먼저 VirtualBox 버전을 확인하고, 
해당 버전에 맞는 Extension Pack을 설치해줍니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/11d95a87-68d0-470f-875f-48bc862a764f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/343e21b7-a448-40de-b836-2e62ef191b2d/image.png" /></p>
<h3 id="2-1-usb-웹캠-연결">2-1. USB 웹캠 연결</h3>
<p>VirtualBox에서 USB 웹캠을 VM으로 연결하려면 직접 할당해야 합니다. 아래 설명은 <a href="https://github.com/jacksonliam/mjpg-streamer">mjpg-streamer_jacksonliam.github</a>를 참고하였습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/263ceb79-76e5-4bc7-87b0-94e8879fb6e5/image.png" /></p>
<p>VM 실행 창 상단 메뉴에서 <strong>장치 → 웹캠</strong> 또는 <strong>장치 → USB</strong> 에서 웹캠 항목을 선택합니다.</p>
<blockquote>
<p>USB 허브를 통해 연결된 경우 인식이 안 될 수 있습니다. PC에 직접 연결하는 것을 권장합니다.</p>
</blockquote>
<p>연결 후 장치가 인식됐는지 확인합니다.</p>
<pre><code class="language-bash">ls /dev/video*</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/07ee37a5-de6c-446e-899c-ad7091c9ac20/image.png" /></p>
<p><code>/dev/video0</code> 또는 다른 번호로 장치가 생성되면 정상입니다.
정확한 장치 번호는 아래 명령으로 확인합니다.</p>
<pre><code class="language-bash">v4l2-ctl --list-devices</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/58a46106-14ff-458b-9281-906017c1e581/image.png" /></p>
<h3 id="2-2-의존성-설치">2-2. 의존성 설치</h3>
<pre><code class="language-bash">sudo apt update
sudo apt install cmake libjpeg8-dev gcc g++</code></pre>
<h3 id="2-3-mjpg-streamer-빌드-및-설치">2-3. mjpg-streamer 빌드 및 설치</h3>
<pre><code class="language-bash">git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install</code></pre>
<h3 id="2-4-실행">2-4. 실행</h3>
<pre><code class="language-bash">export LD_LIBRARY_PATH=.
./mjpg_streamer -o &quot;output_http.so -w ./www -l 0.0.0.0 -p 8080&quot; -i &quot;input_uvc.so -d /dev/video1&quot;</code></pre>
<blockquote>
<p><code>-d</code> 옵션에 실제 장치 번호를 입력합니다. <code>v4l2-ctl --list-devices</code> 로 확인한 번호를 사용합니다.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3736bd79-72ed-431f-93a4-5b0acb07e6ee/image.png" /></p>
<h3 id="2-5-브라우저에서-확인">2-5. 브라우저에서 확인</h3>
<p>VM의 IP를 확인합니다.</p>
<pre><code class="language-bash">ip addr | grep inet</code></pre>
<p>같은 네트워크의 기기에서 브라우저로 접속합니다.</p>
<pre><code>http://VM_IP:8080</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cf323099-196d-41cd-aac8-242ace97ad7f/image.png" /></p>
<hr />
<h2 id="3-raspberry-pi-환경">3. Raspberry Pi 환경</h2>
<p>전체적으로 ubuntu와 흐름은 같습니다.</p>
<h3 id="3-1-의존성-설치">3-1. 의존성 설치</h3>
<p>Raspberry Pi OS (Debian Trixie 기준)에서는 <code>libjpeg8-dev</code> 대신 <code>libjpeg62-turbo-dev</code>를 사용합니다.</p>
<pre><code class="language-bash">sudo apt update
sudo apt install cmake libjpeg62-turbo-dev gcc g++</code></pre>
<h3 id="3-2-mjpg-streamer-빌드-및-설치">3-2. mjpg-streamer 빌드 및 설치</h3>
<pre><code class="language-bash">git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install</code></pre>
<h3 id="3-3-웹캠-장치-확인">3-3. 웹캠 장치 확인</h3>
<pre><code class="language-bash">lsusb
v4l2-ctl --list-devices</code></pre>
<p>USB 웹캠이 정상적으로 연결됐으면 <code>v4l2-ctl --list-devices</code> 출력에 웹캠 이름과 함께 <code>/dev/video0</code> 등의 장치 경로가 표시됩니다.</p>
<h3 id="3-4-실행">3-4. 실행</h3>
<pre><code class="language-bash">export LD_LIBRARY_PATH=.
./mjpg_streamer -o &quot;output_http.so -w ./www -l 0.0.0.0 -p 8080&quot; -i &quot;input_uvc.so -d /dev/video0&quot;</code></pre>
<h3 id="3-5-브라우저에서-확인">3-5. 브라우저에서 확인</h3>
<p>라즈베리파이 IP를 확인합니다.</p>
<pre><code class="language-bash">ip addr | grep inet</code></pre>
<p>같은 네트워크의 기기에서 브라우저로 접속합니다.</p>
<pre><code>http://라즈베리파이_IP:8080</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/094b8b2d-e1d1-4768-91f9-886a956def7d/image.png" /></p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code class="language-bash">웹캠 연결 확인 (lsusb, v4l2-ctl --list-devices)
    ↓
의존성 설치 (cmake, libjpeg-dev)
    ↓
mjpg-streamer 빌드 (make, sudo make install)
    ↓
실행 (input_uvc.so + output_http.so)
    ↓
브라우저에서 http://IP:8080 접속 확인</code></pre>