-- --------------------------------------------------------
-- 호스트:                          aodd.xyz
-- 서버 버전:                        10.4.32-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- pydns 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `pydns` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */;
USE `pydns`;

-- 테이블 pydns.records 구조 내보내기
CREATE TABLE IF NOT EXISTS `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` mediumtext NOT NULL,
  `record` tinytext NOT NULL,
  `value` mediumtext DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `Domain` (`domain`(1024)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- 테이블 데이터 pydns.records:~2 rows (대략적) 내보내기
INSERT INTO `records` (`id`, `domain`, `record`, `value`) VALUES
	(1, '1.0.0.127.in-addr.arpa.', 'A', 'pydns localhost IPv4'),
	(2, '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa.', 'A', 'pydns localhost IPv6');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
