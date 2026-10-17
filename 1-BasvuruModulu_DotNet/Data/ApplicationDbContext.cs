using Microsoft.EntityFrameworkCore;
using EtikKurul.BasvuruModulu.Models;

namespace EtikKurul.BasvuruModulu.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
    }

    public DbSet<Researcher> Researchers => Set<Researcher>();
    public DbSet<Application> Applications => Set<Application>();
    public DbSet<ApplicationDocument> ApplicationDocuments => Set<ApplicationDocument>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Researcher configurations
        modelBuilder.Entity<Researcher>(entity =>
        {
            entity.HasKey(r => r.Id);
            entity.Property(r => r.FullName).IsRequired().HasMaxLength(150);
            entity.Property(r => r.Email).IsRequired().HasMaxLength(150);
            entity.HasIndex(r => r.Email).IsUnique();
        });

        // Application configurations
        modelBuilder.Entity<Application>(entity =>
        {
            entity.HasKey(a => a.Id);
            entity.Property(a => a.ProtocolNumber).IsRequired().HasMaxLength(50);
            entity.HasIndex(a => a.ProtocolNumber).IsUnique();
            entity.Property(a => a.ProjectTitle).IsRequired().HasMaxLength(300);
            entity.Property(a => a.ResearchType).IsRequired().HasMaxLength(100);
            entity.Property(a => a.FieldOfStudy).IsRequired().HasMaxLength(100);

            entity.HasOne(a => a.Researcher)
                  .WithMany(r => r.Applications)
                  .HasForeignKey(a => a.ResearcherId)
                  .OnDelete(DeleteBehavior.Restrict);
        });

        // ApplicationDocument configurations
        modelBuilder.Entity<ApplicationDocument>(entity =>
        {
            entity.HasKey(d => d.Id);
            entity.Property(d => d.DocumentType).IsRequired().HasMaxLength(100);
            entity.Property(d => d.FileName).IsRequired().HasMaxLength(250);

            entity.HasOne(d => d.Application)
                  .WithMany(a => a.Documents)
                  .HasForeignKey(d => d.ApplicationId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

        // Seed initial data
        modelBuilder.Entity<Researcher>().HasData(
            new Researcher
            {
                Id = 1,
                FullName = "Dr. Deniz Kaya",
                Email = "deniz.kaya@universite.edu.tr",
                Title = "Dr. Öğr. Üyesi",
                Department = "Bilgisayar Mühendisliği",
                Institution = "Teknik Üniversite",
                PhoneNumber = "+90 555 123 4567",
                CreatedAt = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            },
            new Researcher
            {
                Id = 2,
                FullName = "Araş. Gör. Zeynep Çelik",
                Email = "zeynep.celik@universite.edu.tr",
                Title = "Araştırma Görevlisi (Doktora Adayı)",
                Department = "Klinik Psikoloji",
                Institution = "Devlet Üniversitesi",
                PhoneNumber = "+90 555 987 6543",
                CreatedAt = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            }
        );
    }
}
