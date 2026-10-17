<?php
// controllers/EvaluationController.php

require_once __DIR__ . '/../models/Evaluation.php';
require_once __DIR__ . '/../models/Assignment.php';
require_once __DIR__ . '/../models/CommitteeMember.php';

class EvaluationController {

    public function submitEvaluation(): void {
        $input = json_decode(file_get_contents('php://input'), true);
        if (!$input) {
            http_response_code(400);
            echo json_encode(['error' => 'Geçersiz JSON verisi.']);
            return;
        }

        $required = ['assignmentId', 'protocolNumber', 'memberId', 'methodologyScore', 'consentFormScore', 'riskAssessmentScore', 'decision', 'feedbackNotes'];
        foreach ($required as $f) {
            if (!isset($input[$f])) {
                http_response_code(400);
                echo json_encode(['error' => "Eksik alan: {$f}"]);
                return;
            }
        }

        $validDecisions = ['Approved', 'RevisionNeeded', 'Rejected'];
        if (!in_array($input['decision'], $validDecisions, true)) {
            http_response_code(400);
            echo json_encode(['error' => "Geçersiz karar türü. Kabul edilenler: " . implode(', ', $validDecisions)]);
            return;
        }

        try {
            $evalId = Evaluation::create([
                'assignment_id' => (int)$input['assignmentId'],
                'protocol_number' => $input['protocolNumber'],
                'member_id' => (int)$input['memberId'],
                'methodology_score' => (int)$input['methodologyScore'],
                'consent_form_score' => (int)$input['consentFormScore'],
                'risk_assessment_score' => (int)$input['riskAssessmentScore'],
                'decision' => $input['decision'],
                'feedback_notes' => $input['feedbackNotes']
            ]);

            // Görev durumunu tamamlandı olarak güncelle
            Assignment::updateStatus((int)$input['assignmentId'], 'Completed');

            // Üyenin aktif dosya sayısını 1 düşür
            CommitteeMember::decrementFileCount((int)$input['memberId'], 1);

            http_response_code(201);
            echo json_encode([
                'status' => 'success',
                'message' => 'Değerlendirme ve görüş başarıyla kaydedildi.',
                'evaluation_id' => $evalId
            ]);
        } catch (Throwable $e) {
            http_response_code(500);
            echo json_encode(['error' => $e->getMessage()]);
        }
    }

    public function getSummary(string $protocolNumber): void {
        $evaluations = Evaluation::findByProtocol($protocolNumber);
        $assignments = Assignment::findByProtocol($protocolNumber);

        $totalAssigned = count($assignments);
        $completedEvaluations = count($evaluations);

        $votes = [
            'Approved' => 0,
            'RevisionNeeded' => 0,
            'Rejected' => 0
        ];

        $totalScore = 0;
        foreach ($evaluations as $e) {
            if (isset($votes[$e['decision']])) {
                $votes[$e['decision']]++;
            }
            $avgIndividual = ($e['methodology_score'] + $e['consent_form_score'] + $e['risk_assessment_score']) / 3.0;
            $totalScore += $avgIndividual;
        }

        $overallAverage = ($completedEvaluations > 0) ? round($totalScore / $completedEvaluations, 2) : 0;

        // Karar tavsiyesi belirleme
        $consensusRecommendation = 'PendingReviews';
        if ($completedEvaluations >= $totalAssigned && $totalAssigned > 0) {
            if ($votes['Rejected'] > 0) {
                $consensusRecommendation = 'Rejected';
            } elseif ($votes['RevisionNeeded'] > 0) {
                $consensusRecommendation = 'RevisionNeeded';
            } else {
                $consensusRecommendation = 'Approved';
            }
        }

        echo json_encode([
            'protocol_number' => $protocolNumber,
            'total_assigned_reviewers' => $totalAssigned,
            'completed_reviews_count' => $completedEvaluations,
            'status' => ($completedEvaluations >= $totalAssigned && $totalAssigned > 0) ? 'AllReviewsCompleted' : 'AwaitingReviews',
            'consensus_recommendation' => $consensusRecommendation,
            'average_ethical_score' => $overallAverage,
            'votes_distribution' => $votes,
            'evaluations' => $evaluations
        ]);
    }
}
