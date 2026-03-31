<p>일주일 동안 하루에 1.5단원 ~ 2단원을 나가면서, 각각 한 단원씩 나갈때는 괜찮았는데, 10단원이 다 쌓이고 나니까 잘 안다고 생각했던 부분도 기억이 안나는 부분이 있고, 진도는 나갔으나 아예 놓쳤던 부분도 있더라구요.
이번 글에서는 지금까지 진도 나갔던 부분에 대한 간단한 쪽지 시험 코드 리뷰를 하려고 합니다.</p>
<hr />
<p><strong>📝 Github Link</strong> : <a href="https://github.com/kyoung-mo/cpp/blob/main/kym_oop_exam.cpp">kym_oop_exam.cpp</a></p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/75ef03d9-ad47-4845-929a-c6b3fb1b03a2/image.png" /></p>
<h3 id="문제-요구사항">문제 요구사항</h3>
<ul>
<li><code>Animal</code> 추상 클래스를 작성하고, 순수 가상 함수 <code>crying()</code>을 선언할 것</li>
<li><code>Dog</code>, <code>Cat</code> 파생 클래스를 구현하고 <code>crying()</code>을 각각 오버라이딩할 것</li>
<li>멤버 변수는 <code>private</code>으로 선언하고, getter/setter를 통해 접근할 것</li>
<li>디폴트 매개변수를 가진 생성자와 복사 생성자를 직접 구현할 것</li>
<li>소멸자에 <code>virtual</code> 키워드를 붙일 것</li>
<li><code>friend</code> 함수 <code>running(Animal*)</code>을 선언하고 전역 함수 <code>run(Animal*)</code>에서 호출할 것</li>
<li>전역 함수 <code>run()</code>으로 다형성을 구현할 것</li>
<li><code>main()</code> 함수 수정 금지</li>
</ul>
<pre><code class="language-c">int main() {
    cout &lt;&lt; &quot;--추상클래스와 파생 클래스 구현--\n&quot;;
    Dog* dog = new Dog(&quot;강아지&quot;, 4, &quot;멍멍&quot;);
    Cat* cat = new Cat(&quot;고양이&quot;, 2, &quot;야옹&quot;);

    cout &lt;&lt; &quot;--매개 변수의 다형성 구현--\n&quot;;
    run(dog);
    run(cat);

    cout &lt;&lt; &quot;\n--복사생성자 직접 구현--\n&quot;;
    Dog copyDog(*dog);
    cout &lt;&lt; copyDog.getName() &lt;&lt; endl;
    cout &lt;&lt; copyDog.getAge() &lt;&lt; endl;
    cout &lt;&lt; copyDog.getBark() &lt;&lt; endl;

    cout &lt;&lt; &quot;\n--소멸자 실행--\n&quot;;
    delete dog;
    delete cat;
    return 0;

}</code></pre>
<hr />
<h3 id="코드-리뷰">코드 리뷰</h3>
<p><strong>1. 순수 가상 함수와 추상 클래스</strong></p>
<pre><code class="language-cpp">virtual void crying() = 0;</code></pre>
<p><code>= 0</code>을 붙이면 순수 가상 함수가 되고, 해당 클래스는 추상 클래스가 됩니다. <code>Animal</code> 객체는 직접 생성할 수 없고, 파생 클래스에서 반드시 구현해야 합니다.</p>
<p><strong>2. 가상 소멸자</strong></p>
<pre><code class="language-cpp">virtual ~Animal() { cout &lt;&lt; &quot;Animal 소멸&quot; &lt;&lt; endl; }</code></pre>
<p><code>Animal*</code> 포인터로 <code>delete</code>를 호출할 때, <code>virtual</code>이 없으면 파생 클래스의 소멸자가 호출되지 않아 메모리 누수가 발생합니다. <code>virtual</code>을 붙이면 <code>Dog 소멸 → Animal 소멸</code> 순서로 정상 호출됩니다.</p>
<p><strong>3. 파생 클래스 생성자에서 부모 생성자 명시 호출</strong></p>
<pre><code class="language-cpp">Dog(string name = &quot;&quot;, int age = 0, string bark = &quot;&quot;) : Animal(name, age)</code></pre>
<p><code>name</code>, <code>age</code>는 <code>Animal</code>의 <code>private</code> 멤버이므로 <code>Dog</code>에서 직접 접근이 불가능합니다. 초기화 리스트에서 <code>: Animal(name, age)</code>로 부모 생성자를 명시 호출해 부모 영역 초기화를 위임합니다.</p>
<p><strong>4. 파생 클래스 복사 생성자</strong></p>
<pre><code class="language-cpp">Dog(const Dog&amp; dog) : Animal(dog)
{
    this-&gt;bark = dog.bark;
}</code></pre>
<p><code>: Animal(dog)</code>를 생략하면, <code>Animal</code>의 기본 생성자 <code>Animal(&quot;&quot;, 0)</code>이 호출되어 <code>name</code>과 <code>age</code>가 빈 값으로 초기화됩니다. 부모 영역까지 올바르게 복사하려면 부모 복사 생성자를 명시 호출해야 합니다.</p>
<p><strong>5. friend 함수와 다형성</strong></p>
<pre><code class="language-cpp">friend void running(Animal* animal);

void run(Animal* animal)
{
    running(animal);
    animal-&gt;crying();
}</code></pre>
<p><code>running()</code>은 <code>Animal</code>의 <code>private</code> 멤버 <code>name</code>에 직접 접근하기 위해 <code>friend</code>로 선언했습니다. <code>run()</code>은 <code>Animal*</code>를 인자로 받기 때문에 <code>Dog*</code>, <code>Cat*</code>가 들어오면 업캐스팅이 일어나고, <code>animal-&gt;crying()</code>은 가상 함수 테이블을 통해 실제 타입의 <code>crying()</code>을 호출합니다.</p>
<hr />
<h3 id="시험-후기">시험 후기</h3>
<p>단원별로 배울 때는 각각의 개념이 명확하게 느껴졌는데, 막상 한 코드에 몰아서 쓰려니 어디에 <code>virtual</code>을 붙여야 하는지, 초기화 리스트에서 부모 생성자를 언제 명시 호출해야 하는지 헷갈리는 부분이 있었습니다. 특히 복사 생성자에서 <code>: Animal(dog)</code>를 빠뜨리면 부모 영역이 빈 값으로 초기화된다는 점을 실수하기 쉬웠습니다. 개념 하나하나보다는 이것들이 한 코드 안에서 어떻게 맞물리는지를 직접 작성해보는 연습이 필요하다고 느꼈습니다.</p>