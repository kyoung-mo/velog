<p>요새 Oh my bash를 알게되고 학원에서 라즈베리파이, wsl, Ubuntu, 개인 노트북, 집 컴퓨터에서 작업을 하면서 몇번이나 똑같은 설정을 하면서 계속 찾게 되어서 한번 정리를 해두려 합니다.</p>
<p>제가 주로 쓰고있는 powerline 테마는 다음과 같이 생겼습니당</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d979b6db-abc1-49a1-a81d-f9b6f6ddaba9/image.png" /></p>
<hr />
<h2 id="oh-my-bash-설치">oh-my-bash 설치</h2>
<p>oh my bash를 설치하기 위해서는 curl을 먼저 설치해주어야 합니다.</p>
<pre><code class="language-bash">sudo apt update
sudo apt install curl</code></pre>
<p>이후 아래 명령어를 통해 바로 설치 후 적용이 가능합니다.</p>
<pre><code class="language-bash">bash -c &quot;$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ea5c6428-3e57-4ae0-9b0c-9512762a92ef/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/417bde72-7fe6-44cd-ae59-89c5440ae9ce/image.png" /></p>
<p>설치 이후에 기본 테마인 <code>font</code> 로 설정된 것을 확인할 수 있습니다.</p>
<p>저는 <code>powerline</code> 테마가 깃허브 관련 디렉토리인지 아닌지 확인 가능하고 깔끔한 편인거 같아서 주로 사용하고 있습니다.</p>
<pre><code class="language-bash">sudo vi ~/.bashrc

# 아래처럼 설정을 바꿔 테마를 적용할 수 있습니다.
OSH_THEME=&quot;powerline&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/174ec7fb-76a4-4090-9739-73cf509ab2a1/image.png" /></p>
<p>테마 적용 후, 재접속하면 적용됩니다.</p>
<hr />
<h2 id="powerline-테마-글자-깨짐">powerline 테마 글자 깨짐?</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f53041d7-3479-4eb0-849d-e1873e3d7c53/image.png" /></p>
<p>현재 github에서 clone해온 디렉토리입니다.
main 옆의 ?는 사실 저렇게 안생겼습니다.. 글자가 깨진 것인데, 폰트를 추가로 설치해주어야합니다.</p>
<p>powerline 테마는 일반 monospace 폰트로는 아이콘을 표시할 수 없고, powerline patched font 혹은 Nerd Font가 필요합니다.</p>
<p>apt 패키지가 있어서 설치를 해봐도 적용이 잘 안되네요.. 그래도 명령어는 적어두겠습니다.</p>
<pre><code class="language-bash">sudo apt install fonts-powerline
source ~/.bashrc # 설치 후 터미널 재시작</code></pre>
<hr />
<h2 id="nerd-font-다운로드wsl">Nerd Font 다운로드(wsl)</h2>
<p>wsl 환경이면 window에서 폰트를 받아야된다고 하네요</p>
<ul>
<li><a href="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/Hack.zip">Hack Nerd Font</a></li>
<li><a href="https://www.nerdfonts.com/font-downloads">nerdfones.com(Hack 이외 다른 글꼴)</a></li>
</ul>
<p>압축 풀어준 후 우클릭 -&gt; 설치</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/36079b31-0e1b-44d3-a078-4c61ecd4830f/image.png" /></p>
<p>이후 터미널에서 글꼴 설정을 바꿔줍니다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/882f1afb-9803-4128-a173-3f9ecdfbcc6d/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c5f43337-1139-4213-9a10-2649ba745132/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2e135b7d-d7b5-415e-af93-da73c03e520c/image.png" /></p>
<p>별건 아니지만 잘 적용됐네요 :D</p>