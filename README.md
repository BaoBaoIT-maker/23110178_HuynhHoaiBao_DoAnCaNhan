# Báo Cáo Project Game 8 Ô Chữ

## 1. Mục tiêu

Project này nhằm mục đích xây dựng một ứng dụng trò chơi 8 ô chữ (8-puzzle) và triển khai, trực quan hóa các thuật toán tìm kiếm khác nhau để giải quyết bài toán này. Mục tiêu bao gồm:
* Hiểu rõ và triển khai các thành phần cơ bản của một bài toán tìm kiếm.
* Áp dụng và so sánh hiệu suất của các nhóm thuật toán tìm kiếm:
    * Tìm kiếm không có thông tin (Uninformed Search)
    * Tìm kiếm có thông tin (Informed Search)
    * Tìm kiếm cục bộ (Local Search)
    * Các thuật toán cho môi trường phức tạp (Complex Environment Search)
    * Tìm kiếm đường đi với ràng buộc (Constrained Pathfinding)
    * Học tăng cường (Reinforcement Learning)
* Cung cấp một giao diện đồ họa để người dùng có thể tương tác, thiết lập trạng thái ban đầu, chọn thuật toán và quan sát quá trình giải đố.
* Đánh giá ưu nhược điểm của từng thuật toán khi áp dụng vào game 8 ô chữ.

## 2. Hướng dẫn sử dụng

1.  **Chạy chương trình:**
    * Đảm bảo bạn đã cài đặt Python và Pygame.
    * Tải xuống file mã nguồn

2.  **Giao diện chính:**
    * **Bảng Trạng thái Ban đầu (Initial State):** Hiển thị cấu hình hiện tại của bảng 8 ô chữ sẽ được dùng làm điểm xuất phát cho các thuật toán. Khi khởi động, một trạng thái mặc định sẽ được tải hoặc bạn sẽ được hỏi để nhập trạng thái.
    * **Bảng Trạng thái Đích (Goal State):** Hiển thị cấu hình đích mà các thuật toán cố gắng đạt tới (thường là `1, 2, 3 / 4, 5, 6 / 7, 8, 0`).
    * **Danh sách thuật toán:** Bên trái màn hình, các thuật toán được nhóm theo loại. Nhấn vào tên một thuật toán để chọn nó. Thuật toán được chọn sẽ được làm nổi bật.
    * **Các nút điều khiển:**
        * **Run:** Sau khi chọn một thuật toán, nhấn nút "Run" để bắt đầu quá trình tìm kiếm/huấn luyện.
        * **Solution:** Sau khi một thuật toán (không phải mô phỏng môi trường phức tạp hoặc RL đang huấn luyện) đã chạy và tìm thấy lời giải, nhấn nút này để xem chi tiết các bước đi trong một cửa sổ mới.
        * **Reset:** Đặt lại trạng thái của trò chơi, xóa lời giải hiện tại, hủy chọn thuật toán và đặt lại bảng về trạng thái ban đầu đã thiết lập. Nếu đang trong quá trình huấn luyện RL hoặc mô phỏng phức tạp, nút này có thể yêu cầu xác nhận hoặc không hoạt động cho đến khi quá trình đó dừng.
    * **Khu vực hiển thị kết quả/mô phỏng:** Bên phải màn hình, khu vực này sẽ hiển thị:
        * Thông tin văn bản về quá trình chạy thuật toán, kết quả, hoặc các bước giải thích (cho các thuật toán phức tạp).
        * Trực quan hóa các mô phỏng cho nhóm "Complex Environment Search".

3.  **Thiết lập Trạng thái Ban đầu:**
    * Khi chương trình khởi động lần đầu, bạn sẽ được hỏi có muốn sử dụng trạng thái mặc định hay nhập trạng thái riêng.
    * Nếu chọn nhập, một hộp thoại sẽ xuất hiện. Nhập trạng thái theo định dạng: 3 số cho hàng đầu tiên, dấu cách, dấu gạch chéo (`/`), dấu cách, 3 số cho hàng thứ hai, v.v. Ví dụ: `1 2 3 / 4 0 5 / 6 7 8` (trong đó `0` là ô trống).
    * Chương trình sẽ kiểm tra tính hợp lệ và khả năng giải được của trạng thái bạn nhập.

4.  **Chọn và Chạy thuật toán:**
    * Nhấn vào tên thuật toán bạn muốn thử nghiệm từ danh sách bên trái.
    * Nhấn nút "Run".
    * Quan sát bảng "Initial State" thay đổi nếu thuật toán có khả năng hiển thị từng bước (ví dụ: A\*, BFS).
    * Theo dõi thông tin ở khu vực kết quả/mô phỏng. Thời gian giải và số bước (nếu có) sẽ được cập nhật.

5.  **Xem lời giải:**
    * Sau khi một thuật toán tìm kiếm đường đi hoàn thành, nhấn nút "Solution".
    * Một cửa sổ mới sẽ hiện ra, hiển thị từng bước đi từ trạng thái ban đầu đến trạng thái đích. Sử dụng thanh cuộn chuột để xem tất cả các bước nếu chúng không vừa với cửa sổ. Đóng cửa sổ này để quay lại giao diện chính.

6.  **Các thuật toán đặc biệt:**
    * **Complex Environment Search (AND-OR, Sensorless, PartiallyObs):** Khi chọn các thuật toán này và nhấn "Run", khu vực bên phải sẽ chuyển sang chế độ mô phỏng tương ứng.
        * **AND-OR Sim:** Nhấn nút "Solve Next 'Easiest' Subgoal" để xem thuật toán giải quyết từng phần của bài toán.
        * **Sensorless/PartiallyObs Sim:** Mô phỏng sẽ tự động chạy. Bạn có thể nhấn `SPACE` để tạm dừng/tiếp tục và `R` để reset mô phỏng đó.
    * **Reinforcement Learning (Q-Learning, TD Learning):**
        * Nhấn "Run" sẽ bắt đầu quá trình huấn luyện. Một lớp phủ "RL Training in Progress..." sẽ xuất hiện. Quá trình này có thể mất thời gian.
        * Theo dõi thông tin huấn luyện ở khu vực kết quả.
        * Sau khi huấn luyện xong (hoặc bị ngắt), nếu thành công, thuật toán sẽ cố gắng giải puzzle bằng chính sách đã học, và bạn có thể xem lời giải nếu nó tìm được đích.

7.  **Lưu ý:**
    * Một số thuật toán (đặc biệt là DFS không giới hạn, hoặc các thuật toán tìm kiếm cục bộ) có thể mất nhiều thời gian hoặc không tìm thấy lời giải tối ưu/bất kỳ lời giải nào.
    * Nút "Reset" rất quan trọng để thử nghiệm các thuật toán khác nhau hoặc chạy lại một thuật toán với thiết lập mới.
    * Nếu giao diện có vẻ không phản hồi trong khi một thuật toán đang chạy, hãy kiên nhẫn chờ hoặc kiểm tra cửa sổ console/terminal để xem có thông báo lỗi nào không. Các thuật toán dài đã được thêm cơ chế kiểm tra sự kiện thoát để giảm thiểu tình trạng treo hoàn toàn.

## 3. Nội dung Chi tiết

### 3.1. Bài toán Tìm kiếm và Trò chơi 8 Ô Chữ

**Các thành phần chính của bài toán tìm kiếm trong game 8 ô chữ:**

1.  **Không gian trạng thái (State Space):** Tập hợp tất cả các cấu hình (arrangements) có thể có của các ô trên bảng 8 ô chữ. Mỗi cấu hình là một trạng thái. Ví dụ, một trạng thái có thể là `[[1, 2, 3], [4, 0, 5], [6, 7, 8]]` trong đó `0` đại diện cho ô trống. Kích thước không gian trạng thái là 9! = 362,880.
2.  **Trạng thái ban đầu (Initial State):** Cấu hình xuất phát của trò chơi do người dùng thiết lập hoặc một trạng thái mặc định. Đây là điểm khởi đầu của quá trình tìm kiếm.
3.  **Hành động (Actions):** Các phép toán (operators) có thể thực hiện để chuyển từ trạng thái này sang trạng thái khác. Trong game 8 ô chữ, hành động là di chuyển ô trống (số 0) theo các hướng: Lên (UP), Xuống (DOWN), Trái (LEFT), Phải (RIGHT). Một hành động chỉ hợp lệ nếu ô trống không di chuyển ra ngoài biên của bảng.
4.  **Hàm chuyển trạng thái (Transition Model):** Được định nghĩa bởi `RESULT(s, a) -> s'`. Nó mô tả trạng thái `s'` là kết quả của việc thực hiện hành động `a` tại một trạng thái `s` cụ thể. Ví dụ, nếu ô trống ở vị trí `(r, c)` và hành động là `UP`, trạng thái mới sẽ là ô trống di chuyển đến `(r-1, c)` và ô ở `(r-1, c)` di chuyển đến `(r, c)`.
5.  **Trạng thái đích (Goal State):** Một hoặc nhiều trạng thái mà bài toán cần đạt được. Trong game 8 ô chữ, trạng thái đích thường là một cấu hình được sắp xếp theo thứ tự nhất định, ví dụ: `[[1, 2, 3], [4, 5, 6], [7, 8, 0]]`. Hàm kiểm tra đích (Goal Test) xác định xem một trạng thái có phải là trạng thái đích hay không.
6.  **Chi phí đường đi (Path Cost):** Một hàm gán giá trị số cho một đường đi (một chuỗi các hành động). Trong trường hợp đơn giản nhất của game 8 ô chữ, mỗi bước di chuyển (hành động) có chi phí là 1. Tổng chi phí của một đường đi là số bước di chuyển trong đường đi đó.

**Solution (Lời giải) là gì?**

Một **solution** cho bài toán 8 ô chữ là một **chuỗi các hành động (sequence of actions)** hợp lệ dẫn từ **trạng thái ban đầu** đến **trạng thái đích**. Một **solution tối ưu (optimal solution)** là solution có chi phí đường đi thấp nhất.

### 3.2. Các thuật toán Tìm kiếm không có thông tin (Uninformed Search / Blind Search)

**Đặc trưng của nhóm:**
Các thuật toán này được gọi là "mù" (blind) vì chúng không sử dụng bất kỳ thông tin nào về bài toán ngoài định nghĩa của nó. Chúng không biết một trạng thái không phải đích "tốt" hay "hứa hẹn" như thế nào so với trạng thái khác. Chiến lược tìm kiếm của chúng chỉ dựa trên thứ tự duyệt các nút trong không gian trạng thái. Chúng chỉ có thể phân biệt được trạng thái đích và các trạng thái không phải đích.

**Các thuật toán được triển khai:**

* **Tìm kiếm theo chiều rộng (Breadth-First Search - BFS):**
    * **Nguyên lý:** BFS mở rộng các nút theo từng lớp (level) của cây tìm kiếm. Nó bắt đầu từ nút gốc (trạng thái ban đầu), sau đó duyệt tất cả các nút con trực tiếp của nút gốc, rồi đến tất cả các nút cháu, và cứ thế tiếp tục. Nó sử dụng một hàng đợi (queue - FIFO) để quản lý các nút sẽ được duyệt. Nút được đưa vào hàng đợi trước sẽ được lấy ra và mở rộng trước.
    * **Solution:** Đảm bảo tìm thấy lời giải nông nhất (có số bước ít nhất) nếu một lời giải tồn tại. BFS là thuật toán đầy đủ (complete) và tối ưu (optimal) nếu chi phí mỗi bước là như nhau.
* **Tìm kiếm theo chiều sâu (Depth-First Search - DFS):**
    * **Nguyên lý:** DFS luôn mở rộng nút sâu nhất trong nhánh hiện tại của cây tìm kiếm. Nó đi sâu vào một đường đi cho đến khi gặp trạng thái đích hoặc đến một nút không có con cháu nào chưa được duyệt (ngõ cụt). Khi đó, nó quay lui (backtrack) lên nút cha và thử một nhánh khác. DFS thường được triển khai bằng cách sử dụng một ngăn xếp (stack - LIFO).
    * **Solution:** Tìm một đường đi bất kỳ đến đích. Không đảm bảo tìm thấy lời giải tối ưu (ngắn nhất). Có thể bị kẹt trong các nhánh vô hạn nếu không gian trạng thái có chu trình hoặc nhánh vô hạn và không có giới hạn độ sâu.
* **Tìm kiếm chi phí đồng nhất (Uniform-Cost Search - UCS):**
    * **Nguyên lý:** UCS mở rộng nút `n` chưa được duyệt có chi phí đường đi `g(n)` (chi phí từ trạng thái ban đầu đến `n`) thấp nhất. Nó sử dụng một hàng đợi ưu tiên (priority queue) để lưu trữ các nút biên, với độ ưu tiên được xác định bởi `g(n)`.
    * **Solution:** Đảm bảo tìm thấy lời giải có tổng chi phí thấp nhất. UCS là thuật toán đầy đủ và tối ưu. Khi tất cả các chi phí bước là như nhau (ví dụ, bằng 1 như trong 8-puzzle cơ bản), UCS hoạt động tương tự như BFS.
* **Tìm kiếm sâu dần (Iterative Deepening Search - IDS):**
    * **Nguyên lý:** IDS là một chiến lược kết hợp lợi ích của BFS và DFS. Nó thực hiện một loạt các tìm kiếm giới hạn độ sâu (Depth-Limited Search - DLS). Bắt đầu với giới hạn độ sâu là 0, sau đó là 1, 2, và cứ thế tăng dần. Trong mỗi lần lặp DLS, nó thực hiện một DFS hoàn chỉnh đến độ sâu giới hạn đó.
    * **Solution:** Giống như BFS, IDS đầy đủ và tối ưu (nếu chi phí bước là 1). Nó có yêu cầu bộ nhớ thấp như DFS (O(bd) với b là yếu tố rẽ nhánh, d là độ sâu của lời giải) nhưng có thể phải duyệt lại các nút ở các mức trên nhiều lần.

**Hình ảnh GIF minh họa:**

Thuật toán BFS:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/BFS.gif?raw=true)

Thuật toán DFS:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/DFS.gif?raw=true)

Thuật toán UCS:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/UCS.gif?raw=true)

Thuật toán IDS:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/IDS.gif?raw=true)


**So sánh hiệu suất (dự kiến):**

* **(Chèn hình ảnh/bảng so sánh hiệu suất của BFS, DFS, UCS, IDS về thời gian chạy, số bước, số nút đã duyệt cho một vài trạng thái ban đầu khác nhau tại đây)**

**Nhận xét về hiệu suất:**

* **BFS và IDS:** Thường tìm thấy lời giải tối ưu (về số bước). BFS có thể tốn nhiều bộ nhớ do phải lưu trữ tất cả các nút ở biên (fringe). IDS hiệu quả hơn về bộ nhớ so với BFS nhưng phải duyệt lại các nút ở các độ sâu trước đó, dẫn đến thời gian chạy có thể lớn hơn một chút, mặc dù bậc độ phức tạp thời gian vẫn tương đương BFS.
* **DFS:** Có thể tìm thấy lời giải rất nhanh nếu may mắn đi đúng hướng, nhưng cũng có thể rất chậm hoặc không tìm thấy lời giải (nếu không giới hạn độ sâu và cây tìm kiếm có nhánh vô hạn hoặc chu trình). Thường không tối ưu. Yêu cầu bộ nhớ thấp (O(bm) với m là độ sâu tối đa của không gian trạng thái).
* **UCS:** Tương tự BFS khi chi phí mỗi bước là 1. Đảm bảo tìm lời giải có chi phí thấp nhất ngay cả khi chi phí các bước khác nhau. Độ phức tạp thời gian và không gian có thể lớn.
* Đối với game 8 ô chữ, không gian trạng thái không quá lớn. BFS và IDS thường là lựa chọn tốt nếu cần lời giải tối ưu về số bước. DFS có thể được sử dụng nếu chỉ cần tìm một lời giải bất kỳ và bộ nhớ là vấn đề chính.

### 3.3. Các thuật toán Tìm kiếm có thông tin (Informed Search / Heuristic Search)

**Đặc trưng của nhóm:**
Các thuật toán này sử dụng kiến thức đặc thù của bài toán, ngoài định nghĩa của bài toán, để hướng dẫn quá trình tìm kiếm một cách hiệu quả hơn. Thông tin này thường được cung cấp dưới dạng một **hàm heuristic `h(n)`**. Hàm heuristic ước tính chi phí từ trạng thái hiện tại `n` đến trạng thái đích gần nhất. Mục tiêu là chọn nút có vẻ "hứa hẹn" nhất để mở rộng, dựa trên đánh giá của hàm heuristic. Một heuristic tốt có thể giảm đáng kể số lượng nút cần duyệt so với tìm kiếm không có thông tin.

**Hàm Heuristic sử dụng trong project:**
Trong project này, hàm heuristic chính được sử dụng là **Khoảng cách Manhattan (Manhattan Distance)**.
* **Định nghĩa:** Với mỗi ô (không tính ô trống), tính tổng số bước di chuyển theo chiều ngang và chiều dọc cần thiết để đưa ô đó từ vị trí hiện tại về vị trí đúng của nó trong trạng thái đích. Tổng các khoảng cách này cho tất cả các ô sai vị trí là giá trị heuristic của trạng thái hiện tại.
* **Tính chất:** Khoảng cách Manhattan là một heuristic **chấp nhận được (admissible)** cho bài toán 8-puzzle, nghĩa là nó không bao giờ đánh giá quá cao chi phí thực tế để đạt được đích. Điều này quan trọng cho tính tối ưu của thuật toán A\*. Nó cũng là một heuristic **nhất quán (consistent/monotonic)**.

**Các thuật toán được triển khai:**

* **Tìm kiếm Tham lam Tốt nhất đầu tiên (Greedy Best-First Search):**
    * **Nguyên lý:** Luôn mở rộng nút được đánh giá là gần đích nhất theo hàm heuristic `h(n)`. Nó chọn nút có `h(n)` nhỏ nhất trong số các nút biên để mở rộng tiếp theo, bỏ qua chi phí đã đi `g(n)`.
    * **Solution:** Không đảm bảo tìm thấy lời giải tối ưu hoặc thậm chí là tìm thấy lời giải (có thể bị kẹt trong các vòng lặp nếu không kiểm tra trạng thái đã duyệt, hoặc đi vào các nhánh dài không dẫn đến đích). Nó "tham lam" vì nó cố gắng tiến nhanh nhất đến đích dựa trên ước tính.
* **Thuật toán A\* (A-Star Search):**
    * **Nguyên lý:** A\* kết hợp thông tin về chi phí đã đi từ trạng thái ban đầu đến nút hiện tại `n` (ký hiệu là `g(n)`) và chi phí ước tính từ nút `n` đến trạng thái đích (hàm heuristic `h(n)`). Nó mở rộng nút có giá trị hàm đánh giá `f(n) = g(n) + h(n)` nhỏ nhất. `f(n)` là ước tính tổng chi phí của đường đi từ trạng thái ban đầu đến đích thông qua nút `n`.
    * **Solution:** Đảm bảo tìm thấy lời giải tối ưu (đường đi có chi phí thấp nhất) nếu hàm heuristic `h(n)` là chấp nhận được (admissible). Nếu `h(n)` còn là nhất quán (consistent/monotonic), A\* sẽ tìm thấy đường đi tối ưu đến một nút ngay lần đầu tiên nó được chọn để mở rộng.
* **Thuật toán IDA\* (Iterative Deepening A\*):**
    * **Nguyên lý:** IDA\* là một biến thể của A\* sử dụng ít bộ nhớ hơn. Nó thực hiện một loạt các tìm kiếm theo chiều sâu. Trong mỗi lần lặp, nó sử dụng một ngưỡng (cutoff) cho giá trị `f(n) = g(n) + h(n)`. Bất kỳ nút nào có `f(n)` vượt quá ngưỡng này sẽ không được mở rộng. Ngưỡng ban đầu thường là `h(start_node)`. Nếu không tìm thấy lời giải, ngưỡng sẽ được tăng lên bằng giá trị `f` nhỏ nhất đã vượt quá ngưỡng ở lần lặp trước. Quá trình này lặp lại cho đến khi tìm thấy lời giải.
    * **Solution:** Tối ưu như A\* (nếu `h(n)` chấp nhận được) và có yêu cầu bộ nhớ tương tự DFS (O(bd)). Tuy nhiên, nó có thể phải duyệt lại các nút nhiều lần, đặc biệt nếu có nhiều giá trị `f` khác nhau.

**Hình ảnh GIF minh họa:**

Thuật toán Greedy:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/Greedy.gif?raw=true)

Thuật toán A*:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/Astar.gif?raw=true)

Thuật toán IDA*:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/IDAstar.gif?raw=true)


**So sánh hiệu suất (dự kiến):**

* **(Chèn hình ảnh/bảng so sánh hiệu suất của Greedy, A\*, IDA\* về thời gian, số bước, số nút đã duyệt tại đây)**

**Nhận xét về hiệu suất:**

* **Greedy Best-First Search:** Thường nhanh nhưng không đảm bảo tối ưu và có thể không đầy đủ (có thể bị kẹt). Dễ bị "lạc đường" nếu heuristic có những điểm "lừa dối" (đánh giá thấp một cách sai lầm một nhánh xấu).
* **A\*:** Là một trong những thuật toán tìm kiếm tối ưu phổ biến và hiệu quả nhất. Với heuristic Manhattan, A\* hoạt động rất tốt cho 8-puzzle, thường tìm ra lời giải tối ưu với số nút duyệt ít hơn đáng kể so với các thuật toán không có thông tin. Tuy nhiên, nó vẫn có thể tốn nhiều bộ nhớ do lưu trữ tất cả các nút đã tạo nhưng chưa được mở rộng (fringe/open list).
* **IDA\*:** Giữ được tính tối ưu của A\* trong khi sử dụng bộ nhớ hiệu quả hơn nhiều (tuyến tính theo độ sâu của lời giải). Tuy nhiên, nó có thể phải duyệt lại các nút nhiều lần, làm tăng thời gian chạy so với A\* trong một số trường hợp, đặc biệt khi có nhiều giá trị `f` khác nhau gần giá trị tối ưu.
* Nhìn chung, A\* và IDA\* là những lựa chọn mạnh mẽ cho 8-puzzle khi cần lời giải tối ưu và heuristic tốt có sẵn.

### 3.4. Các thuật toán Tìm kiếm cục bộ (Local Search)

**Đặc trưng của nhóm:**
Các thuật toán tìm kiếm cục bộ hoạt động bằng cách bắt đầu từ một cấu hình (trạng thái) ban đầu và lặp đi lặp lại việc di chuyển đến một trạng thái lân cận để cố gắng cải thiện một hàm mục tiêu (objective function) hoặc giảm một hàm chi phí (cost function). Chúng không lưu trữ đường đi đã qua mà chỉ quan tâm đến trạng thái hiện tại và các lân cận của nó. Chúng thường không đầy đủ (có thể không tìm thấy lời giải ngay cả khi nó tồn tại) và không tối ưu (có thể bị kẹt ở các cực trị cục bộ thay vì cực trị toàn cục). Tuy nhiên, chúng thường rất hiệu quả về bộ nhớ và có thể tìm ra các giải pháp "đủ tốt" một cách nhanh chóng cho các bài toán tối ưu hóa lớn.

**Các thuật toán được triển khai:**

* **Leo đồi đơn giản (Simple Hill Climbing):**
    * **Nguyên lý:** Tại mỗi bước, thuật toán xem xét các trạng thái lân cận của trạng thái hiện tại. Nó chọn một lân cận đầu tiên mà tốt hơn (ví dụ: có giá trị heuristic thấp hơn) trạng thái hiện tại và di chuyển đến đó. Nếu không có lân cận nào tốt hơn, thuật toán dừng lại.
    * **Đặc điểm:** Rất đơn giản, nhưng dễ bị mắc kẹt ở "vai đồi" (shoulder - một vùng phẳng nơi không có lân cận nào tốt hơn nhưng cũng chưa phải đỉnh) hoặc "cực đại cục bộ" (local maximum - tốt hơn tất cả các lân cận nhưng không phải là tốt nhất toàn cục).
* **Leo đồi dốc nhất (Steepest-Ascent Hill Climbing):**
    * **Nguyên lý:** Tương tự leo đồi đơn giản, nhưng thay vì chọn lân cận tốt hơn đầu tiên tìm thấy, nó đánh giá tất cả các lân cận và chọn lân cận tốt nhất (có cải thiện lớn nhất so với trạng thái hiện tại). Nếu không có lân cận nào tốt hơn, thuật toán dừng lại.
    * **Đặc điểm:** Có thể tránh được một số "vai đồi" nhưng vẫn dễ bị mắc kẹt ở cực đại cục bộ. Tốn nhiều thời gian hơn ở mỗi bước so với leo đồi đơn giản vì phải đánh giá tất cả các lân cận.
* **Leo đồi ngẫu nhiên (Stochastic Hill Climbing):**
    * **Nguyên lý:** Chọn ngẫu nhiên một trong số các lân cận tốt hơn trạng thái hiện tại. Điều này có thể giúp thuật toán khám phá các hướng khác nhau trên "sườn đồi".
    * **Đặc điểm:** Có thể hoạt động tốt hơn leo đồi đơn giản trong một số trường hợp, nhưng vẫn có khả năng bị kẹt.
* **Luyện kim mô phỏng (Simulated Annealing - SA):**
    * **Nguyên lý:** Lấy cảm hứng từ quá trình luyện kim trong vật lý, nơi kim loại được nung nóng rồi làm nguội từ từ để đạt được cấu trúc tinh thể bền vững (năng lượng thấp). SA cho phép di chuyển đến trạng thái lân cận xấu hơn với một xác suất nhất định. Xác suất này phụ thuộc vào mức độ "xấu" của nước đi và một tham số "nhiệt độ" (T). Ban đầu, nhiệt độ cao, cho phép nhiều bước đi xấu hơn. Khi nhiệt độ giảm dần (quá trình "làm nguội"), xác suất chấp nhận nước đi xấu giảm, và thuật toán dần hội tụ về một trạng thái tốt.
    * **Đặc điểm:** Có khả năng thoát khỏi cực tiểu địa phương tốt hơn các thuật toán leo đồi. Hiệu suất phụ thuộc nhiều vào lịch trình làm nguội (cooling schedule: nhiệt độ ban đầu, tốc độ giảm nhiệt độ, điều kiện dừng).
* **Giải thuật di truyền (Genetic Algorithm - GA):**
    * **Nguyên lý:** Mô phỏng quá trình tiến hóa tự nhiên. GA duy trì một "quần thể" (population) các trạng thái (cá thể - individuals). Ở mỗi "thế hệ" (generation), nó chọn lọc các cá thể tốt nhất (dựa trên một "hàm thích nghi" - fitness function, thường ngược dấu với hàm heuristic). Sau đó, nó tạo ra thế hệ mới bằng cách áp dụng các toán tử di truyền như "lai ghép" (crossover - kết hợp thông tin từ hai cá thể cha mẹ để tạo con) và "đột biến" (mutation - thay đổi nhỏ ngẫu nhiên trên một cá thể).
    * **Đặc điểm:** Khám phá không gian trạng thái một cách song song thông qua quần thể. Có khả năng tìm kiếm toàn cục tốt hơn leo đồi. Hiệu suất phụ thuộc vào kích thước quần thể, cách chọn lọc, toán tử lai ghép và đột biến, và số thế hệ.
* **Tìm kiếm chùm (Beam Search):**
    * **Nguyên lý:** Là một biến thể của tìm kiếm theo chiều rộng nhưng chỉ giữ lại một số lượng `k` (beam width - độ rộng chùm) trạng thái tốt nhất ở mỗi mức độ sâu. Ở mỗi bước, nó tạo ra tất cả các trạng thái kế tiếp từ `k` trạng thái hiện tại trong chùm, sau đó chọn ra `k` trạng thái tốt nhất mới từ tập hợp các trạng thái kế tiếp đó để tạo thành chùm cho bước tiếp theo.
    * **Đặc điểm:** Giảm yêu cầu bộ nhớ so với BFS. Nếu `k=1`, nó trở thành Greedy Best-First Search. Nếu `k` tiến đến vô cùng, nó giống BFS. Có thể bỏ lỡ lời giải tối ưu nếu nó nằm ngoài chùm tia ở một bước nào đó.

**Hình ảnh GIF minh họa:**

Thuật toán Simple Hill Climbing:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/simple_hill.gif?raw=true)

Thuật toán Steepest-Ascent Hill Climbing:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/stepest_hill.gif?raw=true)

Thuật toán Stochastic Hill Climbing

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/stochastic_hill.gif?raw=true)

Thuật toán Genetic Algorithm - GA:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/generic.gif?raw=true)

Thuật toán Simulated Annealing - SA:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/simulated_anealing.gif?raw=true)

Thuật toán Beam Search:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/Beam.gif?raw=true)


**So sánh hiệu suất (dự kiến):**

* **(Chèn hình ảnh/bảng so sánh hiệu suất của các thuật toán tìm kiếm cục bộ, có thể so sánh chất lượng giải pháp (ví dụ: giá trị heuristic của trạng thái cuối) và thời gian tìm kiếm tại đây)**

**Nhận xét về hiệu suất:**

* **Hill Climbing (các biến thể):** Rất nhanh nhưng dễ bị mắc kẹt ở cực tiểu địa phương và thường không tìm được trạng thái đích (goal state) trừ khi trạng thái ban đầu rất gần đích hoặc không gian tìm kiếm đơn giản.
* **Simulated Annealing:** Có khả năng thoát khỏi cực tiểu địa phương tốt hơn Hill Climbing. Chất lượng giải pháp phụ thuộc nhiều vào lịch trình làm nguội và số lần lặp. Có thể tìm được trạng thái đích nếu được cấu hình tốt và cho đủ thời gian, nhưng không đảm bảo.
* **Genetic Algorithm:** Có thể khám phá không gian trạng thái rộng hơn và tìm được các giải pháp tốt hơn so với leo đồi đơn giản. Hiệu suất phụ thuộc vào nhiều tham số. Cũng có khả năng tìm được trạng thái đích nhưng không đảm bảo.
* **Beam Search:** Là một sự thỏa hiệp giữa Greedy search và BFS. Có thể hiệu quả hơn Greedy nhưng vẫn có thể bỏ lỡ giải pháp tối ưu.
* Đối với 8-puzzle, các thuật toán tìm kiếm cục bộ này thường được sử dụng để tìm một trạng thái "đủ tốt" (ví dụ, trạng thái có giá trị heuristic thấp) một cách nhanh chóng hơn là tìm trạng thái đích tuyệt đối. Trong project này, nếu chúng tìm được trạng thái đích, A\* sẽ được dùng để tìm đường đi từ trạng thái ban đầu đến trạng thái đích đó.

### 3.5. Các thuật toán cho Môi trường Phức tạp (Complex Environments)

**Đặc trưng của nhóm:**
Nhóm này bao gồm các thuật toán hoặc mô phỏng các khái niệm tìm kiếm được thiết kế cho các môi trường mà tác nhân (agent) không có thông tin hoàn hảo về thế giới hoặc hành động của nó có thể dẫn đến các kết quả không chắc chắn. Chúng thường liên quan đến việc duy trì và cập nhật "tập hợp niềm tin" (belief states) về trạng thái thực sự của môi trường.

**Các khái niệm và thuật toán được mô phỏng:**

* **AND-OR Search (Tìm kiếm AND-OR):**
    * **Nguyên lý:** Được sử dụng cho các bài toán mà hành động có thể không xác định (non-deterministic), nghĩa là một hành động có thể dẫn đến một trong nhiều kết quả có thể. Một kế hoạch (lời giải) phải chỉ định cách đối phó với mọi khả năng. Cây tìm kiếm AND-OR có các nút OR (tương ứng với lựa chọn hành động của tác nhân) và các nút AND (tương ứng với các kết quả có thể xảy ra của một hành động không xác định, do môi trường quyết định). Một lời giải là một cây con mà: (1) chứa nút gốc, (2) với mỗi nút OR trong cây con, nó chứa đúng một nút con kế tiếp, (3) với mỗi nút AND trong cây con, nó chứa tất cả các nút con kế tiếp.
    * **Mô phỏng trong game:** Giao diện cho phép người dùng giải quyết bài toán 8-puzzle bằng cách chọn từng "tiểu mục tiêu" (ví dụ: đưa ô số 1 về đúng vị trí, sau đó đưa ô số 2 về đúng vị trí trong khi giữ ô số 1 cố định). Mỗi tiểu mục tiêu này là một phần của một kế hoạch lớn hơn. Việc giải quyết thành công một tiểu mục tiêu có thể coi là một nhánh AND (phải hoàn thành) trong một kế hoạch AND-OR tổng thể để giải toàn bộ puzzle.
* **Sensorless (Conformant) Problem (Bài toán không cảm biến / Tuân thủ):**
    * **Nguyên lý:** Tác nhân không có cảm biến để xác định trạng thái hiện tại của nó. Nó chỉ biết trạng thái ban đầu có thể là một trong một tập hợp các trạng thái (belief state ban đầu). Một hành động sẽ chuyển mỗi trạng thái trong belief state hiện tại sang một trạng thái kế tiếp tương ứng, tạo ra một belief state mới. Mục tiêu là tìm một chuỗi hành động duy nhất mà khi thực hiện sẽ đưa tác nhân đến trạng thái đích bất kể trạng thái vật lý thực sự ban đầu (trong belief state ban đầu) là gì.
    * **Mô phỏng trong game:** Hiển thị đồng thời nhiều bảng 8-puzzle, mỗi bảng đại diện cho một trạng thái có thể có trong belief state của tác nhân. Khi người dùng chọn một hành động (ví dụ: "UP"), hành động đó được áp dụng đồng thời cho tất cả các bảng. Mục tiêu là tìm một chuỗi hành động đưa tất cả các bảng về cùng một trạng thái đích.
* **Partially Observable Problem (Bài toán quan sát được một phần):**
    * **Nguyên lý:** Tác nhân có cảm biến, nhưng chúng chỉ cung cấp thông tin giới hạn hoặc nhiễu về trạng thái hiện tại. Tác nhân duy trì một belief state (tập hợp các trạng thái có thể, cùng với xác suất của chúng nếu là POMDP). Sau mỗi hành động, tác nhân nhận được một quan sát (observation), và sử dụng quan sát này cùng với mô hình cảm biến (sensor model) để cập nhật belief state của mình.
    * **Mô phỏng trong game:** Hiển thị nhiều bảng 8-puzzle. Một phần của bảng (ví dụ: hàng đầu tiên) được coi là luôn quan sát được chính xác và giống nhau trên tất cả các bảng trong belief state. Các phần còn lại có thể khác nhau. Khi một hành động được thực hiện, nó áp dụng cho tất cả các bảng. Mục tiêu là tìm một chuỗi hành động đưa tất cả các bảng về trạng thái đích, trong đó phần quan sát được vẫn duy trì đúng.

**Hình ảnh GIF minh họa:**

AND-OR Search (Tìm kiếm AND-OR):

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/AndOr.gif?raw=true)


Sensorless (Conformant) Problem (Bài toán không cảm biến / Tuân thủ):

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/sensorless.gif?raw=true)

Partially Observable Problem (Bài toán quan sát được một phần):

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/partail.gif?raw=true)


**Nhận xét:**

* Các mô phỏng này giúp hình dung các khái niệm tìm kiếm nâng cao hơn, thường gặp trong các hệ thống AI phức tạp. Chúng không trực tiếp giải quyết bài toán 8-puzzle theo cách tìm đường đi truyền thống mà minh họa các loại vấn đề và cách tiếp cận khác nhau.
* Việc triển khai đầy đủ các thuật toán cho những môi trường này (ví dụ: AO\*, các thuật toán tìm kiếm trong không gian belief state cho Sensorless và POMDP) thường phức tạp hơn nhiều và nằm ngoài phạm vi của các thuật toán tìm kiếm cơ bản được tập trung trong project này. Các mô phỏng này chủ yếu mang tính chất minh họa khái niệm.

### 3.6. Tìm kiếm đường đi với ràng buộc (Constrained Pathfinding)

**Đặc trưng của nhóm:**
Nhóm này giải quyết các bài toán tìm kiếm đường đi mà ngoài mục tiêu đạt đến trạng thái đích, lời giải còn phải thỏa mãn một hoặc nhiều ràng buộc (constraints) bổ sung trên các trạng thái hoặc hành động trong đường đi. Sự tồn tại của ràng buộc thường làm cho không gian tìm kiếm hiệu quả bị thu hẹp hoặc phức tạp hóa việc kiểm tra tính hợp lệ của các bước đi.

**Ràng buộc được áp dụng trong project:**
* **Ràng buộc kề cận giữa ô số 2 và ô số 5 (2-5 Adjacency):** Trong mọi trạng thái trên đường đi từ trạng thái ban đầu đến trạng thái đích, ô số 2 và ô số 5 phải luôn nằm kề nhau. "Kề nhau" ở đây có nghĩa là chúng có chung một cạnh hoặc một góc (tức là Manhattan distance bằng 1 hoặc Chebyshev distance bằng 1).

**Các thuật toán được triển khai:**

* **Backtracking Search (Tìm kiếm quay lui):**
    * **Nguyên lý:** Đây là một thuật toán tìm kiếm theo chiều sâu cơ bản được điều chỉnh để xử lý ràng buộc. Thuật toán xây dựng một lời giải tiềm năng từng bước một. Tại mỗi bước, nếu việc thêm một hành động (hoặc chuyển đến một trạng thái mới) vi phạm bất kỳ ràng buộc nào, nhánh đó sẽ bị cắt tỉa và thuật toán "quay lui" (backtrack) để thử một lựa chọn khác ở bước trước đó. Nó khám phá một cách có hệ thống không gian các lời giải từng phần.
    * **Áp dụng:** Sau mỗi nước đi tiềm năng, kiểm tra xem trạng thái mới có thỏa mãn ràng buộc 2-5 không. Nếu không, không đi nước đó và thử nước khác.
* **Forward Checking (Kiểm tra phía trước):**
    * **Nguyên lý:** Là một cải tiến của Backtracking, thường được sử dụng trong các Bài toán Thỏa mãn Ràng buộc (CSP). Ý tưởng cơ bản là sau khi thực hiện một lựa chọn (ví dụ, một nước đi), thuật toán "nhìn về phía trước" để dự đoán các hậu quả của lựa chọn đó đối với các lựa chọn tương lai. Nếu một lựa chọn hiện tại dẫn đến tình huống mà không có lựa chọn hợp lệ nào cho tương lai (vi phạm ràng buộc), thì lựa chọn hiện tại đó sẽ bị loại bỏ sớm.
    * **Áp dụng:** Sau mỗi nước đi hợp lệ (không vi phạm ràng buộc 2-5 ngay lập tức), thuật toán có thể (một cách đơn giản hóa) kiểm tra xem từ trạng thái mới này, có còn ít nhất một nước đi hợp lệ tiếp theo mà vẫn duy trì được ràng buộc hay không. Nếu không, nước đi hiện tại có thể không phải là một phần của lời giải.
* **Min-Conflicts (Xung đột tối thiểu) với sửa chữa đường đi:**
    * **Nguyên lý:** Đây là một thuật toán tìm kiếm cục bộ thường dùng cho CSP. Nó bắt đầu với một gán giá trị hoàn chỉnh cho tất cả các biến (trong trường hợp này là một đường đi hoàn chỉnh từ đầu đến cuối, có thể ban đầu không thỏa mãn ràng buộc). Sau đó, nó lặp đi lặp lại việc chọn một "biến" (một trạng thái trong đường đi) đang gây ra xung đột (vi phạm ràng buộc) và thay đổi giá trị của nó (thay đổi trạng thái đó bằng một trạng thái lân cận) sao cho số lượng xung đột được giảm thiểu.
    * **Áp dụng:** Đầu tiên, một đường đi từ trạng thái ban đầu đến đích được tạo ra (ví dụ, bằng A\* chuẩn, không quan tâm đến ràng buộc 2-5). Sau đó, thuật toán Min-Conflicts sẽ cố gắng "sửa chữa" đường đi này. Nó sẽ xác định các trạng thái trong đường đi vi phạm ràng buộc 2-5 hoặc các bước chuyển không hợp lệ. Sau đó, nó sẽ cố gắng thay đổi các trạng thái đó bằng các trạng thái lân cận để giảm số lượng vi phạm, lặp lại cho đến khi không còn vi phạm hoặc đạt giới hạn số lần lặp.

**Hình ảnh GIF minh họa:**

Backtracking Search:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/Backtracking.gif?raw=true)

Forward Checking

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/forward_checking.gif?raw=true)

Min-Conflicts 

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/minconflict.gif?raw=true)

**Nhận xét:**

* Việc thêm ràng buộc làm cho bài toán tìm kiếm đường đi trở nên khó khăn hơn đáng kể, vì không phải tất cả các nước đi hợp lệ trong bài toán gốc đều còn hợp lệ.
* **Backtracking và Forward Checking** là các thuật toán có hệ thống, đảm bảo tìm ra lời giải nếu nó tồn tại (trong giới hạn độ sâu). Tuy nhiên, chúng có thể rất chậm đối với các bài toán có không gian tìm kiếm lớn hoặc ràng buộc chặt chẽ, do phải khám phá nhiều nhánh.
* **Min-Conflicts** là một thuật toán tìm kiếm cục bộ, không đảm bảo tìm thấy lời giải hoặc lời giải tối ưu. Hiệu quả của nó phụ thuộc vào chất lượng của lời giải ban đầu và "địa hình" của không gian xung đột. Nó có thể nhanh chóng tìm thấy một giải pháp chấp nhận được nếu có, hoặc bị kẹt.
* Hiệu suất của các thuật toán này sẽ giảm đáng kể so với các phiên bản không có ràng buộc do phải thực hiện các kiểm tra ràng buộc ở mỗi bước hoặc mỗi trạng thái.

### 3.7. Học tăng cường (Reinforcement Learning - RL)

**Đặc trưng của nhóm:**
Học tăng cường là một lĩnh vực của học máy, nơi một tác nhân (agent) học cách hành xử trong một môi trường bằng cách thực hiện các hành động và quan sát kết quả (phần thưởng hoặc hình phạt). Mục tiêu của tác nhân là học một chính sách (policy) - một ánh xạ từ trạng thái sang hành động - để tối đa hóa tổng phần thưởng tích lũy theo thời gian. Khác với các thuật toán tìm kiếm truyền thống thường yêu cầu một mô hình hoàn chỉnh của môi trường, nhiều thuật toán RL có thể học trực tiếp từ kinh nghiệm (model-free).

**Các thuật toán được triển khai:**

* **Q-Learning:**
    * **Nguyên lý:** Là một thuật toán học giá trị hành động (action-value) không cần mô hình (model-free) và off-policy. "Off-policy" nghĩa là nó có thể học chính sách tối ưu ngay cả khi dữ liệu được thu thập bằng một chính sách khác (ví dụ, một chính sách có tính khám phá cao hơn). Q-Learning học một hàm `Q(s, a)`, đại diện cho chất lượng (giá trị kỳ vọng của tổng phần thưởng tương lai) của việc thực hiện hành động `a` tại trạng thái `s` và sau đó tuân theo chính sách tối ưu. Công thức cập nhật Q-value dựa trên phương trình Bellman:
        `Q(s, a) <- Q(s, a) + alpha * [R + gamma * max_a'(Q(s', a')) - Q(s, a)]`
        Trong đó:
        * `alpha`: Tỷ lệ học (learning rate).
        * `R`: Phần thưởng nhận được sau khi thực hiện hành động `a` tại `s` và chuyển đến `s'`.
        * `gamma`: Hệ số chiết khấu (discount factor), xác định tầm quan trọng của phần thưởng tương lai.
        * `max_a'(Q(s', a'))`: Giá trị Q lớn nhất có thể đạt được từ trạng thái kế tiếp `s'`.
    * **Quá trình:** Tác nhân tương tác với môi trường. Tại mỗi bước, nó chọn một hành động (thường sử dụng chiến lược epsilon-greedy để cân bằng giữa khám phá các hành động mới và khai thác các hành động đã biết là tốt). Sau khi thực hiện hành động, nó quan sát trạng thái mới và phần thưởng, sau đó cập nhật giá trị Q cho cặp (trạng thái, hành động) vừa thực hiện.
* **TD Learning (Value Prediction - Temporal Difference Learning for V(s)):**
    * **Nguyên lý:** Cụ thể hơn, đây là TD(0) cho việc dự đoán hàm giá trị trạng thái `V(s)`. `V(s)` ước tính tổng phần thưởng kỳ vọng có thể nhận được bắt đầu từ trạng thái `s` và tuân theo một chính sách `pi` nào đó. TD Learning là model-free và cập nhật giá trị của một trạng thái dựa trên giá trị ước tính của trạng thái kế tiếp (bootstrap). Công thức cập nhật cho `V(s)`:
        `V(s) <- V(s) + alpha * [R + gamma * V(s') - V(s)]`
        Trong đó `s'` là trạng thái kế tiếp sau khi thực hiện một hành động theo chính sách `pi` từ `s`.
    * **Quá trình:** Tác nhân tuân theo một chính sách (ví dụ, epsilon-greedy dựa trên `V(s)` hiện tại) để chọn hành động, chuyển đến trạng thái mới, nhận phần thưởng và cập nhật `V(s)` của trạng thái trước đó.

**Hình ảnh GIF minh họa (nếu có thể, ví dụ: hiển thị Q-values thay đổi hoặc agent tự chơi sau khi huấn luyện):**

Q-Learning:

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/q_learning.gif?raw=true)

TD Learning (Value Prediction - Temporal Difference Learning for V(s)):

![Demo And-Or](https://github.com/BaoBaoIT-maker/23110178_HuynhHoaiBao_DoAnCaNhan/blob/main/TD_learning.gif?raw=true)


**Nhận xét:**

* **Huấn luyện:** Các thuật toán RL đòi hỏi một giai đoạn huấn luyện đáng kể (nhiều episodes/bước tương tác) để học được chính sách hiệu quả. Trong giai đoạn này, agent sẽ thực hiện nhiều hành động, bao gồm cả các hành động ngẫu nhiên (exploration) để khám phá không gian trạng thái và hành động.
* **Bảng Q/V (Lookup Table):** Đối với 8-puzzle, số lượng trạng thái là 181,440. Nếu sử dụng bảng tra cứu (lookup table) để lưu trữ Q-values (cho mỗi cặp state-action) hoặc V-values (cho mỗi state), kích thước bảng có thể quản lý được. Tuy nhiên, việc đảm bảo tất cả các trạng thái và hành động quan trọng được khám phá đủ vẫn là một thách thức.
* **Hàm phần thưởng (Reward Function):** Thiết kế hàm phần thưởng là cực kỳ quan trọng và ảnh hưởng lớn đến hành vi học được của agent. Một hàm phần thưởng phổ biến có thể là: +1 (hoặc giá trị dương lớn) khi đạt trạng thái đích, -0.01 (hoặc giá trị âm nhỏ) cho mỗi bước đi để khuyến khích tìm lời giải ngắn, và có thể là một hình phạt lớn hơn nếu thực hiện hành động không hợp lệ (mặc dù trong 8-puzzle, các hành động không hợp lệ thường bị chặn).
* **Hội tụ và Tối ưu:** Không có gì đảm bảo rằng các thuật toán này sẽ hội tụ đến chính sách tối ưu toàn cục, đặc biệt với số lần huấn luyện giới hạn hoặc nếu các tham số (alpha, gamma, epsilon) không được chọn phù hợp. Tuy nhiên, chúng thường có thể học được các chính sách "đủ tốt".
* **Sau huấn luyện:** Một khi đã được huấn luyện, agent có thể sử dụng bảng Q (chọn hành động `a` tại trạng thái `s` sao cho `Q(s, a)` là lớn nhất) hoặc bảng V (chọn hành động dẫn đến trạng thái `s'` có `V(s')` lớn nhất) để giải quyết bài toán một cách nhanh chóng mà không cần tìm kiếm lại từ đầu.
* Trong project này, sau khi huấn luyện, agent sẽ cố gắng giải quyết puzzle dựa trên chính sách đã học từ bảng Q hoặc V.

### 3.8.So sánh giữa các thuật toán

![comparison_time_to_solve_extended](https://github.com/user-attachments/assets/23efe2f2-414a-4872-8474-df0c7e6902dc)

![comparison_nodes_expanded_extended](https://github.com/user-attachments/assets/60496326-7821-4bbc-91a2-4c179990bb1e)

![comparison_path_length_extended](https://github.com/user-attachments/assets/8e06048d-aee2-4653-8a3a-eea2aa0b55c8)


## 4. Kết luận

Project này đã thành công trong việc triển khai và trực quan hóa một loạt các thuật toán tìm kiếm AI trên trò chơi 8 ô chữ. Qua đó, có thể rút ra một số kết quả và nhận xét chính:

* **Đa dạng thuật toán:** Project đã bao quát nhiều nhóm thuật toán khác nhau, từ tìm kiếm cơ bản không có thông tin, tìm kiếm có thông tin sử dụng heuristic, tìm kiếm cục bộ, đến các khái niệm phức tạp hơn như tìm kiếm trong môi trường không chắc chắn, tìm kiếm với ràng buộc và học tăng cường.
* **Trực quan hóa:** Giao diện đồ họa cho phép người dùng tương tác và quan sát trực tiếp cách mỗi thuật toán hoạt động, khám phá không gian trạng thái, và (nếu có) quá trình học của agent. Điều này rất hữu ích cho việc hiểu rõ bản chất của từng thuật toán.
* **So sánh hiệu suất:**
    * Các thuật toán có thông tin (A\*, IDA\*) với heuristic tốt (Manhattan distance) thường cho hiệu suất tốt nhất trong việc tìm ra lời giải tối ưu cho 8-puzzle chuẩn.
    * Các thuật toán không có thông tin như BFS và IDS cũng tìm ra lời giải tối ưu nhưng có thể chậm hơn hoặc tốn nhiều tài nguyên hơn. DFS thường không hiệu quả cho việc tìm lời giải tối ưu.
    * Các thuật toán tìm kiếm cục bộ (Hill Climbing, SA, GA) có thể nhanh chóng tìm được các trạng thái "gần đúng" nhưng không đảm bảo tìm được trạng thái đích, trừ khi được cấu hình và cho đủ thời gian. Chúng phù hợp hơn cho các bài toán tối ưu hóa nơi không nhất thiết phải đạt được một mục tiêu cụ thể.
    * Việc thêm ràng buộc (như 2-5 adjacency) làm tăng đáng kể độ phức tạp và thời gian tìm kiếm của các thuật toán CSP.
    * Học tăng cường (Q-Learning, TD Learning) cho thấy một cách tiếp cận khác, nơi agent "học" để giải quyết vấn đề. Mặc dù đòi hỏi thời gian huấn luyện, nhưng sau đó có thể giải quyết nhanh chóng. Hiệu quả phụ thuộc vào thiết kế hàm phần thưởng và quá trình huấn luyện.
* **Mô phỏng môi trường phức tạp:** Các mô phỏng cho AND-OR, Sensorless, và Partially Observable giúp minh họa các thách thức trong các bài toán AI thực tế hơn, nơi thông tin không đầy đủ hoặc hành động không chắc chắn.
* **Hạn chế và Hướng phát triển:**
    * Hiệu suất của một số thuật toán (đặc biệt là tìm kiếm cục bộ và RL) có thể được cải thiện thêm bằng cách tinh chỉnh tham số hoặc sử dụng các kỹ thuật nâng cao hơn (ví dụ: hàm xấp xỉ cho RL thay vì bảng tra cứu cho các bài toán lớn hơn).
    * Giao diện có thể được mở rộng để hiển thị thêm thông tin chi tiết về quá trình tìm kiếm (ví dụ: đồ thị các nút đã duyệt, giá trị heuristic, Q-values).
    * Có thể thử nghiệm với các heuristic phức tạp hơn hoặc các hàm phần thưởng khác cho RL.
    * Triển khai các phiên bản đầy đủ của thuật toán cho môi trường không chắc chắn (ví dụ: AO\*, LAO\*, POMDP solvers) sẽ là một hướng phát triển thú vị.

Nhìn chung, project đã cung cấp một nền tảng vững chắc để khám phá và so sánh các kỹ thuật tìm kiếm AI khác nhau thông qua một bài toán kinh điển là game 8 ô chữ.
