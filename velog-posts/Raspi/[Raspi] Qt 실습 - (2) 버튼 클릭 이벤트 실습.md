<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cb1c3090-5c85-4964-8e04-42818c6cfb07/image.png" /></p>
<p><code>mainwindow.ui</code> 를 더블클릭하면 아래 <code>Design</code> 메뉴로 이동한다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/6658a2cf-341f-4fe4-80f7-5aa3ba71a8ad/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a0c06f88-65c3-45d5-893f-21800cb1f914/image.png" /></p>
<p>왼쪽에 있는 메뉴를 끌어서 <code>pushButton</code> 객체 생성이 가능하다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a05241cf-259f-4af2-85c2-6c5e503eba3f/image.png" /></p>
<p>객체( <code>Class</code> )는 속성, 행동 두 가지를 가진다.
속성에서는 객체의 크기와, 위치 등에 대한 정보를 확인 가능하다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9402a15e-8a6e-40f3-a2d1-7494b61d1535/image.png" /></p>
<p>객체 여러개 만들면 각 개체마다 특징, 속성을 변경 가능하다.
pushButton 이외에도 다른 객체들 생성 가능하고, 지금은 pushButton 하나만 해보자.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b6ea0d0c-29c1-4f77-ad7c-8c267a5d31be/image.png" /></p>
<p>객체가 가지고 있는 또 다른 한 가지는 행동이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7536b9fc-0754-4e6c-ba8c-fbb0232c8161/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5b6df821-7ab8-481b-b395-2fc9cd70e4b0/image.png" /></p>
<p>빌드해보면 위와 같이 나온다.</p>
<p>수정할때마다 빌드를 해서 확인해보자.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/00f5b036-9162-4390-a57c-9566d534a3d0/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/236e16ca-1907-42c1-a4ad-f311ece76b8d/image.png" /></p>
<p>클릭 했을 때 어떻게 동작할지에 대해 확인하기 위해 <code>Go to slot</code> 을 확인해보자.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5f4b8db8-cf64-4e08-8a21-610c6e85379b/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e6ca039e-79c2-4d76-988b-ba3fb2baee84/image.png" /></p>
<p>위와 같은 함수가 생긴 것을 확인 가능하다.</p>
<pre><code class="language-c">#include &quot;mainwindow.h&quot;
#include &quot;./ui_mainwindow.h&quot;

#include &lt;QMessageBox&gt;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui-&gt;setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    QMessageBox::information(this, &quot;Message&quot;,&quot;Hello, World!&quot;);
}</code></pre>
<p>위와 같이 버튼을 눌렀을 때 Message 객체를 통해 Hello, World!를 출력하는 동작을 만들었다. (헤더 파일 <code>QMessageBox</code> 추가 해줄 것)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e5005b9a-3502-4b65-9749-b0079e38849d/image.png" /></p>
<p>클릭 했을 때 Message 객체가 나오고, <code>Ok</code> 버튼 누를 시 객체가 사라지는 것을 확인할 수 있다.</p>
<ul>
<li>콜백함수 ? : </li>
</ul>