<blockquote>
<p>🔗 이전 글 : <a href="https://velog.io/@mommers/Yocto-Project%EB%9E%80">D3-G 보드 yocto 브링업 과정 정리(1)</a></p>
</blockquote>
<p>어제까지 진행 사항 정리 )</p>
<pre><code class="language-bash">1. SDK 소스 받기 (repo sync)          ✅ 완료
2. 빌드 환경 켜기 (source ...)          ✅ 완료
3. 이미지 빌드 (bitbake)              ◀ 지금 여기 (73%에서 한 번 죽음, 재시도 중)
─────────────────────────────────────
4. 펌웨어로 묶기 (stitch)              ⬜ 다음
5. 보드에 플래싱 (굽기)                ⬜
6. 부팅 + UART 확인                    ⬜
7. 디스플레이·CAN 동작 확인            ⬜ ← 캡스톤 목표선</code></pre>
<hr />
<p>bitbake로 굽는 과정 한번 실패해서 어제 돌려놓고 센터 도착하니 성공했네요.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a3a352d9-338d-4de5-b048-7241b02226b4/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f0d89922-dc8d-4b40-8de0-ff63267e2543/image.png" /></p>
<h3 id="4-펌웨어로-묶기-stitch">4. 펌웨어로 묶기 (stitch)</h3>
<p>아래 명령어를 입력해줍니다.</p>
<pre><code class="language-bash">cd ~/topst
./stitch-fai-d3.sh -f</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c0f48337-9d24-4956-a708-6d3a7fd4354a/image.png" /></p>
<p>잘 된것을 확인하고, 다음 단계로 넘어가주었습니다.</p>
<ul>
<li><code>output_d3g.fai</code> ← <strong>펌웨어 본체</strong> (부트로더+부트+dtb+rootfs 4파티션 묶음)</li>
<li><code>output_d3g.gpt</code> ← 파티션 지도</li>
<li><code>fwdn</code>, <code>fwdn.exe</code>, <code>fwdn.bat</code>, <code>fwdn.sh</code> ← <strong>플래싱 도구</strong> (다음 단계)</li>
<li><code>VtcUsbPort.dll</code> ← 윈도우용 USB 드라이버</li>
</ul>
<hr />
<h3 id="5-보드-플래싱">5. 보드 플래싱</h3>
<blockquote>
<p>🔗 <a href="https://topst.ai/tech/docs?page=Quick+Guide/D3-G+Quick+Guide.md">D3-G quick guide</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/09e7ffae-e392-4974-a8b7-801c8383c861/image.png" /></p>
<p>화면에서 FWDN 스위치를 누른 상태로 D3-G 보드에 전원 케이블을 연결하라고 하는데 이거는 C타입 주변에 있는 SW1(BOOT) 버튼입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5a29c083-8e7d-4da9-a74d-2032b8468d88/image.png" /></p>
<p>저는 윈도우 환경에서 보드 플래싱을 진행했고, 보드-컴퓨터 연결해도 알 수 없는 장치라고 나오기 때문에 VTC 드라이버를 설치해주었습니다.</p>
<p>아래는 텔레칩스에서 제공하는 VTC 드라이버 링크입니다.</p>
<blockquote>
<p>🔗 텔레칩스 VTC 드라이버 다운로드
<a href="https://drive.google.com/file/d/1muQnY8kuKxDsy3p3FUiQqcG34Zjk-mnR/view">https://drive.google.com/file/d/1muQnY8kuKxDsy3p3FUiQqcG34Zjk-mnR/view</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b03189de-68a0-47cc-9bb1-80d1a64ec349/image.png" /></p>
<p>Windows10 사용중이기 때문에 <code>win10_x64</code> 에서 설치를 진행해주었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3bee3cce-a338-4098-bbbf-d0304d1f0e29/image.png" /></p>
<p>이후 Telechips TCCxxxx VTC USB Driver를 잘 인식하는 모습입니다.</p>
<p>이제 보드에 플래싱 해주기 위해 wsl에서 산출물 확인</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8cba0e24-bba6-4df6-91c8-fd6ac9b5aa97/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/37332504-cc56-4a51-a6c7-fb6fd5694f5e/image.png" /></p>
<p>해당 링크에 있는 <code>output_d3g.fwdn</code> 압축 폴더를 경로 찾기 쉽게 바탕화면으로 옮겨서 압축해제 해주었습니다.</p>
<p>이후 <code>fwdn.bat</code> 파일 실행</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2159edab-617d-4899-898e-f157482f7cbd/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/27ba0c1e-dbb8-42a2-b0eb-4d137d8a79ec/image.png" /></p>
<p>아래와 같이 로그가 나옵니다.</p>
<blockquote>
<p>보드 상태 읽기 -&gt; 초기화 -&gt; 부트로더 굽기 -&gt; rootfs 굽기</p>
</blockquote>
<p><code>fwdn.bat</code>이 펌웨어를 굽기 전, 위의 4 단계를 순서대로 실행하며 리눅스를 올리는 과정입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b8159966-ce9e-4cc5-9ff0-071f61d79e59/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/42b0b849-8ebc-4ee1-95e9-c901090c5eba/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e9d63b5b-2057-47f3-bc2a-1b51a6b60f03/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2b553463-4fc9-47a5-8fcf-d3a7343bca40/image.png" /></p>
<hr />
<h3 id="6-부팅--uart--can-확인">6. 부팅 + UART / CAN 확인</h3>
<p>시리얼 연결 잘 되는걸 확인했습니당
초기 ID, 비밀번호는 <code>root / root</code></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/45c601bd-4ff6-4ad8-8318-290953388c74/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4be29a8f-18e2-499d-adc4-f6cdf30134d2/image.png" /></p>
<p>로그인 성공했으나.. DP-HDMI 선으로 모니터 연결해봐도 GUI 안나오는걸 보니 yocto로 받은 커스텀 리눅스는 CLI 환경인 것 같습니다.</p>
<p>아래 명령어를 통해 CAN을 사용 가능한지 확인해봤는데 여기서는 빠져 있나봐요..</p>
<pre><code class="language-bash">root@d3-g-topst-main:~# find /proc/device-tree -iname &quot;*can*&quot;
root@d3-g-topst-main:~# find / -name &quot;*.dtb&quot; 2&gt;/dev/null | head -20
root@d3-g-topst-main:~#</code></pre>
<p>Yocto 이용한 보드 브링업 배워가는 과정이라고 생각하고, 텔레칩스에서 만들어둔 GUI 있는 완성형 Ubuntu를 받아 줄 생각입니다.</p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d2c7d522-27d5-4f26-920e-47f5aea24353/image.png" /></p>
<p>아까운것.. 커스텀 리눅스 까는 과정 성공한 김에 CPU, 커널 등등 확인해보고 초기화하려구요.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>WSL</th>
<th>D3-G 보드</th>
</tr>
</thead>
<tbody><tr>
<td>CPU</td>
<td><code>x86_64</code> (인텔)</td>
<td><code>aarch64</code> (ARM) ✅</td>
</tr>
<tr>
<td>커널</td>
<td>WSL 6.18</td>
<td><code>5.10.205-tcc</code> ✅</td>
</tr>
<tr>
<td>OS</td>
<td>Ubuntu 24.04</td>
<td><code>poky-telechips</code> ✅</td>
</tr>
<tr>
<td>그래픽</td>
<td>없음</td>
<td><code>card0</code> 있음 ✅</td>
</tr>
</tbody></table>
<p>같은 명령을 WSL과 D3-G 보드에서 실행해본 비교 결과입니다.</p>