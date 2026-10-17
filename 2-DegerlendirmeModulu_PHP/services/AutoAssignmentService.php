<?php
// services/AutoAssignmentService.php - Akıllı Otomatik Dosya Atama Motoru

require_once __DIR__ . '/../models/CommitteeMember.php';
require_once __DIR__ . '/../models/Assignment.php';

class AutoAssignmentService {

    /**
     * Başvuruyu uzmanlık alanına ve mevcut dosya yük dengesine göre otomatik atar.
     *
     * @param string $protocolNumber Başvuru Protokol No (ETIK-YYYY-XXXXX)
     * @param string $projectTitle Proje Başlığı
     * @param string $fieldOfStudy Araştırma Alanı (Tıp, Psikoloji, Sosyal Bilimler, vb.)
     * @param int $requiredReviewers Atanacak üye sayısı (varsayılan: 2)
     * @return array Atama sonuçları
     */
    public function autoAssign(string $protocolNumber, string $projectTitle, string $fieldOfStudy, int $requiredReviewers = 2): array {
        // Zaten atanmış mı kontrol et
        $existing = Assignment::findByProtocol($protocolNumber);
        if (!empty($existing)) {
            return [
                'status' => 'already_assigned',
                'message' => "Protokol {$protocolNumber} için zaten " . count($existing) . " üye atanmış.",
                'assignments' => $existing
            ];
        }

        $allMembers = CommitteeMember::all(true);
        if (count($allMembers) < $requiredReviewers) {
            throw new RuntimeException("Sistemde yeterli aktif kurul üyesi bulunamadı. Gerekli: {$requiredReviewers}, Mevcut: " . count($allMembers));
        }

        // Adayları puanla: Uzmanlık eşleşmesi + Aktif yük dengesi
        $candidates = [];
        $fieldKeywords = $this->tokenizeField($fieldOfStudy);

        foreach ($allMembers as $member) {
            $expertiseKeywords = $this->tokenizeField($member['field_of_expertise']);
            $matchCount = count(array_intersect($fieldKeywords, $expertiseKeywords));
            
            // Puanlama Formülü:
            // Uzmanlık Eşleşmesi (+100 puan) - Aktif Dosya Yükü (-10 puan * aktif dosya sayısı)
            $score = ($matchCount * 100) - ($member['active_file_count'] * 10);

            $candidates[] = [
                'member' => $member,
                'score' => $score,
                'expertise_match' => ($matchCount > 0),
                'active_file_count' => (int)$member['active_file_count']
            ];
        }

        // Puanı yüksek olana göre sırala (Eşitlik durumunda aktif dosyası az olan öne geçer)
        usort($candidates, function ($a, $b) {
            if ($a['score'] === $b['score']) {
                return $a['active_file_count'] <=> $b['active_file_count'];
            }
            return $b['score'] <=> $a['score'];
        });

        // İlk $requiredReviewers kadar üyeyi seç
        $selectedCandidates = array_slice($candidates, 0, $requiredReviewers);
        $createdAssignments = [];

        foreach ($selectedCandidates as $cand) {
            $member = $cand['member'];
            $assignmentId = Assignment::create([
                'protocol_number' => $protocolNumber,
                'project_title' => $projectTitle,
                'field_of_study' => $fieldOfStudy,
                'member_id' => $member['id']
            ]);

            // Üyenin aktif dosya sayısını 1 artır
            CommitteeMember::incrementFileCount($member['id'], 1);

            $createdAssignments[] = [
                'assignment_id' => $assignmentId,
                'member_id' => $member['id'],
                'member_name' => $member['full_name'],
                'member_title' => $member['title'],
                'field_of_expertise' => $member['field_of_expertise'],
                'match_reason' => $cand['expertise_match'] ? 'Uzmanlık Eşleşmesi & Yük Dengesi' : 'Dengeli Dağıtım (Yedek Raportör)'
            ];
        }

        return [
            'status' => 'success',
            'protocol_number' => $protocolNumber,
            'assigned_count' => count($createdAssignments),
            'assignments' => $createdAssignments
        ];
    }

    private function tokenizeField(string $text): array {
        $clean = mb_strtolower(preg_replace('/[^\p{L}\p{N}\s]/u', ' ', $text), 'UTF-8');
        $words = preg_split('/\s+/', $clean, -1, PREG_SPLIT_NO_EMPTY);
        // Durak kelimeleri filtrele
        $stopWords = ['ve', 'ile', 'veya', 'bir', 'için', 'bilimleri', 'fakültesi'];
        return array_values(array_diff($words, $stopWords));
    }
}
