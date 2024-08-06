-- --------------------------------------------------------
-- 主機:                           127.0.0.1
-- 伺服器版本:                        10.11.6-MariaDB-1:10.11.6+maria~ubu2204 - mariadb.org binary distribution
-- 伺服器作業系統:                      debian-linux-gnu
-- HeidiSQL 版本:                  12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 nchu_auth 的資料庫結構
CREATE DATABASE IF NOT EXISTS `nchu_auth` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `nchu_auth`;

-- 傾印  資料表 nchu_auth.account 結構
CREATE TABLE IF NOT EXISTS `account` (
  `ID` uuid NOT NULL DEFAULT uuid(),
  `Role` varchar(15) NOT NULL DEFAULT 'User' COMMENT '''User'', ''Manager''',
  `Login_ID` varchar(64) DEFAULT NULL,
  `Name` varchar(128) DEFAULT NULL,
  `Email` varchar(320) DEFAULT NULL,
  `Valid_Email` binary(1) DEFAULT '0',
  `Password` varchar(128) DEFAULT NULL,
  `Password_Salt` varchar(16) DEFAULT NULL,
  `Token` varchar(128) DEFAULT NULL,
  `Resource_Token` varchar(64) DEFAULT NULL,
  `Gender` varchar(50) NOT NULL DEFAULT 'Unselected' COMMENT '''Unselected'', ''Male'', ''Female'', ...',
  `Department` varchar(128) DEFAULT NULL,
  `Grade` varchar(32) DEFAULT NULL,
  `Photo` mediumtext DEFAULT NULL,
  `Google_ID` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `Login_ID` (`Login_ID`),
  KEY `google_id` (`Google_ID`) USING BTREE,
  CONSTRAINT `google_id` FOREIGN KEY (`Google_ID`) REFERENCES `google_user` (`ID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 nchu_auth.authenticating 結構
CREATE TABLE IF NOT EXISTS `authenticating` (
  `ID` varchar(64) NOT NULL,
  `State` varchar(15) NOT NULL DEFAULT 'Unused' COMMENT '''Used'', ''Unused''',
  `Expire` datetime NOT NULL,
  `Redirect_URl` text DEFAULT NULL,
  `Client_ID` uuid NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  KEY `FK_authenticating_client` (`Client_ID`),
  CONSTRAINT `FK_authenticating_client` FOREIGN KEY (`Client_ID`) REFERENCES `client` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 nchu_auth.authenticating_email 結構
CREATE TABLE IF NOT EXISTS `authenticating_email` (
  `ID` varchar(128) NOT NULL,
  `Email` varchar(320) NOT NULL,
  `Expire` datetime NOT NULL,
  `CreateBy` uuid NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  KEY `FK_authenticating_email_account` (`CreateBy`),
  CONSTRAINT `FK_authenticating_email_account` FOREIGN KEY (`CreateBy`) REFERENCES `account` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 nchu_auth.client 結構
CREATE TABLE IF NOT EXISTS `client` (
  `Create_Time` datetime NOT NULL DEFAULT current_timestamp(),
  `ID` uuid NOT NULL DEFAULT uuid(),
  `Token` varchar(64) DEFAULT NULL,
  `Name` text NOT NULL,
  `Image` mediumtext NOT NULL,
  `ApplyBy` uuid DEFAULT NULL,
  `State` varchar(10) NOT NULL DEFAULT 'Pending' COMMENT '''Pending'', ''Approved'', ''Rejected''',
  PRIMARY KEY (`ID`),
  KEY `FK_client_account` (`ApplyBy`),
  CONSTRAINT `FK_client_account` FOREIGN KEY (`ApplyBy`) REFERENCES `account` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 nchu_auth.google_user 結構
CREATE TABLE IF NOT EXISTS `google_user` (
  `ID` varchar(512) NOT NULL,
  `Email` text DEFAULT NULL,
  `Name` text DEFAULT NULL,
  `Picture_URL` text DEFAULT NULL,
  `Locale` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 nchu_auth.log 結構
CREATE TABLE IF NOT EXISTS `log` (
  `logID` bigint(20) NOT NULL AUTO_INCREMENT,
  `log_time` datetime DEFAULT current_timestamp(),
  `level` varchar(50) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`logID`)
) ENGINE=InnoDB AUTO_INCREMENT=1637 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
