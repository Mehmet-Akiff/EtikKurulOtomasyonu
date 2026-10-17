namespace EtikKurul.BasvuruModulu.Models;

public enum ApplicationStatus
{
    Draft = 0,
    Submitted = 1,
    UnderReview = 2,
    RevisionRequested = 3,
    Approved = 4,
    Rejected = 5
}

public class Researcher
{
    public int Id { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty; // Prof. Dr., Doç. Dr., vb.
    public string Department { get; set; } = string.Empty;
    public string Institution { get; set; } = string.Empty;
    public string PhoneNumber { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ICollection<Application> Applications { get; set; } = new List<Application>();
}

public class ApplicationDocument
{
    public int Id { get; set; }
    public int ApplicationId { get; set; }
    public string DocumentType { get; set; } = string.Empty; // Onam Formu, Araştırma Protokolü vb.
    public string FileName { get; set; } = string.Empty;
    public string StoredFilePath { get; set; } = string.Empty;
    public string ContentType { get; set; } = string.Empty;
    public long FileSizeBytes { get; set; }
    public DateTime UploadedAt { get; set; } = DateTime.UtcNow;

    public Application? Application { get; set; }
}

public class Application
{
    public int Id { get; set; }
    public string ProtocolNumber { get; set; } = string.Empty; // ETIK-YYYY-XXXXX
    public int ResearcherId { get; set; }
    public Researcher? Researcher { get; set; }

    public string ProjectTitle { get; set; } = string.Empty;
    public string ResearchType { get; set; } = string.Empty; // Tez, Akademik Araştırma, Kurumsal Proje
    public string FieldOfStudy { get; set; } = string.Empty; // Tıp, Sosyal Bilimler, Eğitim, Mühendislik vb.
    public string Abstract { get; set; } = string.Empty;
    public string Methodology { get; set; } = string.Empty;
    public string TargetAudience { get; set; } = string.Empty;
    public int VolunteerCount { get; set; }
    public string RiskLevel { get; set; } = "Düşük"; // Düşük, Orta, Yüksek

    public ApplicationStatus Status { get; set; } = ApplicationStatus.Draft;
    public DateTime? SubmittedAt { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    public ICollection<ApplicationDocument> Documents { get; set; } = new List<ApplicationDocument>();
}
