-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: buscapharma
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `agendamento`
--

DROP TABLE IF EXISTS `agendamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agendamento` (
  `id_agend` int NOT NULL AUTO_INCREMENT,
  `id_unidade` int DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `status` enum('agendado','realizado','cancelado') NOT NULL,
  `data` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `objetivo` enum('Remédio','Vacina') DEFAULT NULL,
  PRIMARY KEY (`id_agend`),
  KEY `FK_Agendamento_Unidade` (`id_unidade`),
  KEY `FK_Agendamento_Usuario` (`id_usuario`),
  CONSTRAINT `FK_Agendamento_Unidade` FOREIGN KEY (`id_unidade`) REFERENCES `unidade` (`id_unidade`),
  CONSTRAINT `FK_Agendamento_Usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendamento`
--

LOCK TABLES `agendamento` WRITE;
/*!40000 ALTER TABLE `agendamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `agendamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aux_item_indicacao`
--

DROP TABLE IF EXISTS `aux_item_indicacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aux_item_indicacao` (
  `id_item` int NOT NULL,
  `id_indicacao` int NOT NULL,
  PRIMARY KEY (`id_item`,`id_indicacao`),
  KEY `FK_Aux_Item_Indicacao_Indicacao` (`id_indicacao`),
  CONSTRAINT `FK_Aux_Item_Indicacao_Indicacao` FOREIGN KEY (`id_indicacao`) REFERENCES `indicacao` (`id_indicacao`),
  CONSTRAINT `FK_Aux_Item_Indicacao_Item` FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aux_item_indicacao`
--

LOCK TABLES `aux_item_indicacao` WRITE;
/*!40000 ALTER TABLE `aux_item_indicacao` DISABLE KEYS */;
INSERT INTO `aux_item_indicacao` VALUES (1,1),(3,1),(13,1),(2,2),(4,2),(5,3),(6,5),(9,5),(7,6),(8,7),(10,8),(12,8),(11,9),(14,10);
/*!40000 ALTER TABLE `aux_item_indicacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aux_unidade_item`
--

DROP TABLE IF EXISTS `aux_unidade_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aux_unidade_item` (
  `id_item` int NOT NULL,
  `id_unidade` int NOT NULL,
  `qtde_atual` int DEFAULT NULL,
  PRIMARY KEY (`id_item`,`id_unidade`),
  KEY `FK_Aux_Unidade_Item_Unidade` (`id_unidade`),
  CONSTRAINT `FK_Aux_Unidade_Item_Item` FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`),
  CONSTRAINT `FK_Aux_Unidade_Item_Unidade` FOREIGN KEY (`id_unidade`) REFERENCES `unidade` (`id_unidade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aux_unidade_item`
--

LOCK TABLES `aux_unidade_item` WRITE;
/*!40000 ALTER TABLE `aux_unidade_item` DISABLE KEYS */;
INSERT INTO `aux_unidade_item` VALUES (1,1,50),(1,2,30),(2,1,150),(2,2,50),(3,3,60),(4,3,40),(5,3,20),(6,4,80),(7,5,70),(8,5,50),(9,2,40),(10,1,80),(11,1,30),(12,2,40),(13,3,20),(14,4,30),(15,1,100),(15,2,100);
/*!40000 ALTER TABLE `aux_unidade_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `indicacao`
--

DROP TABLE IF EXISTS `indicacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `indicacao` (
  `id_indicacao` int NOT NULL AUTO_INCREMENT,
  `categoria_remedio` varchar(150) DEFAULT NULL,
  `posologia` varchar(150) DEFAULT NULL,
  `precaucao` varchar(150) DEFAULT NULL,
  `contra_indicacao` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_indicacao`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indicacao`
--

LOCK TABLES `indicacao` WRITE;
/*!40000 ALTER TABLE `indicacao` DISABLE KEYS */;
INSERT INTO `indicacao` VALUES (1,'Analgesico','1 comprimido a cada 6 horas','Não tomar em jejum','Alergia ao componente ativo'),(2,'Anti-inflamatório','1 comprimido a cada 8 horas','Evitar exposição solar','Insuficiência renal'),(3,'Antibiótico','1 cápsula a cada 12 horas','Tomar com bastante água','Gravidez'),(4,'Antitérmico','1 comprimido a cada 4 horas','Não tomar com álcool','Doença hepática'),(5,'Anti-hipertensivo','1 comprimido por dia','Monitorar pressão arterial regularmente','Bradicardia'),(6,'Antiácido','1 cápsula antes das refeições','Evitar álcool','Insuficiência hepática'),(7,'Antiflatulento','1 comprimido após as refeições','Tomar com água','Hipersensibilidade'),(8,'Anti-histamínico','1 comprimido por dia','Evitar dirigir','Glaucoma'),(9,'Antidiabético','1 comprimido a cada 12 horas','Monitorar glicose','Insuficiência renal'),(10,'Broncodilatador','1 inalação a cada 4 horas','Não exceder a dose','Doença cardíaca');
/*!40000 ALTER TABLE `indicacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `id_item` int NOT NULL AUTO_INCREMENT,
  `id_tipo` int DEFAULT NULL,
  `nome_item` varchar(255) DEFAULT NULL,
  `comp_ativ_itm` varchar(255) DEFAULT NULL,
  `qtde_max` int DEFAULT NULL,
  `qtde_min` int DEFAULT NULL,
  PRIMARY KEY (`id_item`),
  KEY `FK_Item_Tipo_Item` (`id_tipo`),
  CONSTRAINT `FK_Item_Tipo_Item` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_item` (`id_tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,1,'Paracetamol 500mg','Paracetamol',100,10),(2,1,'Aas 100mg','ácido acetilsalicílico',100,10),(3,1,'Dipirona 500mg','dipirona monoidratada',100,10),(4,1,'Ibuprofeno 400mg','ibuprofeno',100,10),(5,1,'Amoxicilina 500mg','amoxicilina',100,10),(6,1,'Captopril 50mg','captopril',100,10),(7,1,'Omeprazol 20mg','omeprazol',100,10),(8,1,'Simeticona 125mg','simeticona',100,10),(9,1,'Losartana potássica 50mg','losartana potássica',100,10),(10,1,'Loratadina 10mg','loratadina',100,10),(11,1,'Metformina 500mg','metformina',100,10),(12,1,'Zyrtec 10mg','dicloridrato de cetirizina',100,10),(13,1,'Clonazepam 2mg','clonazepam',80,10),(14,1,'Aerolin 100mcg/dose','sulfato de salbutamol',80,10),(15,2,'Vacina Polio','vírus da poliomielite dos tipos 1, 2 e 3',200,20);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lote`
--

DROP TABLE IF EXISTS `lote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lote` (
  `num_lote` varchar(20) NOT NULL,
  `id_item` int DEFAULT NULL,
  `validade` date DEFAULT NULL,
  `qtde` int DEFAULT NULL,
  PRIMARY KEY (`num_lote`),
  KEY `FK_Lote_Item` (`id_item`),
  CONSTRAINT `FK_Lote_Item` FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
INSERT INTO `lote` VALUES ('L09876',2,'2025-05-01',50),('L10101',12,'2024-10-05',40),('L11111',3,'2024-10-15',60),('L12121',13,'2024-09-15',20),('L12345',1,'2024-12-31',50),('L13131',14,'2025-01-25',30),('L14141',15,'2025-12-31',200),('L22222',4,'2025-01-20',40),('L33333',5,'2024-09-30',20),('L44444',6,'2025-03-15',80),('L54321',2,'2025-05-01',150),('L55555',7,'2024-08-30',70),('L66666',8,'2025-02-10',50),('L67890',1,'2024-12-31',30),('L77777',9,'2025-07-01',40),('L88888',10,'2024-11-20',80),('L99999',11,'2025-04-10',30);
/*!40000 ALTER TABLE `lote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `protocolo`
--

DROP TABLE IF EXISTS `protocolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocolo` (
  `id_protocolo` int NOT NULL AUTO_INCREMENT,
  `id_item` int DEFAULT NULL,
  `periodicidade` varchar(150) DEFAULT NULL,
  `documento_necessario` varchar(255) DEFAULT NULL,
  `exames` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_protocolo`),
  KEY `FK_Protocolo_Item` (`id_item`),
  CONSTRAINT `FK_Protocolo_Item` FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocolo`
--

LOCK TABLES `protocolo` WRITE;
/*!40000 ALTER TABLE `protocolo` DISABLE KEYS */;
/*!40000 ALTER TABLE `protocolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_item`
--

DROP TABLE IF EXISTS `tipo_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_item` (
  `id_tipo` int NOT NULL AUTO_INCREMENT,
  `descricao` enum('Remédio','Vacina') NOT NULL,
  PRIMARY KEY (`id_tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_item`
--

LOCK TABLES `tipo_item` WRITE;
/*!40000 ALTER TABLE `tipo_item` DISABLE KEYS */;
INSERT INTO `tipo_item` VALUES (1,'Remédio'),(2,'Vacina');
/*!40000 ALTER TABLE `tipo_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_unidade`
--

DROP TABLE IF EXISTS `tipo_unidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_unidade` (
  `id_tipo_unidade` int NOT NULL AUTO_INCREMENT,
  `desc_unidade` enum('Hospital','Ubs','Upa','Farmacia popular','Alto custo') NOT NULL,
  PRIMARY KEY (`id_tipo_unidade`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_unidade`
--

LOCK TABLES `tipo_unidade` WRITE;
/*!40000 ALTER TABLE `tipo_unidade` DISABLE KEYS */;
INSERT INTO `tipo_unidade` VALUES (1,'Hospital'),(2,'Ubs'),(3,'Upa'),(4,'Farmacia popular'),(5,'Alto custo');
/*!40000 ALTER TABLE `tipo_unidade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidade`
--

DROP TABLE IF EXISTS `unidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidade` (
  `id_unidade` int NOT NULL AUTO_INCREMENT,
  `id_tipo_unidade` int DEFAULT NULL,
  `nome` varchar(130) NOT NULL,
  `status` enum('aberto','fechado','em manutencao') NOT NULL,
  `cep` varchar(9) NOT NULL,
  `hora_abertura` time DEFAULT NULL,
  `hora_encerramento` time DEFAULT NULL,
  PRIMARY KEY (`id_unidade`),
  KEY `FK_Unidade_Tipo_Unidade` (`id_tipo_unidade`),
  CONSTRAINT `FK_Unidade_Tipo_Unidade` FOREIGN KEY (`id_tipo_unidade`) REFERENCES `tipo_unidade` (`id_tipo_unidade`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidade`
--

LOCK TABLES `unidade` WRITE;
/*!40000 ALTER TABLE `unidade` DISABLE KEYS */;
INSERT INTO `unidade` VALUES (1,1,'Hospital Central','aberto','12345-678','08:00:00','18:00:00'),(2,2,'UBS Vila Nova','fechado','23456-789','07:00:00','17:00:00'),(3,3,'UPA Zona Sul','em manutencao','34567-890','09:00:00','21:00:00'),(4,2,'UBS Jardim Primavera','aberto','45678-901','07:00:00','17:00:00'),(5,4,'Farmacia Popular Centro','aberto','56789-012','08:00:00','20:00:00');
/*!40000 ALTER TABLE `unidade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `id_unidade` int DEFAULT NULL,
  `cpf` varchar(14) NOT NULL,
  `date_joined` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_staff` tinyint DEFAULT NULL,
  `is_active` tinyint DEFAULT NULL,
  `is_superuser` tinyint DEFAULT NULL,
  `first_name` varchar(120) DEFAULT NULL,
  `last_name` varchar(120) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `telefone` varchar(14) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `FK_Usuario_Unidade` (`id_unidade`),
  CONSTRAINT `FK_Usuario_Unidade` FOREIGN KEY (`id_unidade`) REFERENCES `unidade` (`id_unidade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'buscapharma'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-29 17:21:14
