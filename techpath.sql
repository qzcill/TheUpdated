 USE techpath;


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


DROP TABLE IF EXISTS `quizoptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizoptions` (
  `option_id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `option_text` text NOT NULL,
  `value` int DEFAULT NULL,
  PRIMARY KEY (`option_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `quizoptions_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `quizquestions` (`question_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizoptions`
--

LOCK TABLES `quizoptions` WRITE;
/*!40000 ALTER TABLE `quizoptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `quizoptions` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `quizquestions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizquestions` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `question_text` text NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `quizquestions` WRITE;
/*!40000 ALTER TABLE `quizquestions` DISABLE KEYS */;
/*!40000 ALTER TABLE `quizquestions` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendations` (
  `rec_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `career_path` varchar(100) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`rec_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `recommendations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `recommendations` WRITE;
/*!40000 ALTER TABLE `recommendations` DISABLE KEYS */;
/*!40000 ALTER TABLE `recommendations` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `useranswers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `useranswers` (
  `answer_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `selected_option` int DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `user_id` (`user_id`),
  KEY `question_id` (`question_id`),
  KEY `selected_option` (`selected_option`),
  CONSTRAINT `useranswers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `useranswers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `quizquestions` (`question_id`) ON DELETE CASCADE,
  CONSTRAINT `useranswers_ibfk_3` FOREIGN KEY (`selected_option`) REFERENCES `quizoptions` (`option_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `useranswers` WRITE;
/*!40000 ALTER TABLE `useranswers` DISABLE KEYS */;
/*!40000 ALTER TABLE `useranswers` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


-- Insert 10 questions
INSERT INTO QuizQuestions (question_id, question_text) VALUES
(1, 'What type of problem excites you the most?'),
(2, 'In a team project, which role feels most like you?'),
(3, 'When you see a new technology, your first thought is:'),
(4, 'Which type of course would you enjoy most:'),
(5, 'Which challenge sounds more fun?'),
(6, 'What type of tools do you like working with?'),
(7, 'Which subject did you enjoy most?'),
(8, 'Imagine your future job, what excites you more?'),
(9, 'Your favorite type of project would be?'),
(10, 'Which statement describes you best?');

-- Insert ALL 71 options
INSERT INTO QuizOptions (option_id, question_id, option_text, value) VALUES
(1,1,'Teaching a computer to learn and make predictions',10),
(2,1,'Building an app or website that people can use',8),
(3,1,'Creating smooth and beautiful interfaces',7),
(4,1,'Finding security flaws before hackers do',9),
(5,1,'Discovering hidden insights from big datasets',10),
(6,1,'Designing fun and interactive games',8),
(7,1,'Deploying systems and making them scalable',9),
(8,2,'Writing the algorithm that makes it smart',10),
(9,2,'Building the main functionality of the app',8),
(10,2,'Designing how users will interact with it',7),
(11,2,'Making sure it''s safe and protected',9),
(12,2,'Collecting data and analyzing the results',10),
(13,2,'Designing how users will interact with it',7),
(14,2,'Designing game mechanics and levels',8),
(15,2,'Setting up servers and automating deployment',9),
(16,3,'How can I make this learn by itself?',10),
(17,3,'How can I build something useful with this?',8),
(18,3,'How can I make it look and feel amazing?',7),
(19,3,'How secure is this? Can it be hacked?',9),
(20,3,'What data can I gather and analyze from this?',10),
(21,3,'Can I make a game with this tech?',8),
(22,3,'How do I deploy this in the cloud?',9),
(23,4,'Machine Learning and AI',10),
(24,4,'Web/App Development',8),
(25,4,'UI/UX and Interaction Design',7),
(26,4,'Cybersecurity and Ethical Hacking',9),
(27,4,'Data Science and Big Data Analytics',10),
(28,4,'Game Design and Development',8),
(29,4,'Cloud Computing and DevOps',9),
(30,5,'Building a chatbot that understands users',10),
(31,5,'Creating a to-do list app that everyone likes',8),
(32,5,'Designing a smooth checkout flow for an e-commerce app',7),
(33,5,'Stopping a simulated cyber-attack',9),
(34,5,'Predicting future sales using past data',10),
(35,5,'Developing a multiplayer game',8),
(36,5,'Automating deployment to multiple servers',9),
(37,6,'Python, ML libraries (TensorFlow, PyTorch)',10),
(38,6,'React, Flutter, Node.js',8),
(39,6,'Figma, Adobe XD',7),
(40,6,'Wireshark, Kali Linux',9),
(41,6,'Excel, PowerBI, Jupyter Notebooks',10),
(42,6,'Unity, Unreal Engine',8),
(43,6,'Docker, Kubernetes, AWS',9),
(44,7,'Mathematics and Logic',10),
(45,7,'Computer Programming',8),
(46,7,'Arts and Creative Design',7),
(47,7,'Security and Risk',9),
(48,7,'Statistics and Analysis',10),
(49,7,'Physics and Game Mechanics',8),
(50,7,'Networking and Systems',9),
(51,8,'Building AI solutions',10),
(52,8,'Developing useful applications',8),
(53,8,'Designing experiences people like',7),
(54,8,'Protecting systems from attacks',9),
(55,8,'Turning data into business decisions',10),
(56,8,'Creating entertaining games',8),
(57,8,'Managing infrastructure for millions of users',9),
(58,9,'AI-based recommendation system',10),
(59,9,'E-commerce website or mobile app',8),
(60,9,'UI redesign of a popular app',7),
(61,9,'Penetration testing of a company network',9),
(62,9,'Data dashboard for decision makers',10),
(63,9,'3D game with interactive levels',8),
(64,9,'Scalable cloud service deployment',9),
(65,10,'"I think logically and love algorithms"',10),
(66,10,'"I enjoy building things people can use"',8),
(67,10,'"I care about how apps look and feel"',7),
(68,10,'"I always think about security and risks"',9),
(69,10,'"I like finding patterns in numbers and data"',10),
(70,10,'"I enjoy designing and making fun experiences"',8),
(71,10,'"I like managing systems and automating processes"',9);


SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE recommendations;
TRUNCATE TABLE useranswers;
TRUNCATE TABLE Users;
SET FOREIGN_KEY_CHECKS = 1;

SELECT * FROM Users;
SELECT * FROM quizoptions;
SELECT * FROM recommendations;
SELECT * FROM quizquestions;
SELECT * FROM useranswers;



