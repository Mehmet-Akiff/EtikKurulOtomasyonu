using Microsoft.EntityFrameworkCore;
using EtikKurul.BasvuruModulu.Data;
using EtikKurul.BasvuruModulu.DTOs;
using EtikKurul.BasvuruModulu.Models;
using EtikKurul.BasvuruModulu.Services;
using Xunit;

namespace EtikKurul.BasvuruModulu.Tests;

public class ApplicationServiceTests
{
    private ApplicationDbContext CreateInMemoryDbContext(string dbName)
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(databaseName: dbName)
            .Options;

        var db = new ApplicationDbContext(options);
        db.Database.EnsureCreated();
        return db;
    }

    [Fact]
    public async Task CreateApplication_ShouldGenerateProtocolNumber_AndSetDraftStatus()
    {
        // Arrange
        using var db = CreateInMemoryDbContext("TestDb_CreateApp");
        var service = new ApplicationService(db);

        var researcher = await service.CreateResearcherAsync(new CreateResearcherDto
        {
            FullName = "Prof. Dr. Ahmet Yılmaz",
            Email = "ahmet.yilmaz@test.edu.tr",
            Title = "Prof. Dr.",
            Department = "Tıp Fakültesi",
            Institution = "Ege Üniversitesi"
        });

        var dto = new CreateApplicationDto
        {
            ResearcherId = researcher.Id,
            ProjectTitle = "Yapay Zeka Destekli Biyosensörlerin Etik İncelemesi",
            ResearchType = "Akademik Araştırma",
            FieldOfStudy = "Biyomedikal / Tıp",
            Abstract = "Bu araştırma yeni nesil biyosensörlerin hasta verisi gizliliğini inceler.",
            Methodology = "Çift kör klinik anket ve laboratuvar testi.",
            TargetAudience = "Yetişkin gönüllüler (18-65 yaş)",
            VolunteerCount = 120,
            RiskLevel = "Düşük"
        };

        // Act
        var result = await service.CreateApplicationAsync(dto);

        // Assert
        Assert.NotNull(result);
        Assert.StartsWith("ETIK-", result.ProtocolNumber);
        Assert.Equal("Draft", result.Status);
        Assert.Equal(dto.ProjectTitle, result.ProjectTitle);
        Assert.Equal(researcher.FullName, result.ResearcherName);
    }

    [Fact]
    public async Task SubmitApplication_WithoutDocuments_ShouldThrowInvalidOperationException()
    {
        // Arrange
        using var db = CreateInMemoryDbContext("TestDb_SubmitWithoutDocs");
        var service = new ApplicationService(db);

        var researcher = await service.CreateResearcherAsync(new CreateResearcherDto
        {
            FullName = "Dr. Elif Demir",
            Email = "elif.demir@test.edu.tr"
        });

        var app = await service.CreateApplicationAsync(new CreateApplicationDto
        {
            ResearcherId = researcher.Id,
            ProjectTitle = "Klinik Öncesi İlaç Deneyleri Etik Analizi",
            ResearchType = "Tez",
            FieldOfStudy = "Eczacılık"
        });

        // Act & Assert: Belgesiz başvuru gönderilemez
        await Assert.ThrowsAsync<InvalidOperationException>(() => service.SubmitApplicationAsync(app.Id));
    }

    [Fact]
    public async Task SubmitApplication_WithDocuments_ShouldSetStatusToSubmitted()
    {
        // Arrange
        using var db = CreateInMemoryDbContext("TestDb_SubmitWithDocs");
        var service = new ApplicationService(db);

        var researcher = await service.CreateResearcherAsync(new CreateResearcherDto
        {
            FullName = "Doç. Dr. Barış Akın",
            Email = "baris.akin@test.edu.tr"
        });

        var app = await service.CreateApplicationAsync(new CreateApplicationDto
        {
            ResearcherId = researcher.Id,
            ProjectTitle = "Sosyal Medya Kullanımının Ergen Gelişimi Üzerine Etkileri",
            ResearchType = "Tez",
            FieldOfStudy = "Psikoloji"
        });

        // Belge yükle
        await service.UploadDocumentAsync(app.Id, new UploadDocumentDto
        {
            DocumentType = "Bilgilendirilmiş Onam Formu",
            FileName = "onam_formu.pdf",
            ContentType = "application/pdf"
        });

        await service.UploadDocumentAsync(app.Id, new UploadDocumentDto
        {
            DocumentType = "Araştırma Protokolü",
            FileName = "arastirma_protokolu.pdf",
            ContentType = "application/pdf"
        });

        // Act
        var submitted = await service.SubmitApplicationAsync(app.Id);

        // Assert
        Assert.Equal("Submitted", submitted.Status);
        Assert.NotNull(submitted.SubmittedAt);
        Assert.Equal(2, submitted.Documents.Count);
    }

    [Fact]
    public async Task UpdateStatus_ShouldUpdateApplicationStatusProperly()
    {
        // Arrange
        using var db = CreateInMemoryDbContext("TestDb_UpdateStatus");
        var service = new ApplicationService(db);

        var researcher = await service.CreateResearcherAsync(new CreateResearcherDto
        {
            FullName = "Dr. Merve Şen",
            Email = "merve.sen@test.edu.tr"
        });

        var app = await service.CreateApplicationAsync(new CreateApplicationDto
        {
            ResearcherId = researcher.Id,
            ProjectTitle = "Eğitimde Oyunlaştırma Projesi",
            ResearchType = "Kurumsal Proje",
            FieldOfStudy = "Eğitim Bilimleri"
        });

        // Act
        var updated = await service.UpdateStatusAsync(app.Id, new UpdateStatusDto { Status = "UnderReview" });

        // Assert
        Assert.Equal("UnderReview", updated.Status);
    }
}
