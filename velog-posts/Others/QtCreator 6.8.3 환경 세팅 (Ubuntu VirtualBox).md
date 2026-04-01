<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8ba8012a-2256-4876-9c23-37bc527d8f52/image.png" /></p>
<p>Qt 설치 후 QtCreator를 처음 실행하면 Kit이 올바르게 설정되지 않아 빌드 오류가 발생할 수 있습니다.
이 글에서는 QtCreator를 처음 사용하는 분들을 위해 환경세팅 과정을 순서대로 정리하였습니다.</p>
<p>환경은 아래와 같습니다.</p>
<ul>
<li>Ubuntu 22.04</li>
<li>MobaXterm</li>
</ul>
<hr />
<h2 id="1-path-설정">1. PATH 설정</h2>
<p>QtCreator를 터미널에서 실행하려면 Qt 관련 바이너리 경로를 PATH에 추가해야 합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7a885784-bbad-4144-ae1c-1f556ece65bc/image.png" /></p>
<p><code>~/.bashrc</code>에 아래 줄을 추가합니다. (Qt 6.8.3 기준)</p>
<pre><code class="language-bash">export PATH=&quot;$HOME/Qt/6.8.3/gcc_64/bin:$HOME/Qt/Tools/Ninja:$HOME/Qt/Tools/QtCreator/bin:$HOME/Qt/Tools/CMake/bin:$PATH&quot;</code></pre>
<p>저장 후 적용합니다.</p>
<pre><code class="language-bash">source ~/.bashrc</code></pre>
<p>아래 명령으로 경로가 정상적으로 등록됐는지 확인할 수 있습니다.</p>
<pre><code class="language-bash">echo $PATH</code></pre>
<p>Qt 관련 경로들이 앞쪽에 출력되면 정상입니다.</p>
<hr />
<h2 id="2-qtcreator-실행">2. QtCreator 실행</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0c117ec7-ec7b-4991-97da-b2de6b4ba71a/image.png" /></p>
<p>MobaXterm에서 아래 명령으로 QtCreator를 백그라운드로 실행합니다.</p>
<pre><code class="language-bash">qtcreator &amp;</code></pre>
<blockquote>
<p>실행 시 <code>Failed to initialize instances shared memory</code> 메시지가 출력될 수 있습니다.
이는 단순 경고 메시지로 기능에 영향을 주지 않으므로 무시해도 됩니다.</p>
</blockquote>
<hr />
<h2 id="3-kit-설정">3. Kit 설정</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/43f54ca8-f67d-4472-aff3-734927a6f622/image.png" /></p>
<p>QtCreator 상단 메뉴에서 <strong>Edit → Preferences → Kits</strong> 로 이동합니다.</p>
<h3 id="3-1-qt-versions-확인">3-1. Qt Versions 확인</h3>
<p><strong>Qt Versions</strong> 탭에서 사용할 Qt 버전이 올바르게 인식됐는지 확인합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4fb97932-e22f-4809-8f6c-963ba9db438f/image.png" /></p>
<ul>
<li><code>Qt 6.8.3</code> → <code>/home/ubuntu/Qt/6.8.3/gcc_64/bin/qmake</code> 경로로 등록되어 있으면 정상입니다.</li>
</ul>
<blockquote>
<p>Android용 항목에 빨간 경고가 표시될 수 있습니다. Android SDK가 설치되지 않아서 발생하는 것이므로 Desktop 개발에는 영향이 없습니다.</p>
</blockquote>
<h3 id="3-2-kits-탭-설정">3-2. Kits 탭 설정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/66ccf777-52e2-4301-b9ea-58964233c9e9/image.png" /></p>
<p>저는 위와 같은 오류가 떴어서, <strong>Kits</strong> 탭에서 <strong>Desktop Qt 6.8.3</strong> 을 선택하고 아래 항목을 설정해주었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5c585f7e-895b-4764-a862-2c8ec2affe0f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/beb742d0-4232-4f6e-8f34-8bed2af78891/image.png" /></p>
<table>
<thead>
<tr>
<th>항목</th>
<th>설정값</th>
</tr>
</thead>
<tbody><tr>
<td>Compiler (C/C++)</td>
<td>GCC (x86 64bit at &quot;/bin/gcc&quot;)</td>
</tr>
<tr>
<td>CMake Tool</td>
<td>CMake 3.30.5 (Qt)</td>
</tr>
<tr>
<td>Qt version</td>
<td>Qt 6.8.3</td>
</tr>
<tr>
<td>Debugger</td>
<td>System GDB at /usr/bin/gdb</td>
</tr>
</tbody></table>
<blockquote>
<p><strong>Compiler</strong>는 기본값이 Clang으로 설정되어 있을 수 있습니다. Ubuntu Desktop 환경에서는 <strong>GCC</strong>로 변경해야 정상적으로 빌드됩니다.</p>
</blockquote>
<blockquote>
<p><strong>CMake Tool</strong>은 <code>System CMake</code> 대신 <strong>CMake 3.30.5 (Qt)</strong> 를 선택합니다. Qt 번들 CMake를 사용해야 호환성 문제가 발생하지 않습니다.</p>
</blockquote>
<p>설정 완료 후 <strong>Apply</strong> 를 클릭합니다.</p>
<hr />
<h2 id="4-프로젝트-열기-및-kit-선택">4. 프로젝트 열기 및 Kit 선택</h2>
<p>프로젝트를 열면 <strong>Configure Project</strong> 창이 표시됩니다.</p>
<ul>
<li><strong>Desktop Qt 6.8.3</strong> 항목을 체크합니다.</li>
<li>빌드 타입은 <strong>Debug</strong> 만 체크합니다. (학습/개발 환경 기준)</li>
<li><strong>Configure Project</strong> 버튼을 클릭합니다.</li>
</ul>
<blockquote>
<p>목록에 <code>Desktop</code> (버전 명시 없음) 항목이 있을 수 있습니다. 버전이 불명확하므로 체크를 해제하는 것을 권장합니다.</p>
</blockquote>
<hr />
<h2 id="5-빌드-및-실행">5. 빌드 및 실행</h2>
<p>실행한 프로그램로그램은 <a href="https://github.com/kyoung-mo/qt-study">github</a>에 있는 QT 예제인 ch05/00_QCheckBox 입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1c5db028-d7fb-4064-8fe0-578ab8966da4/image.png" /></p>
<p>Kit 설정이 완료되면 좌측 하단의 <strong>▶ 실행 버튼</strong> 또는 단축키 <code>Ctrl+R</code> 로 빌드 및 실행이 가능합니다.</p>
<p>하단 <strong>Issues</strong> 탭에 오류가 없고 애플리케이션 창이 정상적으로 뜨면 환경세팅이 완료된 것입니다.</p>