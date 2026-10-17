-- Etik Kurul Otomasyonu - Modül 2: Kurul Değerlendirme & Atama (MySQL)

CREATE DATABASE IF NOT EXISTS `etikkurul_degerlendirme` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `etikkurul_degerlendirme`;

-- Kurul Üyeleri Tablosu
CREATE TABLE IF NOT EXISTS `committee_members` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `full_name` VARCHAR(150) NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `field_of_expertise` VARCHAR(100) NOT NULL, -- Tıp, Psikoloji, Biyomedikal, Sosyal Bilimler, Mühendislik, Eğitim
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(50) DEFAULT NULL,
    `active_file_count` INT DEFAULT 0,
    `is_active` TINYINT(1) DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Otomatik Dosya Atamaları Tablosu
CREATE TABLE IF NOT EXISTS `file_assignments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `protocol_number` VARCHAR(50) NOT NULL, -- Modül 1'den gelen ETIK-YYYY-XXXXX
    `project_title` VARCHAR(300) NOT NULL,
    `field_of_study` VARCHAR(100) NOT NULL,
    `member_id` INT NOT NULL,
    `assignment_status` ENUM('Pending', 'InReview', 'Completed') DEFAULT 'Pending',
    `assigned_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `due_date` DATE DEFAULT NULL,
    FOREIGN KEY (`member_id`) REFERENCES `committee_members`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Üye Değerlendirme & Görüş Tablosu
CREATE TABLE IF NOT EXISTS `evaluations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `assignment_id` INT NOT NULL,
    `protocol_number` VARCHAR(50) NOT NULL,
    `member_id` INT NOT NULL,
    `methodology_score` INT NOT NULL CHECK (`methodology_score` BETWEEN 1 AND 5),
    `consent_form_score` INT NOT NULL CHECK (`consent_form_score` BETWEEN 1 AND 5),
    `risk_assessment_score` INT NOT NULL CHECK (`risk_assessment_score` BETWEEN 1 AND 5),
    `decision` ENUM('Approved', 'RevisionNeeded', 'Rejected') NOT NULL,
    `feedback_notes` TEXT NOT NULL,
    `evaluated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`assignment_id`) REFERENCES `file_assignments`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`member_id`) REFERENCES `committee_members`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Örnek Kurul Üyeleri Tohum Verileri (Seed Data)
INSERT INTO `committee_members` (`id`, `full_name`, `title`, `field_of_expertise`, `email`, `phone`, `active_file_count`, `is_active`) VALUES
(1, 'Prof. Dr. Selim Vural', 'Prof. Dr.', 'Tıp / Biyomedikal', 'selim.vural@universite.edu.tr', '+90 532 111 2233', 0, 1),
(2, 'Doç. Dr. Ayşe Gündüz', 'Doç. Dr.', 'Klinik Psikoloji', 'ayse.gunduz@universite.edu.tr', '+90 532 222 3344', 0, 1),
(3, 'Prof. Dr. Kerem Yaman', 'Prof. Dr.', 'Sosyal Bilimler / Hukuk', 'kerem.yaman@universite.edu.tr', '+90 532 333 4455', 0, 1),
(4, 'Doç. Dr. Emre Karaca', 'Doç. Dr.', 'Eğitim Bilimleri', 'emre.karaca@universite.edu.tr', '+90 532 444 5566', 0, 1),
(5, 'Dr. Öğr. Üyesi Burcu Polat', 'Dr. Öğr. Üyesi', 'Biyomedikal / Genetik', 'burcu.polat@universite.edu.tr', '+90 532 555 6677', 0, 1),
(6, 'Prof. Dr. Murat Doğan', 'Prof. Dr.', 'Tıp / Dahili Bilimler', 'murat.dogan@universite.edu.tr', '+90 532 666 7788', 0, 1)
ON DUPLICATE KEY UPDATE `full_name`=VALUES(`full_name`);
