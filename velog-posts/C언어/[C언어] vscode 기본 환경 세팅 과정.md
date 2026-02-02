<p>과제 시작 전에 환경 세팅을 해보겠습니다.</p>
<p>일단 <a href="https://code.visualstudio.com/">vscode</a>를 설치 후, 왼쪽 아래 톱니바퀴를 눌러 <code>profiles</code> 를 선택해줍니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/836cf7db-b58f-4fb1-a426-308f63f5b4ac/image.png" /></p>
<p>New Profile에 원하는 이름으로 생성해주고, Extentions를 다운 받으러 갑시다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/823c8ca5-ef0b-47ac-a950-9907d02639ce/image.png" /></p>
<p><code>C/C++ Extension Pack</code> 이거 하나만 다운 받아도, 아래 파일이 전부 설치됩니다.</p>
<ul>
<li>C/C++ </li>
<li>C/C++ Themes</li>
<li>CMake Tools</li>
</ul>
<p>이후 vscode상에서 위쪽 메뉴 &gt; Terminal 선택
wsl을 켜준 후, 작업 디렉토리를 만들어주고 <code>code .</code> 명령을 실행합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9643e41b-0a1e-458c-bbaa-100d1c142185/image.png" /></p>
<p>이렇게 새로 뜬 창은, 왼쪽에 기본 디렉토리가 방금 <code>code .</code> 명령어를 설치한 디렉토리 위치와 같게 나타납니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0d9541f8-9aa8-45db-9e12-2cc23c4c6829/image.png" /></p>
<p>test.c에서 Hello, World!를 띄워봅시다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/5170df0c-3cec-4265-9092-a47c8faf4e06/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/56a69d06-be24-461e-8ea3-c9cd2811ab5e/image.png" /></p>
<p>파일을 작성했으나, gcc가 안 깔려있기 때문에 설치를 해줍니다. 중간에 y/n 나오면 y 누르고 엔터</p>
<pre><code class="language-bash">sudo apt install gcc</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7c170319-8546-4597-b318-256ab13af055/image.png" /></p>
<p>다 설치된 후, 터미널상에서 실행이 잘 되는것을 확인해보았습니다.</p>
<pre><code class="language-bash">gcc test.c -o test    // 컴파일
./test    // 실행 파일 실행</code></pre>
<hr />
<p>이제 왼쪽 폴더에서 만들어져있는 test.c 파일을 들어가봅시다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9eaab5e7-def1-4b56-8ad4-78de7a26c1ff/image.png" /></p>
<p>F5를 눌러서 Run and Debug를 하면 다음과 같이 나옵니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6a9f867c-1547-4034-b4c4-be0ff8f9a5ae/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c8b552e0-054b-4237-aebe-60a59c72f42f/image.png" /></p>
<p>gdb도 깔아주겠습니다.</p>
<pre><code class="language-bash">sudo apt install gdb -y        // -y는 yes 스킵 용도</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f1b4d5c8-0d0e-49a4-ba81-ab5a02ba3010/image.png" /></p>
<p>이제 F5를 누르면 위와 같이 나옵니다. 가장 위에 메뉴 선택해주시면 됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ab39b712-1f56-4fe1-9e91-448fe956126c/image.png" /></p>
<p>터미널 창에서 출력이 잘 되는것을 확인할 수 있습니다.</p>