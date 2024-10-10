-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: erp_flask
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `endereco` varchar(200) DEFAULT NULL,
  `telefone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'João Silva','Rua 1','1699544-8877'),(2,'Maria Souza','Rua 2','1699544-8877'),(3,'Carlos Pereira','Rua 3','1699544-8877'),(5,'Taiz F B Silva','Rua Tenente Catão Roxo','16997015416'),(6,'Gabriel','Rua 4','16987654322');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configuracoes`
--

DROP TABLE IF EXISTS `configuracoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuracoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chave` varchar(50) NOT NULL,
  `valor` varchar(255) NOT NULL,
  `cor` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracoes`
--

LOCK TABLES `configuracoes` WRITE;
/*!40000 ALTER TABLE `configuracoes` DISABLE KEYS */;
INSERT INTO `configuracoes` VALUES (1,'tema','claro','#4CAF50'),(2,'tema','claro','#4CAF50'),(3,'tema','claro','#4CAF50');
/*!40000 ALTER TABLE `configuracoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `endereco` varchar(255) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresa`
--

LOCK TABLES `empresa` WRITE;
/*!40000 ALTER TABLE `empresa` DISABLE KEYS */;
INSERT INTO `empresa` VALUES (1,'Gabriel Bazo LTDA','12.343.212/0001-23','Rua teste','163344-5566','gbltda@gmail.com');
/*!40000 ALTER TABLE `empresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itens_venda`
--

DROP TABLE IF EXISTS `itens_venda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itens_venda` (
  `id` int NOT NULL AUTO_INCREMENT,
  `venda_id` int DEFAULT NULL,
  `produto_id` int DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `venda_id` (`venda_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `itens_venda_ibfk_1` FOREIGN KEY (`venda_id`) REFERENCES `vendas` (`id`),
  CONSTRAINT `itens_venda_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itens_venda`
--

LOCK TABLES `itens_venda` WRITE;
/*!40000 ALTER TABLE `itens_venda` DISABLE KEYS */;
INSERT INTO `itens_venda` VALUES (1,17,3,1,1.50),(2,17,4,1,2.50),(3,17,1,1,4.50),(4,17,2,1,3.00),(5,18,3,1,1.50),(6,18,4,1,2.50),(7,18,1,1,4.50),(8,18,2,1,3.00),(9,19,3,1,1.50),(10,19,4,1,2.50),(11,19,1,1,4.50),(12,21,3,1,1.50),(13,21,4,1,2.50),(14,21,1,1,4.50),(15,22,3,1,1.50),(16,22,4,1,2.50),(17,22,1,1,4.50),(18,22,2,1,3.00),(19,23,3,3,1.50),(20,23,4,1,2.50),(21,23,1,3,4.50),(22,23,2,1,3.00),(23,24,3,3,1.50),(24,24,3,1,1.50),(25,25,3,1,1.50),(26,26,3,1,1.50),(27,26,4,1,2.50),(28,26,1,1,4.50),(29,26,2,1,3.00),(30,27,3,3,1.50),(31,27,4,3,2.50),(32,27,1,3,4.50),(33,28,3,1,1.50),(34,28,4,1,2.50),(35,29,3,1,1.50),(36,29,4,1,2.50),(37,29,1,1,4.50),(38,29,2,1,3.00),(39,30,3,1,1.50),(40,31,3,1,1.50),(41,32,3,1,1.50),(42,33,3,2,1.50),(43,33,4,4,2.50),(44,33,1,3,4.50),(45,34,3,2,1.50),(46,34,4,2,2.50),(47,34,1,7,4.50),(48,35,3,1,1.50),(49,35,4,1,2.50),(50,35,1,1,4.50),(51,36,3,1,1.50),(52,36,4,1,2.50),(53,36,1,1,4.50),(54,37,3,1,1.50),(55,37,4,1,2.50),(56,37,1,1,4.50),(57,38,3,1,1.50),(58,38,4,1,2.50),(59,38,1,1,4.50),(60,39,3,1,1.50),(61,40,3,10,1.50),(62,41,4,1,2.50),(63,41,1,1,4.50),(64,41,2,1,3.00),(65,42,4,2,2.50),(66,42,1,1,4.50),(67,42,2,1,3.00),(68,43,3,3,1.50),(69,43,4,1,2.50),(70,43,1,3,4.50),(71,43,2,5,3.00);
/*!40000 ALTER TABLE `itens_venda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `quantidade` int NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `cod_barras` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Sanduíche',50,4.50,'1003'),(2,'Suco',30,3.00,'1004'),(3,'Bolacha',10,1.50,'1001'),(4,'Banana',15,2.50,'1002');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'gbazo','$2b$12$3laYyBRUzftUtG05hCU5leaVV1K72Hen1UqTJhYJu6V8uGh5Vb.lm','bazot3@hotmail.com','2024-08-22 18:11:00');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendas`
--

DROP TABLE IF EXISTS `vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_venda` datetime DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) DEFAULT NULL,
  `cliente_cod` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_cod` (`cliente_cod`),
  CONSTRAINT `vendas_ibfk_1` FOREIGN KEY (`cliente_cod`) REFERENCES `clientes` (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas`
--

LOCK TABLES `vendas` WRITE;
/*!40000 ALTER TABLE `vendas` DISABLE KEYS */;
INSERT INTO `vendas` VALUES (17,'2024-08-26 11:30:35',11.50,NULL),(18,'2024-08-26 11:31:45',11.50,NULL),(19,'2024-08-26 11:36:20',8.50,NULL),(20,'2024-08-26 11:38:45',0.00,NULL),(21,'2024-08-26 11:39:27',8.50,NULL),(22,'2024-08-26 11:40:12',11.50,NULL),(23,'2024-08-26 11:43:00',23.50,NULL),(24,'2024-08-26 11:50:47',6.00,NULL),(25,'2024-08-26 11:54:50',1.50,NULL),(26,'2024-08-26 11:57:49',11.50,NULL),(27,'2024-08-26 14:58:35',25.50,NULL),(28,'2024-08-26 15:01:43',4.00,NULL),(29,'2024-08-26 15:22:52',11.50,NULL),(30,'2024-08-26 15:27:00',1.50,NULL),(31,'2024-08-26 15:30:35',1.50,1),(32,'2024-08-26 15:37:15',1.50,NULL),(33,'2024-08-26 16:04:15',26.50,NULL),(34,'2024-08-26 16:12:34',39.50,NULL),(35,'2024-08-26 16:17:59',8.50,NULL),(36,'2024-08-26 16:20:18',8.50,NULL),(37,'2024-08-27 07:55:59',8.50,NULL),(38,'2024-08-27 08:04:32',8.50,NULL),(39,'2024-08-27 09:53:09',1.50,NULL),(40,'2024-08-27 12:03:14',15.00,NULL),(41,'2024-08-27 12:23:37',10.00,NULL),(42,'2024-08-27 12:24:12',12.50,NULL),(43,'2024-08-28 07:50:53',35.50,NULL);
/*!40000 ALTER TABLE `vendas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-28 10:00:09
