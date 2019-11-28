-- MySQL dump 10.13  Distrib 5.7.22, for osx10.13 (x86_64)
--
-- Host: localhost    Database: common
-- ------------------------------------------------------
-- Server version	5.7.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app`
--

DROP TABLE IF EXISTS `app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `icon` varchar(1024) NOT NULL DEFAULT '',
  `name_cn` varchar(64) NOT NULL DEFAULT '',
  `name_en` varchar(64) NOT NULL DEFAULT '',
  `des_cn` varchar(1024) NOT NULL DEFAULT '',
  `des_en` varchar(1024) NOT NULL DEFAULT '',
  `appleid` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `url_scheme` varchar(32) NOT NULL DEFAULT '',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app`
--

LOCK TABLES `app` WRITE;
/*!40000 ALTER TABLE `app` DISABLE KEYS */;
INSERT INTO `app` VALUES (1,'https://api.madan.asia/static/image/footchina.png','足迹中国','Footprint China','用地图记录你去过的中国的省市','track your footprint of china',1482250279,1,'Footprint-China','2019-11-13 15:11:15','2019-11-13 07:11:15'),(2,'https://api.madan.asia/static/image/pseudocall.png','假冒来电','Pseudo Call','假冒来电,来逃离无意义的聚会,或者开开玩笑','Receive fake call to escape meaningless meetings or just play jokes',1475866564,1,'Pseudo-Call','2019-11-13 15:11:15','2019-11-13 07:11:15'),(3,'https://api.madan.asia/static/image/istatwidget.png','iStat Widget','iStat Widget','查看硬件信息','Lookup Hardware Info',1476638491,1,'iStat-Widget','2019-11-13 15:11:15','2019-11-13 07:11:15'),(4,'https://api.madan.asia/static/image/widgetbomb.png','Widget Bomb','Widget Bomb','Top Widget Casual Game','Top Widget Casual Game',1475855829,1,'fingertip-bomb','2019-11-13 15:11:15','2019-11-13 07:11:15'),(5,'https://api.madan.asia/static/image/dailytoolset.jpg','生活小盒子','Daily Toolset','包含各种实用和好玩的小工具','bunch of tools',1450233831,1,'life-box','2019-11-13 15:11:15','2019-11-13 07:11:15'),(6,'https://api.madan.asia/static/image/xCoins.jpg','xCoins','xCoins','破解比特币私钥','Hack Bitcoin Private Key',1335320802,1,'xCoins','2019-11-13 15:11:15','2019-11-13 07:11:15'),(7,'https://api.madan.asia/static/image/quickervpn.jpg','Quicker***','Quicker VPN','securely surfing','securely surfing',1131521365,1,'','2019-11-13 15:11:15','2019-11-13 07:11:15'),(8,'https://api.madan.asia/static/image/ssandvpn.jpg','SS+***','SS+VPN','Secure Web Surfing','Secure Web Surfing',1454747687,1,'','2019-11-13 15:11:15','2019-11-13 07:11:15'),(9,'https://api.madan.asia/static/image/dynamicqrcode.jpg','特效二维码','Dynamic QR','制作会动的二维码','Generate Animated QRCode',1453005528,1,'','2019-11-13 15:11:15','2019-11-13 07:11:15');
/*!40000 ALTER TABLE `app` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-28 20:27:48
