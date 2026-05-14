<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1469c6ce-2a1a-43de-9b0f-53e46ecf724a/image.png" /></p>
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#numpy%EB%9E%80">NumPy란</a></li>
<li><a href="https://api.velog.io/rss/@mommers#numpy-vs-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A6%AC%EC%8A%A4%ED%8A%B8">NumPy vs 파이썬 리스트</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%84%A4%EC%B9%98-%EB%B0%8F-%EB%B6%88%EB%9F%AC%EC%98%A4%EA%B8%B0">설치 및 불러오기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B0%B0%EC%97%B4ndarray-%EC%83%9D%EC%84%B1">배열(ndarray) 생성</a><ul>
<li><a href="https://api.velog.io/rss/@mommers#1%EC%B0%A8%EC%9B%90-%EB%B0%B0%EC%97%B4">1차원 배열</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2%EC%B0%A8%EC%9B%90-%EB%B0%B0%EC%97%B4">2차원 배열</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3%EC%B0%A8%EC%9B%90-%EB%B0%B0%EC%97%B4">3차원 배열</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B0%B0%EC%97%B4%EC%9D%98-%EC%86%8D%EC%84%B1-%ED%99%95%EC%9D%B8">배열의 속성 확인</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%8A%B9%EC%88%98-%EB%B0%B0%EC%97%B4-%EC%83%9D%EC%84%B1">특수 배열 생성</a></li>
</ul>
</li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%9D%B8%EB%8D%B1%EC%8B%B1indexing">인덱싱(Indexing)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8A%AC%EB%9D%BC%EC%9D%B4%EC%8B%B1slicing">슬라이싱(Slicing)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B0%B0%EC%97%B4-%ED%98%95%ED%83%9C-%EB%B3%80%ED%99%98--reshape">배열 형태 변환 — Reshape</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%B0%A8%EC%9B%90-%EC%B6%95%EC%86%8C-%EC%97%B0%EC%82%B0">차원 축소 연산</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B0%B0%EC%97%B4-%EC%97%B0%EC%82%B0">배열 연산</a></li>
</ul>
<hr />
<h2 id="numpy란">NumPy란</h2>
<p>NumPy는 <strong>Numerical Python</strong>의 줄임말로, 파이썬에서 수치 계산을 빠르고 효율적으로 수행하기 위한 핵심 라이브러리입니다. </p>
<p>2005년 Travis Oliphant가 개발했으며, 현재 데이터 분석, 머신러닝 등 거의 모든 파이썬 과학 계산 생태계의 기반이 됩니다.</p>
<p>NumPy의 핵심 자료구조는 <code>ndarray</code>(N-dimensional array)입니다. 
파이썬의 기본 리스트와 달리, ndarray는 <strong>모든 원소가 동일한 자료형</strong>을 가지며 <strong>연속된 메모리(contiguous memory)</strong> 에 저장됩니다. 이 구조 덕분에 메모리 효율과 연산 속도가 크게 향상됩니다.</p>
<p><strong>파이썬 리스트와 NumPy ndarray 비교</strong></p>
<table>
<thead>
<tr>
<th>구분</th>
<th>파이썬 리스트</th>
<th>NumPy ndarray</th>
</tr>
</thead>
<tbody><tr>
<td>원소 타입</td>
<td>여러 타입 혼용 가능</td>
<td>동일 타입만 허용</td>
</tr>
<tr>
<td>메모리 구조</td>
<td>linked list</td>
<td>contiguous memory</td>
</tr>
<tr>
<td>연산 속도</td>
<td>느림</td>
<td>빠름 (C 구현)</td>
</tr>
<tr>
<td>벡터화 연산</td>
<td>불가</td>
<td>가능</td>
</tr>
</tbody></table>
<blockquote>
<p>NumPy는 고속 수치 연산에 최적화되어 있지만, 고수준 데이터 분석 기능은 제공하지 않습니다. 실제 데이터 분석은 NumPy를 기반으로 하는 Pandas를 함께 사용합니다.</p>
</blockquote>
<hr />
<h2 id="numpy-vs-파이썬-리스트">NumPy vs 파이썬 리스트</h2>
<p>NumPy가 얼마나 빠른지 직접 측정한 결과입니다. 1,000개 원소에 대해 제곱 연산을 수행했을 때의 속도 차이입니다.</p>
<pre><code class="language-python">import numpy as np

# NumPy 배열 연산
arr = np.arange(1000)
%timeit a2 = arr**2
# 결과: 1.07 μs ± 108 ns per loop

# 파이썬 리스트 컴프리헨션
L = range(1000)
%timeit L2 = [i**2 for i in L]
# 결과: 52.6 μs ± 2.08 μs per loop</code></pre>
<blockquote>
<p>NumPy 배열 연산이 파이썬 리스트 컴프리헨션보다 약 <strong>73배</strong> 빠릅니다. NumPy의 핵심이 C로 구현되어 저수준 최적화를 활용하는 반면, 파이썬 리스트는 인터프리터가 순차 실행하기 때문에 발생하는 차이입니다.</p>
</blockquote>
<hr />
<h2 id="설치-및-불러오기">설치 및 불러오기</h2>
<pre><code class="language-python"># 설치
pip install numpy

# 불러오기 — np라는 별칭(alias) 사용이 관례입니다
import numpy as np</code></pre>
<p><code>numpy</code>를 매번 전체 이름으로 쓰는 대신 <code>np</code>로 줄여 사용하는 것이 파이썬 커뮤니티의 표준 관례입니다.</p>
<hr />
<h2 id="배열ndarray-생성">배열(ndarray) 생성</h2>
<p><code>np.array()</code> 함수에 파이썬 리스트를 넣으면 ndarray로 변환됩니다. 다차원 배열의 데이터 방향은 <code>axis</code>로 표현하며, 행 방향은 <code>axis=0</code>, 열 방향은 <code>axis=1</code>, 채널 방향은 <code>axis=2</code>로 지정합니다.</p>
<h3 id="1차원-배열">1차원 배열</h3>
<pre><code class="language-python">arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
arr
# 출력: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

type(arr)
# 출력: numpy.ndarray

arr.dtype
# 출력: dtype('int64')</code></pre>
<p>기존 파이썬 리스트를 <code>np.array()</code>로 감싸면 ndarray로 변환됩니다.</p>
<pre><code class="language-python">data1 = [1, 2, 3, 4, 5]   # 파이썬 리스트
arr1 = np.array(data1)     # ndarray로 변환
arr1
# 출력: array([1, 2, 3, 4, 5])</code></pre>
<h3 id="2차원-배열">2차원 배열</h3>
<p>2차원 배열은 행렬(matrix)로, 가로줄(row)과 세로줄(column)로 구성됩니다. 리스트 안에 리스트를 중첩하여 생성합니다.</p>
<pre><code class="language-python"># 2행 × 3열 2차원 배열 생성
c = np.array([[0, 1, 2], [3, 4, 5]])
c
# 출력:
# array([[0, 1, 2],
#        [3, 4, 5]])</code></pre>
<h3 id="3차원-배열">3차원 배열</h3>
<p>3차원 배열은 리스트를 한 단계 더 중첩하여 만듭니다. shape는 <strong>바깥쪽 리스트 길이부터 가장 안쪽 순서</strong>로 표시됩니다.</p>
<pre><code class="language-python"># 2 × 3 × 4 배열 생성
d = np.array([[[1,  2,  3,  4],
               [5,  6,  7,  8],
               [9, 10, 11, 12]],
              [[11, 12, 13, 14],
               [15, 16, 17, 18],
               [19, 20, 21, 22]]])
# shape: (2, 3, 4)</code></pre>
<h3 id="배열의-속성-확인">배열의 속성 확인</h3>
<p>ndarray는 배열의 구조를 확인하는 주요 속성을 제공합니다.</p>
<table>
<thead>
<tr>
<th>속성</th>
<th>설명</th>
<th>예시 결과</th>
</tr>
</thead>
<tbody><tr>
<td><code>.ndim</code></td>
<td>차원 수(축의 개수)</td>
<td><code>1</code>, <code>2</code>, <code>3</code></td>
</tr>
<tr>
<td><code>.shape</code></td>
<td>각 차원의 크기 (tuple)</td>
<td><code>(3,)</code>, <code>(2, 3)</code>, <code>(2, 3, 4)</code></td>
</tr>
<tr>
<td><code>.size</code></td>
<td>전체 원소 개수</td>
<td><code>3</code>, <code>6</code>, <code>24</code></td>
</tr>
<tr>
<td><code>.dtype</code></td>
<td>원소의 자료형</td>
<td><code>dtype('int64')</code>, <code>dtype('float64')</code></td>
</tr>
</tbody></table>
<pre><code class="language-python">ab = np.array([1, 2, 3])

ab.ndim    # 1
ab.shape   # (3,)
ab.size    # 3
ab.dtype   # dtype('int64')</code></pre>
<pre><code class="language-python">abc = np.array([[0, 1, 2], [3, 4, 5]])

print(abc.ndim)   # 2
print(abc.shape)  # (2, 3)</code></pre>
<blockquote>
<p><code>shape</code>는 데이터의 형태를 파악하는 가장 기본적인 명령입니다. 머신러닝에서 입력 데이터의 차원을 확인할 때 가장 자주 사용하게 됩니다.</p>
</blockquote>
<h3 id="특수-배열-생성">특수 배열 생성</h3>
<p>특정 값으로 초기화된 배열을 빠르게 만드는 함수들입니다.</p>
<p><strong><code>np.zeros()</code> — 모든 원소가 0인 배열</strong></p>
<pre><code class="language-python">zero_matrix = np.zeros((3, 3))
print(zero_matrix)
# 출력:
# [[0. 0. 0.]
#  [0. 0. 0.]
#  [0. 0. 0.]]</code></pre>
<p><strong><code>np.ones()</code> — 모든 원소가 1인 배열</strong></p>
<pre><code class="language-python">one_matrix = np.ones((3, 3))
print(one_matrix)
# 출력:
# [[1. 1. 1.]
#  [1. 1. 1.]
#  [1. 1. 1.]]</code></pre>
<p><strong><code>np.zeros()</code>로 초기화 후 값 채우기</strong></p>
<pre><code class="language-python">data = np.zeros(10)
for i in range(10):
    data[i] = i * 2
print(data)
# 출력: [ 0.  2.  4.  6.  8. 10. 12. 14. 16. 18.]</code></pre>
<p><strong><code>np.arange()</code> — 범위 기반 배열 생성</strong></p>
<p><code>arange()</code>는 파이썬의 <code>range()</code>와 동일한 방식으로 동작하며, 결과는 ndarray입니다.</p>
<pre><code class="language-python">a = np.arange(12)
# 출력: array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])</code></pre>
<hr />
<h2 id="인덱싱indexing">인덱싱(Indexing)</h2>
<p>1차원 배열은 파이썬 리스트와 동일한 방식으로 인덱싱합니다. 음수 인덱스도 사용 가능합니다.</p>
<pre><code class="language-python">a = np.array([0, 1, 2, 3, 4])

a[2]   # 2
a[-1]  # 4 (마지막 원소)</code></pre>
<p>2차원 배열은 <code>[행, 열]</code> 형태로 접근합니다.</p>
<pre><code class="language-python">b = np.array([[0, 1, 2],
              [3, 4, 5]])

b[0, 0]   # 0  (0행 0열)
b[0, 1]   # 1  (0행 1열)
b[-1, -1] # 5  (마지막 행, 마지막 열)</code></pre>
<blockquote>
<p>2차원 배열에서 <code>b[0][1]</code> 대신 <code>b[0, 1]</code> 형태로 쓰는 것이 NumPy의 표준 방식입니다. 성능도 더 좋습니다.</p>
</blockquote>
<hr />
<h2 id="슬라이싱slicing">슬라이싱(Slicing)</h2>
<p>리스트 슬라이싱과 동일한 <code>[start:end]</code> 문법을 사용하며, 2차원 이상에서는 각 축에 대해 독립적으로 슬라이싱할 수 있습니다.</p>
<pre><code class="language-python">a = np.array([[0, 1, 2, 3],
              [4, 5, 6, 7]])

a[0, :]    # array([0, 1, 2, 3])  — 0행 전체
a[1, 1:]   # array([5, 6, 7])    — 1행의 1열부터 끝까지
a[:2, :2]  # array([[0, 1],      — 2행까지, 2열까지
           #         [4, 5]])</code></pre>
<p><strong>슬라이싱 실습 예제</strong></p>
<pre><code class="language-python">m = np.array([[ 0,  1,  2,  3,  4],
              [ 5,  6,  7,  8,  9],
              [10, 11, 12, 13, 14]])

m[1, 2]       # 7       — 인덱싱
m[2, 4]       # 14      — 인덱싱
m[1, 1:3]     # [6, 7]  — 슬라이싱
m[0:2, 2]     # [2, 7]  — 열 방향 슬라이싱
m[0:2, 3:5]   # [[3, 4], [8, 9]]</code></pre>
<hr />
<h2 id="배열-형태-변환--reshape">배열 형태 변환 — Reshape</h2>
<p><code>reshape()</code>는 배열의 <strong>내부 데이터는 그대로 유지</strong>하면서 형태(shape)만 변환합니다. 원소 총 개수가 동일해야 합니다.</p>
<pre><code class="language-python">a = np.arange(12)
# array([ 0,  1,  2, ..., 11])

b = a.reshape(3, 4)
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]])</code></pre>
<p><strong><code>-1</code> 사용 — 나머지 크기 자동 계산</strong></p>
<p>한 축의 크기를 <code>-1</code>로 지정하면 NumPy가 나머지 크기를 자동으로 계산합니다.</p>
<pre><code class="language-python">b.reshape(3, -1)   # (3, 4) — 4를 명시하지 않아도 자동 계산
b.reshape(2, -1, 2)  # (2, 3, 2) — 3차원으로 변환</code></pre>
<p><strong>다차원 배열 변환 예시</strong></p>
<pre><code class="language-python">arr = np.arange(1, 13).reshape((2, 2, 3))
reshaped = np.reshape(arr, (4, 3))
# 3차원 (2×2×3) → 2차원 (4×3)으로 변환</code></pre>
<p><strong>1차원으로 펼치기 — <code>flatten()</code> / <code>ravel()</code></strong></p>
<pre><code class="language-python">b.flatten()  # 1차원 배열의 복사본 반환
b.ravel()    # 1차원 배열 반환 (가능하면 원본 참조)
# 결과: array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])</code></pre>
<blockquote>
<p><code>flatten()</code>은 항상 복사본을 반환하고, <code>ravel()</code>은 가능하면 원본 배열을 참조합니다. 메모리 절약이 필요할 때는 <code>ravel()</code>을 사용합니다.</p>
</blockquote>
<hr />
<h2 id="차원-축소-연산">차원 축소 연산</h2>
<p>차원 축소 연산은 배열의 원소들을 집계하여 더 낮은 차원의 결과를 반환합니다.</p>
<p><strong>주요 집계 메서드</strong></p>
<table>
<thead>
<tr>
<th>메서드</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>sum()</code></td>
<td>합계</td>
</tr>
<tr>
<td><code>min()</code> / <code>max()</code></td>
<td>최솟값 / 최댓값</td>
</tr>
<tr>
<td><code>argmin()</code> / <code>argmax()</code></td>
<td>최솟값 / 최댓값의 인덱스</td>
</tr>
<tr>
<td><code>mean()</code></td>
<td>평균</td>
</tr>
<tr>
<td><code>median()</code></td>
<td>중앙값</td>
</tr>
<tr>
<td><code>std()</code></td>
<td>표준편차</td>
</tr>
<tr>
<td><code>var()</code></td>
<td>분산</td>
</tr>
</tbody></table>
<pre><code class="language-python">x = np.array([1, 2, 3, 4])

np.sum(x)   # 10  — 함수 형태
x.sum()     # 10  — 메서드 형태 (권장)
x.min()     # 1
x.max()     # 4
x.mean()    # 2.5</code></pre>
<blockquote>
<p><code>np.sum(x)</code>와 <code>x.sum()</code>은 동일한 결과를 반환합니다. 메서드 형태인 <code>x.sum()</code>이 더 간결하여 일반적으로 선호됩니다.</p>
</blockquote>
<p><strong><code>axis</code> 인수로 방향 지정</strong></p>
<p>2차원 배열에서 <code>axis</code>를 지정하면 행 방향 또는 열 방향으로 집계할 수 있습니다.</p>
<pre><code class="language-python">arr = np.array([[1, 2, 3],
                [4, 5, 6]])

arr.sum()         # 21       — 전체 합계
arr.sum(axis=0)   # [5, 7, 9]  — 열 방향 합계 (행 축 제거)
arr.sum(axis=1)   # [6, 15]    — 행 방향 합계 (열 축 제거)</code></pre>
<hr />
<h2 id="배열-연산">배열 연산</h2>
<p>NumPy 배열은 <strong>원소 단위(element-wise)</strong> 로 연산이 수행됩니다. 파이썬 리스트는 <code>-</code> 연산이 지원되지 않지만, ndarray는 모든 사칙연산이 가능합니다.</p>
<pre><code class="language-python">arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

arr1 + arr2   # array([5, 7, 9])
arr1 - arr2   # array([-3, -3, -3])
arr1 * arr2   # array([ 4, 10, 18])
arr1 / arr2   # array([0.25, 0.4, 0.5])</code></pre>
<p><strong>행렬 곱셈 — element-wise vs 행렬곱</strong></p>
<pre><code class="language-python">arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

arr1 * arr2          # element-wise 곱 (np.multiply)
arr1 @ arr2          # 행렬 곱 (np.matmul)
# 행렬 곱 결과:
# array([[19, 22],
#        [43, 50]])</code></pre>
<blockquote>
<p><code>*</code>는 원소끼리의 곱이고, <code>@</code>는 수학적 행렬 곱셈입니다. 선형대수 계산에서는 <code>@</code> 연산자를 사용합니다.</p>
</blockquote>
<p><strong>조건 기반 마스크 연산</strong></p>
<pre><code class="language-python">data = np.array([[5, 7, 9], [4, 3, 8], [6, 1, 2]])

# 5보다 큰 원소만 선택
mask = np.zeros(data.shape)
mask[data &gt; 5] = 1
selected = data[mask == 1]
print(selected)  # [7 9 8 6]</code></pre>