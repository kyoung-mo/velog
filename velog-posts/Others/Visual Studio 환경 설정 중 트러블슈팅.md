<p>C++ 수업을 새로 나가게 되면서 기본 환경 설정을 하면서 있었던 문제들을 정리하는 과정을 정리해보려합니다.</p>
<hr />
<ol>
<li><p>한글 깨지는 현상
<img alt="" src="https://velog.velcdn.com/images/mommers/post/a42f69cf-7f8f-4578-ab68-9824acfa9178/image.png" /></p>
</li>
<li><p><code>애플리케이션 제어 정책에서 이 파일을 차단했습니다.</code> 오류
<img alt="" src="https://velog.velcdn.com/images/mommers/post/f84b7639-f9fc-40c2-99c1-bceaed6c5a85/image.png" /></p>
</li>
</ol>
<hr />
<h2 id="한글-깨짐">한글 깨짐</h2>
<p>인코딩에 문제가 있었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b3f87de8-13a1-4310-b8d6-be95b77d3019/image.png" /></p>
<p>다른 이름으로 저장 &gt; 저장 옆에 화살표 &gt; 인코딩하여 저장 &gt; 인코딩(E) : <code>한국어(완성) - 코드 페이지 20949</code> 선택</p>
<p>이렇게 하면 당장은 한글이 출력되지만, 새로운 프로젝트를 만들면 다시 글자가 깨지는 현상이 있었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/26131c8a-b828-4a5e-b6ed-6e896a420ee7/image.png" /></p>
<p>Visual Studio에서 
<code>도구</code> &gt; <code>모든 설정</code> &gt; <code>환경</code> &gt; <code>문서</code> &gt; 특정 인코딩을 사용하여 파일 저장 &gt; 인코딩 저장 : <code>한국어(완성) - 코드 페이지 20949</code> 선택</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9c4ff5d0-7a58-465e-b653-7c9515ae406a/image.png" /></p>
<p>이후 프로젝트를 만들어도 글자가 깨지지 않는 것을 확인했습니다.</p>
<hr />
<h2 id="애플리케이션-제어-정책에서-이-파일을-차단했습니다-오류"><code>애플리케이션 제어 정책에서 이 파일을 차단했습니다.</code> 오류</h2>
<p><code>Microsoft Defender SmartScreen</code> 이 켜져있을 때 발생할 수 있는 오류라고 합니다.</p>
<blockquote>
<p><strong>한번 끄면 다시는 재설정 불가능합니다.</strong></p>
</blockquote>
<p>저는 당장 학원PC에서 실습을 진행해야하기 때문에 설정을 껐습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/108dbf4c-0c85-410d-a252-b32e8920fbdb/image.png" /></p>
<p>Window 검색 &quot;<code>앱 및 브라우저 컨트롤</code>&quot; &gt; <code>스마트 앱 컨트롤</code> &gt; <code>끄기</code> 선택</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/00121d46-4a6b-4f90-8a40-b89fb8ab2807/image.png" /></p>
<p>이후 오류 화면이 사라졌습니다.</p>