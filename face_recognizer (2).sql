-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th9 16, 2022 lúc 10:10 AM
-- Phiên bản máy phục vụ: 10.4.18-MariaDB
-- Phiên bản PHP: 7.4.16
create database manh;
use manh;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `face_recognizer`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `admin`
--

CREATE TABLE `admin` (
  `Account` varchar(45) NOT NULL,
  `Password` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `admin`
--

INSERT INTO `admin` (`Account`, `Password`) VALUES
('26565', 'e10adc3949ba59abbe56e057f20f883e'),
('admin', '123456'),
('chicken', '*6966A21D66C4C35D44C0187345DB9CF8A66512A8'),
('chicken1', 'e6053eb8d35e02ae40beeeacef203c1a'),
('chicken2', 'e6053eb8d35e02ae40beeeacef203c1a'),
('chicken29', 'e10adc3949ba59abbe56e057f20f883e');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `attendance`
--

CREATE TABLE `attendance` (
  `IdAuttendance` varchar(45) NOT NULL,
  `Student_id` int(11) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Class` varchar(45) DEFAULT NULL,
  `Time_in` time DEFAULT NULL,
  `Time_out` time DEFAULT NULL,
  `Date` varchar(45) DEFAULT NULL,
  `Lesson_id` int(11) NOT NULL,
  `AttendanceStatus` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `class`
--

CREATE TABLE `class` (
  `Class` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `class`
--

INSERT INTO `class` (`Class`, `Name`) VALUES
('9A', '9aB'),
('9B', 'a');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lesson`
--

CREATE TABLE `lesson` (
  `Lesson_id` int(11) NOT NULL,
  `Time_start` time DEFAULT NULL,
  `Time_end` time DEFAULT NULL,
  `Date` varchar(45) NOT NULL,
  `Class` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `lesson`
--

INSERT INTO `lesson` (`Lesson_id`, `Time_start`, `Time_end`, `Date`, `Class`) VALUES
(1, '07:00:00', '11:30:00', '17/09/2022', '9A'),
(2, '07:00:00', '11:30:00', '17/09/2022', '9B'),
(3, '07:00:00', '11:30:00', '18/09/2022', '9A'),
(4, '07:00:00', '11:30:00', '18/09/2022', '9B'),
(5, '07:00:00', '11:30:00', '19/09/2022', '9A'),
(6, '07:00:00', '11:30:00', '19/09/2022', '9B'),
(7, '07:00:00', '11:30:00', '20/09/2022', '9A'),
(8, '07:00:00', '11:30:00', '20/09/2022', '9B'),
(9, '07:00:00', '11:30:00', '21/09/2022', '9A'),
(10, '07:00:00', '11:30:00', '21/09/2022', '9B'),
(11, '14:00:00', '16:30:00', '21/09/2022', '9A'),
(12, '14:00:00', '16:30:00', '18/09/2022', '9B'),
(13, '07:00:00', '11:30:00', '05/10/2022', '9A'),
(14, '07:00:00', '11:30:00', '06/10/2022', '9A'),
(15, '07:00:00', '11:30:00', '07/10/2022', '9A');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `student`
--

CREATE TABLE `student` (
  `Student_id` int(11) NOT NULL,
  `Year` varchar(45) DEFAULT NULL,
  `Semester` varchar(45) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Class` varchar(45) NOT NULL,
  `Roll` varchar(45) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `Dob` varchar(45) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Phone` varchar(45) DEFAULT NULL,
  `Address` varchar(45) DEFAULT NULL,
  `PhotoSample` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `student`
--

INSERT INTO `student` (`Student_id`, `Year`, `Semester`, `Name`, `Class`, `Roll`, `Gender`, `Dob`, `Email`, `Phone`, `Address`, `PhotoSample`) VALUES
(1, '2022', '1', 'Le Quang Anh', '9A', '12235687410', 'Nam', '16/03/2008', 'nhatlequang@gmail.com', '6523791156', '32 duong Lang', 'Yes'),
(2, '2022', '1', 'Do Manh Dung', '9A', '15638892236', 'Nam', '11/03/2008', 'khongten19@gmail.com', '985186223', 'Hai Phong', 'Yes'),
(3, '2022', '1', 'Mai Quoc Khanh', '9A', '12234486753', 'Nam', '16/09/2008', 'mqk@gmail.com', '388359476', 'Bac Giang', 'Yes'),
(6, '2022', '1', 'Truong Viet Hoang', '9A', '126464646', 'Nam', '16/09/2008', 'chuioi@gmail.com', '8484454', 'HN', 'No'),
(7, '2022', '1', 'Nguyen Viet Hoang', '9A', '157528212', 'Nam', '12/08/2008', 'chuioi@gmail.com', '843225252', 'HN', 'No'),
(8, '2022', '1', 'Le Minh Thu', '9B', '322558587', 'Nu', '03/04/2008', 'chuioi@gmail.com', '842222454', 'HN', 'No'),
(9, '2022', '1', 'Nguyen Thu Phuong', '9B', '55585855', 'Nu', '26/05/2009', 'chuioi@gmail.com', '8424254', 'HN', 'No'),
(10, '2022', '1', 'Trong Bach', '9B', '577575757', 'Nam', '29/12/2008', 'chuioi@gmail.com', '84222222', 'HN', 'No'),
(11, '2022', '1', 'Le Minh Anh', '9B', '132316590', 'Nam', '12/03/2008', 'chuioi@gmail.com', '8899889', 'HN', 'No'),
(12, '2022', '1', 'Hoang Diep', '9B', '32165959', 'Nu', '12/09/2008', 'chuioi@gmail.com', '8454544', 'HN', 'No'),
(13, '2022', '1', 'Le Thi Anh', '9B', '15555552', 'Nu', '19/08/2008', 'chuioi@gmail.com', '84949494', 'HN', 'No'),
(14, '2022', '1', 'Nguyen Duy Nam', '9B', '12358788', 'Nam', '12/02/2008', 'chuioi@gmail.com', '8424242', 'HN', 'No');
-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `teacher`
--

CREATE TABLE `teacher` (
  `Teacher_id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Phone` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `SecurityQ` varchar(45) NOT NULL,
  `SecurityA` varchar(45) NOT NULL,
  `Password` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `teacher`
--

INSERT INTO `teacher` (`Teacher_id`, `Name`, `Phone`, `Email`, `SecurityQ`, `SecurityA`, `Password`) VALUES
(0, 'Admin', '19001235', '', '', '', ''),
(1, 'Canh Phuong Van', '6958592698', 'canhpv@epu.edu.com', 'Sở thích của bạn', 'Code', '123456'),
(2, 'Dungx', '098889221', 'dung@gmail.com', 'Sở thích của bạn', 'Kiếm tiền', '123'),
(3, 'Lea', '06958592', 'ca@gmail.com', 'Bạn thích ăn gì', 'chiu', '123456'),
(4, 'abc', '0988', 'ssas', 'Bạn thích ăn gì', 'meo', '123'),
(5, 'Nhat', '055565656', 'nhat2@gmail.com', 'Sở thích của bạn', 'code', '123'),
(6, '233', '23', '23', 'Bạn thích ăn gì', 'ko', '123'),
(7, 'nhat minh', '13123', 'da', 'Bạn thích ăn gì', '12', '123'),
(8, 'ád', '123', '123', 'Bạn thích ăn gì', '123', '123'),
(9, '12322', '123', '1231', 'Sở thích của bạn', 'a', '1'),
(10, '123', '123', '123', 'Sở thích của bạn', '123', '123'),
(11, 'minh a', 'd', 'a', 'Sở thích của bạn', 'a', 'a');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Account`);

--
-- Chỉ mục cho bảng `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`IdAuttendance`),
  ADD KEY `Student_id` (`Student_id`) USING BTREE,
  ADD KEY `Lesson_id` (`Lesson_id`);

--
-- Chỉ mục cho bảng `class`
--
ALTER TABLE `class`
  ADD PRIMARY KEY (`Class`);

--
-- Chỉ mục cho bảng `lesson`
--
ALTER TABLE `lesson`
  ADD PRIMARY KEY (`Lesson_id`),
  ADD KEY `Class` (`Class`);

--
-- Chỉ mục cho bảng `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`Student_id`),
  ADD KEY `Class` (`Class`);

--
-- Chỉ mục cho bảng `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`Teacher_id`);

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_3` FOREIGN KEY (`Student_id`) REFERENCES `student` (`Student_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_ibfk_4` FOREIGN KEY (`Lesson_id`) REFERENCES `lesson` (`Lesson_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `lesson`
--
ALTER TABLE `lesson`
  ADD CONSTRAINT `lesson_ibfk_1` FOREIGN KEY (`Class`) REFERENCES `class` (`Class`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`Class`) REFERENCES `class` (`Class`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
