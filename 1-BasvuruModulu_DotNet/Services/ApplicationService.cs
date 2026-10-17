using Microsoft.EntityFrameworkCore;
using EtikKurul.BasvuruModulu.Data;
using EtikKurul.BasvuruModulu.DTOs;
using EtikKurul.BasvuruModulu.Models;

namespace EtikKurul.BasvuruModulu.Services;

public class ApplicationService : IApplicationService
{
    private readonly ApplicationDbContext _db;
    private readonly string _uploadFolder;

    public ApplicationService(ApplicationDbContext db)
    {
        _db = db;
        _uploadFolder = Path.Combine(AppContext.BaseDirectory, "uploads");
        if (!Directory.Exists(_uploadFolder))
        {
            Directory.CreateDirectory(_uploadFolder);
        }
    }

    public async Task<Researcher> CreateResearcherAsync(CreateResearcherDto dto)
    {
        var existing = await _db.Researchers.FirstOrDefaultAsync(r => r.Email.ToLower() == dto.Email.ToLower());
        if (existing != null)
        {
            return existing;
        }

        var researcher = new Researcher
        {
            FullName = dto.FullName,
            Email = dto.Email,
            Title = dto.Title,
            Department = dto.Department,
            Institution = dto.Institution,
            PhoneNumber = dto.PhoneNumber,
            CreatedAt = DateTime.UtcNow
        };

        _db.Researchers.Add(researcher);
        await _db.SaveChangesAsync();
        return researcher;
    }

    public async Task<List<Researcher>> GetAllResearchersAsync()
    {
        return await _db.Researchers.AsNoTracking().ToListAsync();
    }

    public async Task<Researcher?> GetResearcherByIdAsync(int id)
    {
        return await _db.Researchers.FindAsync(id);
    }

    public async Task<ApplicationResponseDto> CreateApplicationAsync(CreateApplicationDto dto)
    {
        var researcher = await _db.Researchers.FindAsync(dto.ResearcherId);
        if (researcher == null)
        {
            throw new ArgumentException($"ID'si {dto.ResearcherId} olan araştırmacı bulunamadı.");
        }

        var protocolNumber = await GenerateProtocolNumberAsync();

        var app = new Application
        {
            ProtocolNumber = protocolNumber,
            ResearcherId = dto.ResearcherId,
            ProjectTitle = dto.ProjectTitle,
            ResearchType = dto.ResearchType,
            FieldOfStudy = dto.FieldOfStudy,
            Abstract = dto.Abstract,
            Methodology = dto.Methodology,
            TargetAudience = dto.TargetAudience,
            VolunteerCount = dto.VolunteerCount,
            RiskLevel = string.IsNullOrWhiteSpace(dto.RiskLevel) ? "Düşük" : dto.RiskLevel,
            Status = ApplicationStatus.Draft,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        _db.Applications.Add(app);
        await _db.SaveChangesAsync();

        return MapToDto(app, researcher);
    }

    public async Task<ApplicationResponseDto?> GetApplicationByIdAsync(int id)
    {
        var app = await _db.Applications
            .Include(a => a.Researcher)
            .Include(a => a.Documents)
            .FirstOrDefaultAsync(a => a.Id == id);

        return app == null ? null : MapToDto(app, app.Researcher!);
    }

    public async Task<ApplicationResponseDto?> GetApplicationByProtocolAsync(string protocolNumber)
    {
        var app = await _db.Applications
            .Include(a => a.Researcher)
            .Include(a => a.Documents)
            .FirstOrDefaultAsync(a => a.ProtocolNumber == protocolNumber);

        return app == null ? null : MapToDto(app, app.Researcher!);
    }

    public async Task<List<ApplicationResponseDto>> GetAllApplicationsAsync(string? status = null)
    {
        var query = _db.Applications
            .Include(a => a.Researcher)
            .Include(a => a.Documents)
            .AsNoTracking()
            .AsQueryable();

        if (!string.IsNullOrEmpty(status) && Enum.TryParse<ApplicationStatus>(status, true, out var parsedStatus))
        {
            query = query.Where(a => a.Status == parsedStatus);
        }

        var list = await query.OrderByDescending(a => a.CreatedAt).ToListAsync();
        return list.Select(a => MapToDto(a, a.Researcher!)).ToList();
    }

    public async Task<DocumentResponseDto> UploadDocumentAsync(int applicationId, UploadDocumentDto dto)
    {
        var app = await _db.Applications.FindAsync(applicationId);
        if (app == null)
        {
            throw new ArgumentException($"Başvuru #{applicationId} bulunamadı.");
        }

        string storedFileName = $"{app.ProtocolNumber}_{Guid.NewGuid():N}_{dto.FileName}";
        string filePath = Path.Combine(_uploadFolder, storedFileName);

        if (!string.IsNullOrEmpty(dto.FileBase64))
        {
            var bytes = Convert.FromBase64String(dto.FileBase64);
            await File.WriteAllBytesAsync(filePath, bytes);
        }
        else
        {
            // Empty placeholder file if binary not provided
            await File.WriteAllTextAsync(filePath, $"Document Placeholder for {dto.FileName}");
        }

        var fileInfo = new FileInfo(filePath);

        var doc = new ApplicationDocument
        {
            ApplicationId = applicationId,
            DocumentType = dto.DocumentType,
            FileName = dto.FileName,
            StoredFilePath = filePath,
            ContentType = dto.ContentType,
            FileSizeBytes = fileInfo.Length,
            UploadedAt = DateTime.UtcNow
        };

        _db.ApplicationDocuments.Add(doc);
        app.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        return new DocumentResponseDto
        {
            Id = doc.Id,
            DocumentType = doc.DocumentType,
            FileName = doc.FileName,
            FileSizeBytes = doc.FileSizeBytes,
            UploadedAt = doc.UploadedAt
        };
    }

    public async Task<ApplicationResponseDto> SubmitApplicationAsync(int applicationId)
    {
        var app = await _db.Applications
            .Include(a => a.Researcher)
            .Include(a => a.Documents)
            .FirstOrDefaultAsync(a => a.Id == applicationId);

        if (app == null)
        {
            throw new ArgumentException($"Başvuru #{applicationId} bulunamadı.");
        }

        if (app.Documents.Count == 0)
        {
            throw new InvalidOperationException("Başvuru gönderilmeden önce en az bir belge (Araştırma Protokolü / Onam Formu vb.) yüklenmelidir.");
        }

        app.Status = ApplicationStatus.Submitted;
        app.SubmittedAt = DateTime.UtcNow;
        app.UpdatedAt = DateTime.UtcNow;

        await _db.SaveChangesAsync();

        return MapToDto(app, app.Researcher!);
    }

    public async Task<ApplicationResponseDto> UpdateStatusAsync(int applicationId, UpdateStatusDto dto)
    {
        var app = await _db.Applications
            .Include(a => a.Researcher)
            .Include(a => a.Documents)
            .FirstOrDefaultAsync(a => a.Id == applicationId);

        if (app == null)
        {
            throw new ArgumentException($"Başvuru #{applicationId} bulunamadı.");
        }

        if (Enum.TryParse<ApplicationStatus>(dto.Status, true, out var newStatus))
        {
            app.Status = newStatus;
            app.UpdatedAt = DateTime.UtcNow;
            await _db.SaveChangesAsync();
        }
        else
        {
            throw new ArgumentException($"Geçersiz durum değeri: {dto.Status}");
        }

        return MapToDto(app, app.Researcher!);
    }

    public async Task<string> GenerateProtocolNumberAsync()
    {
        var year = DateTime.UtcNow.Year;
        var countThisYear = await _db.Applications
            .CountAsync(a => a.CreatedAt.Year == year);

        return $"ETIK-{year}-{(countThisYear + 1):D5}";
    }

    private static ApplicationResponseDto MapToDto(Application app, Researcher researcher)
    {
        return new ApplicationResponseDto
        {
            Id = app.Id,
            ProtocolNumber = app.ProtocolNumber,
            ResearcherId = app.ResearcherId,
            ResearcherName = researcher?.FullName ?? string.Empty,
            ResearcherEmail = researcher?.Email ?? string.Empty,
            ProjectTitle = app.ProjectTitle,
            ResearchType = app.ResearchType,
            FieldOfStudy = app.FieldOfStudy,
            Abstract = app.Abstract,
            Methodology = app.Methodology,
            TargetAudience = app.TargetAudience,
            VolunteerCount = app.VolunteerCount,
            RiskLevel = app.RiskLevel,
            Status = app.Status.ToString(),
            SubmittedAt = app.SubmittedAt,
            CreatedAt = app.CreatedAt,
            Documents = app.Documents.Select(d => new DocumentResponseDto
            {
                Id = d.Id,
                DocumentType = d.DocumentType,
                FileName = d.FileName,
                FileSizeBytes = d.FileSizeBytes,
                UploadedAt = d.UploadedAt
            }).ToList()
        };
    }
}
