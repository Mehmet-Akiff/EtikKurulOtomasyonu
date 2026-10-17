using Microsoft.EntityFrameworkCore;
using EtikKurul.BasvuruModulu.Data;
using EtikKurul.BasvuruModulu.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();

// Database configuration
var provider = builder.Configuration["DatabaseProvider"] ?? "SqlServer";
var mssqlConn = builder.Configuration.GetConnectionString("DefaultConnection");
var sqliteConn = builder.Configuration.GetConnectionString("SqliteConnection") ?? "Data Source=etikkurul.db";

builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    if (provider.Equals("SqlServer", StringComparison.OrdinalIgnoreCase))
    {
        try
        {
            options.UseSqlServer(mssqlConn);
        }
        catch
        {
            options.UseSqlite(sqliteConn);
        }
    }
    else
    {
        options.UseSqlite(sqliteConn);
    }
});

// Dependency Injection
builder.Services.AddScoped<IApplicationService, ApplicationService>();

// CORS configuration for cross-module communication
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Auto database creation and migration check
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    try
    {
        db.Database.EnsureCreated();
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[MSSQL Warning] Veritabanı başlatılırken hata oluştu: {ex.Message}. SQLite kullanılacak.");
    }
}

app.UseCors("AllowAll");
app.UseAuthorization();
app.MapControllers();

// Health check endpoint
app.MapGet("/", () => Results.Ok(new
{
    module = "Modül 1: Başvuru ve Belge Yönetimi",
    technology = "ASP.NET Core 9 + MSSQL",
    status = "Active",
    endpoints = new[]
    {
        "GET /api/researchers",
        "POST /api/researchers",
        "GET /api/applications",
        "POST /api/applications",
        "POST /api/applications/{id}/documents",
        "POST /api/applications/{id}/submit",
        "GET /api/applications/protocol/{protocolNumber}"
    }
}));

app.Run();
