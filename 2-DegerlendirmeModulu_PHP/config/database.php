<?php
// config/database.php - PDO Veritabanı Yapılandırması (MySQL & SQLite Fallback)

class Database {
    private static ?PDO $instance = null;

    public static function getConnection(): PDO {
        if (self::$instance !== null) {
            return self::$instance;
        }

        $driver = getenv('DB_DRIVER') ?: 'mysql';
        $host = getenv('DB_HOST') ?: '127.0.0.1';
        $port = getenv('DB_PORT') ?: '3306';
        $dbName = getenv('DB_NAME') ?: 'etikkurul_degerlendirme';
        $user = getenv('DB_USER') ?: 'root';
        $pass = getenv('DB_PASS') ?: '';

        if ($driver === 'mysql') {
            try {
                $dsn = "mysql:host={$host};port={$port};charset=utf8mb4";
                $pdo = new PDO($dsn, $user, $pass, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                    PDO::ATTR_TIMEOUT => 2
                ]);
                $pdo->exec("CREATE DATABASE IF NOT EXISTS `{$dbName}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
                $pdo->exec("USE `{$dbName}`");
                self::$instance = $pdo;
                self::ensureTablesExist(self::$instance, 'mysql');
                return self::$instance;
            } catch (Throwable $e) {
                // MySQL erişilemezse yerel SQLite fallback devreye girer
                error_log("[MySQL Hatası] {$e->getMessage()} - Yerel SQLite veritabanına geçiliyor.");
            }
        }

        // SQLite Fallback / Test DB (Her zaman tam yazma yetkisi olan temp dizini)
        $sqlitePath = sys_get_temp_dir() . '/etikkurul_evaluation.sqlite';
        $pdo = new PDO("sqlite:{$sqlitePath}", null, null, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]);
        $pdo->exec("PRAGMA journal_mode = MEMORY;");
        $pdo->exec("PRAGMA synchronous = OFF;");
        self::$instance = $pdo;
        self::ensureTablesExist(self::$instance, 'sqlite');
        return self::$instance;
    }

    private static function ensureTablesExist(PDO $pdo, string $engine): void {
        $autoInc = ($engine === 'sqlite') ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT AUTO_INCREMENT PRIMARY KEY';
        
        $pdo->exec("CREATE TABLE IF NOT EXISTS committee_members (
            id {$autoInc},
            full_name VARCHAR(150) NOT NULL,
            title VARCHAR(100) NOT NULL,
            field_of_expertise VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            phone VARCHAR(50) DEFAULT NULL,
            active_file_count INT DEFAULT 0,
            is_active INT DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )");

        $pdo->exec("CREATE TABLE IF NOT EXISTS file_assignments (
            id {$autoInc},
            protocol_number VARCHAR(50) NOT NULL,
            project_title VARCHAR(300) NOT NULL,
            field_of_study VARCHAR(100) NOT NULL,
            member_id INT NOT NULL,
            assignment_status VARCHAR(50) DEFAULT 'Pending',
            assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
            due_date TEXT DEFAULT NULL
        )");

        $pdo->exec("CREATE TABLE IF NOT EXISTS evaluations (
            id {$autoInc},
            assignment_id INT NOT NULL,
            protocol_number VARCHAR(50) NOT NULL,
            member_id INT NOT NULL,
            methodology_score INT NOT NULL,
            consent_form_score INT NOT NULL,
            risk_assessment_score INT NOT NULL,
            decision VARCHAR(50) NOT NULL,
            feedback_notes TEXT NOT NULL,
            evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )");

        // Seed if empty
        $stmt = $pdo->query("SELECT COUNT(*) as cnt FROM committee_members");
        $row = $stmt->fetch();
        if ($row && $row['cnt'] == 0) {
            $seeds = [
                ['Prof. Dr. Selim Vural', 'Prof. Dr.', 'Tıp / Biyomedikal', 'selim.vural@universite.edu.tr', '+90 532 111 2233', 0],
                ['Doç. Dr. Ayşe Gündüz', 'Doç. Dr.', 'Klinik Psikoloji', 'ayse.gunduz@universite.edu.tr', '+90 532 222 3344', 0],
                ['Prof. Dr. Kerem Yaman', 'Prof. Dr.', 'Sosyal Bilimler / Hukuk', 'kerem.yaman@universite.edu.tr', '+90 532 333 4455', 0],
                ['Doç. Dr. Emre Karaca', 'Doç. Dr.', 'Eğitim Bilimleri', 'emre.karaca@universite.edu.tr', '+90 532 444 5566', 0],
                ['Dr. Öğr. Üyesi Burcu Polat', 'Dr. Öğr. Üyesi', 'Biyomedikal / Genetik', 'burcu.polat@universite.edu.tr', '+90 532 555 6677', 0],
                ['Prof. Dr. Murat Doğan', 'Prof. Dr.', 'Tıp / Dahili Bilimler', 'murat.dogan@universite.edu.tr', '+90 532 666 7788', 0]
            ];
            $ins = $pdo->prepare("INSERT INTO committee_members (full_name, title, field_of_expertise, email, phone, active_file_count) VALUES (?, ?, ?, ?, ?, ?)");
            foreach ($seeds as $s) {
                $ins->execute($s);
            }
        }
    }
}
