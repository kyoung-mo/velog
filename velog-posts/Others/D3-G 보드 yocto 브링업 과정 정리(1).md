<p>이번 최종 프로젝트를 진행하며 메인 제어기와 분산 ECU 구조를 활용하여 프로젝트를 하면서 메인 제어기를 Dolphin 3M TCC8050 G모델(D3-G)을 사용하게 되었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/138ea82c-ef00-4a54-955c-9ae61d93d362/image.png" /></p>
<p>일반적으로 알고있는 라즈베리파이랑은 다르게, Yocto를 이용하여 Custom Linux를 올려줘야 했기 때문에 과정을 정리해보겠습니다.</p>
<hr />
<p>일단 D3-G 보드를 사용하게 된 이유는 세가지가 있습니다.</p>
<ol>
<li><p>차량 모델을 만들며 실제 차량 구조와, 안전 기능 모사를 고려하여 프로젝트를 해보자고 하여 실제 차량용 Soc를 경험해보고 싶어서였습니다.</p>
</li>
<li><p>CAN 다채널이 내장되어 있었기 때문입니다. 물론 라즈베리파이도 MCP2515라는 모듈을 통해 CAN 컨트롤러 + 트랜시버를 연결해줄 수 있으나 두번의 경험이 있기 때문입니다.</p>
</li>
<li><p>Yocto 커스텀 리눅스 빌드 경험을 쌓고 싶어서 입니다.
라즈베리파이는 기성 이미지를 구우면 끝이지만,
D3-G는 텔레칩스의 BSP를 Yocto로 빌드해서 올려야합니다.
소스부터 빌드, 브링업(디스플레이, CAN 드라이버 동작) 역량을 쌓고 싶었습니다.</p>
</li>
</ol>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d7a8324b-a69a-4ada-aa49-a4b3bb7d5280/image.png" /></p>
<p>D3-G 보드의 뒷면 Getting Started 사이트에 접속해주었습니다.</p>
<blockquote>
<p><a href="https://topst.ai/tech/docs">TOPST docs</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1af224f2-8862-48f2-b103-1b5ed4d4a7b6/image.png" />
<img alt="" src="https://velog.velcdn.com/images/mommers/post/5617d14c-6140-4845-a80d-13569fc467ae/image.png" /></p>
<p>사이트에서 G 모델의 깃허브 링크를 들어가서 SDK를 찾아봤습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6f9afc63-2aa9-4676-b595-0f366e5aa561/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c6132c4e-74e9-4b90-b3eb-77404398cc5e/image.png" /></p>
<blockquote>
<p><a href="https://github.com/topst-development/manifests">https://github.com/topst-development/manifests</a></p>
</blockquote>
<p>위 링크에 필요한 SDK가 있다는 것을 알게되었습니다.</p>
<p>wsl 환경에서 60GB 이상 필요하다고 해서 용량 확인 -&gt; 여유되는것을 확인하였습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1dd23f05-f519-4f95-a434-3c4a9a288edb/image.png" /></p>
<p>차례대로</p>
<pre><code class="language-bash">sudo apt update
sudo apt install -y gawk wget git diffstat unzip texinfo gcc build-essential \
chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils \
iputils-ping python3-git python3-jinja2 python3-subunit zstd liblz4-tool \
file locales libacl1 repo</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/69672665-1932-4702-93c6-2e7ef4d54335/image.png" /></p>
<pre><code class="language-bash">mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo &gt; ~/bin/repo
chmod a+x ~/bin/repo
export PATH=~/bin:$PATH

mkdir -p ~/topst &amp;&amp; cd ~/topst
repo init -u https://github.com/topst-development/manifests -b release/1.2.0 -m linux_yp4.0_topst.xml
repo sync</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/745438f0-b180-44bf-96e3-2c9405c48512/image.png" /></p>
<p>YOCTO 깔린것을 확인</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/33b44c22-5649-4950-b4f4-6f33ef599906/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/931b116e-d4cd-45e1-a72b-958ab795c533/image.png" /></p>
<p>열심히 bitbake를 이용해 이미지 빌드하고있습니다..</p>
<hr />
<p>현재 상황</p>
<pre><code class="language-bash">1. SDK 소스 받기 (repo sync)          ✅ 완료
2. 빌드 환경 켜기 (source ...)          ✅ 완료
3. 이미지 빌드 (bitbake)              ◀ 지금 여기 (73%에서 한 번 죽음, 재시도 중)
─────────────────────────────────────
4. 펌웨어로 묶기 (stitch)              ⬜ 다음
5. 보드에 플래싱 (굽기)                ⬜
6. 부팅 + UART 확인                    ⬜
7. 디스플레이·CAN 동작 확인            ⬜ ← 캡스톤 목표선</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/394858e1-6f2b-4d35-89ea-d0f01be5bc58/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/728939cc-e77f-4cba-9747-689c6736d93a/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/254175ae-c477-4d6c-a020-a07fa50c0c88/image.png" /></p>
<p>성공!</p>