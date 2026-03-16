<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/92d7a6ca-bcbb-4419-a08b-5c3e8e59176f/image.png" /></p>
<ul>
<li><a href="https://velog.io/@mommers/%EC%8B%9C%EC%8A%A4%ED%85%9C-%EC%BD%9C%EC%9D%B4%EB%9E%80-%EA%B0%84%EB%8B%A8-%EC%98%88%EC%A0%9C-%EC%BD%94%EB%93%9C%EB%A6%AC%EB%B7%B0">[이전 글]: 시스템 콜이란? 간단 예제 코드리뷰</a></li>
<li><a href="https://velog.io/@mommers/TCPIP-%EA%B8%B0%EB%B3%B8-%EA%B0%9C%EB%85%90-%EC%A0%95%EB%A6%AC">[이전 글]: TCP/IP 기본 개념 정리</a></li>
<li><a href="https://velog.io/@mommers/%ED%8C%8C%EC%9D%BC-%EB%94%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%84%B0%EB%9E%80">[이전 글]: 파일 디스크립터란?</a></li>
</ul>
<hr />
<p>이전 글에서 시스템 콜의 <code>copy.c</code> 예제 코드와, TCP/IP 기본 예제 <code>hello_client.c</code> , <code>hello_server.c</code> 코드를 병합하는 과제가 있었습니다.</p>
<p><a href="https://github.com/kyoung-mo/linuxC/tree/main/TCPIP_Src/Chapter1">TCP Server/Client 코드 : <code>hello_server.c</code>, <code>hello_client.c</code> 링크</a></p>
<p><strong>1. Client</strong></p>
<ul>
<li><code>./실행파일</code> <code>ip</code> <code>port</code> <code>file</code> 형식으로 실행<ul>
<li>인자 부족하면 오류 메세지 띄움</li>
</ul>
</li>
<li><code>argv[3]</code> 에 해당하는 파일 명을 <code>RDONLY</code> 로 열어서, Server로 전송</li>
</ul>
<p><strong>2. Server</strong></p>
<ul>
<li><code>./실행파일</code> <code>ip</code> <code>file</code> 형식으로 실행<ul>
<li>인자 부족하면 오류 메세지 띄움</li>
</ul>
</li>
<li>Client가 보낸 파일을 <code>argv[2]</code>에 해당하는 파일 명으로 저장</li>
<li><code>buf</code> 크기는 100 단위로 전송</li>
<li>최종 만들어진 파일인 <code>file</code>의 권한 = 644(-rw-r--r--)로 생성</li>
</ul>
<hr />
<p>금요일부터 오늘까지 이런저런 삽질을 하며 AI 도움을 받을까 했지만, 다른 사람들 다 성공하는데 저만 AI 도움 받아서 성공하고 싶지 않아서 다시 공부하면서 진행해봤습니다.</p>
<p>이런 저런 삽질 끝에 결론은,
Read, Write에서 어느 파일 디스크립터(<code>fd</code>)에 nbytes 만큼 buf에 Write 할것이고, 어느 파일 디스크립터(<code>fd</code>)에서 nbytes 만큼 buf만큼 Read 할 것인지가 중요했습니다.</p>
<hr />
<h2 id="copyc">copy.c</h2>
<ul>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/test.d/copy_new.c"><code>copy.c</code> code</a></li>
</ul>
<p>일단 copy.c에서 644의 권한을 만들기 위해 코드를 수정했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/94b4f0a4-8ac8-4099-bfd1-f30b8d44e650/image.png" /></p>
<p><code>out</code>으로 생성되는 파일에만 권한을 부여하면 됐었기 때문에 기존 코드에서 <code>S_IRGRP|S_IROTH</code> 를 추가하여 Group, Other에 읽기 권한을 부여해줬고, copy.c 실행 시 권한 644로 생성되는 것을 확인하고, 병합 단계로 넘어갔습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8fcbc800-0c3f-4f20-806b-a38f34af5c89/image.png" /></p>
<h3 id="최종-코드">최종 코드</h3>
<ul>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/test/copy_new.c"><code>copy_new.c</code> code</a></li>
</ul>
<hr />
<h2 id="tcp-serverclient">TCP Server/Client</h2>
<ul>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/test.d/hello_client.c"><code>hello_client.c</code> code</a></li>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/test.d/hello_server.c"><code>hello_server.c</code> code</a></li>
</ul>
<p>코드 상으로 볼 때는 이론적으로 다 맞다고 생각했는데, 계속 원하는 결과가 안 나와서 필요한 <code>fd</code> 값을 하나하나 찍어봤고,</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bfb3bd48-9974-4167-97b8-9d9c2bd9ebfa/image.png" /></p>
<p>처음에는 왼쪽 사진처럼 client에서 보낼 파일을 <code>in</code>에 저장했었는데, <code>in</code>의 <code>fd</code> 값이 0이 나와서 뭔가 이상하다고 생각했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2a237878-6669-421b-9aaf-5fd890b6efcf/image.png" /></p>
<p>위 코드가 정상 코드인데, 제가 괄호 하나를 실수로 빠뜨려서</p>
<pre><code class="language-c">if((in=open(argv[3], O_RDONLY)&lt;0))
{
...
}</code></pre>
<p> 이런 식으로 계속 코드 수정을 하고 있었고, 왜 오류없이 컴파일이 됐었는지는 잘 몰랐습니다.</p>
<p> 직접 <code>fd</code> 값을 찍어봄으로서 코드에 문제가 있는 것을 확인하였습니다.</p>
<p> <img alt="" src="https://velog.velcdn.com/images/mommers/post/e07ee57f-3ede-42df-b3fd-76f2b982d019/image.png" /></p>
<p>이후로 서버에 전송된 코드는 <code>read : 100</code> 까지만 나오고 그 뒤로 전송이 되지 않았습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6fa2ddbb-dc09-45b8-92a1-78a484b3b053/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/41bcf850-5a6d-4976-9161-31873b89f9b0/image.png" /></p>
<p>이유는 Client 코드에서 file 전송에 관련된 <code>if-else</code> 문에 있었고, 기존 코드는 아래와 같습니다.</p>
<pre><code class="language-c">else
    break;</code></pre>
<p><code>n</code> 값에 <code>in = open(argv[3], O_RDONLY)</code> 에 해당하는 <code>fd</code> 에서 최대 <code>file</code>의 사이즈 만큼 읽어와 크기가 100인 버퍼 <code>file</code>에 저장을 하고,</p>
<p>이후 <code>if-else</code> 문에서 <code>write</code> 함수를 통해 <code>sock</code> fd에 쓰기를 진행하는데, 처음에만 n&gt;0인 if 문에 한번 걸리고 그 뒤로는 읽히지 않는 문제가 있었습니다.</p>
<pre><code class="language-c">if((in=open(argv[3], O_RDONLY)&lt;0))
{
...
}</code></pre>
<p>이런식으로 잘못 사용해서 그랬었고, 코드를 수정해준 후, 값들을 추가로 저장할 수 있었습니다.</p>
<h3 id="최종-코드-1">최종 코드</h3>
<ul>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/test/file_client.c"><code>file_client.c</code> code</a></li>
<li><a href="https://github.com/kyoung-mo/linuxC/blob/main/test/file_server.c"><code>file_server.c</code> code</a></li>
</ul>