<p>이제 자취방에서 본가로 컴퓨터를 옮기고, 너무 느려서 컴퓨터 초기화했습니다.
과제를 하려니 처음부터 환경 설정 다시 해야하는 상황인데, 하는 김에 블로그에 정리해야겠다고 생각했습니다..</p>
<hr />
<p>WSL(Windows Subsystem for Linux)이란 윈도우 환경에서 리눅스를 간단하게 사용할 수 있는 프로그램입니다.</p>
<p>간단한 설치 명령어는 아래와 같습니다.</p>
<pre><code class="language-bash">wsl --install // </code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cc806f00-18c5-49d5-947d-4f3dc7dc35de/image.png" /></p>
<p>저는 Ubuntu 24.04 LTS를 다운받고 싶습니다. wsl을 처음 깔았을 때 친절하게 띄워주는 <code>Linux용 Windows 하위 시스템 시작</code> 을 참고해 설치 가능한 버전을 확인해보았습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/60591a5e-dfdb-495a-bdb5-e0d0f00ca9aa/image.png" /></p>
<ul>
<li>설치 가능한 WSL 배포판 목록 명령<pre><code class="language-bash">wsl.exe -l -o</code></pre>
<img alt="" src="https://velog.velcdn.com/images/mommers/post/5414d553-6318-410d-b640-68a08c392dc8/image.png" /></li>
</ul>
<p>Name : Ubuntu-24.04 / FRENDLTY NAME : Ubuntu 24.04 LTS 저는 이 버전을 다운받으려 합니다.</p>
<pre><code class="language-bash">wsl.exe --install Ubuntu-24.04</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/75ea268b-d11f-4ceb-af24-e00f376dce95/image.png" /></p>
<p>/home 위치에 mommers 홈 디렉토리가 생성된것을 확인하였습니다.
다시 나가서, 아까 기본값으로 설치해둔 Ubuntu와, 방금 설치한 Ubuntu-24.04 버전 이렇게 두 개의 배포판이 있을건데, 확인해봅시다.</p>
<pre><code>wsl --list</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/457a10af-c9c2-4c0f-aa56-767afef8e512/image.png" /></p>
<p>여기서 기본값을 Ubuntu-24.04로 바꿔주기 위해서 <code>wsl.exe --help</code> 를 참고해봤을때,
<img alt="" src="https://velog.velcdn.com/images/mommers/post/d35aaa47-2761-4da8-899c-40c4bcc82685/image.png" /></p>
<p>--set-default, <code>-s Ubuntu-24.04</code></p>
<pre><code class="language-bash"></code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/36d22770-9a0a-4ccd-a80c-f0e9528ac1d5/image.png" /></p>
<p>기본값이 Ubuntu-24.04로 바꼈네요.</p>
<p>이후 기본 패키지들을 설치해줍시다!!</p>
<pre><code class="language-bash">sudo apt update        // 언제 하든 상관 없습니다.
sudo apt upgrade    // 신중하게 진행하셔야합니다. 초반에는 괜찮을 것 같아요!</code></pre>
<p><strong>참고)</strong></p>
<pre><code>C:\Users\User&gt;wsl.exe --help
Copyright (c) Microsoft Corporation. All rights reserved.
이 제품의 개인 정보 보호에 관한 정보는 https://aka.ms/privacy에서 확인하세요.

사용법: wsl.exe [Argument] [Options...] [CommandLine]

Linux 이진 파일을 실행하기 위한 인수:

    명령줄이 제공되지 않으면 wsl.exe는 기본 셸을 시작합니다.

    --exec, -e &lt;CommandLine&gt;
        기본 Linux 셸을 사용하지 않고 지정된 명령을 실행합니다.

    --shell-type &lt;standard|login|none&gt;
        제공된 셸 형식으로 지정된 명령을 실행합니다.

    --
        나머지 명령줄을 있는 그대로 전달합니다.

옵션:
    --cd &lt;Directory&gt;
        지정된 디렉터리를 현재 작업 디렉터리로 설정합니다.
        ~가 사용되는 경우 Linux 사용자의 홈 경로가 사용됩니다. 경로가 시작되면
        / 문자를 사용하면 절대 Linux 경로로 해석됩니다.
        그렇지 않으면 값이 절대 Windows 경로여야 합니다.

    --distribution, -d &lt;DistroName&gt;
        지정된 배포를 실행합니다.

    --distribution-id &lt;DistroGuid&gt;
        지정된 배포 ID를 실행합니다.

    --user, -u &lt;UserName&gt;
        지정된 사용자로 실행합니다.

    --system
        시스템 배포에 대한 셸을 시작합니다.

Linux용 Windows 하위 시스템을 관리하기 위한 인수:

    --help
        사용 정보를 표시합니다.

    --debug-shell
        진단을 위해 WSL2 디버그 셸을 엽니다.

    --install [Distro] [Options...]
        Linux 배포용 Windows 하위 시스템을 설치합니다.
        유효한 배포 목록의 경우 'wsl.exe --list --online'을 사용합니다.

        옵션:
            --enable-wsl1
                WSL1 지원을 사용하도록 설정합니다.

            --fixed-vhd
                배포를 저장할 고정 크기 디스크를 만듭니다.

            --from-file &lt;Path&gt;
                로컬 파일에서 배포를 설치합니다.

            --legacy
                레거시 배포 매니페스트를 사용합니다.

            --location &lt;Location&gt;
                배포에 대한 설치 경로를 설정합니다.

            --name &lt;Name&gt;
                배포의 이름을 설정합니다.

            --no-distribution
                필요한 선택적 구성 요소만 설치하고 배포를 설치하지 않습니다.

            --no-launch, -n
                설치 후 배포를 시작하지 마세요.

            --version &lt;Version&gt;
                새 배포에 사용할 버전을 지정합니다.

            --vhd-size &lt;MemoryString&gt;
                배포를 저장할 디스크의 크기를 지정합니다.

            --web-download
                Microsoft Store 대신 인터넷에서 배포를 다운로드합니다.

    --manage &lt;Distro&gt; &lt;Options...&gt;
        배포판 관련 옵션을 변경합니다.

        옵션:
            --move &lt;Location&gt;
                배포를 새 위치로 이동합니다.

            --set-sparse, -s &lt;true|false&gt;
                배포판의 vhdx를 스파스로 설정하여 디스크 공간을 자동으로 회수할 수 있도록 합니다.

            --set-default-user &lt;Username&gt;
                배포의 기본 사용자를 설정합니다.

            --resize &lt;MemoryString&gt;
                배포 디스크의 크기를 지정된 크기로 조정합니다.

    --mount &lt;Disk&gt;
        모든 WSL 2 배포에서 실제 또는 가상 디스크를 연결하고 탑재합니다.

        옵션:
            --vhd
                &lt;디스크&gt;가 가상 하드 디스크를 참조하도록 지정합니다.

            --bare
                디스크를 WSL2에 연결하고 탑재하지는 마세요.

            --name &lt;Name&gt;
                탑재 지점의 사용자 지정 이름을 사용하여 디스크를 탑재합니다.

            --type &lt;Type&gt;
                디스크를 탑재할 때 사용할 파일 시스템이 지정되지 않은 경우 기본적으로 ext4입니다.

            --options &lt;Options&gt;
                추가 탑재 옵션입니다.

            --partition &lt;Index&gt;
                탑재할 파티션의 인덱스가 지정되지 않은 경우 기본값은 전체 디스크입니다.

    --set-default-version &lt;Version&gt;
        새 배포에 대한 기본 설치 버전을 변경합니다.

    --shutdown
        실행 중인 모든 배포와 WSL 2을 즉시 종료합니다.
        경량 유틸리티 가상 머신입니다.

        옵션:
            --force
                작업이 진행 중인 경우에도 WSL 2 가상 머신을 종료합니다. 데이터 손실을 초래할 수 있습니다.

    --status
        Linux용 Windows 하위 시스템 상태를 표시합니다.

    --unmount [Disk]
        모든 WSL2 배포에서 디스크를 해제하고 분리합니다.
        인수 없이 호출되는 경우 모든 디스크를 해제하고 분리합니다.

    --uninstall
        이 컴퓨터에서 Linux용 Windows 하위 시스템 패키지를 제거합니다.

    --update
        Linux용 Windows 하위 시스템 패키지를 업데이트합니다.

        옵션:
            --pre-release
                사용 가능한 경우 시험판 버전을 다운로드합니다.

    --version, -v
        버전 정보를 표시합니다.

Linux용 Windows 하위 시스템 배포를 관리하기 위한 인수:

    --export &lt;Distro&gt; &lt;FileName&gt; [Options]
        배포를 tar 파일로 내보냅니다.
        파일 이름은 - for stdout 일 수 있습니다.

        옵션:
            --format &lt;Format&gt;
                내보내기 형식을 지정합니다. 지원되는 값: tar, tar.gz, tar.xz, vhd.

    --import &lt;Distro&gt; &lt;InstallLocation&gt; &lt;FileName&gt; [Options]
        지정된 tar 파일을 새 배포로 가져옵니다.
        파일 이름은 - for stdin 일 수 있습니다.

        옵션:
            --version &lt;Version&gt;
                새 배포에 사용할 버전을 지정합니다.

            --vhd
                제공된 파일이 tar 파일이 아닌 .vhdx 파일임을 지정합니다.
                이 작업은 지정된 설치 위치에 .vhdx 파일의 복사본을 만듭니다.

    --import-in-place &lt;Distro&gt; &lt;FileName&gt;
        지정된 .vhdx 파일을 새 배포판로 가져옵니다.
        이 가상 하드 디스크는 ext4 파일 시스템 형식으로 포맷해야 합니다.

    --list, -l [Options]
        배포를 나열합니다.

        옵션:
            --all

배포를 포함하여 모든 배포를 나열합니다.
                현재 설치 중이거나 제거되고 있습니다.

            --running
                현재 실행 중인 배포만 나열합니다.

            --quiet, -q
                배포 이름만 표시합니다.

            --verbose, -v
                모든 배포에 대한 자세한 정보를 표시합니다.

            --online, -o
                'wsl.exe --install'을 사용하여 설치에 사용할 수 있는 배포 목록을 표시합니다.

    --set-default, -s &lt;Distro&gt;
        배포를 기본값으로 설정합니다.

    --set-version &lt;Distro&gt; &lt;Version&gt;
        지정된 배포의 버전을 변경합니다.

    --terminate, -t &lt;Distro&gt;
        지정된 배포를 종료합니다.

    --unregister &lt;Distro&gt;
        배포를 등록 취소하고 루트 파일 시스템을 삭제합니다.</code></pre>