<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9ada36a1-bcf4-4fba-a3ae-a99003edf590/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ccef1cd4-33a6-4fc1-8f2f-ed1f4ee7f741/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f5424815-bd70-498b-af81-c7922d0c18ee/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/02247b2f-2f19-4ee7-8141-0afc7fac9f9c/image.png" /></p>
<p>원래는 다 만들어야 하는데 상속만 받으면 자동으로 생성</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d9225125-7ba3-4a78-8c9a-a09db1c9cd54/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/07c6b596-631d-47bf-8b96-b54a790ae204/image.png" /></p>
<p>debug, release 등 다 만듦</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/689aced9-51e7-4356-9a03-e6a9808e4b80/image.png" /></p>
<p>서브 프로젝트 만들건지? 깃 쓸건지? 지금은 x</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f2e59135-7fe6-4903-bbdc-e543def23bbf/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/52602c9f-4154-4490-a26c-2dbc844a1c01/image.png" /></p>
<p>cmake까지 자동으로 만들어진 것 확인 가능</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/51aa3137-c796-4cfd-afad-d78ecce5324c/image.png" /></p>
<p>링크 라이브러리는 위와 같은 형식으로 계속 추가해주면 된다.</p>
<p>++ cmake 정리하기</p>
<h3 id="2단계-필수-도구-재설치-확인">2단계: 필수 도구 재설치 확인</h3>
<p>RPi5에 CMake와 빌드 필수 도구가 제대로 설치되어 있는지 확인합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/711632b4-8d58-45d6-810f-d906a320b039/image.png" /></p>
<p>터미널 환경에서 cmake 아래를 통해 설치 후 재부팅</p>
<pre><code class="language-bash">sudo apt update
sudo apt install build-essential cmake gdb</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/594fe9c6-1332-4d03-9641-ba0ffc85a622/image.png" /></p>
<p>3단계: Qt Creator 설정 초기화
Qt Creator 자체의 설정 값이 꼬였을 경우, 설정 폴더를 잠시 옮겨서 초기화된 상태로 실행해 봅니다.</p>
<pre><code class="language-bash">mv ~/.config/QtProject ~/.config/QtProject_backup
# 그 다음 다시 실행
qtcreator &amp;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7289cbc7-9d99-44ae-aefd-ad8635174b6f/image.png" /></p>
<p>mobaxterm -&gt; ssh를 통해 위 명령어 입력해주고, <code>qtcreator &amp;</code> 이후 <code>Open Project</code></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/82329959-5bdb-4367-aa20-ecb86d864a4e/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/33be66c8-a2d4-4de3-b1d5-afcbd4d45ee4/image.png" /></p>
<p>이런식으로 오른쪽 아래 뭐가 뜨고, <code>Qt_test1 [master]</code> 안에 <code>Qt_test1</code>, <code>Forms</code>, <code>Header Files</code>, <code>Source Files</code> 가 생기는 것을 확인할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/593c0254-95a9-41f0-9b3e-622de35b5116/image.png" /></p>