using EtikKurul.BasvuruModulu.DTOs;
using EtikKurul.BasvuruModulu.Models;

namespace EtikKurul.BasvuruModulu.Services;

public interface IApplicationService
{
    Task<Researcher> CreateResearcherAsync(CreateResearcherDto dto);
    Task<List<Researcher>> GetAllResearchersAsync();
    Task<Researcher?> GetResearcherByIdAsync(int id);

    Task<ApplicationResponseDto> CreateApplicationAsync(CreateApplicationDto dto);
    Task<ApplicationResponseDto?> GetApplicationByIdAsync(int id);
    Task<ApplicationResponseDto?> GetApplicationByProtocolAsync(string protocolNumber);
    Task<List<ApplicationResponseDto>> GetAllApplicationsAsync(string? status = null);

    Task<DocumentResponseDto> UploadDocumentAsync(int applicationId, UploadDocumentDto dto);
    Task<ApplicationResponseDto> SubmitApplicationAsync(int applicationId);
    Task<ApplicationResponseDto> UpdateStatusAsync(int applicationId, UpdateStatusDto dto);
    Task<string> GenerateProtocolNumberAsync();
}
