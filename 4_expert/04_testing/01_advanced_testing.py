'''
Advanced Testing in Python
=========================

Module này đi sâu vào các kỹ thuật testing nâng cao trong Python,
bao gồm property-based testing, mutation testing, và các chiến lược 
để cải thiện test suites.

CẢNH BÁO: Nội dung này đòi hỏi kiến thức vững về testing cơ bản
và kinh nghiệm với pytest.
'''

print("=== Advanced Testing Techniques ===")

# ====== PROPERTY-BASED TESTING =======
print("\n--- Property-Based Testing với Hypothesis ---")
print("""
Property-based testing là phương pháp kiểm thử tập trung vào các thuộc tính
mà code của bạn phải thỏa mãn, thay vì các test cases cụ thể.

Thư viện Hypothesis giúp tạo ra test data tự động:
""")

def demonstrate_hypothesis():
    try:
        from hypothesis import given
        from hypothesis import strategies as st
        import pytest
        
        # Ví dụ: Hàm đảo ngược chuỗi
        def reverse_string(s):
            return s[::-1]
        
        # Test property: đảo ngược 2 lần = chuỗi ban đầu
        @given(st.text())
        def test_reverse_twice_equals_original(s):
            assert reverse_string(reverse_string(s)) == s
            
        print("Ví dụ với Hypothesis (cú pháp):")
        print("""
        @given(st.text())
        def test_reverse_twice_equals_original(s):
            assert reverse_string(reverse_string(s)) == s
        """)
        print("Hypothesis tự động tạo nhiều test cases khác nhau.")
    except ImportError:
        print("Để chạy ví dụ này, cài đặt: pip install hypothesis pytest")

demonstrate_hypothesis()

# ====== MUTATION TESTING =======
print("\n--- Mutation Testing ---")
print("""
Mutation testing đánh giá chất lượng test suite bằng cách cố tình 
tạo ra các "đột biến" (bugs) trong code và kiểm tra xem tests có phát hiện không.

Thư viện mutmut là một công cụ mutation testing phổ biến trong Python:
""")

print("""
# Cách sử dụng mutmut
# 1. Cài đặt: pip install mutmut
# 2. Chạy: mutmut run
# 3. Xem kết quả: mutmut results

# mutmut sẽ tự động tạo các "đột biến" như:
# - Thay đổi toán tử (+ thành -, == thành !=)
# - Xóa các dòng code
# - Thay đổi giá trị hằng số

# Nếu test suite tốt, nó sẽ phát hiện hầu hết các đột biến!
""")

# ====== MOCKING NÂNG CAO =======
print("\n--- Kỹ thuật Mocking nâng cao ---")
print("""
Mocking không chỉ là thay thế dependencies đơn giản, mà còn có thể 
mô phỏng các tình huống phức tạp:
""")

def demonstrate_advanced_mocking():
    try:
        import unittest
        from unittest import mock
        
        # Ví dụ về mock side_effect và mock context manager
        print("""
        # Mock với side_effect (xử lý nhiều kết quả/exceptions):
        mock_function.side_effect = [1, 2, ValueError("error message"), 3]
        
        # Mock context manager:
        with mock.patch('module.ClassName') as MockClass:
            MockClass.return_value.__enter__.return_value.some_attr = 'value'
            
        # Theo dõi lịch sử cuộc gọi chi tiết:
        assert mock_obj.method.call_args_list == [
            mock.call(1, 2),
            mock.call("a", b=3)
        ]
        """)
    except ImportError:
        print("Thư viện unittest có sẵn trong Python standard library")

demonstrate_advanced_mocking()

# ====== CHIẾN LƯỢC TESTING =======
print("\n--- Chiến lược Testing cho hệ thống phức tạp ---")
print("""
1. Pyramid testing: 
   - Unit tests (nhiều nhất, nhanh nhất)
   - Integration tests (kết hợp các components)
   - End-to-end tests (ít nhất, chậm nhất)

2. Test coverage có ý nghĩa:
   - Không chỉ đo lường % code coverage
   - Tập trung vào code paths quan trọng
   - Kiểm thử các edge cases và error paths

3. Test-Driven Development nâng cao:
   - Outside-in testing (từ ngoài vào trong)
   - Behavior-driven development (BDD)
   - Acceptance-test driven development (ATDD)
""")

# ====== PERFORMANCE TESTING =======
print("\n--- Performance Testing ---")
print("""
Đánh giá và tối ưu performance của code với:

1. Benchmark testing:
""")

def demonstrate_benchmark():
    try:
        import pytest
        
        print("""
        # Sử dụng pytest-benchmark
        def test_performance(benchmark):
            result = benchmark(lambda: function_to_benchmark(param1, param2))
            assert result == expected_value
        """)
    except ImportError:
        print("Để chạy ví dụ này cài đặt: pip install pytest pytest-benchmark")

demonstrate_benchmark()

print("""
2. Profiling trong tests:
   - cProfile và profile modules
   - pytest-profiling plugin
   - memory-profiler

3. Load testing và stress testing cho ứng dụng web
   - locust
   - pytest-aiohttp
""")

# ====== THIẾT KẾ TEST CASES =======
print("\n--- Thiết kế Test Cases Nâng cao ---")
print("""
1. Equivalence partitioning:
   - Chia input thành các nhóm tương đương 
   - Chỉ test một số đại diện từ mỗi nhóm

2. Boundary value analysis:
   - Test các giá trị biên (min, min+1, max-1, max)
   - Test các giá trị ngoài biên (min-1, max+1)

3. Pairwise testing:
   - Kiểm thử tổ hợp các cặp giá trị input
   - Giảm số lượng test cases nhưng vẫn đảm bảo coverage
""")

# ====== BÀI TẬP THỰC HÀNH =======
print("\n--- Bài tập thực hành ---")
print("""
1. Xây dựng một test suite sử dụng property-based testing
2. Thực hiện mutation testing trên một dự án Python hiện có
3. Đánh giá performance của một hàm quan trọng bằng benchmark
4. Thiết kế một test strategy cho một microservice
""")

# Lưu ý cuối cùng
print("\n--- Lưu ý ---")
print("""
"Testing can only prove the presence of bugs, not their absence." - Dijkstra

Testing nâng cao giúp bạn tạo ra phần mềm mạnh mẽ hơn bằng cách
phát hiện bugs sớm và đảm bảo code hoạt động như mong đợi trong
nhiều tình huống.
""")