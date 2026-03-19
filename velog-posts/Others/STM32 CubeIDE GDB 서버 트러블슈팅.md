<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4c90ec71-0de7-417e-89c5-6ab1ac6edbf5/image.png" /></p>
<p>학원에서 STM32F411 NUCLEO Board를 통해 실습을 진행하는 과정에서, 다른 사람들은 다 잘 되는데 제 자리만 문제가 있어서 트러블 슈팅 과정을 정리해보려 합니다.</p>
<p>일단 급하게 수업은 따라가야 했기 때문에, 미리 빌드되어있는 폴더를 그대로 받아서, <code>Stm32CubeProgrammer</code> 프로그램을 통해 ST-LINK에 <code>.elf</code> 파일을 넣어서 수업을 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6bfff651-0b13-4a6a-a618-200f0ed3ce5f/image.png" /></p>
<p><code>.elf</code> 파일은 CubeIDE Workspace에서 프로젝트 폴더 &gt; Debug 폴더 안에서 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/75033086-f97d-48c1-be0c-36c42c2950ba/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f71d2c2e-a98f-476c-af8f-449832602d4b/image.png" /></p>
<hr />
<h2 id="증상">증상</h2>
<p>디버그 실행 시 아래 에러가 발생했습니다.</p>
<pre><code class="language-bash">Error in final launch sequence:

Failed to start GDB server
Failed to start GDB server
Error in initializing ST-LINK device.
Reason: (0) Unknown. Please check power and cabling to target.</code></pre>
<pre><code class="language-bash">STMicroelectronics ST-LINK GDB server. Version 7.12.0
Copyright (c) 2025, STMicroelectronics. All rights reserved.

Starting server with the following options:
        Persistent Mode            : Disabled
        Logging Level              : 1
        Listen Port Number         : 61234
        Status Refresh Delay       : 15s
        Verbose Mode               : Disabled
        SWD Debug                  : Enabled

Failed to bind to port 61235, error code -1: No error
Failure starting SWV server on TCP port: 61235
Failed to bind to port 61234, error code -1: No error
Failure starting GDB server: TCP port 61234 not available.
Shutting down...
Exit.</code></pre>
<hr />
<h2 id="원인-1---windows-포트-예약-충돌">원인 1 - Windows 포트 예약 충돌</h2>
<p>학원 PC라서 <strong>WSL2나 Hyper-V가 설치된 환경</strong>에서 Windows가 부팅할 때 포트 범위를 자동으로 예약하는데, 네트워크 설정이나 설치된 프로그램에 따라 예약 범위가 달라진다고 합니다.</p>
<p>확인 방법</p>
<pre><code class="language-powershell">netsh interface ipv4 show excludedportrange protocol=tcp</code></pre>
<h3 id="결과">결과</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4fd63f3d-ff3e-4f13-83c1-4c28c7724c5a/image.png" /></p>
<p>WSL2 / Hyper-V가 부팅 시 포트 범위를 자동 예약해서 발생</p>
<h3 id="해결">해결</h3>
<p>CubeIDE 디버그 포트를 예약 범위 밖으로 변경해주었습니다. (예: 61300)</p>
<hr />
<h2 id="원인-2---gdb-connection-settings-잘못된-설정">원인 2 - GDB Connection Settings 잘못된 설정</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d7cb0435-a97c-4089-8a6d-484314d5b156/image.png" /></p>
<h3 id="증상-1">증상</h3>
<p>포트 변경 후에도 아래 에러가 발생했습니다.</p>
<pre><code>target remote localhost:61300
localhost:61300: Connection timed out.</code></pre><h3 id="원인">원인</h3>
<p>Run Configurations → Debugger 탭에서</p>
<p>포트 번호를 61300으로 수정하면서, <strong>&quot;Connect to remote GDB server&quot;</strong> 로 선택을 했습니다.</p>
<p>→ 이 옵션은 GDB 서버가 외부에서 이미 실행 중일 때 사용하는 것으로, 서버를 자동으로 띄워주지 않는다고 합니다.</p>
<h3 id="해결-1">해결</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/647e99f4-beaa-4278-a6d9-8f8075501517/image.png" /></p>
<p><strong>&quot;Autostart local GDB server&quot;</strong> 로 변경</p>
<hr />
<h2 id="최종-해결-순서">최종 해결 순서</h2>
<ol>
<li>급한불을 끄기 위해 CubeProgrammer 프로그램을 통해 <code>.elf</code> 파일을 보드에 다운로드</li>
<li><code>netsh</code> 명령으로 예약 포트 범위 확인</li>
<li>예약 범위 밖 포트로 변경 (61300 등)</li>
<li>GDB Connection Settings → <strong>Autostart local GDB server</strong> 선택</li>
<li>Apply → 디버그 실행</li>
</ol>