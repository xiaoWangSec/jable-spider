/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50738
Source Host           : localhost:3306
Source Database       : jable

Target Server Type    : MYSQL
Target Server Version : 50738
File Encoding         : 65001

Date: 2023-10-10 14:35:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for avdb_images
-- ----------------------------
DROP TABLE IF EXISTS `avdb_images`;
CREATE TABLE `avdb_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `car` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `actor` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `img_base64` mediumtext,
  `tags` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `car_inex` (`car`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=27422 DEFAULT CHARSET=utf8mb4;
