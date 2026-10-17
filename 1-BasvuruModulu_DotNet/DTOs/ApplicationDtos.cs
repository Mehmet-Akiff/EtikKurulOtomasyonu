namespace EtikKurul.BasvuruModulu.DTOs;

public class CreateResearcherDto
{
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string Department { get; set; } = string.Empty;
    public string Institution { get; set; } = string.Empty;
    public string PhoneNumber { get; set; } = string.Empty;
}

public class CreateApplicationDto
{
    public int ResearcherId { get; set; }
    public string ProjectTitle { get; set; } = string.Empty;
    public string ResearchType { get; set; } = string.Empty; // Tez, Akademik Araştırma, Kurumsal Proje
    public string FieldOfStudy { get; set; } = string.Empty; // Tıp, Biyoloji, Psikoloji, Eğitim, Mühendislik
    public string Abstract { get; set; } = string.Empty;
    public string Methodology { get; set; } = string.Empty;
    public string TargetAudience { get; set; } = string.Empty;
    public int VolunteerCount { get; set; }
    public string RiskLevel { get; set; } = "Düşük";
}

public class UploadDocumentDto
{
    public string DocumentType { get; set; } = string.Empty; // Onam Formu, Araştırma Protokolü, Anket/Ölçek
    public string FileName { get; set; } = string.Empty;
    public string FileBase64 { get; set; } = string.Empty;
    public string ContentType { get; set; } = "application/pdf";
}

public class UpdateStatusDto
{
    public string Status { get; set; } = string.Empty; // Submitted, UnderReview, RevisionRequested, Approved, Rejected
    public string? Note { get; set; }
}

public class DocumentResponseDto
{
    public int Id { get; set; }
    public string DocumentType { get; set; } = string.Empty;
    public string FileName { get; set; } = string.Empty;
    public long FileSizeBytes { get; set; }
    public DateTime UploadedAt { get; set; }
}

public class ApplicationResponseDto
{
    public int Id { get; set; }
    public string ProtocolNumber { get; set; } = string.Empty;
    public int ResearcherId { get; set; }
    public string ResearcherName { get; set; } = string.Empty;
    public string ResearcherEmail { get; set; } = string.Empty;
    public string ProjectTitle { get; set; } = string.Empty;
    public string ResearchType { get; set; } = string.Empty;
    public string FieldOfStudy { get; set; } = string.Empty;
    public string Abstract { get; set; } = string.Empty;
    public string Methodology { get; set; } = string.Empty;
    public string TargetAudience { get; set; } = string.Empty;
    public int VolunteerCount { get; set; }
    public string RiskLevel { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public DateTime? SubmittedAt { get; set; }
    public DateTime CreatedAt { get; set; }
    public List<DocumentResponseDto> Documents { get; set; } = new();
}
