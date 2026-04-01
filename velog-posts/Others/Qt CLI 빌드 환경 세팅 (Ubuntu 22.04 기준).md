<p><a href="https://velog.io/@mommers/QtCreator-6.8.3-%ED%99%98%EA%B2%BD-%EC%84%B8%ED%8C%85-Ubuntu-VirtualBox">⭐이전 글 : QtCreator 6.8.3 환경 세팅 (Ubuntu VirtualBox)</a></p>
<p>이전 글에서 QtCreator GUI 환경을 세팅하였습니다.
이번 글에서는 터미널에서 직접 Qt 프로젝트를 빌드하고 실행하는 방법을 정리하였습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8cfc02a6-b03e-451b-a958-7c8a903bc9a1/image.png" /></p>
<hr />
<h2 id="1-빌드-스크립트-작성">1. 빌드 스크립트 작성</h2>
<p>매번 cmake 명령을 직접 입력하는 것은 번거롭습니다.
아래와 같이 빌드 스크립트를 작성해두면 실행하려는 폴더 위치에 들어가서 <code>qtbuild.sh</code> 명령어만으로 간편하게 빌드할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/263d3a58-40e0-4067-8af8-e22260eaf28f/image.png" /></p>
<pre><code class="language-bash">mkdir -p ~/bin
vi ~/bin/qtbuild.sh</code></pre>
<p><code>qtbuild.sh</code> 내용:</p>
<pre><code class="language-bash">#!/bin/bash
if [ ! -d build ]; then
    mkdir build
fi
cd build
qt-cmake -G Ninja -S .. -B .
ninja</code></pre>
<ul>
<li><code>qt-cmake</code> : Qt 전용 CMake 래퍼로, Qt 관련 설정이 자동으로 적용됩니다.</li>
<li><code>-G Ninja</code> : 빌드 시스템으로 Ninja를 사용합니다.</li>
<li><code>-S ..</code> : 소스 디렉토리를 상위 폴더(프로젝트 루트)로 지정합니다.</li>
<li><code>-B .</code> : 빌드 디렉토리를 현재 폴더(build/)로 지정합니다.</li>
</ul>
<p>실행 권한을 부여합니다.</p>
<pre><code class="language-bash">chmod +x ~/bin/qtbuild.sh</code></pre>
<hr />
<h2 id="2-bin-path-등록">2. ~/bin PATH 등록</h2>
<p>스크립트를 어디서든 실행하려면 <code>~/bin</code> 을 PATH에 추가해야 합니다. 일단 홈 디렉토리에 <code>bin</code> 디렉토리가 있는지 확인하고, 없다면 <code>mkdir bin</code> 으로 만들어주기만 하면 됩니다.</p>
<p><code>~/.bashrc</code>에 아래 줄을 추가합니다.</p>
<pre><code class="language-bash">export PATH=&quot;$HOME/bin:$PATH&quot;</code></pre>
<p>적용합니다.</p>
<pre><code class="language-bash">source ~/.bashrc</code></pre>
<hr />
<h2 id="3-프로젝트-빌드">3. 프로젝트 빌드</h2>
<p><code>CMakeLists.txt</code> 가 있는 프로젝트 폴더로 이동한 후 스크립트를 실행합니다.</p>
<pre><code class="language-bash">cd ~/qt-class/QT-examples/ch05/02_QCommandLinkButton
qtbuild.sh</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5430c664-be43-418f-b59a-3c6930c38283/image.png" /></p>
<p>빌드가 성공하면 아래와 같이 출력됩니다.</p>
<pre><code>-- Configuring done
-- Generating done
-- Build files have been written to: .../build
[5/5] Linking CXX executable 02_QCommandLinkButton</code></pre><blockquote>
<p><code>CMakeLists.txt</code>가 없는 폴더에서 실행하면 CMake 오류가 발생합니다.
반드시 프로젝트 루트 폴더(CMakeLists.txt가 있는 위치)에서 실행해야 합니다.</p>
</blockquote>
<hr />
<h2 id="4-빌드-결과물-실행">4. 빌드 결과물 실행</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c9b64f7d-9854-4af8-83c4-9c8762befe70/image.png" /></p>
<p>빌드가 완료되면 <code>build/</code> 폴더 안에 실행 파일이 생성됩니다.</p>
<pre><code class="language-bash">./build/02_QCommandLinkButton</code></pre>
<p>애플리케이션 창이 정상적으로 뜨면 빌드 및 실행이 완료된 것입니다.</p>
<hr />
<h2 id="전체-흐름-요약">전체 흐름 요약</h2>
<pre><code>프로젝트 폴더 이동
    ↓
qtbuild.sh 실행  (cmake configure + ninja build)
    ↓
./build/실행파일명 실행</code></pre>