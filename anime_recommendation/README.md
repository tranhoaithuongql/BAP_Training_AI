# Đây là bài về hệ thống gợi ý sử dụng thuật toán matrix factorization và anime datasetdata
![image](https://user-images.githubusercontent.com/86063811/123987753-a4ca5000-d9f1-11eb-80bc-ce6eac5a2ee4.png)


Matrix Factorization_(Phân rã ma trận) là phương pháp chia một ma trận lớn X thành 2 ma trận nhỏ hơn X ~ WH^T. Trong đó, W là một ma trận mà mỗi dòng u là một vector bao gồm K nhân tố tiềm ẩn mô tả user u và H là một ma trận mà mỗi dòng i là một vector bao gồm K nhân tố tiềm ẩn mô tả cho item i.
Mục tiêu của bài toán là tìm một vector w tương ứng với mỗi user sao cho ratings của user đó với item xấp xỉ với: y ~ xw.

